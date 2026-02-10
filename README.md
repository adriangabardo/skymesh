# skymesh

## Getting Started

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 2. Run the Script

```bash
./run_local.sh
```

### 3. Expected Script Behavior

Terminal output:

```
Skymesh graph loaded
Airports (nodes): 6072
Routes (edges): 37042

Sample airport:
GKA {
    "name": "Goroka Airport",
    "city": "Goroka",
    "country": "Papua New Guinea",
    "icao": "AYGA",
    "latitude": -6.081689834590001,
    "longitude": 145.391998291,
    "altitude": 5282,
    "timezone": "10"
}

Sample route:
('GKA', 'HGU') {
    "airline": "CG",
    "airline_id": "1308",
    "codeshare": false,
    "stops": 0,
    "equipment": [
        "DH8",
        "DHT"
    ]
}
```

The graph viz will then open, and remain opened until the process is exited.

## Versioning and Article References

This repository uses git tags to align code versions with articles in _The Graph Series_.

Tags follow the format:

`v{article}.{major}.{minor}`

Where:

- `article` refers to the article number in the series
- `major` indicates a conceptual change within that article’s scope
- `minor` indicates non-breaking changes such as refactors or small fixes

For example, `v2.0.1` corresponds to Article II (_Getting Started and Data Ingestion_), with a minor revision applied after initial publication.

Each article in the series references a specific tag so readers can check out the exact code state used in that article.
