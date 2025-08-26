"""
GIST 604B - Python GeoPandas Introduction
Test Suite for Spatial Data Fundamentals

This test suite validates the implementation of essential spatial data operations:
- Loading spatial data from various formats
- Exploring spatial properties and characteristics
- Validating spatial data quality
- Transforming coordinate reference systems

Tests follow professional pytest standards and cover:
- Basic functionality testing
- Edge cases and error handling
- Integration testing with real spatial data

Author: GIST 604B Course Team
"""

import pytest
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import json
from shapely.geometry import Point, LineString, Polygon
from shapely import wkt
import warnings
import os

# Import the functions to test
from src.spatial_basics import (
    load_spatial_dataset,
    explore_spatial_properties,
    validate_spatial_data,
    standardize_crs
)


class TestLoadSpatialDataset:
    """Test suite for load_spatial_dataset function."""

    @pytest.fixture
    def sample_geojson_file(self, tmp_path):
        """Create a temporary GeoJSON file for testing."""
        cities_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "New York", "population": 8336817},
                    "geometry": {"type": "Point", "coordinates": [-74.006, 40.714]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "London", "population": 8982000},
                    "geometry": {"type": "Point", "coordinates": [-0.118, 51.509]}
                },
                {
                    "type": "Feature",
                    "properties": {"name": "Tokyo", "population": 13960000},
                    "geometry": {"type": "Point", "coordinates": [139.692, 35.689]}
                }
            ]
        }

        geojson_file = tmp_path / "cities.geojson"
        with open(geojson_file, 'w') as f:
            json.dump(cities_data, f)

        return geojson_file

    @pytest.fixture
    def sample_shapefile(self, tmp_path):
        """Create a temporary Shapefile for testing."""
        # Create sample data
        gdf = gpd.GeoDataFrame({
            'name': ['Point A', 'Point B', 'Point C'],
            'value': [10, 20, 30],
            'geometry': [Point(-120, 45), Point(-118, 46), Point(-119, 44)]
        }, crs='EPSG:4326')

        shapefile_path = tmp_path / "test_points.shp"
        gdf.to_file(shapefile_path)
        return shapefile_path

    def test_load_geojson_basic_functionality(self, sample_geojson_file):
        """Test basic GeoJSON loading functionality."""
        result = load_spatial_dataset(sample_geojson_file)

        # Should return a GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)

        # Should have expected number of features
        assert len(result) == 3

        # Should have expected columns
        expected_columns = {'name', 'population', 'geometry'}
        assert expected_columns.issubset(set(result.columns))

        # Should have valid geometries
        assert result.geometry.is_valid.all()

        # Should have correct geometry types
        assert all(geom.geom_type == 'Point' for geom in result.geometry)

    def test_load_shapefile_basic_functionality(self, sample_shapefile):
        """Test basic Shapefile loading functionality."""
        result = load_spatial_dataset(sample_shapefile)

        # Should return a GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)

        # Should have expected number of features
        assert len(result) == 3

        # Should have expected columns
        expected_columns = {'name', 'value', 'geometry'}
        assert expected_columns.issubset(set(result.columns))

        # Should have valid geometries
        assert result.geometry.is_valid.all()

    def test_load_with_path_object(self, sample_geojson_file):
        """Test loading with Path object instead of string."""
        path_obj = Path(sample_geojson_file)
        result = load_spatial_dataset(path_obj)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 3

    def test_file_not_found_error(self, tmp_path):
        """Test that FileNotFoundError is raised for non-existent files."""
        non_existent_file = tmp_path / "does_not_exist.geojson"

        with pytest.raises(FileNotFoundError):
            load_spatial_dataset(non_existent_file)

    def test_invalid_file_format(self, tmp_path):
        """Test handling of invalid/unsupported file formats."""
        # Create a text file with invalid content
        invalid_file = tmp_path / "invalid.txt"
        with open(invalid_file, 'w') as f:
            f.write("This is not spatial data")

        with pytest.raises(ValueError):
            load_spatial_dataset(invalid_file)

    def test_load_with_kwargs(self, sample_geojson_file):
        """Test loading with additional keyword arguments."""
        # Test that kwargs are passed through (encoding parameter)
        result = load_spatial_dataset(sample_geojson_file, encoding='utf-8')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 3


class TestExploreSpatialProperties:
    """Test suite for explore_spatial_properties function."""

    @pytest.fixture
    def sample_mixed_geometries(self):
        """Create a GeoDataFrame with mixed geometry types for testing."""
        geometries = [
            Point(-120, 45),  # Point
            Point(-118, 46),  # Point
            LineString([(-119, 44), (-117, 45)]),  # LineString
            Polygon([(-116, 43), (-115, 43), (-115, 44), (-116, 44), (-116, 43)])  # Polygon
        ]

        gdf = gpd.GeoDataFrame({
            'name': ['Point1', 'Point2', 'Line1', 'Poly1'],
            'type': ['city', 'city', 'road', 'park'],
            'area': [0, 0, 100, 500],
            'geometry': geometries
        }, crs='EPSG:4326')

        return gdf

    @pytest.fixture
    def sample_points_utm(self):
        """Create a GeoDataFrame with UTM projection for CRS testing."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'geometry': [
                Point(500000, 4000000),
                Point(501000, 4001000),
                Point(502000, 4002000)
            ]
        }, crs='EPSG:32633')  # UTM Zone 33N

        return gdf

    def test_basic_properties_extraction(self, sample_mixed_geometries):
        """Test basic spatial properties extraction."""
        result = explore_spatial_properties(sample_mixed_geometries)

        # Should return a dictionary
        assert isinstance(result, dict)

        # Should have required keys
        required_keys = {
            'crs', 'bounds', 'geometry_types', 'feature_count',
            'column_info', 'has_valid_geometries'
        }
        assert required_keys.issubset(set(result.keys()))

    def test_crs_information(self, sample_mixed_geometries):
        """Test CRS information extraction."""
        result = explore_spatial_properties(sample_mixed_geometries)

        # Should have CRS information
        assert 'crs' in result
        # CRS should be WGS84 (EPSG:4326)
        crs_info = result['crs']
        assert 'EPSG:4326' in str(crs_info) or '4326' in str(crs_info)

    def test_bounds_calculation(self, sample_mixed_geometries):
        """Test spatial bounds calculation."""
        result = explore_spatial_properties(sample_mixed_geometries)

        # Should have bounds
        assert 'bounds' in result
        bounds = result['bounds']

        # Bounds should be a tuple or list of 4 values (minx, miny, maxx, maxy)
        assert len(bounds) == 4

        # Check that bounds are reasonable for our test data
        minx, miny, maxx, maxy = bounds
        assert minx <= maxx
        assert miny <= maxy

        # Should include our known coordinate ranges
        assert minx <= -120 and maxx >= -115
        assert miny <= 43 and maxy >= 46

    def test_geometry_types_analysis(self, sample_mixed_geometries):
        """Test geometry types identification."""
        result = explore_spatial_properties(sample_mixed_geometries)

        # Should identify geometry types
        assert 'geometry_types' in result
        geom_types = result['geometry_types']

        # Should find Point, LineString, and Polygon
        expected_types = {'Point', 'LineString', 'Polygon'}
        if isinstance(geom_types, list):
            geom_types_set = set(geom_types)
        else:
            # Might be a dictionary with counts
            geom_types_set = set(geom_types.keys())

        assert expected_types.issubset(geom_types_set)

    def test_feature_count(self, sample_mixed_geometries):
        """Test feature count reporting."""
        result = explore_spatial_properties(sample_mixed_geometries)

        assert 'feature_count' in result
        assert result['feature_count'] == 4  # Our test data has 4 features

    def test_column_information(self, sample_mixed_geometries):
        """Test column information extraction."""
        result = explore_spatial_properties(sample_mixed_geometries)

        assert 'column_info' in result
        column_info = result['column_info']

        # Should include information about our test columns
        expected_columns = {'name', 'type', 'area', 'geometry'}
        if isinstance(column_info, dict):
            assert expected_columns.issubset(set(column_info.keys()))
        elif isinstance(column_info, list):
            assert expected_columns.issubset(set(column_info))

    def test_geometry_validity_check(self, sample_mixed_geometries):
        """Test geometry validity assessment."""
        result = explore_spatial_properties(sample_mixed_geometries)

        assert 'has_valid_geometries' in result
        # Our test data should all be valid
        assert result['has_valid_geometries'] is True

    def test_different_crs(self, sample_points_utm):
        """Test properties extraction with different CRS."""
        result = explore_spatial_properties(sample_points_utm)

        # Should handle UTM coordinates
        assert 'crs' in result
        crs_info = result['crs']
        assert '32633' in str(crs_info) or 'UTM' in str(crs_info)

        # Bounds should be in UTM range (large numbers)
        bounds = result['bounds']
        minx, miny, maxx, maxy = bounds
        assert minx >= 500000  # UTM coordinates are large


class TestValidateSpatialData:
    """Test suite for validate_spatial_data function."""

    @pytest.fixture
    def valid_data(self):
        """Create a GeoDataFrame with valid spatial data."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'geometry': [
                Point(-120, 45),
                Point(-118, 46),
                Point(-119, 44)
            ]
        }, crs='EPSG:4326')
        return gdf

    @pytest.fixture
    def data_with_issues(self):
        """Create a GeoDataFrame with various spatial data issues."""
        # Create some problematic geometries
        invalid_polygon = wkt.loads('POLYGON((0 0, 1 1, 1 0, 0 1, 0 0))')  # Self-intersecting

        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Valid', 'Missing', 'Invalid', 'Empty', 'OutOfRange'],
            'geometry': [
                Point(-120, 45),           # Valid point
                None,                      # Missing geometry
                invalid_polygon,           # Invalid geometry (self-intersecting)
                wkt.loads('POINT EMPTY'),  # Empty geometry
                Point(200, 100)            # Out of range coordinates
            ]
        }, crs='EPSG:4326')
        return gdf

    @pytest.fixture
    def data_no_crs(self):
        """Create a GeoDataFrame without CRS."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [Point(-120, 45), Point(-118, 46), Point(-119, 44)]
        })  # No CRS specified
        return gdf

    def test_valid_data_validation(self, valid_data):
        """Test validation of clean, valid spatial data."""
        result = validate_spatial_data(valid_data)

        # Should return a dictionary
        assert isinstance(result, dict)

        # Should have required keys
        required_keys = {
            'is_valid', 'issues_found', 'invalid_geometries',
            'missing_geometries', 'crs_issues', 'recommendations'
        }
        assert required_keys.issubset(set(result.keys()))

        # Valid data should pass validation
        assert result['is_valid'] is True
        assert len(result['issues_found']) == 0
        assert result['invalid_geometries'] == 0
        assert result['missing_geometries'] == 0

    def test_missing_geometries_detection(self, data_with_issues):
        """Test detection of missing/null geometries."""
        result = validate_spatial_data(data_with_issues)

        # Should detect missing geometries
        assert result['is_valid'] is False
        assert result['missing_geometries'] > 0
        assert 'missing geometries' in str(result['issues_found']).lower() or \
               'null geometries' in str(result['issues_found']).lower()

    def test_invalid_geometries_detection(self, data_with_issues):
        """Test detection of invalid geometries."""
        result = validate_spatial_data(data_with_issues)

        # Should detect invalid geometries
        assert result['is_valid'] is False
        assert result['invalid_geometries'] > 0
        assert any('invalid' in str(issue).lower() for issue in result['issues_found'])

    def test_crs_issues_detection(self, data_no_crs):
        """Test detection of CRS-related issues."""
        result = validate_spatial_data(data_no_crs)

        # Should detect CRS issues
        assert result['is_valid'] is False
        assert len(result['crs_issues']) > 0 or \
               any('crs' in str(issue).lower() for issue in result['issues_found'])

    def test_coordinate_range_validation(self, data_with_issues):
        """Test validation of coordinate ranges."""
        result = validate_spatial_data(data_with_issues)

        # Should detect out-of-range coordinates
        assert result['is_valid'] is False
        # Should have some indication of coordinate issues
        issues_text = ' '.join(str(issue) for issue in result['issues_found']).lower()
        assert 'coordinate' in issues_text or 'range' in issues_text or 'bounds' in issues_text

    def test_recommendations_provided(self, data_with_issues):
        """Test that validation provides helpful recommendations."""
        result = validate_spatial_data(data_with_issues)

        # Should provide recommendations for fixing issues
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0

        # Recommendations should be helpful strings
        for rec in result['recommendations']:
            assert isinstance(rec, str)
            assert len(rec) > 0

    def test_empty_geometries_detection(self, data_with_issues):
        """Test detection of empty geometries."""
        result = validate_spatial_data(data_with_issues)

        # Should detect various types of issues
        assert result['is_valid'] is False
        # The function should handle empty geometries appropriately
        assert len(result['issues_found']) > 0


class TestStandardizeCRS:
    """Test suite for standardize_crs function."""

    @pytest.fixture
    def wgs84_data(self):
        """Create a GeoDataFrame in WGS84."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'geometry': [
                Point(-120, 45),
                Point(-118, 46),
                Point(-119, 44)
            ]
        }, crs='EPSG:4326')
        return gdf

    @pytest.fixture
    def utm_data(self):
        """Create a GeoDataFrame in UTM coordinates."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [
                Point(500000, 4000000),
                Point(501000, 4001000),
                Point(502000, 4002000)
            ]
        }, crs='EPSG:32633')  # UTM Zone 33N
        return gdf

    @pytest.fixture
    def no_crs_data(self):
        """Create a GeoDataFrame without CRS."""
        gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [Point(-120, 45), Point(-118, 46), Point(-119, 44)]
        })  # No CRS
        return gdf

    def test_explicit_crs_transformation(self, wgs84_data):
        """Test explicit CRS transformation to specific target."""
        # Transform to Web Mercator
        result = standardize_crs(wgs84_data, target_crs=3857)

        # Should return GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)

        # Should have correct target CRS
        assert result.crs.to_epsg() == 3857

        # Should have same number of features
        assert len(result) == len(wgs84_data)

        # Coordinates should be different (transformed)
        orig_coords = [(geom.x, geom.y) for geom in wgs84_data.geometry]
        new_coords = [(geom.x, geom.y) for geom in result.geometry]
        assert orig_coords != new_coords

        # Web Mercator coordinates should be much larger
        assert all(abs(x) > 10000 for x, y in new_coords)

    def test_string_crs_specification(self, wgs84_data):
        """Test CRS transformation with string specification."""
        # Transform using EPSG string
        result = standardize_crs(wgs84_data, target_crs='EPSG:3857')

        assert isinstance(result, gpd.GeoDataFrame)
        assert result.crs.to_epsg() == 3857

    def test_auto_crs_selection(self, wgs84_data):
        """Test automatic CRS selection (target_crs=None)."""
        result = standardize_crs(wgs84_data, target_crs=None)

        # Should return GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)

        # Should have a valid CRS
        assert result.crs is not None

        # Should have same number of features
        assert len(result) == len(wgs84_data)

    def test_no_transformation_needed(self, wgs84_data):
        """Test when no transformation is needed (already in target CRS)."""
        # Request transformation to same CRS
        result = standardize_crs(wgs84_data, target_crs=4326)

        # Should return GeoDataFrame
        assert isinstance(result, gpd.GeoDataFrame)

        # Should have same CRS
        assert result.crs.to_epsg() == 4326

        # Coordinates should be the same (or very close)
        orig_coords = [(geom.x, geom.y) for geom in wgs84_data.geometry]
        new_coords = [(geom.x, geom.y) for geom in result.geometry]

        for (x1, y1), (x2, y2) in zip(orig_coords, new_coords):
            assert abs(x1 - x2) < 1e-10
            assert abs(y1 - y2) < 1e-10

    def test_handle_missing_crs(self, no_crs_data):
        """Test handling of data with missing CRS."""
        # Should handle missing CRS gracefully
        result = standardize_crs(no_crs_data, target_crs=4326)

        assert isinstance(result, gpd.GeoDataFrame)
        assert result.crs is not None

    def test_geometry_validity_preserved(self, wgs84_data):
        """Test that geometries remain valid after transformation."""
        result = standardize_crs(wgs84_data, target_crs=3857)

        # All geometries should still be valid
        assert result.geometry.is_valid.all()

        # Should have same geometry types
        orig_types = set(wgs84_data.geometry.geom_type)
        new_types = set(result.geometry.geom_type)
        assert orig_types == new_types

    def test_utm_to_geographic_transformation(self, utm_data):
        """Test transformation from projected to geographic coordinates."""
        result = standardize_crs(utm_data, target_crs=4326)

        # Should transform to WGS84
        assert result.crs.to_epsg() == 4326

        # Coordinates should be in geographic ranges
        coords = [(geom.x, geom.y) for geom in result.geometry]
        for x, y in coords:
            assert -180 <= x <= 180  # Longitude range
            assert -90 <= y <= 90    # Latitude range

    def test_invalid_crs_handling(self, wgs84_data):
        """Test handling of invalid CRS specifications."""
        with pytest.raises((ValueError, Exception)):
            standardize_crs(wgs84_data, target_crs='INVALID:9999')


class TestIntegrationScenarios:
    """Integration tests combining multiple functions."""

    @pytest.fixture
    def sample_dataset_file(self, tmp_path):
        """Create a sample dataset file for integration testing."""
        # Create mixed geometry data with some issues
        geometries = [
            Point(-120.5, 45.5),  # Valid point in Oregon
            Point(-121.0, 46.0),  # Valid point in Washington
            None,                 # Missing geometry
            Point(-119.0, 44.0),  # Valid point in Oregon
        ]

        gdf = gpd.GeoDataFrame({
            'city': ['Portland', 'Seattle', 'Missing', 'Bend'],
            'state': ['OR', 'WA', 'OR', 'OR'],
            'population': [650000, 750000, None, 95000],
            'geometry': geometries
        }, crs='EPSG:4326')

        filepath = tmp_path / "cities.geojson"
        # Only save rows with valid geometry for the file
        valid_gdf = gdf.dropna(subset=['geometry'])
        valid_gdf.to_file(filepath, driver='GeoJSON')
        return filepath

    def test_complete_spatial_workflow(self, sample_dataset_file):
        """Test complete workflow: load → explore → validate → standardize."""

        # Step 1: Load the data
        gdf = load_spatial_dataset(sample_dataset_file)
        assert isinstance(gdf, gpd.GeoDataFrame)

        # Step 2: Explore properties
        properties = explore_spatial_properties(gdf)
        assert isinstance(properties, dict)
        assert properties['feature_count'] > 0
        assert 'geometry_types' in properties

        # Step 3: Validate the data
        validation = validate_spatial_data(gdf)
        assert isinstance(validation, dict)
        assert 'is_valid' in validation

        # Step 4: Standardize CRS (transform to Web Mercator)
        standardized = standardize_crs(gdf, target_crs=3857)
        assert isinstance(standardized, gpd.GeoDataFrame)
        assert standardized.crs.to_epsg() == 3857

        # Verify the workflow maintained data integrity
        assert len(standardized) == len(gdf)
        assert set(standardized.columns) == set(gdf.columns)

    def test_error_recovery_workflow(self, tmp_path):
        """Test workflow with various error conditions."""

        # Test loading non-existent file
        with pytest.raises(FileNotFoundError):
            load_spatial_dataset(tmp_path / "nonexistent.geojson")

        # Create problematic data for validation testing
        problematic_gdf = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': [Point(-120, 45), None]  # Missing geometry
        })  # No CRS

        # Validation should catch issues
        validation = validate_spatial_data(problematic_gdf)
        assert validation['is_valid'] is False
        assert len(validation['issues_found']) > 0


# Fixtures for test data setup
@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """Create a temporary directory with test spatial datasets."""
    data_dir = tmp_path_factory.mktemp("test_spatial_data")

    # Create various test datasets
    # Points dataset
    points = gpd.GeoDataFrame({
        'name': ['Seattle', 'Portland', 'Vancouver'],
        'country': ['USA', 'USA', 'Canada'],
        'geometry': [Point(-122.3, 47.6), Point(-122.7, 45.5), Point(-123.1, 49.3)]
    }, crs='EPSG:4326')
    points.to_file(data_dir / "cities.geojson", driver='GeoJSON')

    # Lines dataset
    lines = gpd.GeoDataFrame({
        'highway': ['I-5', 'I-90'],
        'geometry': [
            LineString([(-122.3, 47.6), (-122.7, 45.5)]),
            LineString([(-122.3, 47.6), (-117.4, 47.7)])
        ]
    }, crs='EPSG:4326')
    lines.to_file(data_dir / "highways.shp")

    return data_dir


# Performance and edge case tests
class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_geodataframe(self):
        """Test functions with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame(columns=['geometry'], crs='EPSG:4326')

        # Functions should handle empty data gracefully
        properties = explore_spatial_properties(empty_gdf)
        assert properties['feature_count'] == 0

        validation = validate_spatial_data(empty_gdf)
        assert isinstance(validation, dict)

        standardized = standardize_crs(empty_gdf, target_crs=3857)
        assert len(standardized) == 0
        assert standardized.crs.to_epsg() == 3857

    def test_single_feature_geodataframe(self):
        """Test functions with single feature."""
        single_gdf = gpd.GeoDataFrame({
            'name': ['Single Point'],
            'geometry': [Point(-120, 45)]
        }, crs='EPSG:4326')

        properties = explore_spatial_properties(single_gdf)
        assert properties['feature_count'] == 1

        validation = validate_spatial_data(single_gdf)
        assert validation['is_valid'] is True

        standardized = standardize_crs(single_gdf, target_crs=3857)
        assert len(standardized) == 1

    def test_large_coordinate_values(self):
        """Test with large coordinate values (UTM, State Plane, etc.)."""
        large_coords_gdf = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': [
                Point(500000, 4000000),  # UTM coordinates
                Point(1000000, 5000000)  # Large UTM coordinates
            ]
        }, crs='EPSG:32633')

        properties = explore_spatial_properties(large_coords_gdf)
        assert properties['feature_count'] == 2

        # Should handle large coordinates
        bounds = properties['bounds']
        assert all(coord >= 500000 for coord in bounds[:2])  # Min coords
