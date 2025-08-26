"""
Test suite for raster-vector integration functionality.

This module contains comprehensive tests for operations that combine raster and vector
data, including zonal statistics, spatial sampling, raster-vector overlays,
and conversion between raster and vector formats.

Author: Student Test Suite
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling
from rasterio.features import rasterize, shapes
from rasterio.mask import mask
import tempfile
from pathlib import Path
import warnings
from unittest.mock import patch, MagicMock
import time
from shapely.geometry import box, Point, Polygon, MultiPolygon
from shapely.geometry import LineString
import json

# Import the functions we're testing
try:
    from src.rasterio_analysis.memory_efficient import (
        extract_raster_statistics_by_zones,
        process_raster_windowed,
        monitor_memory_usage
    )
    from src.rasterio_analysis.raster_processing import (
        analyze_local_raster,
        get_raster_summary
    )
except ImportError as e:
    pytest.skip(f"Could not import raster-vector integration functions: {e}", allow_module_level=True)


class TestRasterVectorIntegration:
    """Test suite for raster-vector integration operations."""

    @pytest.fixture(scope="class")
    def test_raster_path(self, tmp_path_factory):
        """Create a test raster with known values for zonal statistics."""
        tmp_dir = tmp_path_factory.mktemp("raster_vector_data")
        raster_path = tmp_dir / "test_zones.tif"

        width, height = 1000, 800

        # Create zones with different values
        data = np.zeros((height, width), dtype=np.float32)

        # Zone 1: Northwest quadrant = 100
        data[0:400, 0:500] = 100.0

        # Zone 2: Northeast quadrant = 200
        data[0:400, 500:1000] = 200.0

        # Zone 3: Southwest quadrant = 300
        data[400:800, 0:500] = 300.0

        # Zone 4: Southeast quadrant = 400
        data[400:800, 500:1000] = 400.0

        # Add some noise
        noise = np.random.normal(0, 5, (height, width))
        data = data + noise

        # Add some nodata areas
        data[0:50, 0:50] = np.nan
        data[-50:, -50:] = np.nan

        bounds = (-112.0, 33.0, -111.0, 34.0)  # Arizona area
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=transform, nodata=np.nan
        ) as dst:
            dst.write(data, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def landcover_raster_path(self, tmp_path_factory):
        """Create a categorical landcover raster."""
        tmp_dir = tmp_path_factory.mktemp("landcover_data")
        raster_path = tmp_dir / "landcover.tif"

        width, height = 500, 400

        # Create landcover classes (1-5)
        np.random.seed(42)  # For reproducible results
        landcover = np.random.choice([1, 2, 3, 4, 5], size=(height, width),
                                   p=[0.3, 0.2, 0.2, 0.2, 0.1])

        # Create some spatial structure
        # Forest (class 1) in northwest
        landcover[0:150, 0:200] = 1
        # Urban (class 5) in center
        landcover[150:250, 200:350] = 5
        # Water (class 2) as rivers
        landcover[180:200, :] = 2  # Horizontal river
        landcover[:, 240:260] = 2  # Vertical river

        landcover = landcover.astype(np.uint8)

        bounds = (-112.0, 33.0, -111.0, 34.0)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=landcover.dtype, crs='EPSG:4326',
            transform=transform, nodata=0
        ) as dst:
            dst.write(landcover, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def test_polygons_gdf(self):
        """Create test polygons that align with raster zones."""
        polygons = [
            box(-112.0, 33.5, -111.5, 34.0),  # Northwest - should get ~100 values
            box(-111.5, 33.5, -111.0, 34.0),  # Northeast - should get ~200 values
            box(-112.0, 33.0, -111.5, 33.5),  # Southwest - should get ~300 values
            box(-111.5, 33.0, -111.0, 33.5),  # Southeast - should get ~400 values
        ]

        gdf = gpd.GeoDataFrame({
            'zone_id': ['NW', 'NE', 'SW', 'SE'],
            'zone_name': ['Northwest', 'Northeast', 'Southwest', 'Southeast'],
            'expected_mean': [100, 200, 300, 400],
            'geometry': polygons
        }, crs='EPSG:4326')

        return gdf

    @pytest.fixture(scope="class")
    def irregular_polygons_gdf(self):
        """Create irregular polygon shapes for testing."""
        # Complex polygon that crosses multiple raster zones
        complex_poly = Polygon([
            (-112.0, 33.25), (-111.75, 33.25), (-111.75, 33.75),
            (-111.25, 33.75), (-111.25, 34.0), (-112.0, 34.0),
            (-112.0, 33.25)
        ])

        # Small polygon entirely within one zone
        small_poly = Polygon([
            (-111.8, 33.6), (-111.7, 33.6), (-111.7, 33.7), (-111.8, 33.7), (-111.8, 33.6)
        ])

        # Polygon with hole
        outer_ring = [(-111.6, 33.1), (-111.1, 33.1), (-111.1, 33.4), (-111.6, 33.4), (-111.6, 33.1)]
        hole = [(-111.5, 33.15), (-111.2, 33.15), (-111.2, 33.35), (-111.5, 33.35), (-111.5, 33.15)]
        poly_with_hole = Polygon(outer_ring, [hole])

        gdf = gpd.GeoDataFrame({
            'poly_id': ['complex', 'small', 'with_hole'],
            'geometry': [complex_poly, small_poly, poly_with_hole]
        }, crs='EPSG:4326')

        return gdf

    @pytest.fixture(scope="class")
    def test_points_gdf(self):
        """Create test points for point-based sampling."""
        # Points in different zones
        points = [
            Point(-111.75, 33.75),  # Northwest zone
            Point(-111.25, 33.75),  # Northeast zone
            Point(-111.75, 33.25),  # Southwest zone
            Point(-111.25, 33.25),  # Southeast zone
            Point(-111.5, 33.5),    # Center point
        ]

        gdf = gpd.GeoDataFrame({
            'point_id': ['NW_pt', 'NE_pt', 'SW_pt', 'SE_pt', 'center'],
            'expected_zone': ['NW', 'NE', 'SW', 'SE', 'mixed'],
            'geometry': points
        }, crs='EPSG:4326')

        return gdf

    def test_basic_zonal_statistics(self, test_raster_path, test_polygons_gdf):
        """Test basic zonal statistics functionality."""
        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            test_polygons_gdf,
            statistics=['mean', 'std', 'min', 'max', 'count']
        )

        # Check structure
        assert isinstance(result_gdf, gpd.GeoDataFrame)
        assert len(result_gdf) == len(test_polygons_gdf)

        # Should have original columns
        original_cols = set(test_polygons_gdf.columns)
        result_cols = set(result_gdf.columns)
        assert original_cols.issubset(result_cols)

        # Check for statistics columns
        stat_cols = [col for col in result_cols if any(stat in col for stat in ['mean', 'std', 'min', 'max', 'count'])]
        assert len(stat_cols) >= 5  # At least 5 statistics columns

        # Verify statistics are reasonable
        for idx, row in result_gdf.iterrows():
            zone_id = row['zone_id']
            expected_mean = row['expected_mean']

            # Find the mean column
            mean_cols = [col for col in result_cols if 'mean' in col]
            if mean_cols:
                actual_mean = row[mean_cols[0]]
                if pd.notna(actual_mean):
                    # Should be close to expected value (within noise tolerance)
                    assert abs(actual_mean - expected_mean) < 20

    def test_zonal_statistics_different_statistics(self, test_raster_path, test_polygons_gdf):
        """Test zonal statistics with different statistic types."""
        stats_sets = [
            ['mean'],
            ['mean', 'std'],
            ['mean', 'std', 'min', 'max'],
            ['mean', 'std', 'min', 'max', 'count', 'sum']
        ]

        for stats in stats_sets:
            result_gdf = extract_raster_statistics_by_zones(
                test_raster_path,
                test_polygons_gdf,
                statistics=stats
            )

            # Should have columns for each requested statistic
            result_cols = set(result_gdf.columns)
            for stat in stats:
                stat_cols = [col for col in result_cols if stat in col]
                assert len(stat_cols) >= 1, f"No {stat} column found"

    def test_zonal_statistics_categorical_data(self, landcover_raster_path, test_polygons_gdf):
        """Test zonal statistics with categorical data."""
        result_gdf = extract_raster_statistics_by_zones(
            landcover_raster_path,
            test_polygons_gdf,
            statistics=['mode', 'unique_count', 'majority_percent'],
            categorical_bands=[1]
        )

        # Should have categorical statistics
        result_cols = set(result_gdf.columns)
        categorical_stats = ['mode', 'unique', 'majority']
        for cat_stat in categorical_stats:
            matching_cols = [col for col in result_cols if cat_stat in col]
            assert len(matching_cols) > 0, f"No {cat_stat} column found"

        # Check that mode values are valid landcover classes
        mode_cols = [col for col in result_cols if 'mode' in col]
        if mode_cols:
            for mode_val in result_gdf[mode_cols[0]].dropna():
                assert mode_val in [1, 2, 3, 4, 5], f"Invalid landcover class: {mode_val}"

    def test_zonal_statistics_irregular_polygons(self, test_raster_path, irregular_polygons_gdf):
        """Test zonal statistics with irregular polygon shapes."""
        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            irregular_polygons_gdf,
            statistics=['mean', 'count']
        )

        assert len(result_gdf) == len(irregular_polygons_gdf)

        # Complex polygon should have statistics from multiple zones
        complex_row = result_gdf[result_gdf['poly_id'] == 'complex']
        assert len(complex_row) == 1

        count_cols = [col for col in result_gdf.columns if 'count' in col]
        if count_cols:
            complex_count = complex_row[count_cols[0]].iloc[0]
            small_count = result_gdf[result_gdf['poly_id'] == 'small'][count_cols[0]].iloc[0]

            # Complex polygon should have more pixels than small polygon
            assert complex_count > small_count

    def test_zonal_statistics_crs_mismatch_handling(self, test_raster_path, tmp_path):
        """Test handling of CRS mismatches between raster and vector."""
        # Create polygons in a different CRS
        polygons = [box(-12467000, 3896000, -12356000, 4107000)]  # Web Mercator extent
        gdf_wrong_crs = gpd.GeoDataFrame({
            'id': [1],
            'geometry': polygons
        }, crs='EPSG:3857')  # Web Mercator

        # Should either handle reprojection or raise informative error
        try:
            result_gdf = extract_raster_statistics_by_zones(
                test_raster_path,
                gdf_wrong_crs,
                statistics=['mean']
            )
            # If successful, should have reprojected and computed statistics
            assert len(result_gdf) == 1
        except ValueError as e:
            # Should provide clear error about CRS mismatch
            assert 'crs' in str(e).lower() or 'coordinate' in str(e).lower()

    def test_zonal_statistics_no_overlap(self, test_raster_path):
        """Test zonal statistics when polygons don't overlap raster."""
        # Create polygons outside raster bounds
        non_overlapping_polygons = [
            box(-120.0, 40.0, -119.0, 41.0),  # Far north
            box(-100.0, 25.0, -99.0, 26.0)    # Far east
        ]

        gdf_no_overlap = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': non_overlapping_polygons
        }, crs='EPSG:4326')

        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            gdf_no_overlap,
            statistics=['mean', 'count']
        )

        # Should return GeoDataFrame with null/zero statistics
        assert len(result_gdf) == 2

        count_cols = [col for col in result_gdf.columns if 'count' in col]
        if count_cols:
            # Count should be 0 for non-overlapping areas
            assert all(result_gdf[count_cols[0]].fillna(0) == 0)

    def test_point_sampling_from_raster(self, test_raster_path, test_points_gdf, tmp_path):
        """Test sampling raster values at point locations."""
        # This would be a function that samples raster at point locations
        # For now, we'll simulate this functionality

        sampled_points = test_points_gdf.copy()

        # Sample raster values at point locations
        with rasterio.open(test_raster_path) as src:
            # Convert points to pixel coordinates
            coords = [(point.x, point.y) for point in sampled_points.geometry]
            sampled_values = list(src.sample(coords))

            # Add sampled values to the GeoDataFrame
            sampled_points['raster_value'] = [val[0] if not np.isnan(val[0]) else None
                                             for val in sampled_values]

        # Verify sampling worked
        assert 'raster_value' in sampled_points.columns

        # Points should have values corresponding to their zones
        for idx, row in sampled_points.iterrows():
            if row['expected_zone'] in ['NW', 'NE', 'SW', 'SE'] and pd.notna(row['raster_value']):
                expected_range = {
                    'NW': (80, 120),   # ~100 ± noise
                    'NE': (180, 220),  # ~200 ± noise
                    'SW': (280, 320),  # ~300 ± noise
                    'SE': (380, 420)   # ~400 ± noise
                }

                zone = row['expected_zone']
                if zone in expected_range:
                    min_val, max_val = expected_range[zone]
                    assert min_val <= row['raster_value'] <= max_val

    def test_raster_to_vector_conversion(self, landcover_raster_path, tmp_path):
        """Test converting raster data to vector polygons."""
        output_vector = tmp_path / "landcover_polygons.shp"

        # Convert raster to vector polygons
        with rasterio.open(landcover_raster_path) as src:
            image = src.read(1)
            mask_array = image != src.nodata

            # Extract shapes (polygons) from raster
            results = [
                {'properties': {'landcover': v}, 'geometry': s}
                for i, (s, v) in enumerate(
                    shapes(image, mask=mask_array, transform=src.transform))
            ]

        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame.from_features(results, crs=src.crs)

        # Verify conversion
        assert len(gdf) > 0
        assert 'landcover' in gdf.columns
        assert all(gdf.geometry.is_valid)

        # Should have landcover classes 1-5
        unique_classes = set(gdf['landcover'].unique())
        expected_classes = {1, 2, 3, 4, 5}
        assert unique_classes.issubset(expected_classes)

        # Save and verify file creation
        gdf.to_file(output_vector)
        assert output_vector.exists()

    def test_vector_to_raster_conversion(self, test_polygons_gdf, tmp_path):
        """Test converting vector polygons to raster."""
        output_raster = tmp_path / "polygons_raster.tif"

        # Define raster parameters
        width, height = 500, 400
        bounds = test_polygons_gdf.total_bounds
        transform = from_bounds(*bounds, width, height)

        # Add attribute to rasterize
        test_polygons_gdf['burn_value'] = [1, 2, 3, 4]

        # Convert vector to raster
        with rasterio.open(
            output_raster, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=rasterio.uint8, crs=test_polygons_gdf.crs,
            transform=transform, nodata=0
        ) as dst:
            # Rasterize the polygons
            shapes_with_values = [
                (geom, value) for geom, value in
                zip(test_polygons_gdf.geometry, test_polygons_gdf['burn_value'])
            ]

            burned = rasterize(shapes_with_values, out_shape=(height, width),
                             transform=transform, fill=0, dtype=rasterio.uint8)
            dst.write(burned, 1)

        # Verify raster creation
        assert output_raster.exists()

        with rasterio.open(output_raster) as src:
            data = src.read(1)
            unique_values = np.unique(data)

            # Should have background (0) and polygon values (1-4)
            expected_values = {0, 1, 2, 3, 4}
            assert set(unique_values).issubset(expected_values)

    def test_raster_clipping_by_polygon(self, test_raster_path, test_polygons_gdf, tmp_path):
        """Test clipping raster data by polygon boundaries."""
        # Select one polygon for clipping
        clip_polygon = test_polygons_gdf.iloc[0:1]  # First polygon

        with rasterio.open(test_raster_path) as src:
            # Clip raster by polygon
            out_image, out_transform = mask(src, clip_polygon.geometry, crop=True)
            out_meta = src.meta

            # Update metadata
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            # Write clipped raster
            clipped_path = tmp_path / "clipped_raster.tif"
            with rasterio.open(clipped_path, "w", **out_meta) as dest:
                dest.write(out_image)

        # Verify clipping
        assert clipped_path.exists()

        with rasterio.open(clipped_path) as clipped:
            # Clipped raster should be smaller than original
            with rasterio.open(test_raster_path) as original:
                assert clipped.width <= original.width
                assert clipped.height <= original.height

            # Should contain data within the expected value range
            clipped_data = clipped.read(1, masked=True)
            if clipped_data.count() > 0:
                # Values should be in the expected range for the first polygon
                mean_value = clipped_data.mean()
                assert 80 <= mean_value <= 120  # ~100 ± noise

    def test_buffer_analysis_raster_vector(self, test_raster_path, test_points_gdf, tmp_path):
        """Test creating buffers around points and analyzing raster within buffers."""
        # Create buffers around points
        buffer_distance = 0.1  # degrees
        buffered_points = test_points_gdf.copy()
        buffered_points['geometry'] = test_points_gdf.geometry.buffer(buffer_distance)

        # Analyze raster within buffers
        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            buffered_points,
            statistics=['mean', 'std', 'count']
        )

        # Verify buffer analysis
        assert len(result_gdf) == len(test_points_gdf)

        count_cols = [col for col in result_gdf.columns if 'count' in col]
        if count_cols:
            # All buffers should contain some pixels
            counts = result_gdf[count_cols[0]].dropna()
            assert all(counts > 0)

    def test_raster_vector_intersection_analysis(self, test_raster_path, landcover_raster_path,
                                               test_polygons_gdf, tmp_path):
        """Test complex intersection analysis between multiple rasters and vectors."""
        # Analyze both elevation and landcover within the same polygons
        elevation_stats = extract_raster_statistics_by_zones(
            test_raster_path,
            test_polygons_gdf,
            statistics=['mean', 'std']
        )

        landcover_stats = extract_raster_statistics_by_zones(
            landcover_raster_path,
            test_polygons_gdf,
            statistics=['mode', 'unique_count'],
            categorical_bands=[1]
        )

        # Combine results
        combined = elevation_stats.merge(
            landcover_stats[['zone_id'] + [col for col in landcover_stats.columns if col not in elevation_stats.columns]],
            on='zone_id'
        )

        # Verify combined analysis
        assert len(combined) == len(test_polygons_gdf)

        # Should have both elevation and landcover statistics
        elev_cols = [col for col in combined.columns if 'mean' in col or 'std' in col]
        lc_cols = [col for col in combined.columns if 'mode' in col or 'unique' in col]

        assert len(elev_cols) > 0, "Missing elevation statistics"
        assert len(lc_cols) > 0, "Missing landcover statistics"


class TestRasterVectorPerformance:
    """Performance tests for raster-vector operations."""

    def test_large_polygon_zonal_stats_performance(self, test_raster_path, tmp_path):
        """Test performance with large numbers of polygons."""
        # Create many small polygons
        num_polygons = 100
        polygons = []

        for i in range(num_polygons):
            x = -112 + (i % 10) * 0.02
            y = 33 + (i // 10) * 0.02
            poly = box(x, y, x + 0.01, y + 0.01)
            polygons.append(poly)

        large_gdf = gpd.GeoDataFrame({
            'id': range(num_polygons),
            'geometry': polygons
        }, crs='EPSG:4326')

        # Time the operation
        start_time = time.time()
        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            large_gdf,
            statistics=['mean', 'count']
        )
        processing_time = time.time() - start_time

        # Verify results
        assert len(result_gdf) == num_polygons

        # Should complete in reasonable time
        assert processing_time < 30  # Less than 30 seconds

    def test_memory_usage_large_zonal_analysis(self, test_raster_path, tmp_path):
        """Test memory usage during large zonal analysis."""
        # Create moderate number of larger polygons
        polygons = []
        for i in range(20):
            x = -112 + (i % 5) * 0.2
            y = 33 + (i // 5) * 0.2
            poly = box(x, y, x + 0.15, y + 0.15)
            polygons.append(poly)

        gdf = gpd.GeoDataFrame({
            'id': range(20),
            'geometry': polygons
        }, crs='EPSG:4326')

        # Monitor memory
        initial_memory = monitor_memory_usage()['process_mb']

        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            gdf,
            statistics=['mean', 'std', 'min', 'max', 'count']
        )

        final_memory = monitor_memory_usage()['process_mb']
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable
        assert memory_increase < 200  # Less than 200MB increase
        assert len(result_gdf) == 20


class TestRasterVectorEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_geometries_handling(self, test_raster_path):
        """Test handling of empty geometries."""
        # Create GeoDataFrame with empty geometry
        empty_gdf = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [Polygon()]  # Empty polygon
        }, crs='EPSG:4326')

        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            empty_gdf,
            statistics=['mean', 'count']
        )

        # Should handle gracefully
        assert len(result_gdf) == 1

        # Statistics should be null or zero for empty geometry
        count_cols = [col for col in result_gdf.columns if 'count' in col]
        if count_cols:
            assert result_gdf[count_cols[0]].iloc[0] == 0 or pd.isna(result_gdf[count_cols[0]].iloc[0])

    def test_invalid_geometries_handling(self, test_raster_path):
        """Test handling of invalid geometries."""
        # Create self-intersecting polygon (invalid)
        invalid_coords = [
            (-112, 33), (-111, 33), (-111, 34), (-112, 34),
            (-111.5, 33.5), (-112, 33)  # Creates self-intersection
        ]
        invalid_poly = Polygon(invalid_coords)

        invalid_gdf = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [invalid_poly]
        }, crs='EPSG:4326')

        # Should either fix the geometry or handle the error gracefully
        try:
            result_gdf = extract_raster_statistics_by_zones(
                test_raster_path,
                invalid_gdf,
                statistics=['mean']
            )
            # If successful, should return results
            assert len(result_gdf) == 1
        except Exception as e:
            # Should provide informative error message
            assert 'geometry' in str(e).lower() or 'invalid' in str(e).lower()

    def test_very_small_polygons(self, test_raster_path):
        """Test with very small polygons that might not intersect any pixels."""
        # Create very small polygon
        tiny_poly = box(-111.5, 33.5, -111.4999, 33.5001)  # Very small

        tiny_gdf = gpd.GeoDataFrame({
            'id': [1],
            'geometry': [tiny_poly]
        }, crs='EPSG:4326')

        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            tiny_gdf,
            statistics=['mean', 'count']
        )

        # Should handle gracefully, even if no pixels intersected
        assert len(result_gdf) == 1

    def test_multipolygon_handling(self, test_raster_path):
        """Test handling of MultiPolygon geometries."""
        # Create MultiPolygon
        poly1 = box(-112, 33, -111.8, 33.2)
        poly2 = box(-111.7, 33.3, -111.5, 33.5)
        multipoly = MultiPolygon([poly1, poly2
