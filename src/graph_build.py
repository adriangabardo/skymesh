import csv
from pathlib import Path
import networkx as nx


DATA_DIR = Path("./data")

AIRPORTS_FILE = DATA_DIR / "airports.dat"
ROUTES_FILE = DATA_DIR / "routes.dat"


def load_airports(graph: nx.DiGraph) -> None:
    """
    Load airports as nodes into the graph.
    Node key: IATA code (str)
    """
    with AIRPORTS_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            iata = row[4]

            # skip airports without a valid IATA code
            if iata == "\\N" or not iata:
                continue

            graph.add_node(
                iata,
                name=row[1],
                city=row[2],
                country=row[3],
                icao=row[5] if row[5] != "\\N" else None,
                latitude=float(row[6]),
                longitude=float(row[7]),
                altitude=int(row[8]),
                timezone=row[9],
            )


def load_routes(graph: nx.DiGraph) -> None:
    """
    Load routes as directed edges using IATA codes.
    """
    with ROUTES_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            source_iata = row[2]
            destination_iata = row[4]

            if (
                source_iata == "\\N"
                or destination_iata == "\\N"
                or not graph.has_node(source_iata)
                or not graph.has_node(destination_iata)
            ):
                continue

            graph.add_edge(
                source_iata,
                destination_iata,
                airline=row[0],
                airline_id=row[1] if row[1] != "\\N" else None,
                codeshare=row[6] == "Y",
                stops=int(row[7]),
                equipment=row[8].split() if row[8] != "\\N" else [],
            )


def build_graph() -> nx.DiGraph:
    graph = nx.DiGraph()
    load_airports(graph)
    load_routes(graph)
    return graph
