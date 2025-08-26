"""
Test Suite for Spatial Joins Analysis Module
===========================================

This file tests all functions in the spatial_joins_analysis module to ensure
they work correctly with spatial relationships, joins, and aggregations.

Test Categories:
1. spatial_intersection_analysis: Testing spatial intersections and overlays
2. point_in_polygon_analysis: Testing point-in-polygon operations
3. spatial_aggregation: Testing spatial grouping and aggregation
4. multi_criteria_spatial_filter: Testing complex spatial filtering

Run these tests to verify your spatial joins implementations work correctly!
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
from src.geopandas_analysis.spatial_joins_analysis import (
    spatial_intersection_analysis,
    point_in_polygon_analysis,
    spatial_aggregation,
    multi_criteria_spatial_filter
)

# Import test utilities
from tests import (
    create_test_points,
    create_test_polygons,
    create_test_lines,
    SPATIAL_TOLERANCE
)


class TestSpatialIntersectionAnalysis:
    """Test the spatial_intersection_analysis function."""

    def test_polygon_intersection_basic(self):
        """Test basic polygon intersection analysis."""
        # Create overlapping polygons
        gdf1 = gpd.GeoDataFrame({
            'id': [1, 2],
            'name': ['Polygon A', 'Polygon B'],
            'value': [100, 200],
            'geometry': [
                Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
                Polygon([(4, 0), (7, 0), (7, 3), (4, 3)])
            ]
        }, crs='EPSG:4326')

        gdf2 = gpd.GeoDataFrame({
            'id': [10, 20],
            'category': ['Zone X', 'Zone Y'],
            'priority': [1, 2],
            'geometry': [
                Polygon([(2, 0), (5, 0), (5, 3), (2, 3)]),  # Overlaps both A and B
                Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])   # Overlaps only A
            ]
        }, crs='EPSG:4326')

        result = spatial_intersection_analysis(gdf1, gdf2, operation='intersection')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) >= 1  # Should have at least one intersection

        # Should have columns from both input GeoDataFrames
        assert any('name' in col or 'id' in col for col in result.columns)
        assert any('category' in col or 'priority' in col for col in result.columns)

    def test_line_polygon_intersection(self):
        """Test intersection between lines and polygons."""
        lines = create_test_lines()
        polygons = create_test_polygons()

        result = spatial_intersection_analysis(lines, polygons, operation='intersection')

        assert isinstance(result, gpd.GeoDataFrame)
        # Result geometries depend on actual intersections

    def test_spatial_overlay_union(self):
        """Test spatial overlay with union operation."""
        polygons1 = create_test_polygons()
        polygons2 = gpd.GeoDataFrame({
            'id': [100, 200],
            'type': ['Area X', 'Area Y'],
            'geometry': [
                Polygon([(0.5, 0.5), (2.5, 0.5), (2.5, 2.5), (0.5, 2.5)]),
                Polygon([(3, 3), (5, 3), (5, 5), (3, 5)])
            ]
        }, crs='EPSG:4326')

        result = spatial_intersection_analysis(polygons1, polygons2, operation='union')

        assert isinstance(result, gpd.GeoDataFrame)

    def test_spatial_overlay_difference(self):
        """Test spatial overlay with difference operation."""
        polygons1 = create_test_polygons()
        polygons2 = gpd.GeoDataFrame({
            'id': [100],
            'geometry': [Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])]
        }, crs='EPSG:4326')

        result = spatial_intersection_analysis(polygons1, polygons2, operation='difference')

        assert isinstance(result, gpd.GeoDataFrame)

    def test_intersection_with_identical_crs(self):
        """Test intersection with identical CRS."""
        gdf1 = create_test_polygons()
        gdf2 = create_test_polygons()

        result = spatial_intersection_analysis(gdf1, gdf2, operation='intersection')

        assert isinstance(result, gpd.GeoDataFrame)
        assert result.crs == gdf1.crs

    def test_intersection_with_different_crs(self):
        """Test intersection with different CRS (should be handled)."""
        gdf1 = create_test_polygons()  # EPSG:4326
        gdf2 = create_test_polygons().to_crs('EPSG:3857')  # Web Mercator

        result = spatial_intersection_analysis(gdf1, gdf2, operation='intersection')

        assert isinstance(result, gpd.GeoDataFrame)

    def test_no_intersections(self):
        """Test when there are no spatial intersections."""
        gdf1 = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]
        }, crs='EPSG:4326')

        gdf2 = gpd.GeoDataFrame({
            'id': [2],
            'geometry': [Polygon([(5, 5), (6, 5), (6, 6), (5, 6)])]
        }, crs='EPSG:4326')

        result = spatial_intersection_analysis(gdf1, gdf2, operation='intersection')

        assert isinstance(result, gpd.GeoDataFrame)
        # Empty result is valid when no intersections exist

    def test_invalid_operation(self):
        """Test error handling for invalid operations."""
        gdf1 = create_test_polygons()
        gdf2 = create_test_polygons()

        with pytest.raises((ValueError, NotImplementedError)):
            spatial_intersection_analysis(gdf1, gdf2, operation='invalid_operation')


class TestPointInPolygonAnalysis:
    """Test the point_in_polygon_analysis function."""

    def test_basic_point_in_polygon(self):
        """Test basic point-in-polygon analysis."""
        points = gpd.GeoDataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Point A', 'Point B', 'Point C', 'Point D'],
            'value': [10, 20, 30, 40],
            'geometry': [
                Point(1, 1),    # Inside first polygon
                Point(2, 2),    # Inside overlapping area
                Point(5, 5),    # Outside all polygons
                Point(1.5, 3.5) # Inside second polygon
            ]
        }, crs='EPSG:4326')

        polygons = create_test_polygons()

        result = point_in_polygon_analysis(points, polygons)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) >= 1  # At least some points should be inside polygons

        # Should have attributes from both datasets
        assert any('name' in col for col in result.columns)
        assert any(col in ['area_value', 'id'] for col in result.columns)

    def test_point_in_polygon_with_holes(self):
        """Test point-in-polygon with polygons containing holes."""
        # Create polygon with hole
        exterior = [(0, 0), (4, 0), (4, 4), (0, 4)]
        interior = [(1, 1), (3, 1), (3, 3), (1, 3)]
        polygon_with_hole = Polygon(exterior, [interior])

        polygons = gpd.GeoDataFrame({
            'id': [1],
            'name': ['Polygon with hole'],
            'geometry': [polygon_with_hole]
        }, crs='EPSG:4326')

        points = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'geometry': [
                Point(0.5, 0.5),  # Inside polygon, outside hole
                Point(2, 2),      # Inside hole (should not match)
                Point(5, 5)       # Outside polygon entirely
            ]
        }, crs='EPSG:4326')

        result = point_in_polygon_analysis(points, polygons)

        assert isinstance(result, gpd.GeoDataFrame)

    def test_multiple_polygon_matches(self):
        """Test points that fall in multiple overlapping polygons."""
        # Create overlapping polygons
        polygons = gpd.GeoDataFrame({
            'id': [1, 2],
            'zone': ['Zone A', 'Zone B'],
            'geometry': [
                Polygon([(0, 0), (3, 0), (3, 3), (0, 3)]),
                Polygon([(2, 2), (5, 2), (5, 5), (2, 5)])  # Overlaps with Zone A
            ]
        }, crs='EPSG:4326')

        points = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [Point(2.5, 2.5)]  # In overlap area
        }, crs='EPSG:4326')

        result = point_in_polygon_analysis(points, polygons, how='left')

        assert isinstance(result, gpd.GeoDataFrame)

    def test_point_in_polygon_different_predicates(self):
        """Test different spatial predicates (within, intersects, etc.)."""
        points = create_test_points()
        polygons = create_test_polygons()

        # Test 'within' predicate
        result_within = point_in_polygon_analysis(points, polygons, predicate='within')
        assert isinstance(result_within, gpd.GeoDataFrame)

        # Test 'intersects' predicate
        result_intersects = point_in_polygon_analysis(points, polygons, predicate='intersects')
        assert isinstance(result_intersects, gpd.GeoDataFrame)

    def test_no_points_in_polygons(self):
        """Test when no points fall within any polygons."""
        points = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': [Point(10, 10), Point(20, 20)]  # Far from test polygons
        }, crs='EPSG:4326')

        polygons = create_test_polygons()

        result = point_in_polygon_analysis(points, polygons)

        assert isinstance(result, gpd.GeoDataFrame)
        # Empty or no matches is valid

    def test_empty_datasets(self):
        """Test with empty point or polygon datasets."""
        points = create_test_points()
        empty_polygons = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:4326')

        result = point_in_polygon_analysis(points, empty_polygons)

        assert isinstance(result, gpd.GeoDataFrame)

    def test_point_in_polygon_preserve_attributes(self):
        """Test that all attributes are preserved in the join."""
        points = create_test_points()
        polygons = create_test_polygons()

        result = point_in_polygon_analysis(points, polygons, how='left')

        assert isinstance(result, gpd.GeoDataFrame)
        # Should preserve point attributes
        assert all(col in result.columns for col in ['id', 'name', 'value'])


class TestSpatialAggregation:
    """Test the spatial_aggregation function."""

    def test_aggregate_points_by_polygon(self):
        """Test aggregating points within polygons."""
        # Create points with values to aggregate
        points = gpd.GeoDataFrame({
            'id': [1, 2, 3, 4, 5],
            'value': [10, 20, 30, 40, 50],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'geometry': [
                Point(0.5, 0.5),   # Inside first polygon
                Point(1.5, 1.5),   # Inside first polygon
                Point(2.5, 2.5),   # Inside second polygon
                Point(3.5, 3.5),   # Inside second polygon
                Point(10, 10)      # Outside all polygons
            ]
        }, crs='EPSG:4326')

        polygons = create_test_polygons()

        result = spatial_aggregation(points, polygons,
                                   groupby_column='id',
                                   agg_column='value',
                                   agg_function='sum')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) <= len(polygons)

        # Should have aggregated values
        assert any('sum' in col.lower() or 'value' in col.lower() for col in result.columns)

    def test_multiple_aggregation_functions(self):
        """Test multiple aggregation functions on same data."""
        points = create_test_points()
        # Add numeric column for aggregation
        points['score'] = [100, 200, 300, 400]

        polygons = create_test_polygons()

        agg_functions = ['count', 'sum', 'mean', 'max', 'min']

        result = spatial_aggregation(points, polygons,
                                   groupby_column='id',
                                   agg_column='score',
                                   agg_function=agg_functions)

        assert isinstance(result, gpd.GeoDataFrame)

    def test_aggregate_by_attribute(self):
        """Test aggregating by non-spatial attribute."""
        points = gpd.GeoDataFrame({
            'id': [1, 2, 3, 4],
            'zone': ['North', 'North', 'South', 'South'],
            'value': [10, 20, 30, 40],
            'geometry': [Point(x, y) for x, y in [(0, 0), (1, 1), (2, 2), (3, 3)]]
        }, crs='EPSG:4326')

        result = spatial_aggregation(points, groupby_column='zone',
                                   agg_column='value', agg_function='mean')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2  # Two zones: North and South

    def test_aggregate_polygon_areas(self):
        """Test aggregating polygon areas by attribute."""
        polygons = create_test_polygons()
        # Add category for grouping
        polygons['category'] = ['Type1', 'Type2']

        result = spatial_aggregation(polygons, groupby_column='category',
                                   agg_column='area_value', agg_function='sum')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) <= len(polygons.category.unique())

    def test_spatial_dissolve(self):
        """Test spatial dissolve operation."""
        polygons = create_test_polygons()
        # Add dissolve attribute
        polygons['dissolve_field'] = ['Group1', 'Group1']  # Same group to dissolve

        result = spatial_aggregation(polygons, groupby_column='dissolve_field',
                                   operation='dissolve')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 1  # Should dissolve into single polygon

    def test_empty_aggregation(self):
        """Test aggregation with no data."""
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry', 'value'], crs='EPSG:4326')

        result = spatial_aggregation(empty_gdf, groupby_column='value',
                                   agg_column='value', agg_function='sum')

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 0

    def test_invalid_aggregation_function(self):
        """Test error handling for invalid aggregation functions."""
        points = create_test_points()

        with pytest.raises((ValueError, NotImplementedError)):
            spatial_aggregation(points, groupby_column='id',
                              agg_column='value', agg_function='invalid_function')


class TestMultiCriteriaSpatialFilter:
    """Test the multi_criteria_spatial_filter function."""

    def test_attribute_and_spatial_filter(self):
        """Test filtering by both attribute and spatial criteria."""
        points = gpd.GeoDataFrame({
            'id': [1, 2, 3, 4, 5],
            'value': [10, 25, 30, 45, 50],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'geometry': [Point(x, y) for x, y in [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]]
        }, crs='EPSG:4326')

        polygons = create_test_polygons()

        # Filter points: value > 20 AND within polygons
        criteria = {
            'attribute_filter': {'value': {'operator': '>', 'threshold': 20}},
            'spatial_filter': {'geometry': polygons, 'predicate': 'within'}
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) <= len(points)

        # All results should meet both criteria
        if len(result) > 0:
            assert all(result['value'] > 20)

    def test_multiple_attribute_filters(self):
        """Test multiple attribute-based filters."""
        points = create_test_points()
        points['score'] = [85, 92, 78, 96]
        points['active'] = [True, True, False, True]

        criteria = {
            'attribute_filter': {
                'score': {'operator': '>=', 'threshold': 80},
                'active': {'operator': '==', 'threshold': True}
            }
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        if len(result) > 0:
            assert all(result['score'] >= 80)
            assert all(result['active'] == True)

    def test_buffer_distance_filter(self):
        """Test filtering based on distance from features."""
        points = create_test_points()
        reference_points = gpd.GeoDataFrame({
            'id': [100],
            'geometry': [Point(1, 1)]
        }, crs='EPSG:4326')

        criteria = {
            'distance_filter': {
                'reference_geometry': reference_points,
                'distance_threshold': 0.5,
                'operator': '<='
            }
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) <= len(points)

    def test_complex_combined_criteria(self):
        """Test complex combination of multiple criteria types."""
        polygons = create_test_polygons()
        polygons['area_calc'] = polygons.geometry.area
        polygons['priority'] = [1, 3]

        reference_point = gpd.GeoDataFrame({
            'geometry': [Point(2, 2)]
        }, crs='EPSG:4326')

        criteria = {
            'attribute_filter': {
                'priority': {'operator': '>', 'threshold': 1},
                'area_calc': {'operator': '>', 'threshold': 0}
            },
            'spatial_filter': {
                'geometry': reference_point,
                'predicate': 'intersects'
            },
            'distance_filter': {
                'reference_geometry': reference_point,
                'distance_threshold': 2.0,
                'operator': '<='
            }
        }

        result = multi_criteria_spatial_filter(polygons, criteria)

        assert isinstance(result, gpd.GeoDataFrame)

    def test_category_filter(self):
        """Test filtering by categorical values."""
        points = create_test_points()
        points['zone'] = ['North', 'South', 'North', 'East']

        criteria = {
            'category_filter': {
                'zone': {'values': ['North', 'East']}
            }
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        if len(result) > 0:
            assert all(result['zone'].isin(['North', 'East']))

    def test_bounding_box_filter(self):
        """Test filtering by bounding box."""
        points = create_test_points()

        criteria = {
            'bbox_filter': {
                'bounds': [0.5, 0.5, 2.5, 2.5]  # [minx, miny, maxx, maxy]
            }
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) <= len(points)

    def test_no_matching_criteria(self):
        """Test when no features meet the criteria."""
        points = create_test_points()

        criteria = {
            'attribute_filter': {
                'value': {'operator': '>', 'threshold': 1000}  # Very high threshold
            }
        }

        result = multi_criteria_spatial_filter(points, criteria)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 0

    def test_empty_criteria(self):
        """Test with empty or no criteria (should return all data)."""
        points = create_test_points()

        result = multi_criteria_spatial_filter(points, {})

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == len(points)

    def test_invalid_criteria_format(self):
        """Test error handling for invalid criteria format."""
        points = create_test_points()

        with pytest.raises((ValueError, KeyError, TypeError)):
            multi_criteria_spatial_filter(points, {'invalid': 'criteria'})


# Integration and performance tests
class TestSpatialJoinsIntegration:
    """Integration tests combining multiple spatial join operations."""

    def test_complete_spatial_analysis_workflow(self):
        """Test complete workflow: intersection -> point-in-polygon -> aggregation -> filtering."""
        # Create comprehensive test datasets
        points = create_test_points()
        points['score'] = [85, 92, 78, 96]

        polygons = create_test_polygons()
        lines = create_test_lines()

        # Step 1: Point in polygon analysis
        points_in_polygons = point_in_polygon_analysis(points, polygons)

        # Step 2: Spatial aggregation
        if len(points_in_polygons) > 0:
            aggregated = spatial_aggregation(points_in_polygons,
                                           groupby_column='id',
                                           agg_column='score',
                                           agg_function='mean')
            assert isinstance(aggregated, gpd.GeoDataFrame)

        # Step 3: Multi-criteria filtering
        criteria = {'attribute_filter': {'score': {'operator': '>', 'threshold': 80}}}
        filtered_points = multi_criteria_spatial_filter(points, criteria)

        # Step 4: Intersection analysis with lines
        if len(filtered_points) > 0:
            intersection_result = spatial_intersection_analysis(
                filtered_points.buffer(0.1), polygons, operation='intersection'
            )

        # All steps should complete successfully
        assert isinstance(points_in_polygons, gpd.GeoDataFrame)
        assert isinstance(filtered_points, gpd.GeoDataFrame)

    @pytest.mark.benchmark
    def test_performance_large_spatial_join(self):
        """Test performance with larger datasets."""
        # Create larger test datasets
        n_points = 5000
        n_polygons = 50

        # Generate random points
        np.random.seed(42)
        x_coords = np.random.uniform(0, 10, n_points)
        y_coords = np.random.uniform(0, 10, n_points)

        large_points = gpd.GeoDataFrame({
            'id': range(n_points),
            'value': np.random.randint(1, 100, n_points),
            'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
        }, crs='EPSG:4326')

        # Generate random polygons (simplified grid)
        large_polygons = []
        for i in range(n_polygons):
            x = (i % 10) * 1.0
            y = (i // 10) * 1.0
            poly = Polygon([(x, y), (x+0.8, y), (x+0.8, y+0.8), (x, y+0.8)])
            large_polygons.append(poly)

        large_polygon_gdf = gpd.GeoDataFrame({
            'id': range(n_polygons),
            'zone': [f'Zone_{i}' for i in range(n_polygons)],
            'geometry': large_polygons
        }, crs='EPSG:4326')

        # Test that large spatial join completes in reasonable time
        import time

        start_time = time.time()
        result = point_in_polygon_analysis(large_points, large_polygon_gdf)
        join_time = time.time() - start_time

        # Performance assertions (adjust thresholds as needed)
        assert join_time < 60.0  # Should complete within 60 seconds

        assert isinstance(result, gpd.GeoDataFrame)
        print(f"Large spatial join completed in {join_time:.2f} seconds")

    def test_memory_efficiency_spatial_operations(self):
        """Test memory efficiency of spatial operations."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Create moderately sized dataset
        points = create_test_points()
        polygons = create_test_polygons()

        # Perform multiple operations
        for _ in range(10):
            result = point_in_polygon_analysis(points, polygons)
            aggregated = spatial_aggregation(points, groupby_column='id',
                                           agg_column='value', agg_function='count')

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024

    def test_crs_handling_across_operations(self):
        """Test consistent CRS handling across all spatial operations."""
        original_crs = 'EPSG:3857'  # Web Mercator

        points = create_test_points().to_crs(original_crs)
        polygons = create_test_polygons().to_crs(original_crs)

        # All operations should preserve or handle CRS correctly
        pip_result = point_in_polygon_analysis(points, polygons)
        if len(pip_result) > 0:
            assert pip_result.crs == original_crs

        intersection_result = spatial_intersection_analysis(polygons, polygons,
                                                           operation='intersection')
        if len(intersection_result) > 0:
            assert intersection_result.crs == original_crs

        agg_result = spatial_aggregation(points, groupby_column='id',
                                       agg_column='value', agg_function='count')
        if len(agg_result) > 0:
            assert agg_result.crs == original_crs
