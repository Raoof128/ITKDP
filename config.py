"""
Configuration management for Impossible Travel Detection Engine.

This module centralizes all configuration parameters, making the application
more maintainable and easier to deploy in different environments.
"""
import os
from typing import Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DetectionConfig:
    """Configuration for impossible travel detection."""

    # Detection thresholds
    speed_threshold_kmh: float = 1000.0
    min_time_diff_minutes: float = 1.0

    # GeoIP configuration
    geo_db_path: Optional[str] = None
    use_mock_geo_data: bool = True

    # Output configuration
    output_directory: str = "."
    csv_output_enabled: bool = True
    markdown_report_enabled: bool = True

    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Performance configuration
    batch_size: int = 1000
    enable_caching: bool = True

    @classmethod
    def from_env(cls) -> 'DetectionConfig':
        """
        Create configuration from environment variables.

        Returns:
            DetectionConfig instance with values from environment
        """
        return cls(
            speed_threshold_kmh=float(os.getenv('ITKDP_SPEED_THRESHOLD', '1000.0')),
            min_time_diff_minutes=float(os.getenv('ITKDP_MIN_TIME_DIFF', '1.0')),
            geo_db_path=os.getenv('ITKDP_GEO_DB_PATH'),
            use_mock_geo_data=os.getenv('ITKDP_USE_MOCK_DATA', 'true').lower() == 'true',
            output_directory=os.getenv('ITKDP_OUTPUT_DIR', '.'),
            log_level=os.getenv('ITKDP_LOG_LEVEL', 'INFO'),
            batch_size=int(os.getenv('ITKDP_BATCH_SIZE', '1000')),
            enable_caching=os.getenv('ITKDP_ENABLE_CACHE', 'true').lower() == 'true',
        )

    def validate(self) -> None:
        """
        Validate configuration parameters.

        Raises:
            ValueError: If configuration is invalid
        """
        if self.speed_threshold_kmh <= 0:
            raise ValueError("Speed threshold must be positive")

        if self.min_time_diff_minutes < 0:
            raise ValueError("Minimum time difference must be non-negative")

        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")

        if self.log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError(f"Invalid log level: {self.log_level}")

        # Validate output directory exists or can be created
        output_path = Path(self.output_directory)
        output_path.mkdir(parents=True, exist_ok=True)


@dataclass
class AppInfo:
    """Application metadata."""

    name: str = "Impossible Travel Detection Engine"
    version: str = "1.0.0"
    description: str = "Security analytics tool for detecting impossible travel patterns"
    author: str = "Security Engineering Team"
    license: str = "MIT"
    repository: str = "https://github.com/yourusername/impossible-travel-detector"


# Singleton configuration instance
_config: Optional[DetectionConfig] = None


def get_config() -> DetectionConfig:
    """
    Get the global configuration instance.

    Returns:
        DetectionConfig singleton instance
    """
    global _config
    if _config is None:
        _config = DetectionConfig.from_env()
        _config.validate()
    return _config


def set_config(config: DetectionConfig) -> None:
    """
    Set the global configuration instance.

    Args:
        config: Configuration to set as global
    """
    global _config
    config.validate()
    _config = config
