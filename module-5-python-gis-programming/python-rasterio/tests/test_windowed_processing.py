"""
Test suite for windowed processing functionality.

This module contains comprehensive tests for windowed raster processing
operations, including memory-efficient algorithms, parallel processing,
and performance optimization techniques.

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
    pytest.skip(f"Could not import windowed processing functions: {e}", allow_module_level=True)


class TestWindowedProcessing:
    """Test suite for windowed raster processing."""

    @pytest.fixture(scope="class")
    def test_raster_path(self, tmp_path_factory):
        """Create a test raster for windowed processing."""
        tmp_dir = tmp_path_factory.mktemp("windowed_test_data")
        raster_path = tmp_dir / "test_windowed.tif"

        # Create test raster with known pattern
        width, height = 1024, 768

        # Create checkerboard pattern for easy verification
        data = np.zeros((height, width), dtype=np.float32)

        # Create checkerboard pattern
        tile_size = 128
        for i in range(0, height, tile_size):
            for j in range(0, width, tile_size):
                if ((i // tile_size) + (j // tile_size)) % 2 == 0:
                    data[i:i+tile_size, j:j+tile_size] = 100.0
                else:
                    data[i:i+tile_size, j:j+tile_size] = 200.0

        bounds = (-112.0, 33.0, -111.0, 34.0)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(data, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def large_test_raster_path(self, tmp_path_factory):
        """Create a larger test raster for memory testing."""
        tmp_dir = tmp_path_factory.mktemp("large_windowed_data")
        raster_path = tmp_dir / "large_windowed.tif"

        width, height = 2048, 1536

        # Create gradient pattern
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 8, height)
        X, Y = np.meshgrid(x, y)
        data = (X + Y * 2).astype(np.float32)

        bounds = (-115.0, 32.0, -110.0, 37.0)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=transform,
            compress='lzw'
        ) as dst:
            dst.write(data, 1)

        return raster_path

    def test_windowed_processing_basic_function(self, test_raster_path, tmp_path):
        """Test basic windowed processing functionality."""
        output_path = tmp_path / "windowed_result.tif"

        def add_value(data, value=50):
            """Simple function to add a value to all pixels."""
            return data + value

        result = process_raster_windowed(
            test_raster_path,
            output_path,
            add_value,
            window_size=256,
            overlap=0,
            value=50
        )

        # Check output file exists
        assert output_path.exists()

        # Check result structure
        required_keys = [
            'processing_summary', 'windows_processed', 'total_processing_time',
            'memory_usage', 'performance_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Verify processing worked correctly
        with rasterio.open(output_path) as processed:
            with rasterio.open(test_raster_path) as original:
                orig_data = original.read(1)
                proc_data = processed.read(1)

                # Should have same dimensions
                assert orig_data.shape == proc_data.shape

                # Processed data should be original + 50
                np.testing.assert_array_almost_equal(
                    proc_data, orig_data + 50, decimal=2
                )

    def test_windowed_processing_with_overlap(self, test_raster_path, tmp_path):
        """Test windowed processing with overlap to handle edge effects."""
        output_path = tmp_path / "windowed_overlap.tif"

        def smooth_function(data, sigma=1.0):
            """Apply Gaussian smoothing (requires overlap to work properly)."""
            try:
                from scipy.ndimage import gaussian_filter
                return gaussian_filter(data, sigma=sigma, mode='reflect')
            except ImportError:
                # Fallback if scipy not available
                return data

        result = process_raster_windowed(
            test_raster_path,
            output_path,
            smooth_function,
            window_size=512,
            overlap=64,
            sigma=2.0
        )

        assert output_path.exists()
        assert result['processing_summary']['overlap_pixels'] == 64

        # Should have processed multiple windows
        assert result['processing_summary']['windows_processed'] >= 4

    def test_windowed_processing_edge_cases(self, test_raster_path, tmp_path):
        """Test windowed processing edge cases."""
        output_path = tmp_path / "windowed_edge_cases.tif"

        # Test with window size larger than raster
        def identity_function(data):
            return data

        result = process_raster_windowed(
            test_raster_path,
            output_path,
            identity_function,
            window_size=5000  # Larger than 1024x768 raster
        )

        assert output_path.exists()
        # Should still work, just with fewer (maybe 1) window
        assert result['processing_summary']['windows_processed'] >= 1

    def test_windowed_processing_error_handling(self, test_raster_path, tmp_path):
        """Test error handling in windowed processing."""
        output_path = tmp_path / "windowed_error.tif"

        def failing_function(data):
            raise ValueError("Intentional test failure")

        with pytest.raises(ValueError, match="Intentional test failure"):
            process_raster_windowed(
                test_raster_path,
                output_path,
                failing_function,
                window_size=256
            )

    def test_calculate_optimal_window_size_basic(self, test_raster_path):
        """Test optimal window size calculation."""
        window_size, analysis = calculate_optimal_window_size(
            test_raster_path,
            max_memory_mb=256,
            safety_factor=0.8
        )

        assert isinstance(window_size, int)
        assert window_size > 0
        assert window_size <= 1024  # Should not exceed raster width

        # Check analysis structure
        required_keys = [
            'raster_info', 'memory_calculations', 'recommended_window_size',
            'memory_per_window_mb', 'estimated_windows_needed'
        ]
        for key in required_keys:
            assert key in analysis, f"Missing analysis key: {key}"

        # Check memory calculations are reasonable
        assert analysis['memory_per_window_mb'] <= 256 * 0.8

    def test_calculate_optimal_window_size_constraints(self, large_test_raster_path):
        """Test window size calculation with different memory constraints."""
        # Test with very limited memory
        small_window, small_analysis = calculate_optimal_window_size(
            large_test_raster_path,
            max_memory_mb=32,
            safety_factor=0.9
        )

        # Test with generous memory
        large_window, large_analysis = calculate_optimal_window_size(
            large_test_raster_path,
            max_memory_mb=1024,
            safety_factor=0.7
        )

        # Small memory should result in smaller window
        assert small_window <= large_window
        assert small_analysis['memory_per_window_mb'] <= large_analysis['memory_per_window_mb']

    def test_extract_raster_statistics_by_zones_basic(self, test_raster_path):
        """Test basic zonal statistics extraction."""
        # Create test zones
        zones = [
            box(-112.0, 33.0, -111.5, 33.5),  # Southwest
            box(-111.5, 33.0, -111.0, 33.5),  # Southeast
            box(-112.0, 33.5, -111.5, 34.0),  # Northwest
            box(-111.5, 33.5, -111.0, 34.0)   # Northeast
        ]

        zones_gdf = gpd.GeoDataFrame({
            'zone_id': ['SW', 'SE', 'NW', 'NE'],
            'geometry': zones
        }, crs='EPSG:4326')

        result_gdf = extract_raster_statistics_by_zones(
            test_raster_path,
            zones_gdf,
            statistics=['mean', 'std', 'min', 'max', 'count']
        )

        # Check structure
        assert isinstance(result_gdf, gpd.GeoDataFrame)
        assert len(result_gdf) == len(zones_gdf)

        # Should have original columns plus statistics
        original_cols = set(zones_gdf.columns)
        result_cols = set(result_gdf.columns)
        assert original_cols.issubset(result_cols)

        # Check for statistics columns
        stats_cols = [col for col in result_cols if any(stat in col for stat in ['mean', 'std', 'min', 'max', 'count'])]
        assert len(stats_cols) > 0

    def test_resample_raster_to_resolution_basic(self, test_raster_path, tmp_path):
        """Test basic raster resampling."""
        output_path = tmp_path / "resampled.tif"

        # Get original resolution
        with rasterio.open(test_raster_path) as src:
            original_res = abs(src.transform[0])

        # Resample to coarser resolution
        target_res = original_res * 2

        result = resample_raster_to_resolution(
            test_raster_path,
            output_path,
            target_res,
            resampling_method='bilinear'
        )

        assert output_path.exists()

        # Check result structure
        required_keys = [
            'resampling_info', 'original_dimensions', 'new_dimensions',
            'resolution_change', 'processing_time'
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

        # Verify resolution change
        with rasterio.open(output_path) as resampled:
            new_res = abs(resampled.transform[0])
            assert abs(new_res - target_res) < 1e-10

    def test_resample_different_methods(self, test_raster_path, tmp_path):
        """Test different resampling methods."""
        methods = ['nearest', 'bilinear', 'average']

        with rasterio.open(test_raster_path) as src:
            original_res = abs(src.transform[0])
            target_res = original_res * 1.5

        for method in methods:
            output_path = tmp_path / f"resampled_{method}.tif"

            result = resample_raster_to_resolution(
                test_raster_path,
                output_path,
                target_res,
                resampling_method=method
            )

            assert output_path.exists()
            assert result['resampling_info']['method'] == method

    def test_parallel_raster_processing_basic(self, tmp_path):
        """Test parallel processing of multiple rasters."""
        # Create multiple test rasters
        input_paths = []
        for i in range(3):
            raster_path = tmp_path / f"input_{i}.tif"
            data = np.random.randint(0, 100, (200, 200), dtype=np.uint8) + i * 10

            with rasterio.open(
                raster_path, 'w',
                driver='GTiff', height=200, width=200, count=1,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, 200, 200)
            ) as dst:
                dst.write(data, 1)

            input_paths.append(raster_path)

        output_dir = tmp_path / "parallel_output"
        output_dir.mkdir()

        def multiply_by_factor(input_path, output_path, factor=2):
            """Simple processing function."""
            with rasterio.open(input_path) as src:
                data = src.read()
                profile = src.profile

            result = data * factor

            with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(result)

        result = process_large_raster_parallel(
            input_paths,
            output_dir,
            multiply_by_factor,
            max_workers=2,
            factor=3
        )

        # Check result structure
        required_keys = [
            'processing_summary', 'successful_files', 'failed_files',
            'total_processing_time', 'performance_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

        # Should have processed all files successfully
        assert result['processing_summary']['successful_count'] == 3
        assert result['processing_summary']['failed_count'] == 0

    def test_create_raster_overview_pyramid_basic(self, test_raster_path):
        """Test overview pyramid creation."""
        # Create a copy to modify
        test_copy = test_raster_path.parent / "test_with_overviews.tif"

        # Copy the raster
        import shutil
        shutil.copy2(test_raster_path, test_copy)

        result = create_raster_overview_pyramid(
            test_copy,
            overview_factors=[2, 4, 8],
            resampling_method='average'
        )

        # Check result structure
        required_keys = [
            'overview_info', 'factors_created', 'file_size_change',
            'creation_time', 'overview_sizes'
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

        # Verify overviews were created
        with rasterio.open(test_copy) as src:
            overviews = src.overviews(1)
            assert len(overviews) > 0
            assert set(overviews).issubset({2, 4, 8})

        # Clean up
        test_copy.unlink()

    def test_monitor_memory_usage_basic(self):
        """Test memory usage monitoring."""
        memory_info = monitor_memory_usage()

        required_keys = ['total_mb', 'available_mb', 'used_mb', 'process_mb', 'usage_percent']
        for key in required_keys:
            assert key in memory_info, f"Missing key: {key}"

        # Check reasonable values
        assert memory_info['total_mb'] > 0
        assert memory_info['available_mb'] >= 0
        assert memory_info['used_mb'] >= 0
        assert memory_info['process_mb'] >= 0
        assert 0 <= memory_info['usage_percent'] <= 100

    def test_memory_efficient_processor_basic(self, test_raster_path, tmp_path):
        """Test MemoryEfficientProcessor class."""
        processor = MemoryEfficientProcessor(max_memory_mb=512)

        # Test workflow processing
        workflow_steps = [
            {
                'function': 'add_constant',
                'parameters': {'constant': 25}
            }
        ]

        output_dir = tmp_path / "processor_output"
        output_dir.mkdir()

        result = processor.process_workflow(
            [test_raster_path],
            output_dir,
            workflow_steps
        )

        required_keys = [
            'workflow_summary', 'step_results', 'total_processing_time',
            'memory_monitoring', 'output_files'
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_processor_statistics_tracking(self):
        """Test processing statistics tracking."""
        processor = MemoryEfficientProcessor()

        stats = processor.get_processing_statistics()
        assert isinstance(stats, pd.DataFrame)


class TestWindowedProcessingEdgeCases:
    """Test edge cases and error conditions."""

    def test_windowed_processing_invalid_inputs(self, tmp_path):
        """Test windowed processing with invalid inputs."""
        output_path = tmp_path / "invalid_test.tif"

        def dummy_function(data):
            return data

        # Non-existent input file
        with pytest.raises(FileNotFoundError):
            process_raster_windowed(
                "nonexistent.tif",
                output_path,
                dummy_function
            )

        # Invalid window size
        test_raster = tmp_path / "small_test.tif"
        data = np.ones((10, 10), dtype=np.uint8)

        with rasterio.open(
            test_raster, 'w',
            driver='GTiff', height=10, width=10, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 10, 10)
        ) as dst:
            dst.write(data, 1)

        with pytest.raises(ValueError):
            process_raster_windowed(
                test_raster,
                output_path,
                dummy_function,
                window_size=0
            )

    def test_memory_constraints_edge_cases(self, tmp_path):
        """Test memory constraint edge cases."""
        # Create tiny raster
        tiny_raster = tmp_path / "tiny.tif"
        data = np.ones((5, 5), dtype=np.uint8)

        with rasterio.open(
            tiny_raster, 'w',
            driver='GTiff', height=5, width=5, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 5, 5)
        ) as dst:
            dst.write(data, 1)

        # Very restrictive memory limit
        with pytest.raises(ValueError):
            calculate_optimal_window_size(
                tiny_raster,
                max_memory_mb=0.001  # Impossibly small
            )

    def test_parallel_processing_with_errors(self, tmp_path):
        """Test parallel processing when some operations fail."""
        # Create mix of valid and invalid inputs
        input_paths = []

        # Valid raster
        valid_raster = tmp_path / "valid.tif"
        data = np.ones((50, 50), dtype=np.uint8)
        with rasterio.open(
            valid_raster, 'w',
            driver='GTiff', height=50, width=50, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 50, 50)
        ) as dst:
            dst.write(data, 1)
        input_paths.append(valid_raster)

        # Invalid file
        invalid_file = tmp_path / "invalid.txt"
        invalid_file.write_text("Not a raster")
        input_paths.append(invalid_file)

        output_dir = tmp_path / "mixed_output"
        output_dir.mkdir()

        def simple_process(input_path, output_path):
            # This will fail for non-raster files
            with rasterio.open(input_path) as src:
                data = src.read()
                profile = src.profile

            with rasterio.open(output_path, 'w', **profile) as dst:
                dst.write(data)

        result = process_large_raster_parallel(
            input_paths,
            output_dir,
            simple_process,
            max_workers=2
        )

        # Should handle mix of success and failure
        assert result['processing_summary']['successful_count'] == 1
        assert result['processing_summary']['failed_count'] == 1

    def test_overview_creation_edge_cases(self, tmp_path):
        """Test overview creation edge cases."""
        # Create very small raster
        small_raster = tmp_path / "small_overview_test.tif"
        data = np.ones((16, 16), dtype=np.uint8)

        with rasterio.open(
            small_raster, 'w',
            driver='GTiff', height=16, width=16, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 16, 16)
        ) as dst:
            dst.write(data, 1)

        # Try to create overviews larger than the image
        result = create_raster_overview_pyramid(
            small_raster,
            overview_factors=[2, 4, 16, 32],  # 32 would be larger than 16x16
            resampling_method='average'
        )

        # Should handle gracefully
        assert result['overview_info']['completed'] == True

        # Verify reasonable overviews were created
        with rasterio.open(small_raster) as src:
            overviews = src.overviews(1)
            # Should not create overviews that would result in <1 pixel
            for factor in overviews:
                assert 16 // factor >= 1


class TestWindowedProcessingPerformance:
    """Performance-focused tests for windowed processing."""

    def test_windowed_vs_full_memory_usage(self, tmp_path):
        """Compare memory usage: windowed vs full raster loading."""
        # Create moderately large raster
        large_raster = tmp_path / "memory_test.tif"
        width, height = 2048, 1536
        data = np.random.randint(0, 255, (height, width), dtype=np.uint8)

        with rasterio.open(
            large_raster, 'w',
            driver='GTiff', height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-115, 32, -110, 37, width, height)
        ) as dst:
            dst.write(data, 1)

        output_path = tmp_path / "windowed_memory_test.tif"

        def identity_process(arr):
            return arr

        # Monitor memory during windowed processing
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

        result = process_raster_windowed(
            large_raster,
            output_path,
            identity_process,
            window_size=512
        )

        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        windowed_memory_increase = peak_memory - initial_memory

        # Memory increase should be reasonable for windowed processing
        assert windowed_memory_increase < 100  # Less than 100MB increase
        assert result['processing_summary']['windows_processed'] > 4

    def test_optimal_window_size_performance(self, tmp_path):
        """Test that optimal window size calculation is fast."""
        # Create test raster
        test_raster = tmp_path / "performance_test.tif"
        data = np.random.randint(0, 100, (1024, 1024), dtype=np.uint8)

        with rasterio.open(
            test_raster, 'w',
            driver='GTiff', height=1024, width=1024, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 1024, 1024)
        ) as dst:
            dst.write(data, 1)

        # Time the calculation
        start_time = time.time()
        window_size, analysis = calculate_optimal_window_size(test_raster)
        calculation_time = time.time() - start_time

        # Should complete quickly
        assert calculation_time < 1.0  # Less than 1 second
        assert window_size > 0
