"""
Rasterio Analysis Tests Package
===============================

This package contains automated tests for the Rasterio advanced processing assignment.
These tests verify that your raster analysis functions work correctly and
help you understand what each function should do.

Test Structure:
- test_raster_processing.py: Tests for core raster operations and analysis
- test_cog_operations.py: Tests for Cloud Optimized GeoTIFF workflows
- test_stac_integration.py: Tests for STAC API integration and data access
- test_memory_efficient.py: Tests for large-scale processing and optimization

Running Tests:
- All tests: pytest tests/
- Specific module: pytest tests/test_raster_processing.py
- Verbose output: pytest tests/ -v
- With coverage: pytest tests/ --cov=src
- Skip slow tests: pytest tests/ -m "not slow"

The tests use sample raster datasets and verify that your functions:
1. Handle edge cases (nodata values, invalid CRS, memory limits)
2. Produce correct raster analysis results (NDVI, statistics, etc.)
3. Create valid Cloud Optimized GeoTIFFs
4. Integrate properly with STAC APIs and cloud data
5. Use memory efficiently for large raster processing
"""

__version__ = "0.1.0"

# Test configuration
import pytest
import warnings
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.transform import from_bounds
from pathlib import Path
import tempfile
import os

# Suppress common warnings during testing
warnings.filterwarnings("ignore", category=UserWarning, module="rasterio")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyproj")
warnings.filterwarnings("ignore", category=FutureWarning, module="xarray")
warnings.filterwarnings("ignore", category=UserWarning, module="dask")
warnings.filterwarnings("ignore", ".*GDAL.*", category=UserWarning)

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Common test utilities
def assert_raster_properties_equal(profile1, profile2, ignore_keys=None):
    """Assert that two raster profiles have matching properties."""
    ignore_keys = ignore_keys or []

    for key in profile1.keys():
        if key not in ignore_keys:
            assert key in profile2, f"Missing key in profile2: {key}"
            assert profile1[key] == profile2[key], f"Value mismatch for {key}: {profile1[key]} != {profile2[key]}"

def assert_arrays_close(arr1, arr2, rtol=1e-5, atol=1e-8, ignore_nodata=True):
    """Assert that two numpy arrays are approximately equal, handling nodata."""
    if ignore_nodata:
        # Create masks for nodata values
        mask1 = np.isfinite(arr1) if np.issubdtype(arr1.dtype, np.floating) else arr1 != -9999
        mask2 = np.isfinite(arr2) if np.issubdtype(arr2.dtype, np.floating) else arr2 != -9999

        # Only compare valid data
        valid_mask = mask1 & mask2
        if np.any(valid_mask):
            np.testing.assert_allclose(arr1[valid_mask], arr2[valid_mask], rtol=rtol, atol=atol)
    else:
        np.testing.assert_allclose(arr1, arr2, rtol=rtol, atol=atol)

def create_test_raster(width=100, height=80, bands=1, dtype='float32', crs='EPSG:4326',
                      bounds=(-110, 32, -109, 33), nodata=None):
    """Create a sample raster dataset for testing."""

    # Calculate transform
    transform = from_bounds(*bounds, width, height)

    # Create test data
    if bands == 1:
        # Single band with gradient pattern
        data = np.arange(width * height, dtype=dtype).reshape(height, width)
        data = (data / data.max() * 1000).astype(dtype)  # Scale to reasonable values
    else:
        # Multi-band with different patterns per band
        data = np.zeros((bands, height, width), dtype=dtype)
        for b in range(bands):
            band_data = np.random.random((height, width)) * (b + 1) * 100
            data[b] = band_data.astype(dtype)

    # Add some nodata values if specified
    if nodata is not None:
        if bands == 1:
            data[0:5, 0:5] = nodata
        else:
            data[:, 0:5, 0:5] = nodata

    # Create profile
    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': bands,
        'dtype': dtype,
        'crs': crs,
        'transform': transform,
        'compress': 'lzw',
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256
    }

    if nodata is not None:
        profile['nodata'] = nodata

    return data, profile

def create_landsat_like_raster():
    """Create a Landsat-like multispectral raster for testing."""
    # Landsat bands: Blue, Green, Red, NIR, SWIR1, SWIR2
    bands = 6
    width, height = 512, 512

    data = np.zeros((bands, height, width), dtype='uint16')

    # Simulate realistic Landsat values (scaled by 10000)
    np.random.seed(42)  # Reproducible
    base_pattern = np.random.random((height, width))

    # Band 1 (Blue): Lower values
    data[0] = (base_pattern * 0.8 + 0.1) * 2000

    # Band 2 (Green): Medium values
    data[1] = (base_pattern * 0.9 + 0.15) * 2500

    # Band 3 (Red): Medium-high values
    data[2] = (base_pattern * 1.0 + 0.2) * 3000

    # Band 4 (NIR): High values (vegetation)
    data[3] = (base_pattern * 1.2 + 0.3) * 4000

    # Band 5 (SWIR1): Medium values
    data[4] = (base_pattern * 0.8 + 0.25) * 2800

    # Band 6 (SWIR2): Lower values
    data[5] = (base_pattern * 0.6 + 0.15) * 2200

    # Ensure values are within uint16 range
    data = np.clip(data, 0, 65535).astype('uint16')

    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': bands,
        'dtype': 'uint16',
        'crs': 'EPSG:32612',  # UTM Zone 12N (Arizona)
        'transform': from_bounds(400000, 3600000, 415360, 3615360, width, height),
        'nodata': 0,
        'compress': 'lzw',
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256
    }

    return data, profile

def create_dem_raster():
    """Create a Digital Elevation Model raster for testing."""
    width, height = 200, 150

    # Create elevation data with realistic topography
    x = np.linspace(0, 10, width)
    y = np.linspace(0, 7.5, height)
    X, Y = np.meshgrid(x, y)

    # Simulate mountain/valley topography
    elevation = (
        1000 +  # Base elevation
        500 * np.sin(X * 0.8) * np.cos(Y * 0.6) +  # Large features
        200 * np.sin(X * 2.0) * np.sin(Y * 1.5) +   # Medium features
        50 * np.random.random((height, width))       # Small noise
    )

    elevation = elevation.astype('float32')

    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:32612',  # UTM Zone 12N
        'transform': from_bounds(400000, 3600000, 410000, 3607500, width, height),
        'nodata': -9999.0,
        'compress': 'lzw',
        'tiled': True,
        'blockxsize': 128,
        'blockysize': 128
    }

    return elevation, profile

def write_test_raster(data, profile, filepath):
    """Write test raster data to file."""
    with rasterio.open(filepath, 'w', **profile) as dst:
        if len(data.shape) == 2:
            dst.write(data, 1)
        else:
            for i in range(data.shape[0]):
                dst.write(data[i], i + 1)

# Test fixtures - these can be used by importing from tests
def get_test_single_band():
    """Get test single-band raster data and profile."""
    return create_test_raster(width=100, height=80, bands=1, dtype='float32')

def get_test_multiband():
    """Get test multi-band raster data and profile."""
    return create_test_raster(width=100, height=80, bands=6, dtype='uint16', nodata=0)

def get_test_landsat():
    """Get Landsat-like test data."""
    return create_landsat_like_raster()

def get_test_dem():
    """Get DEM test data."""
    return create_dem_raster()

# Temporary file handling
@pytest.fixture
def tmp_raster_file():
    """Create temporary raster file for testing."""
    fd, path = tempfile.mkstemp(suffix='.tif')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)

# Tolerance for floating point comparisons
RASTER_TOLERANCE = 1e-6
COG_TOLERANCE = 1e-4
NDVI_TOLERANCE = 1e-3

# Common test data bounds (Phoenix, AZ area)
PHOENIX_BOUNDS = (-112.5, 33.0, -111.5, 34.0)
TEST_CRS = 'EPSG:4326'
TEST_UTM_CRS = 'EPSG:32612'

print(f"Rasterio Tests Package v{__version__} initialized")
print(f"Test utilities available: assert_raster_*, create_test_*, get_test_* fixtures")
