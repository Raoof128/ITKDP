"""
Unit tests for utility functions
"""
import pytest
from utils import haversine_distance, calculate_time_diff_hours, calculate_required_speed, format_location


class TestHaversineDistance:
    """Test Haversine distance calculations."""

    def test_london_to_new_york(self):
        """Test distance from London to New York."""
        # London: 51.5074° N, 0.1278° W
        # New York: 40.7128° N, 74.0060° W
        distance = haversine_distance(51.5074, -0.1278, 40.7128, -74.0060)
        # Expected: ~5570 km
        assert 5500 < distance < 5600

    def test_sydney_to_london(self):
        """Test distance from Sydney to London."""
        # Sydney: -33.8688° S, 151.2093° E
        # London: 51.5074° N, 0.1278° W
        distance = haversine_distance(-33.8688, 151.2093, 51.5074, -0.1278)
        # Expected: ~17000 km
        assert 16900 < distance < 17100

    def test_same_location(self):
        """Test distance between same coordinates."""
        distance = haversine_distance(0.0, 0.0, 0.0, 0.0)
        assert distance == 0.0

    def test_equator_points(self):
        """Test distance along equator."""
        # 1 degree longitude at equator ≈ 111 km
        distance = haversine_distance(0.0, 0.0, 0.0, 1.0)
        assert 110 < distance < 112


class TestTimeDifferenceCalculation:
    """Test time difference calculations."""

    def test_two_hour_difference(self):
        """Test 2-hour time difference."""
        time_diff = calculate_time_diff_hours(
            "2025-01-15T10:00:00",
            "2025-01-15T12:00:00"
        )
        assert time_diff == 2.0

    def test_half_hour_difference(self):
        """Test 30-minute time difference."""
        time_diff = calculate_time_diff_hours(
            "2025-01-15T10:00:00",
            "2025-01-15T10:30:00"
        )
        assert time_diff == 0.5

    def test_same_timestamp(self):
        """Test zero time difference."""
        time_diff = calculate_time_diff_hours(
            "2025-01-15T10:00:00",
            "2025-01-15T10:00:00"
        )
        assert time_diff == 0.0

    def test_day_difference(self):
        """Test 24-hour time difference."""
        time_diff = calculate_time_diff_hours(
            "2025-01-15T10:00:00",
            "2025-01-16T10:00:00"
        )
        assert time_diff == 24.0


class TestSpeedCalculation:
    """Test required speed calculations."""

    def test_normal_speed(self):
        """Test normal travel speed."""
        speed = calculate_required_speed(1000, 2)
        assert speed == 500.0

    def test_impossible_speed(self):
        """Test impossible travel speed."""
        speed = calculate_required_speed(5000, 1)
        assert speed == 5000.0

    def test_zero_time(self):
        """Test division by zero handling."""
        speed = calculate_required_speed(1000, 0)
        assert speed == float('inf')

    def test_slow_speed(self):
        """Test slow travel speed."""
        speed = calculate_required_speed(100, 10)
        assert speed == 10.0


class TestLocationFormatting:
    """Test location formatting."""

    def test_normal_location(self):
        """Test normal location formatting."""
        location = format_location("London", "United Kingdom")
        assert location == "London, United Kingdom"

    def test_unknown_city(self):
        """Test unknown city handling."""
        location = format_location("UNKNOWN", "United States")
        assert location == "UNKNOWN"

    def test_unknown_country(self):
        """Test unknown country handling."""
        location = format_location("New York", "UNKNOWN")
        assert location == "UNKNOWN"

    def test_both_unknown(self):
        """Test both unknown."""
        location = format_location("UNKNOWN", "UNKNOWN")
        assert location == "UNKNOWN"
