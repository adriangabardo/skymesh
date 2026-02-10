import msgspec
from datetime import datetime, timedelta


class Flight(msgspec.Struct, frozen=True):
    flight_id: str

    origin: str
    destination: str

    departure_time: datetime
    arrival_time: datetime

    @property
    def duration(self) -> timedelta:
        return self.arrival_time - self.departure_time
