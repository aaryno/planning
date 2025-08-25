"""
GeoPandas Analysis Tests Package
================================

This package contains automated tests for the GeoPandas analysis assignment.
These tests verify that your spatial analysis functions work correctly and
help you understand what each function should do.

Test Structure:
- test_spatial_data_loading.py: Tests for loading and exploring spatial data
- test_geometric_operations.py: Tests for spatial measurements and transformations
- test_spatial_joins_analysis.py: Tests for spatial relationships and joins
- test_visualization_mapping.py: Tests for map creation and visualization

Running Tests:
- All tests: pytest tests/
- Specific module: pytest tests/test_spatial_data_loading.py
- Verbose output: pytest tests/ -v
- With coverage: pytest tests/ --cov=src

The tests use sample spatial datasets and verify that your functions:
1. Handle edge cases (empty data, missing CRS, etc.)
2. Produce correct spatial analysis results
3. Return data in the expected format
4. Include appropriate metadata and error handling
"""

__version__ = "0.1.0"

# Test configuration
import pytest
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path

# Suppress common warnings during testing
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyproj")
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Common test utilities
def assert_gdf_equal(gdf1, gdf2, check_crs=True, check_geom_type=True):
    """Assert that two GeoDataFrames are equal."""
    assert len(gdf1) == len(gdf2), f"Length mismatch: {len(gdf1)} != {len(gdf2)}"

    if check_crs:
        assert gdf1.crs == gdf2.crs, f"CRS mismatch: {gdf1.crs} != {gdf2.crs}"

    if check_geom_type:
        assert gdf1.geometry.geom_type.equals(gdf2.geometry.geom_type), "Geometry types don't match"

def create_test_points():
    """Create sample point data for testing."""
    points = gpd.GeoDataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Point A', 'Point B', 'Point C', 'Point D'],
        'value': [10, 20, 30, 40],
        'geometry': gpd.points_from_xy([0, 1, 2, 3], [0, 1, 2, 3])
    }, crs='EPSG:4326')
    return points

def create_test_polygons():
    """Create sample polygon data for testing."""
    from shapely.geometry import Polygon

    polygons = gpd.GeoDataFrame({
        'id': [1, 2],
        'name': ['Polygon A', 'Polygon B'],
        'area_value': [100, 200],
        'geometry': [
            Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
            Polygon([(1, 1), (4, 1), (4, 4), (1, 4)])
        ]
    }, crs='EPSG:4326')
    return polygons

def create_test_lines():
    """Create sample line data for testing."""
    from shapely.geometry import LineString

    lines = gpd.GeoDataFrame({
        'id': [1, 2],
        'name': ['Line A', 'Line B'],
        'length_value': [50, 75],
        'geometry': [
            LineString([(0, 0), (1, 1), (2, 0)]),
            LineString([(1, 2), (3, 3), (4, 2)])
        ]
    }, crs='EPSG:4326')
    return lines

# Test fixtures - these can be used by importing from tests
TEST_POINTS = create_test_points()
TEST_POLYGONS = create_test_polygons()
TEST_LINES = create_test_lines()

# Tolerance for floating point comparisons
SPATIAL_TOLERANCE = 1e-6

print(f"GeoPandas Tests Package v{__version__} initialized")
print(f"Test utilities available: assert_gdf_equal, create_test_*, TEST_* fixtures")
