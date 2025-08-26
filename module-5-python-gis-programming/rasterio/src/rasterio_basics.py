"""
Python Rasterio Assignment - Core Functions
===========================================

This module contains 4 core functions for working with raster data using the rasterio library.
Each function focuses on a fundamental aspect of raster data processing.

Your task is to implement each function according to the specifications and pass all tests.

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Simplified Raster Data Processing
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any, Optional
from rasterio.windows import Window
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box


def load_and_explore_raster(raster_path: str) -> Dict[str, Any]:
    """
    Load a raster file and extract comprehensive information about its properties.

    This function opens a raster file and returns detailed metadata including
    dimensions, coordinate reference system, data types, and basic statistics.

    Args:
        raster_path (str): Path to the raster file to analyze

    Returns:
        Dict[str, Any]: Dictionary containing raster information with keys:
            - 'width': Width in pixels (int)
            - 'height': Height in pixels (int)
            - 'count': Number of bands (int)
            - 'crs': Coordinate reference system as string
            - 'driver': File format driver (str)
            - 'dtype': Data type of the raster (str)
            - 'nodata': NoData value (float or None)
            - 'bounds': Geographic bounds as dict with 'left', 'bottom', 'right', 'top'
            - 'transform': Affine transformation parameters (list of 6 values)
            - 'pixel_size': Pixel resolution as tuple (x_res, y_res)

    Example:
        >>> info = load_and_explore_raster('elevation.tif')
        >>> print(f"Raster size: {info['width']} x {info['height']}")
        >>> print(f"CRS: {info['crs']}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open the raster file using rasterio.open()
    # HINT: Use a 'with' statement to ensure proper file handling
    #
    # STEP 2: Extract basic properties (width, height, count, crs, driver, dtype, nodata)
    # HINT: These are properties of the rasterio dataset object
    #
    # STEP 3: Get the geographic bounds
    # HINT: Use dataset.bounds which returns left, bottom, right, top
    #
    # STEP 4: Get the transformation matrix
    # HINT: Use dataset.transform and convert to list if needed
    #
    # STEP 5: Calculate pixel size from the transformation
    # HINT: Transform[0] is x pixel size, abs(transform[4]) is y pixel size
    #
    # STEP 6: Return all information as a dictionary

    pass  # Replace with your implementation


def calculate_raster_statistics(raster_path: str, band_number: int = 1,
                               exclude_nodata: bool = True) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for a specific band in a raster dataset.

    This function computes various statistical measures including basic stats
    (min, max, mean, std) and additional metrics like percentiles and data range.

    Args:
        raster_path (str): Path to the raster file
        band_number (int): Band number to analyze (1-based indexing)
        exclude_nodata (bool): Whether to exclude nodata values from calculations

    Returns:
        Dict[str, float]: Dictionary containing statistical measures:
            - 'min': Minimum value
            - 'max': Maximum value
            - 'mean': Average value
            - 'median': Median value
            - 'std': Standard deviation
            - 'range': Data range (max - min)
            - 'percentile_25': 25th percentile
            - 'percentile_75': 75th percentile
            - 'valid_pixels': Count of valid (non-nodata) pixels
            - 'total_pixels': Total number of pixels
            - 'nodata_pixels': Count of nodata pixels

    Example:
        >>> stats = calculate_raster_statistics('elevation.tif', band_number=1)
        >>> print(f"Elevation range: {stats['min']:.1f} to {stats['max']:.1f}")
        >>> print(f"Average elevation: {stats['mean']:.1f}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open the raster file
    # HINT: Use rasterio.open() with 'with' statement
    #
    # STEP 2: Read the specified band as a numpy array
    # HINT: Use dataset.read(band_number) to get the data
    #
    # STEP 3: Handle nodata values
    # HINT: Get nodata value with dataset.nodata
    # HINT: Create a mask for valid data if exclude_nodata is True
    #
    # STEP 4: Calculate basic statistics
    # HINT: Use numpy functions like np.min(), np.max(), np.mean(), np.std()
    # HINT: Use np.median() and np.percentile() for additional stats
    #
    # STEP 5: Count pixels (total, valid, nodata)
    # HINT: Use array.size for total, np.sum() on masks for counts
    #
    # STEP 6: Return all statistics as a dictionary
    # HINT: Convert numpy types to Python types (float, int) for JSON compatibility

    pass  # Replace with your implementation


def extract_raster_subset(raster_path: str, bounds: Tuple[float, float, float, float],
                         output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract a spatial subset from a raster using geographic bounds.

    This function clips a raster to a specified bounding box and optionally
    saves the result to a new file. It returns information about the subset.

    Args:
        raster_path (str): Path to the input raster file
        bounds (Tuple[float, float, float, float]): Bounding box as (left, bottom, right, top)
        output_path (Optional[str]): Path to save the clipped raster (optional)

    Returns:
        Dict[str, Any]: Dictionary containing subset information:
            - 'subset_bounds': Actual bounds of the extracted subset
            - 'subset_width': Width of subset in pixels
            - 'subset_height': Height of subset in pixels
            - 'subset_transform': Affine transform of the subset
            - 'original_bounds': Bounds of the original raster
            - 'data_summary': Basic stats of the subset data
            - 'file_saved': Boolean indicating if file was saved
            - 'output_path': Path where file was saved (if applicable)

    Example:
        >>> bounds = (-120.5, 35.0, -119.5, 36.0)  # left, bottom, right, top
        >>> result = extract_raster_subset('elevation.tif', bounds, 'subset.tif')
        >>> print(f"Subset size: {result['subset_width']} x {result['subset_height']}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open the source raster
    # HINT: Use rasterio.open() with 'with' statement
    #
    # STEP 2: Create a bounding box geometry from the bounds
    # HINT: Use shapely.geometry.box(left, bottom, right, top)
    #
    # STEP 3: Clip the raster using the bounding box
    # HINT: Use rasterio.mask.mask() function with the geometry
    # HINT: mask() returns (clipped_data, clipped_transform)
    #
    # STEP 4: Get information about the clipped data
    # HINT: Check the shape of clipped_data for dimensions
    # HINT: Calculate basic statistics of the clipped data
    #
    # STEP 5: If output_path is provided, save the clipped raster
    # HINT: Use rasterio.open() in write mode with the same profile as source
    # HINT: Update the profile with new transform, width, height
    #
    # STEP 6: Return comprehensive information about the operation
    # HINT: Include original bounds, subset bounds, dimensions, and file info

    pass  # Replace with your implementation


def visualize_raster_data(raster_path: str, band_number: int = 1,
                         colormap: str = 'viridis', figsize: Tuple[int, int] = (10, 8),
                         title: Optional[str] = None, save_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a visualization of raster data with proper styling and information.

    This function creates a matplotlib plot of the raster data with customizable
    styling, colormap, and optional saving capability.

    Args:
        raster_path (str): Path to the raster file
        band_number (int): Band number to visualize (1-based indexing)
        colormap (str): Matplotlib colormap name (e.g., 'viridis', 'terrain', 'hot')
        figsize (Tuple[int, int]): Figure size as (width, height) in inches
        title (Optional[str]): Custom title for the plot
        save_path (Optional[str]): Path to save the plot (optional)

    Returns:
        Dict[str, Any]: Dictionary containing visualization information:
            - 'data_range': Min and max values of the displayed data
            - 'data_stats': Basic statistics of the visualized data
            - 'figure_size': Actual figure size used
            - 'colormap_used': Colormap applied to the visualization
            - 'plot_saved': Boolean indicating if plot was saved
            - 'save_path': Path where plot was saved (if applicable)
            - 'valid_pixels_displayed': Count of valid pixels shown

    Example:
        >>> viz_info = visualize_raster_data('elevation.tif', colormap='terrain',
        ...                                 title='Elevation Map', save_path='elevation_map.png')
        >>> print(f"Displayed data range: {viz_info['data_range']}")
    """
    # TODO: Implement this function
    #
    # STEP 1: Open and read the raster data
    # HINT: Use rasterio.open() and read the specified band
    #
    # STEP 2: Handle nodata values for visualization
    # HINT: Create a masked array to hide nodata values in the plot
    # HINT: Use np.ma.masked_where() or similar
    #
    # STEP 3: Create the matplotlib figure and axis
    # HINT: Use plt.subplots() with the specified figsize
    #
    # STEP 4: Display the raster data
    # HINT: Use plt.imshow() or ax.imshow() with the specified colormap
    # HINT: Set proper extent using raster bounds for geographic context
    #
    # STEP 5: Add plot enhancements
    # HINT: Add colorbar, title, axis labels
    # HINT: Set title using provided title or generate from filename
    #
    # STEP 6: Save the plot if save_path is provided
    # HINT: Use plt.savefig() with appropriate DPI and bbox_inches settings
    #
    # STEP 7: Calculate and return information about the visualization
    # HINT: Include data range, statistics, and file information

    pass  # Replace with your implementation


# Helper functions (students don't need to modify these)

def _validate_raster_path(raster_path: str) -> None:
    """Validate that the raster path exists and is readable."""
    if not Path(raster_path).exists():
        raise FileNotFoundError(f"Raster file not found: {raster_path}")


def _safe_stats_calculation(data: np.ndarray, exclude_nodata: bool = True,
                           nodata_value: Optional[float] = None) -> Dict[str, float]:
    """Helper function to safely calculate statistics with nodata handling."""
    if exclude_nodata and nodata_value is not None:
        valid_mask = data != nodata_value
        valid_data = data[valid_mask]
    else:
        valid_data = data.flatten()

    if len(valid_data) == 0:
        return {
            'min': None, 'max': None, 'mean': None, 'median': None,
            'std': None, 'range': None, 'percentile_25': None, 'percentile_75': None
        }

    return {
        'min': float(np.min(valid_data)),
        'max': float(np.max(valid_data)),
        'mean': float(np.mean(valid_data)),
        'median': float(np.median(valid_data)),
        'std': float(np.std(valid_data)),
        'range': float(np.ptp(valid_data)),  # peak-to-peak (max - min)
        'percentile_25': float(np.percentile(valid_data, 25)),
        'percentile_75': float(np.percentile(valid_data, 75))
    }


# Example usage and testing (students can use this to test their functions)
if __name__ == "__main__":
    # Example test code (uncomment and modify paths as needed)

    # Test load_and_explore_raster
    # sample_raster = "data/sample_elevation.tif"  # Update with actual path
    # info = load_and_explore_raster(sample_raster)
    # print("Raster Info:", info)

    # Test calculate_raster_statistics
    # stats = calculate_raster_statistics(sample_raster)
    # print("Raster Statistics:", stats)

    # Test extract_raster_subset
    # bounds = (-120.0, 35.0, -119.0, 36.0)  # Example bounds
    # subset_info = extract_raster_subset(sample_raster, bounds)
    # print("Subset Info:", subset_info)

    # Test visualize_raster_data
    # viz_info = visualize_raster_data(sample_raster, title="Test Visualization")
    # print("Visualization Info:", viz_info)

    print("All functions are defined. Implement them to pass the tests!")
