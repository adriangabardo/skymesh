from __future__ import annotations

from datetime import datetime

import msgspec


class Flight(msgspec.Struct, frozen=True):
    flight_id: str

    # IATA identifiers
    origin: str
    destination: str

    # Resolved airport metadata
    origin_name: str
    origin_city: str
    origin_country: str

    destination_name: str
    destination_city: str
    destination_country: str

    # Time-aware fields
    departure_time: datetime
    arrival_time: datetime

    # Airline metadata
    airline_code: str
    airline_name: str
