"""
Impossible Travel Detection Engine

A Python-based security analytics tool for detecting impossible travel patterns
in user login events.
"""

__version__ = "1.0.0"
__author__ = "Security Engineering Team"
__license__ = "MIT"

from .config import DetectionConfig, AppInfo, get_config, set_config
from .geo import GeoIPResolver, GeoLocation
from .analysis import ImpossibleTravelAnalyzer
from .report import ReportGenerator
from .utils import (
    haversine_distance,
    calculate_time_diff_hours,
    calculate_required_speed,
    format_location,
)

__all__ = [
    # Configuration
    "DetectionConfig",
    "AppInfo",
    "get_config",
    "set_config",
    # Core classes
    "GeoIPResolver",
    "GeoLocation",
    "ImpossibleTravelAnalyzer",
    "ReportGenerator",
    # Utility functions
    "haversine_distance",
    "calculate_time_diff_hours",
    "calculate_required_speed",
    "format_location",
]
