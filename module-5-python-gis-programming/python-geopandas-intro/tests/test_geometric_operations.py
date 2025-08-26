"""
Test Suite for Geometric Operations Module
==========================================

This file tests all functions in the geometric_operations module to ensure
they work correctly with spatial measurements, transformations, and proximity analysis.

Test Categories:
1. calculate_spatial_metrics: Testing area, length, and distance calculations
2. create_buffers_and_zones: Testing buffer creation and zone analysis
3. geometric_transformations: Testing shape transformations and centroids
4. proximity_analysis: Testing nearest neighbor and distance analysis

Run these tests to verify your spatial geometry implementations work correctly!
"""

import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import Path
import tempfile
import warnings
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from shapely.validation import make_valid

# Import the functions we're testing
from src.geopandas_analysis.geometric_operations import (
    calculate_spatial_metrics,
    create_buffers_and_zones,
    geometric_transformations,
    proximity_analysis
)

# Import test utilities
from tests import (
    create_test_points,
    create_test_polygons,
    create_test_lines,
    SPATIAL_TOLERANCE
)


class TestCalculateSpatialMetrics:
    """Test the calculate_spatial_metrics function."""

    def test_calculate_metrics_for_polygons(self):
        """Test spatial metrics calculation for polygon data."""
        # Create test polygons with known areas
        polygons = gpd.GeoDataFrame({
            'id': [1, 2],
            'name': ['Square', 'Rectangle'],
            'geometry': [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),  # 100 sq units
                Polygon([(0, 0), (20, 0), (20, 5), (0, 5)])     # 100 sq units
            ]
        }, crs='EPSG:3857')  # Projected CRS for accurate measurements

        result = calculate_spatial_metrics(polygons)

        assert isinstance(result, gpd.GeoDataFrame)
        assert 'area' in result.columns
        assert 'perimeter' in result.columns
        assert len(result) == 2

        # Check that areas are calculated (exact values depend on implementation)
        assert all(result['area'] > 0)
        assert all(result['perimeter'] > 0)

    def test_calculate_metrics_for_lines(self):
        """Test spatial metrics calculation for line data."""
        lines = gpd.GeoDataFrame({
            'id': [1, 2],
            'name': ['Line A', 'Line B'],
            'geometry': [
                LineString([(0, 0), (10, 0)]),  # 10 units long
                LineString([(0, 0), (0, 10)])   # 10 units long
            ]
        }, crs='EPSG:3857')

        result = calculate_spatial_metrics(lines)

        assert isinstance(result, gpd.GeoDataFrame)
        assert 'length' in result.columns
        assert len(result) == 2
        assert all(result['length'] > 0)

    def test_calculate_metrics_for_points(self):
        """Test spatial metrics calculation for point data."""
        points = create_test_points()
        # Convert to projected CRS
        points = points.to_crs('EPSG:3857')

        result = calculate_spatial_metrics(points)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)
        # Points should have distance metrics
        assert any('distance' in col.lower() for col in result.columns)

    def test_metrics_with_unit_conversion(self):
        """Test spatial metrics with unit conversion."""
        polygons = create_test_polygons()
        polygons = polygons.to_crs('EPSG:3857')

        result = calculate_spatial_metrics(polygons, unit_conversion='km')

        assert isinstance(result, gpd.GeoDataFrame)
        # Should have converted units appropriately
        assert all(col in result.columns for col in ['area', 'perimeter'])

    def test_metrics_with_geographic_crs_warning(self):
        """Test that function warns when using geographic CRS."""
        polygons = create_test_polygons()  # This has EPSG:4326

        with pytest.warns(UserWarning):
            result = calculate_spatial_metrics(polygons)

    def test_metrics_empty_geodataframe(self):
        """Test metrics calculation with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:3857')

        result = calculate_spatial_metrics(empty_gdf)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 0


class TestCreateBuffersAndZones:
    """Test the create_buffers_and_zones function."""

    def test_create_basic_buffers(self):
        """Test basic buffer creation around points."""
        points = create_test_points()
        points = points.to_crs('EPSG:3857')

        result = create_buffers_and_zones(points, buffer_distance=1000)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)
        # All geometries should be polygons after buffering
        assert all(geom_type in ['Polygon', 'MultiPolygon'] for geom_type in result.geometry.geom_type)

    def test_create_variable_buffers(self):
        """Test buffer creation with variable distances."""
        points = create_test_points()
        points = points.to_crs('EPSG:3857')
        distances = [500, 1000, 1500, 2000]

        result = create_buffers_and_zones(points, buffer_distance=distances)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)
        assert all(geom_type in ['Polygon', 'MultiPolygon'] for geom_type in result.geometry.geom_type)

    def test_create_multiple_zones(self):
        """Test creating multiple buffer zones."""
        points = create_test_points()
        points = points.to_crs('EPSG:3857')

        result = create_buffers_and_zones(points, buffer_distance=1000, num_zones=3)

        assert isinstance(result, gpd.GeoDataFrame)
        # Should have multiple zones per point
        assert 'zone_id' in result.columns or 'buffer_ring' in result.columns

    def test_buffers_around_lines(self):
        """Test buffer creation around line features."""
        lines = create_test_lines()
        lines = lines.to_crs('EPSG:3857')

        result = create_buffers_and_zones(lines, buffer_distance=500)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(lines)
        assert all(geom_type in ['Polygon', 'MultiPolygon'] for geom_type in result.geometry.geom_type)

    def test_buffers_around_polygons(self):
        """Test buffer creation around polygon features."""
        polygons = create_test_polygons()
        polygons = polygons.to_crs('EPSG:3857')

        result = create_buffers_and_zones(polygons, buffer_distance=500)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(polygons)

    def test_negative_buffer(self):
        """Test negative buffer (inward buffer) on polygons."""
        polygons = create_test_polygons()
        polygons = polygons.to_crs('EPSG:3857')

        result = create_buffers_and_zones(polygons, buffer_distance=-100)

        assert isinstance(result, gpd.GeoDataFrame)
        # Some geometries might become empty with negative buffers


class TestGeometricTransformations:
    """Test the geometric_transformations function."""

    def test_calculate_centroids(self):
        """Test centroid calculation for various geometries."""
        mixed_gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [
                create_test_points().iloc[0].geometry,
                create_test_lines().iloc[0].geometry,
                create_test_polygons().iloc[0].geometry
            ]
        }, crs='EPSG:3857')

        result = geometric_transformations(mixed_gdf, operation='centroid')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(mixed_gdf)
        # All centroids should be points
        assert all(geom_type == 'Point' for geom_type in result.geometry.geom_type)

    def test_simplify_geometries(self):
        """Test geometry simplification."""
        polygons = create_test_polygons()

        result = geometric_transformations(polygons, operation='simplify', tolerance=0.1)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(polygons)
        # Simplified geometries should still be valid
        assert all(result.geometry.is_valid)

    def test_convex_hull(self):
        """Test convex hull calculation."""
        points = create_test_points()

        result = geometric_transformations(points, operation='convex_hull')

        assert isinstance(result, gpd.GeoDataFrame)
        # Convex hull of points should be a polygon or point
        assert all(geom_type in ['Point', 'Polygon'] for geom_type in result.geometry.geom_type)

    def test_envelope_bounds(self):
        """Test envelope (bounding box) calculation."""
        lines = create_test_lines()

        result = geometric_transformations(lines, operation='envelope')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(lines)
        # Envelopes should be polygons
        assert all(geom_type == 'Polygon' for geom_type in result.geometry.geom_type)

    def test_invalid_operation(self):
        """Test error handling for invalid operations."""
        points = create_test_points()

        with pytest.raises((ValueError, NotImplementedError)):
            geometric_transformations(points, operation='invalid_operation')

    def test_transformation_preserves_attributes(self):
        """Test that transformations preserve non-geometry attributes."""
        polygons = create_test_polygons()
        original_cols = set(polygons.columns) - {'geometry'}

        result = geometric_transformations(polygons, operation='centroid')

        # Should preserve original columns (except geometry is transformed)
        result_cols = set(result.columns) - {'geometry'}
        assert original_cols.issubset(result_cols)


class TestProximityAnalysis:
    """Test the proximity_analysis function."""

    def test_nearest_neighbor_points(self):
        """Test finding nearest neighbors between point datasets."""
        points1 = create_test_points()
        points2 = gpd.GeoDataFrame({
            'id': [101, 102],
            'name': ['Target A', 'Target B'],
            'geometry': [Point(0.5, 0.5), Point(2.5, 2.5)]
        }, crs='EPSG:4326')

        result = proximity_analysis(points1, points2, analysis_type='nearest_neighbor')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points1)
        # Should have distance and nearest neighbor information
        assert any('distance' in col.lower() for col in result.columns)
        assert any('nearest' in col.lower() or 'neighbor' in col.lower() for col in result.columns)

    def test_distance_matrix(self):
        """Test creating distance matrix between features."""
        points = create_test_points()

        result = proximity_analysis(points, analysis_type='distance_matrix')

        assert isinstance(result, (pd.DataFrame, np.ndarray, dict))
        # Distance matrix should be square
        if isinstance(result, pd.DataFrame):
            assert result.shape[0] == result.shape[1] == len(points)

    def test_proximity_within_threshold(self):
        """Test finding features within distance threshold."""
        points1 = create_test_points()
        points2 = create_test_points()
        # Offset the second dataset slightly
        points2.geometry = points2.geometry.translate(xoff=0.01, yoff=0.01)

        result = proximity_analysis(points1, points2, analysis_type='within_distance',
                                  distance_threshold=0.1)

        assert isinstance(result, gpd.GeoDataFrame)
        # Should return pairs within threshold
        assert len(result) >= 0

    def test_k_nearest_neighbors(self):
        """Test finding k nearest neighbors."""
        points1 = create_test_points()
        points2 = create_test_points()

        result = proximity_analysis(points1, points2, analysis_type='k_nearest', k=2)

        assert isinstance(result, gpd.GeoDataFrame)
        # Should have k neighbors per input point
        assert len(result) <= len(points1) * 2

    def test_proximity_analysis_projected_crs(self):
        """Test proximity analysis with projected CRS for accurate distances."""
        points1 = create_test_points()
        points2 = create_test_points()

        # Convert to projected CRS
        points1 = points1.to_crs('EPSG:3857')
        points2 = points2.to_crs('EPSG:3857')

        result = proximity_analysis(points1, points2, analysis_type='nearest_neighbor')

        assert isinstance(result, gpd.GeoDataFrame)
        assert result.crs == points1.crs

    def test_proximity_with_different_geometry_types(self):
        """Test proximity analysis between different geometry types."""
        points = create_test_points()
        polygons = create_test_polygons()

        result = proximity_analysis(points, polygons, analysis_type='nearest_neighbor')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)

    def test_self_proximity_analysis(self):
        """Test proximity analysis within same dataset."""
        points = create_test_points()

        result = proximity_analysis(points, analysis_type='nearest_neighbor')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)

    def test_empty_dataset_proximity(self):
        """Test proximity analysis with empty dataset."""
        points = create_test_points()
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:4326')

        result = proximity_analysis(points, empty_gdf, analysis_type='nearest_neighbor')

        # Should handle empty dataset gracefully
        assert isinstance(result, gpd.GeoDataFrame)

    def test_invalid_analysis_type(self):
        """Test error handling for invalid analysis types."""
        points = create_test_points()

        with pytest.raises((ValueError, NotImplementedError)):
            proximity_analysis(points, analysis_type='invalid_type')


# Integration and performance tests
class TestGeometricOperationsIntegration:
    """Integration tests combining multiple geometric operations."""

    def test_complete_geometric_workflow(self):
        """Test complete workflow: load data -> calculate metrics -> buffer -> analyze proximity."""
        # Start with points
        points = create_test_points()
        points = points.to_crs('EPSG:3857')

        # Calculate metrics
        points_with_metrics = calculate_spatial_metrics(points)

        # Create buffers
        buffered = create_buffers_and_zones(points_with_metrics, buffer_distance=1000)

        # Transform to centroids
        centroids = geometric_transformations(buffered, operation='centroid')

        # Analyze proximity
        proximity_result = proximity_analysis(centroids, analysis_type='distance_matrix')

        # All steps should complete successfully
        assert isinstance(points_with_metrics, gpd.GeoDataFrame)
        assert isinstance(buffered, gpd.GeoDataFrame)
        assert isinstance(centroids, gpd.GeoDataFrame)
        assert proximity_result is not None

    @pytest.mark.benchmark
    def test_performance_large_dataset(self):
        """Test performance with larger dataset."""
        # Create larger test dataset
        n_points = 1000
        x_coords = np.random.uniform(-180, 180, n_points)
        y_coords = np.random.uniform(-90, 90, n_points)

        large_points = gpd.GeoDataFrame({
            'id': range(n_points),
            'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
        }, crs='EPSG:4326')

        large_points = large_points.to_crs('EPSG:3857')

        # Test that operations complete in reasonable time
        import time

        start_time = time.time()
        metrics = calculate_spatial_metrics(large_points)
        metrics_time = time.time() - start_time

        start_time = time.time()
        buffered = create_buffers_and_zones(large_points.head(100), buffer_distance=1000)
        buffer_time = time.time() - start_time

        # Performance assertions (adjust thresholds as needed)
        assert metrics_time < 10.0  # Should complete within 10 seconds
        assert buffer_time < 30.0   # Buffer creation might be slower

        assert len(metrics) == n_points
        assert len(buffered) == 100

    def test_crs_consistency_across_operations(self):
        """Test that CRS is preserved across geometric operations."""
        original_crs = 'EPSG:3857'
        points = create_test_points().to_crs(original_crs)

        # All operations should preserve CRS
        metrics = calculate_spatial_metrics(points)
        assert metrics.crs == original_crs

        buffered = create_buffers_and_zones(points, buffer_distance=1000)
        assert buffered.crs == original_crs

        transformed = geometric_transformations(points, operation='centroid')
        assert transformed.crs == original_crs
