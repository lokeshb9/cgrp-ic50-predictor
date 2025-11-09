"""
Setup Script for CGRP Predictor
================================

Professional package installation configuration.

Usage:
    pip install -e .              # Development install
    pip install .                 # Production install
    pip install -e ".[dev]"       # With development dependencies

Author: Dani Geiger
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text().strip().split('\n')
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]

# Read development requirements
dev_requirements_path = Path(__file__).parent / "requirements-dev.txt"
dev_requirements = []
if dev_requirements_path.exists():
    dev_requirements = dev_requirements_path.read_text().strip().split('\n')
    dev_requirements = [r.strip() for r in dev_requirements if r.strip() and not r.startswith('#')]

setup(
    name="cgrp-predictor",
    version="1.0.0",
    author="Dani Geiger",
    author_email="dani.geiger@example.com",
    description="ML-powered IC50 prediction for CGRP receptor antagonists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danigeiger/CGRP_gepant_ML_project",
    project_urls={
        "Bug Reports": "https://github.com/danigeiger/CGRP_gepant_ML_project/issues",
        "Source": "https://github.com/danigeiger/CGRP_gepant_ML_project",
        "Documentation": "https://github.com/danigeiger/CGRP_gepant_ML_project/blob/main/README.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
        "docs": [
            "sphinx>=7.2.6",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cgrp-predict=cgrp_predictor.cli:main",  # Future CLI tool
        ],
    },
    include_package_data=True,
    package_data={
        "cgrp_predictor": ["../config/*.yaml"],
    },
    zip_safe=False,
    keywords=[
        "machine-learning",
        "drug-discovery",
        "bioinformatics",
        "cgrp",
        "ic50",
        "molecular-fingerprints",
        "cheminformatics",
        "migraine-research",
    ],
)

