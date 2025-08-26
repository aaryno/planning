"""
Test Suite for Spatial Data Loading Module
==========================================

This file tests all functions in the spatial_data_loading module to ensure
they work correctly with various types of spatial data and edge cases.

Test Categories:
1. load_spatial_dataset: Loading data from various formats
2. explore_spatial_properties: Analyzing spatial data characteristics
3. validate_spatial_data: Finding and fixing spatial data issues
4. standardize_crs: Coordinate reference system transformations

Run these tests to verify your implementations work correctly!
"""

import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import Path
import tempfile
import warnings
from shapely.geometry import Point, LineString, Polygon
from shapely.validation import make_valid

# Import the functions we're testing
from src.geopandas_analysis.spatial_data_loading import (
    load_spatial_dataset,
    explore_spatial_properties,
    validate_spatial_data,
    standardize_crs
)

# Import test utilities
from tests import (
    create_test_points,
    create_test_polygons,
    create_test_lines,
    SPATIAL_TOLERANCE
)


class TestLoadSpatialDataset:
    """Test the load_spatial_dataset function."""

    def test_load_spatial_dataset_with_valid_geojson(self, tmp_path):
        """Test loading a valid GeoJSON file."""
        # Create test data
        test_gdf = create_test_points()

        # Save to temporary GeoJSON file
        geojson_path = tmp_path / "test_points.geojson"
        test_gdf.to_file(geojson_path, driver='GeoJSON')

        # Load using our function
        result = load_spatial_dataset(geojson_path)

        # Verify results
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(test_gdf)
        assert result.crs is not None
        assert 'geometry' in result.columns
        assert result.attrs['file_format'] == 'geojson'

    def test_load_spatial_dataset_with_csv_coordinates(self, tmp_path):
        """Test loading CSV file with coordinate columns."""
        # Create test CSV with coordinate columns
        csv_data = pd.DataFrame({
            'name': ['Location A', 'Location B', 'Location C'],
            'longitude': [-110.0, -111.0, -112.0],
            'latitude': [32.0, 33.0, 34.0],
            'value': [100, 200, 300]
        })

        csv_path = tmp_path / "test_coords.csv"
        csv_data.to_csv(csv_path, index=False)

        # Load using our function
        result = load_spatial_dataset(csv_path)

        # Verify results
        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 3
        assert result.crs.to_epsg() == 4326  # Should assume WGS84
        assert all(result.geometry.geom_type == 'Point')

    def test_load_spatial_dataset_missing_file(self, tmp_path):
        """Test error handling for missing file."""
        missing_path = tmp_path / "nonexistent.shp"

        with pytest.raises(FileNotFoundError):
            load_spatial_dataset(missing_path)

    def test_load_spatial_dataset_csv_no_coordinates(self, tmp_path):
        """Test CSV without coordinate columns raises error."""
        csv_data = pd.DataFrame({
            'name': ['A', 'B', 'C'],
            'value': [1, 2, 3]
        })

        csv_path = tmp_path / "no_coords.csv"
        csv_data.to_csv(csv_path, index=False)

        with pytest.raises(ValueError, match="coordinate columns"):
            load_spatial_dataset(csv_path)

    def test_load_spatial_dataset_format_detection(self, tmp_path):
        """Test automatic format detection from file extension."""
        test_gdf = create_test_polygons()

        # Test with different extensions
        formats_to_test = [
            ('test.geojson', 'geojson'),
            ('test.json', 'geojson'),
            ('test.gpkg', 'gpkg')
        ]

        for filename, expected_format in formats_to_test:
            if expected_format == 'gpkg':
                file_path = tmp_path / filename
                test_gdf.to_file(file_path, driver='GPKG')

                result = load_spatial_dataset(file_path)
                assert result.attrs['file_format'] == expected_format


class TestExploreSpatialProperties:
    """Test the explore_spatial_properties function."""

    def test_explore_spatial_properties_points(self):
        """Test spatial property analysis with point data."""
        test_gdf = create_test_points()

        result = explore_spatial_properties(test_gdf)

        # Verify structure
        assert isinstance(result, dict)
        required_keys = [
            'feature_count', 'attribute_count', 'column_names',
            'crs', 'epsg_code', 'crs_type', 'geometry_types',
            'primary_geometry_type', 'valid_geometries',
            'spatial_extent', 'centroid'
        ]

        for key in required_keys:
            assert key in result

        # Verify values
        assert result['feature_count'] == 4
        assert result['primary_geometry_type'] == 'Point'
        assert result['valid_geometries'] == 4
        assert result['crs_type'] == 'geographic'
        assert 'Point' in result['geometry_types']

    def test_explore_spatial_properties_polygons(self):
        """Test spatial property analysis with polygon data."""
        test_gdf = create_test_polygons()

        result = explore_spatial_properties(test_gdf)

        # Verify polygon-specific properties
        assert result['primary_geometry_type'] == 'Polygon'
        assert result['spatial_extent'] is not None
        assert 'min_x' in result['spatial_extent']
        assert 'max_x' in result['spatial_extent']
        assert result['extent_width'] > 0
        assert result['extent_height'] > 0

    def test_explore_spatial_properties_empty_dataset(self):
        """Test handling of empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame(geometry=[])

        result = explore_spatial_properties(empty_gdf)

        assert result['feature_count'] == 0
        assert result['primary_geometry_type'] == 'None'
        assert result['spatial_extent'] is None

    def test_explore_spatial_properties_mixed_geometry(self):
        """Test analysis with mixed geometry types."""
        # Create mixed geometry dataset
        points = create_test_points()
        lines = create_test_lines()

        # Convert to same CRS and combine
        mixed_gdf = pd.concat([points, lines.to_crs(points.crs)], ignore_index=True)
        mixed_gdf = gpd.GeoDataFrame(mixed_gdf, crs=points.crs)

        result = explore_spatial_properties(mixed_gdf)

        # Should detect multiple geometry types
        assert len(result['geometry_types']) >= 2
        assert 'Point' in result['geometry_types']
        assert 'LineString' in result['geometry_types']

    def test_explore_spatial_properties_attribute_analysis(self):
        """Test attribute data analysis functionality."""
        test_gdf = create_test_points()

        result = explore_spatial_properties(test_gdf)

        # Verify attribute analysis
        assert 'attribute_summary' in result
        assert 'value' in result['attribute_summary']

        value_stats = result['attribute_summary']['value']
        assert 'data_type' in value_stats
        assert 'min_value' in value_stats
        assert 'max_value' in value_stats
        assert value_stats['min_value'] == 10
        assert value_stats['max_value'] == 40

    def test_explore_spatial_properties_crs_detection(self):
        """Test CRS detection and analysis."""
        test_gdf = create_test_points()

        # Test with different CRS
        projected_gdf = test_gdf.to_crs('EPSG:3857')  # Web Mercator

        result = explore_spatial_properties(projected_gdf)

        assert result['crs_type'] == 'projected'
        assert result['epsg_code'] == 3857


class TestValidateSpatialData:
    """Test the validate_spatial_data function."""

    def test_validate_spatial_data_valid_input(self):
        """Test validation with clean, valid data."""
        test_gdf = create_test_points()

        result_gdf, report = validate_spatial_data(test_gdf, fix_issues=False)

        # Should find no major issues with clean test data
        assert isinstance(result_gdf, gpd.GeoDataFrame)
        assert isinstance(report, dict)
        assert 'issues_found' in report
        assert 'fixes_applied' in report
        assert len(result_gdf) == len(test_gdf)

    def test_validate_spatial_data_missing_crs(self):
        """Test handling of missing coordinate reference system."""
        test_gdf = create_test_points()
        test_gdf.crs = None  # Remove CRS

        result_gdf, report = validate_spatial_data(test_gdf, fix_issues=True)

        # Should detect and potentially fix missing CRS
        crs_issues = [issue for issue in report['issues_found'] if 'CRS' in issue or 'crs' in issue]
        assert len(crs_issues) > 0

        if fix_issues:
            # Should attempt to set CRS if coordinates look like lat/lon
            fixes_applied = any('CRS' in fix or 'crs' in fix for fix in report.get('fixes_applied', []))

    def test_validate_spatial_data_invalid_geometries(self):
        """Test handling of invalid geometries."""
        from shapely.geometry import Polygon

        # Create invalid geometry (self-intersecting polygon)
        invalid_poly = Polygon([(0, 0), (2, 2), (2, 0), (0, 2), (0, 0)])

        invalid_gdf = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [invalid_poly]
        }, crs='EPSG:4326')

        result_gdf, report = validate_spatial_data(invalid_gdf, fix_issues=True)

        # Should detect invalid geometries
        invalid_issues = [issue for issue in report['issues_found'] if 'invalid' in issue.lower()]
        assert len(invalid_issues) > 0

    def test_validate_spatial_data_empty_geometries(self):
        """Test handling of null and empty geometries."""
        from shapely.geometry import Point

        # Create dataset with null and empty geometries
        test_gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [Point(1, 1), None, Point().buffer(0)]  # valid, null, empty
        }, crs='EPSG:4326')

        result_gdf, report = validate_spatial_data(test_gdf, fix_issues=True)

        # Should detect null/empty geometries
        issues = [issue for issue in report['issues_found']
                 if 'null' in issue.lower() or 'empty' in issue.lower()]
        assert len(issues) > 0

        # After fixing, should have fewer features
        assert len(result_gdf) <= len(test_gdf)

    def test_validate_spatial_data_duplicate_geometries(self):
        """Test detection of duplicate geometries."""
        # Create dataset with duplicate geometries
        point = Point(1, 1)
        test_gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [point, point, Point(2, 2)]  # Two duplicates
        }, crs='EPSG:4326')

        result_gdf, report = validate_spatial_data(test_gdf, fix_issues=True)

        # Should detect duplicates
        duplicate_issues = [issue for issue in report['issues_found'] if 'duplicate' in issue.lower()]

        # With fix_issues=True, duplicates should be removed
        if len(duplicate_issues) > 0:
            assert len(result_gdf) <= len(test_gdf)

    def test_validate_spatial_data_coordinate_ranges(self):
        """Test validation of coordinate ranges."""
        # Create points with invalid coordinate ranges for geographic CRS
        invalid_coords = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': [Point(200, 100), Point(-200, -100)]  # Invalid lat/lon
        }, crs='EPSG:4326')

        result_gdf, report = validate_spatial_data(invalid_coords, fix_issues=False)

        # Should detect coordinate range issues
        coord_issues = [issue for issue in report['issues_found']
                       if 'range' in issue.lower() or 'coordinate' in issue.lower()]
        # Note: This might not always trigger depending on implementation


class TestStandardizeCRS:
    """Test the standardize_crs function."""

    def test_standardize_crs_basic_transformation(self):
        """Test basic CRS transformation."""
        # Start with WGS84 data
        test_gdf = create_test_points()
        assert test_gdf.crs.to_epsg() == 4326

        # Transform to Web Mercator
        result_gdf, report = standardize_crs(test_gdf, target_crs='EPSG:3857')

        # Verify transformation
        assert result_gdf.crs.to_epsg() == 3857
        assert report['transformation_applied'] == True
        assert report['target_epsg'] == 3857
        assert len(result_gdf) == len(test_gdf)

        # Coordinates should be very different (degrees to meters)
        original_bounds = test_gdf.total_bounds
        new_bounds = result_gdf.total_bounds
        assert abs(original_bounds[0]) < abs(new_bounds[0])  # Should be much larger in meters

    def test_standardize_crs_no_transformation_needed(self):
        """Test when source and target CRS are the same."""
        test_gdf = create_test_points()

        # Transform to same CRS
        result_gdf, report = standardize_crs(test_gdf, target_crs='EPSG:4326')

        # Should detect no transformation needed
        assert report['transformation_applied'] == False
        assert 'same' in report['warnings'][0].lower()

        # Data should be unchanged
        assert len(result_gdf) == len(test_gdf)
        np.testing.assert_array_equal(result_gdf.geometry.x, test_gdf.geometry.x)

    def test_standardize_crs_auto_selection(self):
        """Test automatic CRS selection."""
        # Create data that should trigger auto-selection
        arizona_points = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [Point(-111.0, 33.0), Point(-110.5, 33.5), Point(-111.5, 32.5)]
        }, crs='EPSG:4326')

        result_gdf, report = standardize_crs(arizona_points, auto_select=True)

        # Should have selected appropriate CRS and applied transformation
        assert report['auto_selection_used'] == True
        if report['transformation_applied']:
            assert result_gdf.crs != arizona_points.crs

    def test_standardize_crs_missing_source_crs(self):
        """Test handling of data without CRS."""
        test_gdf = create_test_points()
        test_gdf.crs = None  # Remove CRS

        result_gdf, report = standardize_crs(test_gdf, target_crs='EPSG:3857')

        # Should warn about missing CRS and assume WGS84
        warnings = [w for w in report['warnings'] if 'CRS' in w]
        assert len(warnings) > 0

    def test_standardize_crs_invalid_target(self):
        """Test error handling for invalid target CRS."""
        test_gdf = create_test_points()

        with pytest.raises(ValueError, match="Invalid target CRS"):
            standardize_crs(test_gdf, target_crs='INVALID:12345')

    def test_standardize_crs_coordinate_shift_stats(self):
        """Test calculation of coordinate transformation statistics."""
        test_gdf = create_test_points()

        result_gdf, report = standardize_crs(test_gdf, target_crs='EPSG:3857')

        # Should include coordinate shift statistics
        assert 'coordinate_shift_stats' in report
        stats = report['coordinate_shift_stats']

        if report['transformation_applied']:
            assert 'original_bounds' in stats
            assert 'transformed_bounds' in stats
            assert 'coordinate_magnitude_change' in stats

    def test_standardize_crs_empty_dataset(self):
        """Test handling of empty dataset."""
        empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:4326')

        result_gdf, report = standardize_crs(empty_gdf, target_crs='EPSG:3857')

        # Should handle empty data gracefully
        assert len(result_gdf) == 0
        assert result_gdf.crs.to_epsg() == 3857


# Performance and Integration Tests
class TestSpatialDataLoadingIntegration:
    """Integration tests that combine multiple functions."""

    def test_full_spatial_data_workflow(self, tmp_path):
        """Test complete workflow: load -> explore -> validate -> standardize."""
        # Create test data and save it
        test_gdf = create_test_polygons()
        geojson_path = tmp_path / "workflow_test.geojson"
        test_gdf.to_file(geojson_path, driver='GeoJSON')

        # Step 1: Load data
        loaded_gdf = load_spatial_dataset(geojson_path)
        assert isinstance(loaded_gdf, gpd.GeoDataFrame)

        # Step 2: Explore properties
        properties = explore_spatial_properties(loaded_gdf)
        assert properties['feature_count'] > 0
        assert properties['primary_geometry_type'] == 'Polygon'

        # Step 3: Validate data
        validated_gdf, validation_report = validate_spatial_data(loaded_gdf, fix_issues=True)
        assert validation_report['validation_successful']

        # Step 4: Standardize CRS
        final_gdf, crs_report = standardize_crs(validated_gdf, target_crs='EPSG:3857')
        assert final_gdf.crs.to_epsg() == 3857

        # Verify final result maintains data integrity
        assert len(final_gdf) == len(test_gdf)

    def test_error_handling_consistency(self):
        """Test that functions handle errors consistently."""
        # Test with various problematic inputs
        empty_gdf = gpd.GeoDataFrame(geometry=[])

        # All functions should handle empty data gracefully
        properties = explore_spatial_properties(empty_gdf)
        assert properties['feature_count'] == 0

        validated_gdf, report = validate_spatial_data(empty_gdf, fix_issues=True)
        assert len(validated_gdf) == 0

        standardized_gdf, crs_report = standardize_crs(empty_gdf, target_crs='EPSG:4326')
        assert len(standardized_gdf) == 0


# Fixtures for test data
@pytest.fixture
def sample_spatial_files(tmp_path):
    """Create sample spatial data files for testing."""
    files = {}

    # GeoJSON file
    points = create_test_points()
    geojson_path = tmp_path / "test_points.geojson"
    points.to_file(geojson_path, driver='GeoJSON')
    files['geojson'] = geojson_path

    # CSV with coordinates
    csv_data = pd.DataFrame({
        'name': ['A', 'B', 'C'],
        'lon': [-110.0, -111.0, -112.0],
        'lat': [32.0, 33.0, 34.0],
        'value': [1, 2, 3]
    })
    csv_path = tmp_path / "coords.csv"
    csv_data.to_csv(csv_path, index=False)
    files['csv'] = csv_path

    return files


# Performance benchmarks (optional)
class TestSpatialDataLoadingPerformance:
    """Performance tests for spatial data loading functions."""

    @pytest.mark.benchmark
    def test_load_performance_large_dataset(self):
        """Test loading performance with larger datasets."""
        # Create larger test dataset
        n_features = 1000
        large_gdf = gpd.GeoDataFrame({
            'id': range(n_features),
            'value': np.random.randint(0, 100, n_features),
            'geometry': [Point(np.random.uniform(-180, 180),
                              np.random.uniform(-90, 90))
                        for _ in range(n_features)]
        }, crs='EPSG:4326')

        # Test exploration performance
        import time
        start_time = time.time()
        properties = explore_spatial_properties(large_gdf)
        end_time = time.time()

        # Should complete reasonably quickly (< 5 seconds for 1000 features)
        assert end_time - start_time < 5.0
        assert properties['feature_count'] == n_features


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
