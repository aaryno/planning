"""
Raster Processing Module - Core Functionality

This module provides fundamental raster processing capabilities using rasterio,
focusing on local and remote raster analysis, COG processing, and basic
raster operations.

Author: Student
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
from rasterio.warp import calculate_default_transform, reproject
from rasterio.profiles import default_gtiff_profile
import matplotlib.pyplot as plt
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress common warnings for cleaner output
warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)


def analyze_local_raster(raster_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Comprehensive analysis of local raster datasets.

    Demonstrates fundamental rasterio operations including metadata extraction,
    basic statistics, and data quality assessment for local raster files.

    Args:
        raster_path: Path to the local raster file

    Returns:
        Dictionary containing comprehensive raster analysis results

    Raises:
        FileNotFoundError: If the raster file doesn't exist
        rasterio.errors.RasterioIOError: If the file cannot be read

    Example:
        >>> results = analyze_local_raster("data/phoenix_dem.tif")
        >>> print(f"Raster shape: {results['dimensions']}")
        >>> print(f"Data type: {results['dtype']}")
    """
    raster_path = Path(raster_path)

    if not raster_path.exists():
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    logger.info(f"Analyzing local raster: {raster_path}")

    try:
        with rasterio.open(raster_path) as src:
            # Basic metadata
            metadata = {
                'filename': raster_path.name,
                'driver': src.driver,
                'dtype': src.dtypes[0],
                'dimensions': (src.width, src.height),
                'band_count': src.count,
                'crs': src.crs,
                'bounds': src.bounds,
                'transform': src.transform,
                'resolution': (abs(src.transform[0]), abs(src.transform[4])),
                'nodata': src.nodata,
                'is_tiled': src.is_tiled,
                'block_shapes': src.block_shapes,
                'compression': src.compression,
            }

            # Read data for statistical analysis
            # Use windowed reading for large files
            if src.width * src.height > 10_000_000:  # ~10M pixels
                logger.warning("Large raster detected. Using sampling for statistics.")
                # Sample every 100th pixel for large rasters
                sample_window = Window(0, 0,
                                     min(1000, src.width),
                                     min(1000, src.height))
                data = src.read(1, window=sample_window)
            else:
                data = src.read(1)

            # Calculate statistics
            valid_data = data[data != src.nodata] if src.nodata else data

            if len(valid_data) > 0:
                statistics = {
                    'min': float(np.min(valid_data)),
                    'max': float(np.max(valid_data)),
                    'mean': float(np.mean(valid_data)),
                    'std': float(np.std(valid_data)),
                    'median': float(np.median(valid_data)),
                    'valid_pixel_count': int(len(valid_data)),
                    'total_pixel_count': int(data.size),
                    'nodata_pixel_count': int(data.size - len(valid_data)),
                    'data_completeness': float(len(valid_data) / data.size * 100),
                }
            else:
                statistics = {
                    'min': None,
                    'max': None,
                    'mean': None,
                    'std': None,
                    'median': None,
                    'valid_pixel_count': 0,
                    'total_pixel_count': int(data.size),
                    'nodata_pixel_count': int(data.size),
                    'data_completeness': 0.0,
                }

            # Quality assessment
            quality_flags = []

            if metadata['crs'] is None:
                quality_flags.append("No CRS defined")

            if metadata['nodata'] is None:
                quality_flags.append("No NoData value defined")

            if statistics['data_completeness'] < 50:
                quality_flags.append("Low data completeness (<50%)")

            if metadata['compression'] is None:
                quality_flags.append("No compression applied")

            # Combine all results
            analysis_results = {
                **metadata,
                'statistics': statistics,
                'quality_flags': quality_flags,
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
            }

            logger.info(f"Analysis complete. Data completeness: {statistics['data_completeness']:.1f}%")
            return analysis_results

    except rasterio.errors.RasterioIOError as e:
        logger.error(f"Failed to read raster file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during raster analysis: {e}")
        raise


def process_multiband_imagery(image_path: Union[str, Path],
                            band_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Process multiband imagery for vegetation analysis and band calculations.

    This function demonstrates working with multiband rasters, calculating
    vegetation indices (NDVI), and handling multispectral imagery common
    in remote sensing applications.

    Args:
        image_path: Path to multiband imagery file
        band_names: Optional list of band names for labeling

    Returns:
        Dictionary containing band statistics and calculated indices

    Example:
        >>> results = process_multiband_imagery("data/phoenix_landsat.tif",
        ...                                   ["Blue", "Green", "Red", "NIR"])
        >>> ndvi_stats = results['indices']['NDVI']['statistics']
        >>> print(f"Mean NDVI: {ndvi_stats['mean']:.3f}")
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    logger.info(f"Processing multiband imagery: {image_path}")

    with rasterio.open(image_path) as src:
        if src.count < 2:
            raise ValueError("Multiband processing requires at least 2 bands")

        # Read all bands
        image_data = src.read()  # Shape: (bands, height, width)

        # Create band names if not provided
        if band_names is None:
            band_names = [f"Band_{i+1}" for i in range(src.count)]
        elif len(band_names) != src.count:
            logger.warning(f"Band names count ({len(band_names)}) doesn't match band count ({src.count})")
            band_names = [f"Band_{i+1}" for i in range(src.count)]

        # Calculate statistics for each band
        band_statistics = {}
        for i, band_name in enumerate(band_names):
            band_data = image_data[i]

            # Handle nodata values
            if src.nodata is not None:
                valid_data = band_data[band_data != src.nodata]
            else:
                valid_data = band_data.flatten()

            if len(valid_data) > 0:
                band_statistics[band_name] = {
                    'min': float(np.min(valid_data)),
                    'max': float(np.max(valid_data)),
                    'mean': float(np.mean(valid_data)),
                    'std': float(np.std(valid_data)),
                    'percentile_25': float(np.percentile(valid_data, 25)),
                    'percentile_75': float(np.percentile(valid_data, 75)),
                }
            else:
                band_statistics[band_name] = {
                    'min': None, 'max': None, 'mean': None, 'std': None,
                    'percentile_25': None, 'percentile_75': None,
                }

        # Calculate vegetation indices if we have appropriate bands
        indices = {}

        # NDVI calculation (assuming bands are ordered: Blue, Green, Red, NIR)
        if src.count >= 4:
            red_band = image_data[2]  # Assuming Red is band 3
            nir_band = image_data[3]  # Assuming NIR is band 4

            # Calculate NDVI with error handling for division by zero
            with np.errstate(divide='ignore', invalid='ignore'):
                ndvi = (nir_band - red_band) / (nir_band + red_band)
                ndvi = np.where(np.isfinite(ndvi), ndvi, np.nan)

            # Calculate NDVI statistics
            valid_ndvi = ndvi[~np.isnan(ndvi)]
            if len(valid_ndvi) > 0:
                indices['NDVI'] = {
                    'description': 'Normalized Difference Vegetation Index',
                    'formula': '(NIR - Red) / (NIR + Red)',
                    'statistics': {
                        'min': float(np.min(valid_ndvi)),
                        'max': float(np.max(valid_ndvi)),
                        'mean': float(np.mean(valid_ndvi)),
                        'std': float(np.std(valid_ndvi)),
                    },
                    'vegetation_categories': {
                        'water_bare_soil': float(np.sum(valid_ndvi < 0.1) / len(valid_ndvi) * 100),
                        'sparse_vegetation': float(np.sum((valid_ndvi >= 0.1) & (valid_ndvi < 0.3)) / len(valid_ndvi) * 100),
                        'moderate_vegetation': float(np.sum((valid_ndvi >= 0.3) & (valid_ndvi < 0.6)) / len(valid_ndvi) * 100),
                        'dense_vegetation': float(np.sum(valid_ndvi >= 0.6) / len(valid_ndvi) * 100),
                    }
                }

        # EVI calculation if available (requires Blue band)
        if src.count >= 4:
            blue_band = image_data[0]  # Assuming Blue is band 1
            red_band = image_data[2]
            nir_band = image_data[3]

            # Enhanced Vegetation Index
            with np.errstate(divide='ignore', invalid='ignore'):
                evi = 2.5 * (nir_band - red_band) / (nir_band + 6 * red_band - 7.5 * blue_band + 1)
                evi = np.where(np.isfinite(evi), evi, np.nan)

            valid_evi = evi[~np.isnan(evi)]
            if len(valid_evi) > 0:
                indices['EVI'] = {
                    'description': 'Enhanced Vegetation Index',
                    'formula': '2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)',
                    'statistics': {
                        'min': float(np.min(valid_evi)),
                        'max': float(np.max(valid_evi)),
                        'mean': float(np.mean(valid_evi)),
                        'std': float(np.std(valid_evi)),
                    }
                }

        results = {
            'image_metadata': {
                'filename': image_path.name,
                'band_count': src.count,
                'dimensions': (src.width, src.height),
                'dtype': src.dtypes[0],
                'crs': src.crs,
                'bounds': src.bounds,
                'band_names': band_names,
            },
            'band_statistics': band_statistics,
            'indices': indices,
            'processing_timestamp': pd.Timestamp.now().isoformat(),
        }

        logger.info(f"Multiband processing complete. Bands: {src.count}, Indices calculated: {len(indices)}")
        return results


def process_remote_cog(cog_url: str,
                      bbox: Optional[Tuple[float, float, float, float]] = None,
                      max_size: int = 2048) -> Dict[str, Any]:
    """
    Process Cloud-Optimized GeoTIFF (COG) from remote URLs.

    Demonstrates efficient access to remote raster data using COG format,
    including partial reading and memory-efficient processing techniques.

    Args:
        cog_url: URL to the COG file
        bbox: Optional bounding box (minx, miny, maxx, maxy) for subset reading
        max_size: Maximum dimension size to prevent memory issues

    Returns:
        Dictionary containing COG metadata and processed data statistics

    Example:
        >>> phoenix_bbox = (-112.3, 33.3, -111.9, 33.7)
        >>> results = process_remote_cog("https://example.com/data.tif",
        ...                            bbox=phoenix_bbox)
        >>> print(f"COG tiling: {results['is_cloud_optimized']}")
    """
    logger.info(f"Processing remote COG: {cog_url}")

    try:
        with rasterio.open(cog_url) as src:
            # Check if it's a proper COG
            cog_info = {
                'is_cloud_optimized': src.is_tiled and len(src.overviews(1)) > 0,
                'is_tiled': src.is_tiled,
                'overview_count': len(src.overviews(1)),
                'block_shapes': src.block_shapes,
                'compression': src.compression,
            }

            # Determine reading strategy
            if bbox:
                # Read subset based on bounding box
                try:
                    window = rasterio.windows.from_bounds(*bbox, src.transform)
                    window = window.intersection(Window(0, 0, src.width, src.height))

                    if window.width == 0 or window.height == 0:
                        raise ValueError("Bounding box doesn't intersect with raster")

                    # Check if subset is too large
                    if window.width * window.height > max_size * max_size:
                        # Use overview for large areas
                        overview_level = 0
                        for i, overview_factor in enumerate(src.overviews(1)):
                            if (window.width // overview_factor) * (window.height // overview_factor) <= max_size * max_size:
                                overview_level = i + 1
                                break

                        if overview_level > 0:
                            logger.info(f"Using overview level {overview_level} for efficient reading")
                            data = src.read(1, window=window, out_shape=(
                                int(window.height // src.overviews(1)[overview_level - 1]),
                                int(window.width // src.overviews(1)[overview_level - 1])
                            ), resampling=Resampling.average)
                        else:
                            # Fallback: sample the data
                            sample_window = Window(
                                window.col_off, window.row_off,
                                min(max_size, int(window.width)),
                                min(max_size, int(window.height))
                            )
                            data = src.read(1, window=sample_window)
                    else:
                        data = src.read(1, window=window)

                    subset_bounds = rasterio.windows.bounds(window, src.transform)

                except Exception as e:
                    logger.warning(f"Bbox reading failed: {e}. Reading full raster with overview.")
                    # Fallback to overview reading
                    if src.overviews(1):
                        overview_level = -1  # Use smallest overview
                        data = src.read(1, out_shape=(max_size, max_size),
                                      resampling=Resampling.average)
                    else:
                        raise ValueError("Cannot read large raster without overviews")
                    subset_bounds = src.bounds
            else:
                # Read full raster using appropriate overview
                if src.width * src.height > max_size * max_size:
                    if src.overviews(1):
                        # Use the most appropriate overview
                        target_pixels = max_size * max_size
                        best_overview = 0
                        for i, overview_factor in enumerate(src.overviews(1)):
                            overview_pixels = (src.width // overview_factor) * (src.height // overview_factor)
                            if overview_pixels <= target_pixels:
                                best_overview = i + 1
                                break

                        if best_overview > 0:
                            overview_factor = src.overviews(1)[best_overview - 1]
                            out_shape = (src.height // overview_factor, src.width // overview_factor)
                            logger.info(f"Using overview {best_overview} with shape {out_shape}")
                        else:
                            out_shape = (max_size, max_size)

                        data = src.read(1, out_shape=out_shape, resampling=Resampling.average)
                    else:
                        raise ValueError(f"Raster too large ({src.width}x{src.height}) and no overviews available")
                else:
                    data = src.read(1)

                subset_bounds = src.bounds

            # Calculate statistics for the read data
            if src.nodata is not None:
                valid_data = data[data != src.nodata]
            else:
                valid_data = data.flatten()

            if len(valid_data) > 0:
                statistics = {
                    'min': float(np.min(valid_data)),
                    'max': float(np.max(valid_data)),
                    'mean': float(np.mean(valid_data)),
                    'std': float(np.std(valid_data)),
                    'valid_pixels': int(len(valid_data)),
                    'total_pixels': int(data.size),
                    'data_shape': data.shape,
                }
            else:
                statistics = {
                    'min': None, 'max': None, 'mean': None, 'std': None,
                    'valid_pixels': 0, 'total_pixels': int(data.size),
                    'data_shape': data.shape,
                }

            results = {
                'url': cog_url,
                'source_metadata': {
                    'driver': src.driver,
                    'dtype': src.dtypes[0],
                    'dimensions': (src.width, src.height),
                    'band_count': src.count,
                    'crs': src.crs,
                    'bounds': src.bounds,
                    'transform': src.transform,
                },
                'cog_optimization': cog_info,
                'subset_bounds': subset_bounds,
                'bbox_requested': bbox,
                'statistics': statistics,
                'processing_timestamp': pd.Timestamp.now().isoformat(),
            }

            logger.info(f"COG processing complete. Shape: {data.shape}, Valid pixels: {statistics['valid_pixels']}")
            return results

    except Exception as e:
        logger.error(f"Failed to process remote COG: {e}")
        raise


def create_optimized_cog(input_path: Union[str, Path],
                        output_path: Union[str, Path],
                        compress: str = 'lzw',
                        tiled: bool = True,
                        blocksize: int = 512) -> Dict[str, Any]:
    """
    Create a Cloud-Optimized GeoTIFF from an existing raster.

    This function demonstrates COG creation with proper tiling, compression,
    and overview generation for optimal cloud-based access patterns.

    Args:
        input_path: Path to input raster file
        output_path: Path for output COG file
        compress: Compression method ('lzw', 'deflate', 'jpeg', etc.)
        tiled: Whether to create tiled output
        blocksize: Tile block size in pixels

    Returns:
        Dictionary containing COG creation results and optimization metrics

    Example:
        >>> result = create_optimized_cog("data/large_raster.tif",
        ...                             "output/optimized.tif",
        ...                             compress='lzw')
        >>> print(f"Size reduction: {result['size_reduction_percent']:.1f}%")
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input raster not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Creating COG: {input_path} -> {output_path}")

    # Get original file size
    original_size = input_path.stat().st_size

    with rasterio.open(input_path) as src:
        # Create output profile with COG optimizations
        profile = src.profile.copy()

        # COG-specific optimizations
        profile.update({
            'driver': 'GTiff',
            'tiled': tiled,
            'blockxsize': blocksize,
            'blockysize': blocksize,
            'compress': compress,
            'interleave': 'pixel',
            'BIGTIFF': 'IF_SAFER',  # Use BigTIFF if needed
        })

        # Add predictor for better compression with certain data types
        if compress in ['lzw', 'deflate']:
            if src.dtypes[0] in ['uint16', 'int16', 'uint32', 'int32']:
                profile['predictor'] = 2  # Horizontal differencing
            elif src.dtypes[0] in ['float32', 'float64']:
                profile['predictor'] = 3  # Floating point predictor

        logger.info(f"COG profile: tiled={tiled}, compression={compress}, blocksize={blocksize}")

        # Create the COG
        with rasterio.open(output_path, 'w', **profile) as dst:
            # Copy data
            for band in range(1, src.count + 1):
                data = src.read(band)
                dst.write(data, band)

            # Copy metadata
            dst.update_tags(**src.tags())
            for band in range(1, src.count + 1):
                dst.update_tags(band, **src.tags(band))

        # Build overviews for the COG
        logger.info("Building overviews...")
        with rasterio.open(output_path, 'r+') as dst:
            # Calculate overview levels
            overview_factors = []
            max_dimension = max(dst.width, dst.height)
            factor = 2
            while max_dimension // factor >= 256:  # Don't create tiny overviews
                overview_factors.append(factor)
                factor *= 2

            if overview_factors:
                dst.build_overviews(overview_factors, Resampling.average)
                dst.update_tags(ns='rio_overview', resampling='average')
                logger.info(f"Created {len(overview_factors)} overview levels: {overview_factors}")

    # Get final file size and calculate metrics
    optimized_size = output_path.stat().st_size
    size_reduction = (1 - optimized_size / original_size) * 100

    # Verify COG optimization
    with rasterio.open(output_path) as cog:
        cog_validation = {
            'is_tiled': cog.is_tiled,
            'has_overviews': len(cog.overviews(1)) > 0,
            'overview_count': len(cog.overviews(1)),
            'compression': cog.compression,
            'block_shape': cog.block_shapes[0],
        }

    results = {
        'input_file': str(input_path),
        'output_file': str(output_path),
        'original_size_bytes': original_size,
        'optimized_size_bytes': optimized_size,
        'size_reduction_percent': size_reduction,
        'cog_validation': cog_validation,
        'optimization_settings': {
            'compression': compress,
            'tiled': tiled,
            'blocksize': blocksize,
            'overview_factors': overview_factors,
        },
        'creation_timestamp': pd.Timestamp.now().isoformat(),
    }

    logger.info(f"COG creation complete. Size reduction: {size_reduction:.1f}%")
    return results


# Helper functions for data validation and utilities

def validate_raster_file(file_path: Union[str, Path]) -> bool:
    """
    Validate that a file is a readable raster.

    Args:
        file_path: Path to the raster file

    Returns:
        True if valid raster, False otherwise
    """
    try:
        with rasterio.open(file_path) as src:
            # Try to read basic metadata
            _ = src.width, src.height, src.count
            return True
    except Exception:
        return False


def get_raster_summary(file_path: Union[str, Path]) -> str:
    """
    Get a quick text summary of a raster file.

    Args:
        file_path: Path to the raster file

    Returns:
        Formatted string summary
    """
    if not validate_raster_file(file_path):
        return f"Invalid or unreadable raster file: {file_path}"

    with rasterio.open(file_path) as src:
        summary = f"""
Raster Summary: {Path(file_path).name}
{'=' * 50}
Dimensions: {src.width} x {src.height} pixels
Bands: {src.count}
Data Type: {src.dtypes[0]}
CRS: {src.crs}
Bounds: {src.bounds}
Resolution: {abs(src.transform[0]):.6f} x {abs(src.transform[4]):.6f}
Tiled: {src.is_tiled}
Compression: {src.compression or 'None'}
        """.strip()

        return summary
