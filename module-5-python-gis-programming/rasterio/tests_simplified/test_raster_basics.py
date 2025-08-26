"""
Tests for Raster Basics Functions

This file tests the basic raster reading functions you'll implement.
Each test is simple and checks one specific thing about your function.

Don't worry about understanding all the test code - focus on making
your functions return the right values!

Author: Instructor
Course: GIST 604B - Open Source GIS Programming
"""

import pytest
import rasterio
import numpy as np
from pathlib import Path
import tempfile
import os

# Import the functions you need to implement
try:
    from src.rasterio_analysis.raster_basics import (
        read_raster_info,
        get_raster_stats,
        get_raster_extent
    )
except ImportError as e:
    pytest.skip(f"Could not import your functions: {e}", allow_module_level=True)


class TestRasterBasics:
    """Tests for your raster basics functions."""

    @pytest.fixture(scope="class")
    def sample_raster_path(self):
        """Create a simple test raster file for testing."""
        # Create a temporary raster file for testing
        temp_dir = tempfile.mkdtemp()
        raster_path = os.path.join(temp_dir, "test_raster.tif")

        # Create simple test data: 10x10 raster with elevation values
        width, height = 10, 10
        test_data = np.arange(100, dtype=np.float32).reshape(height, width)

        # Add some nodata values for testing
        test_data[0, 0] = -9999  # This will be our nodata value
        test_data[9, 9] = -9999

        # Define the geographic extent (a small area)
        transform = rasterio.transform.from_bounds(
            -120.0, 35.0, -119.0, 36.0,  # left, bottom, right, top
            width, height
        )

        # Create the raster file
        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,  # One band
            dtype=test_data.dtype,
            crs='EPSG:4326',  # WGS84 geographic coordinates
            transform=transform,
            nodata=-9999
        ) as dst:
            dst.write(test_data, 1)

        return raster_path

    def test_read_raster_info_basic(self, sample_raster_path):
        """
        Test that read_raster_info() returns the basic raster information.

        Your function should return a dictionary with these keys:
        - width, height, count, crs, driver
        """
        # Call your function
        result = read_raster_info(sample_raster_path)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['width', 'height', 'count', 'crs', 'driver']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check that the values are correct
        assert result['width'] == 10, "Width should be 10 pixels"
        assert result['height'] == 10, "Height should be 10 pixels"
        assert result['count'] == 1, "Should have 1 band"
        assert 'EPSG:4326' in str(result['crs']), "CRS should be EPSG:4326"
        assert result['driver'] == 'GTiff', "Driver should be GTiff"

    def test_read_raster_info_file_not_found(self):
        """Test that your function handles missing files properly."""
        with pytest.raises(Exception):
            read_raster_info("nonexistent_file.tif")

    def test_get_raster_stats_basic(self, sample_raster_path):
        """
        Test that get_raster_stats() calculates statistics correctly.

        Your function should return a dictionary with these keys:
        - min, max, mean, std, nodata_count
        """
        # Call your function
        result = get_raster_stats(sample_raster_path, band_number=1)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['min', 'max', 'mean', 'std', 'nodata_count']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check that the values make sense
        # Our test data goes from 0 to 99, but with 2 nodata values (-9999)
        assert result['min'] == 1.0, "Min should be 1 (excluding nodata)"
        assert result['max'] == 98.0, "Max should be 98 (excluding nodata)"
        assert 45 < result['mean'] < 55, f"Mean should be around 49.5, got {result['mean']}"
        assert result['std'] > 0, "Standard deviation should be positive"
        assert result['nodata_count'] == 2, "Should find 2 nodata pixels"

    def test_get_raster_stats_different_bands(self, sample_raster_path):
        """Test that the band_number parameter works."""
        # This should work fine
        result = get_raster_stats(sample_raster_path, band_number=1)
        assert result is not None

        # This should fail because there's only 1 band
        with pytest.raises(Exception):
            get_raster_stats(sample_raster_path, band_number=2)

    def test_get_raster_extent_basic(self, sample_raster_path):
        """
        Test that get_raster_extent() returns the correct geographic extent.

        Your function should return a dictionary with these keys:
        - left, bottom, right, top, width, height
        """
        # Call your function
        result = get_raster_extent(sample_raster_path)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['left', 'bottom', 'right', 'top', 'width', 'height']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check that the values are correct (we set these when creating the test raster)
        assert result['left'] == -120.0, "Left boundary should be -120.0"
        assert result['bottom'] == 35.0, "Bottom boundary should be 35.0"
        assert result['right'] == -119.0, "Right boundary should be -119.0"
        assert result['top'] == 36.0, "Top boundary should be 36.0"
        assert result['width'] == 1.0, "Width should be 1.0 degrees"
        assert result['height'] == 1.0, "Height should be 1.0 degrees"

    def test_get_raster_extent_consistent(self, sample_raster_path):
        """Test that width and height are calculated correctly."""
        result = get_raster_extent(sample_raster_path)

        # Width should equal right minus left
        expected_width = result['right'] - result['left']
        assert abs(result['width'] - expected_width) < 0.000001, \
            "Width should equal right - left"

        # Height should equal top minus bottom
        expected_height = result['top'] - result['bottom']
        assert abs(result['height'] - expected_height) < 0.000001, \
            "Height should equal top - bottom"

    def test_all_functions_work_together(self, sample_raster_path):
        """
        Test that all three functions work with the same file.
        This simulates how you might use them together in real work.
        """
        # Get basic info
        info = read_raster_info(sample_raster_path)
        assert info['width'] == 10
        assert info['height'] == 10

        # Get statistics
        stats = get_raster_stats(sample_raster_path)
        assert stats['min'] is not None
        assert stats['max'] is not None

        # Get extent
        extent = get_raster_extent(sample_raster_path)
        assert extent['left'] < extent['right']
        assert extent['bottom'] < extent['top']

        print("✅ All functions work together correctly!")


# Helpful test runner for students
if __name__ == "__main__":
    print("Running basic tests for your raster functions...")
    print("If you see errors, check your function implementations!")
    print()

    # You can run just this file to test your functions
    pytest.main([__file__, "-v"])
