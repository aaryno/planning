"""
Rasterio Analysis Assignment - Advanced Raster Processing and Analysis
=====================================================================

This module contains 5 analytical functions for advanced raster data processing using rasterio.
Each function focuses on real-world GIS analysis applications including topographic analysis,
vegetation monitoring, point sampling, Cloud Optimized GeoTIFFs, and STAC integration.

Your task is to implement each function according to the specifications and pass all tests.

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Rasterio Analysis - Advanced Raster Data Analysis
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any, Optional
import geopandas as gpd
from shapely.geometry import Point
import requests
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.windows import from_bounds
import pystac
import pystac_client
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def calculate_topographic_metrics(dem_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive topographic metrics from a Digital Elevation Model (DEM).

    This function computes slope, aspect, and hillshade from elevation data, providing
    essential terrain analysis capabilities for geomorphological and hydrological studies.

    Args:
        dem_path (str): Path to the DEM raster file
        output_dir (Optional[str]): Directory to save output rasters (optional)

    Returns:
        Dict[str, Any]: Dictionary containing topographic analysis results:
            - 'slope_stats': Statistics of slope values (degrees)
            - 'aspect_stats': Statistics of aspect values (degrees)
            - 'hillshade_stats': Statistics of hillshade values (0-255)
            - 'terrain_classification': Dict with counts of terrain types
            - 'slope_array': 2D numpy array of slope values
            - 'aspect_array': 2D numpy array of aspect values
            - 'hillshade_array': 2D numpy array of hillshade values
            - 'files_created': List of output files created
            - 'cell_size': Resolution of the DEM in map units
            - 'elevation_range': Min and max elevation values

    Implementation Requirements:
        - Calculate slope in degrees using gradient method
        - Calculate aspect in degrees (0-360, where 0 = North)
        - Generate hillshade with sun azimuth=315°, altitude=45°
        - Classify terrain: flat (<2°), gentle (2-5°), moderate (5-15°),
          steep (15-30°), very steep (>30°)
        - Handle edge effects and nodata values appropriately
        - Optionally save slope, aspect, and hillshade as separate GeoTIFF files

    Example:
        >>> metrics = calculate_topographic_metrics('elevation.tif', 'outputs/')
        >>> print(f"Average slope: {metrics['slope_stats']['mean']:.1f} degrees")
        >>> print(f"Terrain types: {metrics['terrain_classification']}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open DEM and read elevation data
    # HINT: Use rasterio.open() and read the first band
    # HINT: Get transform and CRS for output files
    #
    # STEP 2: Calculate slope using gradient method
    # HINT: Use np.gradient() to get dx, dy derivatives
    # HINT: Convert to degrees: slope = np.arctan(np.sqrt(dx² + dy²)) * 180/π
    # HINT: Account for cell size in the calculation
    #
    # STEP 3: Calculate aspect using gradient method
    # HINT: aspect = np.arctan2(-dy, dx) * 180/π
    # HINT: Convert to 0-360° range (North = 0°)
    #
    # STEP 4: Calculate hillshade
    # HINT: Use illumination model with azimuth=315°, altitude=45°
    # HINT: Formula involves aspect, slope, and sun position
    #
    # STEP 5: Classify terrain based on slope thresholds
    # HINT: Use np.digitize() or conditional statements
    #
    # STEP 6: Calculate statistics for each metric
    # HINT: Use helper function or np statistical functions
    #
    # STEP 7: Optionally save outputs as GeoTIFF files
    # HINT: Use rasterio.open() in write mode with proper profile

    pass  # Replace with your implementation


def analyze_vegetation_indices(multispectral_path: str, red_band: int = 3,
                              nir_band: int = 4, blue_band: int = 1) -> Dict[str, Any]:
    """
    Calculate and analyze vegetation indices from multispectral imagery.

    This function computes NDVI, EVI, and other vegetation metrics, then classifies
    vegetation health and provides comprehensive analysis for ecological monitoring.

    Args:
        multispectral_path (str): Path to multispectral raster (e.g., Landsat, Sentinel)
        red_band (int): Band number for red wavelength (default: 3)
        nir_band (int): Band number for near-infrared (default: 4)
        blue_band (int): Band number for blue wavelength (default: 1)

    Returns:
        Dict[str, Any]: Dictionary containing vegetation analysis results:
            - 'ndvi_stats': NDVI statistics including mean, std, percentiles
            - 'evi_stats': Enhanced Vegetation Index statistics
            - 'vegetation_classification': Pixel counts for vegetation classes
            - 'ndvi_array': 2D numpy array of NDVI values
            - 'evi_array': 2D numpy array of EVI values
            - 'vegetation_mask': Boolean mask of vegetated areas (NDVI > 0.2)
            - 'health_assessment': Dict with vegetation health metrics
            - 'seasonal_suitability': Assessment for different seasons
            - 'water_mask': Boolean mask identifying water bodies (NDVI < 0)
            - 'bare_soil_mask': Boolean mask for bare soil/urban areas

    Implementation Requirements:
        - NDVI = (NIR - Red) / (NIR + Red)
        - EVI = 2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))
        - Classify vegetation: water (<0), bare soil (0-0.2), sparse vegetation (0.2-0.4),
          moderate vegetation (0.4-0.6), dense vegetation (0.6-0.8), very dense (>0.8)
        - Handle division by zero and invalid values
        - Provide vegetation health assessment based on NDVI distribution
        - Create masks for different land cover types

    Example:
        >>> analysis = analyze_vegetation_indices('landsat8.tif', red_band=4, nir_band=5)
        >>> print(f"Mean NDVI: {analysis['ndvi_stats']['mean']:.3f}")
        >>> print(f"Vegetated area: {analysis['vegetation_classification']['vegetated_pixels']:,} pixels")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open multispectral image and read required bands
    # HINT: Use rasterio.open() and read specific bands
    # HINT: Convert to float to avoid integer overflow in calculations
    #
    # STEP 2: Calculate NDVI with proper handling of invalid values
    # HINT: NDVI = (NIR - Red) / (NIR + Red)
    # HINT: Use np.where() to handle division by zero
    # HINT: Mask out values outside valid range [-1, 1]
    #
    # STEP 3: Calculate Enhanced Vegetation Index (EVI)
    # HINT: EVI = 2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))
    # HINT: Handle division by zero similarly to NDVI
    #
    # STEP 4: Classify vegetation based on NDVI thresholds
    # HINT: Create classification arrays using np.digitize() or conditions
    #
    # STEP 5: Create land cover masks
    # HINT: Water: NDVI < 0, Vegetation: NDVI > 0.2, etc.
    #
    # STEP 6: Calculate comprehensive statistics
    # HINT: Use np functions for mean, std, percentiles
    # HINT: Count pixels in each vegetation class
    #
    # STEP 7: Assess vegetation health and seasonal suitability
    # HINT: Based on NDVI distribution and statistical measures

    pass  # Replace with your implementation


def sample_raster_at_locations(raster_path: str, locations: List[Tuple[float, float]],
                              buffer_radius: float = 0, interpolation: str = 'nearest',
                              band_numbers: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Extract raster values at specified geographic locations with various sampling options.

    This function samples raster data at point locations with support for buffered sampling,
    different interpolation methods, and multi-band extraction for field validation and
    ground truth collection.

    Args:
        raster_path (str): Path to the raster file to sample
        locations (List[Tuple[float, float]]): List of (longitude, latitude) coordinates
        buffer_radius (float): Radius in map units for buffered sampling (0 = point sampling)
        interpolation (str): Interpolation method ('nearest', 'bilinear', 'cubic')
        band_numbers (Optional[List[int]]): Specific bands to sample (None = all bands)

    Returns:
        Dict[str, Any]: Dictionary containing sampling results:
            - 'sampled_values': List of dicts with values for each location
            - 'locations_geographic': Input coordinates in geographic CRS
            - 'locations_projected': Coordinates in raster CRS
            - 'sampling_summary': Statistics of sampled values per band
            - 'valid_samples': Count of successful samples
            - 'failed_samples': Count of failed samples (outside raster, nodata)
            - 'buffer_stats': If buffered, statistics within each buffer
            - 'interpolation_used': Interpolation method applied
            - 'crs_info': Information about coordinate transformations
            - 'raster_metadata': Basic info about the sampled raster

    Implementation Requirements:
        - Handle coordinate transformation between geographic and raster CRS
        - Support point sampling (buffer_radius = 0) and buffered sampling
        - Implement different interpolation methods for point sampling
        - For buffered sampling, calculate mean, std, min, max within buffer
        - Handle locations outside raster bounds gracefully
        - Support sampling from multiple bands
        - Provide detailed metadata about the sampling process

    Example:
        >>> locations = [(-120.5, 37.8), (-121.0, 37.5), (-119.5, 38.0)]
        >>> results = sample_raster_at_locations('elevation.tif', locations,
        ...                                     buffer_radius=100, interpolation='bilinear')
        >>> for i, values in enumerate(results['sampled_values']):
        ...     print(f"Location {i+1}: {values['elevation_mean']:.1f}m")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open raster and get metadata
    # HINT: Use rasterio.open() to get CRS, transform, bounds
    # HINT: Determine which bands to sample
    #
    # STEP 2: Handle coordinate transformation if needed
    # HINT: Check if input coordinates match raster CRS
    # HINT: Use pyproj or rasterio.warp.transform for reprojection
    #
    # STEP 3: Convert geographic coordinates to pixel indices
    # HINT: Use rasterio transform methods (~transform * coords)
    #
    # STEP 4: For each location, extract values based on sampling method
    # HINT: Point sampling: use array indexing with interpolation
    # HINT: Buffer sampling: define circular buffer and extract all pixels
    #
    # STEP 5: Handle different interpolation methods
    # HINT: 'nearest': simple array indexing
    # HINT: 'bilinear': weighted average of 4 nearest pixels
    # HINT: 'cubic': more complex interpolation algorithm
    #
    # STEP 6: Calculate buffer statistics if buffer_radius > 0
    # HINT: Use np.mean, np.std, np.min, np.max on pixels within buffer
    #
    # STEP 7: Compile results with comprehensive metadata
    # HINT: Track successful/failed samples, CRS info, etc.

    pass  # Replace with your implementation


def process_cloud_optimized_geotiff(cog_url: str, bounds: Optional[Tuple[float, float, float, float]] = None,
                                  target_resolution: Optional[float] = None,
                                  output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Efficiently process Cloud Optimized GeoTIFFs with windowed reading and analysis.

    This function demonstrates modern raster processing techniques including remote data access,
    windowed reading, and efficient processing of large datasets using COG capabilities.

    Args:
        cog_url (str): URL or path to Cloud Optimized GeoTIFF
        bounds (Optional[Tuple]): Bounding box to clip (left, bottom, right, top)
        target_resolution (Optional[float]): Target resolution for resampling (map units)
        output_path (Optional[str]): Path to save processed result

    Returns:
        Dict[str, Any]: Dictionary containing COG processing results:
            - 'cog_info': Metadata about the COG structure (overviews, tiles, etc.)
            - 'data_summary': Statistics of the processed data
            - 'processing_efficiency': Metrics about data transfer and processing
            - 'overview_levels': Available overview levels and their resolutions
            - 'optimal_overview': Recommended overview level for given bounds/resolution
            - 'bytes_read': Total bytes read from remote source
            - 'processing_time': Time taken for various processing steps
            - 'spatial_coverage': Information about spatial extent processed
            - 'resampling_info': Details about any resampling performed
            - 'file_saved': Whether output file was created

    Implementation Requirements:
        - Efficiently read only required data using windowed access
        - Analyze COG structure (tiled, overviews, compression)
        - Select optimal overview level based on target resolution/bounds
        - Implement efficient windowed reading to minimize data transfer
        - Support both local and remote COG access
        - Calculate processing efficiency metrics
        - Handle resampling if target resolution is specified
        - Provide comprehensive analysis of COG optimization benefits

    Example:
        >>> cog_url = "https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/044/034/LC08_L1TP_044034_20201231_20210106_02_T1/LC08_L1TP_044034_20201231_20210106_02_T1_B4.TIF"
        >>> bounds = (-120.5, 37.5, -120.0, 38.0)  # Small area of interest
        >>> result = process_cloud_optimized_geotiff(cog_url, bounds=bounds)
        >>> print(f"Data read: {result['bytes_read']:,} bytes")
        >>> print(f"Efficiency: Read {result['processing_efficiency']['data_reduction_factor']:.1f}x less data")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open COG and analyze structure
    # HINT: Use rasterio.open() with GDAL options for COG info
    # HINT: Check for tiling, overviews, compression using dataset properties
    #
    # STEP 2: Determine optimal reading strategy
    # HINT: If bounds specified, calculate window for reading
    # HINT: If target_resolution specified, select appropriate overview level
    # HINT: Use dataset.overviews() to get available levels
    #
    # STEP 3: Perform efficient windowed reading
    # HINT: Use rasterio.windows.from_bounds() for spatial window
    # HINT: Read data using dataset.read(window=window)
    # HINT: Track bytes read using dataset properties or file size info
    #
    # STEP 4: Handle resampling if needed
    # HINT: Use rasterio.warp.reproject() for resolution changes
    # HINT: Calculate new dimensions based on target resolution
    #
    # STEP 5: Analyze processing efficiency
    # HINT: Compare bytes read vs. full file size
    # HINT: Calculate data reduction factor
    # HINT: Time different processing steps
    #
    # STEP 6: Generate comprehensive COG analysis
    # HINT: Document tiling scheme, compression, overview structure
    # HINT: Assess COG optimization quality
    #
    # STEP 7: Save results if output path provided
    # HINT: Create new COG with proper tiling and compression

    pass  # Replace with your implementation


def query_stac_and_analyze(stac_catalog_url: str, bbox: Tuple[float, float, float, float],
                          datetime_range: str, collections: List[str],
                          analysis_type: str = 'ndvi_timeseries') -> Dict[str, Any]:
    """
    Query STAC catalogs and perform temporal analysis on satellite imagery.

    This function demonstrates modern geospatial data discovery and analysis workflows
    using STAC (SpatioTemporal Asset Catalog) for finding and analyzing time series
    of satellite imagery.

    Args:
        stac_catalog_url (str): URL of the STAC catalog to query
        bbox (Tuple[float, float, float, float]): Bounding box (west, south, east, north)
        datetime_range (str): Date range in ISO format (e.g., "2023-01-01/2023-12-31")
        collections (List[str]): STAC collection IDs to search
        analysis_type (str): Type of analysis ('ndvi_timeseries', 'change_detection', 'composite')

    Returns:
        Dict[str, Any]: Dictionary containing STAC query and analysis results:
            - 'items_found': Number of matching STAC items
            - 'date_range_actual': Actual date range of found items
            - 'collections_found': Collections that had matching items
            - 'temporal_coverage': Analysis of temporal distribution
            - 'analysis_results': Results specific to analysis_type
            - 'ndvi_timeseries': If applicable, NDVI values over time
            - 'change_metrics': If change detection, before/after statistics
            - 'composite_info': If composite, information about final product
            - 'data_gaps': Identified gaps in temporal coverage
            - 'cloud_coverage': Cloud coverage statistics for found scenes
            - 'processing_summary': Summary of data processing steps

    Implementation Requirements:
        - Use pystac_client to search STAC catalogs
        - Filter results by spatial, temporal, and collection criteria
        - Handle different analysis types with appropriate processing
        - For NDVI timeseries: calculate NDVI for each time step
        - For change detection: compare before/after periods
        - For composite: create cloud-free composite image
        - Assess data quality and coverage gaps
        - Provide comprehensive metadata about the analysis

    Example:
        >>> bbox = (-120.5, 37.5, -120.0, 38.0)  # San Francisco Bay Area
        >>> results = query_stac_and_analyze(
        ...     "https://earth-search.aws.element84.com/v1",
        ...     bbox, "2023-06-01/2023-08-31", ["sentinel-2-l2a"],
        ...     analysis_type='ndvi_timeseries')
        >>> print(f"Found {results['items_found']} Sentinel-2 scenes")
        >>> print(f"NDVI trend: {results['analysis_results']['trend_direction']}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Initialize STAC client and perform search
    # HINT: Use pystac_client.Client.open() to connect to catalog
    # HINT: Use client.search() with bbox, datetime, collections parameters
    #
    # STEP 2: Process search results and extract metadata
    # HINT: Iterate through items to get dates, collections, cloud coverage
    # HINT: Sort by date for temporal analysis
    #
    # STEP 3: Implement analysis based on analysis_type
    # HINT: For 'ndvi_timeseries': process each item to calculate NDVI
    # HINT: For 'change_detection': compare early vs late period
    # HINT: For 'composite': create cloud-free mosaic
    #
    # STEP 4: For NDVI timeseries analysis
    # HINT: Download red and NIR bands for each scene
    # HINT: Calculate NDVI and extract mean value for AOI
    # HINT: Create time series array with dates and NDVI values
    #
    # STEP 5: Analyze temporal patterns and data quality
    # HINT: Identify data gaps in time series
    # HINT: Assess cloud coverage impact on data quality
    # HINT: Calculate trend statistics if applicable
    #
    # STEP 6: Generate comprehensive analysis report
    # HINT: Include data discovery metrics, processing results
    # HINT: Provide recommendations for data usage
    #
    # STEP 7: Handle errors gracefully
    # HINT: Network errors, missing data, invalid responses
    # HINT: Provide useful error messages and partial results

    pass  # Replace with your implementation


# Helper functions for the assignment

def _calculate_hillshade(elevation: np.ndarray, cell_size: float,
                        azimuth: float = 315, altitude: float = 45) -> np.ndarray:
    """
    Helper function to calculate hillshade from elevation data.

    Args:
        elevation: 2D numpy array of elevation values
        cell_size: Resolution of the elevation data
        azimuth: Sun azimuth angle in degrees (315 = northwest)
        altitude: Sun altitude angle in degrees (45 = 45° above horizon)

    Returns:
        2D numpy array of hillshade values (0-255)
    """
    # Convert angles to radians
    azimuth_rad = np.radians(azimuth)
    altitude_rad = np.radians(altitude)

    # Calculate gradients
    dy, dx = np.gradient(elevation, cell_size)

    # Calculate slope and aspect
    slope = np.arctan(np.sqrt(dx**2 + dy**2))
    aspect = np.arctan2(-dx, dy)

    # Calculate hillshade
    hillshade = np.sin(altitude_rad) * np.sin(slope) + \
                np.cos(altitude_rad) * np.cos(slope) * \
                np.cos(azimuth_rad - aspect)

    # Convert to 0-255 range
    hillshade = np.clip(hillshade * 255, 0, 255)
    return hillshade.astype(np.uint8)


def _validate_coordinates(locations: List[Tuple[float, float]]) -> bool:
    """
    Helper function to validate coordinate pairs.

    Args:
        locations: List of (longitude, latitude) tuples

    Returns:
        bool: True if all coordinates are valid
    """
    for lon, lat in locations:
        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            return False
    return True


def _safe_divide(numerator: np.ndarray, denominator: np.ndarray,
                fill_value: float = np.nan) -> np.ndarray:
    """
    Helper function for safe division avoiding division by zero.

    Args:
        numerator: Numerator array
        denominator: Denominator array
        fill_value: Value to use when denominator is zero

    Returns:
        Result of division with safe handling of zero denominators
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = np.divide(numerator, denominator,
                          out=np.full_like(numerator, fill_value, dtype=float),
                          where=(denominator != 0))
    return result


def _create_sample_stac_response() -> Dict[str, Any]:
    """
    Helper function to create sample STAC response for testing when API is unavailable.

    Returns:
        Mock STAC response dictionary
    """
    return {
        'type': 'FeatureCollection',
        'features': [
            {
                'id': 'sample_scene_1',
                'bbox': [-120.5, 37.5, -120.0, 38.0],
                'properties': {
                    'datetime': '2023-07-15T18:30:00Z',
                    'eo:cloud_cover': 5.2,
                    'collection': 'sentinel-2-l2a'
                },
                'assets': {
                    'red': {'href': 'sample_red_band.tif'},
                    'nir': {'href': 'sample_nir_band.tif'}
                }
            }
        ]
    }


# Example usage and testing
if __name__ == "__main__":
    print("Rasterio Analysis Assignment - 5 Advanced Functions")
    print("=" * 55)
    print("Functions to implement:")
    print("1. calculate_topographic_metrics() - Slope, aspect, hillshade analysis")
    print("2. analyze_vegetation_indices() - NDVI, EVI, vegetation health assessment")
    print("3. sample_raster_at_locations() - Point sampling with interpolation")
    print("4. process_cloud_optimized_geotiff() - Efficient COG processing")
    print("5. query_stac_and_analyze() - STAC catalog search and temporal analysis")
    print("\nEach function includes comprehensive documentation and requirements.")
    print("Implement all functions to pass the automated tests!")
