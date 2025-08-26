"""
Test suite for memory-efficient processing functionality.

This module contains comprehensive tests for memory-efficient raster processing
operations in the rasterio_analysis.memory_efficient module, including windowed
processing, parallel operations, and memory management strategies.

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
import tempfile
from pathlib import Path
import warnings
from unittest.mock import patch, MagicMock
import psutil
import time
from shapely.geometry import box, Polygon
from concurrent.futures import ThreadPoolExecutor
import gc

# Import the functions we're testing
try:
    from src.rasterio_analysis.memory_efficient import (
        process_raster_windowed,
        calculate_optimal_window_size,
        extract_raster_statistics_by_zones,
        resample_raster_to_resolution,
        process_large_raster_parallel,
        create_raster_overview_pyramid,
        monitor_memory_usage,
        MemoryEfficientProcessor
    )
except ImportError as e:
    pytest.skip(f"Could not import memory efficient functions: {e}", allow_module_level=True)


class TestMemoryEfficientProcessing:
    """Test suite for memory-efficient processing functionality."""

    @pytest.fixture(scope="class")
    def large_raster_path(self, tmp_path_factory):
        """Create a large raster for memory testing."""
        tmp_dir = tmp_path_factory.mktemp("memory_test_data")
        raster_path = tmp_dir / "large_test_raster.tif"

        # Create a reasonably large raster for testing
        width, height = 2048, 1536

        # Generate synthetic elevation data
        np.random.seed(42)  # For reproducible tests
        x = np.linspace(0, 20, width)
        y = np.linspace(0, 15, height)
        X, Y = np.meshgrid(x, y)

        # Create realistic elevation with some patterns
        elevation = (1000 +
                    500 * np.sin(X/5) +
                    300 * np.cos(Y/3) +
                    100 * np.random.random((height, width)))
        elevation = elevation.astype(np.float32)

        # Add some nodata areas
        elevation[:50, :50] = np.nan
        elevation[-50:, -50:] = np.nan

        bounds = (-115.0, 32.0, -110.0, 37.0)  # Arizona/Nevada area
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=elevation.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=np.nan,
            compress='lzw'
        ) as dst:
            dst.write(elevation, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def multiband_large_raster_path(self, tmp_path_factory):
        """Create a large multiband raster for testing."""
        tmp_dir = tmp_path_factory.mktemp("multiband_memory_data")
        raster_path = tmp_dir / "large_multiband.tif"

        width, height = 1024, 768
        bands = 4

        # Generate Landsat-like data
        np.random.seed(42)
        blue = np.random.randint(800, 1200, (height, width)).astype(np.uint16)
        green = np.random.randint(900, 1400, (height, width)).astype(np.uint16)
        red = np.random.randint(1000, 1600, (height, width)).astype(np.uint16)
        nir = np.random.randint(2000, 4000, (height, width)).astype(np.uint16)

        imagery = np.stack([blue, green, red, nir])

        bounds = (-112.0, 33.0, -111.0, 34.0)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=imagery.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=0
        ) as dst:
            for i in range(bands):
                dst.write(imagery[i], i + 1)

        return raster_path

    @pytest.fixture(scope="class")
    def test_polygons_gdf(self):
        """Create test polygons for zonal statistics."""
        # Create several test polygons
        polygons = [
            box(-112.0, 33.0, -111.5, 33.5),  # Southwest quad
            box(-111.5, 33.0, -111.0, 33.5),  # Southeast quad
            box(-112.0, 33.5, -111.5, 34.0),  # Northwest quad
            box(-111.5, 33.5, -111.0, 34.0),  # Northeast quad
        ]

        gdf = gpd.GeoDataFrame({
            'zone_id': ['SW', 'SE', 'NW', 'NE'],
            'zone_name': ['Southwest', 'Southeast', 'Northwest', 'Northeast'],
            'geometry': polygons
        }, crs='EPSG:4326')

        return gdf

    def test_calculate_optimal_window_size_basic(self, large_raster_path):
        """Test optimal window size calculation."""
        window_size, analysis_info = calculate_optimal_window_size(
            large_raster_path,
            max_memory_mb=512,
            safety_factor=0.8
        )

        # Check that we get a valid window size
        assert isinstance(window_size, int)
        assert window_size > 0
        assert window_size <= 2048  # Should not exceed raster dimensions

        # Check analysis info structure
        required_keys = [
            'raster_info', 'memory_calculations', 'recommended_window_size',
            'memory_per_window_mb', 'estimated_windows_needed'
        ]
        for key in required_keys:
            assert key in analysis_info, f"Missing required key: {key}"

        # Check memory calculations
        mem_calc = analysis_info['memory_calculations']
        assert 'bytes_per_pixel' in mem_calc
        assert 'total_pixels' in mem_calc
        assert 'available_memory_mb' in mem_calc

    def test_calculate_optimal_window_size_small_memory(self, large_raster_path):
        """Test window size calculation with small memory constraint."""
        window_size, analysis_info = calculate_optimal_window_size(
            large_raster_path,
            max_memory_mb=64,  # Very small memory limit
            safety_factor=0.9
        )

        # Should still provide a valid window size, likely smaller
        assert window_size > 0
        assert analysis_info['memory_per_window_mb'] <= 64 * 0.9

    def test_calculate_optimal_window_size_invalid_file(self):
        """Test window size calculation with invalid file."""
        with pytest.raises(FileNotFoundError):
            calculate_optimal_window_size("nonexistent.tif")

    def test_process_raster_windowed_basic(self, large_raster_path, tmp_path):
        """Test basic windowed raster processing."""
        output_path = tmp_path / "windowed_output.tif"

        # Define a simple processing function (add 100 to all values)
        def add_offset(data, offset=100):
            result = data.copy()
            valid_mask = ~np.isnan(result)
            result[valid_mask] += offset
            return result

        result = process_raster_windowed(
            large_raster_path,
            output_path,
            add_offset,
            window_size=512,
            overlap=0,
            offset=100
        )

        # Check output file was created
        assert output_path.exists()

        # Check result structure
        required_keys = [
            'processing_summary', 'windows_processed', 'total_processing_time',
            'memory_usage', 'performance_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check processing summary
        summary = result['processing_summary']
        assert summary['windows_processed'] > 0
        assert summary['successful_windows'] > 0

        # Verify output raster properties
        with rasterio.open(output_path) as src:
            with rasterio.open(large_raster_path) as orig:
                # Should have same dimensions and metadata
                assert src.width == orig.width
                assert src.height == orig.height
                assert src.count == orig.count
                assert src.crs == orig.crs

                # Check that processing was applied
                orig_data = orig.read(1, masked=True)
                processed_data = src.read(1, masked=True)

                # Where data is valid, processed should be original + 100
                valid_orig = ~orig_data.mask
                if np.any(valid_orig):
                    np.testing.assert_array_almost_equal(
                        processed_data.data[valid_orig],
                        orig_data.data[valid_orig] + 100,
                        decimal=2
                    )

    def test_process_raster_windowed_with_overlap(self, large_raster_path, tmp_path):
        """Test windowed processing with overlap."""
        output_path = tmp_path / "windowed_overlap_output.tif"

        def smooth_filter(data):
            from scipy.ndimage import gaussian_filter
            return gaussian_filter(data, sigma=1.0, mode='reflect')

        # Skip if scipy not available
        try:
            import scipy.ndimage
        except ImportError:
            pytest.skip("scipy not available for filtering test")

        result = process_raster_windowed(
            large_raster_path,
            output_path,
            smooth_filter,
            window_size=256,
            overlap=32  # 32 pixel overlap
        )

        assert output_path.exists()
        assert result['processing_summary']['overlap_pixels'] == 32

    def test_process_raster_windowed_invalid_function(self, large_raster_path, tmp_path):
        """Test windowed processing with invalid processing function."""
        output_path = tmp_path / "invalid_output.tif"

        # Invalid function that will cause errors
        def broken_function(data):
            raise ValueError("This function is broken")

        with pytest.raises(ValueError):
            process_raster_windowed(
                large_raster_path,
                output_path,
                broken_function,
                window_size=256
            )

    def test_extract_raster_statistics_by_zones(self, multiband_large_raster_path, test_polygons_gdf):
        """Test zonal statistics extraction."""
        result_gdf = extract_raster_statistics_by_zones(
            multiband_large_raster_path,
            test_polygons_gdf,
            statistics=['mean', 'std', 'min', 'max', 'count']
        )

        # Check that result is a GeoDataFrame
        assert isinstance(result_gdf, gpd.GeoDataFrame)

        # Should have same number of rows as input
        assert len(result_gdf) == len(test_polygons_gdf)

        # Should have original columns plus statistics columns
        original_cols = set(test_polygons_gdf.columns)
        result_cols = set(result_gdf.columns)
        assert original_cols.issubset(result_cols)

        # Check for statistics columns (for each band)
        expected_stats_patterns = ['_mean', '_std', '_min', '_max', '_count']
        for pattern in expected_stats_patterns:
            matching_cols = [col for col in result_cols if col.endswith(pattern)]
            assert len(matching_cols) > 0, f"No columns found with pattern {pattern}"

        # Check that statistics are reasonable
        for idx, row in result_gdf.iterrows():
            for col in result_cols:
                if col.endswith('_mean') and pd.notna(row[col]):
                    # Mean should be reasonable for uint16 Landsat-like data
                    assert 0 <= row[col] <= 65535

    def test_extract_raster_statistics_by_zones_categorical(self, tmp_path, test_polygons_gdf):
        """Test zonal statistics with categorical data."""
        # Create categorical raster (land cover classes)
        categorical_path = tmp_path / "landcover.tif"
        width, height = 500, 400

        # Create land cover data (classes 1-5)
        np.random.seed(42)
        landcover = np.random.randint(1, 6, (height, width), dtype=np.uint8)

        bounds = (-112.0, 33.0, -111.0, 34.0)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            categorical_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=landcover.dtype, crs='EPSG:4326',
            transform=transform, nodata=0
        ) as dst:
            dst.write(landcover, 1)

        result_gdf = extract_raster_statistics_by_zones(
            categorical_path,
            test_polygons_gdf,
            statistics=['mode', 'count', 'unique'],
            categorical_bands=[1]
        )

        # Should include mode and unique value counts
        assert any('_mode' in col for col in result_gdf.columns)
        assert any('_unique' in col for col in result_gdf.columns)

    def test_resample_raster_to_resolution(self, large_raster_path, tmp_path):
        """Test raster resampling to new resolution."""
        output_path = tmp_path / "resampled.tif"

        # Get original resolution
        with rasterio.open(large_raster_path) as src:
            orig_transform = src.transform
            orig_resolution = abs(orig_transform[0])  # Assuming square pixels

        # Resample to half resolution (double the pixel size)
        target_resolution = orig_resolution * 2

        result = resample_raster_to_resolution(
            large_raster_path,
            output_path,
            target_resolution,
            resampling_method='bilinear',
            chunk_size=1024
        )

        # Check output file exists
        assert output_path.exists()

        # Check result structure
        required_keys = [
            'resampling_info', 'original_dimensions', 'new_dimensions',
            'resolution_change', 'processing_time'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Verify new resolution
        with rasterio.open(output_path) as src:
            new_transform = src.transform
            new_resolution = abs(new_transform[0])
            assert abs(new_resolution - target_resolution) < 1e-6

            # New dimensions should be roughly half
            assert src.width < result['original_dimensions'][0]
            assert src.height < result['original_dimensions'][1]

    def test_resample_raster_invalid_method(self, large_raster_path, tmp_path):
        """Test resampling with invalid method."""
        output_path = tmp_path / "invalid_resample.tif"

        with pytest.raises(ValueError, match="Invalid resampling method"):
            resample_raster_to_resolution(
                large_raster_path,
                output_path,
                100.0,
                resampling_method='invalid_method'
            )

    def test_process_large_raster_parallel(self, tmp_path):
        """Test parallel processing of multiple rasters."""
        # Create multiple test rasters
        raster_paths = []
        for i in range(3):
            raster_path = tmp_path / f"test_raster_{i}.tif"
            data = np.random.randint(0, 1000, (200, 200), dtype=np.uint16)

            with rasterio.open(
                raster_path, 'w',
                driver='GTiff', height=200, width=200, count=1,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, 200, 200)
            ) as dst:
                dst.write(data, 1)

            raster_paths.append(raster_path)

        output_dir = tmp_path / "parallel_output"
        output_dir.mkdir()

        # Define a simple processing function
        def apply_threshold(input_path, output_path, threshold=500):
            with rasterio.open(input_path) as src:
                data = src.read(1)
                profile = src.profile

            # Apply threshold
            result = np.where(data > threshold, data, 0)

            with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(result, 1)

        result = process_large_raster_parallel(
            raster_paths,
            output_dir,
            apply_threshold,
            max_workers=2,
            threshold=500
        )

        # Check result structure
        required_keys = [
            'processing_summary', 'successful_files', 'failed_files',
            'total_processing_time', 'performance_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check processing results
        summary = result['processing_summary']
        assert summary['total_files'] == 3
        assert summary['successful_count'] >= 0
        assert summary['failed_count'] >= 0

        # Check output files exist for successful processing
        for success_info in result['successful_files']:
            output_path = Path(success_info['output_path'])
            assert output_path.exists()

    def test_create_raster_overview_pyramid(self, large_raster_path):
        """Test creation of raster overview pyramids."""
        # Create a copy to modify (since overviews modify the file)
        test_raster = Path(large_raster_path).parent / "test_with_overviews.tif"

        # Copy the raster
        import shutil
        shutil.copy2(large_raster_path, test_raster)

        result = create_raster_overview_pyramid(
            test_raster,
            overview_factors=[2, 4, 8],
            resampling_method='average'
        )

        # Check result structure
        required_keys = [
            'overview_info', 'factors_created', 'file_size_change',
            'creation_time', 'overview_sizes'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Verify overviews were created
        with rasterio.open(test_raster) as src:
            overviews = src.overviews(1)
            assert len(overviews) > 0
            assert overviews == [2, 4, 8]

        # Clean up
        test_raster.unlink()

    def test_create_raster_overview_pyramid_readonly_file(self, large_raster_path):
        """Test overview creation with read-only file."""
        # Make file read-only
        large_raster_path.chmod(0o444)

        try:
            with pytest.raises(PermissionError):
                create_raster_overview_pyramid(large_raster_path)
        finally:
            # Restore write permissions for cleanup
            large_raster_path.chmod(0o644)

    def test_monitor_memory_usage(self):
        """Test memory usage monitoring."""
        memory_info = monitor_memory_usage()

        # Check result structure
        required_keys = [
            'total_mb', 'available_mb', 'used_mb', 'process_mb', 'usage_percent'
        ]
        for key in required_keys:
            assert key in memory_info, f"Missing required key: {key}"

        # Check reasonable values
        assert memory_info['total_mb'] > 0
        assert memory_info['available_mb'] >= 0
        assert memory_info['used_mb'] >= 0
        assert memory_info['process_mb'] >= 0
        assert 0 <= memory_info['usage_percent'] <= 100

        # Basic sanity checks
        assert memory_info['used_mb'] <= memory_info['total_mb']
        assert memory_info['available_mb'] <= memory_info['total_mb']


class TestMemoryEfficientProcessor:
    """Test the MemoryEfficientProcessor class."""

    def test_processor_initialization(self):
        """Test processor initialization."""
        # Default initialization
        processor = MemoryEfficientProcessor()
        assert processor.max_memory_mb == 2048
        assert processor.safety_factor == 0.8
        assert len(processor.processing_history) == 0

        # Custom initialization
        custom_processor = MemoryEfficientProcessor(
            max_memory_mb=1024,
            safety_factor=0.9
        )
        assert custom_processor.max_memory_mb == 1024
        assert custom_processor.safety_factor == 0.9

    def test_processor_context_manager(self):
        """Test processor as context manager."""
        with MemoryEfficientProcessor(max_memory_mb=1024) as processor:
            assert processor is not None
            assert processor.max_memory_mb == 1024

    def test_processor_workflow_basic(self, large_raster_path, tmp_path):
        """Test basic workflow processing."""
        processor = MemoryEfficientProcessor(max_memory_mb=1024)

        # Define simple workflow steps
        workflow_steps = [
            {
                'function': 'add_constant',
                'parameters': {'constant': 50}
            },
            {
                'function': 'apply_threshold',
                'parameters': {'threshold': 1200}
            }
        ]

        output_dir = tmp_path / "workflow_output"
        output_dir.mkdir()

        result = processor.process_workflow(
            [large_raster_path],
            output_dir,
            workflow_steps
        )

        # Check result structure
        required_keys = [
            'workflow_summary', 'step_results', 'total_processing_time',
            'memory_monitoring', 'output_files'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

    def test_processor_get_statistics(self):
        """Test processing statistics tracking."""
        processor = MemoryEfficientProcessor()

        # Initially should have no statistics
        stats = processor.get_processing_statistics()
        assert isinstance(stats, pd.DataFrame)
        assert len(stats) == 0

        # After some operations, should have statistics
        # (This would be populated by actual processing operations)


class TestMemoryEfficientEdgeCases:
    """Test edge cases and error conditions."""

    def test_windowed_processing_tiny_windows(self, large_raster_path, tmp_path):
        """Test windowed processing with very small windows."""
        output_path = tmp_path / "tiny_windows.tif"

        def identity_function(data):
            return data

        # Very small window size
        result = process_raster_windowed(
            large_raster_path,
            output_path,
            identity_function,
            window_size=32  # Very small
        )

        assert output_path.exists()
        assert result['processing_summary']['windows_processed'] > 100  # Many small windows

    def test_zonal_stats_no_overlap(self, large_raster_path):
        """Test zonal statistics with polygons that don't overlap raster."""
        # Create polygons outside raster bounds
        non_overlapping_polygons = [
            box(-180, -90, -170, -80),  # Far from test raster
            box(170, 80, 180, 90)      # Also far away
        ]

        gdf = gpd.GeoDataFrame({
            'id': [1, 2],
            'geometry': non_overlapping_polygons
        }, crs='EPSG:4326')

        result_gdf = extract_raster_statistics_by_zones(
            large_raster_path,
            gdf,
            statistics=['mean', 'count']
        )

        # Should return GeoDataFrame with null/zero statistics
        assert len(result_gdf) == 2

        # Count should be zero or null for non-overlapping areas
        count_cols = [col for col in result_gdf.columns if '_count' in col]
        for col in count_cols:
            assert all(result_gdf[col].fillna(0) == 0)

    def test_parallel_processing_with_failures(self, tmp_path):
        """Test parallel processing with some failing operations."""
        # Create mix of valid and invalid input files
        input_paths = []

        # Valid raster
        valid_path = tmp_path / "valid.tif"
        data = np.random.randint(0, 100, (50, 50), dtype=np.uint8)
        with rasterio.open(
            valid_path, 'w',
            driver='GTiff', height=50, width=50, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 50, 50)
        ) as dst:
            dst.write(data, 1)
        input_paths.append(valid_path)

        # Invalid file (not a raster)
        invalid_path = tmp_path / "invalid.txt"
        invalid_path.write_text("This is not a raster")
        input_paths.append(invalid_path)

        # Non-existent file
        input_paths.append(tmp_path / "nonexistent.tif")

        output_dir = tmp_path / "mixed_output"
        output_dir.mkdir()

        def simple_copy(input_path, output_path):
            # This will fail for non-raster files
            with rasterio.open(input_path) as src:
                profile = src.profile
                data = src.read()

            with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(data)

        result = process_large_raster_parallel(
            input_paths,
            output_dir,
            simple_copy,
            max_workers=2
        )

        # Should handle mix of successes and failures
        summary = result['processing_summary']
        assert summary['successful_count'] == 1  # Only valid raster should succeed
        assert summary['failed_count'] == 2     # Two failures expected
        assert len(result['failed_files']) == 2

    def test_memory_monitoring_under_load(self):
        """Test memory monitoring during heavy operations."""
        # Create some memory load
        initial_memory = monitor_memory_usage()

        # Allocate some memory
        large_arrays = []
        for i in range(5):
            arr = np.random.random((1000, 1000))  # ~8MB each
            large_arrays.append(arr)

        loaded_memory = monitor_memory_usage()

        # Should show increased memory usage
        assert loaded_memory['process_mb'] >= initial_memory['process_mb']

        # Clean up
        del large_arrays
        gc.collect()

        final_memory = monitor_memory_usage()
        # Memory should be released (though may not be immediate due to GC)
        assert final_memory is not None

    def test_resampling_extreme_resolution_change(self, tmp_path):
        """Test resampling with extreme resolution changes."""
        # Create small test raster
        small_raster = tmp_path / "small_test.tif"
        data = np.random.randint(0, 100, (100, 100), dtype=np.uint8)

        with rasterio.open(
            small_raster, 'w',
            driver='GTiff', height=100, width=100, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 100, 100)  # 0.02 degree resolution
        ) as dst:
            dst.write(data, 1)

        # Extreme upsampling (much finer resolution)
        upsampled_path = tmp_path / "upsampled.tif"
        result_up = resample_raster_to_resolution(
            small_raster,
            upsampled_path,
            target_resolution=0.001,  # Much finer
            resampling_method='bilinear'
        )

        assert upsampled_path.exists()
        assert result_up['new_dimensions'][0] > result_up['original_dimensions'][0]

        # Extreme downsampling (much coarser resolution)
        downsampled_path = tmp_path / "downsampled.tif"
        result_down = resample_raster_to_resolution(
            small_raster,
            downsampled_path,
            target_resolution=0.1,  # Much coarser
            resampling_method='average'
        )

        assert downsampled_path.exists()
        assert result_down['new_dimensions'][0] < result_down['original_dimensions'][0]
