# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Impossible Travel Detection Engine team takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:

**[security@yourdomain.com]** (Update with your actual security contact)

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

Please include the following information in your report:

* Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

### What to Expect

* **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
* **Communication**: We will send you regular updates about our progress
* **Verification**: We will work with you to understand and verify the issue
* **Fix Development**: We will develop a fix for the vulnerability
* **Disclosure**: We will coordinate with you on the disclosure timeline

### Disclosure Policy

* **Coordinated Disclosure**: We practice coordinated disclosure
* **Timeline**: We aim to patch critical vulnerabilities within 90 days
* **Credit**: Security researchers who responsibly disclose vulnerabilities will be credited (unless you prefer to remain anonymous)
* **CVE**: Critical vulnerabilities will be assigned CVE identifiers when applicable

## Security Best Practices

### For Users

When using the Impossible Travel Detection Engine, follow these security best practices:

**1. Data Privacy**
* Only analyze login data you are authorized to access
* Ensure compliance with GDPR, CCPA, and relevant data protection regulations
* Anonymize sensitive user data when possible
* Implement proper access controls on output files

**2. Deployment Security**
* Run the tool in isolated environments for sensitive data
* Use environment variables for configuration (not hard-coded values)
* Secure output directories with appropriate permissions
* Regularly update to the latest version for security patches

**3. API Keys and Credentials**
* Never commit API keys, passwords, or credentials to version control
* Use environment variables or secure vaults for sensitive configuration
* Rotate credentials regularly
* Use read-only API keys when possible

**4. Input Validation**
* Validate CSV input files before processing
* Sanitize file paths to prevent directory traversal attacks
* Implement file size limits to prevent resource exhaustion
* Verify data integrity with checksums when applicable

**5. Logging and Monitoring**
* Review logs regularly for suspicious activity
* Implement log rotation to prevent disk exhaustion
* Ensure logs don't contain sensitive user data
* Monitor for unusual resource consumption patterns

### For Developers

**1. Secure Coding Practices**
* Follow OWASP secure coding guidelines
* Validate all inputs
* Use parameterized queries (if database features added)
* Implement proper error handling (don't expose stack traces to users)
* Use cryptographically secure random number generators when needed

**2. Dependency Management**
* Keep all dependencies up to date
* Use `pip-audit` or similar tools to check for vulnerable dependencies
* Pin dependency versions in `requirements.txt`
* Review dependencies before adding new ones

**3. Code Review**
* All code changes must be reviewed before merging
* Security-sensitive changes require review by a security-aware developer
* Use automated security scanning tools in CI/CD pipeline

**4. Testing**
* Write security-focused test cases
* Test with malformed/malicious inputs
* Perform fuzzing on input parsers
* Conduct regular penetration testing

## Known Security Considerations

### 1. GeoIP Database

The default configuration uses a mock GeoIP database for demonstration. In production:

* Use official MaxMind GeoLite2 database
* Keep the database updated regularly
* Implement proper licensing compliance
* Consider privacy implications of IP geolocation

### 2. Log Files

Log files may contain sensitive information:

* User IDs
* IP addresses
* Timestamps
* Geographic locations

**Recommendations:**
* Implement log rotation and retention policies
* Secure log storage with encryption
* Limit access to logs via file permissions
* Consider anonymizing sensitive data in logs

### 3. CSV Input Files

CSV files may contain PII (Personally Identifiable Information):

* User identifiers
* IP addresses
* Login timestamps

**Recommendations:**
* Validate CSV structure before processing
* Implement data retention policies
* Use encryption for CSV files at rest
* Secure transmission of CSV files (use HTTPS, SFTP)

### 4. Output Files

Generated reports contain sensitive security information:

* Impossible travel detections
* User behavior patterns
* Geographic location data

**Recommendations:**
* Restrict output file permissions (chmod 600)
* Store output files in secure locations
* Implement access logging for output files
* Delete output files after analysis is complete

## Vulnerability Response Process

### Internal Process

1. **Triage** (24 hours)
   - Assess severity (Critical, High, Medium, Low)
   - Assign to appropriate developer
   - Create private security advisory

2. **Investigation** (1-3 days)
   - Reproduce the vulnerability
   - Determine affected versions
   - Assess impact and exploitability

3. **Fix Development** (1-2 weeks for critical, longer for lower severity)
   - Develop and test fix
   - Create regression tests
   - Prepare security advisory

4. **Release** (Coordinated with reporter)
   - Deploy fix to all affected versions
   - Publish security advisory
   - Update documentation
   - Notify users via security mailing list

### Severity Classification

**Critical**
* Remote code execution
* Authentication bypass
* Privilege escalation
* Data breach potential

**High**
* Denial of service
* Information disclosure of sensitive data
* CSRF allowing significant actions

**Medium**
* XSS vulnerabilities
* Non-critical information disclosure
* Security misconfigurations

**Low**
* Minor information leakage
* Non-exploitable vulnerabilities
* Issues requiring significant prerequisites

## Security Hall of Fame

We recognize security researchers who have responsibly disclosed vulnerabilities:

(This section will be updated as researchers contribute)

## Contact

For security-related questions or concerns:
* Email: security@yourdomain.com
* For general bugs (non-security): Use GitHub Issues
* For questions: Use GitHub Discussions

## Additional Resources

* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* [CWE Top 25](https://cwe.mitre.org/top25/)
* [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

Last Updated: 2025-01-19
