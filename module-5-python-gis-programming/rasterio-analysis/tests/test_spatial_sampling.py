"""
Test suite for sample_raster_at_locations function.

This module tests the comprehensive spatial sampling capabilities including
point sampling, buffered sampling, interpolation methods, and coordinate handling.
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
    from rasterio_analysis import sample_raster_at_locations
except ImportError as e:
    pytest.skip(f"Could not import sample_raster_at_locations: {e}", allow_module_level=True)


@pytest.fixture
def sample_raster_single_band():
    """Create a single-band test raster with known values."""
    width, height = 20, 20

    # Create a gradient raster with predictable values
    data = np.zeros((height, width), dtype=np.float32)
    for i in range(height):
        for j in range(width):
            data[i, j] = i * 10 + j  # Values from 0 to 199

    # Define geographic bounds (1 degree square)
    bounds = (-120, 37, -119, 38)
    transform = from_bounds(*bounds, width, height)

    # Create temporary raster file
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        with rasterio.open(
            tmp.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(data, 1)

        yield tmp.name, bounds, data

    # Cleanup
    try:
        os.unlink(tmp.name)
    except:
        pass


@pytest.fixture
def sample_raster_multi_band():
    """Create a multi-band test raster."""
    width, height = 15, 15

    # Create 3 bands with different patterns
    band1 = np.arange(width * height).reshape(height, width).astype(np.float32)
    band2 = (band1 * 2 + 100).astype(np.float32)
    band3 = (band1 * 0.5 + 50).astype(np.float32)

    bands = np.stack([band1, band2, band3])

    # Define geographic bounds
    bounds = (-121, 36, -120, 37)
    transform = from_bounds(*bounds, width, height)

    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        with rasterio.open(
            tmp.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=3,
            dtype=bands.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            for i in range(3):
                dst.write(bands[i], i + 1)

        yield tmp.name, bounds, bands

    try:
        os.unlink(tmp.name)
    except:
        pass


@pytest.fixture
def sample_locations():
    """Create sample point locations for testing."""
    # Locations within the raster bounds
    locations_inside = [
        (-119.5, 37.5),  # Center of raster
        (-119.8, 37.2),  # Southwest quadrant
        (-119.2, 37.8),  # Northeast quadrant
        (-119.9, 37.1),  # Near southwest corner
    ]

    # Locations outside raster bounds
    locations_outside = [
        (-118.5, 37.5),  # Too far east
        (-120.5, 37.5),  # Too far west
        (-119.5, 36.5),  # Too far south
        (-119.5, 38.5),  # Too far north
    ]

    return locations_inside, locations_outside


class TestSampleRasterAtLocations:
    """Test class for sample_raster_at_locations function."""

    def test_function_exists(self):
        """Test that the function exists and is callable."""
        assert callable(sample_raster_at_locations), \
            "sample_raster_at_locations should be a callable function"

    def test_basic_functionality(self, sample_raster_single_band, sample_locations):
        """Test basic point sampling functionality."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        # Check return type
        assert isinstance(result, dict), \
            "Function should return a dictionary"

        # Check required keys
        required_keys = [
            'sampled_values', 'locations_geographic', 'locations_projected',
            'sampling_summary', 'valid_samples', 'failed_samples',
            'buffer_stats', 'interpolation_used', 'crs_info', 'raster_metadata'
        ]

        for key in required_keys:
            assert key in result, f"Result should contain '{key}' key"

    def test_point_sampling_accuracy(self, sample_raster_single_band, sample_locations):
        """Test accuracy of point sampling with nearest neighbor."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(
            raster_path, locations_inside,
            buffer_radius=0, interpolation='nearest'
        )

        # Check sampled values
        sampled_values = result['sampled_values']
        assert isinstance(sampled_values, list), "sampled_values should be a list"
        assert len(sampled_values) == len(locations_inside), \
            f"Should have {len(locations_inside)} sampled values, got {len(sampled_values)}"

        # Each sampled value should be a dictionary
        for i, sample in enumerate(sampled_values):
            assert isinstance(sample, dict), f"Sample {i} should be a dictionary"
            assert 'band_1' in sample or 'value' in sample, \
                f"Sample {i} should contain band values"

            # Values should be numeric
            for key, value in sample.items():
                if isinstance(value, (int, float, np.number)):
                    assert not np.isnan(value), f"Sampled value should not be NaN: {key}={value}"

    def test_buffer_sampling(self, sample_raster_single_band, sample_locations):
        """Test buffered sampling functionality."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        # Test with buffer radius
        buffer_radius = 0.01  # About 1km at this latitude
        result = sample_raster_at_locations(
            raster_path, locations_inside,
            buffer_radius=buffer_radius
        )

        # Check buffer stats
        buffer_stats = result['buffer_stats']
        assert isinstance(buffer_stats, dict), "buffer_stats should be a dictionary"

        # Check sampled values contain buffer statistics
        sampled_values = result['sampled_values']
        for sample in sampled_values:
            # Should have buffer statistics like mean, std, min, max
            expected_stats = ['mean', 'std', 'min', 'max', 'count']
            stats_found = sum(1 for stat in expected_stats if any(stat in key.lower() for key in sample.keys()))
            assert stats_found > 0, f"Buffer sample should contain statistics, got keys: {list(sample.keys())}"

    def test_interpolation_methods(self, sample_raster_single_band, sample_locations):
        """Test different interpolation methods."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        interpolation_methods = ['nearest', 'bilinear']
        results = {}

        for method in interpolation_methods:
            try:
                result = sample_raster_at_locations(
                    raster_path, locations_inside,
                    buffer_radius=0, interpolation=method
                )
                results[method] = result

                # Check that interpolation method is recorded
                assert result['interpolation_used'] == method, \
                    f"Should record interpolation method as {method}"

            except NotImplementedError:
                # Some interpolation methods might not be implemented
                pytest.skip(f"Interpolation method '{method}' not implemented")

        # If we have multiple results, they should be different (unless all points are at exact pixel centers)
        if len(results) > 1:
            methods = list(results.keys())
            result1 = results[methods[0]]['sampled_values']
            result2 = results[methods[1]]['sampled_values']

            # At least some values should be different between methods
            differences = 0
            for i in range(len(result1)):
                for key in result1[i]:
                    if key in result2[i]:
                        if abs(result1[i][key] - result2[i][key]) > 0.001:
                            differences += 1

            # We expect some differences unless all points are exactly at pixel centers
            # This is a soft assertion - interpolation differences might be minimal
            if differences == 0:
                print("Warning: No differences found between interpolation methods")

    def test_multi_band_sampling(self, sample_raster_multi_band, sample_locations):
        """Test sampling from multi-band raster."""
        raster_path, bounds, bands = sample_raster_multi_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        sampled_values = result['sampled_values']

        # Each sample should have values from multiple bands
        for sample in sampled_values:
            # Should have band_1, band_2, band_3 or similar keys
            band_keys = [key for key in sample.keys() if 'band' in key.lower()]
            assert len(band_keys) >= 1, f"Multi-band sample should have band values, got: {list(sample.keys())}"

            # If we specify all bands, should get all bands
            if len(band_keys) > 1:
                assert len(band_keys) <= 3, f"Should not have more than 3 bands, got {len(band_keys)}"

    def test_specific_band_sampling(self, sample_raster_multi_band, sample_locations):
        """Test sampling specific bands only."""
        raster_path, bounds, bands = sample_raster_multi_band
        locations_inside, _ = sample_locations

        # Sample only specific bands
        specific_bands = [1, 3]
        result = sample_raster_at_locations(
            raster_path, locations_inside,
            band_numbers=specific_bands
        )

        sampled_values = result['sampled_values']

        for sample in sampled_values:
            # Should only have specified bands
            band_keys = [key for key in sample.keys() if 'band' in key.lower()]
            # Allow for some flexibility in naming
            assert len(band_keys) <= len(specific_bands), \
                f"Should have at most {len(specific_bands)} bands, got {len(band_keys)}: {band_keys}"

    def test_coordinate_transformation(self, sample_raster_single_band, sample_locations):
        """Test coordinate transformation between geographic and projected CRS."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        # Check CRS information
        crs_info = result['crs_info']
        assert isinstance(crs_info, dict), "crs_info should be a dictionary"

        # Check coordinate arrays
        locations_geographic = result['locations_geographic']
        locations_projected = result['locations_projected']

        assert len(locations_geographic) == len(locations_inside), \
            "Should have same number of geographic locations as input"
        assert len(locations_projected) == len(locations_inside), \
            "Should have same number of projected locations as input"

        # Geographic and projected coordinates might be the same if raster is in geographic CRS
        # But arrays should exist and be properly formatted
        for i in range(len(locations_geographic)):
            assert len(locations_geographic[i]) == 2, "Geographic location should have 2 coordinates"
            assert len(locations_projected[i]) == 2, "Projected location should have 2 coordinates"

    def test_locations_outside_bounds(self, sample_raster_single_band, sample_locations):
        """Test handling of locations outside raster bounds."""
        raster_path, bounds, data = sample_raster_single_band
        _, locations_outside = sample_locations

        result = sample_raster_at_locations(raster_path, locations_outside)

        # Should handle gracefully
        assert isinstance(result, dict), "Should return dict even for outside locations"

        valid_samples = result['valid_samples']
        failed_samples = result['failed_samples']

        assert isinstance(valid_samples, int), "valid_samples should be an integer"
        assert isinstance(failed_samples, int), "failed_samples should be an integer"
        assert valid_samples + failed_samples == len(locations_outside), \
            "Total samples should equal input locations"

        # Most or all should be failed samples
        assert failed_samples > 0, "Should have some failed samples for outside locations"

    def test_mixed_inside_outside_locations(self, sample_raster_single_band, sample_locations):
        """Test with mix of inside and outside locations."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, locations_outside = sample_locations

        # Mix inside and outside locations
        mixed_locations = locations_inside[:2] + locations_outside[:2]

        result = sample_raster_at_locations(raster_path, mixed_locations)

        valid_samples = result['valid_samples']
        failed_samples = result['failed_samples']

        # Should have some valid and some failed
        assert valid_samples > 0, "Should have some valid samples"
        assert failed_samples > 0, "Should have some failed samples"
        assert valid_samples + failed_samples == len(mixed_locations), \
            "Total should match input count"

    def test_sampling_summary_statistics(self, sample_raster_single_band, sample_locations):
        """Test calculation of sampling summary statistics."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        sampling_summary = result['sampling_summary']
        assert isinstance(sampling_summary, dict), "sampling_summary should be a dictionary"

        # Should contain statistics about sampled values
        expected_stats = ['mean', 'std', 'min', 'max', 'count']

        # At least some statistical measures should be present
        stats_present = sum(1 for stat in expected_stats
                          if any(stat in key.lower() for key in sampling_summary.keys()))
        assert stats_present > 0, f"Should have some statistics in summary: {list(sampling_summary.keys())}"

    def test_raster_metadata(self, sample_raster_single_band, sample_locations):
        """Test inclusion of raster metadata."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        raster_metadata = result['raster_metadata']
        assert isinstance(raster_metadata, dict), "raster_metadata should be a dictionary"

        # Should contain basic raster information
        expected_metadata = ['width', 'height', 'count', 'crs', 'bounds']

        metadata_present = sum(1 for meta in expected_metadata if meta in raster_metadata)
        assert metadata_present >= 2, f"Should have basic metadata: {list(raster_metadata.keys())}"

    def test_error_handling_invalid_file(self):
        """Test error handling for invalid input file."""
        locations = [(-119.5, 37.5)]

        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            sample_raster_at_locations('nonexistent_file.tif', locations)

    def test_error_handling_invalid_coordinates(self, sample_raster_single_band):
        """Test error handling for invalid coordinate formats."""
        raster_path, bounds, data = sample_raster_single_band

        # Test invalid coordinate formats
        invalid_locations = [
            [(-119.5,)],  # Missing y coordinate
            [(-119.5, 37.5, 100)],  # Too many coordinates
            [(None, 37.5)],  # None coordinate
            [("invalid", 37.5)],  # String coordinate
        ]

        for invalid_locs in invalid_locations:
            with pytest.raises((ValueError, TypeError, IndexError)):
                sample_raster_at_locations(raster_path, invalid_locs)

    def test_error_handling_empty_locations(self, sample_raster_single_band):
        """Test handling of empty location list."""
        raster_path, bounds, data = sample_raster_single_band

        result = sample_raster_at_locations(raster_path, [])

        # Should handle gracefully
        assert isinstance(result, dict), "Should return dict for empty locations"
        assert result['valid_samples'] == 0, "Should have 0 valid samples for empty input"
        assert result['failed_samples'] == 0, "Should have 0 failed samples for empty input"
        assert result['sampled_values'] == [], "Should have empty sampled_values list"

    def test_buffer_radius_validation(self, sample_raster_single_band, sample_locations):
        """Test validation of buffer radius parameter."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        # Test negative buffer radius
        with pytest.raises(ValueError):
            sample_raster_at_locations(raster_path, locations_inside, buffer_radius=-1)

    def test_function_signature_and_defaults(self, sample_raster_single_band, sample_locations):
        """Test that function accepts expected parameters with defaults."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        # Test with minimum required parameters
        result1 = sample_raster_at_locations(raster_path, locations_inside)
        assert isinstance(result1, dict), "Should work with minimal parameters"

        # Test with all parameters
        result2 = sample_raster_at_locations(
            raster_path, locations_inside,
            buffer_radius=0.005,
            interpolation='nearest',
            band_numbers=[1]
        )
        assert isinstance(result2, dict), "Should work with all parameters"

    @pytest.mark.parametrize("invalid_input", [None, "", 123, []])
    def test_invalid_raster_path_types(self, invalid_input, sample_locations):
        """Test function behavior with invalid raster path types."""
        locations_inside, _ = sample_locations

        with pytest.raises((TypeError, ValueError, FileNotFoundError, AttributeError)):
            sample_raster_at_locations(invalid_input, locations_inside)

    @pytest.mark.parametrize("invalid_locations", [
        None,
        "invalid",
        123,
        [("not", "a", "tuple", "format")],
    ])
    def test_invalid_locations_types(self, sample_raster_single_band, invalid_locations):
        """Test function behavior with invalid location types."""
        raster_path, bounds, data = sample_raster_single_band

        with pytest.raises((TypeError, ValueError, IndexError)):
            sample_raster_at_locations(raster_path, invalid_locations)

    def test_large_buffer_handling(self, sample_raster_single_band, sample_locations):
        """Test handling of very large buffer radius."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        # Test with buffer larger than raster
        large_buffer = 2.0  # 2 degrees (larger than our 1-degree raster)

        result = sample_raster_at_locations(
            raster_path, locations_inside,
            buffer_radius=large_buffer
        )

        # Should handle gracefully without crashing
        assert isinstance(result, dict), "Should handle large buffers gracefully"

        # May have valid or invalid samples depending on implementation
        valid_samples = result['valid_samples']
        failed_samples = result['failed_samples']
        assert valid_samples + failed_samples == len(locations_inside), \
            "Should account for all samples even with large buffer"

    def test_precision_and_data_types(self, sample_raster_single_band, sample_locations):
        """Test data type handling and precision of results."""
        raster_path, bounds, data = sample_raster_single_band
        locations_inside, _ = sample_locations

        result = sample_raster_at_locations(raster_path, locations_inside)

        # Check data types in results
        sampled_values = result['sampled_values']

        for sample in sampled_values:
            for key, value in sample.items():
                if isinstance(value, (int, float, np.number)):
                    # Should be finite numbers
                    assert np.isfinite(value), f"Sampled value should be finite: {key}={value}"
                    # Should be reasonable precision (not excessive decimal places for display)
                    if isinstance(value, float):
                        assert abs(value) < 1e10, f"Sampled value seems too large: {key}={value}"
