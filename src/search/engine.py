from __future__ import annotations

from datetime import datetime
from typing import List

from entities.flight import Flight
from entities.flight_route import FlightRoute
from entities.price import Price
from providers.base import FlightDataProvider
from search.constraints import is_connection_time_valid


def find_flight_routes(
    *,
    origin: str,
    destination: str,
    provider: FlightDataProvider,
    departure_time: datetime,
    max_legs: int = 3,
    max_routes: int = 10,
) -> List[FlightRoute]:
    """
    Iterative Deepening DFS (IDDFS) search.

    - Depth (legs) is the primary ordering.
    - Within each depth, routes are sorted by total duration.
    - max_routes is respected globally.
    """

    final_results: List[FlightRoute] = []

    # ------------------------------------------------------------------
    # Iterate depth-first by hop count (IDDFS)
    # ------------------------------------------------------------------

    for depth_limit in range(1, max_legs + 1):

        depth_results: List[FlightRoute] = []

        def dfs(
            current_airport: str,
            current_time: datetime,
            path: List[Flight],
        ) -> None:

            # Stop exploring deeper than current depth limit
            if len(path) > depth_limit:
                return

            # Destination reached at this depth
            if path and current_airport == destination:

                route = FlightRoute(flights=tuple(path))
                price: Price = provider.price_route(route)

                priced_route = FlightRoute(
                    flights=route.flights,
                    price=price,
                )

                depth_results.append(priced_route)
                return

            # Continue exploring
            outbound_flights = provider.get_outbound_flights(
                origin=current_airport,
                departure_time=current_time,
            )

            for flight in outbound_flights:

                # Avoid cycles
                visited_airports = {f.origin for f in path}
                if flight.destination in visited_airports:
                    continue

                # Validate connection time
                if path:
                    previous_flight = path[-1]
                    if not is_connection_time_valid(
                        previous_arrival=previous_flight.arrival_time,
                        next_departure=flight.departure_time,
                    ):
                        continue

                dfs(
                    current_airport=flight.destination,
                    current_time=flight.arrival_time,
                    path=path + [flight],
                )

        # Run DFS for this depth
        dfs(
            current_airport=origin,
            current_time=departure_time,
            path=[],
        )

        # --------------------------------------------------------------
        # Sort ONCE per depth by total trip time
        # --------------------------------------------------------------

        depth_results.sort(key=lambda r: r.total_trip_time)

        # Add best from this depth to final results
        for route in depth_results:
            if len(final_results) >= max_routes:
                return final_results
            final_results.append(route)

        # If we already have enough routes, stop deepening
        if len(final_results) >= max_routes:
            break

    return final_results
