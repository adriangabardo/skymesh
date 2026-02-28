from datetime import datetime
from pathlib import Path

from providers.openflights import OpenFlightsProvider
from search.engine import find_flight_routes


def main() -> None:
    data_dir = Path("./data")

    # Instantiate data provider (OpenFlights-backed)
    provider = OpenFlightsProvider(data_dir)

    print("Skymesh provider loaded")
    print(f"Airports loaded: {len(provider.airports)}")
    print(f"Origins with outbound routes: {len(provider.adjacency)}")

    # 1 March 2026 at 08:00 (08:00 AM local time)
    departure_time = datetime(2026, 3, 1, 8, 0)

    airport_pairs = [
        ("SYD", "MEL"),
        ("YYC", "SYD"),
        ("LHR", "JFK"),
        ("CDG", "DXB"),
        ("JFK", "SYD"),
    ]

    for origin, destination in airport_pairs:
        print("\n" + "=" * 60)
        print(f"Searching routes: {origin} -> {destination}")

        routes = find_flight_routes(
            origin=origin,
            destination=destination,
            provider=provider,
            departure_time=departure_time,
            max_legs=3,
            max_routes=5,
        )

        if not routes:
            print("No routes found.")
            continue

        routes = sorted(routes, key=lambda r: r.total_trip_time)

        for route in routes:
            # Toggle between "code" and "name"
            print(route.to_string(airline_format="name", airport_format="iata"))
            print()

    print("\nSearch complete.")


if __name__ == "__main__":
    main()
