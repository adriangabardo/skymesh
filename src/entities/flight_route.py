from __future__ import annotations

from datetime import timedelta
from typing import Tuple, Optional

import msgspec

from entities.flight import Flight
from entities.price import Price


class FlightRoute(msgspec.Struct, frozen=True):
    flights: Tuple[Flight, ...]
    price: Optional[Price] = None

    # ---------------------------------------------------------------------
    # Core Properties
    # ---------------------------------------------------------------------

    @property
    def origin(self) -> str:
        return self.flights[0].origin

    @property
    def destination(self) -> str:
        return self.flights[-1].destination

    @property
    def legs(self) -> int:
        return len(self.flights)

    # ---------------------------------------------------------------------
    # Time Properties
    # ---------------------------------------------------------------------

    @property
    def departure_time(self):
        return self.flights[0].departure_time

    @property
    def arrival_time(self):
        return self.flights[-1].arrival_time

    @property
    def total_trip_time(self) -> timedelta:
        return self.arrival_time - self.departure_time

    @property
    def layovers(self) -> Tuple[timedelta, ...]:
        if len(self.flights) <= 1:
            return ()

        layovers = []
        for i in range(1, len(self.flights)):
            previous = self.flights[i - 1]
            current = self.flights[i]
            layovers.append(current.departure_time - previous.arrival_time)

        return tuple(layovers)

    # ---------------------------------------------------------------------
    # Presentation
    # ---------------------------------------------------------------------

    def to_string(
        self,
        airline_format: str = "code",
        airport_format: str = "iata",
    ) -> str:

        lines = []

        header = (
            f"{self.origin} -> {self.destination} "
            f"({self.legs} legs, total {self._format_td(self.total_trip_time)})"
        )

        lines.append(header)

        for i, flight in enumerate(self.flights):

            airline_display = (
                flight.airline_name if airline_format == "name" else flight.airline_code
            )

            origin_display = (
                f"{flight.origin_name} ({flight.origin})"
                if airport_format == "full"
                else flight.origin
            )

            destination_display = (
                f"{flight.destination_name} ({flight.destination})"
                if airport_format == "full"
                else flight.destination
            )

            leg_line = "\n\t".join(
                [
                    f"Leg {i + 1}: {origin_display} -> {destination_display}",
                    f"Airline: {airline_display}",
                    f"Dep: {flight.departure_time.strftime('%-I:%M %p, %d-%m-%Y (%Z)')}",
                    f"Arr: {flight.arrival_time.strftime('%-I:%M %p, %d-%m-%Y (%Z)')}",
                ]
            )

            lines.append("\t" + leg_line)

            if i < len(self.layovers):
                layover = self.layovers[i]
                lines.append(f"\n\tLayover: {self._format_td(layover)}\n")

        if self.price:
            lines.append(f"\n\tTotal Price: {self.price}\n")

        return "\n".join(lines)

    def __str__(self) -> str:
        return self.to_string()

    @staticmethod
    def _format_td(td: timedelta) -> str:
        total_minutes = int(td.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}h {minutes}m"
