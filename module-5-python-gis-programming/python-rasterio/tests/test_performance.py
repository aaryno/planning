"""
Performance test suite for rasterio processing functionality.

This module contains performance benchmarks and timing tests for raster processing
operations, including memory usage monitoring, processing speed comparisons,
and scalability testing.

Author: Student Test Suite
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import pytest
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling
import tempfile
from pathlib import Path
import warnings
import time
import psutil
import gc
from unittest.mock import patch
import threading

# Import the functions we're testing
try:
    from src.rasterio_analysis.raster_processing import (
        analyze_local_raster,
        process_multiband_imagery,
        create_optimized_cog,
        get_raster_summary
    )
    from src.rasterio_analysis.cog_operations import (
        validate_cog_structure,
        optimize_for_cog,
        read_cog_efficiently
    )
    from src.rasterio_analysis.memory_efficient import (
        process_raster_windowed,
        calculate_optimal_window_size,
        monitor_memory_usage
    )
except ImportError as e:
    pytest.skip(f"Could not import processing functions: {e}", allow_module_level=True)


class TestPerformanceBenchmarks:
    """Performance benchmarks for raster operations."""

    @pytest.fixture(scope="class")
    def small_raster_path(self, tmp_path_factory):
        """Create small raster for quick benchmarks."""
        tmp_dir = tmp_path_factory.mktemp("perf_small")
        raster_path = tmp_dir / "small_perf.tif"

        width, height = 512, 384
        data = np.random.randint(0, 1000, (height, width), dtype=np.uint16)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff', height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, width, height)
        ) as dst:
            dst.write(data, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def medium_raster_path(self, tmp_path_factory):
        """Create medium raster for performance testing."""
        tmp_dir = tmp_path_factory.mktemp("perf_medium")
        raster_path = tmp_dir / "medium_perf.tif"

        width, height = 2048, 1536
        data = np.random.randint(0, 4000, (height, width), dtype=np.uint16)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff', height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-112, 33, -111, 34, width, height),
            compress='lzw'
        ) as dst:
            dst.write(data, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def large_multiband_path(self, tmp_path_factory):
        """Create large multiband raster for stress testing."""
        tmp_dir = tmp_path_factory.mktemp("perf_large")
        raster_path = tmp_dir / "large_multiband_perf.tif"

        width, height, bands = 1024, 1024, 6

        # Generate realistic satellite-like data
        np.random.seed(42)
        imagery = np.random.randint(500, 3000, (bands, height, width), dtype=np.uint16)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff', height=height, width=width, count=bands,
            dtype=imagery.dtype, crs='EPSG:4326',
            transform=from_bounds(-113, 32, -110, 35, width, height),
            compress='lzw'
        ) as dst:
            for i in range(bands):
                dst.write(imagery[i], i + 1)

        return raster_path

    def test_raster_analysis_performance_small(self, benchmark, small_raster_path):
        """Benchmark basic raster analysis on small files."""
        def analyze_raster():
            return analyze_local_raster(small_raster_path)

        result = benchmark(analyze_raster)

        # Basic performance assertions
        assert result is not None
        assert 'statistics' in result
        assert 'analysis_timestamp' in result

    def test_raster_analysis_performance_medium(self, benchmark, medium_raster_path):
        """Benchmark raster analysis on medium files."""
        def analyze_medium():
            return analyze_local_raster(medium_raster_path)

        result = benchmark(analyze_medium)

        # Should complete within reasonable time
        assert result is not None
        assert result['dimensions'] == (2048, 1536)

    def test_multiband_processing_performance(self, benchmark, large_multiband_path):
        """Benchmark multiband imagery processing."""
        band_names = ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2']

        def process_multiband():
            return process_multiband_imagery(large_multiband_path, band_names)

        result = benchmark(process_multiband)

        assert result is not None
        assert len(result['band_statistics']) == 6

    def test_cog_optimization_performance(self, benchmark, medium_raster_path, tmp_path):
        """Benchmark COG optimization performance."""
        output_path = tmp_path / "perf_cog.tif"

        def optimize_cog():
            return create_optimized_cog(
                medium_raster_path,
                output_path,
                compress='lzw',
                tiled=True
            )

        result = benchmark(optimize_cog)

        assert output_path.exists()
        assert result['cog_validation']['is_valid_cog'] == True

    def test_cog_validation_performance(self, benchmark, tmp_path, medium_raster_path):
        """Benchmark COG validation performance."""
        # Create COG first
        cog_path = tmp_path / "validation_test.tif"
        create_optimized_cog(medium_raster_path, cog_path)

        def validate_cog():
            return validate_cog_structure(cog_path)

        result = benchmark(validate_cog)

        assert result['is_valid_cog'] == True

    def test_window_size_calculation_performance(self, benchmark, large_multiband_path):
        """Benchmark optimal window size calculation."""
        def calc_window_size():
            return calculate_optimal_window_size(
                large_multiband_path,
                max_memory_mb=1024
            )

        window_size, analysis = benchmark(calc_window_size)

        assert window_size > 0
        assert 'memory_calculations' in analysis


class TestMemoryPerformance:
    """Memory usage and efficiency tests."""

    def test_memory_usage_raster_analysis(self, medium_raster_path):
        """Test memory usage during raster analysis."""
        # Monitor memory before
        initial_memory = monitor_memory_usage()
        gc.collect()  # Clean up before test

        baseline_memory = psutil.Process().memory_info().rss / 1024 / 1024

        # Perform analysis
        result = analyze_local_raster(medium_raster_path)

        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = peak_memory - baseline_memory

        # Clean up
        del result
        gc.collect()

        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_released = peak_memory - final_memory

        # Memory usage should be reasonable
        assert memory_increase < 500  # Less than 500MB increase
        assert memory_released >= 0   # Some memory should be released

    def test_memory_efficiency_windowed_processing(self, tmp_path):
        """Test memory efficiency of windowed processing."""
        # Create large raster for memory testing
        large_raster = tmp_path / "memory_test.tif"
        width, height = 4096, 3072  # Large enough to test memory

        # Use smaller data type to manage memory
        data = np.random.randint(0, 255, (height, width), dtype=np.uint8)

        with rasterio.open(
            large_raster, 'w',
            driver='GTiff', height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-115, 32, -110, 37, width, height)
        ) as dst:
            dst.write(data, 1)

        output_path = tmp_path / "windowed_output.tif"

        # Monitor memory during windowed processing
        def identity_process(arr):
            return arr  # Simple passthrough

        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

        result = process_raster_windowed(
            large_raster,
            output_path,
            identity_process,
            window_size=512
        )

        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = peak_memory - initial_memory

        # Windowed processing should use limited memory
        assert memory_increase < 200  # Should not load entire raster into memory
        assert output_path.exists()
        assert result['windows_processed'] > 10  # Should process multiple windows

    def test_memory_monitoring_accuracy(self):
        """Test accuracy of memory monitoring function."""
        # Get system memory info
        system_memory = psutil.virtual_memory()

        # Use our monitoring function
        our_memory = monitor_memory_usage()

        # Compare values (should be reasonably close)
        total_diff = abs(our_memory['total_mb'] - system_memory.total / 1024 / 1024)
        available_diff = abs(our_memory['available_mb'] - system_memory.available / 1024 / 1024)

        # Should be within 5% or 100MB
        assert total_diff < max(our_memory['total_mb'] * 0.05, 100)
        assert available_diff < max(our_memory['available_mb'] * 0.05, 100)

    def test_memory_leak_detection(self, small_raster_path):
        """Test for memory leaks in repeated operations."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

        # Perform repeated operations
        for i in range(10):
            result = analyze_local_raster(small_raster_path)
            del result  # Explicitly delete

            if i % 5 == 0:
                gc.collect()  # Force garbage collection

        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_growth = final_memory - initial_memory

        # Should not grow significantly with repeated operations
        assert memory_growth < 50  # Less than 50MB growth


class TestScalabilityPerformance:
    """Test performance scaling with different data sizes."""

    def test_analysis_time_scaling(self, tmp_path):
        """Test how analysis time scales with raster size."""
        sizes = [(256, 256), (512, 512), (1024, 1024)]
        times = []

        for width, height in sizes:
            raster_path = tmp_path / f"scale_test_{width}x{height}.tif"
            data = np.random.randint(0, 1000, (height, width), dtype=np.uint16)

            with rasterio.open(
                raster_path, 'w',
                driver='GTiff', height=height, width=width, count=1,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, width, height)
            ) as dst:
                dst.write(data, 1)

            # Time the analysis
            start_time = time.time()
            result = analyze_local_raster(raster_path)
            end_time = time.time()

            times.append(end_time - start_time)
            assert result is not None

        # Time should scale reasonably (not exponentially)
        # Each doubling of pixels shouldn't increase time by more than 5x
        for i in range(1, len(times)):
            pixel_ratio = (sizes[i][0] * sizes[i][1]) / (sizes[i-1][0] * sizes[i-1][1])
            time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 1

            # Time scaling should be reasonable
            assert time_ratio < pixel_ratio * 1.5  # Allow some overhead

    def test_multiband_scaling(self, tmp_path):
        """Test performance scaling with number of bands."""
        band_counts = [1, 3, 6, 12]
        times = []

        width, height = 512, 512

        for band_count in band_counts:
            raster_path = tmp_path / f"multiband_{band_count}.tif"
            data = np.random.randint(0, 2000, (band_count, height, width), dtype=np.uint16)

            with rasterio.open(
                raster_path, 'w',
                driver='GTiff', height=height, width=width, count=band_count,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, width, height)
            ) as dst:
                for i in range(band_count):
                    dst.write(data[i], i + 1)

            # Time multiband processing
            band_names = [f'Band_{i+1}' for i in range(band_count)]

            start_time = time.time()
            result = process_multiband_imagery(raster_path, band_names)
            end_time = time.time()

            times.append(end_time - start_time)
            assert len(result['band_statistics']) == band_count

        # Processing time should scale roughly linearly with band count
        for i in range(1, len(times)):
            band_ratio = band_counts[i] / band_counts[i-1]
            time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 1

            # Time should scale reasonably with band count
            assert time_ratio < band_ratio * 2  # Allow for some overhead


class TestComparativePerformance:
    """Compare performance between different approaches."""

    def test_cog_vs_standard_read_performance(self, tmp_path, medium_raster_path):
        """Compare reading performance: COG vs standard raster."""
        # Create COG version
        cog_path = tmp_path / "comparison_cog.tif"
        optimize_for_cog(medium_raster_path, cog_path)

        # Time standard raster reading
        start_time = time.time()
        with rasterio.open(medium_raster_path) as src:
            standard_data = src.read()
        standard_time = time.time() - start_time

        # Time COG reading
        start_time = time.time()
        with rasterio.open(cog_path) as src:
            cog_data = src.read()
        cog_time = time.time() - start_time

        # Data should be equivalent
        np.testing.assert_array_equal(standard_data, cog_data)

        # COG might be slightly slower for full reads due to organization
        # But should be within reasonable bounds
        time_ratio = cog_time / standard_time if standard_time > 0 else 1
        assert time_ratio < 3  # COG shouldn't be more than 3x slower for full reads

    def test_windowed_vs_full_read_performance(self, tmp_path):
        """Compare windowed vs full reading for partial data access."""
        # Create test raster
        width, height = 2048, 1536
        raster_path = tmp_path / "windowed_test.tif"
        data = np.random.randint(0, 1000, (height, width), dtype=np.uint16)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff', height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, width, height)
        ) as dst:
            dst.write(data, 1)

        # Time full read + subset
        start_time = time.time()
        with rasterio.open(raster_path) as src:
            full_data = src.read(1)
            subset = full_data[500:1000, 500:1000]  # Extract subset
        full_read_time = time.time() - start_time

        # Time windowed read
        from rasterio.windows import Window
        start_time = time.time()
        with rasterio.open(raster_path) as src:
            window = Window(500, 500, 500, 500)
            windowed_data = src.read(1, window=window)
        windowed_time = time.time() - start_time

        # Data should be equivalent
        np.testing.assert_array_equal(subset, windowed_data)

        # Windowed read should be faster for small subsets
        assert windowed_time < full_read_time
        time_improvement = full_read_time / windowed_time if windowed_time > 0 else 1
        assert time_improvement > 2  # Should be at least 2x faster

    def test_compression_performance_comparison(self, tmp_path):
        """Compare performance of different compression methods."""
        width, height = 1024, 768
        data = np.random.randint(0, 4000, (height, width), dtype=np.uint16)

        compressions = ['none', 'lzw', 'deflate']
        write_times = {}
        read_times = {}
        file_sizes = {}

        for compression in compressions:
            raster_path = tmp_path / f"compression_{compression}.tif"

            # Time writing
            start_time = time.time()
            with rasterio.open(
                raster_path, 'w',
                driver='GTiff', height=height, width=width, count=1,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, width, height),
                compress=compression if compression != 'none' else None
            ) as dst:
                dst.write(data, 1)
            write_times[compression] = time.time() - start_time

            # Time reading
            start_time = time.time()
            with rasterio.open(raster_path) as src:
                read_data = src.read(1)
            read_times[compression] = time.time() - start_time

            # File size
            file_sizes[compression] = raster_path.stat().st_size / 1024 / 1024  # MB

            # Verify data integrity
            np.testing.assert_array_equal(data, read_data)

        # Compressed files should be smaller
        assert file_sizes['lzw'] < file_sizes['none']
        assert file_sizes['deflate'] < file_sizes['none']

        # Write times: compression might be slower
        # Read times: should be comparable or faster due to less I/O


class TestConcurrencyPerformance:
    """Test performance under concurrent access."""

    def test_concurrent_read_performance(self, medium_raster_path):
        """Test performance of concurrent raster reads."""
        num_threads = 4
        results = []
        errors = []

        def read_raster():
            try:
                start_time = time.time()
                result = analyze_local_raster(medium_raster_path)
                end_time = time.time()
                results.append({
                    'thread': threading.current_thread().name,
                    'time': end_time - start_time,
                    'success': True
                })
            except Exception as e:
                errors.append({
                    'thread': threading.current_thread().name,
                    'error': str(e)
                })

        # Run concurrent reads
        threads = []
        start_time = time.time()

        for i in range(num_threads):
            thread = threading.Thread(target=read_raster, name=f'Thread-{i}')
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_time = time.time() - start_time

        # All threads should succeed
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == num_threads

        # Concurrent reads should not be much slower than sequential
        avg_thread_time = sum(r['time'] for r in results) / len(results)

        # Total wall clock time should be less than sum of individual times
        assert total_time < avg_thread_time * num_threads * 0.8  # Some parallelization benefit

    def test_memory_usage_under_concurrency(self, small_raster_path):
        """Test memory usage during concurrent operations."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

        def memory_intensive_operation():
            # Perform several operations
            for _ in range(3):
                result = analyze_local_raster(small_raster_path)
                time.sleep(0.1)  # Small delay
                del result

        # Run concurrent operations
        threads = []
        for i in range(3):
            thread = threading.Thread(target=memory_intensive_operation)
            threads.append(thread)
            thread.start()

        # Monitor peak memory during execution
        peak_memory = initial_memory
        while any(t.is_alive() for t in threads):
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            peak_memory = max(peak_memory, current_memory)
            time.sleep(0.05)

        for thread in threads:
            thread.join()

        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_growth = peak_memory - initial_memory

        # Memory growth should be reasonable even under concurrency
        assert memory_growth < 300  # Less than 300MB growth
        assert final_memory < peak_memory * 1.1  # Memory should be mostly released


class TestPerformanceRegression:
    """Test for performance regressions."""

    def test_analysis_performance_baseline(self, medium_raster_path):
        """Establish baseline for raster analysis performance."""
        # This test serves as a baseline for performance regression testing
        times = []

        # Run multiple iterations for stable measurement
        for _ in range(5):
            start_time = time.time()
            result = analyze_local_raster(medium_raster_path)
            end_time = time.time()
            times.append(end_time - start_time)
            assert result is not None

        avg_time = sum(times) / len(times)
        std_time = np.std(times)

        # Performance should be consistent
        assert std_time < avg_time * 0.5  # Standard deviation < 50% of mean

        # Baseline expectation: should complete within reasonable time
        # For a 2048x1536 raster, should complete in < 10 seconds
        assert avg_time < 10.0

        print(f"Performance baseline: {avg_time:.3f}s ± {std_time:.3f}s")

    def test_memory_usage_baseline(self, medium_raster_path):
        """Establish baseline for memory usage."""
        gc.collect()  # Clean up first
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

        result = analyze_local_raster(medium_raster_path)

        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_usage = peak_memory - initial_memory

        del result
        gc.collect()

        # Memory usage baseline
        assert memory_usage < 100  # Should use less than 100MB for medium raster

        print(f"Memory usage baseline: {memory_usage:.1f} MB")
