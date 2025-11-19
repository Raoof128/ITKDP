"""
Unit tests for GeoIP resolution
"""
import pytest
from geo import GeoIPResolver, GeoLocation


class TestGeoIPResolver:
    """Test GeoIP resolution functionality."""

    def test_resolver_initialization(self):
        """Test GeoIP resolver initialization."""
        resolver = GeoIPResolver()
        assert resolver is not None
        assert resolver.mock_db is not None
        assert len(resolver.mock_db) > 0

    def test_known_ip_resolution(self):
        """Test resolution of known IP addresses."""
        resolver = GeoIPResolver()
        location = resolver.resolve("203.0.113.1")  # Sydney

        assert isinstance(location, GeoLocation)
        assert location.city == "Sydney"
        assert location.country == "Australia"
        assert location.latitude == -33.8688
        assert location.longitude == 151.2093

    def test_unknown_ip_resolution(self):
        """Test resolution of unknown IP addresses."""
        resolver = GeoIPResolver()
        location = resolver.resolve("192.0.2.1")  # Not in mock DB

        assert isinstance(location, GeoLocation)
        assert location.city == "UNKNOWN"
        assert location.country == "UNKNOWN"
        assert location.latitude == 0.0
        assert location.longitude == 0.0

    def test_london_ip(self):
        """Test London IP resolution."""
        resolver = GeoIPResolver()
        location = resolver.resolve("203.0.113.2")

        assert location.city == "London"
        assert location.country == "United Kingdom"

    def test_new_york_ip(self):
        """Test New York IP resolution."""
        resolver = GeoIPResolver()
        location = resolver.resolve("203.0.113.3")

        assert location.city == "New York"
        assert location.country == "United States"

    def test_context_manager(self):
        """Test context manager functionality."""
        with GeoIPResolver() as resolver:
            location = resolver.resolve("203.0.113.1")
            assert location.city == "Sydney"

    def test_multiple_resolutions(self):
        """Test multiple IP resolutions."""
        resolver = GeoIPResolver()

        locations = [
            resolver.resolve("203.0.113.1"),  # Sydney
            resolver.resolve("203.0.113.2"),  # London
            resolver.resolve("203.0.113.3"),  # New York
        ]

        assert len(locations) == 3
        assert locations[0].city == "Sydney"
        assert locations[1].city == "London"
        assert locations[2].city == "New York"


class TestGeoLocation:
    """Test GeoLocation dataclass."""

    def test_geolocation_creation(self):
        """Test creating a GeoLocation object."""
        location = GeoLocation(
            latitude=51.5074,
            longitude=-0.1278,
            city="London",
            country="United Kingdom",
            ip_address="203.0.113.2"
        )

        assert location.latitude == 51.5074
        assert location.longitude == -0.1278
        assert location.city == "London"
        assert location.country == "United Kingdom"
        assert location.ip_address == "203.0.113.2"
