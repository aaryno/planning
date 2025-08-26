"""
Rasterio Basics - Python Rasterio Assignment

This module contains 4 core functions for working with raster data using rasterio.
Students should implement each function by replacing the TODO sections with working code.

Functions to implement:
1. load_and_explore_raster() - Load and examine raster metadata
2. calculate_raster_statistics() - Analyze pixel values and statistics
3. extract_raster_subset() - Extract spatial subsets using windowed reading
4. visualize_raster_data() - Create professional raster visualizations

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Working with Raster Data
"""

# Import the libraries you'll need
import rasterio
from rasterio.windows import Window, from_bounds
from rasterio.transform import from_bounds as transform_from_bounds
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Tuple, Union, Optional, Any


def load_and_explore_raster(raster_path: str) -> Dict[str, Any]:
    """
    Load a raster file and extract comprehensive metadata and properties.

    This function opens a raster file safely and extracts key information
    including dimensions, coordinate system, spatial extent, and data types.

    Args:
        raster_path (str): Path to the raster file (e.g., 'data/elevation_dem.tif')

    Returns:
        Dict[str, Any]: Dictionary containing raster properties and metadata

    Example return format:
        {
            'filename': 'elevation_dem.tif',
            'width': 1024,
            'height': 768,
            'count': 1,
            'dtype': 'float32',
            'crs': 'EPSG:4326',
            'nodata': -9999.0,
            'bounds': {
                'left': -120.5,
                'bottom': 35.0,
                'right': -119.5,
                'top': 36.0
            },
            'pixel_size_x': 0.001,
            'pixel_size_y': 0.001,
            'extent_width': 1.0,
            'extent_height': 1.0
        }
    """

    # TODO: Import necessary libraries at top of file (already done above)

    # TODO: Check if the file exists
    # HINT: Use Path(raster_path).exists()

    # TODO: Open the raster file safely using a context manager
    # HINT: Use 'with rasterio.open(raster_path) as src:'

    # TODO: Extract basic metadata
    # HINT: src.width, src.height, src.count, src.dtype, src.crs, src.nodata

    # TODO: Get spatial extent information
    # HINT: src.bounds gives you left, bottom, right, top coordinates

    # TODO: Calculate pixel size from the transform
    # HINT: src.transform.a for X pixel size, abs(src.transform.e) for Y pixel size

    # TODO: Calculate extent dimensions in coordinate units
    # HINT: width = right - left, height = top - bottom

    # TODO: Print a clear summary for the user
    # HINT: Include dimensions, extent, CRS, and data type information

    # TODO: Create and return a dictionary with all the metadata
    # HINT: Organize into logical groups - basic info, spatial properties

    # TODO: Handle errors appropriately
    # HINT: FileNotFoundError, rasterio.RasterioIOError, general Exception

    pass  # Replace this with your implementation


def calculate_raster_statistics(raster_path: str, band_number: int = 1) -> Dict[str, Any]:
    """
    Calculate comprehensive statistics for a specific raster band.

    This function reads a raster band, properly handles NoData values,
    and calculates essential statistics including percentiles and counts.

    Args:
        raster_path (str): Path to the raster file
        band_number (int): Which band to analyze (1-based indexing, default=1)

    Returns:
        Dict[str, Any]: Dictionary containing comprehensive statistics

    Example return format:
        {
            'band_number': 1,
            'filename': 'elevation_dem.tif',
            'min': 1247.5,
            'max': 4421.2,
            'mean': 2834.8,
            'std': 623.1,
            'median': 2798.0,
            'percentile_25': 2401.0,
            'percentile_75': 3267.5,
            'total_pixels': 786432,
            'valid_pixels': 786432,
            'nodata_pixels': 0,
            'valid_percentage': 100.0,
            'nodata_value': -9999.0,
            'data_type': 'float32'
        }
    """

    # TODO: Validate inputs
    # HINT: Check if file exists, band_number is positive integer

    # TODO: Open the raster file safely
    # HINT: Use context manager 'with rasterio.open(raster_path) as src:'

    # TODO: Validate that the requested band exists
    # HINT: Compare band_number with src.count

    # TODO: Read the specified band data as numpy array
    # HINT: Use src.read(band_number) - note 1-based indexing

    # TODO: Get the NoData value for this raster
    # HINT: Use src.nodata

    # TODO: Handle NoData values by creating a mask
    # HINT: If nodata exists, create boolean mask: valid_data = band_data[band_data != nodata]

    # TODO: Check if any valid data exists (handle case of all NoData)
    # HINT: if len(valid_data) == 0: return error info

    # TODO: Calculate basic statistics on valid data only
    # HINT: Use np.min(), np.max(), np.mean(), np.std() on valid_data

    # TODO: Calculate percentiles for distribution analysis
    # HINT: Use np.percentile(valid_data, [25, 50, 75])

    # TODO: Count pixels (total, valid, nodata)
    # HINT: total = band_data.size, valid = len(valid_data), nodata = total - valid

    # TODO: Print clear summary of statistics for user
    # HINT: Format nicely with value ranges, percentages, pixel counts

    # TODO: Create and return dictionary with all statistics
    # HINT: Include all calculated values plus metadata

    # TODO: Handle all errors gracefully
    # HINT: FileNotFoundError, IndexError (invalid band), RasterioIOError

    pass  # Replace this with your implementation


def extract_raster_subset(raster_path: str, window_bounds: Tuple[float, float, float, float],
                         output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract a spatial subset from a raster using windowed reading.

    This function defines a geographic window, converts it to pixel coordinates,
    reads only the needed portion (memory efficient), and optionally saves the subset.

    Args:
        raster_path (str): Path to input raster file
        window_bounds (tuple): Geographic bounds as (left, bottom, right, top)
        output_path (str, optional): Path to save subset file (if desired)

    Returns:
        Dict[str, Any]: Dictionary with subset data and metadata

    Example return format:
        {
            'subset_array': numpy.ndarray,
            'original_shape': (768, 1024),
            'subset_shape': (300, 400),
            'window_bounds': (-120.2, 35.3, -119.8, 35.7),
            'pixel_window': Window(200, 150, 400, 300),
            'subset_transform': Affine(...),
            'crs': 'EPSG:4326',
            'memory_saved_percent': 67.5,
            'output_file': 'path/to/subset.tif' or None
        }
    """

    # TODO: Validate inputs
    # HINT: Check file exists, window_bounds has 4 values, bounds are valid

    # TODO: Open the raster file safely
    # HINT: Use context manager

    # TODO: Validate that window_bounds are within raster extent
    # HINT: Compare with src.bounds

    # TODO: Convert geographic bounds to pixel window
    # HINT: Use rasterio.windows.from_bounds(left, bottom, right, top, transform=src.transform)

    # TODO: Validate that the window is valid (positive dimensions)
    # HINT: Check window.width > 0 and window.height > 0

    # TODO: Read the subset data using windowed reading
    # HINT: Use src.read(1, window=window) for memory efficiency

    # TODO: Calculate the spatial transform for the subset
    # HINT: Use src.window_transform(window)

    # TODO: Calculate memory savings
    # HINT: Compare subset size to full raster size

    # TODO: If output_path provided, save the subset to new file
    # HINT: Create new profile with updated dimensions and transform
    # HINT: Use rasterio.open(output_path, 'w', **profile) to write

    # TODO: Print summary of extraction results
    # HINT: Show original vs subset dimensions, memory savings, output location

    # TODO: Create and return results dictionary
    # HINT: Include array, metadata, window info, and savings calculations

    # TODO: Handle errors appropriately
    # HINT: Invalid bounds, file writing errors, memory issues

    pass  # Replace this with your implementation


def visualize_raster_data(raster_path: str, band_number: int = 1,
                         output_path: Optional[str] = None) -> plt.Figure:
    """
    Create a professional visualization of raster data.

    This function loads raster data, handles NoData appropriately, chooses
    suitable colormaps, and creates publication-quality plots with proper
    labeling and geographic context.

    Args:
        raster_path (str): Path to raster file
        band_number (int): Which band to visualize (1-based indexing, default=1)
        output_path (str, optional): Path to save plot image (if desired)

    Returns:
        matplotlib.figure.Figure: The created figure object

    Example usage:
        fig = visualize_raster_data('data/elevation_dem.tif')
        fig.show()  # Display the plot

        # Or save directly:
        visualize_raster_data('data/elevation_dem.tif', output_path='elevation_map.png')
    """

    # TODO: Validate inputs
    # HINT: Check file exists, band_number is valid

    # TODO: Open the raster file safely
    # HINT: Use context manager

    # TODO: Validate that requested band exists
    # HINT: Check band_number <= src.count

    # TODO: Read the band data
    # HINT: Use src.read(band_number)

    # TODO: Handle NoData values for visualization
    # HINT: Use np.ma.masked_equal(band_data, src.nodata) if nodata exists

    # TODO: Choose appropriate colormap based on data type
    # HINT: 'terrain' for elevation, 'coolwarm' for temperature, 'viridis' for general
    # HINT: Check filename for clues: 'elevation', 'temp', 'ndvi', etc.

    # TODO: Create figure with good size
    # HINT: Use plt.subplots(figsize=(10, 8))

    # TODO: Create the main plot with geographic extent
    # HINT: Use ax.imshow() with extent=[left, right, bottom, top]

    # TODO: Add colorbar with appropriate label
    # HINT: Use plt.colorbar() and set label based on data type

    # TODO: Set informative title
    # HINT: Include filename and band number if multi-band

    # TODO: Add axis labels (Longitude, Latitude)
    # HINT: Use ax.set_xlabel() and ax.set_ylabel()

    # TODO: Add grid for reference
    # HINT: Use ax.grid(True, alpha=0.3)

    # TODO: Add coordinate system info as text
    # HINT: Use ax.text() to show CRS in corner

    # TODO: Add data summary statistics as text
    # HINT: Calculate and display min, max, mean, pixel count

    # TODO: If output_path provided, save the plot
    # HINT: Use plt.savefig() with high DPI for quality

    # TODO: Print summary of visualization created
    # HINT: Show data range, colormap used, output location

    # TODO: Return the figure object
    # HINT: Return fig for further customization

    # TODO: Handle errors appropriately
    # HINT: Invalid band, plotting errors, file save errors

    pass  # Replace this with your implementation


# Bonus helper functions (optional, but useful for testing)

def print_raster_summary(raster_path: str) -> None:
    """
    Print a comprehensive summary of a raster file.

    This function combines information from load_and_explore_raster() and
    calculate_raster_statistics() to provide a complete overview.
    You can implement this as practice!
    """
    # TODO: Use your other functions to create a complete summary
    # HINT: Call load_and_explore_raster() and calculate_raster_statistics()
    # HINT: Format output nicely for easy reading
    pass


def compare_rasters(raster_path1: str, raster_path2: str) -> None:
    """
    Compare two raster files side by side.

    Advanced function for comparing dimensions, extents, and data ranges.
    Good practice for understanding raster properties!
    """
    # TODO: Load both rasters and compare properties
    # HINT: Use your load_and_explore_raster() function
    # HINT: Compare dimensions, extents, CRS, data types
    pass


# Example usage and testing (you can run this to test your functions)
if __name__ == "__main__":
    # Test with sample data (uncomment when your functions are implemented)

    # sample_raster = "data/elevation_dem.tif"

    # Test function 1
    # print("Testing load_and_explore_raster()...")
    # metadata = load_and_explore_raster(sample_raster)

    # Test function 2
    # print("\nTesting calculate_raster_statistics()...")
    # stats = calculate_raster_statistics(sample_raster)

    # Test function 3
    # print("\nTesting extract_raster_subset()...")
    # bounds = (-120.2, 35.3, -119.8, 35.7)  # Adjust for your data
    # subset = extract_raster_subset(sample_raster, bounds)

    # Test function 4
    # print("\nTesting visualize_raster_data()...")
    # fig = visualize_raster_data(sample_raster)
    # fig.show()

    print("🎯 Implementation template ready!")
    print("📝 Replace each 'pass' statement with your working code.")
    print("🧪 Test each function with: uv run pytest tests/test_rasterio_basics.py::test_function_name -v")
