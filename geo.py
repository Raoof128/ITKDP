"""
GeoIP lookup module for resolving IP addresses to geographic locations.
"""
import logging
from typing import Dict, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GeoLocation:
    """Represents a geographic location."""
    latitude: float
    longitude: float
    city: str
    country: str
    ip_address: str


class GeoIPResolver:
    """
    Resolves IP addresses to geographic locations.

    This class uses a mock database for demonstration purposes.
    In production, use geoip2 with the GeoLite2-City database:

    Example:
        import geoip2.database
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ip_address)
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the GeoIP resolver.

        Args:
            db_path: Path to GeoLite2-City.mmdb database (optional)
        """
        self.db_path = db_path
        self.reader = None
        self._init_mock_database()

    def _init_mock_database(self):
        """
        Initialize a mock IP database for demonstration.

        This provides realistic test data without requiring the actual GeoLite2 database.
        """
        self.mock_db = {
            # Major cities for testing
            "203.0.113.1": GeoLocation(-33.8688, 151.2093, "Sydney", "Australia", "203.0.113.1"),
            "203.0.113.2": GeoLocation(51.5074, -0.1278, "London", "United Kingdom", "203.0.113.2"),
            "203.0.113.3": GeoLocation(40.7128, -74.0060, "New York", "United States", "203.0.113.3"),
            "203.0.113.4": GeoLocation(35.6762, 139.6503, "Tokyo", "Japan", "203.0.113.4"),
            "203.0.113.5": GeoLocation(48.8566, 2.3522, "Paris", "France", "203.0.113.5"),
            "203.0.113.6": GeoLocation(55.7558, 37.6173, "Moscow", "Russia", "203.0.113.6"),
            "203.0.113.7": GeoLocation(-23.5505, -46.6333, "São Paulo", "Brazil", "203.0.113.7"),
            "203.0.113.8": GeoLocation(1.3521, 103.8198, "Singapore", "Singapore", "203.0.113.8"),
            "203.0.113.9": GeoLocation(52.5200, 13.4050, "Berlin", "Germany", "203.0.113.9"),
            "203.0.113.10": GeoLocation(37.7749, -122.4194, "San Francisco", "United States", "203.0.113.10"),
            "203.0.113.11": GeoLocation(25.2048, 55.2708, "Dubai", "United Arab Emirates", "203.0.113.11"),
            "203.0.113.12": GeoLocation(-26.2041, 28.0473, "Johannesburg", "South Africa", "203.0.113.12"),
            "203.0.113.13": GeoLocation(19.4326, -99.1332, "Mexico City", "Mexico", "203.0.113.13"),
            "203.0.113.14": GeoLocation(28.6139, 77.2090, "New Delhi", "India", "203.0.113.14"),
            "203.0.113.15": GeoLocation(39.9042, 116.4074, "Beijing", "China", "203.0.113.15"),
            "203.0.113.16": GeoLocation(-37.8136, 144.9631, "Melbourne", "Australia", "203.0.113.16"),
            "203.0.113.17": GeoLocation(45.4215, -75.6972, "Ottawa", "Canada", "203.0.113.17"),
            "203.0.113.18": GeoLocation(41.9028, 12.4964, "Rome", "Italy", "203.0.113.18"),
            "203.0.113.19": GeoLocation(59.3293, 18.0686, "Stockholm", "Sweden", "203.0.113.19"),
            "203.0.113.20": GeoLocation(-41.2865, 174.7762, "Wellington", "New Zealand", "203.0.113.20"),
        }
        logger.info(f"Mock database initialized with {len(self.mock_db)} locations")

    def resolve(self, ip_address: str) -> GeoLocation:
        """
        Resolve an IP address to a geographic location.

        Args:
            ip_address: IP address to resolve

        Returns:
            GeoLocation object with coordinates and location info

        Example:
            >>> resolver = GeoIPResolver()
            >>> location = resolver.resolve("203.0.113.1")
            >>> print(f"{location.city}, {location.country}")
            Sydney, Australia
        """
        # Try mock database first
        if ip_address in self.mock_db:
            logger.debug(f"Resolved {ip_address} from mock database")
            return self.mock_db[ip_address]

        # If using real GeoIP2 database (uncomment in production):
        # if self.reader:
        #     try:
        #         response = self.reader.city(ip_address)
        #         return GeoLocation(
        #             latitude=response.location.latitude,
        #             longitude=response.location.longitude,
        #             city=response.city.name or "UNKNOWN",
        #             country=response.country.name or "UNKNOWN",
        #             ip_address=ip_address
        #         )
        #     except Exception as e:
        #         logger.warning(f"GeoIP lookup failed for {ip_address}: {e}")

        # Return UNKNOWN location
        logger.warning(f"No location found for {ip_address}, returning UNKNOWN")
        return GeoLocation(
            latitude=0.0,
            longitude=0.0,
            city="UNKNOWN",
            country="UNKNOWN",
            ip_address=ip_address
        )

    def close(self):
        """Close the GeoIP database reader."""
        if self.reader:
            self.reader.close()
            logger.info("GeoIP database reader closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
