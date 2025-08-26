"""
Tests for calculate_raster_statistics function

This module contains comprehensive tests for the calculate_raster_statistics function
that validates statistical calculations on raster data with various configurations.

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
import math

# Import the function to test
import sys
sys.path.insert(0, 'src')
from rasterio_basics import calculate_raster_statistics


class TestCalculateRasterStatistics:
    """Test suite for calculate_raster_statistics function."""

    @pytest.fixture
    def integer_raster_no_nodata(self):
        """Create integer raster without nodata values."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create predictable integer data for testing
        width, height = 10, 8
        # Create data with known statistics: values 1-80
        data = np.arange(1, width * height + 1, dtype=np.int16).reshape(height, width)

        transform = from_bounds(0, 0, 10, 8, width, height)

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
    def float_raster_with_nodata(self):
        """Create float raster with nodata values."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height = 12, 10
        # Create elevation-like data
        data = np.random.uniform(500, 2000, size=(height, width)).astype(np.float32)

        # Add specific nodata areas
        data[0, :] = -9999.0  # Top row nodata
        data[:, 0] = -9999.0  # Left column nodata
        data[5:7, 5:7] = -9999.0  # Center block nodata

        transform = from_bounds(-111, 40, -110, 41, width, height)

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
    def multiband_raster(self):
        """Create multi-band raster for band selection testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height, bands = 6, 5, 3

        # Band 1: Low values (0-50)
        band1 = np.random.randint(0, 51, size=(height, width), dtype=np.uint8)

        # Band 2: Medium values (100-150)
        band2 = np.random.randint(100, 151, size=(height, width), dtype=np.uint8)

        # Band 3: High values (200-255)
        band3 = np.random.randint(200, 256, size=(height, width), dtype=np.uint8)

        data = np.stack([band1, band2, band3])

        transform = from_bounds(0, 0, 6, 5, width, height)

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
    def all_nodata_raster(self):
        """Create raster with all nodata values."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height = 5, 4
        data = np.full((height, width), -32768, dtype=np.int16)

        transform = from_bounds(0, 0, 5, 4, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            nodata=-32768
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def single_pixel_raster(self):
        """Create single pixel raster."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        data = np.array([[42]], dtype=np.int32)

        transform = from_bounds(0, 0, 1, 1, 1, 1)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=1,
            width=1,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    def test_basic_functionality(self, integer_raster_no_nodata):
        """Test basic functionality with integer raster without nodata."""
        result = calculate_raster_statistics(integer_raster_no_nodata)

        # Test return type
        assert isinstance(result, dict), "Function should return a dictionary"

        # Test required keys are present
        required_keys = [
            'min', 'max', 'mean', 'median', 'std', 'range',
            'percentile_25', 'percentile_75', 'valid_pixels',
            'total_pixels', 'nodata_pixels'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Test data types
        for key in ['min', 'max', 'mean', 'median', 'std', 'range', 'percentile_25', 'percentile_75']:
            assert isinstance(result[key], (int, float)), f"{key} should be numeric"

        for key in ['valid_pixels', 'total_pixels', 'nodata_pixels']:
            assert isinstance(result[key], int), f"{key} should be integer"

    def test_known_statistics(self, integer_raster_no_nodata):
        """Test with known data to verify statistical calculations."""
        result = calculate_raster_statistics(integer_raster_no_nodata)

        # Data is 1-80, so we know the statistics
        expected_min = 1
        expected_max = 80
        expected_mean = 40.5  # (1+80)/2
        expected_median = 40.5
        expected_range = 79  # 80-1

        assert result['min'] == expected_min, f"Min should be {expected_min}"
        assert result['max'] == expected_max, f"Max should be {expected_max}"
        assert abs(result['mean'] - expected_mean) < 0.1, f"Mean should be approximately {expected_mean}"
        assert abs(result['median'] - expected_median) < 0.1, f"Median should be approximately {expected_median}"
        assert result['range'] == expected_range, f"Range should be {expected_range}"

        # Test pixel counts
        assert result['total_pixels'] == 80, "Total pixels should be 80"
        assert result['valid_pixels'] == 80, "Valid pixels should be 80"
        assert result['nodata_pixels'] == 0, "NoData pixels should be 0"

    def test_percentile_calculations(self, integer_raster_no_nodata):
        """Test percentile calculations."""
        result = calculate_raster_statistics(integer_raster_no_nodata)

        # For data 1-80, 25th percentile should be around 20.25, 75th around 60.75
        assert 19 <= result['percentile_25'] <= 22, "25th percentile should be around 20"
        assert 59 <= result['percentile_75'] <= 62, "75th percentile should be around 61"

        # Logical relationship: 25th < median < 75th
        assert result['percentile_25'] < result['median'], "25th percentile should be less than median"
        assert result['median'] < result['percentile_75'], "Median should be less than 75th percentile"

    def test_nodata_handling_exclude_true(self, float_raster_with_nodata):
        """Test nodata handling with exclude_nodata=True."""
        result = calculate_raster_statistics(float_raster_with_nodata, exclude_nodata=True)

        # Should have some nodata pixels
        assert result['nodata_pixels'] > 0, "Should detect nodata pixels"
        assert result['valid_pixels'] < result['total_pixels'], "Valid pixels should be less than total"
        assert result['valid_pixels'] + result['nodata_pixels'] == result['total_pixels'], "Pixel counts should sum correctly"

        # Statistics should not include nodata values
        assert result['min'] >= 500, "Min should be >= 500 (excluding nodata)"
        assert result['max'] <= 2000, "Max should be <= 2000 (excluding nodata)"

    def test_nodata_handling_exclude_false(self, float_raster_with_nodata):
        """Test nodata handling with exclude_nodata=False."""
        result = calculate_raster_statistics(float_raster_with_nodata, exclude_nodata=False)

        # Should still count nodata pixels but include them in statistics
        assert result['nodata_pixels'] > 0, "Should still detect nodata pixels"

        # Statistics should include nodata values, so min should be the nodata value
        assert result['min'] == -9999.0, "Min should include nodata value when exclude_nodata=False"

    def test_multiband_different_bands(self, multiband_raster):
        """Test statistics calculation on different bands."""
        # Test band 1 (low values 0-50)
        result_band1 = calculate_raster_statistics(multiband_raster, band_number=1)

        # Test band 2 (medium values 100-150)
        result_band2 = calculate_raster_statistics(multiband_raster, band_number=2)

        # Test band 3 (high values 200-255)
        result_band3 = calculate_raster_statistics(multiband_raster, band_number=3)

        # Band 1 should have lower values than band 2 and 3
        assert result_band1['max'] < result_band2['min'], "Band 1 max should be less than band 2 min"
        assert result_band2['max'] < result_band3['min'], "Band 2 max should be less than band 3 min"

        # All bands should have same pixel counts
        for band_result in [result_band1, result_band2, result_band3]:
            assert band_result['total_pixels'] == 30, "Each band should have 30 pixels"
            assert band_result['valid_pixels'] == 30, "Each band should have 30 valid pixels"
            assert band_result['nodata_pixels'] == 0, "Each band should have 0 nodata pixels"

    def test_all_nodata_raster(self, all_nodata_raster):
        """Test with raster containing only nodata values."""
        result = calculate_raster_statistics(all_nodata_raster, exclude_nodata=True)

        # All statistics should be None when all pixels are nodata
        stat_keys = ['min', 'max', 'mean', 'median', 'std', 'range', 'percentile_25', 'percentile_75']
        for key in stat_keys:
            assert result[key] is None, f"{key} should be None when all pixels are nodata"

        # Pixel counts should be correct
        assert result['total_pixels'] == 20, "Total pixels should be 20"
        assert result['valid_pixels'] == 0, "Valid pixels should be 0"
        assert result['nodata_pixels'] == 20, "NoData pixels should be 20"

    def test_single_pixel_raster(self, single_pixel_raster):
        """Test with single pixel raster."""
        result = calculate_raster_statistics(single_pixel_raster)

        # With single pixel, all statistics should equal that value
        expected_value = 42
        stat_keys = ['min', 'max', 'mean', 'median', 'percentile_25', 'percentile_75']
        for key in stat_keys:
            assert result[key] == expected_value, f"{key} should equal {expected_value} for single pixel"

        # Standard deviation should be 0
        assert result['std'] == 0.0, "Standard deviation should be 0 for single pixel"

        # Range should be 0
        assert result['range'] == 0, "Range should be 0 for single pixel"

        # Pixel counts
        assert result['total_pixels'] == 1, "Total pixels should be 1"
        assert result['valid_pixels'] == 1, "Valid pixels should be 1"
        assert result['nodata_pixels'] == 0, "NoData pixels should be 0"

    def test_invalid_band_number(self, multiband_raster):
        """Test error handling for invalid band numbers."""
        # Test band number too high
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            calculate_raster_statistics(multiband_raster, band_number=10)

        # Test band number 0 (should be 1-based)
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            calculate_raster_statistics(multiband_raster, band_number=0)

        # Test negative band number
        with pytest.raises((ValueError, IndexError, rasterio.RasterioIOError)):
            calculate_raster_statistics(multiband_raster, band_number=-1)

    def test_file_not_found_error(self):
        """Test error handling for non-existent file."""
        non_existent_file = "this_file_does_not_exist.tif"

        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            calculate_raster_statistics(non_existent_file)

    def test_parameter_validation(self, integer_raster_no_nodata):
        """Test parameter type validation."""
        # Test valid parameters work
        result = calculate_raster_statistics(integer_raster_no_nodata, band_number=1, exclude_nodata=True)
        assert isinstance(result, dict)

        result = calculate_raster_statistics(integer_raster_no_nodata, band_number=1, exclude_nodata=False)
        assert isinstance(result, dict)

    def test_standard_deviation_calculation(self, integer_raster_no_nodata):
        """Test standard deviation calculation accuracy."""
        result = calculate_raster_statistics(integer_raster_no_nodata)

        # For data 1-80, calculate expected standard deviation
        data = np.arange(1, 81)
        expected_std = np.std(data)

        assert abs(result['std'] - expected_std) < 0.1, f"Standard deviation should be approximately {expected_std}"

    def test_range_calculation(self, float_raster_with_nodata):
        """Test range calculation with nodata exclusion."""
        result = calculate_raster_statistics(float_raster_with_nodata, exclude_nodata=True)

        # Range should be max - min
        expected_range = result['max'] - result['min']
        assert abs(result['range'] - expected_range) < 0.001, "Range should equal max - min"

    def test_return_value_json_serializable(self, integer_raster_no_nodata):
        """Test that returned values are JSON serializable."""
        import json

        result = calculate_raster_statistics(integer_raster_no_nodata)

        # This should not raise an exception if all values are JSON serializable
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON serializable: {e}")

    def test_large_value_raster(self):
        """Test with raster containing large values to ensure no overflow."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        try:
            # Create data with large values
            width, height = 3, 3
            data = np.array([
                [1000000, 2000000, 3000000],
                [4000000, 5000000, 6000000],
                [7000000, 8000000, 9000000]
            ], dtype=np.int32)

            transform = from_bounds(0, 0, 3, 3, width, height)

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

            result = calculate_raster_statistics(temp_file.name)

            assert result['min'] == 1000000, "Should handle large values correctly"
            assert result['max'] == 9000000, "Should handle large values correctly"
            assert result['mean'] == 5000000, "Should calculate mean of large values correctly"

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    @pytest.mark.parametrize("exclude_nodata", [True, False])
    def test_exclude_nodata_parameter(self, float_raster_with_nodata, exclude_nodata):
        """Test exclude_nodata parameter with both True and False values."""
        result = calculate_raster_statistics(float_raster_with_nodata, exclude_nodata=exclude_nodata)

        # Should always return valid dictionary structure
        assert isinstance(result, dict)

        # Pixel counts should be consistent regardless of exclude_nodata setting
        assert result['total_pixels'] > 0
        assert result['nodata_pixels'] > 0  # This raster has nodata
        assert result['valid_pixels'] + result['nodata_pixels'] == result['total_pixels']

        if exclude_nodata:
            # When excluding nodata, min should not be the nodata value
            assert result['min'] != -9999.0
        else:
            # When including nodata, min should be the nodata value
            assert result['min'] == -9999.0

    def test_comprehensive_integration(self, float_raster_with_nodata):
        """Comprehensive integration test checking all aspects together."""
        result = calculate_raster_statistics(float_raster_with_nodata, band_number=1, exclude_nodata=True)

        # Verify all expected keys with correct types
        expected_structure = {
            'min': (type(None), int, float),
            'max': (type(None), int, float),
            'mean': (type(None), int, float),
            'median': (type(None), int, float),
            'std': (type(None), int, float),
            'range': (type(None), int, float),
            'percentile_25': (type(None), int, float),
            'percentile_75': (type(None), int, float),
            'valid_pixels': int,
            'total_pixels': int,
            'nodata_pixels': int
        }

        for key, expected_type in expected_structure.items():
            assert key in result, f"Missing key: {key}"
            if isinstance(expected_type, tuple):
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type: {type(result[key])}"
            else:
                assert isinstance(result[key], expected_type), f"Key {key} has wrong type: {type(result[key])}"

        # Verify logical relationships between statistics (when not None)
        if all(result[key] is not None for key in ['min', 'max', 'mean', 'median']):
            assert result['min'] <= result['mean'] <= result['max'], "Min <= Mean <= Max relationship should hold"
            assert result['min'] <= result['median'] <= result['max'], "Min <= Median <= Max relationship should hold"
            assert result['percentile_25'] <= result['median'] <= result['percentile_75'], "Percentile relationships should hold"

        # Verify pixel count relationships
        assert result['total_pixels'] > 0, "Total pixels should be positive"
        assert result['valid_pixels'] >= 0, "Valid pixels should be non-negative"
        assert result['nodata_pixels'] >= 0, "NoData pixels should be non-negative"
        assert result['valid_pixels'] + result['nodata_pixels'] == result['total_pixels'], "Pixel counts should sum correctly"
