import json
from graph_build import build_graph
from services.path_finder import find_flight_routes
from graph_viz import draw_geographic_projection


def main() -> None:
    graph = build_graph()

    print("Skymesh graph loaded")
    print(f"Airports (nodes): {graph.number_of_nodes()}")
    print(f"Routes (edges): {graph.number_of_edges()}")

    # print("\nSample airport:")
    # sample_node = next(iter(graph.nodes))
    # print(sample_node, json.dumps(graph.nodes[sample_node], indent=4, sort_keys=False))

    # print("\nSample route:")
    # sample_edge = next(iter(graph.edges))
    # print(sample_edge, json.dumps(graph.edges[sample_edge], indent=4, sort_keys=False))

    # draw_geographic_projection(graph, n=50)

    airport_pairs = [
        ("SYD", "MEL"),
        ("YYC", "SYD"),
        ("LHR", "JFK"),
        ("CDG", "DXB"),
    ]

    for origin, destination in airport_pairs:
        print("\n" + "=" * 60)
        print(f"Searching routes: {origin} -> {destination}")

        routes = find_flight_routes(
            origin=origin,
            destination=destination,
            graph=graph,
            max_legs=3,
            max_routes=3,
        )

        if not routes:
            print("No routes found.")
            continue

        for r in routes:
            print(r)

        print()  # spacing between searches


if __name__ == "__main__":
    main()
