"""
Band Math - Part 2 of Python Rasterio Assignment

This module contains functions for working with multi-band imagery and
calculating vegetation indices. Each function has detailed step-by-step
instructions to guide you through the implementation.

NDVI (Normalized Difference Vegetation Index) is one of the most common
vegetation indices used in remote sensing. It helps identify healthy
vegetation by comparing red and near-infrared light reflectance.

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Working with Raster Data
"""

# Import the libraries we need
import rasterio
import numpy as np
from pathlib import Path
from typing import Dict, List, Union, Any, Tuple
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=RuntimeWarning)


def calculate_ndvi(raster_path: str, red_band: int = 3, nir_band: int = 4) -> Dict[str, Any]:
    """
    Calculate NDVI (Normalized Difference Vegetation Index) from multi-band imagery.

    NDVI is calculated using this formula:
    NDVI = (NIR - Red) / (NIR + Red)

    Where:
    - NIR = Near-Infrared band (usually band 4 in Landsat)
    - Red = Red band (usually band 3 in Landsat)

    NDVI values range from -1 to 1:
    - Values near 1 = healthy, dense vegetation
    - Values near 0 = bare soil or rock
    - Negative values = water or clouds

    Args:
        raster_path (str): Path to the multi-band raster file
        red_band (int): Band number for red light (default: 3)
        nir_band (int): Band number for near-infrared (default: 4)

    Returns:
        Dict[str, Any]: Dictionary containing NDVI array and statistics

    Example return format:
        {
            'ndvi_array': numpy_array,  # 2D array of NDVI values
            'min_ndvi': -0.2,
            'max_ndvi': 0.8,
            'mean_ndvi': 0.4,
            'vegetation_pixels': 15432,
            'total_pixels': 20000
        }
    """
    # STEP 1: Open the multi-band raster file
    with rasterio.open(raster_path) as src:

        # STEP 2: Check that we have enough bands
        if src.count < max(red_band, nir_band):
            raise ValueError(f"Raster only has {src.count} bands, but you requested bands {red_band} and {nir_band}")

        # STEP 3: Read the red and near-infrared bands
        # HINT: Use src.read(band_number) to read each band
        # The result will be a 2D numpy array for each band

        red_data = src.read(red_band).astype(np.float32)   # Convert to float for calculations
        nir_data = src.read(nir_band).astype(np.float32)   # Convert to float for calculations

        # STEP 4: Handle nodata values
        # Get the nodata value from the raster
        nodata_value = src.nodata
        if nodata_value is not None:
            # Create masks for valid data (not nodata)
            red_valid = red_data != nodata_value
            nir_valid = nir_data != nodata_value
            valid_mask = red_valid & nir_valid  # Both bands must be valid
        else:
            valid_mask = np.ones_like(red_data, dtype=bool)  # All pixels are valid

        # STEP 5: Calculate NDVI using the formula
        # NDVI = (NIR - Red) / (NIR + Red)

        # Initialize NDVI array with NaN (Not a Number) values
        ndvi = np.full_like(red_data, np.nan, dtype=np.float32)

        # Calculate the sum and difference for valid pixels
        nir_plus_red = nir_data + red_data
        nir_minus_red = nir_data - red_data

        # Only calculate NDVI where:
        # 1. Both bands have valid data
        # 2. The denominator (NIR + Red) is not zero
        calculation_mask = valid_mask & (nir_plus_red != 0)

        # TODO: Calculate NDVI for valid pixels
        # HINT: Use the mask to only calculate where it's safe
        ndvi[calculation_mask] = nir_minus_red[calculation_mask] / nir_plus_red[calculation_mask]

        # STEP 6: Calculate statistics for the NDVI values
        # Get only the valid NDVI values (not NaN)
        valid_ndvi = ndvi[~np.isnan(ndvi)]

        if len(valid_ndvi) > 0:
            min_ndvi = float(np.min(valid_ndvi))
            max_ndvi = float(np.max(valid_ndvi))
            mean_ndvi = float(np.mean(valid_ndvi))

            # Count vegetation pixels (NDVI > 0.2 is often considered vegetation)
            vegetation_pixels = int(np.sum(valid_ndvi > 0.2))
        else:
            min_ndvi = None
            max_ndvi = None
            mean_ndvi = None
            vegetation_pixels = 0

        # STEP 7: Create the result dictionary
        result = {
            'ndvi_array': ndvi,
            'min_ndvi': min_ndvi,
            'max_ndvi': max_ndvi,
            'mean_ndvi': mean_ndvi,
            'vegetation_pixels': vegetation_pixels,
            'total_pixels': int(np.sum(valid_mask)),
            'nodata_pixels': int(np.sum(~valid_mask))
        }

        # STEP 8: Return the results
        return result


def analyze_vegetation(ndvi_array: np.ndarray) -> Dict[str, Any]:
    """
    Classify vegetation health based on NDVI values.

    This function takes an NDVI array and classifies each pixel into
    vegetation health categories commonly used by ecologists and
    land managers.

    Classification scheme:
    - Water/Clouds: NDVI < 0
    - Non-vegetation: 0 ≤ NDVI < 0.2 (bare soil, buildings, rocks)
    - Sparse vegetation: 0.2 ≤ NDVI < 0.4 (grassland, sparse shrubs)
    - Moderate vegetation: 0.4 ≤ NDVI < 0.7 (crops, mixed vegetation)
    - Dense vegetation: NDVI ≥ 0.7 (forests, healthy crops)

    Args:
        ndvi_array (np.ndarray): 2D array of NDVI values from calculate_ndvi()

    Returns:
        Dict[str, Any]: Dictionary containing classification results

    Example return format:
        {
            'water_clouds': {'pixels': 1200, 'percent': 6.0},
            'non_vegetation': {'pixels': 5000, 'percent': 25.0},
            'sparse_vegetation': {'pixels': 8000, 'percent': 40.0},
            'moderate_vegetation': {'pixels': 4800, 'percent': 24.0},
            'dense_vegetation': {'pixels': 1000, 'percent': 5.0},
            'total_valid_pixels': 20000,
            'classification_array': numpy_array
        }
    """
    # STEP 1: Get only valid NDVI values (not NaN)
    valid_mask = ~np.isnan(ndvi_array)
    valid_ndvi = ndvi_array[valid_mask]
    total_valid = len(valid_ndvi)

    # STEP 2: Create a classification array
    # Start with all pixels as 0 (will represent non-vegetation)
    classification = np.zeros_like(ndvi_array, dtype=np.int8)

    # Set invalid pixels to -1 (for nodata/NaN)
    classification[~valid_mask] = -1

    # STEP 3: Classify pixels based on NDVI values
    # TODO: Use boolean indexing to classify pixels into categories

    # Classification codes:
    # -1 = No data
    #  0 = Water/Clouds (NDVI < 0)
    #  1 = Non-vegetation (0 <= NDVI < 0.2)
    #  2 = Sparse vegetation (0.2 <= NDVI < 0.4)
    #  3 = Moderate vegetation (0.4 <= NDVI < 0.7)
    #  4 = Dense vegetation (NDVI >= 0.7)

    # Water/Clouds: NDVI < 0
    classification[valid_mask & (ndvi_array < 0)] = 0

    # Non-vegetation: 0 <= NDVI < 0.2
    classification[valid_mask & (ndvi_array >= 0) & (ndvi_array < 0.2)] = 1

    # Sparse vegetation: 0.2 <= NDVI < 0.4
    classification[valid_mask & (ndvi_array >= 0.2) & (ndvi_array < 0.4)] = 2

    # Moderate vegetation: 0.4 <= NDVI < 0.7
    classification[valid_mask & (ndvi_array >= 0.4) & (ndvi_array < 0.7)] = 3

    # Dense vegetation: NDVI >= 0.7
    classification[valid_mask & (ndvi_array >= 0.7)] = 4

    # STEP 4: Count pixels in each category
    # TODO: Count how many pixels fall into each category
    # HINT: Use np.sum() with boolean conditions

    water_clouds_count = int(np.sum(classification == 0))
    non_vegetation_count = int(np.sum(classification == 1))
    sparse_vegetation_count = int(np.sum(classification == 2))
    moderate_vegetation_count = int(np.sum(classification == 3))
    dense_vegetation_count = int(np.sum(classification == 4))

    # STEP 5: Calculate percentages
    # TODO: Calculate what percentage of valid pixels each category represents

    if total_valid > 0:
        water_clouds_percent = (water_clouds_count / total_valid) * 100
        non_vegetation_percent = (non_vegetation_count / total_valid) * 100
        sparse_vegetation_percent = (sparse_vegetation_count / total_valid) * 100
        moderate_vegetation_percent = (moderate_vegetation_count / total_valid) * 100
        dense_vegetation_percent = (dense_vegetation_count / total_valid) * 100
    else:
        water_clouds_percent = 0
        non_vegetation_percent = 0
        sparse_vegetation_percent = 0
        moderate_vegetation_percent = 0
        dense_vegetation_percent = 0

    # STEP 6: Create the results dictionary
    results = {
        'water_clouds': {
            'pixels': water_clouds_count,
            'percent': round(water_clouds_percent, 2)
        },
        'non_vegetation': {
            'pixels': non_vegetation_count,
            'percent': round(non_vegetation_percent, 2)
        },
        'sparse_vegetation': {
            'pixels': sparse_vegetation_count,
            'percent': round(sparse_vegetation_percent, 2)
        },
        'moderate_vegetation': {
            'pixels': moderate_vegetation_count,
            'percent': round(moderate_vegetation_percent, 2)
        },
        'dense_vegetation': {
            'pixels': dense_vegetation_count,
            'percent': round(dense_vegetation_percent, 2)
        },
        'total_valid_pixels': total_valid,
        'classification_array': classification
    }

    # STEP 7: Return the results
    return results


# BONUS: Helper function to print vegetation analysis results nicely
def print_vegetation_summary(analysis_results: Dict[str, Any]):
    """
    Print a nice summary of vegetation analysis results.

    This is a bonus function that makes the results easier to read.
    You don't need to modify this!
    """
    print("\n=== VEGETATION ANALYSIS SUMMARY ===")
    print(f"Total analyzed pixels: {analysis_results['total_valid_pixels']:,}")
    print()

    categories = [
        ('Water/Clouds', 'water_clouds'),
        ('Non-vegetation', 'non_vegetation'),
        ('Sparse vegetation', 'sparse_vegetation'),
        ('Moderate vegetation', 'moderate_vegetation'),
        ('Dense vegetation', 'dense_vegetation')
    ]

    for name, key in categories:
        count = analysis_results[key]['pixels']
        percent = analysis_results[key]['percent']
        print(f"{name:18}: {count:8,} pixels ({percent:5.1f}%)")

    print("=" * 40)


# BONUS: Helper function to create a simple vegetation health map
def print_ndvi_interpretation(ndvi_value: float):
    """
    Interpret what an NDVI value means in practical terms.

    This helps students understand what NDVI values represent in the real world.
    """
    if ndvi_value < 0:
        return "Water, clouds, or snow"
    elif ndvi_value < 0.2:
        return "Bare soil, buildings, or rocks"
    elif ndvi_value < 0.4:
        return "Sparse vegetation (grassland, desert shrubs)"
    elif ndvi_value < 0.7:
        return "Moderate vegetation (crops, mixed forest)"
    else:
        return "Dense, healthy vegetation (forests, healthy crops)"


# Example usage (you can run this to test your functions):
if __name__ == "__main__":
    # Test with a sample file (you'll need to provide a real path)
    # sample_file = "data/sample_landsat.tif"
    #
    # print("Calculating NDVI...")
    # ndvi_results = calculate_ndvi(sample_file)
    # print(f"NDVI range: {ndvi_results['min_ndvi']:.3f} to {ndvi_results['max_ndvi']:.3f}")
    # print(f"Mean NDVI: {ndvi_results['mean_ndvi']:.3f}")
    #
    # print("\nAnalyzing vegetation...")
    # veg_analysis = analyze_vegetation(ndvi_results['ndvi_array'])
    # print_vegetation_summary(veg_analysis)

    pass
