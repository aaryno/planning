"""
Raster Basics - Part 1 of Python Rasterio Assignment

This module contains the basic functions for reading and analyzing raster data.
Each function has detailed step-by-step instructions to guide you through
the implementation.

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Working with Raster Data
"""

# Import the libraries we need
import rasterio
import numpy as np
from pathlib import Path
from typing import Dict, List, Union, Any


def read_raster_info(raster_path: str) -> Dict[str, Any]:
    """
    Read basic information about a raster file.

    This function opens a raster file and extracts basic metadata like
    dimensions, number of bands, and coordinate system information.

    Args:
        raster_path (str): Path to the raster file

    Returns:
        Dict[str, Any]: Dictionary containing raster information

    Example return format:
        {
            'width': 1024,
            'height': 768,
            'count': 3,
            'crs': 'EPSG:4326',
            'driver': 'GTiff'
        }
    """
    # STEP 1: Open the raster file using rasterio
    # HINT: Use 'with rasterio.open(raster_path) as src:' to safely open the file
    with rasterio.open(raster_path) as src:

        # STEP 2: Extract the basic properties
        # HINT: Available properties include src.width, src.height, src.count, src.crs, src.driver

        # TODO: Create a dictionary with the raster information
        # Fill in the values using src.property_name
        info = {
            'width': src.width,           # Width in pixels
            'height': src.height,         # Height in pixels
            'count': src.count,           # Number of bands
            'crs': str(src.crs),         # Coordinate reference system
            'driver': src.driver          # File format driver (like 'GTiff')
        }

        # STEP 3: Return the information dictionary
        return info

    # NOTE: The 'with' statement automatically closes the file when done!


def get_raster_stats(raster_path: str, band_number: int = 1) -> Dict[str, float]:
    """
    Calculate basic statistics for a raster band.

    This function reads a specific band from a raster file and calculates
    common statistics like minimum, maximum, mean, and standard deviation.

    Args:
        raster_path (str): Path to the raster file
        band_number (int): Which band to analyze (1-based indexing)

    Returns:
        Dict[str, float]: Dictionary containing statistics

    Example return format:
        {
            'min': 0.0,
            'max': 255.0,
            'mean': 127.5,
            'std': 73.9,
            'nodata_count': 42
        }
    """
    # STEP 1: Open the raster file
    with rasterio.open(raster_path) as src:

        # STEP 2: Read the specified band as a numpy array
        # HINT: Use src.read(band_number) to read a specific band
        # The result will be a 2D numpy array
        band_data = src.read(band_number)

        # STEP 3: Handle nodata values
        # HINT: Get the nodata value with src.nodata
        nodata_value = src.nodata

        # STEP 4: Create a mask for valid data
        # If there's a nodata value, mask it out. Otherwise, use all data.
        if nodata_value is not None:
            # Create boolean mask: True for valid data, False for nodata
            valid_mask = band_data != nodata_value
            valid_data = band_data[valid_mask]
            nodata_count = np.sum(~valid_mask)  # Count of nodata pixels
        else:
            valid_data = band_data
            nodata_count = 0

        # STEP 5: Calculate statistics using numpy functions
        # TODO: Calculate min, max, mean, and standard deviation
        # HINT: Use np.min(), np.max(), np.mean(), np.std()

        stats = {
            'min': float(np.min(valid_data)) if len(valid_data) > 0 else None,
            'max': float(np.max(valid_data)) if len(valid_data) > 0 else None,
            'mean': float(np.mean(valid_data)) if len(valid_data) > 0 else None,
            'std': float(np.std(valid_data)) if len(valid_data) > 0 else None,
            'nodata_count': int(nodata_count)
        }

        # STEP 6: Return the statistics dictionary
        return stats


def get_raster_extent(raster_path: str) -> Dict[str, float]:
    """
    Get the geographic extent (bounding box) of a raster.

    This function extracts the geographic bounds of the raster in its
    coordinate reference system.

    Args:
        raster_path (str): Path to the raster file

    Returns:
        Dict[str, float]: Dictionary containing extent information

    Example return format:
        {
            'left': -120.5,      # Western boundary
            'bottom': 35.0,      # Southern boundary
            'right': -119.5,     # Eastern boundary
            'top': 36.0,         # Northern boundary
            'width': 1.0,        # Width in coordinate units
            'height': 1.0        # Height in coordinate units
        }
    """
    # STEP 1: Open the raster file
    with rasterio.open(raster_path) as src:

        # STEP 2: Get the bounds
        # HINT: Use src.bounds which returns a BoundingBox object
        # The bounds are in order: (left, bottom, right, top)
        bounds = src.bounds

        # STEP 3: Extract individual boundary values
        # TODO: Get the left, bottom, right, and top coordinates
        left = bounds.left      # Western edge
        bottom = bounds.bottom  # Southern edge
        right = bounds.right    # Eastern edge
        top = bounds.top        # Northern edge

        # STEP 4: Calculate width and height
        # TODO: Calculate the width and height of the extent
        width = right - left
        height = top - bottom

        # STEP 5: Create the extent dictionary
        extent = {
            'left': float(left),
            'bottom': float(bottom),
            'right': float(right),
            'top': float(top),
            'width': float(width),
            'height': float(height)
        }

        # STEP 6: Return the extent information
        return extent


# BONUS: Helper function to print raster info in a nice format
def print_raster_summary(raster_path: str):
    """
    Print a nice summary of raster information.

    This is a bonus function that combines the other functions
    to create a readable summary. You don't need to modify this!
    """
    print(f"\n=== RASTER SUMMARY: {Path(raster_path).name} ===")

    # Get basic info
    info = read_raster_info(raster_path)
    print(f"Dimensions: {info['width']} x {info['height']} pixels")
    print(f"Bands: {info['count']}")
    print(f"Format: {info['driver']}")
    print(f"CRS: {info['crs']}")

    # Get extent
    extent = get_raster_extent(raster_path)
    print(f"\nExtent:")
    print(f"  Left: {extent['left']:.6f}")
    print(f"  Right: {extent['right']:.6f}")
    print(f"  Bottom: {extent['bottom']:.6f}")
    print(f"  Top: {extent['top']:.6f}")

    # Get stats for first band
    stats = get_raster_stats(raster_path, band_number=1)
    print(f"\nBand 1 Statistics:")
    print(f"  Min: {stats['min']}")
    print(f"  Max: {stats['max']}")
    print(f"  Mean: {stats['mean']:.2f}" if stats['mean'] else "  Mean: None")
    print(f"  Std Dev: {stats['std']:.2f}" if stats['std'] else "  Std Dev: None")
    print(f"  NoData pixels: {stats['nodata_count']}")

    print("=" * 50)


# Example usage (you can run this to test your functions):
if __name__ == "__main__":
    # Test with a sample file (you'll need to provide a real path)
    # sample_file = "data/sample_elevation.tif"
    # print_raster_summary(sample_file)
    pass
