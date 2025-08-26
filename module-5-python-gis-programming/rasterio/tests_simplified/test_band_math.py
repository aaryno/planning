"""
Tests for Band Math Functions

This file tests the NDVI and vegetation analysis functions you'll implement.
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
    from src.rasterio_analysis.band_math import (
        calculate_ndvi,
        analyze_vegetation
    )
except ImportError as e:
    pytest.skip(f"Could not import your functions: {e}", allow_module_level=True)


class TestBandMath:
    """Tests for your band math functions."""

    @pytest.fixture(scope="class")
    def multiband_raster_path(self):
        """Create a simple multi-band test raster for NDVI testing."""
        temp_dir = tempfile.mkdtemp()
        raster_path = os.path.join(temp_dir, "test_multiband.tif")

        # Create simple test data: 10x10 raster with 4 bands
        width, height = 10, 10

        # Create realistic band data
        # Band 1: Blue (not used in NDVI)
        blue_data = np.full((height, width), 50, dtype=np.float32)

        # Band 2: Green (not used in NDVI)
        green_data = np.full((height, width), 75, dtype=np.float32)

        # Band 3: Red (used in NDVI)
        red_data = np.full((height, width), 100, dtype=np.float32)

        # Band 4: Near-Infrared (used in NDVI)
        # Make it higher than red to simulate vegetation
        nir_data = np.full((height, width), 200, dtype=np.float32)

        # Add some variation to make it realistic
        for i in range(height):
            for j in range(width):
                # Create different vegetation types in different areas
                if i < 3:  # Dense vegetation area
                    red_data[i, j] = 80 + np.random.uniform(-10, 10)
                    nir_data[i, j] = 240 + np.random.uniform(-20, 20)
                elif i < 6:  # Moderate vegetation
                    red_data[i, j] = 120 + np.random.uniform(-10, 10)
                    nir_data[i, j] = 180 + np.random.uniform(-20, 20)
                else:  # Sparse/no vegetation
                    red_data[i, j] = 140 + np.random.uniform(-10, 10)
                    nir_data[i, j] = 120 + np.random.uniform(-20, 20)

        # Add some nodata pixels
        red_data[0, 0] = -9999
        nir_data[0, 0] = -9999

        # Stack all bands
        all_bands = np.stack([blue_data, green_data, red_data, nir_data])

        # Define the geographic extent
        transform = rasterio.transform.from_bounds(
            -120.0, 35.0, -119.0, 36.0,
            width, height
        )

        # Create the multi-band raster file
        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=4,  # Four bands
            dtype=all_bands.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=-9999
        ) as dst:
            for band_num in range(4):
                dst.write(all_bands[band_num], band_num + 1)

        return raster_path

    @pytest.fixture
    def sample_ndvi_array(self):
        """Create a sample NDVI array for testing vegetation analysis."""
        # Create 10x10 NDVI array with different vegetation types
        ndvi = np.full((10, 10), np.nan, dtype=np.float32)

        # Water/clouds (NDVI < 0)
        ndvi[0:2, 0:2] = -0.2

        # Non-vegetation (0 <= NDVI < 0.2)
        ndvi[0:2, 2:4] = 0.1

        # Sparse vegetation (0.2 <= NDVI < 0.4)
        ndvi[2:4, 0:4] = 0.3

        # Moderate vegetation (0.4 <= NDVI < 0.7)
        ndvi[4:7, 0:5] = 0.55

        # Dense vegetation (NDVI >= 0.7)
        ndvi[7:10, 0:3] = 0.8

        # Leave some NaN values for nodata
        ndvi[0, 0] = np.nan
        ndvi[9, 9] = np.nan

        return ndvi

    def test_calculate_ndvi_basic(self, multiband_raster_path):
        """
        Test that calculate_ndvi() computes NDVI correctly.

        Your function should return a dictionary with NDVI results.
        """
        # Call your function
        result = calculate_ndvi(multiband_raster_path, red_band=3, nir_band=4)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['ndvi_array', 'min_ndvi', 'max_ndvi', 'mean_ndvi',
                        'vegetation_pixels', 'total_pixels']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check the NDVI array
        ndvi_array = result['ndvi_array']
        assert isinstance(ndvi_array, np.ndarray), "NDVI array should be a numpy array"
        assert ndvi_array.shape == (10, 10), "NDVI array should be 10x10"

        # Check that NDVI values are in valid range (-1 to 1)
        valid_ndvi = ndvi_array[~np.isnan(ndvi_array)]
        assert np.all(valid_ndvi >= -1), "NDVI values should be >= -1"
        assert np.all(valid_ndvi <= 1), "NDVI values should be <= 1"

        # Check statistics make sense
        assert result['min_ndvi'] is not None, "Should calculate min NDVI"
        assert result['max_ndvi'] is not None, "Should calculate max NDVI"
        assert result['mean_ndvi'] is not None, "Should calculate mean NDVI"
        assert result['min_ndvi'] <= result['max_ndvi'], "Min should be <= Max"

    def test_calculate_ndvi_formula(self, multiband_raster_path):
        """Test that NDVI is calculated using the correct formula."""
        result = calculate_ndvi(multiband_raster_path, red_band=3, nir_band=4)

        # For our test data, we can verify the formula manually
        # We know dense vegetation areas should have high NDVI
        # and sparse vegetation areas should have low NDVI
        ndvi_array = result['ndvi_array']

        # Check that we get reasonable NDVI values
        # (The exact values depend on our test data)
        assert result['mean_ndvi'] > 0, "Mean NDVI should be positive for vegetated area"
        assert result['max_ndvi'] > 0.3, "Should have some areas with decent vegetation"

    def test_calculate_ndvi_handles_nodata(self, multiband_raster_path):
        """Test that calculate_ndvi() properly handles nodata values."""
        result = calculate_ndvi(multiband_raster_path, red_band=3, nir_band=4)

        # Should handle nodata pixels properly
        ndvi_array = result['ndvi_array']

        # Check that nodata pixels become NaN in NDVI
        assert np.isnan(ndvi_array[0, 0]), "Nodata pixels should become NaN in NDVI"

        # Check counts
        assert result['total_pixels'] < 100, "Should exclude nodata pixels from total count"

    def test_calculate_ndvi_invalid_bands(self, multiband_raster_path):
        """Test that calculate_ndvi() handles invalid band numbers properly."""
        # Try to use a band that doesn't exist
        with pytest.raises(ValueError):
            calculate_ndvi(multiband_raster_path, red_band=3, nir_band=10)

    def test_analyze_vegetation_basic(self, sample_ndvi_array):
        """
        Test that analyze_vegetation() classifies NDVI values correctly.

        Your function should return a dictionary with vegetation classifications.
        """
        # Call your function
        result = analyze_vegetation(sample_ndvi_array)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['water_clouds', 'non_vegetation', 'sparse_vegetation',
                        'moderate_vegetation', 'dense_vegetation', 'total_valid_pixels']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check that each category has 'pixels' and 'percent' keys
        categories = ['water_clouds', 'non_vegetation', 'sparse_vegetation',
                     'moderate_vegetation', 'dense_vegetation']
        for category in categories:
            assert 'pixels' in result[category], f"{category} should have 'pixels' key"
            assert 'percent' in result[category], f"{category} should have 'percent' key"
            assert isinstance(result[category]['pixels'], int), f"{category} pixels should be integer"
            assert isinstance(result[category]['percent'], (int, float)), f"{category} percent should be numeric"

    def test_analyze_vegetation_classification(self, sample_ndvi_array):
        """Test that vegetation classification uses correct thresholds."""
        result = analyze_vegetation(sample_ndvi_array)

        # Based on our sample data, we should have pixels in each category
        assert result['water_clouds']['pixels'] > 0, "Should find some water/cloud pixels (NDVI < 0)"
        assert result['non_vegetation']['pixels'] > 0, "Should find some non-vegetation pixels"
        assert result['sparse_vegetation']['pixels'] > 0, "Should find some sparse vegetation pixels"
        assert result['moderate_vegetation']['pixels'] > 0, "Should find some moderate vegetation pixels"
        assert result['dense_vegetation']['pixels'] > 0, "Should find some dense vegetation pixels"

        # Check that percentages add up to approximately 100%
        total_percent = sum([result[cat]['percent'] for cat in
                           ['water_clouds', 'non_vegetation', 'sparse_vegetation',
                            'moderate_vegetation', 'dense_vegetation']])
        assert 99 <= total_percent <= 101, f"Percentages should add up to ~100%, got {total_percent}"

    def test_analyze_vegetation_handles_nan(self):
        """Test that analyze_vegetation() properly handles NaN values."""
        # Create array with only NaN values
        nan_array = np.full((5, 5), np.nan)

        result = analyze_vegetation(nan_array)

        # Should handle all-NaN array gracefully
        assert result['total_valid_pixels'] == 0, "Should report 0 valid pixels for all-NaN array"

        # All categories should have 0 pixels
        categories = ['water_clouds', 'non_vegetation', 'sparse_vegetation',
                     'moderate_vegetation', 'dense_vegetation']
        for category in categories:
            assert result[category]['pixels'] == 0, f"{category} should have 0 pixels for all-NaN array"

    def test_analyze_vegetation_array_output(self, sample_ndvi_array):
        """Test that analyze_vegetation() returns a classification array."""
        result = analyze_vegetation(sample_ndvi_array)

        # Check for classification array
        if 'classification_array' in result:
            class_array = result['classification_array']
            assert isinstance(class_array, np.ndarray), "Classification array should be numpy array"
            assert class_array.shape == sample_ndvi_array.shape, "Classification should have same shape as input"

    def test_functions_work_together(self, multiband_raster_path):
        """
        Test that calculate_ndvi() and analyze_vegetation() work together.
        This simulates the typical workflow.
        """
        # Step 1: Calculate NDVI
        ndvi_result = calculate_ndvi(multiband_raster_path)
        assert ndvi_result['ndvi_array'] is not None

        # Step 2: Analyze vegetation using the NDVI array
        veg_analysis = analyze_vegetation(ndvi_result['ndvi_array'])
        assert veg_analysis['total_valid_pixels'] > 0

        print("✅ NDVI calculation and vegetation analysis work together!")

    def test_realistic_ndvi_values(self, multiband_raster_path):
        """Test that NDVI values are realistic for the test data."""
        result = calculate_ndvi(multiband_raster_path)

        # Our test data should produce reasonable NDVI values
        # (We designed it with vegetation in mind)
        assert -0.5 < result['min_ndvi'] < 1.0, "Min NDVI should be reasonable"
        assert -0.5 < result['max_ndvi'] < 1.0, "Max NDVI should be reasonable"
        assert -0.5 < result['mean_ndvi'] < 1.0, "Mean NDVI should be reasonable"


# Helpful test runner for students
if __name__ == "__main__":
    print("Running tests for your band math functions...")
    print("If you see errors, check your function implementations!")
    print()

    # You can run just this file to test your functions
    pytest.main([__file__, "-v"])
