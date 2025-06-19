#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding CLI - Python Package
Terminal tabanlı AI geliştirme aracı
"""

__version__ = "1.0.0"
__author__ = "VibeCoding Team"
__email__ = "info@vibecoding.com"
__description__ = "Terminal tabanlı AI geliştirme aracı - Claude Code benzeri"

# Ana CLI sınıfını import et
try:
    from .vibe_cli import VibeCodingCLI, main
except ImportError:
    from vibe_cli import VibeCodingCLI, main

__all__ = ["VibeCodingCLI", "main", "__version__"] 