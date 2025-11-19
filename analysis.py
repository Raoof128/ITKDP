"""
Core analysis engine for detecting impossible travel patterns.
"""
import pandas as pd
import logging
from typing import List, Dict
from datetime import datetime

from geo import GeoIPResolver, GeoLocation
from utils import haversine_distance, calculate_time_diff_hours, calculate_required_speed, format_location

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImpossibleTravelAnalyzer:
    """
    Analyzes login events to detect impossible travel patterns.

    This class processes login events, performs GeoIP lookups, calculates
    travel distances and speeds, and flags impossible travel scenarios.
    """

    def __init__(self, speed_threshold_kmh: float = 1000.0, geo_resolver: GeoIPResolver = None):
        """
        Initialize the analyzer.

        Args:
            speed_threshold_kmh: Speed threshold in km/h (default: 1000)
            geo_resolver: GeoIP resolver instance (optional)
        """
        self.speed_threshold = speed_threshold_kmh
        self.geo_resolver = geo_resolver or GeoIPResolver()
        logger.info(f"Initialized analyzer with speed threshold: {speed_threshold_kmh} km/h")

    def load_login_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load login events from CSV file.

        Args:
            csv_path: Path to CSV file with login events

        Returns:
            DataFrame with login events

        Expected CSV columns:
            - user_id: User identifier
            - timestamp: ISO format timestamp
            - ip_address: IP address of login
        """
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} login events from {csv_path}")

            # Validate required columns
            required_columns = ['user_id', 'timestamp', 'ip_address']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            # Sort by user and timestamp
            df = df.sort_values(['user_id', 'timestamp'])

            return df

        except Exception as e:
            logger.error(f"Failed to load login data: {e}")
            raise

    def enrich_with_geolocation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich login events with geographic location data.

        Args:
            df: DataFrame with login events

        Returns:
            DataFrame with added geo columns
        """
        logger.info("Enriching events with geolocation data...")

        geo_data = []
        for ip in df['ip_address']:
            location = self.geo_resolver.resolve(ip)
            geo_data.append({
                'latitude': location.latitude,
                'longitude': location.longitude,
                'city': location.city,
                'country': location.country
            })

        geo_df = pd.DataFrame(geo_data)
        enriched_df = pd.concat([df.reset_index(drop=True), geo_df], axis=1)

        logger.info(f"Enriched {len(enriched_df)} events with geolocation data")
        return enriched_df

    def analyze_travel_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze travel patterns for each user.

        Args:
            df: DataFrame with enriched login events

        Returns:
            DataFrame with travel analysis
        """
        logger.info("Analyzing travel patterns...")

        results = []

        # Group by user
        for user_id, user_events in df.groupby('user_id'):
            user_events = user_events.sort_values('timestamp')

            # Compare consecutive login pairs
            for i in range(len(user_events) - 1):
                prev_event = user_events.iloc[i]
                curr_event = user_events.iloc[i + 1]

                # Calculate distance
                distance_km = haversine_distance(
                    prev_event['latitude'],
                    prev_event['longitude'],
                    curr_event['latitude'],
                    curr_event['longitude']
                )

                # Calculate time difference
                time_diff_hours = calculate_time_diff_hours(
                    prev_event['timestamp'],
                    curr_event['timestamp']
                )

                # Calculate required speed
                required_speed = calculate_required_speed(distance_km, time_diff_hours)

                # Check if impossible travel
                is_impossible = required_speed > self.speed_threshold

                # Format locations
                prev_location = format_location(prev_event['city'], prev_event['country'])
                curr_location = format_location(curr_event['city'], curr_event['country'])

                results.append({
                    'user_id': user_id,
                    'previous_location': prev_location,
                    'new_location': curr_location,
                    'previous_ip': prev_event['ip_address'],
                    'new_ip': curr_event['ip_address'],
                    'previous_timestamp': prev_event['timestamp'],
                    'new_timestamp': curr_event['timestamp'],
                    'distance_km': distance_km,
                    'time_diff_hours': time_diff_hours,
                    'required_speed_kmh': required_speed,
                    'is_impossible_travel': is_impossible
                })

        results_df = pd.DataFrame(results)
        logger.info(f"Analyzed {len(results_df)} login transitions")

        return results_df

    def filter_impossible_travel(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter only impossible travel events.

        Args:
            df: DataFrame with travel analysis

        Returns:
            DataFrame with only impossible travel events
        """
        impossible_df = df[df['is_impossible_travel'] == True].copy()
        logger.info(f"Found {len(impossible_df)} impossible travel events")
        return impossible_df

    def get_summary_statistics(self, full_df: pd.DataFrame, impossible_df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics.

        Args:
            full_df: Full analysis DataFrame
            impossible_df: Impossible travel events DataFrame

        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_events_analyzed': len(full_df),
            'impossible_travel_events': len(impossible_df),
            'affected_users': impossible_df['user_id'].nunique() if len(impossible_df) > 0 else 0,
            'detection_rate': f"{(len(impossible_df) / len(full_df) * 100):.2f}%" if len(full_df) > 0 else "0%",
            'max_speed_detected': impossible_df['required_speed_kmh'].max() if len(impossible_df) > 0 else 0,
            'avg_distance': f"{full_df['distance_km'].mean():.2f}" if len(full_df) > 0 else "0",
            'speed_threshold': self.speed_threshold
        }

        logger.info(f"Summary: {stats['impossible_travel_events']} impossible travel events detected")
        return stats

    def run_analysis(self, csv_path: str) -> tuple:
        """
        Run the complete analysis pipeline.

        Args:
            csv_path: Path to login events CSV

        Returns:
            Tuple of (full_analysis_df, impossible_travel_df, statistics)
        """
        logger.info("=" * 60)
        logger.info("Starting Impossible Travel Detection Analysis")
        logger.info("=" * 60)

        # Load data
        df = self.load_login_data(csv_path)

        # Enrich with geolocation
        enriched_df = self.enrich_with_geolocation(df)

        # Analyze travel patterns
        full_analysis = self.analyze_travel_patterns(enriched_df)

        # Filter impossible travel
        impossible_travel = self.filter_impossible_travel(full_analysis)

        # Get statistics
        stats = self.get_summary_statistics(full_analysis, impossible_travel)

        logger.info("=" * 60)
        logger.info("Analysis Complete")
        logger.info("=" * 60)

        return full_analysis, impossible_travel, stats
