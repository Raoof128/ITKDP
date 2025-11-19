# API Documentation

## Module: config.py

### Configuration Management

#### `DetectionConfig`

Data class for detection configuration.

```python
@dataclass
class DetectionConfig:
    speed_threshold_kmh: float = 1000.0
    min_time_diff_minutes: float = 1.0
    geo_db_path: Optional[str] = None
    use_mock_geo_data: bool = True
    output_directory: str = "."
    csv_output_enabled: bool = True
    markdown_report_enabled: bool = True
    log_level: str = "INFO"
    batch_size: int = 1000
    enable_caching: bool = True
```

**Class Methods:**

##### `from_env() -> DetectionConfig`

Create configuration from environment variables.

**Returns:**
- `DetectionConfig`: Configuration instance

**Environment Variables:**
- `ITKDP_SPEED_THRESHOLD`: Speed threshold in km/h
- `ITKDP_MIN_TIME_DIFF`: Minimum time difference in minutes
- `ITKDP_GEO_DB_PATH`: Path to GeoIP database
- `ITKDP_USE_MOCK_DATA`: Use mock GeoIP data (true/false)
- `ITKDP_OUTPUT_DIR`: Output directory path
- `ITKDP_LOG_LEVEL`: Logging level
- `ITKDP_BATCH_SIZE`: Batch processing size
- `ITKDP_ENABLE_CACHE`: Enable caching (true/false)

**Example:**
```python
config = DetectionConfig.from_env()
```

##### `validate() -> None`

Validate configuration parameters.

**Raises:**
- `ValueError`: If configuration is invalid

---

#### `get_config() -> DetectionConfig`

Get the global configuration singleton instance.

**Returns:**
- `DetectionConfig`: Global configuration

**Example:**
```python
from config import get_config

config = get_config()
print(f"Speed threshold: {config.speed_threshold_kmh} km/h")
```

#### `set_config(config: DetectionConfig) -> None`

Set the global configuration instance.

**Parameters:**
- `config` (DetectionConfig): Configuration to set

**Example:**
```python
from config import DetectionConfig, set_config

custom_config = DetectionConfig(speed_threshold_kmh=1200.0)
set_config(custom_config)
```

---

## Module: geo.py

### GeoIP Resolution

#### `GeoLocation`

Data class representing a geographic location.

```python
@dataclass
class GeoLocation:
    latitude: float
    longitude: float
    city: str
    country: str
    ip_address: str
```

**Attributes:**
- `latitude` (float): Latitude in degrees
- `longitude` (float): Longitude in degrees
- `city` (str): City name or "UNKNOWN"
- `country` (str): Country name or "UNKNOWN"
- `ip_address` (str): Original IP address

---

#### `GeoIPResolver`

Resolves IP addresses to geographic locations.

```python
class GeoIPResolver:
    def __init__(self, db_path: Optional[str] = None)
    def resolve(self, ip_address: str) -> GeoLocation
    def close(self) -> None
```

##### `__init__(db_path: Optional[str] = None)`

Initialize the GeoIP resolver.

**Parameters:**
- `db_path` (Optional[str]): Path to GeoLite2-City.mmdb database

**Example:**
```python
# Use mock database (default)
resolver = GeoIPResolver()

# Use real GeoIP database
resolver = GeoIPResolver(db_path="/path/to/GeoLite2-City.mmdb")
```

##### `resolve(ip_address: str) -> GeoLocation`

Resolve an IP address to geographic location.

**Parameters:**
- `ip_address` (str): IP address to resolve

**Returns:**
- `GeoLocation`: Location information

**Example:**
```python
resolver = GeoIPResolver()
location = resolver.resolve("203.0.113.1")
print(f"{location.city}, {location.country}")
# Output: Sydney, Australia
```

##### `close() -> None`

Close the GeoIP database reader.

**Example:**
```python
resolver = GeoIPResolver()
# ... use resolver ...
resolver.close()
```

**Context Manager Support:**
```python
with GeoIPResolver() as resolver:
    location = resolver.resolve("203.0.113.1")
    print(location.city)
```

---

## Module: utils.py

### Utility Functions

#### `haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float`

Calculate great-circle distance between two points on Earth.

**Parameters:**
- `lat1` (float): Latitude of first point (degrees)
- `lon1` (float): Longitude of first point (degrees)
- `lat2` (float): Latitude of second point (degrees)
- `lon2` (float): Longitude of second point (degrees)

**Returns:**
- `float`: Distance in kilometers (rounded to 2 decimal places)

**Example:**
```python
# London to New York
distance = haversine_distance(51.5074, -0.1278, 40.7128, -74.0060)
print(f"{distance} km")  # ~5570.22 km
```

**Formula:**
```
a = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)
c = 2 · atan2(√a, √(1−a))
d = R · c  (R = 6371 km)
```

---

#### `calculate_time_diff_hours(timestamp1: str, timestamp2: str) -> float`

Calculate time difference between two timestamps.

**Parameters:**
- `timestamp1` (str): Earlier timestamp (ISO format)
- `timestamp2` (str): Later timestamp (ISO format)

**Returns:**
- `float`: Time difference in hours (rounded to 2 decimal places)

**Example:**
```python
time_diff = calculate_time_diff_hours(
    "2025-01-15T10:00:00",
    "2025-01-15T12:30:00"
)
print(f"{time_diff} hours")  # 2.5 hours
```

---

#### `calculate_required_speed(distance_km: float, time_hours: float) -> float`

Calculate required travel speed.

**Parameters:**
- `distance_km` (float): Distance in kilometers
- `time_hours` (float): Time in hours

**Returns:**
- `float`: Speed in km/h (rounded to 2 decimal places)
  - Returns `float('inf')` if `time_hours` is zero

**Example:**
```python
speed = calculate_required_speed(1000, 2)
print(f"{speed} km/h")  # 500.0 km/h
```

---

#### `format_location(city: str, country: str) -> str`

Format location string for display.

**Parameters:**
- `city` (str): City name
- `country` (str): Country name

**Returns:**
- `str`: Formatted location string

**Example:**
```python
location = format_location("London", "United Kingdom")
print(location)  # "London, United Kingdom"

unknown = format_location("UNKNOWN", "UNKNOWN")
print(unknown)  # "UNKNOWN"
```

---

## Module: analysis.py

### Detection Engine

#### `ImpossibleTravelAnalyzer`

Main analysis engine for impossible travel detection.

```python
class ImpossibleTravelAnalyzer:
    def __init__(
        self,
        speed_threshold_kmh: float = 1000.0,
        geo_resolver: Optional[GeoIPResolver] = None
    )
    def load_login_data(self, csv_path: str) -> pd.DataFrame
    def enrich_with_geolocation(self, df: pd.DataFrame) -> pd.DataFrame
    def analyze_travel_patterns(self, df: pd.DataFrame) -> pd.DataFrame
    def filter_impossible_travel(self, df: pd.DataFrame) -> pd.DataFrame
    def get_summary_statistics(
        self,
        full_df: pd.DataFrame,
        impossible_df: pd.DataFrame
    ) -> Dict
    def run_analysis(self, csv_path: str) -> tuple
```

##### `__init__(speed_threshold_kmh: float = 1000.0, geo_resolver: Optional[GeoIPResolver] = None)`

Initialize the analyzer.

**Parameters:**
- `speed_threshold_kmh` (float): Speed threshold in km/h (default: 1000.0)
- `geo_resolver` (Optional[GeoIPResolver]): Custom GeoIP resolver

**Example:**
```python
# Default configuration
analyzer = ImpossibleTravelAnalyzer()

# Custom threshold
analyzer = ImpossibleTravelAnalyzer(speed_threshold_kmh=1200.0)

# Custom resolver
custom_resolver = GeoIPResolver(db_path="/custom/path")
analyzer = ImpossibleTravelAnalyzer(geo_resolver=custom_resolver)
```

##### `load_login_data(csv_path: str) -> pd.DataFrame`

Load login events from CSV file.

**Parameters:**
- `csv_path` (str): Path to CSV file

**Returns:**
- `pd.DataFrame`: Login events DataFrame

**Required CSV Columns:**
- `user_id`: User identifier
- `timestamp`: ISO format timestamp
- `ip_address`: IP address

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If required columns are missing

**Example:**
```python
df = analyzer.load_login_data("logins.csv")
print(f"Loaded {len(df)} events")
```

##### `enrich_with_geolocation(df: pd.DataFrame) -> pd.DataFrame`

Enrich login events with geographic location data.

**Parameters:**
- `df` (pd.DataFrame): DataFrame with login events

**Returns:**
- `pd.DataFrame`: Enriched DataFrame with geo columns
  - `latitude`: Geographic latitude
  - `longitude`: Geographic longitude
  - `city`: City name
  - `country`: Country name

**Example:**
```python
df = analyzer.load_login_data("logins.csv")
enriched_df = analyzer.enrich_with_geolocation(df)
print(enriched_df[['user_id', 'city', 'country']].head())
```

##### `analyze_travel_patterns(df: pd.DataFrame) -> pd.DataFrame`

Analyze travel patterns for each user.

**Parameters:**
- `df` (pd.DataFrame): Enriched DataFrame with geolocation

**Returns:**
- `pd.DataFrame`: Analysis results with columns:
  - `user_id`: User identifier
  - `previous_location`: Previous login location
  - `new_location`: Current login location
  - `previous_ip`: Previous IP address
  - `new_ip`: Current IP address
  - `previous_timestamp`: Previous login time
  - `new_timestamp`: Current login time
  - `distance_km`: Distance in kilometers
  - `time_diff_hours`: Time difference in hours
  - `required_speed_kmh`: Required travel speed
  - `is_impossible_travel`: Boolean flag

**Example:**
```python
df = analyzer.load_login_data("logins.csv")
enriched_df = analyzer.enrich_with_geolocation(df)
analysis_df = analyzer.analyze_travel_patterns(enriched_df)
print(f"Analyzed {len(analysis_df)} login transitions")
```

##### `filter_impossible_travel(df: pd.DataFrame) -> pd.DataFrame`

Filter only impossible travel events.

**Parameters:**
- `df` (pd.DataFrame): Full analysis DataFrame

**Returns:**
- `pd.DataFrame`: Impossible travel events only

**Example:**
```python
impossible_df = analyzer.filter_impossible_travel(analysis_df)
print(f"Found {len(impossible_df)} impossible travel events")
```

##### `get_summary_statistics(full_df: pd.DataFrame, impossible_df: pd.DataFrame) -> Dict`

Calculate summary statistics.

**Parameters:**
- `full_df` (pd.DataFrame): Full analysis DataFrame
- `impossible_df` (pd.DataFrame): Impossible travel DataFrame

**Returns:**
- `Dict`: Statistics dictionary with keys:
  - `total_events_analyzed`: Total login transitions
  - `impossible_travel_events`: Number of impossible travel events
  - `affected_users`: Number of affected users
  - `detection_rate`: Detection rate as percentage
  - `max_speed_detected`: Maximum speed detected
  - `avg_distance`: Average distance between logins
  - `speed_threshold`: Configured threshold

**Example:**
```python
stats = analyzer.get_summary_statistics(full_df, impossible_df)
print(f"Detection rate: {stats['detection_rate']}")
```

##### `run_analysis(csv_path: str) -> tuple`

Run the complete analysis pipeline.

**Parameters:**
- `csv_path` (str): Path to login events CSV

**Returns:**
- `tuple`: (full_analysis_df, impossible_travel_df, statistics)

**Example:**
```python
analyzer = ImpossibleTravelAnalyzer()
full_df, impossible_df, stats = analyzer.run_analysis("logins.csv")

print(f"Total events: {stats['total_events_analyzed']}")
print(f"Impossible travel: {stats['impossible_travel_events']}")
```

---

## Module: report.py

### Report Generation

#### `ReportGenerator`

Generates comprehensive markdown reports.

```python
class ReportGenerator:
    def generate_full_report(
        self,
        impossible_df: pd.DataFrame,
        full_df: pd.DataFrame,
        stats: Dict,
        output_path: str = "report.md"
    ) -> str
```

##### `generate_full_report(...) -> str`

Generate complete markdown report.

**Parameters:**
- `impossible_df` (pd.DataFrame): Impossible travel events
- `full_df` (pd.DataFrame): Full analysis results
- `stats` (Dict): Summary statistics
- `output_path` (str): Output file path (default: "report.md")

**Returns:**
- `str`: Generated report content

**Report Sections:**
1. Executive Summary
2. Key Findings (statistics)
3. Impossible Travel Events (top events)
4. Affected Users Summary
5. Security Recommendations
6. Technical Methodology
7. References & Disclaimer

**Example:**
```python
reporter = ReportGenerator()
report_content = reporter.generate_full_report(
    impossible_df=impossible_df,
    full_df=full_df,
    stats=stats,
    output_path="./output/report.md"
)
print("Report generated successfully")
```

---

## Complete Usage Example

```python
from impossible_travel import (
    ImpossibleTravelAnalyzer,
    ReportGenerator,
    DetectionConfig,
    get_config
)

# Configure
config = DetectionConfig(
    speed_threshold_kmh=1200.0,
    output_directory="./results"
)

# Analyze
analyzer = ImpossibleTravelAnalyzer(
    speed_threshold_kmh=config.speed_threshold_kmh
)

full_df, impossible_df, stats = analyzer.run_analysis("logins.csv")

# Generate report
reporter = ReportGenerator()
reporter.generate_full_report(
    impossible_df=impossible_df,
    full_df=full_df,
    stats=stats,
    output_path=f"{config.output_directory}/report.md"
)

# Save CSVs
impossible_df.to_csv(f"{config.output_directory}/impossible_travel.csv", index=False)
full_df.to_csv(f"{config.output_directory}/full_analysis.csv", index=False)

print(f"Analysis complete!")
print(f"Events detected: {stats['impossible_travel_events']}")
print(f"Affected users: {stats['affected_users']}")
```

---

## Error Handling

All modules implement proper error handling:

```python
try:
    analyzer = ImpossibleTravelAnalyzer()
    full_df, impossible_df, stats = analyzer.run_analysis("logins.csv")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid data: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    logger.error(f"Analysis failed: {e}", exc_info=True)
```

---

**Last Updated:** 2025-01-19
