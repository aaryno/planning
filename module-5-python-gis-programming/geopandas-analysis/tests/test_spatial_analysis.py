"""
Test suite for Python GeoPandas Analysis - Essential Spatial Operations

This module contains comprehensive tests for the three core spatial analysis functions:
1. load_and_explore_spatial_data()
2. calculate_basic_spatial_metrics()
3. create_spatial_buffer_analysis()

GIST 604B - Open Source GIS Programming
Module 5: Python GIS Programming
"""

import pytest
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from pathlib import Path
import tempfile
import os

# Import the functions to test
from src.spatial_analysis import (
    load_and_explore_spatial_data,
    calculate_basic_spatial_metrics,
    create_spatial_buffer_analysis
)


# =============================================================================
# FIXTURES - Test Data Setup
# =============================================================================

@pytest.fixture
def sample_points():
    """Create sample point geometries for testing."""
    points = [
        Point(-122.4194, 37.7749),  # San Francisco
        Point(-118.2437, 34.0522),  # Los Angeles
        Point(-117.1611, 32.7157)   # San Diego
    ]

    gdf = gpd.GeoDataFrame({
        'city_name': ['San Francisco', 'Los Angeles', 'San Diego'],
        'population': [883305, 3979576, 1423851],
        'state': ['CA', 'CA', 'CA'],
        'geometry': points
    }, crs='EPSG:4326')

    return gdf


@pytest.fixture
def sample_polygons():
    """Create sample polygon geometries for testing."""
    polygons = [
        Polygon([(-122.5, 37.7), (-122.4, 37.7), (-122.4, 37.8), (-122.5, 37.8), (-122.5, 37.7)]),
        Polygon([(-118.3, 34.0), (-118.2, 34.0), (-118.2, 34.1), (-118.3, 34.1), (-118.3, 34.0)]),
        Polygon([(-117.2, 32.7), (-117.1, 32.7), (-117.1, 32.8), (-117.2, 32.8), (-117.2, 32.7)])
    ]

    gdf = gpd.GeoDataFrame({
        'park_name': ['Golden Gate Park', 'Griffith Park', 'Balboa Park'],
        'area_acres': [1017, 4310, 1200],
        'type': ['urban_park', 'urban_park', 'urban_park'],
        'geometry': polygons
    }, crs='EPSG:4326')

    return gdf


@pytest.fixture
def sample_lines():
    """Create sample line geometries for testing."""
    lines = [
        LineString([(-122.5, 37.75), (-122.45, 37.76), (-122.4, 37.77)]),
        LineString([(-118.3, 34.05), (-118.25, 34.06), (-118.2, 34.07)])
    ]

    gdf = gpd.GeoDataFrame({
        'river_name': ['SF River', 'LA River'],
        'length_km': [15.2, 18.7],
        'flow_type': ['perennial', 'intermittent'],
        'geometry': lines
    }, crs='EPSG:4326')

    return gdf


@pytest.fixture
def mixed_geometry_gdf():
    """Create GeoDataFrame with mixed geometry types."""
    geometries = [
        Point(-122.4194, 37.7749),
        Polygon([(-122.5, 37.7), (-122.4, 37.7), (-122.4, 37.8), (-122.5, 37.8), (-122.5, 37.7)]),
        LineString([(-122.5, 37.75), (-122.45, 37.76), (-122.4, 37.77)])
    ]

    gdf = gpd.GeoDataFrame({
        'name': ['SF Point', 'SF Polygon', 'SF Line'],
        'type': ['city', 'park', 'river'],
        'geometry': geometries
    }, crs='EPSG:4326')

    return gdf


@pytest.fixture
def temp_geojson_file(sample_points):
    """Create a temporary GeoJSON file for testing file loading."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
        sample_points.to_file(f.name, driver='GeoJSON')
        temp_file_path = f.name

    yield temp_file_path

    # Cleanup
    os.unlink(temp_file_path)


# =============================================================================
# TEST CLASS 1: LOAD AND EXPLORE SPATIAL DATA
# =============================================================================

class TestLoadAndExploreSpatialData:
    """Test suite for load_and_explore_spatial_data() function."""

    def test_load_valid_geojson_file(self, temp_geojson_file, capsys):
        """Test loading a valid GeoJSON file."""
        result = load_and_explore_spatial_data(temp_geojson_file)

        # Check that function returns a GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 3
        assert result.crs is not None
        assert 'geometry' in result.columns

        # Check that it prints exploration information
        captured = capsys.readouterr()
        assert "LOADING AND EXPLORING SPATIAL DATA" in captured.out
        assert "Spatial file loaded successfully" in captured.out
        assert "SPATIAL DATASET OVERVIEW" in captured.out
        assert "Geometry types:" in captured.out

    def test_load_nonexistent_file(self, capsys):
        """Test error handling when file doesn't exist."""
        result = load_and_explore_spatial_data('nonexistent_file.geojson')

        assert result is None

        captured = capsys.readouterr()
        assert "File not found" in captured.out

    def test_load_invalid_file_path(self):
        """Test with invalid file path (directory instead of file)."""
        result = load_and_explore_spatial_data('.')

        assert result is None

    def test_function_output_content(self, temp_geojson_file, capsys):
        """Test that function outputs comprehensive spatial information."""
        result = load_and_explore_spatial_data(temp_geojson_file)

        captured = capsys.readouterr()

        # Check for key information sections
        assert "Shape:" in captured.out
        assert "CRS:" in captured.out
        assert "Geometry types:" in captured.out
        assert "Spatial bounds:" in captured.out
        assert "FIRST 3 FEATURES:" in captured.out
        assert "DATA QUALITY CHECK:" in captured.out

    def test_data_quality_checks(self, temp_geojson_file, capsys):
        """Test that data quality checks are performed and reported."""
        result = load_and_explore_spatial_data(temp_geojson_file)

        captured = capsys.readouterr()

        # Should check for missing values, empty geometries, invalid geometries
        assert "missing values" in captured.out.lower() or "no missing" in captured.out.lower()
        assert "empty geometries" in captured.out.lower() or "no empty" in captured.out.lower()
        assert "valid" in captured.out.lower()


# =============================================================================
# TEST CLASS 2: CALCULATE BASIC SPATIAL METRICS
# =============================================================================

class TestCalculateBasicSpatialMetrics:
    """Test suite for calculate_basic_spatial_metrics() function."""

    def test_basic_functionality_points(self, sample_points, capsys):
        """Test basic functionality with point geometries."""
        result = calculate_basic_spatial_metrics(sample_points)

        assert isinstance(result, dict)
        assert 'areas' in result
        assert 'perimeters' in result
        assert 'centroids' in result
        assert 'total_area' in result
        assert 'total_perimeter' in result
        assert 'geometry_types' in result
        assert 'crs_used' in result

        # Points should have zero areas
        assert all(area == 0 for area in result['areas'])

        # Should have centroids for all points
        assert len(result['centroids']) == len(sample_points)

        captured = capsys.readouterr()
        assert "CALCULATING BASIC SPATIAL METRICS" in captured.out

    def test_basic_functionality_polygons(self, sample_polygons):
        """Test basic functionality with polygon geometries."""
        result = calculate_basic_spatial_metrics(sample_polygons)

        assert isinstance(result, dict)

        # Polygons should have meaningful areas (> 0)
        assert all(area > 0 for area in result['areas'])
        assert result['total_area'] > 0

        # Should have perimeters for polygons
        assert all(perim > 0 for perim in result['perimeters'])

        # Should have centroids
        assert len(result['centroids']) == len(sample_polygons)

    def test_basic_functionality_lines(self, sample_lines):
        """Test basic functionality with line geometries."""
        result = calculate_basic_spatial_metrics(sample_lines)

        assert isinstance(result, dict)

        # Lines should have zero areas
        assert all(area == 0 for area in result['areas'])

        # Lines should have meaningful lengths (> 0)
        assert all(length > 0 for length in result['perimeters'])

        # Should have centroids
        assert len(result['centroids']) == len(sample_lines)

    def test_mixed_geometries(self, mixed_geometry_gdf):
        """Test with mixed geometry types."""
        result = calculate_basic_spatial_metrics(mixed_geometry_gdf)

        assert isinstance(result, dict)
        assert len(result['areas']) == len(mixed_geometry_gdf)
        assert len(result['centroids']) == len(mixed_geometry_gdf)

        # Check that geometry types are correctly counted
        geom_counts = result['geometry_types']
        assert 'Point' in geom_counts
        assert 'Polygon' in geom_counts
        assert 'LineString' in geom_counts

    def test_crs_handling_geographic(self, sample_polygons, capsys):
        """Test that geographic CRS is properly handled (reprojected)."""
        # Ensure input is in geographic CRS
        sample_polygons = sample_polygons.to_crs('EPSG:4326')

        result = calculate_basic_spatial_metrics(sample_polygons)

        captured = capsys.readouterr()
        assert "Reprojecting to" in captured.out

        # Should have calculated meaningful areas
        assert result['total_area'] > 0
        assert 'EPSG:326' in result['crs_used'] or 'EPSG:327' in result['crs_used']

    def test_error_handling_none_input(self, capsys):
        """Test error handling with None input."""
        result = calculate_basic_spatial_metrics(None)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_error_handling_empty_gdf(self, capsys):
        """Test error handling with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame()
        result = calculate_basic_spatial_metrics(empty_gdf)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_no_geometry_column(self, capsys):
        """Test error handling when no geometry column exists."""
        df = pd.DataFrame({'name': ['test'], 'value': [1]})
        gdf = gpd.GeoDataFrame(df)  # No geometry column

        result = calculate_basic_spatial_metrics(gdf)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out


# =============================================================================
# TEST CLASS 3: CREATE SPATIAL BUFFER ANALYSIS
# =============================================================================

class TestCreateSpatialBufferAnalysis:
    """Test suite for create_spatial_buffer_analysis() function."""

    def test_basic_functionality_points(self, sample_points, capsys):
        """Test basic buffer creation with point geometries."""
        buffer_distance = 1000  # 1km

        result = create_spatial_buffer_analysis(sample_points, buffer_distance)

        assert isinstance(result, dict)
        assert 'buffered_gdf' in result
        assert 'original_gdf' in result
        assert 'buffer_areas' in result
        assert 'total_buffered_area' in result
        assert 'average_buffer_area' in result
        assert 'overlapping_buffers' in result
        assert 'distance_used' in result
        assert 'crs_used' in result

        # Check buffered GeoDataFrame
        buffered_gdf = result['buffered_gdf']
        assert isinstance(buffered_gdf, gpd.GeoDataFrame)
        assert len(buffered_gdf) == len(sample_points)
        assert all(geom_type == 'Polygon' for geom_type in buffered_gdf.geom_type)

        # Check that areas are calculated
        assert result['total_buffered_area'] > 0
        assert result['average_buffer_area'] > 0
        assert len(result['buffer_areas']) == len(sample_points)

        captured = capsys.readouterr()
        assert "CREATE SPATIAL BUFFER ANALYSIS" in captured.out
        assert f"Creating {buffer_distance}m buffers" in captured.out

    def test_basic_functionality_polygons(self, sample_polygons):
        """Test buffer creation with polygon geometries."""
        buffer_distance = 500  # 500m

        result = create_spatial_buffer_analysis(sample_polygons, buffer_distance)

        assert isinstance(result, dict)
        assert result['total_buffered_area'] > 0
        assert result['distance_used'] == buffer_distance

        # Buffered polygons should be larger than originals
        buffered_gdf = result['buffered_gdf']
        assert len(buffered_gdf) == len(sample_polygons)

    def test_basic_functionality_lines(self, sample_lines):
        """Test buffer creation with line geometries."""
        buffer_distance = 100  # 100m

        result = create_spatial_buffer_analysis(sample_lines, buffer_distance)

        assert isinstance(result, dict)
        assert result['total_buffered_area'] > 0

        # Line buffers should create polygon corridors
        buffered_gdf = result['buffered_gdf']
        assert all(geom_type == 'Polygon' for geom_type in buffered_gdf.geom_type)

    def test_different_buffer_distances(self, sample_points):
        """Test with different buffer distances."""
        distances = [100, 500, 1000, 2000]
        previous_area = 0

        for distance in distances:
            result = create_spatial_buffer_analysis(sample_points, distance)

            assert result['distance_used'] == distance
            assert result['total_buffered_area'] > previous_area
            previous_area = result['total_buffered_area']

    def test_overlapping_buffer_detection(self, capsys):
        """Test detection of overlapping buffers with close points."""
        # Create points that are close together (will have overlapping buffers)
        close_points = [
            Point(-122.4194, 37.7749),
            Point(-122.4200, 37.7750),  # Very close to first point
            Point(-122.4190, 37.7748)   # Also very close
        ]

        close_gdf = gpd.GeoDataFrame({
            'name': ['Point 1', 'Point 2', 'Point 3'],
            'geometry': close_points
        }, crs='EPSG:4326')

        result = create_spatial_buffer_analysis(close_gdf, 1000)  # Large buffer

        # Should detect overlapping buffers
        assert result['overlapping_buffers'] > 0

        captured = capsys.readouterr()
        assert "Analyzing buffer overlaps" in captured.out

    def test_crs_handling_geographic(self, sample_points, capsys):
        """Test that geographic CRS is properly handled for buffering."""
        # Ensure input is in geographic CRS
        sample_points = sample_points.to_crs('EPSG:4326')

        result = create_spatial_buffer_analysis(sample_points, 1000)

        captured = capsys.readouterr()
        assert "Reprojecting to" in captured.out

        # Should use UTM CRS for calculations
        assert 'EPSG:326' in result['crs_used'] or 'EPSG:327' in result['crs_used']

    def test_error_handling_none_input(self, capsys):
        """Test error handling with None input."""
        result = create_spatial_buffer_analysis(None, 1000)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_error_handling_empty_gdf(self, capsys):
        """Test error handling with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame()
        result = create_spatial_buffer_analysis(empty_gdf, 1000)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out

    def test_error_handling_negative_distance(self, sample_points, capsys):
        """Test error handling with negative buffer distance."""
        result = create_spatial_buffer_analysis(sample_points, -500)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "positive" in captured.out

    def test_error_handling_zero_distance(self, sample_points, capsys):
        """Test error handling with zero buffer distance."""
        result = create_spatial_buffer_analysis(sample_points, 0)

        assert result is None

        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "positive" in captured.out

    def test_return_data_types(self, sample_points):
        """Test that return values have correct data types."""
        result = create_spatial_buffer_analysis(sample_points, 1000)

        assert isinstance(result['buffered_gdf'], gpd.GeoDataFrame)
        assert isinstance(result['original_gdf'], gpd.GeoDataFrame)
        assert isinstance(result['buffer_areas'], pd.Series)
        assert isinstance(result['total_buffered_area'], float)
        assert isinstance(result['average_buffer_area'], float)
        assert isinstance(result['overlapping_buffers'], int)
        assert isinstance(result['distance_used'], (int, float))
        assert isinstance(result['crs_used'], str)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_complete_workflow(self, temp_geojson_file):
        """Test complete workflow: load → calculate metrics → create buffers."""
        # Step 1: Load spatial data
        gdf = load_and_explore_spatial_data(temp_geojson_file)
        assert gdf is not None

        # Step 2: Calculate spatial metrics
        metrics = calculate_basic_spatial_metrics(gdf)
        assert metrics is not None
        assert metrics['total_area'] >= 0  # Points have 0 area

        # Step 3: Create buffer analysis
        buffers = create_spatial_buffer_analysis(gdf, 1000)
        assert buffers is not None
        assert buffers['total_buffered_area'] > 0

        # Verify data consistency
        assert len(gdf) == len(metrics['areas'])
        assert len(gdf) == len(buffers['buffered_gdf'])

    def test_workflow_with_different_geometry_types(self, mixed_geometry_gdf):
        """Test workflow with mixed geometry types."""
        # Calculate metrics
        metrics = calculate_basic_spatial_metrics(mixed_geometry_gdf)
        assert metrics is not None

        # Create buffers
        buffers = create_spatial_buffer_analysis(mixed_geometry_gdf, 500)
        assert buffers is not None

        # All geometries should have buffers (now polygons)
        assert all(geom_type == 'Polygon' for geom_type in buffers['buffered_gdf'].geom_type)


# =============================================================================
# EDGE CASES AND STRESS TESTS
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_feature_datasets(self):
        """Test functions with single-feature datasets."""
        single_point = gpd.GeoDataFrame({
            'name': ['Single Point'],
            'geometry': [Point(-122.4194, 37.7749)]
        }, crs='EPSG:4326')

        # Test metrics calculation
        metrics = calculate_basic_spatial_metrics(single_point)
        assert metrics is not None
        assert len(metrics['areas']) == 1

        # Test buffer analysis
        buffers = create_spatial_buffer_analysis(single_point, 1000)
        assert buffers is not None
        assert len(buffers['buffered_gdf']) == 1
        assert buffers['overlapping_buffers'] == 0  # No overlaps with single feature

    def test_very_small_buffer_distances(self, sample_points):
        """Test with very small buffer distances."""
        result = create_spatial_buffer_analysis(sample_points, 1)  # 1 meter

        assert result is not None
        assert result['total_buffered_area'] > 0
        assert result['distance_used'] == 1

    def test_very_large_buffer_distances(self, sample_points):
        """Test with very large buffer distances."""
        result = create_spatial_buffer_analysis(sample_points, 100000)  # 100 km

        assert result is not None
        assert result['total_buffered_area'] > 0
        assert result['distance_used'] == 100000

        # Large buffers should likely overlap
        assert result['overlapping_buffers'] > 0


# =============================================================================
# PERFORMANCE AND VALIDATION TESTS
# =============================================================================

class TestValidation:
    """Tests for validating calculation accuracy."""

    def test_circular_buffer_area_calculation(self):
        """Test that circular buffer areas are approximately correct."""
        # Single point buffer should create approximately circular area
        single_point = gpd.GeoDataFrame({
            'name': ['Test Point'],
            'geometry': [Point(0, 0)]  # Origin point
        }, crs='EPSG:4326')

        buffer_distance = 1000  # 1 km
        result = create_spatial_buffer_analysis(single_point, buffer_distance)

        # Expected area of circle = π * r²
        expected_area_km2 = np.pi * (buffer_distance / 1000) ** 2
        actual_area_km2 = result['total_buffered_area']

        # Allow for some tolerance due to projection and coordinate system effects
        tolerance = expected_area_km2 * 0.1  # 10% tolerance
        assert abs(actual_area_km2 - expected_area_km2) <= tolerance

    def test_area_calculation_consistency(self, sample_polygons):
        """Test that area calculations are consistent."""
        metrics = calculate_basic_spatial_metrics(sample_polygons)

        # Total area should equal sum of individual areas
        calculated_total = metrics['areas'].sum()
        reported_total = metrics['total_area']

        assert abs(calculated_total - reported_total) < 0.000001  # Very small tolerance for float precision
