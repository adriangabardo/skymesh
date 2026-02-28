# ---------------------------------------------------------------------------
# Physics & Flight Modelling
# ---------------------------------------------------------------------------

# Used to calculate great-circle distance
EARTH_RADIUS_KM = 6371.0

# Buffer added to all flights (taxi, climb, descent)
GROUND_BUFFER_MINUTES = 20

# Default cruise speed (km/h) if aircraft unknown
DEFAULT_CRUISE_SPEED = 850

# Known aircraft cruise speeds (km/h)
AIRCRAFT_SPEED_KMH = {
    "DH8": 550,
    "AT7": 550,
    "320": 840,
    "321": 840,
    "738": 840,
    "739": 840,
    "777": 900,
    "788": 900,
    "789": 900,
    "332": 880,
    "333": 880,
}

# ---------------------------------------------------------------------------
# Pricing Simulation (OpenFlights Only)
# ---------------------------------------------------------------------------

BASE_FARE_PER_LEG = 50.0
PRICE_PER_KM = 0.12
LAYOVER_PENALTY_PER_HOUR = 15.0
DEFAULT_CURRENCY = "USD"
