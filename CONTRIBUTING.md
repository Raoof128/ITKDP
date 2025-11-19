# Contributing to Impossible Travel Detection Engine

First off, thank you for considering contributing to the Impossible Travel Detection Engine! It's people like you that make this tool valuable for the security community.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples** to demonstrate the steps
* **Describe the behavior you observed** and what behavior you expected
* **Include logs and error messages**
* **Include your environment** (OS, Python version, etc.)

**Bug Report Template:**
```markdown
## Description
[Clear description of the bug]

## Steps to Reproduce
1. [First Step]
2. [Second Step]
3. [etc.]

## Expected Behavior
[What you expected to happen]

## Actual Behavior
[What actually happened]

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.11]
- Package Version: [e.g., 1.0.0]

## Additional Context
[Any additional information, screenshots, logs]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description** of the suggested enhancement
* **Explain why this enhancement would be useful** to most users
* **List some examples** of how it would be used

### Pull Requests

The process described here has several goals:

- Maintain code quality
- Fix problems that are important to users
- Engage the community in working toward the best possible tool
- Enable a sustainable system for maintainers to review contributions

**Pull Request Process:**

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**, following our coding standards (see below)

3. **Add tests** for your changes. The project maintains 100% test coverage on core functionality.

4. **Ensure all tests pass**:
   ```bash
   make test
   ```

5. **Update documentation** as needed (README, docstrings, etc.)

6. **Commit your changes** using clear, descriptive commit messages:
   ```bash
   git commit -m "feat: add new detection algorithm for VPN detection"
   ```

7. **Push to your fork** and submit a pull request

8. **Wait for review**. Maintainers will review your PR and may request changes.

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- git

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/impossible-travel-detector.git
cd impossible-travel-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
make test
```

## Coding Standards

### Python Style Guide

This project follows [PEP 8](https://pep8.org/) with some specific guidelines:

**Code Formatting:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use double quotes for strings

**Naming Conventions:**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Prefix private methods with underscore: `_private_method`

**Type Hints:**
```python
from typing import List, Dict, Optional

def process_events(events: List[Dict[str, str]], threshold: float = 1000.0) -> Optional[Dict]:
    """
    Process login events for impossible travel detection.

    Args:
        events: List of login event dictionaries
        threshold: Speed threshold in km/h

    Returns:
        Analysis results or None if no events

    Raises:
        ValueError: If events list is empty
    """
    pass
```

**Docstrings:**
- Use Google-style docstrings
- Document all public functions and classes
- Include examples for complex functions

**Error Handling:**
```python
# Good
try:
    data = load_data(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
    return None

# Bad
try:
    data = load_data(file_path)
except:
    pass
```

### Testing

**All code contributions must include tests:**

```python
import pytest
from impossible_travel import haversine_distance

class TestHaversineDistance:
    """Test suite for haversine distance calculations."""

    def test_london_to_new_york(self):
        """Test distance from London to New York."""
        distance = haversine_distance(51.5074, -0.1278, 40.7128, -74.0060)
        assert 5500 < distance < 5600

    def test_invalid_coordinates(self):
        """Test handling of invalid coordinates."""
        with pytest.raises(ValueError):
            haversine_distance(91, 0, 0, 0)  # Invalid latitude
```

**Running Tests:**
```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/test_utils.py

# Run in verbose mode
pytest -v
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(detection): add VPN detection capability

Implement VPN detection by analyzing IP address ranges
and adding known VPN provider database lookup.

Closes #42
```

```
fix(geo): handle null coordinates in GeoIP lookup

Previously, null coordinates would cause crashes.
Now returns UNKNOWN location instead.

Fixes #38
```

## Project Structure

```
impossible-travel-detector/
├── main.py                 # CLI entry point
├── analysis.py            # Detection engine
├── geo.py                 # GeoIP resolution
├── report.py              # Report generation
├── utils.py               # Utility functions
├── config.py              # Configuration management
├── tests/                 # Test suite
│   ├── test_utils.py
│   ├── test_geo.py
│   └── test_analysis.py
├── docs/                  # Additional documentation
├── examples/              # Usage examples
└── scripts/               # Utility scripts
```

## Release Process

Releases are managed by project maintainers:

1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Create release tag: `git tag -a v1.0.0 -m "Release version 1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will automatically build and publish

## Getting Help

- **Documentation**: Check the [README](README.md) and [docs/](docs/) folder
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Security**: For security issues, see [SECURITY.md](SECURITY.md)

## Recognition

Contributors are recognized in:
- GitHub contributors graph
- Release notes
- Project README (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making the security community stronger!
