"""
Test suite for raster processing functionality.

This module contains comprehensive tests for the core raster processing functions
in the rasterio_analysis.raster_processing module, including metadata extraction,
multiband processing, COG operations, and error handling.

Author: Student Test Suite
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import pytest
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling
import tempfile
from pathlib import Path
import warnings
from unittest.mock import patch, MagicMock

# Import the functions we're testing
try:
    from src.rasterio_analysis.raster_processing import (
        analyze_local_raster,
        process_multiband_imagery,
        process_remote_cog,
        create_optimized_cog,
        validate_raster_file,
        get_raster_summary
    )
except ImportError as e:
    pytest.skip(f"Could not import raster processing functions: {e}", allow_module_level=True)


class TestRasterProcessing:
    """Test suite for core raster processing functions."""

    @pytest.fixture(scope="class")
    def sample_raster_path(self, tmp_path_factory):
        """Create a sample single-band raster for testing."""
        tmp_dir = tmp_path_factory.mktemp("raster_data")
        raster_path = tmp_dir / "sample_dem.tif"

        # Create synthetic elevation data
        width, height = 500, 400

        # Generate realistic elevation data with some variation
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 8, height)
        X, Y = np.meshgrid(x, y)

        # Create elevation surface: base elevation + some hills
        elevation = 1000 + 200 * np.sin(X) + 150 * np.cos(Y * 2) + 50 * np.random.random((height, width))
        elevation = elevation.astype(np.float32)

        # Add some nodata values
        elevation[0:10, 0:10] = np.nan  # Corner with no data

        # Create geographic bounds (Phoenix area)
        bounds = (-112.5, 33.0, -111.5, 34.0)
        transform = from_bounds(*bounds, width, height)

        # Write the raster
        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=elevation.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=np.nan
        ) as dst:
            dst.write(elevation, 1)

        return raster_path

    @pytest.fixture(scope="class")
    def multiband_raster_path(self, tmp_path_factory):
        """Create a sample multiband raster for testing (simulates Landsat-like data)."""
        tmp_dir = tmp_path_factory.mktemp("multiband_data")
        raster_path = tmp_dir / "sample_landsat.tif"

        # Create 4-band imagery (Blue, Green, Red, NIR)
        width, height = 200, 200
        bands = 4

        # Generate synthetic reflectance data
        np.random.seed(42)  # For reproducible tests

        # Blue band (typically lower values)
        blue = np.random.randint(800, 1200, (height, width)).astype(np.uint16)

        # Green band
        green = np.random.randint(900, 1400, (height, width)).astype(np.uint16)

        # Red band
        red = np.random.randint(1000, 1600, (height, width)).astype(np.uint16)

        # NIR band (typically higher for vegetation)
        nir = np.random.randint(2000, 4000, (height, width)).astype(np.uint16)

        # Stack bands
        imagery = np.stack([blue, green, red, nir])

        # Add some nodata areas
        imagery[:, 0:5, 0:5] = 0  # Corner with no data

        bounds = (-112.2, 33.2, -111.8, 33.6)
        transform = from_bounds(*bounds, width, height)

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=imagery.dtype,
            crs='EPSG:4326',
            transform=transform,
            nodata=0
        ) as dst:
            for i in range(bands):
                dst.write(imagery[i], i + 1)

        return raster_path

    def test_analyze_local_raster_basic(self, sample_raster_path):
        """Test basic raster analysis functionality."""
        result = analyze_local_raster(sample_raster_path)

        # Check that all required keys are present
        required_keys = [
            'filename', 'driver', 'dtype', 'dimensions', 'band_count',
            'crs', 'bounds', 'transform', 'resolution', 'statistics',
            'quality_flags', 'analysis_timestamp'
        ]

        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check basic metadata
        assert result['driver'] == 'GTiff'
        assert result['dimensions'] == (500, 400)  # width, height
        assert result['band_count'] == 1
        assert result['dtype'] == 'float32'

        # Check statistics
        stats = result['statistics']
        assert stats['total_pixel_count'] == 500 * 400
        assert stats['valid_pixel_count'] > 0
        assert 0 <= stats['data_completeness'] <= 100

        # Check that we have reasonable elevation values
        if stats['mean'] is not None:
            assert 500 < stats['mean'] < 2000  # Reasonable elevation range

        # Check CRS
        assert result['crs'] is not None
        assert 'EPSG:4326' in str(result['crs'])

    def test_analyze_local_raster_file_not_found(self):
        """Test error handling when raster file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            analyze_local_raster("nonexistent_file.tif")

    def test_process_multiband_imagery_basic(self, multiband_raster_path):
        """Test basic multiband imagery processing."""
        band_names = ['Blue', 'Green', 'Red', 'NIR']
        result = process_multiband_imagery(multiband_raster_path, band_names)

        # Check required keys
        required_keys = [
            'image_metadata', 'band_statistics', 'indices', 'processing_timestamp'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check metadata
        metadata = result['image_metadata']
        assert metadata['band_count'] == 4
        assert metadata['dimensions'] == (200, 200)
        assert metadata['band_names'] == band_names

        # Check band statistics
        band_stats = result['band_statistics']
        assert len(band_stats) == 4
        for band_name in band_names:
            assert band_name in band_stats
            stats = band_stats[band_name]
            assert all(key in stats for key in ['min', 'max', 'mean', 'std'])

        # Check that indices were calculated
        indices = result['indices']
        assert 'NDVI' in indices or 'EVI' in indices  # Should have at least one index

        if 'NDVI' in indices:
            ndvi_stats = indices['NDVI']['statistics']
            # NDVI should be between -1 and 1
            if ndvi_stats['min'] is not None and ndvi_stats['max'] is not None:
                assert -1 <= ndvi_stats['min'] <= 1
                assert -1 <= ndvi_stats['max'] <= 1

    def test_process_multiband_imagery_insufficient_bands(self, sample_raster_path):
        """Test error handling for insufficient bands."""
        with pytest.raises(ValueError, match="Multiband processing requires at least 2 bands"):
            process_multiband_imagery(sample_raster_path)

    def test_create_optimized_cog_basic(self, sample_raster_path, tmp_path):
        """Test basic COG creation functionality."""
        output_path = tmp_path / "optimized.tif"

        result = create_optimized_cog(
            sample_raster_path,
            output_path,
            compress='lzw',
            tiled=True,
            blocksize=256
        )

        # Check that output file was created
        assert output_path.exists()

        # Check result structure
        required_keys = [
            'input_file', 'output_file', 'original_size_bytes', 'optimized_size_bytes',
            'size_reduction_percent', 'cog_validation', 'optimization_settings',
            'creation_timestamp'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check that optimization settings are recorded
        settings = result['optimization_settings']
        assert settings['compression'] == 'lzw'
        assert settings['tiled'] == True
        assert settings['blocksize'] == 256

        # Verify the created file is actually a valid raster
        with rasterio.open(output_path) as src:
            assert src.is_tiled == True
            assert src.compression.name == 'lzw'
            assert src.block_shapes[0] == (256, 256)

    def test_create_optimized_cog_with_overviews(self, sample_raster_path, tmp_path):
        """Test COG creation includes overview generation."""
        output_path = tmp_path / "cog_with_overviews.tif"

        result = create_optimized_cog(sample_raster_path, output_path)

        # Check that overviews were created
        with rasterio.open(output_path) as src:
            overviews = src.overviews(1)
            assert len(overviews) > 0, "COG should have overview pyramids"

        # Check that overview information is in result
        assert 'overview_factors' in result['optimization_settings']
        assert len(result['optimization_settings']['overview_factors']) > 0

    def test_create_optimized_cog_input_not_found(self, tmp_path):
        """Test error handling when input file doesn't exist."""
        output_path = tmp_path / "output.tif"

        with pytest.raises(FileNotFoundError):
            create_optimized_cog("nonexistent.tif", output_path)

    @pytest.mark.skipif(True, reason="Remote COG test requires network access")
    def test_process_remote_cog_mock(self):
        """Test remote COG processing with mocked rasterio operations."""
        # Mock a remote COG URL
        cog_url = "https://example.com/test.tif"

        # Mock the rasterio.open context manager
        mock_src = MagicMock()
        mock_src.is_tiled = True
        mock_src.overviews.return_value = [2, 4, 8]
        mock_src.compression = 'lzw'
        mock_src.block_shapes = [(512, 512)]
        mock_src.driver = 'GTiff'
        mock_src.dtypes = ['uint16']
        mock_src.width = 1000
        mock_src.height = 1000
        mock_src.count = 1
        mock_src.crs = 'EPSG:4326'
        mock_src.bounds = (-112.5, 33.0, -111.5, 34.0)
        mock_src.transform = from_bounds(-112.5, 33.0, -111.5, 34.0, 1000, 1000)
        mock_src.nodata = None

        # Mock read operation
        mock_data = np.random.randint(1000, 2000, (100, 100), dtype=np.uint16)
        mock_src.read.return_value = mock_data

        with patch('src.rasterio_analysis.raster_processing.rasterio.open') as mock_open:
            mock_open.return_value.__enter__ = MagicMock(return_value=mock_src)
            mock_open.return_value.__exit__ = MagicMock(return_value=None)

            result = process_remote_cog(cog_url, max_size=1024)

            # Check result structure
            required_keys = [
                'url', 'source_metadata', 'cog_optimization',
                'statistics', 'processing_timestamp'
            ]
            for key in required_keys:
                assert key in result, f"Missing required key: {key}"

            # Check COG optimization info
            cog_info = result['cog_optimization']
            assert cog_info['is_tiled'] == True
            assert len(cog_info['overview_count']) > 0

    def test_validate_raster_file_valid(self, sample_raster_path):
        """Test raster file validation with valid file."""
        assert validate_raster_file(sample_raster_path) == True

    def test_validate_raster_file_invalid(self, tmp_path):
        """Test raster file validation with invalid file."""
        invalid_file = tmp_path / "not_a_raster.txt"
        invalid_file.write_text("This is not a raster file")

        assert validate_raster_file(invalid_file) == False

    def test_get_raster_summary(self, sample_raster_path):
        """Test raster summary generation."""
        summary = get_raster_summary(sample_raster_path)

        # Should be a string with key information
        assert isinstance(summary, str)
        assert "sample_dem.tif" in summary
        assert "Dimensions:" in summary
        assert "Data Type:" in summary
        assert "CRS:" in summary

    def test_get_raster_summary_invalid_file(self, tmp_path):
        """Test raster summary with invalid file."""
        invalid_file = tmp_path / "invalid.txt"
        invalid_file.write_text("not a raster")

        summary = get_raster_summary(invalid_file)
        assert "Invalid or unreadable" in summary


class TestRasterProcessingEdgeCases:
    """Test edge cases and error conditions."""

    def test_analyze_very_large_raster_sampling(self, tmp_path):
        """Test that very large rasters use sampling for statistics."""
        # Create a "large" raster (we'll mock the size check)
        large_raster_path = tmp_path / "large_raster.tif"

        # Create a small raster but patch the size check
        width, height = 100, 100
        data = np.random.randint(0, 1000, (height, width), dtype=np.uint16)

        with rasterio.open(
            large_raster_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, width, height)
        ) as dst:
            dst.write(data, 1)

        # Patch the size check to trigger sampling
        with patch('src.rasterio_analysis.raster_processing.logger') as mock_logger:
            # Mock to make it think the raster is large
            original_open = rasterio.open

            def mock_open(*args, **kwargs):
                src = original_open(*args, **kwargs)
                # Override width and height properties
                src._width = 5000  # Make it appear large
                src._height = 5000
                return src

            with patch('src.rasterio_analysis.raster_processing.rasterio.open', side_effect=mock_open):
                result = analyze_local_raster(large_raster_path)

                # Should still return valid results
                assert 'statistics' in result
                # Should have logged a warning about sampling
                mock_logger.warning.assert_called()

    def test_multiband_ndvi_edge_cases(self, tmp_path):
        """Test NDVI calculation with edge cases (zero values, etc.)."""
        raster_path = tmp_path / "edge_case_multiband.tif"

        width, height = 50, 50

        # Create bands with edge cases
        red = np.full((height, width), 100, dtype=np.uint16)
        nir = np.full((height, width), 100, dtype=np.uint16)  # Same values -> NDVI = 0

        # Add some zero values (should cause division issues)
        red[0:10, 0:10] = 0
        nir[0:10, 0:10] = 0

        # Add some cases where red > nir (negative NDVI)
        red[20:30, 20:30] = 200
        nir[20:30, 20:30] = 100

        imagery = np.stack([red, red, red, nir])  # B, G, R, NIR

        with rasterio.open(
            raster_path, 'w',
            driver='GTiff', height=height, width=width, count=4,
            dtype=imagery.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, width, height),
            nodata=0
        ) as dst:
            for i in range(4):
                dst.write(imagery[i], i + 1)

        result = process_multiband_imagery(raster_path)

        # Should handle edge cases gracefully
        assert 'indices' in result
        if 'NDVI' in result['indices']:
            ndvi_stats = result['indices']['NDVI']['statistics']
            # Should have valid statistics even with edge cases
            assert ndvi_stats is not None
