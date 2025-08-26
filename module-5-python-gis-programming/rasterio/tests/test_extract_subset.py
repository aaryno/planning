"""
Tests for extract_raster_subset function

This module contains comprehensive tests for the extract_raster_subset function
that validates spatial subsetting and clipping operations on raster data.

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
from typing import Dict, Any, Tuple
from shapely.geometry import box
import shutil

# Import the function to test
import sys
sys.path.insert(0, 'src')
from rasterio_basics import extract_raster_subset


class TestExtractRasterSubset:
    """Test suite for extract_raster_subset function."""

    @pytest.fixture
    def base_raster(self):
        """Create a base raster covering a known geographic extent."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create 100x80 raster covering 1°x1° extent
        width, height = 100, 80
        left, bottom, right, top = -120.0, 35.0, -119.0, 36.0

        # Create elevation-like data with spatial pattern
        x = np.linspace(left, right, width)
        y = np.linspace(bottom, top, height)
        X, Y = np.meshgrid(x, y)

        # Create data with spatial pattern (elevation increases with longitude and latitude)
        data = (1000 + (X + 120) * 500 + (Y - 35) * 300).astype(np.float32)

        transform = from_bounds(left, bottom, right, top, width, height)

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
    def utm_raster(self):
        """Create a UTM-projected raster for projection testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        # Create raster in UTM coordinates
        width, height = 50, 40
        left, bottom, right, top = 500000, 4000000, 505000, 4004000  # UTM coordinates

        data = np.random.randint(0, 255, size=(height, width), dtype=np.uint8)
        transform = from_bounds(left, bottom, right, top, width, height)

        with rasterio.open(
            temp_file.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=data.dtype,
            crs=CRS.from_epsg(32633),  # UTM Zone 33N
            transform=transform
        ) as dst:
            dst.write(data, 1)

        yield temp_file.name

        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

    @pytest.fixture
    def multiband_raster(self):
        """Create multi-band raster for band handling testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.tif', delete=False)
        temp_file.close()

        width, height, bands = 30, 25, 3
        left, bottom, right, top = 0.0, 0.0, 30.0, 25.0

        # Create RGB-like data
        data = np.random.randint(0, 255, size=(bands, height, width), dtype=np.uint8)
        transform = from_bounds(left, bottom, right, top, width, height)

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
    def temp_output_dir(self):
        """Create temporary directory for output files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_basic_functionality(self, base_raster):
        """Test basic subset extraction without saving."""
        # Define bounds that are within the raster extent
        # Original: -120.0, 35.0, -119.0, 36.0
        bounds = (-119.8, 35.2, -119.2, 35.8)  # Interior subset

        result = extract_raster_subset(base_raster, bounds)

        # Test return type
        assert isinstance(result, dict), "Function should return a dictionary"

        # Test required keys are present
        required_keys = [
            'subset_bounds', 'subset_width', 'subset_height',
            'subset_transform', 'original_bounds', 'data_summary',
            'file_saved', 'output_path'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Test data types
        assert isinstance(result['subset_bounds'], dict), "Subset bounds should be dict"
        assert isinstance(result['subset_width'], int), "Subset width should be int"
        assert isinstance(result['subset_height'], int), "Subset height should be int"
        assert isinstance(result['subset_transform'], list), "Subset transform should be list"
        assert isinstance(result['original_bounds'], dict), "Original bounds should be dict"
        assert isinstance(result['data_summary'], dict), "Data summary should be dict"
        assert isinstance(result['file_saved'], bool), "File saved should be bool"

        # Test logical values
        assert result['subset_width'] > 0, "Subset width should be positive"
        assert result['subset_height'] > 0, "Subset height should be positive"
        assert result['file_saved'] is False, "File should not be saved when no output path given"
        assert result['output_path'] is None, "Output path should be None when not saving"

    def test_bounds_validation(self, base_raster):
        """Test bounds format and validation."""
        # Valid bounds
        bounds = (-119.8, 35.2, -119.2, 35.8)
        result = extract_raster_subset(base_raster, bounds)
        assert isinstance(result, dict)

        # Test that subset bounds are reasonable
        subset_bounds = result['subset_bounds']
        assert 'left' in subset_bounds and 'bottom' in subset_bounds
        assert 'right' in subset_bounds and 'top' in subset_bounds

        # Subset bounds should be within or equal to requested bounds
        assert subset_bounds['left'] >= bounds[0] - 0.1  # Allow small tolerance
        assert subset_bounds['bottom'] >= bounds[1] - 0.1
        assert subset_bounds['right'] <= bounds[2] + 0.1
        assert subset_bounds['top'] <= bounds[3] + 0.1

    def test_transform_calculation(self, base_raster):
        """Test that subset transform is correctly calculated."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        result = extract_raster_subset(base_raster, bounds)

        transform = result['subset_transform']

        # Transform should have 6 elements
        assert len(transform) == 6, "Transform should have 6 elements"

        # All elements should be numeric
        for i, val in enumerate(transform):
            assert isinstance(val, (int, float)), f"Transform element {i} should be numeric"

        # First element (x pixel size) should be positive
        assert transform[0] > 0, "X pixel size should be positive"

        # Fifth element (y pixel size) should be negative (standard for north-up images)
        assert transform[4] < 0, "Y pixel size should be negative for north-up images"

    def test_data_summary_contents(self, base_raster):
        """Test that data summary contains expected statistics."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        result = extract_raster_subset(base_raster, bounds)

        data_summary = result['data_summary']

        # Should contain basic statistics
        expected_stats = ['min', 'max', 'mean', 'count']
        for stat in expected_stats:
            assert stat in data_summary, f"Data summary should contain {stat}"
            if data_summary[stat] is not None:
                assert isinstance(data_summary[stat], (int, float)), f"{stat} should be numeric"

        # Logical relationships
        if data_summary['min'] is not None and data_summary['max'] is not None:
            assert data_summary['min'] <= data_summary['max'], "Min should be <= max"

        if data_summary['count'] is not None:
            assert data_summary['count'] >= 0, "Count should be non-negative"

    def test_subset_with_file_saving(self, base_raster, temp_output_dir):
        """Test subset extraction with file saving."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        output_path = os.path.join(temp_output_dir, "subset.tif")

        result = extract_raster_subset(base_raster, bounds, output_path)

        # Test file saving indicators
        assert result['file_saved'] is True, "File should be saved"
        assert result['output_path'] == output_path, "Output path should match"

        # Test that file actually exists
        assert os.path.exists(output_path), "Output file should exist"

        # Test that saved file is valid raster
        with rasterio.open(output_path) as src:
            assert src.width == result['subset_width'], "Saved file width should match result"
            assert src.height == result['subset_height'], "Saved file height should match result"
            assert src.count >= 1, "Saved file should have at least one band"

    def test_subset_dimensions_calculation(self, base_raster):
        """Test that subset dimensions are calculated correctly."""
        # Test with bounds that should produce known dimensions
        # Original raster: 100x80 pixels, -120 to -119 (1°) x 35 to 36 (1°)
        # So pixel size is 0.01° x 0.0125°

        bounds = (-119.9, 35.1, -119.1, 35.9)  # 0.8° x 0.8° subset
        result = extract_raster_subset(base_raster, bounds)

        # Should get reasonable dimensions (approximate since clipping is involved)
        assert 60 <= result['subset_width'] <= 90, f"Width should be reasonable, got {result['subset_width']}"
        assert 50 <= result['subset_height'] <= 80, f"Height should be reasonable, got {result['subset_height']}"

    def test_bounds_outside_raster_extent(self, base_raster):
        """Test with bounds completely outside raster extent."""
        # Original extent: -120.0, 35.0, -119.0, 36.0
        bounds = (-122.0, 37.0, -121.0, 38.0)  # Completely outside

        # This might either return empty result or raise an error
        # We test that it handles this case gracefully
        try:
            result = extract_raster_subset(base_raster, bounds)
            # If it succeeds, it should indicate no data or empty result
            if result['subset_width'] == 0 or result['subset_height'] == 0:
                assert True, "Correctly handled bounds outside extent"
            else:
                # If it returns data, dimensions should be reasonable
                assert result['subset_width'] > 0
                assert result['subset_height'] > 0
        except (ValueError, RuntimeError):
            # It's also acceptable to raise an error for bounds outside extent
            assert True, "Correctly raised error for bounds outside extent"

    def test_partial_overlap_bounds(self, base_raster):
        """Test with bounds that partially overlap the raster."""
        # Original extent: -120.0, 35.0, -119.0, 36.0
        bounds = (-120.5, 35.5, -119.5, 36.5)  # Partially overlapping

        result = extract_raster_subset(base_raster, bounds)

        # Should return valid result with reasonable dimensions
        assert result['subset_width'] > 0, "Should have positive width"
        assert result['subset_height'] > 0, "Should have positive height"

        # Subset bounds should be clipped to actual data extent
        subset_bounds = result['subset_bounds']
        original_bounds = result['original_bounds']

        # Subset should not extend beyond original bounds
        assert subset_bounds['left'] >= original_bounds['left'] - 0.1
        assert subset_bounds['right'] <= original_bounds['right'] + 0.1
        assert subset_bounds['bottom'] >= original_bounds['bottom'] - 0.1
        assert subset_bounds['top'] <= original_bounds['top'] + 0.1

    def test_multiband_raster_handling(self, multiband_raster):
        """Test subset extraction on multi-band raster."""
        bounds = (5.0, 5.0, 25.0, 20.0)  # Interior subset

        result = extract_raster_subset(multiband_raster, bounds)

        # Should handle multi-band data correctly
        assert isinstance(result, dict)
        assert result['subset_width'] > 0
        assert result['subset_height'] > 0

        # Data summary should account for multi-band data
        data_summary = result['data_summary']
        assert isinstance(data_summary, dict)

    def test_utm_projected_raster(self, utm_raster):
        """Test subset extraction on UTM-projected raster."""
        # UTM coordinates: 500000, 4000000, 505000, 4004000
        bounds = (501000, 4001000, 504000, 4003000)  # Interior subset in UTM

        result = extract_raster_subset(utm_raster, bounds)

        # Should work with UTM coordinates
        assert result['subset_width'] > 0
        assert result['subset_height'] > 0

        # Bounds should be in UTM coordinates
        subset_bounds = result['subset_bounds']
        assert subset_bounds['left'] >= 500000, "UTM coordinates should be preserved"
        assert subset_bounds['right'] <= 505000, "UTM coordinates should be preserved"

    def test_single_pixel_subset(self, base_raster):
        """Test extraction of very small subset (single pixel)."""
        # Try to get a very small area that should result in 1 pixel
        bounds = (-119.505, 35.505, -119.495, 35.515)  # Very small area

        result = extract_raster_subset(base_raster, bounds)

        # Should get at least 1 pixel
        assert result['subset_width'] >= 1, "Should get at least 1 pixel width"
        assert result['subset_height'] >= 1, "Should get at least 1 pixel height"

        # Data summary should be valid even for small subset
        assert isinstance(result['data_summary'], dict)

    def test_invalid_bounds_format(self, base_raster):
        """Test error handling for invalid bounds format."""
        invalid_bounds_cases = [
            (-119.0, 35.0, -120.0, 36.0),  # left > right
            (-119.0, 36.0, -118.0, 35.0),  # bottom > top
            (-119.0,),  # Too few values
            (-119.0, 35.0, -118.0, 36.0, 37.0),  # Too many values
        ]

        for invalid_bounds in invalid_bounds_cases:
            with pytest.raises((ValueError, TypeError, IndexError)):
                extract_raster_subset(base_raster, invalid_bounds)

    def test_file_not_found_error(self):
        """Test error handling for non-existent input file."""
        non_existent_file = "this_file_does_not_exist.tif"
        bounds = (-119.0, 35.0, -118.0, 36.0)

        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            extract_raster_subset(non_existent_file, bounds)

    def test_invalid_output_path(self, base_raster):
        """Test error handling for invalid output path."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        invalid_output_path = "/invalid/directory/that/does/not/exist/output.tif"

        # Should either create directories or raise appropriate error
        with pytest.raises((OSError, IOError, PermissionError)):
            extract_raster_subset(base_raster, bounds, invalid_output_path)

    def test_output_file_overwrite(self, base_raster, temp_output_dir):
        """Test behavior when output file already exists."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        output_path = os.path.join(temp_output_dir, "test_overwrite.tif")

        # Create a dummy file first
        with open(output_path, 'w') as f:
            f.write("dummy content")

        # Function should overwrite existing file
        result = extract_raster_subset(base_raster, bounds, output_path)

        assert result['file_saved'] is True
        assert os.path.exists(output_path)

        # File should be valid raster (not dummy content)
        with rasterio.open(output_path) as src:
            assert src.width > 0
            assert src.height > 0

    def test_bounds_edge_cases(self, base_raster):
        """Test edge cases for bounds specifications."""
        # Original extent: -120.0, 35.0, -119.0, 36.0

        # Test bounds exactly matching raster extent
        bounds = (-120.0, 35.0, -119.0, 36.0)
        result = extract_raster_subset(base_raster, bounds)
        assert result['subset_width'] > 0
        assert result['subset_height'] > 0

        # Test bounds slightly larger than raster extent
        bounds = (-120.1, 34.9, -118.9, 36.1)
        result = extract_raster_subset(base_raster, bounds)
        # Should clip to actual raster extent
        subset_bounds = result['subset_bounds']
        original_bounds = result['original_bounds']
        assert subset_bounds['left'] >= original_bounds['left'] - 0.1
        assert subset_bounds['right'] <= original_bounds['right'] + 0.1

    def test_return_value_json_serializable(self, base_raster):
        """Test that returned values are JSON serializable."""
        import json

        bounds = (-119.8, 35.2, -119.2, 35.8)
        result = extract_raster_subset(base_raster, bounds)

        # This should not raise an exception if all values are JSON serializable
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON serializable: {e}")

    def test_comprehensive_integration(self, base_raster, temp_output_dir):
        """Comprehensive integration test checking all aspects together."""
        bounds = (-119.8, 35.2, -119.2, 35.8)
        output_path = os.path.join(temp_output_dir, "integration_test.tif")

        result = extract_raster_subset(base_raster, bounds, output_path)

        # Verify all expected keys with correct types
        expected_structure = {
            'subset_bounds': dict,
            'subset_width': int,
            'subset_height': int,
            'subset_transform': list,
            'original_bounds': dict,
            'data_summary': dict,
            'file_saved': bool,
            'output_path': str
        }

        for key, expected_type in expected_structure.items():
            assert key in result, f"Missing key: {key}"
            assert isinstance(result[key], expected_type), f"Key {key} has wrong type: {type(result[key])}"

        # Verify bounds dictionaries have required keys
        for bounds_dict_key in ['subset_bounds', 'original_bounds']:
            bounds_dict = result[bounds_dict_key]
            for coord_key in ['left', 'bottom', 'right', 'top']:
                assert coord_key in bounds_dict, f"Missing coordinate key {coord_key} in {bounds_dict_key}"
                assert isinstance(bounds_dict[coord_key], (int, float)), f"Coordinate {coord_key} should be numeric"

        # Verify transform has 6 numeric elements
        transform = result['subset_transform']
        assert len(transform) == 6, "Transform should have 6 elements"
        for i, val in enumerate(transform):
            assert isinstance(val, (int, float)), f"Transform element {i} should be numeric"

        # Verify dimensions are positive
        assert result['subset_width'] > 0, "Subset width should be positive"
        assert result['subset_height'] > 0, "Subset height should be positive"

        # Verify file operations
        assert result['file_saved'] is True, "File should be saved"
        assert os.path.exists(result['output_path']), "Output file should exist"
        assert result['output_path'] == output_path, "Output path should match input"

        # Verify saved file is valid and matches metadata
        with rasterio.open(output_path) as src:
            assert src.width == result['subset_width'], "Saved file width should match result"
            assert src.height == result['subset_height'], "Saved file height should match result"

        # Verify data summary contains expected statistics
        data_summary = result['data_summary']
        for stat_key in ['min', 'max', 'mean', 'count']:
            assert stat_key in data_summary, f"Missing statistic: {stat_key}"
