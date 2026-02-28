from __future__ import annotations

import csv
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

import msgspec

from entities.flight import Flight
from entities.flight_route import FlightRoute
from entities.price import Price
from providers.base import FlightDataProvider
from constants import (
    EARTH_RADIUS_KM,
    GROUND_BUFFER_MINUTES,
    DEFAULT_CRUISE_SPEED,
    AIRCRAFT_SPEED_KMH,
    BASE_FARE_PER_LEG,
    PRICE_PER_KM,
    LAYOVER_PENALTY_PER_HOUR,
    DEFAULT_CURRENCY,
)


class _RouteTemplate(msgspec.Struct, frozen=True):
    origin: str
    destination: str
    airline_code: str
    equipment: tuple[str, ...]


class OpenFlightsProvider(FlightDataProvider):

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

        self.airports: Dict[str, dict] = {}
        self.airlines: Dict[str, str] = {}
        self.adjacency: Dict[str, List[_RouteTemplate]] = {}

        self._load_airports()
        self._load_airlines()
        self._load_routes()

    # ---------------------------------------------------------------------
    # Data Loading
    # ---------------------------------------------------------------------

    def _load_airports(self) -> None:
        with (self.data_dir / "airports.dat").open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                iata = row[4]
                if iata == "\\N" or not iata:
                    continue

                tz_offset = float(row[9]) if row[9] != "\\N" else 0.0

                self.airports[iata] = {
                    "name": row[1],
                    "city": row[2],
                    "country": row[3],
                    "latitude": float(row[6]),
                    "longitude": float(row[7]),
                    "timezone": timezone(timedelta(hours=tz_offset)),
                }

    def _load_airlines(self) -> None:
        with (self.data_dir / "airlines.dat").open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                name = row[1]
                code = row[3]
                if code != "\\N" and code:
                    self.airlines[code] = name

    def _load_routes(self) -> None:
        with (self.data_dir / "routes.dat").open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                origin = row[2]
                destination = row[4]
                airline_code = row[0]
                stops = row[7]

                if (
                    origin == "\\N"
                    or destination == "\\N"
                    or origin not in self.airports
                    or destination not in self.airports
                    or stops != "0"
                ):
                    continue

                template = _RouteTemplate(
                    origin=origin,
                    destination=destination,
                    airline_code=airline_code,
                    equipment=tuple(row[8].split()) if row[8] != "\\N" else (),
                )

                self.adjacency.setdefault(origin, []).append(template)

    # ---------------------------------------------------------------------
    # Public Interface
    # ---------------------------------------------------------------------

    def get_outbound_flights(
        self,
        *,
        origin: str,
        departure_time: datetime,
    ) -> List[Flight]:

        templates = self.adjacency.get(origin, [])
        return [
            self._instantiate_flight(template, departure_time) for template in templates
        ]

    def price_route(self, route: FlightRoute) -> Price:
        base_total = 0.0
        distance_total = 0.0
        layover_total = 0.0

        for flight in route.flights:
            origin_meta = self.airports[flight.origin]
            dest_meta = self.airports[flight.destination]

            distance_km = self._haversine_km(
                origin_meta["latitude"],
                origin_meta["longitude"],
                dest_meta["latitude"],
                dest_meta["longitude"],
            )

            base_total += BASE_FARE_PER_LEG
            distance_total += distance_km * PRICE_PER_KM

        for layover in route.layovers:
            hours = layover.total_seconds() / 3600
            layover_total += hours * LAYOVER_PENALTY_PER_HOUR

        total = base_total + distance_total + layover_total

        return Price(
            amount=round(total, 2),
            currency=DEFAULT_CURRENCY,
            breakdown_base=round(base_total, 2),
            breakdown_distance=round(distance_total, 2),
            breakdown_layover=round(layover_total, 2),
        )

    # ---------------------------------------------------------------------
    # Flight Instantiation
    # ---------------------------------------------------------------------

    def _instantiate_flight(
        self,
        template: _RouteTemplate,
        requested_departure: datetime,
    ) -> Flight:

        origin_meta = self.airports[template.origin]
        dest_meta = self.airports[template.destination]

        origin_tz = origin_meta["timezone"]
        dest_tz = dest_meta["timezone"]

        departure_local = self._next_departure_at_nine(
            requested_departure,
            origin_tz,
        )

        distance_km = self._haversine_km(
            origin_meta["latitude"],
            origin_meta["longitude"],
            dest_meta["latitude"],
            dest_meta["longitude"],
        )

        cruise_speed = self._resolve_cruise_speed(template.equipment)

        cruise_minutes = (distance_km / cruise_speed) * 60
        total_minutes = cruise_minutes + GROUND_BUFFER_MINUTES
        duration = timedelta(minutes=total_minutes)

        departure_utc = departure_local.astimezone(timezone.utc)
        arrival_utc = departure_utc + duration
        arrival_local = arrival_utc.astimezone(dest_tz)

        airline_name = self.airlines.get(
            template.airline_code,
            template.airline_code,
        )

        flight_id = (
            f"{template.airline_code}-" f"{template.origin}-" f"{template.destination}"
        )

        return Flight(
            flight_id=flight_id,
            origin=template.origin,
            destination=template.destination,
            origin_name=origin_meta["name"],
            origin_city=origin_meta["city"],
            origin_country=origin_meta["country"],
            destination_name=dest_meta["name"],
            destination_city=dest_meta["city"],
            destination_country=dest_meta["country"],
            departure_time=departure_local,
            arrival_time=arrival_local,
            airline_code=template.airline_code,
            airline_name=airline_name,
        )

    # ---------------------------------------------------------------------

    def _next_departure_at_nine(
        self,
        requested_departure: datetime,
        origin_tz,
    ) -> datetime:

        local_time = requested_departure.astimezone(origin_tz)

        candidate = local_time.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0,
        )

        if candidate <= local_time:
            candidate += timedelta(days=1)

        return candidate

    def _resolve_cruise_speed(self, equipment: tuple[str, ...]) -> float:
        for eq in equipment:
            if eq in AIRCRAFT_SPEED_KMH:
                return AIRCRAFT_SPEED_KMH[eq]
        return DEFAULT_CRUISE_SPEED

    def _haversine_km(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return EARTH_RADIUS_KM * c
