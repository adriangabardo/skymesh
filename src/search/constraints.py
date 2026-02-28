from __future__ import annotations

from datetime import datetime, timedelta
from typing import Tuple

from entities.flight import Flight


# ---------------------------------------------------------------------------
# Core Time Constraints
# ---------------------------------------------------------------------------

MIN_CONNECTION_TIME = timedelta(minutes=45)
MAX_CONNECTION_TIME = timedelta(hours=6)


# ---------------------------------------------------------------------------
# Constraint Evaluation
# ---------------------------------------------------------------------------


def is_connection_time_valid(
    *,
    previous_arrival: datetime,
    next_departure: datetime,
) -> bool:
    """
    Validate that a connection between two flights satisfies
    minimum and maximum layover rules.
    """

    layover = next_departure - previous_arrival

    if layover < MIN_CONNECTION_TIME:
        return False

    if layover > MAX_CONNECTION_TIME:
        return False

    return True


def is_cycle_free(
    *,
    next_airport: str,
    visited: set[str],
) -> bool:
    """
    Prevent revisiting the same airport within a route.
    """
    return next_airport not in visited


def is_flight_sequence_valid(
    *,
    path: Tuple[Flight, ...],
    candidate: Flight,
    visited: set[str],
) -> bool:
    """
    Validate whether a candidate flight can extend the current path.

    This function centralises all route-level constraints.
    """

    # Prevent cycles
    if not is_cycle_free(
        next_airport=candidate.destination,
        visited=visited,
    ):
        return False

    # First leg always valid
    if not path:
        return True

    previous_flight = path[-1]

    if not is_connection_time_valid(
        previous_arrival=previous_flight.arrival_time,
        next_departure=candidate.departure_time,
    ):
        return False

    return True
