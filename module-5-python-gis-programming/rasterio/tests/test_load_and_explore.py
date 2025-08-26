"""
Tests for load_and_explore_raster function

This module contains comprehensive tests for the load_and_explore_raster function
that validates raster file loading and metadata extraction capabilities.

Author: GIST 604B Teaching Team
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Simplified Raster Data Processing
"""

import pytest
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

# Import the function to test
import sys
sys.path.insert(0, 'src')
from rasterio_basics import load_and_explore_raster


class TestLoadAndExploreRaster:
    """Test suite for load_and_explore_raster function."""

    @pytest.fixture
    def sample_raster_gtiff(self):
        """Create a sample GeoTIFF raster file for testing."""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create sample data
        width, height = 100, 80
        data = np.random.randint(0, 255, size=(height, width), dtype=np.uint8)

        # Define spatial properties
        left, bottom, right, top = -120.0, 35.0, -119.0, 36.0
        transform = from_bounds(left, bottom, right, top, width, height)
        crs = CRS.from_epsg(4326)

        # Write raster file
        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=crs,
            transform=transform,
            nodata=255
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        # Cleanup
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def multiband_raster(self):
        """Create a multi-band raster file for testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create 3-band RGB-like data
        width, height, bands = 50, 40, 3
        data = np.random.randint(0, 255, size=(bands, height, width), dtype=np.uint8)

        # Define spatial properties
        left, bottom, right, top = 0.0, 0.0, 1000.0, 800.0  # UTM-like coordinates
        transform = from_bounds(left, bottom, right, top, width, height)
        crs = CRS.from_epsg(32633)  # UTM Zone 33N

        # Write raster file
        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=data.dtype,
            crs=crs,
            transform=transform
        ) as dst:
            dst.write(data)

        yield temp_file.name

        # Cleanup
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def float32_raster_with_nodata(self):
        """Create a float32 raster with nodata values for testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create elevation-like data with some nodata areas
        width, height = 60, 50
        data = np.random.uniform(100, 1500, size=(height, width)).astype(np.float32)

        # Add some nodata values
        data[0:5, 0:5] = -9999.0  # nodata corner
        data[25:30, 25:30] = -9999.0  # nodata center area

        # Define spatial properties
        left, bottom, right, top = -111.0, 40.0, -110.0, 41.0
        transform = from_bounds(left, bottom, right, top, width, height)
        crs = CRS.from_epsg(4326)

        # Write raster file
        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=crs,
            transform=transform,
            nodata=-9999.0
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        # Cleanup
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    def test_basic_functionality(self, sample_raster_gtiff):
        """Test basic functionality with a standard GeoTIFF."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Test return type
        assert isinstance(result, dict), "Function should return a dictionary"

        # Test required keys are present
        required_keys = [
            'width', 'height', 'count', 'crs', 'driver', 'dtype',
            'nodata', 'bounds', 'transform', 'pixel_size'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Test data types and basic values
        assert isinstance(result['width'], int), "Width should be integer"
        assert isinstance(result['height'], int), "Height should be integer"
        assert isinstance(result['count'], int), "Count should be integer"
        assert isinstance(result['driver'], str), "Driver should be string"
        assert isinstance(result['dtype'], str), "Dtype should be string"

        # Test specific values for our sample
        assert result['width'] == 100, "Width should be 100"
        assert result['height'] == 80, "Height should be 80"
        assert result['count'] == 1, "Count should be 1"
        assert result['driver'] == 'GTiff', "Driver should be GTiff"
        assert result['nodata'] == 255, "NoData should be 255"

    def test_crs_handling(self, sample_raster_gtiff):
        """Test CRS information extraction and formatting."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Test CRS is present and properly formatted
        assert 'crs' in result
        crs_str = result['crs']
        assert isinstance(crs_str, str), "CRS should be string"
        assert 'EPSG:4326' in crs_str or 'WGS 84' in crs_str, "Should contain WGS84/EPSG:4326 info"

    def test_bounds_extraction(self, sample_raster_gtiff):
        """Test geographic bounds extraction."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Test bounds structure
        assert 'bounds' in result
        bounds = result['bounds']
        assert isinstance(bounds, dict), "Bounds should be dictionary"

        # Test required bounds keys
        bounds_keys = ['left', 'bottom', 'right', 'top']
        for key in bounds_keys:
            assert key in bounds, f"Missing bounds key: {key}"
            assert isinstance(bounds[key], (int, float)), f"Bounds {key} should be numeric"

        # Test logical bounds relationships
        assert bounds['left'] < bounds['right'], "Left should be less than right"
        assert bounds['bottom'] < bounds['top'], "Bottom should be less than top"

        # Test approximate values for our sample
        assert abs(bounds['left'] - (-120.0)) < 0.01, "Left bound should be approximately -120.0"
        assert abs(bounds['right'] - (-119.0)) < 0.01, "Right bound should be approximately -119.0"

    def test_transform_extraction(self, sample_raster_gtiff):
        """Test affine transformation matrix extraction."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Test transform is present
        assert 'transform' in result
        transform = result['transform']
        assert isinstance(transform, list), "Transform should be list"
        assert len(transform) == 6, "Transform should have 6 elements"

        # Test all elements are numeric
        for i, val in enumerate(transform):
            assert isinstance(val, (int, float)), f"Transform element {i} should be numeric"

    def test_pixel_size_calculation(self, sample_raster_gtiff):
        """Test pixel size calculation from transform."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Test pixel_size structure
        assert 'pixel_size' in result
        pixel_size = result['pixel_size']
        assert isinstance(pixel_size, (tuple, list)), "Pixel size should be tuple or list"
        assert len(pixel_size) == 2, "Pixel size should have 2 elements (x_res, y_res)"

        # Test pixel size values are positive
        x_res, y_res = pixel_size
        assert isinstance(x_res, (int, float)), "X resolution should be numeric"
        assert isinstance(y_res, (int, float)), "Y resolution should be numeric"
        assert x_res > 0, "X resolution should be positive"
        assert y_res > 0, "Y resolution should be positive"

        # Test approximate pixel size for our 1°x1° extent with 100x80 pixels
        expected_x_res = 1.0 / 100  # ~0.01 degrees
        expected_y_res = 1.0 / 80   # ~0.0125 degrees
        assert abs(x_res - expected_x_res) < 0.001, f"X resolution should be ~{expected_x_res}"
        assert abs(y_res - expected_y_res) < 0.001, f"Y resolution should be ~{expected_y_res}"

    def test_multiband_raster(self, multiband_raster):
        """Test with multi-band raster data."""
        result = load_and_explore_raster(multiband_raster)

        # Test multi-band specific properties
        assert result['count'] == 3, "Should detect 3 bands"
        assert result['width'] == 50, "Width should be 50"
        assert result['height'] == 40, "Height should be 40"

        # Test UTM CRS detection
        crs_str = result['crs']
        assert '32633' in crs_str or 'UTM' in crs_str, "Should detect UTM CRS"

    def test_float_raster_with_nodata(self, float32_raster_with_nodata):
        """Test with float32 raster containing nodata values."""
        result = load_and_explore_raster(float32_raster_with_nodata)

        # Test data type detection
        assert 'float32' in result['dtype'], "Should detect float32 dtype"

        # Test nodata value detection
        assert result['nodata'] == -9999.0, "Should detect nodata value of -9999.0"

    def test_file_not_found_error(self):
        """Test error handling for non-existent file."""
        non_existent_file = "this_file_does_not_exist.tif"

        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            load_and_explore_raster(non_existent_file)

    def test_invalid_file_error(self):
        """Test error handling for invalid raster file."""
        # Create a text file with .tif extension
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False, mode='w')
        temp_file.write("This is not a raster file!")
        temp_file.close()

        try:
            with pytest.raises(rasterio.RasterioIOError):
                load_and_explore_raster(temp_file.name)
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_raster_no_nodata(self, multiband_raster):
        """Test raster without nodata value."""
        result = load_and_explore_raster(multiband_raster)

        # This raster was created without nodata
        assert result['nodata'] is None, "Should return None for raster without nodata"

    @pytest.mark.parametrize("width,height", [
        (1, 1),      # Minimum size
        (10, 5),     # Small rectangular
        (500, 500),  # Large square
    ])
    def test_various_raster_sizes(self, width, height):
        """Test with various raster dimensions."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        try:
            # Create raster with specified dimensions
            data = np.ones((height, width), dtype=np.int16)
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

            # Test the function
            result = load_and_explore_raster(temp_file.name)
            assert result['width'] == width, f"Width should be {width}"
            assert result['height'] == height, f"Height should be {height}"

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_comprehensive_integration(self, sample_raster_gtiff):
        """Comprehensive integration test checking all aspects together."""
        result = load_and_explore_raster(sample_raster_gtiff)

        # Verify all expected keys are present with correct types
        expected_structure = {
            'width': int,
            'height': int,
            'count': int,
            'crs': str,
            'driver': str,
            'dtype': str,
            'nodata': (type(None), int, float),
            'bounds': dict,
            'transform': list,
            'pixel_size': (tuple, list)
        }

        for key, expected_type in expected_structure.items():
            assert key in result, f"Missing key: {key}"
            if isinstance(expected_type, tuple):
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type"
            else:
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type"

        # Verify bounds dictionary structure
        bounds = result['bounds']
        for bounds_key in ['left', 'bottom', 'right', 'top']:
            assert bounds_key in bounds, f"Missing bounds key: {bounds_key}"
            assert isinstance(bounds[bounds_key], (int, float)), f"Bounds {bounds_key} should be numeric"

        # Verify transform has 6 numeric elements
        transform = result['transform']
        assert len(transform) == 6, "Transform should have 6 elements"
        for i, val in enumerate(transform):
            assert isinstance(val, (int, float)), f"Transform element {i} should be numeric"

        # Verify pixel_size has 2 positive numeric elements
        pixel_size = result['pixel_size']
        assert len(pixel_size) == 2, "Pixel size should have 2 elements"
        assert all(isinstance(val, (int, float)) and val > 0 for val in pixel_size), "Pixel size elements should be positive numbers"

    def test_return_value_json_serializable(self, sample_raster_gtiff):
        """Test that returned values are JSON serializable."""
        import json

        result = load_and_explore_raster(sample_raster_gtiff)

        # This should not raise an exception if all values are JSON serializable
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON serializable: {e}")
