"""
Report generation module for creating markdown analysis reports.
"""
import pandas as pd
from datetime import datetime
from typing import Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates comprehensive markdown reports for impossible travel analysis.
    """

    def __init__(self):
        """Initialize the report generator."""
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_header(self) -> str:
        """
        Generate report header.

        Returns:
            Markdown formatted header
        """
        header = f"""# Impossible Travel Detection Report

**Generated:** {self.timestamp}

---

## Executive Summary

This report presents the findings of an automated impossible travel detection analysis.
Impossible travel occurs when a user account shows login activity from geographically
distant locations within a timeframe that would require physically impossible travel speeds.

### What is Impossible Travel?

Impossible travel is a key security indicator that often suggests:
- **Account Compromise**: Unauthorized access from a different geographic location
- **Credential Sharing**: Multiple users sharing the same account
- **VPN/Proxy Usage**: Legitimate users accessing systems through various endpoints

### Detection Methodology

The analysis uses the following approach:

1. **GeoIP Resolution**: Convert IP addresses to geographic coordinates
2. **Distance Calculation**: Use Haversine formula to calculate great-circle distance
3. **Speed Calculation**: Determine required travel speed between consecutive logins
4. **Threshold Detection**: Flag events exceeding 1000 km/h (typical intercontinental flight: ~900 km/h)

---

"""
        return header

    def generate_statistics_section(self, stats: Dict) -> str:
        """
        Generate statistics section.

        Args:
            stats: Dictionary with summary statistics

        Returns:
            Markdown formatted statistics section
        """
        section = f"""## Key Findings

| Metric | Value |
|--------|-------|
| **Total Login Transitions Analyzed** | {stats['total_events_analyzed']} |
| **Impossible Travel Events Detected** | {stats['impossible_travel_events']} |
| **Affected User Accounts** | {stats['affected_users']} |
| **Detection Rate** | {stats['detection_rate']} |
| **Maximum Speed Detected** | {stats['max_speed_detected']:.2f} km/h |
| **Average Distance Between Logins** | {stats['avg_distance']} km |
| **Speed Threshold Used** | {stats['speed_threshold']} km/h |

"""
        return section

    def generate_impossible_travel_section(self, impossible_df: pd.DataFrame) -> str:
        """
        Generate impossible travel events section.

        Args:
            impossible_df: DataFrame with impossible travel events

        Returns:
            Markdown formatted events section
        """
        if len(impossible_df) == 0:
            section = """## Impossible Travel Events

**No impossible travel events detected.** All login patterns appear normal.

"""
            return section

        section = """## Impossible Travel Events

The following events were flagged as impossible travel:

"""

        # Show top 10 events by speed
        top_events = impossible_df.nlargest(min(10, len(impossible_df)), 'required_speed_kmh')

        section += "### Top Events by Speed\n\n"

        for idx, event in top_events.iterrows():
            section += f"""#### Event #{idx + 1}

- **User ID:** `{event['user_id']}`
- **Travel Path:** {event['previous_location']} → {event['new_location']}
- **Distance:** {event['distance_km']:.2f} km
- **Time Window:** {event['time_diff_hours']:.2f} hours
- **Required Speed:** **{event['required_speed_kmh']:.2f} km/h** ⚠️
- **Previous Login:** {event['previous_timestamp']} from {event['previous_ip']}
- **New Login:** {event['new_timestamp']} from {event['new_ip']}

**Analysis:** This login pattern requires travel at {event['required_speed_kmh']:.2f} km/h, which is {(event['required_speed_kmh'] / 900 * 100):.1f}% of maximum commercial flight speed.

---

"""

        return section

    def generate_affected_users_section(self, impossible_df: pd.DataFrame) -> str:
        """
        Generate affected users section.

        Args:
            impossible_df: DataFrame with impossible travel events

        Returns:
            Markdown formatted users section
        """
        if len(impossible_df) == 0:
            return ""

        section = """## Affected Users Summary

| User ID | Events | Max Speed (km/h) | Locations Involved |
|---------|--------|------------------|-------------------|
"""

        # Group by user
        for user_id, user_events in impossible_df.groupby('user_id'):
            event_count = len(user_events)
            max_speed = user_events['required_speed_kmh'].max()

            # Get unique locations
            locations = set()
            for _, event in user_events.iterrows():
                locations.add(event['previous_location'])
                locations.add(event['new_location'])
            locations = [loc for loc in locations if loc != "UNKNOWN"]

            location_str = ", ".join(locations[:3])
            if len(locations) > 3:
                location_str += f" (+{len(locations) - 3} more)"

            section += f"| `{user_id}` | {event_count} | {max_speed:.2f} | {location_str} |\n"

        section += "\n"
        return section

    def generate_recommendations_section(self, impossible_df: pd.DataFrame) -> str:
        """
        Generate security recommendations section.

        Args:
            impossible_df: DataFrame with impossible travel events

        Returns:
            Markdown formatted recommendations
        """
        section = """## Security Recommendations

Based on the analysis findings:

"""

        if len(impossible_df) == 0:
            section += """### No Immediate Action Required

All login patterns appear normal. Continue monitoring for anomalies.

**Preventive Measures:**
- Maintain regular security awareness training
- Enforce strong password policies
- Consider implementing MFA for all accounts
- Monitor for unusual login times or locations

"""
        else:
            section += f"""### Immediate Actions Required

**{len(impossible_df)} impossible travel event(s) detected** affecting **{impossible_df['user_id'].nunique()} user account(s)**.

**Recommended Actions:**

1. **Account Investigation**
   - Review all flagged accounts for signs of compromise
   - Check for unauthorized access or data exfiltration
   - Verify with users their recent travel and login activity

2. **Access Control**
   - Force password reset for affected accounts
   - Enable Multi-Factor Authentication (MFA)
   - Review and revoke suspicious sessions

3. **Incident Response**
   - Document all flagged events for security audit
   - Correlate with other security logs (VPN, firewall, etc.)
   - Consider escalating high-risk accounts to SOC

4. **Long-term Improvements**
   - Implement automated impossible travel alerts
   - Deploy adaptive authentication based on risk score
   - Enhance monitoring for credential stuffing attacks
   - Review and update geographic access policies

"""

        return section

    def generate_methodology_section(self) -> str:
        """
        Generate methodology section.

        Returns:
            Markdown formatted methodology explanation
        """
        section = """## Technical Methodology

### Distance Calculation

The Haversine formula is used to calculate the great-circle distance between two points on Earth:

```
a = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)
c = 2 · atan2(√a, √(1−a))
d = R · c
```

Where:
- φ is latitude
- λ is longitude
- R is Earth's radius (6,371 km)

### Speed Calculation

```
Required Speed (km/h) = Distance (km) / Time Difference (hours)
```

### Detection Criteria

An event is flagged as impossible travel when:

```
Required Speed > 1000 km/h
```

**Rationale:** Commercial aircraft cruise at approximately 900 km/h. Any required speed
exceeding 1000 km/h indicates either:
- Security incident (account compromise)
- Technical anomaly (clock skew, VPN switching)
- Legitimate edge case (requires manual review)

---

"""
        return section

    def generate_footer(self) -> str:
        """
        Generate report footer.

        Returns:
            Markdown formatted footer
        """
        footer = """## Appendix

### About This Report

This report was generated by the **Impossible Travel Detection Engine**, an automated
security analytics tool that simulates Azure Sentinel / SIEM detection logic.

### References

- [MITRE ATT&CK: Valid Accounts](https://attack.mitre.org/techniques/T1078/)
- [Azure Sentinel: Impossible Travel Detection](https://docs.microsoft.com/en-us/azure/sentinel/)
- [OWASP: Authentication and Session Management](https://owasp.org/www-project-top-ten/)

### Disclaimer

This tool is designed for authorized security testing and monitoring purposes only.
Ensure you have proper authorization before analyzing user login data.

---

**End of Report**
"""
        return footer

    def generate_full_report(self, impossible_df: pd.DataFrame, full_df: pd.DataFrame, stats: Dict, output_path: str = "report.md"):
        """
        Generate the complete markdown report.

        Args:
            impossible_df: DataFrame with impossible travel events
            full_df: DataFrame with full analysis
            stats: Summary statistics dictionary
            output_path: Output file path for the report
        """
        logger.info("Generating comprehensive markdown report...")

        report_content = ""
        report_content += self.generate_header()
        report_content += self.generate_statistics_section(stats)
        report_content += self.generate_impossible_travel_section(impossible_df)
        report_content += self.generate_affected_users_section(impossible_df)
        report_content += self.generate_recommendations_section(impossible_df)
        report_content += self.generate_methodology_section()
        report_content += self.generate_footer()

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"Report saved to: {output_path}")

        return report_content
