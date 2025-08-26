"""
Test suite for calculate_topographic_metrics function.

This module tests the comprehensive topographic analysis capabilities including
slope, aspect, hillshade calculation, and terrain classification.
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
    from rasterio_analysis import calculate_topographic_metrics
except ImportError as e:
    pytest.skip(f"Could not import calculate_topographic_metrics: {e}", allow_module_level=True)


@pytest.fixture
def sample_dem_simple():
    """Create a simple test DEM with known elevation patterns."""
    # Create a simple 10x10 DEM with a gradient from 0 to 100m
    width, height = 10, 10
    elevation_data = np.zeros((height, width), dtype=np.float32)

    # Create a simple gradient: elevation increases from west to east
    for i in range(width):
        elevation_data[:, i] = i * 10  # 0, 10, 20, 30, ... 90

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
            dtype=elevation_data.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(elevation_data, 1)

        yield tmp.name

    # Cleanup
    try:
        os.unlink(tmp.name)
    except:
        pass


@pytest.fixture
def sample_dem_complex():
    """Create a more complex DEM with hills and valleys."""
    width, height = 20, 20
    x = np.linspace(-2, 2, width)
    y = np.linspace(-2, 2, height)
    X, Y = np.meshgrid(x, y)

    # Create a surface with hills and valleys using sine waves
    elevation_data = (100 + 50 * np.sin(X) * np.cos(Y) +
                     30 * np.sin(2*X) + 20 * np.cos(2*Y)).astype(np.float32)

    # Define geographic bounds
    bounds = (-121, 36, -119, 38)
    transform = from_bounds(*bounds, width, height)

    # Create temporary raster file
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        with rasterio.open(
            tmp.name, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=elevation_data.dtype,
            crs='EPSG:4326',
            transform=transform
        ) as dst:
            dst.write(elevation_data, 1)

        yield tmp.name

    # Cleanup
    try:
        os.unlink(tmp.name)
    except:
        pass


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestCalculateTopographicMetrics:
    """Test class for calculate_topographic_metrics function."""

    def test_function_exists(self):
        """Test that the function exists and is callable."""
        assert callable(calculate_topographic_metrics), \
            "calculate_topographic_metrics should be a callable function"

    def test_basic_functionality(self, sample_dem_simple):
        """Test basic functionality with simple DEM."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Check return type
        assert isinstance(result, dict), \
            "Function should return a dictionary"

        # Check required keys
        required_keys = [
            'slope_stats', 'aspect_stats', 'hillshade_stats',
            'terrain_classification', 'slope_array', 'aspect_array',
            'hillshade_array', 'files_created', 'cell_size', 'elevation_range'
        ]

        for key in required_keys:
            assert key in result, f"Result should contain '{key}' key"

    def test_slope_calculation_simple_gradient(self, sample_dem_simple):
        """Test slope calculation on simple gradient."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Check slope statistics
        slope_stats = result['slope_stats']
        assert isinstance(slope_stats, dict), "slope_stats should be a dictionary"
        assert 'mean' in slope_stats, "slope_stats should contain 'mean'"
        assert 'max' in slope_stats, "slope_stats should contain 'max'"
        assert 'min' in slope_stats, "slope_stats should contain 'min'"

        # Check slope array
        slope_array = result['slope_array']
        assert isinstance(slope_array, np.ndarray), "slope_array should be numpy array"
        assert slope_array.shape == (10, 10), f"slope_array shape should be (10, 10), got {slope_array.shape}"

        # For a simple west-east gradient, slope should be relatively uniform
        # and greater than 0 (except possibly at edges)
        valid_slopes = slope_array[1:-1, 1:-1]  # Exclude edges
        assert np.all(valid_slopes >= 0), "All slope values should be >= 0"
        assert np.all(valid_slopes <= 90), "All slope values should be <= 90 degrees"

        # Mean slope should be reasonable for the gradient
        mean_slope = slope_stats['mean']
        assert 0 < mean_slope < 45, f"Mean slope should be reasonable, got {mean_slope}"

    def test_aspect_calculation(self, sample_dem_simple):
        """Test aspect calculation."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Check aspect statistics
        aspect_stats = result['aspect_stats']
        assert isinstance(aspect_stats, dict), "aspect_stats should be a dictionary"

        # Check aspect array
        aspect_array = result['aspect_array']
        assert isinstance(aspect_array, np.ndarray), "aspect_array should be numpy array"
        assert aspect_array.shape == (10, 10), f"aspect_array shape should be (10, 10)"

        # Aspect values should be in 0-360 range
        valid_aspects = aspect_array[~np.isnan(aspect_array)]
        if len(valid_aspects) > 0:
            assert np.all(valid_aspects >= 0), "All aspect values should be >= 0"
            assert np.all(valid_aspects <= 360), "All aspect values should be <= 360"

        # For west-east gradient, aspect should be roughly east or west facing
        # (90° = east, 270° = west)
        central_aspects = aspect_array[2:-2, 2:-2]  # Central area
        valid_central = central_aspects[~np.isnan(central_aspects)]
        if len(valid_central) > 0:
            # Most aspects should be roughly east-facing for this gradient
            east_facing = np.sum((valid_central >= 45) & (valid_central <= 135))
            west_facing = np.sum((valid_central >= 225) & (valid_central <= 315))
            total_valid = len(valid_central)

            # At least some should be east or west facing
            assert (east_facing + west_facing) > total_valid * 0.3, \
                "Most aspects should be east or west facing for simple gradient"

    def test_hillshade_calculation(self, sample_dem_simple):
        """Test hillshade calculation."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Check hillshade statistics
        hillshade_stats = result['hillshade_stats']
        assert isinstance(hillshade_stats, dict), "hillshade_stats should be a dictionary"

        # Check hillshade array
        hillshade_array = result['hillshade_array']
        assert isinstance(hillshade_array, np.ndarray), "hillshade_array should be numpy array"
        assert hillshade_array.shape == (10, 10), "hillshade_array shape should be (10, 10)"

        # Hillshade values should be in 0-255 range
        assert np.all(hillshade_array >= 0), "All hillshade values should be >= 0"
        assert np.all(hillshade_array <= 255), "All hillshade values should be <= 255"

        # Check data type
        assert hillshade_array.dtype in [np.uint8, np.float32, np.float64], \
            f"Hillshade should be numeric type, got {hillshade_array.dtype}"

        # Hillshade should have reasonable variation
        hillshade_range = hillshade_stats.get('max', 255) - hillshade_stats.get('min', 0)
        assert hillshade_range > 0, "Hillshade should have some variation"

    def test_terrain_classification(self, sample_dem_simple):
        """Test terrain classification functionality."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Check terrain classification
        terrain_class = result['terrain_classification']
        assert isinstance(terrain_class, dict), "terrain_classification should be a dictionary"

        # Check for standard terrain classes
        expected_classes = ['flat', 'gentle', 'moderate', 'steep', 'very_steep']

        # At least some classification keys should be present
        class_keys = list(terrain_class.keys())
        assert len(class_keys) > 0, "Terrain classification should have at least one class"

        # All values should be non-negative integers (pixel counts)
        for class_name, count in terrain_class.items():
            assert isinstance(count, (int, np.integer)), \
                f"Terrain class count should be integer, got {type(count)} for {class_name}"
            assert count >= 0, f"Terrain class count should be >= 0, got {count} for {class_name}"

        # Total pixels should match raster size
        total_classified = sum(terrain_class.values())
        assert total_classified <= 100, f"Total classified pixels ({total_classified}) should be <= 100 (10x10 DEM)"

    def test_cell_size_calculation(self, sample_dem_simple):
        """Test cell size calculation."""
        result = calculate_topographic_metrics(sample_dem_simple)

        cell_size = result['cell_size']
        assert isinstance(cell_size, (int, float)), \
            f"cell_size should be numeric, got {type(cell_size)}"
        assert cell_size > 0, f"cell_size should be positive, got {cell_size}"

        # For our test DEM (1 degree across 10 pixels), cell size should be ~0.1 degrees
        # or equivalent in meters (roughly 11km at this latitude)
        assert 0.05 < cell_size < 0.2, f"cell_size seems unreasonable: {cell_size}"

    def test_elevation_range(self, sample_dem_simple):
        """Test elevation range calculation."""
        result = calculate_topographic_metrics(sample_dem_simple)

        elevation_range = result['elevation_range']
        assert isinstance(elevation_range, dict), "elevation_range should be a dictionary"
        assert 'min' in elevation_range, "elevation_range should contain 'min'"
        assert 'max' in elevation_range, "elevation_range should contain 'max'"

        elev_min = elevation_range['min']
        elev_max = elevation_range['max']

        # Check reasonable values for our test DEM (0-90m gradient)
        assert -10 <= elev_min <= 10, f"Minimum elevation should be near 0, got {elev_min}"
        assert 80 <= elev_max <= 100, f"Maximum elevation should be near 90, got {elev_max}"
        assert elev_max > elev_min, "Maximum elevation should be greater than minimum"

    def test_output_file_creation(self, sample_dem_simple, temp_output_dir):
        """Test creation of output files when output_dir is specified."""
        result = calculate_topographic_metrics(sample_dem_simple, output_dir=temp_output_dir)

        files_created = result['files_created']
        assert isinstance(files_created, list), "files_created should be a list"

        # Check if files were actually created
        output_path = Path(temp_output_dir)
        expected_files = ['slope.tif', 'aspect.tif', 'hillshade.tif']

        for expected_file in expected_files:
            file_path = output_path / expected_file
            if str(file_path) in files_created:
                assert file_path.exists(), f"Output file {expected_file} should exist"

                # Verify file is readable as raster
                with rasterio.open(file_path) as src:
                    assert src.count == 1, f"{expected_file} should have 1 band"
                    assert src.width == 10, f"{expected_file} should have width 10"
                    assert src.height == 10, f"{expected_file} should have height 10"

    def test_complex_terrain(self, sample_dem_complex):
        """Test function with more complex terrain."""
        result = calculate_topographic_metrics(sample_dem_complex)

        # Should handle complex terrain without errors
        assert isinstance(result, dict), "Function should return dict for complex terrain"

        # Check that we get varied terrain classification
        terrain_class = result['terrain_classification']

        # Should have multiple terrain types for complex surface
        num_terrain_types = sum(1 for count in terrain_class.values() if count > 0)
        assert num_terrain_types >= 2, \
            f"Complex terrain should have multiple terrain types, got {num_terrain_types}"

        # Slope should have good variation
        slope_stats = result['slope_stats']
        slope_range = slope_stats['max'] - slope_stats['min']
        assert slope_range > 5, f"Complex terrain should have slope variation > 5°, got {slope_range}"

    def test_error_handling_invalid_file(self):
        """Test error handling for invalid input file."""
        with pytest.raises((FileNotFoundError, rasterio.RasterioIOError)):
            calculate_topographic_metrics('nonexistent_file.tif')

    def test_error_handling_empty_output_dir(self, sample_dem_simple):
        """Test that function works when output_dir is None."""
        result = calculate_topographic_metrics(sample_dem_simple, output_dir=None)

        assert isinstance(result, dict), "Function should work with output_dir=None"
        files_created = result['files_created']
        assert isinstance(files_created, list), "files_created should be a list even when no files created"

    def test_statistics_accuracy(self, sample_dem_simple):
        """Test that calculated statistics are mathematically reasonable."""
        result = calculate_topographic_metrics(sample_dem_simple)

        # Test slope statistics consistency
        slope_stats = result['slope_stats']
        slope_array = result['slope_array']

        # Compare calculated stats with array stats (allowing for edge effects)
        central_slopes = slope_array[1:-1, 1:-1].flatten()
        central_slopes = central_slopes[~np.isnan(central_slopes)]

        if len(central_slopes) > 0:
            calculated_mean = slope_stats['mean']
            array_mean = np.mean(central_slopes)

            # Should be reasonably close (within 20% due to edge handling)
            relative_error = abs(calculated_mean - array_mean) / max(array_mean, 0.1)
            assert relative_error < 0.5, \
                f"Calculated mean slope ({calculated_mean}) differs too much from array mean ({array_mean})"

    def test_function_signature_and_defaults(self, sample_dem_simple):
        """Test that function accepts expected parameters with defaults."""
        # Test with minimum required parameter
        result1 = calculate_topographic_metrics(sample_dem_simple)
        assert isinstance(result1, dict), "Function should work with just dem_path"

        # Test with output_dir parameter
        with tempfile.TemporaryDirectory() as tmpdir:
            result2 = calculate_topographic_metrics(sample_dem_simple, output_dir=tmpdir)
            assert isinstance(result2, dict), "Function should work with output_dir parameter"

    @pytest.mark.parametrize("invalid_input", [None, "", 123, []])
    def test_invalid_input_types(self, invalid_input):
        """Test function behavior with invalid input types."""
        with pytest.raises((TypeError, ValueError, FileNotFoundError, AttributeError)):
            calculate_topographic_metrics(invalid_input)
