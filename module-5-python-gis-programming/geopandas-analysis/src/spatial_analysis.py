"""
GIST 604B - Python GeoPandas Analysis
Essential Spatial Operations

This module contains functions for essential spatial analysis operations:
- Loading and exploring spatial datasets
- Calculating basic geometric properties
- Creating buffer zones for proximity analysis

Student: [Your Name]
Date: [Current Date]
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional, Any
import warnings

# Suppress coordinate system warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

# ============================================================================
# FUNCTION 1: LOAD AND EXPLORE SPATIAL DATA (6 points)
# ============================================================================

def load_and_explore_spatial_data(file_path: str) -> gpd.GeoDataFrame:
    """
    Load a spatial dataset and display comprehensive information about it.

    This function demonstrates the first step in any spatial analysis:
    loading spatial data and understanding its properties, coordinate system,
    geometry types, and spatial extent.

    Args:
        file_path (str): Path to spatial data file (shapefile, GeoJSON, etc.)

    Returns:
        gpd.GeoDataFrame: The loaded spatial dataset, or None if loading failed

    Example:
        >>> cities = load_and_explore_spatial_data('data/cities.geojson')
        Spatial dataset loaded successfully!
        File: data/cities.geojson
        CRS: EPSG:4326 (WGS84)
        Geometry type: Point
        Features: 150 cities
        Bounds: [-124.7, 32.5, -114.1, 42.0]

    TODO: Implement this function following these steps:

    1. Check if file exists:
       - Use Path(file_path).exists() to verify file exists
       - If not found, print error message and return None

    2. Load the spatial data:
       - Use gpd.read_file(file_path) to load the data
       - Handle common errors (invalid file format, corrupted data)
       - Print success message with file name

    3. Display basic spatial information:
       - Show file path and format
       - Display coordinate reference system (CRS)
       - Show geometry types present in the dataset
       - Display number of features (rows)
       - Show spatial bounds (extent)

    4. Display first few features:
       - Use .head() to show first 3-5 rows
       - Include both attributes and geometry

    5. Check for spatial data quality issues:
       - Check for missing CRS: gdf.crs is None
       - Check for invalid geometries: ~gdf.geometry.is_valid
       - Check for empty geometries: gdf.geometry.is_empty
       - Report any issues found

    6. Return the loaded GeoDataFrame

    Error handling should cover:
    - File not found
    - Unsupported file format
    - Corrupted or invalid spatial data
    - Empty datasets
    """

    print("=" * 60)
    print("LOADING AND EXPLORING SPATIAL DATA")
    print("=" * 60)

    # TODO: Implement load_and_explore_spatial_data function
    # Step 1: Check if file exists
    # Step 2: Load the spatial data with error handling
    # Step 3: Display basic spatial information
    # Step 4: Show first few features
    # Step 5: Check for spatial data quality issues
    # Step 6: Return the GeoDataFrame

    pass  # Remove this and implement your solution


# ============================================================================
# FUNCTION 2: CALCULATE BASIC SPATIAL METRICS (6 points)
# ============================================================================

def calculate_basic_spatial_metrics(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """
    Calculate essential geometric properties for spatial features.

    This function computes area, perimeter, and centroid information for
    spatial features, handling coordinate system conversions as needed for
    accurate measurements.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial dataset

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'areas': Series of area values (km² for polygons, 0 for others)
            - 'perimeters': Series of perimeter values (km for polygons/lines)
            - 'centroids': GeoSeries of centroid points
            - 'total_area': Sum of all polygon areas in km²
            - 'total_perimeter': Sum of all perimeters in km
            - 'geometry_types': Count of each geometry type
            - 'crs_used': CRS used for calculations

    Example:
        >>> metrics = calculate_basic_spatial_metrics(watersheds_gdf)
        Calculating spatial metrics for 25 watersheds...
        Reprojecting to UTM Zone 10N for accurate measurements...

        Metrics calculated:
        - Total area: 15,847.23 km²
        - Average area: 633.89 km²
        - Total perimeter: 2,156.78 km
        - All centroids generated successfully

    TODO: Implement this function following these steps:

    1. Input validation:
       - Check if gdf is empty or None
       - Verify it has a geometry column
       - Print dataset summary (number of features, geometry types)

    2. Handle coordinate reference system:
       - Check current CRS: gdf.crs
       - If geographic (like EPSG:4326), need to reproject for accurate measurements
       - Find appropriate UTM zone or use a projected CRS
       - Use gdf.to_crs() to reproject for calculations
       - Keep track of what CRS was used

    3. Calculate areas:
       - Use gdf.area to get area values
       - Convert from square meters to square kilometers (divide by 1,000,000)
       - Only polygons will have meaningful areas (points/lines = 0)

    4. Calculate perimeters:
       - Use gdf.length to get perimeter/length values
       - Convert from meters to kilometers (divide by 1,000)
       - Works for both lines (length) and polygons (perimeter)

    5. Calculate centroids:
       - Use gdf.centroid to generate centroid points
       - These work for all geometry types
       - May want to reproject back to original CRS for display

    6. Calculate summary statistics:
       - Total area (sum of polygon areas only)
       - Total perimeter (sum of all perimeters/lengths)
       - Count geometry types: gdf.geom_type.value_counts()

    7. Display results summary:
       - Print total and average areas
       - Print total perimeter
       - Show geometry type breakdown
       - Confirm all centroids generated successfully

    8. Return dictionary with all calculated values

    Note: Be careful with coordinate systems! Geographic coordinates
    (lat/lon) give incorrect area/distance measurements.
    """

    print("\n" + "=" * 60)
    print("CALCULATING BASIC SPATIAL METRICS")
    print("=" * 60)

    # TODO: Implement calculate_basic_spatial_metrics function
    # Step 1: Input validation
    # Step 2: Handle coordinate reference system
    # Step 3: Calculate areas (convert to km²)
    # Step 4: Calculate perimeters (convert to km)
    # Step 5: Calculate centroids
    # Step 6: Calculate summary statistics
    # Step 7: Display results summary
    # Step 8: Return dictionary with all results

    pass  # Remove this and implement your solution


# ============================================================================
# FUNCTION 3: CREATE SPATIAL BUFFER ANALYSIS (6 points)
# ============================================================================

def create_spatial_buffer_analysis(gdf: gpd.GeoDataFrame,
                                 buffer_distance: float) -> Dict[str, Any]:
    """
    Create buffer zones around spatial features and perform proximity analysis.

    This function generates buffer zones around features and calculates
    analysis metrics including total buffered area and overlap detection.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial features to buffer
        buffer_distance (float): Buffer distance in meters

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'buffered_gdf': GeoDataFrame with buffer geometries
            - 'original_gdf': Original features (for comparison)
            - 'buffer_areas': Series of individual buffer areas (km²)
            - 'total_buffered_area': Total area of all buffers (km²)
            - 'average_buffer_area': Average buffer area (km²)
            - 'overlapping_buffers': Number of overlapping buffer pairs
            - 'distance_used': Buffer distance applied (meters)
            - 'crs_used': CRS used for buffer calculations

    Example:
        >>> result = create_spatial_buffer_analysis(cities_gdf, 1000)
        Creating 1000m buffers around 50 cities...
        Reprojecting to appropriate UTM zone for buffer analysis...

        Buffer analysis complete:
        - Created 50 buffer zones
        - Total buffered area: 157.08 km²
        - Average buffer area: 3.14 km²
        - Buffer overlaps detected: 8 cases

    TODO: Implement this function following these steps:

    1. Input validation:
       - Check if gdf is empty or None
       - Validate buffer_distance is positive number
       - Print analysis summary (number of features, distance)

    2. Coordinate system handling:
       - Check current CRS
       - If geographic, reproject to appropriate projected CRS for buffering
       - UTM zones work well, or use local projected CRS
       - Remember original CRS for final output

    3. Create buffer zones:
       - Use gdf.buffer(buffer_distance) to create buffers
       - This creates circular buffers around points, expanded areas around polygons
       - Keep original attributes with buffered geometries

    4. Calculate buffer areas:
       - Use buffered_gdf.area to get buffer areas
       - Convert from square meters to square kilometers
       - Calculate total and average buffer areas

    5. Detect overlapping buffers:
       - Use buffered_gdf.unary_union to merge overlapping areas
       - Compare total individual areas vs. merged area
       - Count approximate number of overlapping pairs
       - Or use more sophisticated overlap detection

    6. Create visualization (optional but helpful):
       - Simple plot showing original features and buffers
       - Different colors for original vs. buffer zones
       - Use matplotlib or geopandas .plot() method

    7. Display results summary:
       - Number of buffers created
       - Total buffered area
       - Average buffer area
       - Number of overlaps detected
       - Distance and CRS used

    8. Return comprehensive results dictionary:
       - Include both original and buffered GeoDataFrames
       - Include all calculated metrics
       - Reproject back to original CRS if needed

    Note: Accurate buffering requires projected coordinates!
    Geographic coordinates (degrees) don't work for distance-based operations.
    """

    print("\n" + "=" * 60)
    print("CREATE SPATIAL BUFFER ANALYSIS")
    print("=" * 60)

    # TODO: Implement create_spatial_buffer_analysis function
    # Step 1: Input validation
    # Step 2: Handle coordinate system for accurate buffering
    # Step 3: Create buffer zones
    # Step 4: Calculate buffer areas
    # Step 5: Detect overlapping buffers
    # Step 6: Create visualization (optional)
    # Step 7: Display results summary
    # Step 8: Return comprehensive results dictionary

    pass  # Remove this and implement your solution


# ============================================================================
# HELPER FUNCTIONS (provided for your use)
# ============================================================================

def _determine_utm_zone(gdf: gpd.GeoDataFrame) -> str:
    """
    Helper function to determine appropriate UTM zone for a dataset.

    Args:
        gdf: GeoDataFrame to analyze

    Returns:
        str: EPSG code for appropriate UTM zone
    """
    # Get centroid of the dataset bounds
    bounds = gdf.total_bounds
    center_lon = (bounds[0] + bounds[2]) / 2
    center_lat = (bounds[1] + bounds[3]) / 2

    # Calculate UTM zone from longitude
    utm_zone = int((center_lon + 180) / 6) + 1

    # Determine hemisphere (North/South)
    hemisphere = 'N' if center_lat >= 0 else 'S'

    # Convert to EPSG code
    if hemisphere == 'N':
        epsg_code = f"EPSG:326{utm_zone:02d}"
    else:
        epsg_code = f"EPSG:327{utm_zone:02d}"

    return epsg_code


def _format_area(area_km2: float) -> str:
    """
    Helper function to format area values for display.

    Args:
        area_km2: Area in square kilometers

    Returns:
        str: Formatted area string
    """
    if area_km2 < 1:
        return f"{area_km2*1000000:.2f} m²"
    elif area_km2 < 1000:
        return f"{area_km2:.2f} km²"
    else:
        return f"{area_km2:,.2f} km²"


def _format_distance(distance_km: float) -> str:
    """
    Helper function to format distance values for display.

    Args:
        distance_km: Distance in kilometers

    Returns:
        str: Formatted distance string
    """
    if distance_km < 1:
        return f"{distance_km*1000:.0f} m"
    else:
        return f"{distance_km:.2f} km"
