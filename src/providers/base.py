from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from entities.flight import Flight
from entities.flight_route import FlightRoute
from entities.price import Price


class FlightDataProvider(ABC):
    """
    Abstract interface for any flight data source.

    A provider is responsible for generating outbound Flight objects
    for a given airport and departure time.

    The search engine depends only on this contract.
    """

    @abstractmethod
    def get_outbound_flights(
        self,
        *,
        origin: str,
        departure_time: datetime,
    ) -> List[Flight]:
        """
        Return all flights departing from `origin`
        at or after `departure_time`.
        """
        raise NotImplementedError

    @abstractmethod
    def price_route(self, route: FlightRoute) -> Price:
        raise NotImplementedError
