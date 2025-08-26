"""
Applications - Part 3 of Python Rasterio Assignment

This module contains practical applications of raster analysis that GIS
professionals commonly use in their work. Each function demonstrates
real-world use cases with detailed step-by-step instructions.

Author: [Your Name]
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio - Working with Raster Data
"""

# Import the libraries we need
import rasterio
from rasterio.windows import from_bounds
from rasterio.transform import rowcol
import numpy as np
from pathlib import Path
from typing import Dict, List, Union, Any, Tuple
import json

# Import our other modules to reuse functions
from .raster_basics import read_raster_info, get_raster_stats, get_raster_extent
from .band_math import calculate_ndvi


def sample_raster_at_points(raster_path: str, points_list: List[Tuple[float, float]]) -> Dict[str, Any]:
    """
    Extract raster values at specific coordinate locations.

    This is one of the most common GIS operations - you have point locations
    (like weather stations, sample sites, or GPS coordinates) and you want to
    know what the raster values are at those locations.

    For example:
    - What's the elevation at each weather station?
    - What's the temperature at each sample site?
    - What's the land cover type at each GPS point?

    Args:
        raster_path (str): Path to the raster file
        points_list (List[Tuple[float, float]]): List of (x, y) coordinate pairs
            Example: [(-120.5, 35.2), (-120.3, 35.4), (-120.1, 35.6)]

    Returns:
        Dict[str, Any]: Dictionary containing point values and metadata

    Example return format:
        {
            'point_values': [245.6, 312.8, 289.1],  # Raster values at each point
            'coordinates': [(-120.5, 35.2), (-120.3, 35.4), (-120.1, 35.6)],
            'points_inside_raster': 3,
            'points_outside_raster': 0,
            'raster_crs': 'EPSG:4326',
            'total_points': 3
        }
    """
    # STEP 1: Open the raster file and get its properties
    with rasterio.open(raster_path) as src:

        # Get raster properties we'll need
        raster_bounds = src.bounds
        raster_transform = src.transform
        raster_crs = str(src.crs)

        # STEP 2: Initialize lists to store results
        point_values = []
        points_inside = 0
        points_outside = 0

        # STEP 3: Loop through each point and extract the raster value
        for i, (x, y) in enumerate(points_list):

            # STEP 3a: Check if the point is within the raster bounds
            # TODO: Check if x and y are within the raster extent
            # HINT: Compare with raster_bounds.left, right, bottom, top

            if (raster_bounds.left <= x <= raster_bounds.right and
                raster_bounds.bottom <= y <= raster_bounds.top):

                # Point is inside the raster
                points_inside += 1

                # STEP 3b: Convert geographic coordinates to pixel coordinates
                # HINT: Use rowcol() function to convert x,y to row,col
                try:
                    row, col = rowcol(raster_transform, x, y)

                    # STEP 3c: Make sure the pixel coordinates are valid
                    # Check if row and col are within the raster dimensions
                    if (0 <= row < src.height and 0 <= col < src.width):

                        # STEP 3d: Read the pixel value
                        # TODO: Read the value at the specific pixel location
                        # HINT: Use src.read(1, window=Window(col, row, 1, 1)) for one pixel
                        # Or use array indexing after reading the whole band

                        # Method 1: Read just one pixel (more efficient for few points)
                        from rasterio.windows import Window
                        window = Window(col, row, 1, 1)
                        pixel_value = src.read(1, window=window)[0, 0]

                        # Handle nodata values
                        if src.nodata is not None and pixel_value == src.nodata:
                            point_values.append(None)  # No data at this location
                        else:
                            point_values.append(float(pixel_value))

                    else:
                        # Pixel coordinates are outside raster dimensions
                        point_values.append(None)
                        points_outside += 1

                except Exception as e:
                    # Error in coordinate conversion
                    point_values.append(None)
                    points_outside += 1

            else:
                # Point is outside the raster bounds
                points_outside += 1
                point_values.append(None)

        # STEP 4: Create the results dictionary
        results = {
            'point_values': point_values,
            'coordinates': points_list,
            'points_inside_raster': points_inside,
            'points_outside_raster': points_outside,
            'raster_crs': raster_crs,
            'total_points': len(points_list),
            'raster_bounds': {
                'left': float(raster_bounds.left),
                'bottom': float(raster_bounds.bottom),
                'right': float(raster_bounds.right),
                'top': float(raster_bounds.top)
            }
        }

        # STEP 5: Return the results
        return results


def read_remote_raster(url: str, bbox: Tuple[float, float, float, float] = None) -> Dict[str, Any]:
    """
    Read a raster from a remote URL (like a Cloud-Optimized GeoTIFF).

    This demonstrates how to work with remote raster data without downloading
    the entire file first. This is very useful for working with large datasets
    stored in the cloud (like satellite imagery or global climate data).

    Cloud-Optimized GeoTIFFs (COGs) are specially formatted to allow efficient
    reading of small portions from remote locations.

    Args:
        url (str): URL to the remote raster file
        bbox (Tuple[float, float, float, float], optional): Bounding box to read
            Format: (left, bottom, right, top) in the raster's coordinate system

    Returns:
        Dict[str, Any]: Dictionary containing raster data and metadata

    Example return format:
        {
            'data_array': numpy_array,  # The actual raster data
            'width': 512,
            'height': 384,
            'crs': 'EPSG:4326',
            'transform': Affine(...),
            'bounds': {...},
            'data_type': 'float32',
            'url': 'https://...'
        }
    """
    # STEP 1: Try to open the remote raster
    # HINT: rasterio.open() works with URLs just like local files!
    try:
        with rasterio.open(url) as src:

            # STEP 2: Get basic information about the remote raster
            raster_info = {
                'width': src.width,
                'height': src.height,
                'count': src.count,
                'crs': str(src.crs),
                'bounds': {
                    'left': src.bounds.left,
                    'bottom': src.bounds.bottom,
                    'right': src.bounds.right,
                    'top': src.bounds.top
                },
                'data_type': str(src.dtypes[0]),
                'transform': src.transform,
                'url': url
            }

            # STEP 3: Read the data (either full raster or clipped to bbox)
            if bbox is not None:
                # STEP 3a: Read only the area within the bounding box
                # TODO: Use windowed reading to get just the area we want
                # HINT: Use from_bounds() to create a window, then src.read() with that window

                left, bottom, right, top = bbox

                # Create a window for the bounding box
                try:
                    window = from_bounds(left, bottom, right, top, src.transform)

                    # Read the data within the window
                    data = src.read(1, window=window)  # Read first band

                    # Update the transform for the windowed data
                    windowed_transform = src.window_transform(window)

                    raster_info.update({
                        'data_array': data,
                        'windowed': True,
                        'requested_bbox': bbox,
                        'actual_width': data.shape[1],
                        'actual_height': data.shape[0],
                        'windowed_transform': windowed_transform
                    })

                except Exception as e:
                    # If windowed reading fails, read the full raster
                    print(f"Warning: Could not read windowed data ({e}), reading full raster")
                    data = src.read(1)
                    raster_info.update({
                        'data_array': data,
                        'windowed': False,
                        'warning': f"Windowed reading failed: {e}"
                    })

            else:
                # STEP 3b: Read the entire raster
                # TODO: Read all the data from the first band
                # HINT: Use src.read(1) to read the first band

                data = src.read(1)  # Read first band
                raster_info.update({
                    'data_array': data,
                    'windowed': False
                })

            # STEP 4: Add some basic statistics about the data
            valid_data = data[~np.isnan(data)] if src.nodata else data
            if len(valid_data) > 0:
                raster_info.update({
                    'min_value': float(np.min(valid_data)),
                    'max_value': float(np.max(valid_data)),
                    'mean_value': float(np.mean(valid_data)),
                    'valid_pixels': len(valid_data),
                    'total_pixels': data.size
                })

            return raster_info

    except Exception as e:
        # STEP 5: Handle errors gracefully
        return {
            'error': str(e),
            'url': url,
            'success': False,
            'message': f"Could not read remote raster: {e}"
        }


def create_raster_summary(raster_path: str) -> Dict[str, Any]:
    """
    Create a comprehensive summary of a raster dataset.

    This function combines information from all our other functions to create
    a complete overview of a raster file. This is useful for quickly understanding
    what's in a raster dataset before doing detailed analysis.

    Args:
        raster_path (str): Path to the raster file (local or remote URL)

    Returns:
        Dict[str, Any]: Comprehensive summary of the raster

    Example return format:
        {
            'file_info': {...},      # From read_raster_info()
            'statistics': {...},     # From get_raster_stats()
            'extent': {...},         # From get_raster_extent()
            'ndvi_analysis': {...},  # From calculate_ndvi() if multi-band
            'summary': {             # High-level summary
                'file_size_mb': 15.2,
                'pixel_size_meters': 30.0,
                'is_multiband': True,
                'has_ndvi_capability': True,
                'data_quality': 'Good'
            }
        }
    """
    # STEP 1: Initialize the summary dictionary
    summary = {
        'raster_path': raster_path,
        'analysis_date': str(pd.Timestamp.now().date()) if 'pd' in globals() else 'Unknown'
    }

    try:
        # STEP 2: Get basic file information
        # TODO: Use your read_raster_info() function
        # HINT: You already wrote this function in raster_basics.py!

        file_info = read_raster_info(raster_path)
        summary['file_info'] = file_info

        # STEP 3: Get basic statistics for the first band
        # TODO: Use your get_raster_stats() function
        statistics = get_raster_stats(raster_path, band_number=1)
        summary['statistics'] = statistics

        # STEP 4: Get the geographic extent
        # TODO: Use your get_raster_extent() function
        extent = get_raster_extent(raster_path)
        summary['extent'] = extent

        # STEP 5: Try to calculate NDVI if this is a multi-band image
        if file_info['count'] >= 4:  # Need at least 4 bands for typical NDVI
            try:
                # TODO: Use your calculate_ndvi() function
                # HINT: Assume red=3, NIR=4 for Landsat-style imagery
                ndvi_results = calculate_ndvi(raster_path, red_band=3, nir_band=4)
                summary['ndvi_analysis'] = {
                    'min_ndvi': ndvi_results['min_ndvi'],
                    'max_ndvi': ndvi_results['max_ndvi'],
                    'mean_ndvi': ndvi_results['mean_ndvi'],
                    'vegetation_pixels': ndvi_results['vegetation_pixels'],
                    'vegetation_percentage': round(
                        (ndvi_results['vegetation_pixels'] / ndvi_results['total_pixels']) * 100, 1
                    ) if ndvi_results['total_pixels'] > 0 else 0
                }
                has_ndvi = True
            except Exception as e:
                summary['ndvi_analysis'] = {'error': str(e)}
                has_ndvi = False
        else:
            summary['ndvi_analysis'] = {'note': 'Insufficient bands for NDVI calculation'}
            has_ndvi = False

        # STEP 6: Create a high-level summary
        # TODO: Calculate some useful summary statistics

        # Estimate pixel size in meters (rough approximation)
        if 'EPSG:4326' in str(file_info['crs']):
            # Geographic coordinates - rough conversion to meters at equator
            pixel_size_degrees = extent['width'] / file_info['width']
            pixel_size_meters = pixel_size_degrees * 111320  # meters per degree at equator
        else:
            pixel_size_meters = None  # Unknown for projected coordinates

        # Estimate file size (very rough)
        total_pixels = file_info['width'] * file_info['height'] * file_info['count']
        estimated_size_mb = (total_pixels * 4) / (1024 * 1024)  # Assume 4 bytes per pixel

        # Assess data quality
        if statistics['nodata_count'] == 0:
            data_quality = 'Excellent'
        elif statistics['nodata_count'] < (file_info['width'] * file_info['height'] * 0.05):
            data_quality = 'Good'
        elif statistics['nodata_count'] < (file_info['width'] * file_info['height'] * 0.20):
            data_quality = 'Fair'
        else:
            data_quality = 'Poor - many missing values'

        summary['summary'] = {
            'total_pixels': total_pixels,
            'estimated_size_mb': round(estimated_size_mb, 1),
            'pixel_size_meters': round(pixel_size_meters, 1) if pixel_size_meters else None,
            'is_multiband': file_info['count'] > 1,
            'has_ndvi_capability': has_ndvi,
            'data_quality': data_quality,
            'coverage_area_km2': round((extent['width'] * extent['height']) / 1000000, 1) if pixel_size_meters else None
        }

        # STEP 7: Return the complete summary
        return summary

    except Exception as e:
        # Handle any errors
        return {
            'raster_path': raster_path,
            'error': str(e),
            'success': False,
            'message': f"Could not create raster summary: {e}"
        }


# BONUS: Helper function to print the summary in a nice format
def print_raster_summary_report(summary: Dict[str, Any]):
    """
    Print a nicely formatted raster summary report.

    This is a bonus function that makes the summary easier to read.
    You don't need to modify this!
    """
    print("\n" + "="*60)
    print("         COMPREHENSIVE RASTER ANALYSIS REPORT")
    print("="*60)

    print(f"\nFile: {Path(summary['raster_path']).name}")
    print(f"Path: {summary['raster_path']}")

    if 'file_info' in summary:
        info = summary['file_info']
        print(f"\nBASIC INFORMATION:")
        print(f"  Dimensions: {info['width']} × {info['height']} pixels")
        print(f"  Bands: {info['count']}")
        print(f"  Format: {info['driver']}")
        print(f"  Coordinate System: {info['crs']}")

    if 'extent' in summary:
        extent = summary['extent']
        print(f"\nGEOGRAPHIC EXTENT:")
        print(f"  Left: {extent['left']:.6f}")
        print(f"  Right: {extent['right']:.6f}")
        print(f"  Bottom: {extent['bottom']:.6f}")
        print(f"  Top: {extent['top']:.6f}")

    if 'statistics' in summary:
        stats = summary['statistics']
        print(f"\nDATA STATISTICS (Band 1):")
        print(f"  Range: {stats['min']:.2f} to {stats['max']:.2f}")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Standard Deviation: {stats['std']:.2f}")
        print(f"  Missing pixels: {stats['nodata_count']:,}")

    if 'ndvi_analysis' in summary and 'min_ndvi' in summary['ndvi_analysis']:
        ndvi = summary['ndvi_analysis']
        print(f"\nVEGETATION ANALYSIS (NDVI):")
        print(f"  NDVI Range: {ndvi['min_ndvi']:.3f} to {ndvi['max_ndvi']:.3f}")
        print(f"  Mean NDVI: {ndvi['mean_ndvi']:.3f}")
        print(f"  Vegetation Coverage: {ndvi['vegetation_percentage']}%")

    if 'summary' in summary:
        sum_info = summary['summary']
        print(f"\nSUMMARY:")
        print(f"  Total Pixels: {sum_info['total_pixels']:,}")
        print(f"  Estimated File Size: {sum_info['estimated_size_mb']} MB")
        print(f"  Multi-band: {'Yes' if sum_info['is_multiband'] else 'No'}")
        print(f"  NDVI Capable: {'Yes' if sum_info['has_ndvi_capability'] else 'No'}")
        print(f"  Data Quality: {sum_info['data_quality']}")

        if sum_info['pixel_size_meters']:
            print(f"  Pixel Size: ~{sum_info['pixel_size_meters']} meters")
        if sum_info['coverage_area_km2']:
            print(f"  Coverage Area: ~{sum_info['coverage_area_km2']} km²")

    print("\n" + "="*60)


# Example usage (you can run this to test your functions):
if __name__ == "__main__":
    # Test with sample data (you'll need to provide real paths)

    # Example 1: Sample raster at points
    # sample_points = [(-120.5, 35.2), (-120.3, 35.4), (-120.1, 35.6)]
    # point_results = sample_raster_at_points("data/sample_elevation.tif", sample_points)
    # print("Point sampling results:", point_results)

    # Example 2: Read remote raster
    # cog_url = "https://example.com/sample_data.tif"
    # bbox = (-121.0, 35.0, -120.0, 36.0)  # Small area
    # remote_results = read_remote_raster(cog_url, bbox)
    # print("Remote raster results:", remote_results)

    # Example 3: Create comprehensive summary
    # summary = create_raster_summary("data/sample_landsat.tif")
    # print_raster_summary_report(summary)

    pass
