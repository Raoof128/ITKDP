"""
Unit tests for analysis engine
"""
import pytest
import pandas as pd
from pathlib import Path
from analysis import ImpossibleTravelAnalyzer
from geo import GeoIPResolver


class TestImpossibleTravelAnalyzer:
    """Test impossible travel analysis functionality."""

    @pytest.fixture
    def analyzer(self):
        """Create an analyzer instance for testing."""
        return ImpossibleTravelAnalyzer(speed_threshold_kmh=1000.0)

    @pytest.fixture
    def sample_data(self, tmp_path):
        """Create sample login data for testing."""
        csv_path = tmp_path / "test_logins.csv"
        data = """user_id,timestamp,ip_address
alice,2025-01-15T08:00:00,203.0.113.1
alice,2025-01-15T08:45:00,203.0.113.2
bob,2025-01-15T09:00:00,203.0.113.4
bob,2025-01-15T15:00:00,203.0.113.4
"""
        csv_path.write_text(data)
        return csv_path

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.speed_threshold == 1000.0
        assert analyzer.geo_resolver is not None

    def test_load_login_data(self, analyzer, sample_data):
        """Test loading login data from CSV."""
        df = analyzer.load_login_data(str(sample_data))

        assert len(df) == 4
        assert 'user_id' in df.columns
        assert 'timestamp' in df.columns
        assert 'ip_address' in df.columns

    def test_enrich_with_geolocation(self, analyzer, sample_data):
        """Test geolocation enrichment."""
        df = analyzer.load_login_data(str(sample_data))
        enriched_df = analyzer.enrich_with_geolocation(df)

        assert 'latitude' in enriched_df.columns
        assert 'longitude' in enriched_df.columns
        assert 'city' in enriched_df.columns
        assert 'country' in enriched_df.columns
        assert len(enriched_df) == len(df)

    def test_analyze_travel_patterns(self, analyzer, sample_data):
        """Test travel pattern analysis."""
        df = analyzer.load_login_data(str(sample_data))
        enriched_df = analyzer.enrich_with_geolocation(df)
        analysis_df = analyzer.analyze_travel_patterns(enriched_df)

        assert 'distance_km' in analysis_df.columns
        assert 'time_diff_hours' in analysis_df.columns
        assert 'required_speed_kmh' in analysis_df.columns
        assert 'is_impossible_travel' in analysis_df.columns

    def test_filter_impossible_travel(self, analyzer, sample_data):
        """Test filtering impossible travel events."""
        df = analyzer.load_login_data(str(sample_data))
        enriched_df = analyzer.enrich_with_geolocation(df)
        analysis_df = analyzer.analyze_travel_patterns(enriched_df)
        impossible_df = analyzer.filter_impossible_travel(analysis_df)

        # All events in impossible_df should be flagged
        assert all(impossible_df['is_impossible_travel'])

    def test_summary_statistics(self, analyzer, sample_data):
        """Test summary statistics generation."""
        df = analyzer.load_login_data(str(sample_data))
        enriched_df = analyzer.enrich_with_geolocation(df)
        analysis_df = analyzer.analyze_travel_patterns(enriched_df)
        impossible_df = analyzer.filter_impossible_travel(analysis_df)

        stats = analyzer.get_summary_statistics(analysis_df, impossible_df)

        assert 'total_events_analyzed' in stats
        assert 'impossible_travel_events' in stats
        assert 'affected_users' in stats
        assert 'detection_rate' in stats
        assert stats['speed_threshold'] == 1000.0

    def test_custom_speed_threshold(self):
        """Test analyzer with custom speed threshold."""
        analyzer = ImpossibleTravelAnalyzer(speed_threshold_kmh=1500.0)
        assert analyzer.speed_threshold == 1500.0

    def test_run_full_analysis(self, analyzer, sample_data):
        """Test complete analysis pipeline."""
        full_df, impossible_df, stats = analyzer.run_analysis(str(sample_data))

        assert isinstance(full_df, pd.DataFrame)
        assert isinstance(impossible_df, pd.DataFrame)
        assert isinstance(stats, dict)
        assert len(impossible_df) <= len(full_df)
