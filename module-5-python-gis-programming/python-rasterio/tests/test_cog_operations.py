"""
Test suite for COG operations functionality.

This module contains comprehensive tests for Cloud-Optimized GeoTIFF operations
in the rasterio_analysis.cog_operations module, including COG validation,
optimization, remote access, and performance testing.

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
import requests
import time

# Import the functions we're testing
try:
    from src.rasterio_analysis.cog_operations import (
        COGProcessor,
        validate_cog_structure,
        optimize_for_cog,
        read_cog_efficiently,
        compare_cog_performance,
        generate_cog_metadata
    )
except ImportError as e:
    pytest.skip(f"Could not import COG operations functions: {e}", allow_module_level=True)


class TestCOGOperations:
    """Test suite for COG operations functionality."""

    @pytest.fixture(scope="class")
    def standard_raster_path(self, tmp_path_factory):
        """Create a standard (non-COG) raster for testing COG conversion."""
        tmp_dir = tmp_path_factory.mktemp("cog_test_data")
        raster_path = tmp_dir / "standard_raster.tif"

        # Create a reasonably sized raster for COG testing
        width, height = 2048, 1536
        bands = 3

        # Generate synthetic RGB data
        np.random.seed(42)  # For reproducible tests
        red = np.random.randint(0, 255, (height, width), dtype=np.uint8)
        green = np.random.randint(0, 255, (height, width), dtype=np.uint8)
        blue = np.random.randint(0, 255, (height, width), dtype=np.uint8)

        imagery = np.stack([red, green, blue])

        bounds = (-120.0, 35.0, -119.0, 36.0)  # California area
        transform = from_bounds(*bounds, width, height)

        # Write standard raster (not COG optimized)
        with rasterio.open(
            raster_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=imagery.dtype,
            crs='EPSG:4326',
            transform=transform,
            compress='lzw',
            tiled=False  # Non-tiled to ensure it's not COG
        ) as dst:
            for i in range(bands):
                dst.write(imagery[i], i + 1)

        return raster_path

    @pytest.fixture(scope="class")
    def cog_raster_path(self, tmp_path_factory):
        """Create a COG-optimized raster for testing."""
        tmp_dir = tmp_path_factory.mktemp("cog_optimized")
        cog_path = tmp_dir / "test_cog.tif"

        width, height = 1024, 768

        # Create elevation-like data
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 8, height)
        X, Y = np.meshgrid(x, y)
        elevation = 1000 + 200 * np.sin(X) + 150 * np.cos(Y) + np.random.random((height, width)) * 50
        elevation = elevation.astype(np.float32)

        bounds = (-111.0, 33.0, -110.0, 34.0)  # Arizona area
        transform = from_bounds(*bounds, width, height)

        # Create COG-optimized raster
        with rasterio.open(
            cog_path, 'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=elevation.dtype,
            crs='EPSG:4326',
            transform=transform,
            compress='lzw',
            tiled=True,
            blockxsize=512,
            blockysize=512,
            interleave='pixel'
        ) as dst:
            dst.write(elevation, 1)
            # Build overviews for COG compliance
            dst.build_overviews([2, 4, 8], Resampling.average)

        return cog_path

    def test_cog_processor_initialization(self):
        """Test COGProcessor class initialization."""
        processor = COGProcessor()

        # Check default values
        assert hasattr(processor, 'session')
        assert processor.session_timeout == 30
        assert processor.max_retries == 3

        # Test custom initialization
        custom_processor = COGProcessor(session_timeout=60, max_retries=5)
        assert custom_processor.session_timeout == 60
        assert custom_processor.max_retries == 5

    def test_validate_cog_structure_valid_cog(self, cog_raster_path):
        """Test COG validation with a valid COG file."""
        result = validate_cog_structure(cog_raster_path)

        # Check result structure
        required_keys = [
            'is_valid_cog', 'validation_details', 'optimization_score',
            'issues_found', 'recommendations', 'file_info'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Should be a valid COG
        assert result['is_valid_cog'] == True
        assert result['optimization_score'] > 70  # Should score well

        # Check validation details
        details = result['validation_details']
        assert details['is_tiled'] == True
        assert len(details['overview_count']) > 0
        assert details['has_internal_overviews'] == True

    def test_validate_cog_structure_standard_raster(self, standard_raster_path):
        """Test COG validation with a standard (non-COG) raster."""
        result = validate_cog_structure(standard_raster_path)

        # Should not be a valid COG
        assert result['is_valid_cog'] == False
        assert result['optimization_score'] < 50  # Should score poorly

        # Should identify specific issues
        issues = result['issues_found']
        assert any('tiled' in issue.lower() for issue in issues)

        # Should provide recommendations
        recommendations = result['recommendations']
        assert len(recommendations) > 0
        assert any('tile' in rec.lower() or 'overview' in rec.lower() for rec in recommendations)

    def test_validate_cog_structure_invalid_file(self, tmp_path):
        """Test COG validation with invalid file."""
        invalid_file = tmp_path / "not_a_raster.txt"
        invalid_file.write_text("This is not a raster file")

        with pytest.raises(FileNotFoundError):
            validate_cog_structure("nonexistent.tif")

        # Invalid raster format should be handled gracefully
        result = validate_cog_structure(invalid_file)
        assert result['is_valid_cog'] == False
        assert 'invalid file format' in str(result['issues_found']).lower()

    def test_optimize_for_cog_basic(self, standard_raster_path, tmp_path):
        """Test basic COG optimization functionality."""
        output_path = tmp_path / "optimized_cog.tif"

        result = optimize_for_cog(
            standard_raster_path,
            output_path,
            tile_size=512,
            compression='lzw',
            overview_levels=[2, 4, 8]
        )

        # Check output file exists
        assert output_path.exists()

        # Check result structure
        required_keys = [
            'input_file', 'output_file', 'optimization_settings',
            'file_size_reduction', 'cog_validation', 'processing_time',
            'performance_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Verify optimization settings
        settings = result['optimization_settings']
        assert settings['tile_size'] == 512
        assert settings['compression'] == 'lzw'
        assert settings['overview_levels'] == [2, 4, 8]

        # Verify the output is actually COG-compliant
        with rasterio.open(output_path) as src:
            assert src.is_tiled == True
            assert src.block_shapes[0] == (512, 512)
            assert len(src.overviews(1)) > 0

    def test_optimize_for_cog_different_compressions(self, standard_raster_path, tmp_path):
        """Test COG optimization with different compression methods."""
        compression_methods = ['lzw', 'deflate', 'jpeg']

        for compression in compression_methods:
            output_path = tmp_path / f"cog_{compression}.tif"

            result = optimize_for_cog(
                standard_raster_path,
                output_path,
                compression=compression
            )

            assert output_path.exists()
            assert result['optimization_settings']['compression'] == compression

            # Verify compression was applied
            with rasterio.open(output_path) as src:
                if compression == 'jpeg':
                    # JPEG might not be available for all data types
                    assert src.compression.value in ['jpeg', 'lzw']  # Fallback acceptable
                else:
                    assert src.compression.value == compression

    def test_optimize_for_cog_custom_tile_sizes(self, standard_raster_path, tmp_path):
        """Test COG optimization with different tile sizes."""
        tile_sizes = [256, 512, 1024]

        for tile_size in tile_sizes:
            output_path = tmp_path / f"cog_tile_{tile_size}.tif"

            result = optimize_for_cog(
                standard_raster_path,
                output_path,
                tile_size=tile_size
            )

            assert output_path.exists()

            # Verify tile size
            with rasterio.open(output_path) as src:
                assert src.block_shapes[0] == (tile_size, tile_size)

    @patch('requests.get')
    def test_read_cog_efficiently_mock_remote(self, mock_get):
        """Test efficient COG reading with mocked remote access."""
        # Mock response for remote COG
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-length': '1000000'}
        mock_get.return_value = mock_response

        cog_url = "https://example.com/test.cog.tif"

        # Mock rasterio operations
        with patch('src.rasterio_analysis.cog_operations.rasterio.open') as mock_open:
            mock_src = MagicMock()
            mock_src.width = 4096
            mock_src.height = 4096
            mock_src.count = 1
            mock_src.is_tiled = True
            mock_src.overviews.return_value = [2, 4, 8]
            mock_src.block_shapes = [(512, 512)]

            # Mock data reading
            mock_data = np.random.randint(0, 1000, (512, 512), dtype=np.uint16)
            mock_src.read.return_value = mock_data

            mock_open.return_value.__enter__ = MagicMock(return_value=mock_src)
            mock_open.return_value.__exit__ = MagicMock(return_value=None)

            result = read_cog_efficiently(
                cog_url,
                bbox=(-120, 35, -119, 36),
                max_resolution=100
            )

            # Check result structure
            required_keys = [
                'data', 'metadata', 'read_strategy', 'performance_info', 'bbox_used'
            ]
            for key in required_keys:
                assert key in result, f"Missing required key: {key}"

            # Check data was returned
            assert result['data'] is not None
            assert isinstance(result['data'], np.ndarray)

            # Check metadata
            metadata = result['metadata']
            assert 'dimensions' in metadata
            assert 'overview_levels' in metadata

    def test_read_cog_efficiently_local_file(self, cog_raster_path):
        """Test efficient COG reading with local file."""
        result = read_cog_efficiently(
            cog_raster_path,
            bbox=(-111.0, 33.0, -110.5, 33.5),
            target_resolution=50
        )

        # Check result structure
        required_keys = [
            'data', 'metadata', 'read_strategy', 'performance_info', 'bbox_used'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check data
        assert result['data'] is not None
        assert isinstance(result['data'], np.ndarray)
        assert result['data'].ndim in [2, 3]  # 2D or 3D array

        # Check performance info
        perf_info = result['performance_info']
        assert 'read_time_seconds' in perf_info
        assert 'data_size_mb' in perf_info

    def test_compare_cog_performance(self, standard_raster_path, tmp_path):
        """Test COG performance comparison functionality."""
        # Create COG version for comparison
        cog_path = tmp_path / "comparison_cog.tif"
        optimize_for_cog(standard_raster_path, cog_path)

        result = compare_cog_performance(
            standard_raster=standard_raster_path,
            cog_raster=cog_path,
            test_scenarios=['full_read', 'window_read', 'overview_read']
        )

        # Check result structure
        required_keys = [
            'test_scenarios', 'standard_performance', 'cog_performance',
            'performance_improvements', 'recommendations'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check that performance tests ran
        assert len(result['test_scenarios']) > 0

        # Check performance metrics exist
        for raster_type in ['standard_performance', 'cog_performance']:
            perf = result[raster_type]
            assert 'full_read' in perf
            assert 'read_time_seconds' in perf['full_read']

    def test_generate_cog_metadata(self, cog_raster_path):
        """Test COG metadata generation."""
        result = generate_cog_metadata(
            cog_raster_path,
            include_statistics=True,
            include_histogram=True
        )

        # Check result structure
        required_keys = [
            'file_info', 'cog_properties', 'spatial_info', 'band_info',
            'optimization_info', 'access_patterns'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check file info
        file_info = result['file_info']
        assert 'file_size_mb' in file_info
        assert 'creation_time' in file_info

        # Check COG properties
        cog_props = result['cog_properties']
        assert 'is_valid_cog' in cog_props
        assert 'tile_size' in cog_props
        assert 'overview_count' in cog_props

        # Check spatial info
        spatial_info = result['spatial_info']
        assert 'crs' in spatial_info
        assert 'bounds' in spatial_info
        assert 'resolution' in spatial_info


class TestCOGProcessor:
    """Test the COGProcessor class functionality."""

    def test_cog_processor_context_manager(self):
        """Test COGProcessor as context manager."""
        with COGProcessor() as processor:
            assert processor is not None
            assert hasattr(processor, 'session')

    def test_cog_processor_batch_validation(self, tmp_path):
        """Test batch COG validation functionality."""
        processor = COGProcessor()

        # Create multiple test files
        test_files = []
        for i in range(3):
            file_path = tmp_path / f"test_{i}.tif"

            # Create simple raster
            data = np.random.randint(0, 100, (100, 100), dtype=np.uint8)
            with rasterio.open(
                file_path, 'w',
                driver='GTiff', height=100, width=100, count=1,
                dtype=data.dtype, crs='EPSG:4326',
                transform=from_bounds(-1, -1, 1, 1, 100, 100)
            ) as dst:
                dst.write(data, 1)

            test_files.append(file_path)

        results = processor.validate_multiple_cogs(test_files)

        # Check results structure
        assert isinstance(results, dict)
        assert len(results) == len(test_files)

        for file_path in test_files:
            assert str(file_path) in results
            result = results[str(file_path)]
            assert 'is_valid_cog' in result
            assert 'validation_details' in result

    def test_cog_processor_optimization_workflow(self, standard_raster_path, tmp_path):
        """Test COG optimization workflow through processor."""
        processor = COGProcessor()

        output_path = tmp_path / "workflow_cog.tif"

        result = processor.optimize_raster_to_cog(
            standard_raster_path,
            output_path,
            optimization_profile='web_optimized'
        )

        # Check that optimization completed
        assert output_path.exists()
        assert result['success'] == True
        assert 'optimization_profile' in result
        assert result['optimization_profile'] == 'web_optimized'


class TestCOGEdgeCases:
    """Test edge cases and error conditions for COG operations."""

    def test_cog_validation_corrupted_file(self, tmp_path):
        """Test COG validation with corrupted file."""
        corrupted_file = tmp_path / "corrupted.tif"

        # Create file with invalid TIFF header
        with open(corrupted_file, 'wb') as f:
            f.write(b'Not a TIFF file header')

        result = validate_cog_structure(corrupted_file)
        assert result['is_valid_cog'] == False
        assert len(result['issues_found']) > 0

    def test_cog_optimization_edge_cases(self, tmp_path):
        """Test COG optimization with edge cases."""
        # Create very small raster
        small_raster = tmp_path / "small.tif"
        data = np.random.randint(0, 100, (10, 10), dtype=np.uint8)

        with rasterio.open(
            small_raster, 'w',
            driver='GTiff', height=10, width=10, count=1,
            dtype=data.dtype, crs='EPSG:4326',
            transform=from_bounds(-1, -1, 1, 1, 10, 10)
        ) as dst:
            dst.write(data, 1)

        output_path = tmp_path / "small_cog.tif"

        # Should handle small rasters gracefully
        result = optimize_for_cog(small_raster, output_path, tile_size=512)
        assert output_path.exists()

        # Small raster might not need tiling, but should still be valid
        assert result['success'] == True

    def test_memory_efficient_cog_reading(self, cog_raster_path):
        """Test memory-efficient reading of large COG sections."""
        # Test reading multiple small windows efficiently
        windows = [
            (-110.8, 33.2, -110.6, 33.4),  # Small bbox 1
            (-110.6, 33.4, -110.4, 33.6),  # Small bbox 2
            (-110.4, 33.6, -110.2, 33.8),  # Small bbox 3
        ]

        results = []
        for bbox in windows:
            result = read_cog_efficiently(
                cog_raster_path,
                bbox=bbox,
                memory_limit_mb=50  # Small memory limit
            )
            results.append(result)

            # Each result should be small and efficient
            assert result['performance_info']['data_size_mb'] < 10

        # All reads should have completed successfully
        assert len(results) == len(windows)

    def test_concurrent_cog_access(self, cog_raster_path):
        """Test concurrent access to COG file."""
        import threading

        results = []
        errors = []

        def read_cog_section(bbox):
            try:
                result = read_cog_efficiently(cog_raster_path, bbox=bbox)
                results.append(result)
            except Exception as e:
                errors.append(e)

        # Create multiple threads reading different sections
        threads = []
        bboxes = [
            (-110.9, 33.1, -110.8, 33.2),
            (-110.8, 33.2, -110.7, 33.3),
            (-110.7, 33.3, -110.6, 33.4),
            (-110.6, 33.4, -110.5, 33.5),
        ]

        for bbox in bboxes:
            thread = threading.Thread(target=read_cog_section, args=(bbox,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Should have no errors and all results
        assert len(errors) == 0
        assert len(results) == len(bboxes)
