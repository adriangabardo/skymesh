import json
from graph_build import build_graph
from graph_viz import draw_hub_subgraph


def main() -> None:
    graph = build_graph()

    print("Skymesh graph loaded")
    print(f"Airports (nodes): {graph.number_of_nodes()}")
    print(f"Routes (edges): {graph.number_of_edges()}")

    print("\nSample airport:")
    sample_node = next(iter(graph.nodes))
    print(sample_node, json.dumps(graph.nodes[sample_node], indent=4, sort_keys=False))

    print("\nSample route:")
    sample_edge = next(iter(graph.edges))
    print(sample_edge, json.dumps(graph.edges[sample_edge], indent=4, sort_keys=False))

    draw_hub_subgraph(graph, n=20)


if __name__ == "__main__":
    main()
