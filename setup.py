#!/usr/bin/env python3
"""
VibeCoding CLI - Setup Script
Global kurulum için setuptools konfigürasyonu
"""

from setuptools import setup, find_packages
import os

# README dosyasını oku
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Requirements dosyasını oku
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vibe-coding-cli",
    version="1.0.0",
    author="VibeCoding Team",
    author_email="info@vibecoding.com",
    description="Terminal tabanlı AI geliştirme aracı - Claude Code benzeri",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/vibecoding/vibe-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "vibe=vibe_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords="ai, cli, code-generation, development-tools, vibecoding",
    project_urls={
        "Bug Reports": "https://github.com/vibecoding/vibe-cli/issues",
        "Source": "https://github.com/vibecoding/vibe-cli",
        "Documentation": "https://github.com/vibecoding/vibe-cli/blob/main/README.md",
    },
) 