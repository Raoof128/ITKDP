"""
Setup configuration for Impossible Travel Detection Engine.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="impossible-travel-detector",
    version="1.0.0",
    author="Security Engineering Team",
    author_email="security@yourdomain.com",
    description="Security analytics tool for detecting impossible travel patterns in login events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/impossible-travel-detector",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/impossible-travel-detector/issues",
        "Documentation": "https://github.com/yourusername/impossible-travel-detector#readme",
        "Source Code": "https://github.com/yourusername/impossible-travel-detector",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "impossible-travel=main:main",
        ],
    },
    keywords=[
        "security",
        "detection",
        "impossible-travel",
        "siem",
        "azure-sentinel",
        "geolocation",
        "threat-detection",
        "cybersecurity",
        "analytics",
    ],
    license="MIT",
    zip_safe=False,
    include_package_data=True,
)
