#!/usr/bin/env python3
"""
Impossible Travel Detection Engine

A security analytics tool that detects impossible travel patterns in user login events.
Simulates Azure Sentinel KQL detection logic for identifying potential account compromises.

Usage:
    python main.py [input_file] [--output-dir OUTPUT_DIR] [--speed-threshold SPEED]

Example:
    python main.py sample_logins.csv
    python main.py logins.csv --output-dir ./results --speed-threshold 1200
"""

import argparse
import sys
import logging
from pathlib import Path

from analysis import ImpossibleTravelAnalyzer
from report import ReportGenerator
from geo import GeoIPResolver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Impossible Travel Detection Engine - Detect suspicious login patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py sample_logins.csv
  python main.py logins.csv --output-dir ./results
  python main.py logins.csv --speed-threshold 1200

Output Files:
  - impossible_travel.csv    : Only flagged impossible travel events
  - full_analysis.csv        : Complete analysis of all login transitions
  - report.md                : Comprehensive markdown report with recommendations
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Path to CSV file with login events (columns: user_id, timestamp, ip_address)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for results (default: current directory)'
    )

    parser.add_argument(
        '--speed-threshold',
        type=float,
        default=1000.0,
        help='Speed threshold in km/h for impossible travel detection (default: 1000)'
    )

    parser.add_argument(
        '--geo-db',
        type=str,
        default=None,
        help='Path to GeoLite2-City.mmdb database (optional)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()


def validate_input_file(file_path: str) -> Path:
    """
    Validate that input file exists.

    Args:
        file_path: Path to input file

    Returns:
        Path object

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    return path


def create_output_directory(output_dir: str) -> Path:
    """
    Create output directory if it doesn't exist.

    Args:
        output_dir: Output directory path

    Returns:
        Path object
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_results(full_df, impossible_df, stats, output_dir: Path):
    """
    Save analysis results to CSV files.

    Args:
        full_df: Full analysis DataFrame
        impossible_df: Impossible travel events DataFrame
        stats: Summary statistics
        output_dir: Output directory path
    """
    # Save impossible travel events
    impossible_travel_path = output_dir / 'impossible_travel.csv'
    impossible_df.to_csv(impossible_travel_path, index=False)
    logger.info(f"Saved impossible travel events to: {impossible_travel_path}")

    # Save full analysis
    full_analysis_path = output_dir / 'full_analysis.csv'
    full_df.to_csv(full_analysis_path, index=False)
    logger.info(f"Saved full analysis to: {full_analysis_path}")


def print_summary(stats: dict, impossible_df):
    """
    Print analysis summary to console.

    Args:
        stats: Summary statistics dictionary
        impossible_df: Impossible travel DataFrame
    """
    print("\n" + "=" * 70)
    print("IMPOSSIBLE TRAVEL DETECTION SUMMARY")
    print("=" * 70)
    print(f"Total Login Transitions Analyzed: {stats['total_events_analyzed']}")
    print(f"Impossible Travel Events Detected: {stats['impossible_travel_events']}")
    print(f"Affected User Accounts: {stats['affected_users']}")
    print(f"Detection Rate: {stats['detection_rate']}")
    print(f"Speed Threshold: {stats['speed_threshold']} km/h")
    print("=" * 70)

    if len(impossible_df) > 0:
        print("\nTOP 5 IMPOSSIBLE TRAVEL EVENTS:")
        print("-" * 70)
        top_5 = impossible_df.nlargest(min(5, len(impossible_df)), 'required_speed_kmh')

        for idx, event in top_5.iterrows():
            print(f"\n  User: {event['user_id']}")
            print(f"  Path: {event['previous_location']} → {event['new_location']}")
            print(f"  Speed Required: {event['required_speed_kmh']:.2f} km/h")
            print(f"  Distance: {event['distance_km']:.2f} km in {event['time_diff_hours']:.2f} hours")

        print("\n" + "-" * 70)
        print("\n⚠️  WARNING: Potential security incidents detected!")
        print("Review the report.md file for detailed analysis and recommendations.")
    else:
        print("\n✓ No impossible travel events detected.")
        print("All login patterns appear normal.")

    print("\n" + "=" * 70 + "\n")


def main():
    """
    Main entry point for the Impossible Travel Detection Engine.
    """
    try:
        # Parse arguments
        args = parse_arguments()

        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        # Print banner
        print("\n" + "=" * 70)
        print("IMPOSSIBLE TRAVEL DETECTION ENGINE")
        print("Simulating Azure Sentinel KQL Detection Logic")
        print("=" * 70 + "\n")

        # Validate input
        logger.info(f"Input file: {args.input_file}")
        input_path = validate_input_file(args.input_file)

        # Create output directory
        output_dir = create_output_directory(args.output_dir)
        logger.info(f"Output directory: {output_dir}")

        # Initialize GeoIP resolver
        logger.info("Initializing GeoIP resolver...")
        geo_resolver = GeoIPResolver(db_path=args.geo_db)

        # Initialize analyzer
        logger.info(f"Initializing analyzer (threshold: {args.speed_threshold} km/h)...")
        analyzer = ImpossibleTravelAnalyzer(
            speed_threshold_kmh=args.speed_threshold,
            geo_resolver=geo_resolver
        )

        # Run analysis
        full_df, impossible_df, stats = analyzer.run_analysis(str(input_path))

        # Save results
        save_results(full_df, impossible_df, stats, output_dir)

        # Generate report
        logger.info("Generating comprehensive report...")
        report_generator = ReportGenerator()
        report_path = output_dir / 'report.md'
        report_generator.generate_full_report(
            impossible_df=impossible_df,
            full_df=full_df,
            stats=stats,
            output_path=str(report_path)
        )

        # Print summary
        print_summary(stats, impossible_df)

        # Success message
        print("Analysis complete! Generated files:")
        print(f"  - {output_dir / 'impossible_travel.csv'}")
        print(f"  - {output_dir / 'full_analysis.csv'}")
        print(f"  - {output_dir / 'report.md'}")
        print("\n")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
