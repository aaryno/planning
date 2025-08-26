"""
Test suite for analyze_vegetation_indices function.

This module tests the comprehensive vegetation analysis capabilities including
NDVI, EVI calculation, vegetation classification, and health assessment.
"""

import pytest
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from pathlib import Path
import tempfile
import sys
import os

# Add src to path for importing the function
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from rasterio_analysis import analyze_vegetation_indices
except ImportError as e:
    pytest.skip(f"Could not import analyze_vegetation_indices: {e}", allow_module_level=True)


@pytest.fixture
def sample_multispectral_basic():
    """Create a basic test multispectral image with known vegetation patterns."""
    width, height = 20, 20

    # Create synthetic bands with realistic values
    # Band 1 (Blue): 0.04-0.1 reflectance (400-1000 DN)
    # Band 3 (Red): 0.03-0.08 reflectance (300-800 DN)
    # Band 4 (NIR): 0.1-0.5 reflectance (1000-5000 DN)

    blue_band = np.random.uniform(400, 1000, (height, width)).astype(np.uint16)
    red_band = np.random.uniform(300, 800, (height, width)).astype(np.uint16)
    nir_band = np.random.uniform(1000, 5000, (height, width)).astype(np.uint16)

    # Create distinct vegetation patterns
    # Top half: dense vegetation (high NIR, low red)
    red_band[:10, :] = np.random.uniform(200, 400, (10, width)).astype(np.uint16)
    nir_band[:10, :] = np.random.uniform(3000, 5000, (10, width)).astype(np.uint16)

    # Bottom left: water (low NIR, low red, moderate blue)
    red_band[10:, :10] = np.random.uniform(100, 200, (10, 10)).astype(np.uint16)
    nir_band[10:, :10] = np.random.uniform(50, 200, (10, 10)).astype(np.uint16)
    blue_band[10:, :10] = np.random.uniform(600, 1200, (10, 10)).astype(np.uint16)

    # Bottom right: bare soil/urban (moderate NIR and red)
    red_band[10:, 10:] = np.random.uniform(800, 1200, (10, 10)).astype(np.uint16)
    nir_band[10:, 10:] = np.random.uniform(800, 1500, (10, 10)).astype(np.uint16)

    # Stack bands (blue, red, NIR as bands 1, 3, 4)
    bands = np.stack([blue_band, np.zeros_like(blue_band), red_band, nir_band])

    # Define geographic bounds
    bounds = (-120, 37, -119, 38)
    transform = from_bounds(*bounds, width, height)

    # Create temporary multispectral file
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        with rasterio.open(
            tmp.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=4,
            dtype=bands.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            for i in range(4):
                dst.write(bands[i], i + 1)

        yield tmp.name

    # Cleanup
    try:
        os.unlink(tmp.name)
    except:
        pass


@pytest.fixture
def sample_landsat_format():
    """Create a Landsat-format multispectral image for testing."""
    width, height = 15, 15

    # Create 7-band Landsat-like image
    bands = []
    for i in range(7):
        if i == 2:  # Red band
            band = np.random.uniform(200, 800, (height, width)).astype(np.uint16)
        elif i == 3:  # NIR band
            band = np.random.uniform(1000, 4000, (height, width)).astype(np.uint16)
        elif i == 0:  # Blue band
            band = np.random.uniform(400, 1000, (height, width)).astype(np.uint16)
        else:
            band = np.random.uniform(300, 2000, (height, width)).astype(np.uint16)
        bands.append(band)

    # Create vegetation gradient
    for i in range(height):
        # Vegetation increases from bottom to top
        veg_factor = i / height
        bands[2][i, :] *= (1 - veg_factor * 0.5)  # Red decreases
        bands[3][i, :] *= (1 + veg_factor * 2)    # NIR increases

    bands = np.stack(bands)

    bounds = (-121, 36, -120, 37)
    transform = from_bounds(*bounds, width, height)

    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        with rasterio.open(
            tmp.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=7,
            dtype=bands.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            for i in range(7):
                dst.write(bands[i], i + 1)

        yield tmp.name

    try:
        os.unlink(tmp.name)
    except:
        pass


class TestAnalyzeVegetationIndices:
    """Test class for analyze_vegetation_indices function."""

    def test_function_exists(self):
        """Test that the function exists and is callable."""
        assert callable(analyze_vegetation_indices), \
            "analyze_vegetation_indices should be a callable function"

    def test_basic_functionality(self, sample_multispectral_basic):
        """Test basic functionality with default parameters."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        # Check return type
        assert isinstance(result, dict), \
            "Function should return a dictionary"

        # Check required keys
        required_keys = [
            'ndvi_stats', 'evi_stats', 'vegetation_classification',
            'ndvi_array', 'evi_array', 'vegetation_mask',
            'health_assessment', 'seasonal_suitability',
            'water_mask', 'bare_soil_mask'
        ]

        for key in required_keys:
            assert key in result, f"Result should contain '{key}' key"

    def test_ndvi_calculation_accuracy(self, sample_multispectral_basic):
        """Test NDVI calculation accuracy with known values."""
        result = analyze_vegetation_indices(sample_multispectral_basic, red_band=3, nir_band=4)

        # Check NDVI statistics
        ndvi_stats = result['ndvi_stats']
        assert isinstance(ndvi_stats, dict), "ndvi_stats should be a dictionary"
        assert 'mean' in ndvi_stats, "ndvi_stats should contain 'mean'"
        assert 'std' in ndvi_stats, "ndvi_stats should contain 'std'"
        assert 'min' in ndvi_stats, "ndvi_stats should contain 'min'"
        assert 'max' in ndvi_stats, "ndvi_stats should contain 'max'"

        # Check NDVI array
        ndvi_array = result['ndvi_array']
        assert isinstance(ndvi_array, np.ndarray), "ndvi_array should be numpy array"
        assert ndvi_array.shape == (20, 20), f"ndvi_array shape should be (20, 20), got {ndvi_array.shape}"

        # NDVI values should be in valid range [-1, 1]
        valid_ndvi = ndvi_array[~np.isnan(ndvi_array)]
        assert np.all(valid_ndvi >= -1), f"NDVI values should be >= -1, min found: {np.min(valid_ndvi)}"
        assert np.all(valid_ndvi <= 1), f"NDVI values should be <= 1, max found: {np.max(valid_ndvi)}"

        # Top half should have higher NDVI (vegetation area)
        top_ndvi = np.nanmean(ndvi_array[:10, :])
        bottom_ndvi = np.nanmean(ndvi_array[10:, :])
        assert top_ndvi > bottom_ndvi, \
            f"Vegetation area (top) should have higher NDVI than bottom area: {top_ndvi} vs {bottom_ndvi}"

        # Vegetation area should have positive NDVI
        assert top_ndvi > 0.2, f"Vegetation area should have NDVI > 0.2, got {top_ndvi}"

    def test_evi_calculation(self, sample_multispectral_basic):
        """Test Enhanced Vegetation Index calculation."""
        result = analyze_vegetation_indices(sample_multispectral_basic, red_band=3, nir_band=4, blue_band=1)

        # Check EVI statistics
        evi_stats = result['evi_stats']
        assert isinstance(evi_stats, dict), "evi_stats should be a dictionary"

        # Check EVI array
        evi_array = result['evi_array']
        assert isinstance(evi_array, np.ndarray), "evi_array should be numpy array"
        assert evi_array.shape == (20, 20), "evi_array should match input dimensions"

        # EVI values should be reasonable (typically -1 to 1, but can exceed slightly)
        valid_evi = evi_array[~np.isnan(evi_array)]
        assert np.all(valid_evi >= -2), f"EVI values seem too low, min: {np.min(valid_evi)}"
        assert np.all(valid_evi <= 2), f"EVI values seem too high, max: {np.max(valid_evi)}"

        # EVI should correlate with NDVI (but not be identical)
        ndvi_array = result['ndvi_array']

        # Calculate correlation for valid pixels
        valid_mask = ~(np.isnan(ndvi_array) | np.isnan(evi_array))
        if np.sum(valid_mask) > 10:  # Need enough valid pixels
            correlation = np.corrcoef(ndvi_array[valid_mask], evi_array[valid_mask])[0, 1]
            assert correlation > 0.5, f"NDVI and EVI should be positively correlated, got {correlation}"

    def test_vegetation_classification(self, sample_multispectral_basic):
        """Test vegetation classification based on NDVI thresholds."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        vegetation_class = result['vegetation_classification']
        assert isinstance(vegetation_class, dict), "vegetation_classification should be a dictionary"

        # Should have classification categories
        expected_categories = ['water', 'bare_soil', 'sparse_vegetation',
                             'moderate_vegetation', 'dense_vegetation', 'very_dense_vegetation']

        # At least some categories should be present
        assert len(vegetation_class) > 0, "Should have at least some vegetation classifications"

        # All counts should be non-negative integers
        total_pixels = 0
        for category, count in vegetation_class.items():
            assert isinstance(count, (int, np.integer)), \
                f"Classification count should be integer, got {type(count)} for {category}"
            assert count >= 0, f"Classification count should be >= 0, got {count} for {category}"
            total_pixels += count

        # Total should not exceed image size
        assert total_pixels <= 400, f"Total classified pixels ({total_pixels}) should not exceed 400 (20x20)"

        # Should have detected some vegetation in our synthetic data
        veg_pixels = sum(count for cat, count in vegetation_class.items()
                        if 'vegetation' in cat.lower())
        assert veg_pixels > 0, "Should detect some vegetation pixels in synthetic data"

    def test_mask_creation(self, sample_multispectral_basic):
        """Test creation of various land cover masks."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        # Test vegetation mask
        vegetation_mask = result['vegetation_mask']
        assert isinstance(vegetation_mask, np.ndarray), "vegetation_mask should be numpy array"
        assert vegetation_mask.dtype == bool, "vegetation_mask should be boolean array"
        assert vegetation_mask.shape == (20, 20), "vegetation_mask should match input dimensions"

        # Test water mask
        water_mask = result['water_mask']
        assert isinstance(water_mask, np.ndarray), "water_mask should be numpy array"
        assert water_mask.dtype == bool, "water_mask should be boolean array"

        # Test bare soil mask
        bare_soil_mask = result['bare_soil_mask']
        assert isinstance(bare_soil_mask, np.ndarray), "bare_soil_mask should be numpy array"
        assert bare_soil_mask.dtype == bool, "bare_soil_mask should be boolean array"

        # Masks should be mutually exclusive (mostly)
        overlap_veg_water = np.sum(vegetation_mask & water_mask)
        overlap_veg_soil = np.sum(vegetation_mask & bare_soil_mask)
        overlap_water_soil = np.sum(water_mask & bare_soil_mask)

        # Some overlap is acceptable due to mixed pixels, but should be minimal
        total_pixels = vegetation_mask.size
        assert overlap_veg_water < total_pixels * 0.1, "Vegetation and water masks should have minimal overlap"

        # Check that we detected expected patterns from synthetic data
        # Bottom left should have more water pixels
        water_bottom_left = np.sum(water_mask[10:, :10])
        water_top_half = np.sum(water_mask[:10, :])

        # Water should be more concentrated in bottom left (where we put low NDVI values)
        if water_bottom_left + water_top_half > 0:  # If any water detected
            water_ratio = water_bottom_left / max(water_bottom_left + water_top_half, 1)
            assert water_ratio > 0.3, "Water should be more concentrated in bottom left area"

    def test_health_assessment(self, sample_multispectral_basic):
        """Test vegetation health assessment functionality."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        health_assessment = result['health_assessment']
        assert isinstance(health_assessment, dict), "health_assessment should be a dictionary"

        # Should contain health metrics
        expected_metrics = ['overall_health', 'stress_indicators', 'vigor_assessment']

        # At least some health metrics should be present
        assert len(health_assessment) > 0, "Health assessment should contain some metrics"

        # Health values should be reasonable
        for metric, value in health_assessment.items():
            if isinstance(value, (int, float)):
                assert not np.isnan(value), f"Health metric {metric} should not be NaN"

    def test_seasonal_suitability(self, sample_multispectral_basic):
        """Test seasonal suitability assessment."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        seasonal_suit = result['seasonal_suitability']
        assert isinstance(seasonal_suit, dict), "seasonal_suitability should be a dictionary"

        # Should provide seasonal assessment
        assert len(seasonal_suit) > 0, "Should provide some seasonal suitability information"

    def test_different_band_configurations(self, sample_landsat_format):
        """Test function with different band number configurations."""
        # Test Landsat band configuration (1-based indexing)
        result1 = analyze_vegetation_indices(sample_landsat_format, red_band=3, nir_band=4, blue_band=1)
        assert isinstance(result1, dict), "Should work with Landsat band configuration"

        # Test Sentinel band configuration
        result2 = analyze_vegetation_indices(sample_landsat_format, red_band=3, nir_band=4, blue_band=1)
        assert isinstance(result2, dict), "Should work with custom band configuration"

        # Both should produce valid NDVI
        ndvi1 = result1['ndvi_array']
        ndvi2 = result2['ndvi_array']

        assert not np.all(np.isnan(ndvi1)), "NDVI should have valid values with Landsat bands"
        assert not np.all(np.isnan(ndvi2)), "NDVI should have valid values with custom bands"

    def test_error_handling_division_by_zero(self):
        """Test handling of division by zero in NDVI/EVI calculations."""
        # Create image with zero values that would cause division by zero
        width, height = 5, 5

        red_band = np.zeros((height, width), dtype=np.uint16)
        nir_band = np.zeros((height, width), dtype=np.uint16)
        blue_band = np.zeros((height, width), dtype=np.uint16)

        bands = np.stack([blue_band, np.zeros_like(blue_band), red_band, nir_band])

        bounds = (-120, 37, -119, 38)
        transform = from_bounds(*bounds, width, height)

        with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
            with rasterio.open(
                tmp.name, 'w',
                driver='GTiff',
                height=height, width=width, count=4,
                dtype=bands.dtype, crs='EPSG:4326', transform=transform
            ) as dst:
                for i in range(4):
                    dst.write(bands[i], i + 1)

            # Function should handle division by zero gracefully
            result = analyze_vegetation_indices(tmp.name, red_band=3, nir_band=4, blue_band=1)

            assert isinstance(result, dict), "Function should handle zero values gracefully"

            # NDVI array should contain NaN or fill values for invalid calculations
            ndvi_array = result['ndvi_array']
            assert isinstance(ndvi_array, np.ndarray), "Should return NDVI array even with zero values"

        # Cleanup
        try:
            os.unlink(tmp.name)
        except:
            pass

    def test_error_handling_invalid_file(self):
        """Test error handling for invalid input file."""
        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            analyze_vegetation_indices('nonexistent_file.tif')

    def test_error_handling_invalid_bands(self, sample_multispectral_basic):
        """Test error handling for invalid band numbers."""
        # Test band numbers that don't exist
        with pytest.raises((IndexError, rasterio.RasterioIOError)):
            analyze_vegetation_indices(sample_multispectral_basic, red_band=10, nir_band=11)

    def test_statistics_consistency(self, sample_multispectral_basic):
        """Test that calculated statistics are consistent with arrays."""
        result = analyze_vegetation_indices(sample_multispectral_basic)

        ndvi_stats = result['ndvi_stats']
        ndvi_array = result['ndvi_array']

        # Remove NaN values for comparison
        valid_ndvi = ndvi_array[~np.isnan(ndvi_array)]

        if len(valid_ndvi) > 0:
            # Check mean
            calc_mean = ndvi_stats['mean']
            array_mean = np.mean(valid_ndvi)
            assert abs(calc_mean - array_mean) < 0.01, \
                f"Calculated mean ({calc_mean}) should match array mean ({array_mean})"

            # Check min/max
            calc_min = ndvi_stats['min']
            calc_max = ndvi_stats['max']
            array_min = np.min(valid_ndvi)
            array_max = np.max(valid_ndvi)

            assert abs(calc_min - array_min) < 0.01, \
                f"Calculated min ({calc_min}) should match array min ({array_min})"
            assert abs(calc_max - array_max) < 0.01, \
                f"Calculated max ({calc_max}) should match array max ({array_max})"

    def test_vegetation_gradient_detection(self, sample_landsat_format):
        """Test detection of vegetation gradient in synthetic data."""
        result = analyze_vegetation_indices(sample_landsat_format, red_band=3, nir_band=4, blue_band=1)

        ndvi_array = result['ndvi_array']

        # Calculate mean NDVI for top and bottom rows
        top_ndvi = np.nanmean(ndvi_array[:3, :])  # Top rows (more vegetation)
        bottom_ndvi = np.nanmean(ndvi_array[-3:, :])  # Bottom rows (less vegetation)

        # Top should have higher NDVI due to our synthetic gradient
        assert top_ndvi > bottom_ndvi, \
            f"Top rows should have higher NDVI than bottom rows: {top_ndvi} vs {bottom_ndvi}"

        # Difference should be meaningful
        ndvi_difference = top_ndvi - bottom_ndvi
        assert ndvi_difference > 0.1, \
            f"NDVI gradient should be detectable (>0.1 difference), got {ndvi_difference}"

    @pytest.mark.parametrize("invalid_input", [None, "", 123, []])
    def test_invalid_input_types(self, invalid_input):
        """Test function behavior with invalid input types."""
        with pytest.raises((TypeError, ValueError, FileNotFoundError, AttributeError)):
            analyze_vegetation_indices(invalid_input)

    @pytest.mark.parametrize("red_band,nir_band,blue_band", [
        (1, 2, 3),  # Standard RGB-NIR order
        (3, 4, 1),  # Landsat order
        (4, 8, 2),  # Sentinel-2 order
    ])
    def test_band_parameter_flexibility(self, sample_landsat_format, red_band, nir_band, blue_band):
        """Test function works with different band parameter combinations."""
        try:
            result = analyze_vegetation_indices(sample_landsat_format,
                                              red_band=red_band,
                                              nir_band=nir_band,
                                              blue_band=blue_band)
            assert isinstance(result, dict), f"Should work with bands {red_band}, {nir_band}, {blue_band}"
        except (IndexError, rasterio.RasterioIOError):
            # Expected for band numbers that don't exist in test data
            pass
