from datetime import timedelta
import msgspec

from entities.flight import Flight


class FlightRoute(msgspec.Struct, frozen=True):
    flights: tuple[Flight, ...]

    @property
    def origin(self) -> str:
        return self.flights[0].origin

    @property
    def destination(self) -> str:
        return self.flights[-1].destination

    @property
    def legs(self) -> int:
        return len(self.flights)

    def __str__(self) -> str:
        airports = [self.origin] + [f.destination for f in self.flights]
        path = " -> ".join(airports)
        return f"{path} ({self.legs} legs)"

    def __repr__(self) -> str:
        airports = [self.origin] + [f.destination for f in self.flights]
        path = " -> ".join(airports)
        return f"FlightRoute(" f"path='{path}', " f"legs={self.legs}" f")"
