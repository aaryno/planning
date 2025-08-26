"""
GIST 604B - Python GeoPandas Introduction
Source Package

This package contains the spatial data fundamental functions for the GeoPandas
introduction assignment.

Author: GIST 604B Course Team
"""

__version__ = "1.0.0"
__author__ = "GIST 604B Course Team"

# Package-level imports for convenience
from .spatial_basics import (
    load_spatial_dataset,
    explore_spatial_properties,
    validate_spatial_data,
    standardize_crs
)

__all__ = [
    "load_spatial_dataset",
    "explore_spatial_properties",
    "validate_spatial_data",
    "standardize_crs"
]
