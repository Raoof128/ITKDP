"""
Utility functions for Impossible Travel Detection Engine
"""
import math
from typing import Tuple
from datetime import datetime


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Uses the Haversine formula to calculate distance in kilometers.

    Args:
        lat1: Latitude of first point (degrees)
        lon1: Longitude of first point (degrees)
        lat2: Latitude of second point (degrees)
        lon2: Longitude of second point (degrees)

    Returns:
        Distance in kilometers

    Example:
        >>> haversine_distance(51.5074, -0.1278, 40.7128, -74.0060)  # London to NYC
        5570.222
    """
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return round(distance, 2)


def calculate_time_diff_hours(timestamp1: str, timestamp2: str) -> float:
    """
    Calculate time difference between two timestamps in hours.

    Args:
        timestamp1: Earlier timestamp (ISO format)
        timestamp2: Later timestamp (ISO format)

    Returns:
        Time difference in hours

    Example:
        >>> calculate_time_diff_hours("2025-01-01T10:00:00", "2025-01-01T12:30:00")
        2.5
    """
    dt1 = datetime.fromisoformat(timestamp1.replace('Z', '+00:00'))
    dt2 = datetime.fromisoformat(timestamp2.replace('Z', '+00:00'))

    time_diff = abs((dt2 - dt1).total_seconds())
    hours = time_diff / 3600

    return round(hours, 2)


def calculate_required_speed(distance_km: float, time_hours: float) -> float:
    """
    Calculate the required travel speed in km/h.

    Args:
        distance_km: Distance in kilometers
        time_hours: Time in hours

    Returns:
        Speed in km/h

    Example:
        >>> calculate_required_speed(1000, 2)
        500.0
    """
    if time_hours == 0:
        return float('inf')

    speed = distance_km / time_hours
    return round(speed, 2)


def format_location(city: str, country: str) -> str:
    """
    Format location string for display.

    Args:
        city: City name
        country: Country name

    Returns:
        Formatted location string

    Example:
        >>> format_location("London", "United Kingdom")
        "London, United Kingdom"
    """
    if city == "UNKNOWN" or country == "UNKNOWN":
        return "UNKNOWN"
    return f"{city}, {country}"
