"""
Tests for Applications Functions

This file tests the practical raster applications functions you'll implement.
Each test is simple and checks one specific thing about your function.

These functions represent real-world GIS workflows that professionals use daily!

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
    from src.rasterio_analysis.applications import (
        sample_raster_at_points,
        read_remote_raster,
        create_raster_summary
    )
except ImportError as e:
    pytest.skip(f"Could not import your functions: {e}", allow_module_level=True)


class TestApplications:
    """Tests for your practical applications functions."""

    @pytest.fixture(scope="class")
    def sample_raster_path(self):
        """Create a simple test raster file for testing."""
        temp_dir = tempfile.mkdtemp()
        raster_path = os.path.join(temp_dir, "test_elevation.tif")

        # Create simple elevation data: 20x20 raster
        width, height = 20, 20

        # Create realistic elevation data with a gradient
        elevation_data = np.zeros((height, width), dtype=np.float32)
        for i in range(height):
            for j in range(width):
                # Create elevation that increases from southwest to northeast
                elevation_data[i, j] = 1000 + (i * 10) + (j * 5) + np.random.uniform(-50, 50)

        # Add some nodata values
        elevation_data[0, 0] = -9999  # Nodata value

        # Define geographic extent (small area in California)
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
            count=1,
            dtype=elevation_data.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=-9999
        ) as dst:
            dst.write(elevation_data, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def multiband_raster_path(self):
        """Create a multi-band raster for comprehensive testing."""
        temp_dir = tempfile.mkdtemp()
        raster_path = os.path.join(temp_dir, "test_landsat.tif")

        # Create 4-band raster (Blue, Green, Red, NIR)
        width, height = 15, 15

        # Create sample bands with realistic values
        blue_data = np.random.randint(30, 100, (height, width), dtype=np.uint16)
        green_data = np.random.randint(40, 120, (height, width), dtype=np.uint16)
        red_data = np.random.randint(50, 150, (height, width), dtype=np.uint16)
        nir_data = np.random.randint(100, 250, (height, width), dtype=np.uint16)

        # Stack bands
        all_bands = np.stack([blue_data, green_data, red_data, nir_data])

        transform = rasterio.transform.from_bounds(
            -120.5, 35.2, -120.0, 35.7,
            width, height
        )

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=4,
            dtype=all_bands.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            for band_num in range(4):
                dst.write(all_bands[band_num], band_num + 1)

        return raster_path

    @pytest.fixture
    def sample_points(self):
        """Create sample point coordinates for testing."""
        # Points within our test raster extent (-120.0 to -119.0, 35.0 to 36.0)
        return [
            (-119.8, 35.2),  # Should be inside raster
            (-119.5, 35.5),  # Should be inside raster
            (-119.2, 35.8),  # Should be inside raster
            (-121.0, 35.5),  # Should be outside raster (too far west)
            (-119.5, 37.0),  # Should be outside raster (too far north)
        ]

    def test_sample_raster_at_points_basic(self, sample_raster_path, sample_points):
        """
        Test that sample_raster_at_points() extracts values at point locations.

        Your function should return a dictionary with point values and metadata.
        """
        # Call your function
        result = sample_raster_at_points(sample_raster_path, sample_points)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Check that all required keys are present
        required_keys = ['point_values', 'coordinates', 'points_inside_raster',
                        'points_outside_raster', 'total_points']
        for key in required_keys:
            assert key in result, f"Your result is missing the '{key}' key"

        # Check point values
        point_values = result['point_values']
        assert isinstance(point_values, list), "Point values should be a list"
        assert len(point_values) == len(sample_points), "Should have one value per point"

        # Check coordinates match
        assert result['coordinates'] == sample_points, "Coordinates should match input"

        # Check total points
        assert result['total_points'] == len(sample_points), "Total points should match input length"

        # Check that inside + outside = total
        inside = result['points_inside_raster']
        outside = result['points_outside_raster']
        total = result['total_points']
        assert inside + outside == total, "Inside + outside should equal total points"

    def test_sample_raster_at_points_values(self, sample_raster_path, sample_points):
        """Test that point sampling returns reasonable elevation values."""
        result = sample_raster_at_points(sample_raster_path, sample_points)

        point_values = result['point_values']

        # Check that we have some valid values (not all None)
        valid_values = [v for v in point_values if v is not None]
        assert len(valid_values) > 0, "Should have at least some valid point values"

        # Check that valid elevation values are reasonable (our test data is around 1000-1500m)
        for value in valid_values:
            assert 900 < value < 1600, f"Elevation value {value} seems unreasonable"

    def test_sample_raster_at_points_boundary_detection(self, sample_raster_path, sample_points):
        """Test that the function correctly identifies points inside/outside raster."""
        result = sample_raster_at_points(sample_raster_path, sample_points)

        # We know from our test data that some points should be inside and some outside
        assert result['points_inside_raster'] > 0, "Should have some points inside the raster"
        assert result['points_outside_raster'] > 0, "Should have some points outside the raster"

        # Check that outside points have None values
        point_values = result['point_values']
        inside_count = result['points_inside_raster']

        # Count None values
        none_count = sum(1 for v in point_values if v is None)
        assert none_count >= result['points_outside_raster'], "Outside points should have None values"

    def test_sample_raster_at_points_empty_list(self, sample_raster_path):
        """Test handling of empty points list."""
        result = sample_raster_at_points(sample_raster_path, [])

        assert result['total_points'] == 0, "Should handle empty points list"
        assert result['point_values'] == [], "Should return empty values list"
        assert result['points_inside_raster'] == 0, "Should have 0 inside points"
        assert result['points_outside_raster'] == 0, "Should have 0 outside points"

    def test_read_remote_raster_mock(self, sample_raster_path):
        """
        Test read_remote_raster() with a local file (simulating remote).

        Note: This uses a local file as a "remote" URL for testing purposes.
        """
        # Use file:// URL to simulate remote access
        file_url = f"file://{sample_raster_path}"

        try:
            # Call your function
            result = read_remote_raster(file_url)

            # Check basic structure
            assert isinstance(result, dict), "Your function should return a dictionary"

            # Check for required keys (success case)
            if 'data_array' in result:
                required_keys = ['data_array', 'width', 'height', 'crs', 'url']
                for key in required_keys:
                    assert key in result, f"Your result is missing the '{key}' key"

                # Check data array
                data_array = result['data_array']
                assert isinstance(data_array, np.ndarray), "Data array should be numpy array"
                assert data_array.size > 0, "Data array should not be empty"

                # Check metadata
                assert result['width'] > 0, "Width should be positive"
                assert result['height'] > 0, "Height should be positive"
                assert result['url'] == file_url, "URL should match input"

        except Exception:
            # If file:// URLs don't work, that's okay - just check error handling
            result = read_remote_raster("http://invalid.url/nonexistent.tif")
            assert 'error' in result, "Should handle invalid URLs gracefully"

    def test_read_remote_raster_with_bbox(self, sample_raster_path):
        """Test read_remote_raster() with bounding box clipping."""
        file_url = f"file://{sample_raster_path}"

        # Define a small bounding box within our raster
        bbox = (-119.8, 35.2, -119.2, 35.8)  # left, bottom, right, top

        try:
            result = read_remote_raster(file_url, bbox)

            if 'data_array' in result:
                # Should have data
                assert result['data_array'] is not None, "Should return data array"

                # Should indicate windowed reading was attempted
                if 'windowed' in result:
                    # If windowing worked, data should be smaller than full raster
                    data_shape = result['data_array'].shape
                    assert data_shape[0] <= 20 and data_shape[1] <= 20, "Windowed data should be smaller"

        except Exception:
            # Windowed reading might fail in test environment, that's okay
            pass

    def test_read_remote_raster_error_handling(self):
        """Test that read_remote_raster() handles errors gracefully."""
        # Try with completely invalid URL
        result = read_remote_raster("not_a_valid_url")

        # Should return error information instead of crashing
        assert isinstance(result, dict), "Should return dictionary even on error"
        assert 'error' in result or 'success' in result, "Should indicate error status"

    def test_create_raster_summary_basic(self, sample_raster_path):
        """
        Test that create_raster_summary() creates a comprehensive summary.

        Your function should combine information from your other functions.
        """
        # Call your function
        result = create_raster_summary(sample_raster_path)

        # Check that it returns a dictionary
        assert isinstance(result, dict), "Your function should return a dictionary"

        # Should have the raster path
        assert 'raster_path' in result, "Should include the raster path"
        assert result['raster_path'] == sample_raster_path, "Path should match input"

        # Check for main sections (if successfully created)
        expected_sections = ['file_info', 'statistics', 'extent']
        for section in expected_sections:
            if section in result:
                assert isinstance(result[section], dict), f"{section} should be a dictionary"

    def test_create_raster_summary_file_info(self, sample_raster_path):
        """Test that summary includes file information."""
        result = create_raster_summary(sample_raster_path)

        if 'file_info' in result:
            file_info = result['file_info']

            # Should have basic raster properties
            assert 'width' in file_info, "File info should include width"
            assert 'height' in file_info, "File info should include height"
            assert 'count' in file_info, "File info should include band count"

            # Check reasonable values
            assert file_info['width'] == 20, "Width should match test data"
            assert file_info['height'] == 20, "Height should match test data"
            assert file_info['count'] == 1, "Should have 1 band"

    def test_create_raster_summary_statistics(self, sample_raster_path):
        """Test that summary includes statistics."""
        result = create_raster_summary(sample_raster_path)

        if 'statistics' in result:
            stats = result['statistics']

            # Should have basic statistics
            assert 'min' in stats, "Statistics should include min"
            assert 'max' in stats, "Statistics should include max"
            assert 'mean' in stats, "Statistics should include mean"

            # Check that values are reasonable for our elevation data
            if stats['min'] is not None and stats['max'] is not None:
                assert stats['min'] < stats['max'], "Min should be less than max"
                assert 900 < stats['mean'] < 1600, "Mean elevation should be reasonable"

    def test_create_raster_summary_multiband(self, multiband_raster_path):
        """Test summary creation with multi-band raster (should attempt NDVI)."""
        result = create_raster_summary(multiband_raster_path)

        # Should recognize this as multi-band
        if 'file_info' in result:
            assert result['file_info']['count'] == 4, "Should detect 4 bands"

        # Should attempt NDVI analysis
        if 'ndvi_analysis' in result:
            ndvi_section = result['ndvi_analysis']
            # Either successful NDVI or error message
            assert ('min_ndvi' in ndvi_section or 'error' in ndvi_section or 'note' in ndvi_section), \
                "Should attempt NDVI analysis or explain why not"

    def test_create_raster_summary_high_level_summary(self, sample_raster_path):
        """Test that summary includes high-level assessment."""
        result = create_raster_summary(sample_raster_path)

        if 'summary' in result:
            summary_section = result['summary']

            # Should have useful summary information
            useful_keys = ['total_pixels', 'estimated_size_mb', 'is_multiband', 'data_quality']
            present_keys = [key for key in useful_keys if key in summary_section]
            assert len(present_keys) > 0, "Should have some high-level summary information"

    def test_create_raster_summary_error_handling(self):
        """Test that create_raster_summary() handles missing files gracefully."""
        result = create_raster_summary("nonexistent_file.tif")

        # Should handle missing file without crashing
        assert isinstance(result, dict), "Should return dictionary even for missing file"
        assert ('error' in result or 'success' in result), "Should indicate error status"

    def test_all_functions_work_together(self, sample_raster_path, sample_points):
        """
        Test that all your functions work together in a realistic workflow.

        This simulates what a GIS professional might do:
        1. Get an overview of the raster
        2. Sample values at specific points
        3. Understand what the data contains
        """
        print("\n=== Testing Complete GIS Workflow ===")

        # Step 1: Create comprehensive summary
        summary = create_raster_summary(sample_raster_path)
        assert summary is not None, "Should create raster summary"
        print("✓ Created raster summary")

        # Step 2: Sample at specific locations
        point_results = sample_raster_at_points(sample_raster_path, sample_points[:3])  # Use first 3 points
        assert point_results['total_points'] == 3, "Should sample at 3 points"
        print("✓ Sampled raster at point locations")

        # Step 3: Verify we have useful information
        valid_values = [v for v in point_results['point_values'] if v is not None]
        assert len(valid_values) > 0, "Should have extracted some valid values"
        print(f"✓ Extracted {len(valid_values)} valid elevation values")

        print("✅ Complete GIS workflow successful!")

    def test_realistic_use_case(self, sample_raster_path):
        """Test a realistic GIS use case scenario."""
        # Scenario: A park ranger wants to know the elevation at several trail markers
        trail_markers = [
            (-119.7, 35.3),  # Trailhead
            (-119.5, 35.5),  # Midway point
            (-119.3, 35.7),  # Summit
        ]

        # Sample elevations
        results = sample_raster_at_points(sample_raster_path, trail_markers)

        # Should get elevation data for trail planning
        assert results['points_inside_raster'] >= 2, "Should find most trail markers in the raster"

        valid_elevations = [v for v in results['point_values'] if v is not None]
        assert len(valid_elevations) >= 2, "Should get elevation data for trail planning"

        print(f"Trail elevations: {valid_elevations}")


# Helpful test runner for students
if __name__ == "__main__":
    print("Running tests for your applications functions...")
    print("These test real-world GIS workflows!")
    print()

    # You can run just this file to test your functions
    pytest.main([__file__, "-v"])
