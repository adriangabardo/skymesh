import matplotlib.pyplot as plt
import networkx as nx


def draw_hub_subgraph(graph: nx.DiGraph, n: int = 50) -> None:
    hub_nodes = [
        node for node, _ in sorted(graph.degree, key=lambda x: x[1], reverse=True)[:n]
    ]

    subgraph = graph.subgraph(hub_nodes)

    # better spacing than default spring layout
    pos = nx.spring_layout(
        subgraph, seed=42, k=1.2, iterations=100  # increase node repulsion
    )

    plt.figure(figsize=(10, 10))

    # draw edges first (lighter, thinner)
    nx.draw_networkx_edges(subgraph, pos, alpha=0.25, width=0.8, arrows=False)

    # draw nodes
    nx.draw_networkx_nodes(subgraph, pos, node_size=600, node_color="#1f77b4")

    # draw labels last (on top)
    nx.draw_networkx_labels(subgraph, pos, font_size=9, font_weight="bold")

    plt.title(f"Skymesh - Hub-Centric Airport Graph ({n} Airports)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
