import matplotlib.pyplot as plt
import networkx as nx

import matplotlib.pyplot as plt
import networkx as nx
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def draw_hub_subgraph(graph: nx.DiGraph, n: int = 50) -> None:
    hub_nodes = [
        node for node, _ in sorted(graph.degree, key=lambda x: x[1], reverse=True)[:n]
    ]

    subgraph = graph.subgraph(hub_nodes)

    # better spacing than default spring layout
    pos = nx.spring_layout(
        subgraph, seed=42, k=1.2, iterations=100  # increase node repulsion
    )

    plt.figure(figsize=(10, 10), num="Skymesh")

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


def draw_geographic_projection(graph: nx.DiGraph, n: int = 300) -> None:
    """
    Dark-mode geographic projection focused on North America + Europe
    with curved great-circle edges.
    """

    hub_nodes = [
        node for node, _ in sorted(graph.degree, key=lambda x: x[1], reverse=True)[:n]
    ]

    subgraph = graph.subgraph(hub_nodes)

    pos = {
        node: (subgraph.nodes[node]["longitude"], subgraph.nodes[node]["latitude"])
        for node in subgraph.nodes()
    }

    # --- Dark mode figure ---
    fig = plt.figure(figsize=(16, 8), facecolor="#0b0b0b")
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_facecolor("#0b0b0b")

    # Slightly zoomed out
    ax.set_extent([-145, 60, 15, 80], crs=ccrs.PlateCarree())

    # Dark map styling
    ax.add_feature(cfeature.LAND, facecolor="#171717")
    ax.add_feature(cfeature.OCEAN, facecolor="#0b0b0b")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor="#333333")
    ax.add_feature(cfeature.BORDERS, linewidth=0.2, edgecolor="#222222")

    # Draw curved great-circle edges (now white)
    for source, target in subgraph.edges():
        lon1, lat1 = pos[source]
        lon2, lat2 = pos[target]

        ax.plot(
            [lon1, lon2],
            [lat1, lat2],
            transform=ccrs.Geodetic(),
            alpha=0.07,
            linewidth=0.6,
            color="white",
        )

    # Degree-scaled node sizes (slightly larger)
    degrees = dict(subgraph.degree)
    sizes = [40 + degrees[node] * 0.8 for node in subgraph.nodes()]

    xs = [pos[node][0] for node in subgraph.nodes()]
    ys = [pos[node][1] for node in subgraph.nodes()]

    ax.scatter(xs, ys, transform=ccrs.PlateCarree(), s=sizes, color="#ff4d4d", zorder=5)

    # macOS-friendly font stack
    plt.title(
        f"Skymesh - Global Aviation Network ({n} Hub Airports)",
        color="white",
        pad=20,
        fontfamily="SF Pro Display",  # macOS native
    )

    plt.tight_layout()
    plt.show()
