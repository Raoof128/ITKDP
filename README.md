# Impossible Travel Detection Engine

A Python-based security analytics tool that detects impossible travel patterns in user login events, simulating Azure Sentinel KQL detection logic for identifying potential account compromises and security anomalies.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/security-SIEM%20simulation-red.svg)

## Overview

**Impossible Travel** occurs when a user account shows login activity from geographically distant locations within a timeframe that would require physically impossible travel speeds. This is a critical security indicator often suggesting:

- **Account Compromise**: Unauthorized access from different geographic locations
- **Credential Sharing**: Multiple users sharing the same credentials
- **VPN/Proxy Usage**: Legitimate users accessing systems through various endpoints
- **Identity Theft**: Attackers using stolen credentials

This tool replicates the logic used in enterprise SIEM solutions like Azure Sentinel, Microsoft Defender, and Splunk, but runs locally without requiring expensive cloud infrastructure.

## How It Works

```
┌─────────────────┐
│  Login Events   │
│   (CSV Input)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GeoIP Lookup   │ ◄── Resolves IP → Lat/Lon coordinates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Distance Calc   │ ◄── Haversine formula
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Speed Check    │ ◄── Distance / Time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Detection Logic │ ◄── Speed > 1000 km/h?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Report & CSV   │
│   Output Files  │
└─────────────────┘
```

### Detection Methodology

1. **GeoIP Resolution**: Convert IP addresses to geographic coordinates (latitude/longitude)
2. **Distance Calculation**: Use Haversine formula to calculate great-circle distance between login locations
3. **Speed Calculation**: Determine required travel speed: `speed = distance_km / time_hours`
4. **Threshold Detection**: Flag events where `required_speed > 1000 km/h`

**Rationale**: Commercial aircraft cruise at approximately 900 km/h. Any required speed exceeding 1000 km/h indicates a potential security incident.

## Features

- **GeoIP Resolution**: Resolve IP addresses to cities and coordinates
- **Haversine Distance Calculation**: Accurate geographic distance computation
- **Automated Detection**: Configurable speed threshold for impossible travel
- **Comprehensive Reporting**: CSV outputs and detailed markdown reports
- **Professional Analysis**: Security recommendations and affected user summaries
- **Extensible Architecture**: Easy to integrate with real GeoIP databases

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/impossible-travel-detector.git
cd impossible-travel-detector

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Optional: Real GeoIP Database

For production use with real IP addresses, download the MaxMind GeoLite2 database:

```bash
# Download from MaxMind (requires free account)
# https://dev.maxmind.com/geoip/geolite2-free-geolocation-data

# Extract to project directory
tar -xzf GeoLite2-City.tar.gz
```

## Usage

### Basic Usage

```bash
python main.py sample_logins.csv
```

### Advanced Options

```bash
# Specify output directory
python main.py logins.csv --output-dir ./results

# Custom speed threshold (e.g., 1200 km/h)
python main.py logins.csv --speed-threshold 1200

# Use real GeoIP database
python main.py logins.csv --geo-db GeoLite2-City.mmdb

# Enable verbose logging
python main.py logins.csv --verbose
```

### Input Format

Your CSV file should have the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `user_id` | User identifier | alice |
| `timestamp` | ISO format timestamp | 2025-01-15T08:00:00 |
| `ip_address` | IPv4 address | 203.0.113.1 |

**Example CSV:**

```csv
user_id,timestamp,ip_address
alice,2025-01-15T08:00:00,203.0.113.1
alice,2025-01-15T08:45:00,203.0.113.2
bob,2025-01-15T09:00:00,203.0.113.4
```

### Output Files

The tool generates three output files:

1. **`impossible_travel.csv`** - Only flagged impossible travel events
2. **`full_analysis.csv`** - Complete analysis of all login transitions
3. **`report.md`** - Comprehensive markdown report with security recommendations

## Example Output

```
======================================================================
IMPOSSIBLE TRAVEL DETECTION ENGINE
Simulating Azure Sentinel KQL Detection Logic
======================================================================

2025-01-15 10:30:15 - INFO - Loaded 30 login events from sample_logins.csv
2025-01-15 10:30:15 - INFO - Enriched 30 events with geolocation data
2025-01-15 10:30:15 - INFO - Analyzed 20 login transitions
2025-01-15 10:30:15 - INFO - Found 5 impossible travel events

======================================================================
IMPOSSIBLE TRAVEL DETECTION SUMMARY
======================================================================
Total Login Transitions Analyzed: 20
Impossible Travel Events Detected: 5
Affected User Accounts: 4
Detection Rate: 25.00%
Speed Threshold: 1000 km/h
======================================================================

TOP 5 IMPOSSIBLE TRAVEL EVENTS:

  User: alice
  Path: Sydney, Australia → London, United Kingdom
  Speed Required: 25856.44 km/h
  Distance: 17050.96 km in 0.75 hours

  User: eve
  Path: Dubai, United Arab Emirates → Johannesburg, South Africa
  Speed Required: 15392.40 km/h
  Distance: 7696.20 km in 0.50 hours

⚠️  WARNING: Potential security incidents detected!
Review the report.md file for detailed analysis and recommendations.
```

## Project Structure

```
impossible-travel-detector/
├── main.py                 # Main orchestrator
├── analysis.py            # Core detection engine
├── geo.py                 # GeoIP resolution logic
├── report.py              # Report generation
├── utils.py               # Utility functions (Haversine, etc.)
├── sample_logins.csv      # Sample data for testing
├── requirements.txt       # Python dependencies
├── tests/                 # Unit tests
│   ├── test_utils.py
│   ├── test_geo.py
│   └── test_analysis.py
├── LICENSE                # MIT License
└── README.md              # This file
```

## Technical Details

### Haversine Formula

The great-circle distance between two points on Earth is calculated using:

```python
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
```

### Speed Calculation

```python
required_speed = distance_km / time_diff_hours
is_impossible = required_speed > speed_threshold
```

## Use Cases

### Security Operations Center (SOC)

- Monitor user login patterns for anomalies
- Detect compromised accounts in real-time
- Generate incident reports for investigation

### Compliance and Auditing

- Analyze historical login data for security audits
- Demonstrate security monitoring capabilities
- Document detection methodologies

### Security Research

- Study geographic login patterns
- Test detection algorithms
- Develop threat intelligence

### Educational Purposes

- Learn SIEM detection logic
- Understand geographic calculations
- Practice security analytics with Python

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_utils.py
```

## Security Considerations

- **Authorization Required**: Only analyze login data you are authorized to access
- **Data Privacy**: Ensure compliance with GDPR, CCPA, and relevant regulations
- **False Positives**: VPN usage and legitimate travel can trigger alerts
- **Manual Review**: Always review flagged events with human judgment

## Limitations

- **Mock Database**: Default configuration uses test IP addresses
- **Speed Threshold**: May need tuning for specific environments
- **Time Zones**: Assumes timestamps are in consistent format
- **VPN Detection**: Cannot distinguish between VPN usage and actual compromise

## Roadmap

- [ ] Support for IPv6 addresses
- [ ] Integration with real-time log sources (Syslog, API)
- [ ] Machine learning-based anomaly scoring
- [ ] Web dashboard for visualization
- [ ] Email alerting for detected incidents
- [ ] Integration with ticketing systems (Jira, ServiceNow)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **MaxMind GeoLite2**: Free GeoIP database
- **Azure Sentinel**: Inspiration for detection logic
- **MITRE ATT&CK**: Framework for understanding attack patterns

## References

- [MITRE ATT&CK: Valid Accounts (T1078)](https://attack.mitre.org/techniques/T1078/)
- [Azure Sentinel Impossible Travel Detection](https://docs.microsoft.com/en-us/azure/sentinel/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula)

## Author

Security Engineering Project

## Resume Summary

> **Developed an Impossible Travel Detection Engine using Python, GeoIP2, and Pandas to simulate Azure Sentinel KQL analytics logic and identify high-risk identity anomalies.**

---

**Disclaimer**: This tool is designed for authorized security testing and monitoring purposes only. Ensure you have proper authorization before analyzing user login data.
