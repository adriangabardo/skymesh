import json
import networkx as nx
from entities.flight import Flight
from entities.flight_route import FlightRoute
from datetime import datetime, timedelta

MAX_ALLOWED_LEGS = 4  # Hardcoded limit so user-input can't blow up the search algo
MIN_CONNECTION_TIME = timedelta(minutes=45)


def find_flight_routes(
    *,
    origin: str,
    destination: str,
    graph: nx.DiGraph,
    max_legs: int,
    min_routes: int = 3,
    max_routes: int = 15,
) -> list[FlightRoute]:
    """
    Enumerate viable flight routes as graph paths between two airports.

    This function treats the flight network as a directed graph and returns
    sequences of flights (routes) that connect the given origin airport to the
    destination airport. At this stage, routes are purely structural: temporal
    feasibility, pricing, and optimisation are intentionally ignored.

    The search is performed using a progressive deepening strategy over path
    length (number of legs). All direct routes are explored first, followed by
    two-leg routes, then three-leg routes, and so on, up to a specified maximum.
    The search terminates early once a minimum number of routes has been found,
    or immediately if a hard maximum on returned routes is reached.

    Cycles are prevented by disallowing revisits to the same airport within a
    single route.

    Parameters
    ----------
    origin : str
        IATA airport code representing the starting point of the route search.

    destination : str
        IATA airport code representing the final destination of the route search.

    graph : nx.DiGraph
        Directed graph representing the flight network. Nodes are airports and
        directed edges represent possible direct connections between airports.
        Edge attributes are ignored at this stage.

    max_legs : int
        Maximum number of flight legs allowed in a route. This value is capped
        internally to a small hard limit to prevent pathological searches.

    min_routes : int, optional
        Minimum number of routes to find before terminating the search early.
        Defaults to 1.

    max_routes : int, optional
        Hard upper bound on the number of routes returned. Once this limit is
        reached, the search stops immediately. Defaults to 15.

    Returns
    -------
    list[FlightRoute]
        A list of `FlightRoute` objects, each representing a unique path through
        the graph from origin to destination.
    """

    max_legs = min(max_legs, MAX_ALLOWED_LEGS)
    assert max_legs >= 1
    assert min_routes >= 1
    assert max_routes >= 1

    routes: list[FlightRoute] = []

    def dfs_exact_legs(
        current_airport: str,
        target_legs: int,
        path: tuple[Flight, ...],
        visited: set[str],
    ) -> None:
        # Global hard stop
        if len(routes) >= max_routes:
            return

        if len(path) > target_legs:
            return

        if len(path) == target_legs:
            if current_airport == destination:
                routes.append(FlightRoute(path))
            return

        for _, next_airport, _ in graph.out_edges(current_airport, data=True):
            if next_airport in visited:
                continue

            flight = Flight(
                flight_id=f"{current_airport}->{next_airport}",
                origin=current_airport,
                destination=next_airport,
                departure_time=datetime.min,
                arrival_time=datetime.min,
            )

            dfs_exact_legs(
                next_airport,
                target_legs,
                path + (flight,),
                visited | {next_airport},
            )

            if len(routes) >= max_routes:
                return

    # Progressive deepening by leg count
    for legs in range(1, max_legs + 1):
        dfs_exact_legs(
            origin,
            target_legs=legs,
            path=(),
            visited={origin},
        )

        if len(routes) >= min_routes:
            break

    metadata = {
        "origin": origin,
        "destination": destination,
        "max_legs": max_legs,
        "min_routes": min_routes,
        "max_routes": max_routes,
        "routes_found": len(routes),
    }

    print("Search for flight routes complete. \n", json.dumps(metadata, indent=4))

    return routes
