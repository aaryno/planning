"""
COG Operations Module - Cloud-Optimized GeoTIFF Processing

This module provides specialized functionality for working with Cloud-Optimized
GeoTIFFs (COGs), including remote access, validation, optimization, and
efficient partial reading strategies.

Author: Student
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from urllib.parse import urlparse
import time

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
from rasterio.warp import calculate_default_transform, reproject
from rasterio.crs import CRS
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress common warnings for cleaner output
warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)


class COGProcessor:
    """
    A class for comprehensive COG processing operations.

    This class encapsulates methods for working with Cloud-Optimized GeoTIFFs,
    including validation, optimization, and efficient access patterns.
    """

    def __init__(self, session_timeout: int = 30, max_retries: int = 3):
        """
        Initialize COG processor with HTTP session configuration.

        Args:
            session_timeout: Timeout for HTTP requests in seconds
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.timeout = session_timeout

        logger.info(f"COG Processor initialized with {max_retries} retries and {session_timeout}s timeout")


def validate_cog(file_path: Union[str, Path],
                remote: bool = None) -> Dict[str, Any]:
    """
    Validate whether a file is a properly formatted Cloud-Optimized GeoTIFF.

    This function checks for all the requirements of a valid COG:
    - Tiled structure
    - Overview pyramids
    - Proper internal organization
    - Efficient access patterns

    Args:
        file_path: Path or URL to the GeoTIFF file
        remote: Whether to treat as remote file (auto-detected if None)

    Returns:
        Dictionary containing validation results and recommendations

    Example:
        >>> validation = validate_cog("https://example.com/data.tif")
        >>> if validation['is_valid_cog']:
        ...     print("✅ Valid COG")
        >>> else:
        ...     print("❌ Issues found:", validation['issues'])
    """
    file_path_str = str(file_path)

    # Auto-detect if remote
    if remote is None:
        remote = file_path_str.startswith(('http://', 'https://'))

    logger.info(f"Validating COG: {file_path} (remote: {remote})")

    validation_results = {
        'file_path': file_path_str,
        'is_remote': remote,
        'is_valid_cog': False,
        'issues': [],
        'warnings': [],
        'recommendations': [],
        'validation_timestamp': pd.Timestamp.now().isoformat(),
    }

    try:
        with rasterio.open(file_path_str) as src:
            # Basic file information
            validation_results['file_info'] = {
                'driver': src.driver,
                'width': src.width,
                'height': src.height,
                'band_count': src.count,
                'dtype': src.dtypes[0],
                'crs': src.crs,
                'compression': src.compression,
            }

            # Check 1: Must be GeoTIFF
            if src.driver != 'GTiff':
                validation_results['issues'].append(f"Not a GeoTIFF (driver: {src.driver})")
                return validation_results

            # Check 2: Must be tiled
            if not src.is_tiled:
                validation_results['issues'].append("Not tiled - COGs must use tiled structure")
            else:
                # Check tile size
                block_shape = src.block_shapes[0]
                if block_shape[0] != block_shape[1]:
                    validation_results['warnings'].append(
                        f"Non-square tiles ({block_shape}) may be less efficient"
                    )
                elif block_shape[0] < 256 or block_shape[0] > 1024:
                    validation_results['warnings'].append(
                        f"Tile size {block_shape[0]} not optimal (recommend 512x512)"
                    )

            # Check 3: Must have overviews
            overview_count = len(src.overviews(1))
            if overview_count == 0:
                validation_results['issues'].append("No overviews found - COGs require overview pyramids")
            else:
                # Analyze overview structure
                overviews = src.overviews(1)
                expected_levels = []
                max_dim = max(src.width, src.height)
                level = 2
                while max_dim // level >= 256:
                    expected_levels.append(level)
                    level *= 2

                validation_results['overview_analysis'] = {
                    'count': overview_count,
                    'factors': overviews,
                    'expected_factors': expected_levels,
                    'has_sufficient_levels': len(overviews) >= len(expected_levels) // 2,
                }

                if len(overviews) < len(expected_levels) // 2:
                    validation_results['warnings'].append(
                        f"Few overview levels ({len(overviews)}) for raster size"
                    )

            # Check 4: Compression analysis
            if src.compression is None:
                validation_results['warnings'].append("No compression - file size could be reduced")
                validation_results['recommendations'].append("Apply LZW or DEFLATE compression")

            # Check 5: Internal organization
            # For COGs, we want to ensure data is organized for efficient access
            try:
                # Check if we can efficiently access a small window
                test_window = Window(0, 0, min(256, src.width), min(256, src.height))
                start_time = time.time()
                _ = src.read(1, window=test_window)
                read_time = time.time() - start_time

                validation_results['performance'] = {
                    'small_window_read_time': read_time,
                    'is_fast_access': read_time < 0.5,  # Should be very fast for COG
                }

                if read_time > 1.0:
                    validation_results['warnings'].append("Slow random access - may not be optimized")

            except Exception as e:
                validation_results['warnings'].append(f"Could not test access performance: {e}")

            # Check 6: Pixel interleaving (should be 'pixel' for COGs)
            try:
                if hasattr(src, 'interleaving') and src.interleaving != 'pixel':
                    validation_results['warnings'].append(
                        f"Interleaving is {src.interleaving}, 'pixel' recommended for COGs"
                    )
            except:
                pass

            # Determine if it's a valid COG
            has_critical_issues = len(validation_results['issues']) > 0
            validation_results['is_valid_cog'] = not has_critical_issues

            # Generate recommendations
            if not validation_results['is_valid_cog']:
                validation_results['recommendations'].extend([
                    "Convert to tiled GeoTIFF with proper tile size (512x512 recommended)",
                    "Generate overview pyramids with powers of 2",
                    "Apply appropriate compression (LZW for most cases)",
                    "Use pixel interleaving for multiband imagery",
                ])

            # Summary
            status = "✅ Valid COG" if validation_results['is_valid_cog'] else "❌ Not a valid COG"
            issue_count = len(validation_results['issues'])
            warning_count = len(validation_results['warnings'])

            logger.info(f"Validation complete: {status} ({issue_count} issues, {warning_count} warnings)")

    except Exception as e:
        validation_results['issues'].append(f"Failed to read file: {str(e)}")
        logger.error(f"COG validation failed: {e}")

    return validation_results


def optimize_for_cog(input_path: Union[str, Path],
                    output_path: Union[str, Path],
                    compression: str = 'lzw',
                    tile_size: int = 512,
                    overview_resampling: Resampling = Resampling.average,
                    overview_min_size: int = 256) -> Dict[str, Any]:
    """
    Optimize a raster file for Cloud-Optimized GeoTIFF format.

    This function creates a properly formatted COG with tiling, compression,
    and overview pyramids optimized for cloud-based access patterns.

    Args:
        input_path: Path to input raster file
        output_path: Path for optimized COG output
        compression: Compression algorithm ('lzw', 'deflate', 'jpeg', etc.)
        tile_size: Tile size in pixels (should be power of 2)
        overview_resampling: Resampling method for overviews
        overview_min_size: Minimum size for generating overviews

    Returns:
        Dictionary containing optimization results and metrics

    Example:
        >>> result = optimize_for_cog("large_raster.tif", "optimized.tif")
        >>> print(f"COG created with {result['overview_count']} overviews")
        >>> print(f"File size reduced by {result['size_reduction_percent']:.1f}%")
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Optimizing raster for COG: {input_path} -> {output_path}")

    # Get original file size
    original_size = input_path.stat().st_size
    start_time = time.time()

    with rasterio.open(input_path) as src:
        # Create optimized profile
        profile = src.profile.copy()

        # COG-specific settings
        cog_profile = {
            'driver': 'GTiff',
            'tiled': True,
            'blockxsize': tile_size,
            'blockysize': tile_size,
            'compress': compression,
            'interleave': 'pixel',
            'BIGTIFF': 'IF_SAFER',
        }

        # Add predictor for better compression
        if compression.lower() in ['lzw', 'deflate']:
            if src.dtypes[0] in ['uint16', 'int16', 'uint32', 'int32']:
                cog_profile['predictor'] = 2  # Horizontal differencing
            elif src.dtypes[0] in ['float32', 'float64']:
                cog_profile['predictor'] = 3  # Floating point predictor

        profile.update(cog_profile)

        logger.info(f"COG settings: {tile_size}x{tile_size} tiles, {compression} compression")

        # Write the optimized raster
        with rasterio.open(output_path, 'w', **profile) as dst:
            # Copy data band by band for memory efficiency
            for band_idx in range(1, src.count + 1):
                logger.debug(f"Processing band {band_idx}/{src.count}")

                # For very large rasters, process in chunks
                if src.width * src.height > 50_000_000:  # ~50M pixels
                    # Process in windows
                    window_size = 2048
                    for row in range(0, src.height, window_size):
                        for col in range(0, src.width, window_size):
                            window = Window(
                                col, row,
                                min(window_size, src.width - col),
                                min(window_size, src.height - row)
                            )
                            data = src.read(band_idx, window=window)
                            dst.write(data, band_idx, window=window)
                else:
                    # Read entire band
                    data = src.read(band_idx)
                    dst.write(data, band_idx)

            # Copy metadata
            dst.update_tags(**src.tags())
            for band_idx in range(1, src.count + 1):
                dst.update_tags(band_idx, **src.tags(band_idx))

    # Build overviews
    logger.info("Building overview pyramids...")
    with rasterio.open(output_path, 'r+') as dst:
        # Calculate overview levels
        overview_factors = []
        max_dimension = max(dst.width, dst.height)
        factor = 2

        while max_dimension // factor >= overview_min_size:
            overview_factors.append(factor)
            factor *= 2

        if overview_factors:
            dst.build_overviews(overview_factors, overview_resampling)
            dst.update_tags(ns='rio_overview', resampling=overview_resampling.name)
            logger.info(f"Created {len(overview_factors)} overview levels: {overview_factors}")
        else:
            logger.warning("No overviews created - raster may be too small")

    # Calculate optimization results
    processing_time = time.time() - start_time
    optimized_size = output_path.stat().st_size
    size_reduction = ((original_size - optimized_size) / original_size) * 100

    # Validate the created COG
    validation = validate_cog(output_path, remote=False)

    results = {
        'input_file': str(input_path),
        'output_file': str(output_path),
        'original_size_bytes': original_size,
        'optimized_size_bytes': optimized_size,
        'size_reduction_percent': size_reduction,
        'processing_time_seconds': processing_time,
        'optimization_settings': {
            'compression': compression,
            'tile_size': tile_size,
            'overview_resampling': overview_resampling.name,
            'overview_min_size': overview_min_size,
        },
        'overview_count': len(overview_factors),
        'overview_factors': overview_factors,
        'is_valid_cog': validation['is_valid_cog'],
        'cog_validation': validation,
        'optimization_timestamp': pd.Timestamp.now().isoformat(),
    }

    status = "✅" if validation['is_valid_cog'] else "⚠️"
    logger.info(f"{status} COG optimization complete in {processing_time:.1f}s")
    logger.info(f"Size change: {size_reduction:+.1f}% ({original_size/1024/1024:.1f}MB -> {optimized_size/1024/1024:.1f}MB)")

    return results


def efficient_cog_read(cog_path: Union[str, Path],
                      bbox: Optional[Tuple[float, float, float, float]] = None,
                      target_resolution: Optional[float] = None,
                      max_pixels: int = 4_000_000) -> Dict[str, Any]:
    """
    Efficiently read from a COG using optimal access patterns.

    This function demonstrates best practices for reading COG data,
    including using appropriate overview levels and windowed reading
    to minimize data transfer and memory usage.

    Args:
        cog_path: Path or URL to the COG file
        bbox: Bounding box (minx, miny, maxx, maxy) for subset reading
        target_resolution: Target resolution for reading (uses overviews)
        max_pixels: Maximum number of pixels to read

    Returns:
        Dictionary containing read data and access statistics

    Example:
        >>> phoenix_bbox = (-112.3, 33.3, -111.9, 33.7)
        >>> data = efficient_cog_read("https://example.com/landsat.tif",
        ...                          bbox=phoenix_bbox,
        ...                          target_resolution=120.0)
        >>> array = data['raster_data']
        >>> print(f"Read {array.shape} array in {data['read_time']:.2f}s")
    """
    cog_path_str = str(cog_path)
    is_remote = cog_path_str.startswith(('http://', 'https://'))

    logger.info(f"Efficient COG read: {cog_path} (bbox: {bbox}, resolution: {target_resolution})")

    start_time = time.time()

    try:
        with rasterio.open(cog_path_str) as src:
            # Determine reading strategy
            overview_level = 0
            read_shape = None

            # If target resolution is specified, find appropriate overview
            if target_resolution and src.res[0] < target_resolution:
                for i, overview_factor in enumerate(src.overviews(1)):
                    overview_resolution = src.res[0] * overview_factor
                    if overview_resolution >= target_resolution:
                        overview_level = i + 1
                        break

                if overview_level > 0:
                    overview_factor = src.overviews(1)[overview_level - 1]
                    read_shape = (
                        src.height // overview_factor,
                        src.width // overview_factor
                    )
                    logger.info(f"Using overview level {overview_level} (factor: {overview_factor})")

            # Determine window for reading
            if bbox:
                # Convert bbox to window
                window = rasterio.windows.from_bounds(*bbox, src.transform)
                window = window.intersection(Window(0, 0, src.width, src.height))

                if window.width <= 0 or window.height <= 0:
                    raise ValueError("Bounding box doesn't intersect with raster")

                # Check if window is too large
                window_pixels = window.width * window.height
                if read_shape:
                    # Account for overview scaling
                    overview_factor = src.overviews(1)[overview_level - 1]
                    window_pixels = (window.width // overview_factor) * (window.height // overview_factor)

                if window_pixels > max_pixels:
                    # Use a smaller overview or subsample
                    if not read_shape:
                        # Find overview level to fit within max_pixels
                        for i, overview_factor in enumerate(src.overviews(1)):
                            scaled_pixels = (window.width // overview_factor) * (window.height // overview_factor)
                            if scaled_pixels <= max_pixels:
                                overview_level = i + 1
                                read_shape = (
                                    window.height // overview_factor,
                                    window.width // overview_factor
                                )
                                logger.info(f"Auto-selected overview {overview_level} to fit {max_pixels} pixel limit")
                                break

                        if not read_shape:
                            # Even smallest overview is too large, subsample
                            target_size = int(np.sqrt(max_pixels))
                            read_shape = (target_size, target_size)
                            logger.warning(f"Subsampling to {read_shape} to fit memory constraints")

                subset_bounds = rasterio.windows.bounds(window, src.transform)
            else:
                window = Window(0, 0, src.width, src.height)
                subset_bounds = src.bounds

                # Check total size
                total_pixels = src.width * src.height
                if read_shape:
                    overview_factor = src.overviews(1)[overview_level - 1] if overview_level > 0 else 1
                    total_pixels = (src.width // overview_factor) * (src.height // overview_factor)

                if total_pixels > max_pixels:
                    if not read_shape:
                        # Find appropriate overview
                        for i, overview_factor in enumerate(src.overviews(1)):
                            scaled_pixels = (src.width // overview_factor) * (src.height // overview_factor)
                            if scaled_pixels <= max_pixels:
                                overview_level = i + 1
                                read_shape = (
                                    src.height // overview_factor,
                                    src.width // overview_factor
                                )
                                logger.info(f"Using overview {overview_level} for full raster read")
                                break

                    if total_pixels > max_pixels:
                        target_size = int(np.sqrt(max_pixels))
                        read_shape = (target_size, target_size)
                        logger.warning(f"Resampling to {read_shape} to fit memory constraints")

            # Perform the read
            read_start = time.time()

            if read_shape and read_shape != (src.height, src.width):
                # Read with resampling/overview
                raster_data = src.read(
                    window=window,
                    out_shape=(src.count,) + read_shape,
                    resampling=Resampling.average
                )
            else:
                # Direct read
                raster_data = src.read(window=window)

            read_time = time.time() - read_start

            # Calculate statistics
            data_stats = {}
            for band in range(raster_data.shape[0]):
                band_data = raster_data[band]

                # Handle nodata
                if src.nodata is not None:
                    valid_data = band_data[band_data != src.nodata]
                else:
                    valid_data = band_data.flatten()

                if len(valid_data) > 0:
                    data_stats[f'band_{band + 1}'] = {
                        'min': float(np.min(valid_data)),
                        'max': float(np.max(valid_data)),
                        'mean': float(np.mean(valid_data)),
                        'std': float(np.std(valid_data)),
                        'valid_pixels': len(valid_data),
                    }

            # Calculate effective resolution
            if bbox:
                bounds_width = subset_bounds[2] - subset_bounds[0]
                bounds_height = subset_bounds[3] - subset_bounds[1]
                effective_resolution = (
                    bounds_width / raster_data.shape[2],
                    bounds_height / raster_data.shape[1]
                )
            else:
                if read_shape:
                    overview_factor = src.overviews(1)[overview_level - 1] if overview_level > 0 else 1
                    effective_resolution = (
                        src.res[0] * overview_factor,
                        src.res[1] * overview_factor
                    )
                else:
                    effective_resolution = src.res

            total_time = time.time() - start_time

            results = {
                'raster_data': raster_data,
                'source_metadata': {
                    'crs': src.crs,
                    'bounds': src.bounds,
                    'shape': (src.height, src.width),
                    'band_count': src.count,
                    'dtype': src.dtypes[0],
                    'nodata': src.nodata,
                },
                'read_metadata': {
                    'subset_bounds': subset_bounds,
                    'data_shape': raster_data.shape,
                    'overview_level': overview_level,
                    'effective_resolution': effective_resolution,
                    'bbox_requested': bbox,
                    'target_resolution_requested': target_resolution,
                },
                'performance': {
                    'total_time_seconds': total_time,
                    'read_time_seconds': read_time,
                    'pixels_read': raster_data.size,
                    'megapixels_per_second': (raster_data.size / 1_000_000) / read_time,
                    'is_remote': is_remote,
                },
                'statistics': data_stats,
                'read_timestamp': pd.Timestamp.now().isoformat(),
            }

            logger.info(f"COG read complete: {raster_data.shape} in {total_time:.2f}s ({read_time:.2f}s read)")
            return results

    except Exception as e:
        logger.error(f"Failed to read COG: {e}")
        raise


def compare_cog_vs_regular(regular_path: Union[str, Path],
                          cog_path: Union[str, Path],
                          test_windows: List[Window] = None,
                          iterations: int = 3) -> Dict[str, Any]:
    """
    Compare access performance between regular GeoTIFF and COG.

    This function benchmarks the performance difference between accessing
    data from a regular GeoTIFF versus a Cloud-Optimized GeoTIFF,
    demonstrating the benefits of COG optimization.

    Args:
        regular_path: Path to regular GeoTIFF
        cog_path: Path to COG version
        test_windows: List of windows to test (auto-generated if None)
        iterations: Number of iterations for each test

    Returns:
        Dictionary containing performance comparison results

    Example:
        >>> comparison = compare_cog_vs_regular("regular.tif", "optimized.tif")
        >>> speedup = comparison['performance_summary']['cog_speedup_factor']
        >>> print(f"COG is {speedup:.1f}x faster for random access")
    """
    regular_path = Path(regular_path)
    cog_path = Path(cog_path)

    logger.info(f"Comparing performance: {regular_path} vs {cog_path}")

    if not regular_path.exists():
        raise FileNotFoundError(f"Regular file not found: {regular_path}")
    if not cog_path.exists():
        raise FileNotFoundError(f"COG file not found: {cog_path}")

    # Generate test windows if not provided
    if test_windows is None:
        with rasterio.open(regular_path) as src:
            # Create various test windows
            test_windows = [
                # Small windows (typical COG use case)
                Window(0, 0, 256, 256),
                Window(src.width // 4, src.height // 4, 256, 256),
                Window(src.width // 2, src.height // 2, 256, 256),

                # Medium windows
                Window(0, 0, 512, 512),
                Window(src.width // 3, src.height // 3, 512, 512),

                # Large window
                Window(0, 0, min(1024, src.width), min(1024, src.height)),
            ]

    # Performance results storage
    results = {
        'test_configuration': {
            'regular_file': str(regular_path),
            'cog_file': str(cog_path),
            'test_windows': len(test_windows),
            'iterations_per_test': iterations,
        },
        'regular_times': [],
        'cog_times': [],
        'window_results': [],
    }

    # Test each window
    for i, window in enumerate(test_windows):
        logger.info(f"Testing window {i + 1}/{len(test_windows)}: {window.width}x{window.height}")

        window_result = {
            'window_size': (window.width, window.height),
            'regular_times': [],
            'cog_times': [],
        }

        # Test regular file
        for iteration in range(iterations):
            try:
                with rasterio.open(regular_path) as src:
                    start_time = time.time()
                    data = src.read(1, window=window)
                    read_time = time.time() - start_time
                    window_result['regular_times'].append(read_time)
                    results['regular_times'].append(read_time)
            except Exception as e:
                logger.warning(f"Regular file read failed: {e}")
                window_result['regular_times'].append(float('inf'))

        # Test COG file
        for iteration in range(iterations):
            try:
                with rasterio.open(cog_path) as src:
                    start_time = time.time()
                    data = src.read(1, window=window)
                    read_time = time.time() - start_time
                    window_result['cog_times'].append(read_time)
                    results['cog_times'].append(read_time)
            except Exception as e:
                logger.warning(f"COG file read failed: {e}")
                window_result['cog_times'].append(float('inf'))

        # Calculate window statistics
        window_result['regular_avg'] = np.mean(window_result['regular_times'])
        window_result['cog_avg'] = np.mean(window_result['cog_times'])
        window_result['speedup'] = window_result['regular_avg'] / window_result['cog_avg']

        results['window_results'].append(window_result)

    # Calculate overall performance summary
    regular_avg = np.mean([t for t in results['regular_times'] if t != float('inf')])
    cog_avg = np.mean([t for t in results['cog_times'] if t != float('inf')])

    performance_summary = {
        'regular_avg_time': regular_avg,
        'cog_avg_time': cog_avg,
        'cog_speedup_factor': regular_avg / cog_avg,
        'regular_total_time': sum(results['regular_times']),
        'cog_total_time': sum(results['cog_times']),
        'time_saved_percent': ((regular_avg - cog_avg) / regular_avg) * 100,
    }

    results['performance_summary'] = performance_summary
    results['comparison_timestamp'] = pd.Timestamp.now().isoformat()

    speedup = performance_summary['cog_speedup_factor']
    time_saved = performance_summary['time_saved_percent']

    logger.info(f"Performance comparison complete:")
    logger.info(f"  COG is {speedup:.1f}x faster on average")
    logger.info(f"  Time saved: {time_saved:.1f}%")

    return results


def analyze_cog_structure(cog_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Analyze the internal structure of a COG file.

    This function provides detailed analysis of COG internal organization,
    including tile structure, overview pyramids, and optimization metrics
    useful for understanding performance characteristics.

    Args:
        cog_path: Path or URL to the COG file

    Returns:
        Dictionary containing detailed structural analysis

    Example:
        >>> analysis = analyze_cog_structure("optimized.tif")
        >>> print(f"Tile size: {analysis['tile_info']['tile_size']}")
        >>> print(f"Overviews: {len(analysis['overviews'])}")
    """
    cog_path_str = str(cog_path)
    is_remote = cog_path_str.startswith(('http://', 'https://'))

    logger.info(f"Analyzing COG structure: {cog_path}")

    try:
        with rasterio.open(cog_path_str) as src:
            # Basic file information
            basic_info = {
                'file_path': cog_path_str,
                'is_remote': is_remote,
                'driver': src.driver,
                'width': src.width,
                'height': src.height,
                'band_count': src.count,
                'dtype': src.dtypes[0],
                'crs': src.crs,
                'bounds': src.bounds,
                'transform': src.transform,
                'resolution': src.res,
            }

            # Tile information
            tile_info = {
                'is_tiled': src.is_tiled,
                'tile_size': src.block_shapes[0] if src.is_tiled else None,
                'block_shapes': src.block_shapes,
                'tiles_x': src.width // src.block_shapes[0][1] if src.is_tiled else 0,
                'tiles_y': src.height // src.block_shapes[0][0] if src.is_tiled else 0,
            }

            if src.is_tiled:
                tile_info['total_tiles'] = tile_info['tiles_x'] * tile_info['tiles_y']
                tile_info['is_square_tiles'] = src.block_shapes[0][0] == src.block_shapes[0][1]

            # Overview analysis
            overviews = []
            for band in range(1, src.count + 1):
                overview_factors = src.overviews(band)
                if band == 1:  # Use first band for primary analysis
                    for i, factor in enumerate(overview_factors):
                        overview_info = {
                            'level': i + 1,
                            'factor': factor,
                            'width': src.width // factor,
                            'height': src.height // factor,
                            'pixels': (src.width // factor) * (src.height // factor),
                            'resolution': (src.res[0] * factor, src.res[1] * factor),
                        }
                        overviews.append(overview_info)

            # Compression analysis
            compression_info = {
                'compression': src.compression,
                'interleave': getattr(src, 'interleave', 'unknown'),
                'predictor': getattr(src, 'predictor', None),
            }

            # Calculate storage efficiency metrics
            pixel_count = src.width * src.height * src.count
            bytes_per_pixel = np.dtype(src.dtypes[0]).itemsize

            # Estimate uncompressed size
            uncompressed_size = pixel_count * bytes_per_pixel

            # Get actual file size (if local)
            if not is_remote and Path(cog_path).exists():
                actual_size = Path(cog_path).stat().st_size
                compression_ratio = uncompressed_size / actual_size
                storage_info = {
                    'uncompressed_size_bytes': uncompressed_size,
                    'actual_size_bytes': actual_size,
                    'compression_ratio': compression_ratio,
                    'space_saved_percent': ((uncompressed_size - actual_size) / uncompressed_size) * 100,
                }
            else:
                storage_info = {
                    'uncompressed_size_bytes': uncompressed_size,
                    'actual_size_bytes': None,
                    'compression_ratio': None,
                    'space_saved_percent': None,
                }

            # Performance characteristics
            performance_metrics = {
                'random_access_friendly': src.is_tiled and len(overviews) > 0,
                'web_optimized': src.is_tiled and src.compression is not None,
                'overview_coverage': len(overviews),
                'max_overview_reduction': max([ov['factor'] for ov in overviews]) if overviews else 1,
            }

            # Quality assessment
            quality_flags = []
            if not src.is_tiled:
                quality_flags.append("Not tiled - poor random access performance")
            if len(overviews) == 0:
                quality_flags.append("No overviews - poor zoom performance")
            if src.compression is None:
                quality_flags.append("No compression - inefficient storage")
            if src.is_tiled and src.block_shapes[0][0] != src.block_shapes[0][1]:
                quality_flags.append("Non-square tiles - may be less efficient")

            analysis_results = {
                'basic_info': basic_info,
                'tile_info': tile_info,
                'overviews': overviews,
                'compression_info': compression_info,
                'storage_info': storage_info,
                'performance_metrics': performance_metrics,
                'quality_flags': quality_flags,
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
            }

            logger.info(f"Structure analysis complete: {len(overviews)} overviews, {len(quality_flags)} issues")
            return analysis_results

    except Exception as e:
        logger.error(f"Failed to analyze COG structure: {e}")
        raise


# Utility functions for COG operations

def estimate_cog_read_time(width: int, height: int, band_count: int = 1,
                          is_remote: bool = False, has_overviews: bool = True) -> Dict[str, float]:
    """
    Estimate read times for COG access patterns.

    Args:
        width: Raster width in pixels
        height: Raster height in pixels
        band_count: Number of bands
        is_remote: Whether accessing remotely
        has_overviews: Whether COG has overviews

    Returns:
        Dictionary with estimated read times for different scenarios
    """
    # Base read rates (pixels per second) - rough estimates
    local_rate = 50_000_000  # 50M pixels/sec for local SSD
    remote_rate = 5_000_000   # 5M pixels/sec for good network

    base_rate = remote_rate if is_remote else local_rate

    # Adjust for band count
    total_pixels = width * height * band_count

    # Different access patterns
    full_read_time = total_pixels / base_rate

    # Small window (256x256)
    small_window_pixels = 256 * 256 * band_count
    small_window_time = small_window_pixels / base_rate
    if not has_overviews and is_remote:
        small_window_time *= 2  # Penalty for no overviews on remote

    # Overview read (assume 1/4 resolution)
    overview_pixels = (width // 4) * (height // 4) * band_count
    overview_time = overview_pixels / base_rate if has_overviews else full_read_time

    return {
        'full_raster_seconds': full_read_time,
        'small_window_seconds': small_window_time,
        'overview_read_seconds': overview_time,
        'estimated_for': f"{width}x{height}x{band_count} ({'remote' if is_remote else 'local'})"
    }


def get_optimal_cog_settings(width: int, height: int, dtype: str,
                           use_case: str = 'general') -> Dict[str, Any]:
    """
    Get optimal COG settings for a given raster and use case.

    Args:
        width: Raster width in pixels
        height: Raster height in pixels
        dtype: Data type (e.g., 'uint16', 'float32')
        use_case: Use case ('web', 'analysis', 'archive', 'general')

    Returns:
        Dictionary with recommended COG settings
    """
    # Base settings
    settings = {
        'tiled': True,
        'compress': 'lzw',
        'predictor': 2,
        'tile_size': 512,
        'overview_resampling': 'average',
        'overview_min_size': 256,
        'interleave': 'pixel',
    }

    # Adjust compression based on data type
    if dtype.startswith('float'):
        settings['predictor'] = 3  # Floating point predictor
        if use_case == 'analysis':
            settings['compress'] = 'deflate'  # Better for scientific data
    elif dtype in ['uint8', 'int8']:
        settings['compress'] = 'jpeg'  # Good for 8-bit imagery
        settings['predictor'] = None

    # Adjust tile size based on raster size and use case
    total_pixels = width * height

    if total_pixels > 100_000_000:  # Very large rasters
        settings['tile_size'] = 1024
    elif total_pixels < 1_000_000:  # Small rasters
        settings['tile_size'] = 256

    if use_case == 'web':
        settings['tile_size'] = 256  # Better for web tiles
        settings['compress'] = 'jpeg'
        settings['overview_min_size'] = 128
    elif use_case == 'archive':
        settings['compress'] = 'lzw'  # Lossless compression
        settings['tile_size'] = 1024  # Larger tiles for better compression
    elif use_case == 'analysis':
        settings['compress'] = 'deflate'  # Good balance
        settings['tile_size'] = 512

    return settings


# Alias functions to match test expectations
def validate_cog_structure(file_path: Union[str, Path], remote: bool = None) -> Dict[str, Any]:
    """
    Validate COG structure - alias for validate_cog function.

    This function is an alias for the validate_cog function to match test expectations.
    """
    result = validate_cog(file_path, remote)

    # Restructure result to match test expectations
    return {
        'is_valid_cog': result['is_valid_cog'],
        'validation_details': {
            'is_tiled': result.get('file_info', {}).get('is_tiled', False),
            'overview_count': result.get('file_info', {}).get('overview_count', 0),
            'has_internal_overviews': result.get('file_info', {}).get('overview_count', 0) > 0,
            'compression': result.get('file_info', {}).get('compression', 'none'),
            'block_size': result.get('file_info', {}).get('block_size', (0, 0))
        },
        'optimization_score': 100 if result['is_valid_cog'] else 25,
        'issues_found': result.get('issues', []),
        'recommendations': result.get('recommendations', []),
        'file_info': result.get('file_info', {})
    }


def read_cog_efficiently(
    cog_path: Union[str, Path],
    bbox: Tuple[float, float, float, float] = None,
    target_resolution: float = None,
    max_resolution: float = None,
    bands: List[int] = None
) -> Dict[str, Any]:
    """
    Efficiently read data from a COG using optimal access patterns.

    Parameters:
    -----------
    cog_path : str or Path
        Path or URL to COG file
    bbox : tuple, optional
        Bounding box (minx, miny, maxx, maxy) for spatial subset
    target_resolution : float, optional
        Target resolution for reading
    max_resolution : float, optional
        Maximum resolution threshold
    bands : list of int, optional
        Specific bands to read

    Returns:
    --------
    dict
        Dictionary with data, metadata, and performance info
    """
    import time
    import sys

    start_time = time.time()
    cog_path = str(cog_path)

    try:
        with rasterio.open(cog_path) as src:
            # Determine read strategy
            read_strategy = 'full_resolution'
            window = None

            # Handle bbox
            if bbox:
                from rasterio.windows import from_bounds
                window = from_bounds(*bbox, src.transform)
                read_strategy = 'windowed_read'

            # Select appropriate overview level
            overview_level = 0
            if target_resolution or max_resolution:
                # Find best overview level
                overviews = src.overviews(1)
                if overviews:
                    current_res = abs(src.transform[0])
                    target_res = target_resolution or max_resolution

                    for i, factor in enumerate(overviews):
                        overview_res = current_res * factor
                        if overview_res <= target_res * 1.5:  # Allow some tolerance
                            overview_level = i + 1
                            read_strategy = 'overview_read'
                            break

            # Read the data
            if bands:
                if window:
                    data = src.read(bands, window=window, out_shape=(
                        len(bands),
                        int(window.height // (overview_level + 1)),
                        int(window.width // (overview_level + 1))
                    ) if overview_level > 0 else None)
                else:
                    data = src.read(bands)
            else:
                if window:
                    data = src.read(window=window, out_shape=(
                        src.count,
                        int(window.height // (overview_level + 1)),
                        int(window.width // (overview_level + 1))
                    ) if overview_level > 0 else None)
                else:
                    data = src.read()

            # Calculate data size
            data_size_mb = data.nbytes / (1024 * 1024)

            end_time = time.time()

            return {
                'data': data,
                'metadata': {
                    'dimensions': (src.width, src.height),
                    'bands': src.count,
                    'dtype': src.dtypes[0],
                    'crs': str(src.crs) if src.crs else None,
                    'transform': list(src.transform),
                    'overview_levels': src.overviews(1) if src.count > 0 else []
                },
                'read_strategy': read_strategy,
                'performance_info': {
                    'read_time_seconds': end_time - start_time,
                    'data_size_mb': data_size_mb,
                    'overview_level_used': overview_level
                },
                'bbox_used': bbox
            }

    except Exception as e:
        return {
            'data': None,
            'metadata': {},
            'read_strategy': 'failed',
            'performance_info': {
                'read_time_seconds': time.time() - start_time,
                'error': str(e)
            },
            'bbox_used': bbox
        }


def compare_cog_performance(
    standard_raster: Union[str, Path],
    cog_raster: Union[str, Path],
    test_scenarios: List[str] = None
) -> Dict[str, Any]:
    """
    Compare performance between standard raster and COG.

    Parameters:
    -----------
    standard_raster : str or Path
        Path to standard raster file
    cog_raster : str or Path
        Path to COG raster file
    test_scenarios : list of str, optional
        Test scenarios to run

    Returns:
    --------
    dict
        Performance comparison results
    """
    import time

    if test_scenarios is None:
        test_scenarios = ['full_read', 'window_read', 'overview_read']

    results = {
        'test_scenarios': test_scenarios,
        'standard_performance': {},
        'cog_performance': {},
        'performance_improvements': {},
        'recommendations': []
    }

    for scenario in test_scenarios:
        # Test standard raster
        try:
            start_time = time.time()
            with rasterio.open(standard_raster) as src:
                if scenario == 'full_read':
                    data = src.read()
                elif scenario == 'window_read':
                    from rasterio.windows import Window
                    window = Window(0, 0, min(512, src.width), min(512, src.height))
                    data = src.read(window=window)
                elif scenario == 'overview_read':
                    # Read at reduced resolution
                    data = src.read(out_shape=(src.count, src.height//2, src.width//2))

            standard_time = time.time() - start_time
            results['standard_performance'][scenario] = {
                'read_time_seconds': standard_time,
                'data_shape': data.shape if 'data' in locals() else None
            }
        except Exception as e:
            results['standard_performance'][scenario] = {
                'read_time_seconds': float('inf'),
                'error': str(e)
            }

        # Test COG raster
        try:
            start_time = time.time()
            with rasterio.open(cog_raster) as src:
                if scenario == 'full_read':
                    data = src.read()
                elif scenario == 'window_read':
                    from rasterio.windows import Window
                    window = Window(0, 0, min(512, src.width), min(512, src.height))
                    data = src.read(window=window)
                elif scenario == 'overview_read':
                    # Use actual overviews if available
                    if src.overviews(1):
                        data = src.read(out_shape=(src.count, src.height//2, src.width//2))
                    else:
                        data = src.read()

            cog_time = time.time() - start_time
            results['cog_performance'][scenario] = {
                'read_time_seconds': cog_time,
                'data_shape': data.shape if 'data' in locals() else None
            }

            # Calculate improvement
            if scenario in results['standard_performance']:
                standard_time = results['standard_performance'][scenario]['read_time_seconds']
                if standard_time > 0 and cog_time > 0:
                    improvement = standard_time / cog_time
                    results['performance_improvements'][scenario] = improvement
        except Exception as e:
            results['cog_performance'][scenario] = {
                'read_time_seconds': float('inf'),
                'error': str(e)
            }

    # Generate recommendations
    avg_improvement = sum(results['performance_improvements'].values()) / len(results['performance_improvements']) if results['performance_improvements'] else 1.0

    if avg_improvement > 1.5:
        results['recommendations'].append("COG format shows significant performance benefits")
    elif avg_improvement > 1.1:
        results['recommendations'].append("COG format shows moderate performance benefits")
    else:
        results['recommendations'].append("COG format performance is similar to standard raster")

    return results


def generate_cog_metadata(
    cog_path: Union[str, Path],
    include_statistics: bool = False,
    include_histogram: bool = False
) -> Dict[str, Any]:
    """
    Generate comprehensive metadata for a COG file.

    Parameters:
    -----------
    cog_path : str or Path
        Path to COG file
    include_statistics : bool, default=False
        Whether to include band statistics
    include_histogram : bool, default=False
        Whether to include histogram data

    Returns:
    --------
    dict
        Comprehensive COG metadata
    """
    import os
    from datetime import datetime

    cog_path = Path(cog_path)

    try:
        with rasterio.open(cog_path) as src:
            # Basic file info
            file_info = {
                'file_path': str(cog_path),
                'file_size_mb': cog_path.stat().st_size / (1024 * 1024),
                'creation_time': datetime.fromtimestamp(cog_path.stat().st_mtime).isoformat(),
                'driver': src.driver
            }

            # COG properties
            cog_properties = {
                'is_valid_cog': src.is_tiled,
                'tile_size': src.block_shapes[0] if src.block_shapes else None,
                'overview_count': len(src.overviews(1)) if src.count > 0 else 0,
                'compression': src.compression.value if src.compression else 'none',
                'interleave': src.interleaving.value if src.interleaving else 'pixel'
            }

            # Spatial info
            spatial_info = {
                'crs': str(src.crs) if src.crs else None,
                'bounds': src.bounds,
                'resolution': (abs(src.transform[0]), abs(src.transform[4])),
                'dimensions': (src.width, src.height),
                'band_count': src.count
            }

            # Band info
            band_info = []
            for i in range(1, src.count + 1):
                band_data = {
                    'band_number': i,
                    'dtype': src.dtypes[i-1],
                    'nodata': src.nodatavals[i-1] if i <= len(src.nodatavals) else None
                }

                if include_statistics:
                    try:
                        data = src.read(i, masked=True)
                        if data.count() > 0:  # Has valid data
                            band_data['statistics'] = {
                                'min': float(data.min()),
                                'max': float(data.max()),
                                'mean': float(data.mean()),
                                'std': float(data.std())
                            }
                    except Exception:
                        pass

                if include_histogram:
                    try:
                        data = src.read(i, masked=True)
                        if data.count() > 0:
                            hist, bin_edges = np.histogram(data.compressed(), bins=50)
                            band_data['histogram'] = {
                                'counts': hist.tolist(),
                                'bin_edges': bin_edges.tolist()
                            }
                    except Exception:
                        pass

                band_info.append(band_data)

            # Optimization info
            optimization_info = {
                'is_tiled': src.is_tiled,
                'has_overviews': len(src.overviews(1)) > 0 if src.count > 0 else False,
                'block_size': src.block_shapes[0] if src.block_shapes else None,
                'overview_factors': src.overviews(1) if src.count > 0 else []
            }

            # Access patterns (estimated)
            access_patterns = {
                'optimal_for_web': cog_properties['tile_size'] == (256, 256) if cog_properties['tile_size'] else False,
                'optimal_for_analysis': cog_properties['tile_size'] in [(512, 512), (1024, 1024)] if cog_properties['tile_size'] else False,
                'has_pyramids': optimization_info['has_overviews'],
                'cloud_optimized': optimization_info['is_tiled'] and optimization_info['has_overviews']
            }

            return {
                'file_info': file_info,
                'cog_properties': cog_properties,
                'spatial_info': spatial_info,
                'band_info': band_info,
                'optimization_info': optimization_info,
                'access_patterns': access_patterns
            }

    except Exception as e:
        return {
            'file_info': {'file_path': str(cog_path), 'error': str(e)},
            'cog_properties': {},
            'spatial_info': {},
            'band_info': [],
            'optimization_info': {},
            'access_patterns': {}
        }
