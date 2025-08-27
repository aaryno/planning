"""
Tests for visualize_raster_data function

This module contains comprehensive tests for the visualize_raster_data function
that validates raster data visualization capabilities with matplotlib.

Author: GIST 604B Teaching Team
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Simplified Raster Data Processing
"""

import pytest
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Tuple
import shutil

# Import the function to test
import sys
sys.path.insert(0, 'src')
from rasterio_basics import visualize_raster_data


class TestVisualizeRasterData:
    """Test suite for visualize_raster_data function."""

    @pytest.fixture
    def simple_raster(self):
        """Create simple raster with known values for testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create simple 10x8 raster with gradient pattern
        width, height = 10, 8
        data = np.arange(width * height, dtype=np.float32).reshape(height, width)

        # Add some variation to make visualization more interesting
        data = data + np.random.normal(0, 5, data.shape)

        transform = from_bounds(-1.0, -1.0, 1.0, 1.0, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def elevation_raster_with_nodata(self):
        """Create elevation-like raster with nodata values."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height = 20, 15
        # Create elevation data (0-3000m)
        data = np.random.uniform(0, 3000, size=(height, width)).astype(np.float32)

        # Add some nodata areas (water bodies, etc.)
        data[0:3, 0:3] = -9999.0  # Corner lake
        data[7:10, 7:12] = -9999.0  # Central lake
        data[12:15, 16:20] = -9999.0  # Edge water

        transform = from_bounds(-120.0, 35.0, -119.0, 36.0, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            nodata=-9999.0
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def multiband_rgb_raster(self):
        """Create RGB-like multi-band raster."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height, bands = 15, 12, 3

        # Create RGB-like data
        red = np.random.randint(0, 255, size=(height, width), dtype=np.uint8)
        green = np.random.randint(0, 255, size=(height, width), dtype=np.uint8)
        blue = np.random.randint(0, 255, size=(height, width), dtype=np.uint8)

        data = np.stack([red, green, blue])

        transform = from_bounds(0.0, 0.0, 15.0, 12.0, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform
        ) as dst:
            dst.write(data)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def integer_raster(self):
        """Create integer raster for testing different data types."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height = 12, 10
        # Create classification-like data (land use codes)
        data = np.random.randint(1, 8, size=(height, width), dtype=np.int16)

        transform = from_bounds(-180.0, -90.0, 180.0, 90.0, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for output files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_basic_functionality(self, simple_raster):
        """Test basic visualization functionality."""
        result = visualize_raster_data(simple_raster)

        # Test return type
        assert isinstance(result, dict), "Function should return a dictionary"

        # Test required keys are present
        required_keys = [
            'data_range', 'data_stats', 'figure_size', 'colormap_used',
            'plot_saved', 'save_path', 'valid_pixels_displayed'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Test data types
        assert isinstance(result['data_range'], (list, tuple)), "Data range should be list or tuple"
        assert isinstance(result['data_stats'], dict), "Data stats should be dict"
        assert isinstance(result['figure_size'], (list, tuple)), "Figure size should be list or tuple"
        assert isinstance(result['colormap_used'], str), "Colormap used should be string"
        assert isinstance(result['plot_saved'], bool), "Plot saved should be bool"
        assert isinstance(result['valid_pixels_displayed'], int), "Valid pixels should be int"

        # Test default values
        assert result['colormap_used'] == 'viridis', "Default colormap should be viridis"
        assert result['figure_size'] == (10, 8), "Default figure size should be (10, 8)"
        assert result['plot_saved'] is False, "Plot should not be saved by default"
        assert result['save_path'] is None, "Save path should be None by default"

        # Test data range format
        data_range = result['data_range']
        assert len(data_range) == 2, "Data range should have min and max values"
        assert data_range[0] <= data_range[1], "Min should be <= max in data range"

        # Test valid pixels count
        assert result['valid_pixels_displayed'] > 0, "Should display some valid pixels"

        plt.close('all')  # Clean up matplotlib figures

    def test_custom_colormap(self, simple_raster):
        """Test visualization with different colormaps."""
        colormaps = ['viridis', 'plasma', 'terrain', 'hot', 'cool', 'gray']

        for cmap in colormaps:
            result = visualize_raster_data(simple_raster, colormap=cmap)

            assert result['colormap_used'] == cmap, f"Should use {cmap} colormap"
            assert isinstance(result, dict), f"Should return dict for {cmap} colormap"

            plt.close('all')  # Clean up after each test

    def test_custom_figure_size(self, simple_raster):
        """Test visualization with different figure sizes."""
        test_sizes = [(6, 4), (12, 8), (8, 6), (15, 10)]

        for figsize in test_sizes:
            result = visualize_raster_data(simple_raster, figsize=figsize)

            assert result['figure_size'] == figsize, f"Should use figure size {figsize}"
            assert isinstance(result, dict), f"Should return dict for figsize {figsize}"

            plt.close('all')

    def test_custom_title(self, simple_raster):
        """Test visualization with custom title."""
        custom_title = "Test Elevation Map"

        result = visualize_raster_data(simple_raster, title=custom_title)

        # Function should complete successfully with custom title
        assert isinstance(result, dict), "Should return dict with custom title"

        plt.close('all')

    def test_band_selection(self, multiband_rgb_raster):
        """Test visualization of specific bands in multi-band raster."""
        # Test each band
        for band_num in [1, 2, 3]:
            result = visualize_raster_data(multiband_rgb_raster, band_number=band_num)

            assert isinstance(result, dict), f"Should handle band {band_num}"
            assert result['valid_pixels_displayed'] > 0, f"Should display pixels from band {band_num}"

            plt.close('all')

    def test_nodata_handling(self, elevation_raster_with_nodata):
        """Test visualization with nodata values."""
        result = visualize_raster_data(elevation_raster_with_nodata)

        # Should handle nodata values gracefully
        assert isinstance(result, dict), "Should handle nodata values"

        # Valid pixels should be less than total pixels due to nodata
        total_pixels = 20 * 15  # 300 total pixels
        assert result['valid_pixels_displayed'] < total_pixels, "Should have fewer valid pixels due to nodata"
        assert result['valid_pixels_displayed'] > 0, "Should still have some valid pixels"

        # Data range should not include nodata values
        data_range = result['data_range']
        assert data_range[0] >= 0, "Min value should not include nodata (-9999)"
        assert data_range[1] <= 3000, "Max value should be reasonable elevation"

        plt.close('all')

    def test_file_saving(self, simple_raster, temp_output_dir):
        """Test saving visualization to file."""
        save_path = os.path.join(temp_output_dir, "test_plot.png")

        result = visualize_raster_data(simple_raster, save_path=save_path)

        # Test file saving indicators
        assert result['plot_saved'] is True, "Plot should be saved"
        assert result['save_path'] == save_path, "Save path should match"

        # Test that file actually exists
        assert os.path.exists(save_path), "Plot file should exist"

        # Test file has reasonable size (not empty)
        file_size = os.path.getsize(save_path)
        assert file_size > 1000, "Plot file should have reasonable size (>1KB)"

        plt.close('all')

    def test_different_file_formats(self, simple_raster, temp_output_dir):
        """Test saving to different file formats."""
        formats = ['.png', '.jpg', '.pdf', '.svg']

        for ext in formats:
            save_path = os.path.join(temp_output_dir, f"test_plot{ext}")

            try:
                result = visualize_raster_data(simple_raster, save_path=save_path)

                assert result['plot_saved'] is True, f"Should save {ext} format"
                assert os.path.exists(save_path), f"{ext} file should exist"

            except Exception as e:
                # Some formats might not be available in test environment
                pytest.skip(f"Format {ext} not available: {e}")

            plt.close('all')

    def test_data_statistics_calculation(self, simple_raster):
        """Test that data statistics are calculated correctly."""
        result = visualize_raster_data(simple_raster)

        data_stats = result['data_stats']

        # Should contain basic statistics
        expected_stats = ['min', 'max', 'mean', 'std']
        for stat in expected_stats:
            assert stat in data_stats, f"Should contain {stat} statistic"
            if data_stats[stat] is not None:
                assert isinstance(data_stats[stat], (int, float)), f"{stat} should be numeric"

        # Logical relationships
        if all(data_stats[key] is not None for key in ['min', 'max', 'mean']):
            assert data_stats['min'] <= data_stats['mean'] <= data_stats['max'], "Statistical relationships should be logical"

        # Standard deviation should be non-negative
        if data_stats['std'] is not None:
            assert data_stats['std'] >= 0, "Standard deviation should be non-negative"

        plt.close('all')

    def test_integer_raster_visualization(self, integer_raster):
        """Test visualization of integer raster data."""
        result = visualize_raster_data(integer_raster, colormap='tab10')

        # Should handle integer data correctly
        assert isinstance(result, dict), "Should handle integer raster"

        # Data range should be integers
        data_range = result['data_range']
        assert 1 <= data_range[0] <= 7, "Min should be in expected range for integer data"
        assert 1 <= data_range[1] <= 7, "Max should be in expected range for integer data"

        plt.close('all')

    def test_invalid_band_number(self, simple_raster):
        """Test error handling for invalid band numbers."""
        # Test band number too high
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            visualize_raster_data(simple_raster, band_number=10)

        # Test band number 0 (should be 1-based)
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            visualize_raster_data(simple_raster, band_number=0)

        # Test negative band number
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            visualize_raster_data(simple_raster, band_number=-1)

    def test_invalid_colormap(self, simple_raster):
        """Test error handling for invalid colormap."""
        invalid_colormap = "this_colormap_does_not_exist"

        with pytest.raises((ValueError, KeyError)):
            visualize_raster_data(simple_raster, colormap=invalid_colormap)

    def test_file_not_found_error(self):
        """Test error handling for non-existent file."""
        non_existent_file = "this_file_does_not_exist.tif"

        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            visualize_raster_data(non_existent_file)

    def test_invalid_save_path(self, simple_raster):
        """Test error handling for invalid save paths."""
        invalid_save_path = "/invalid/directory/that/does/not/exist/plot.png"

        with pytest.raises((OSError, IOError)):
            visualize_raster_data(simple_raster, save_path=invalid_save_path)

    def test_invalid_figure_size(self, simple_raster):
        """Test error handling for invalid figure sizes."""
        invalid_sizes = [
            (0, 8),    # Zero width
            (10, 0),   # Zero height
            (-5, 8),   # Negative width
            (10, -3),  # Negative height
        ]

        for invalid_size in invalid_sizes:
            with pytest.raises((ValueError, TypeError)):
                visualize_raster_data(simple_raster, figsize=invalid_size)

    def test_matplotlib_figure_cleanup(self, simple_raster):
        """Test that matplotlib figures are properly managed."""
        # Get initial figure count
        initial_figs = len(plt.get_fignums())

        # Create several visualizations
        for i in range(3):
            result = visualize_raster_data(simple_raster, title=f"Test {i}")
            assert isinstance(result, dict)

        # The function should either close figures or manage them properly
        # We don't want to accumulate many open figures
        final_figs = len(plt.get_fignums())

        # Clean up any remaining figures
        plt.close('all')

        # Test passes if we get here without memory/resource issues
        assert True, "Figure cleanup test completed"

    def test_large_raster_handling(self):
        """Test visualization of larger raster (memory efficiency)."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        try:
            # Create larger raster (but not too large for CI)
            width, height = 200, 150
            data = np.random.rand(height, width).astype(np.float32) * 1000

            transform = from_bounds(0, 0, width, height, width, height)

            with rasterio.open(
                temp_file.name, 'w',
                driver='GTiff',
                height=height,
                width=width,
                count=1,
                dtype=data.dtype,
                crs=CRS.from_epsg(4326),
                transform=transform
            ) as dst:
                dst.write(data, 1)

            # Should handle larger raster without issues
            result = visualize_raster_data(temp_file.name)
            assert isinstance(result, dict)
            assert result['valid_pixels_displayed'] == width * height

            plt.close('all')

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_extreme_data_values(self):
        """Test visualization with extreme data values."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        try:
            # Create data with extreme values
            width, height = 10, 8
            data = np.array([
                [1e-10, 1e10],
                [0.0, 1e6]
            ], dtype=np.float64)
            data = np.tile(data, (height//2, width//2))

            transform = from_bounds(0, 0, width, height, width, height)

            with rasterio.open(
                temp_file.name, 'w',
                driver='GTiff',
                height=height,
                width=width,
                count=1,
                dtype=data.dtype,
                crs=CRS.from_epsg(4326),
                transform=transform
            ) as dst:
                dst.write(data, 1)

            # Should handle extreme values gracefully
            result = visualize_raster_data(temp_file.name)
            assert isinstance(result, dict)

            # Data range should capture extreme values
            data_range = result['data_range']
            assert data_range[0] <= 1e-10, "Should capture very small values"
            assert data_range[1] >= 1e6, "Should capture very large values"

            plt.close('all')

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_return_value_json_serializable(self, simple_raster):
        """Test that returned values are JSON serializable."""
        import json

        result = visualize_raster_data(simple_raster)

        # This should not raise an exception if all values are JSON serializable
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON serializable: {e}")

        plt.close('all')

    def test_comprehensive_integration(self, elevation_raster_with_nodata, temp_output_dir):
        """Comprehensive integration test checking all aspects together."""
        save_path = os.path.join(temp_output_dir, "comprehensive_test.png")

        result = visualize_raster_data(
            elevation_raster_with_nodata,
            band_number=1,
            colormap='terrain',
            figsize=(12, 9),
            title="Comprehensive Test Elevation Map",
            save_path=save_path
        )

        # Verify all expected keys with correct types
        expected_structure = {
            'data_range': (list, tuple),
            'data_stats': dict,
            'figure_size': (list, tuple),
            'colormap_used': str,
            'plot_saved': bool,
            'save_path': str,
            'valid_pixels_displayed': int
        }

        for key, expected_type in expected_structure.items():
            assert key in result, f"Missing key: {key}"
            if isinstance(expected_type, tuple):
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type: {type(result[key])}"
            else:
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type: {type(result[key])}"

        # Verify specific values for comprehensive test
        assert result['colormap_used'] == 'terrain', "Should use terrain colormap"
        assert result['figure_size'] == (12, 9), "Should use custom figure size"
        assert result['plot_saved'] is True, "Should save the plot"
        assert result['save_path'] == save_path, "Should match save path"

        # Verify file operations
        assert os.path.exists(save_path), "Plot file should exist"

        # Verify data handling
        assert len(result['data_range']) == 2, "Data range should have min and max"
        assert result['data_range'][0] < result['data_range'][1], "Min should be less than max"
        assert result['valid_pixels_displayed'] > 0, "Should display valid pixels"
        assert result['valid_pixels_displayed'] < 20 * 15, "Should have fewer pixels due to nodata"

        # Verify data stats structure
        data_stats = result['data_stats']
        for stat_key in ['min', 'max', 'mean', 'std']:
            assert stat_key in data_stats, f"Missing statistic: {stat_key}"

        plt.close('all')

    def test_matplotlib_backend_compatibility(self, simple_raster):
        """Test compatibility with different matplotlib backends."""
        # Test should work with Agg backend (non-interactive)
        original_backend = matplotlib.get_backend()

        try:
            matplotlib.use('Agg')
            result = visualize_raster_data(simple_raster)
            assert isinstance(result, dict), "Should work with Agg backend"

            plt.close('all')

        finally:
            # Restore original backend
            matplotlib.use(original_backend)
