"""
Rasterio Analysis Package - Simplified Version for GIST 604B

This package contains beginner-friendly functions for working with raster data
using the rasterio library. It's designed for GIS professionals learning Python.

Modules:
--------
- raster_basics: Basic raster reading and information extraction
- band_math: Vegetation indices and band calculations
- applications: Practical raster analysis workflows

Author: Student (you!)
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Working with Raster Data
"""

# Import all the functions students need to implement
# This makes them available as: from rasterio_analysis import function_name

from .raster_basics import (
    read_raster_info,
    get_raster_stats,
    get_raster_extent
)

from .band_math import (
    calculate_ndvi,
    analyze_vegetation
)

from .applications import (
    sample_raster_at_points,
    read_remote_raster,
    create_raster_summary
)

# Package metadata
__version__ = "1.0.0"
__author__ = "GIST 604B Student"

# List all available functions
__all__ = [
    # Raster Basics (Part 1)
    'read_raster_info',
    'get_raster_stats',
    'get_raster_extent',

    # Band Math (Part 2)
    'calculate_ndvi',
    'analyze_vegetation',

    # Applications (Part 3)
    'sample_raster_at_points',
    'read_remote_raster',
    'create_raster_summary'
]

print("📦 Rasterio Analysis Package loaded successfully!")
print("🎯 Functions available for Part 1 (Raster Basics):")
print("   - read_raster_info()")
print("   - get_raster_stats()")
print("   - get_raster_extent()")
print("🎯 Functions available for Part 2 (Band Math):")
print("   - calculate_ndvi()")
print("   - analyze_vegetation()")
print("🎯 Functions available for Part 3 (Applications):")
print("   - sample_raster_at_points()")
print("   - read_remote_raster()")
print("   - create_raster_summary()")
