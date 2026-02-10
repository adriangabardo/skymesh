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
