#!/usr/bin/env python3
"""
Simple Test Runner for Your Rasterio Functions

This script helps you test your functions as you implement them.
Run it with: python test_my_functions.py

It will create sample data and test each of your functions,
giving you clear feedback about what's working and what needs fixing.

Author: Instructor
Course: GIST 604B - Open Source GIS Programming
"""

import os
import sys
import tempfile
import numpy as np
import rasterio
from pathlib import Path

def create_sample_data():
    """Create sample raster files for testing."""
    print("🔧 Creating sample test data...")

    temp_dir = tempfile.mkdtemp()

    # Create simple single-band raster (elevation)
    elevation_path = Path(temp_dir) / "test_elevation.tif"
    elevation_data = np.random.randint(1000, 2000, (10, 10), dtype=np.int16)
    elevation_data[0, 0] = -9999  # Add a nodata value

    with rasterio.open(
        elevation_path, 'w',
        driver='GTiff', height=10, width=10, count=1,
        dtype=elevation_data.dtype, crs='EPSG:4326',
        transform=rasterio.transform.from_bounds(-120, 35, -119, 36, 10, 10),
        nodata=-9999
    ) as dst:
        dst.write(elevation_data, 1)

    # Create multi-band raster (satellite imagery)
    satellite_path = Path(temp_dir) / "test_satellite.tif"
    blue = np.random.randint(30, 100, (8, 8), dtype=np.uint16)
    green = np.random.randint(40, 120, (8, 8), dtype=np.uint16)
    red = np.random.randint(50, 150, (8, 8), dtype=np.uint16)
    nir = np.random.randint(100, 300, (8, 8), dtype=np.uint16)

    all_bands = np.stack([blue, green, red, nir])

    with rasterio.open(
        satellite_path, 'w',
        driver='GTiff', height=8, width=8, count=4,
        dtype=all_bands.dtype, crs='EPSG:4326',
        transform=rasterio.transform.from_bounds(-120.5, 35.2, -120.0, 35.7, 8, 8)
    ) as dst:
        for band_num in range(4):
            dst.write(all_bands[band_num], band_num + 1)

    print(f"✅ Created test elevation raster: {elevation_path.name}")
    print(f"✅ Created test satellite raster: {satellite_path.name}")

    return str(elevation_path), str(satellite_path)

def test_function_import(module_name, function_names):
    """Test if functions can be imported."""
    print(f"\n📦 Testing imports from {module_name}...")

    imported_functions = {}

    for func_name in function_names:
        try:
            module = __import__(f"src.rasterio_analysis.{module_name}", fromlist=[func_name])
            func = getattr(module, func_name)
            imported_functions[func_name] = func
            print(f"  ✅ {func_name}() imported successfully")
        except ImportError as e:
            print(f"  ❌ Could not import {func_name}(): {e}")
            print(f"     💡 Make sure you've created src/rasterio_analysis/{module_name}.py")
        except AttributeError as e:
            print(f"  ❌ {func_name}() not found in module: {e}")
            print(f"     💡 Make sure you've defined the function in {module_name}.py")
        except Exception as e:
            print(f"  ❌ Error importing {func_name}(): {e}")

    return imported_functions

def test_raster_basics(functions, elevation_path):
    """Test the raster basics functions."""
    print(f"\n🗺️  Testing Part 1: Raster Basics Functions")
    print("=" * 50)

    # Test read_raster_info
    if 'read_raster_info' in functions:
        print("\n🔍 Testing read_raster_info()...")
        try:
            result = functions['read_raster_info'](elevation_path)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_keys = ['width', 'height', 'count', 'crs', 'driver']
                missing_keys = [key for key in expected_keys if key not in result]

                if not missing_keys:
                    print("  ✅ Has all required keys")
                    if result['width'] == 10 and result['height'] == 10:
                        print("  ✅ Correct dimensions")
                    else:
                        print(f"  ⚠️  Dimensions: {result['width']}x{result['height']} (expected 10x10)")
                else:
                    print(f"  ❌ Missing keys: {missing_keys}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your function implementation")

    # Test get_raster_stats
    if 'get_raster_stats' in functions:
        print("\n📊 Testing get_raster_stats()...")
        try:
            result = functions['get_raster_stats'](elevation_path)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_keys = ['min', 'max', 'mean', 'std', 'nodata_count']
                missing_keys = [key for key in expected_keys if key not in result]

                if not missing_keys:
                    print("  ✅ Has all required keys")
                    if result['min'] < result['max']:
                        print("  ✅ Min < Max (logical)")
                    if result['nodata_count'] >= 1:
                        print("  ✅ Detected nodata values")
                    else:
                        print("  ⚠️  No nodata detected (expected at least 1)")
                else:
                    print(f"  ❌ Missing keys: {missing_keys}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your function implementation")

    # Test get_raster_extent
    if 'get_raster_extent' in functions:
        print("\n🌐 Testing get_raster_extent()...")
        try:
            result = functions['get_raster_extent'](elevation_path)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_keys = ['left', 'bottom', 'right', 'top', 'width', 'height']
                missing_keys = [key for key in expected_keys if key not in result]

                if not missing_keys:
                    print("  ✅ Has all required keys")
                    if result['left'] < result['right'] and result['bottom'] < result['top']:
                        print("  ✅ Logical extent (left<right, bottom<top)")
                    if abs(result['width'] - 1.0) < 0.01:
                        print("  ✅ Correct width calculation")
                    else:
                        print(f"  ⚠️  Width: {result['width']} (expected ~1.0)")
                else:
                    print(f"  ❌ Missing keys: {missing_keys}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your function implementation")

def test_band_math(functions, satellite_path):
    """Test the band math functions."""
    print(f"\n🌱 Testing Part 2: Band Math Functions")
    print("=" * 50)

    # Test calculate_ndvi
    if 'calculate_ndvi' in functions:
        print("\n📈 Testing calculate_ndvi()...")
        try:
            result = functions['calculate_ndvi'](satellite_path, red_band=3, nir_band=4)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_keys = ['ndvi_array', 'min_ndvi', 'max_ndvi', 'mean_ndvi']
                missing_keys = [key for key in expected_keys if key not in result]

                if not missing_keys:
                    print("  ✅ Has required keys")

                    if 'ndvi_array' in result:
                        ndvi_array = result['ndvi_array']
                        if isinstance(ndvi_array, np.ndarray):
                            print("  ✅ NDVI array is numpy array")
                            if ndvi_array.shape == (8, 8):
                                print("  ✅ Correct array dimensions")
                        else:
                            print(f"  ❌ NDVI array should be numpy array, got {type(ndvi_array)}")

                    if all(k in result for k in ['min_ndvi', 'max_ndvi', 'mean_ndvi']):
                        if -1 <= result['min_ndvi'] <= 1 and -1 <= result['max_ndvi'] <= 1:
                            print("  ✅ NDVI values in valid range (-1 to 1)")
                        else:
                            print(f"  ⚠️  NDVI values outside expected range: {result['min_ndvi']:.3f} to {result['max_ndvi']:.3f}")
                else:
                    print(f"  ❌ Missing keys: {missing_keys}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your NDVI calculation and error handling")

    # Test analyze_vegetation
    if 'analyze_vegetation' in functions:
        print("\n🌿 Testing analyze_vegetation()...")
        try:
            # First create some sample NDVI data
            sample_ndvi = np.array([
                [0.8, 0.7, 0.3, 0.1],
                [0.6, 0.5, 0.2, -0.1],
                [0.4, 0.3, 0.15, 0.05],
                [0.2, 0.1, 0.0, np.nan]
            ], dtype=np.float32)

            result = functions['analyze_vegetation'](sample_ndvi)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_categories = ['water_clouds', 'non_vegetation', 'sparse_vegetation',
                                     'moderate_vegetation', 'dense_vegetation']

                missing_categories = [cat for cat in expected_categories if cat not in result]

                if not missing_categories:
                    print("  ✅ Has all vegetation categories")

                    # Check that each category has pixels and percent
                    all_good = True
                    for cat in expected_categories:
                        if not (isinstance(result[cat], dict) and 'pixels' in result[cat] and 'percent' in result[cat]):
                            all_good = False
                            break

                    if all_good:
                        print("  ✅ Each category has 'pixels' and 'percent' keys")
                    else:
                        print("  ❌ Categories should have 'pixels' and 'percent' keys")

                else:
                    print(f"  ❌ Missing categories: {missing_categories}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your vegetation classification logic")

def test_applications(functions, elevation_path):
    """Test the applications functions."""
    print(f"\n🎯 Testing Part 3: Applications Functions")
    print("=" * 50)

    # Test sample_raster_at_points
    if 'sample_raster_at_points' in functions:
        print("\n📍 Testing sample_raster_at_points()...")
        try:
            # Test points (some inside, some outside the raster extent)
            test_points = [
                (-119.5, 35.5),  # Should be inside
                (-119.2, 35.8),  # Should be inside
                (-121.0, 35.0),  # Should be outside
            ]

            result = functions['sample_raster_at_points'](elevation_path, test_points)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                expected_keys = ['point_values', 'coordinates', 'points_inside_raster',
                               'points_outside_raster', 'total_points']
                missing_keys = [key for key in expected_keys if key not in result]

                if not missing_keys:
                    print("  ✅ Has all required keys")

                    if len(result['point_values']) == len(test_points):
                        print("  ✅ Correct number of point values")

                    if result['total_points'] == len(test_points):
                        print("  ✅ Correct total point count")

                    if result['points_inside_raster'] + result['points_outside_raster'] == result['total_points']:
                        print("  ✅ Inside + outside = total points")

                else:
                    print(f"  ❌ Missing keys: {missing_keys}")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check your coordinate handling and boundary detection")

    # Test create_raster_summary
    if 'create_raster_summary' in functions:
        print("\n📋 Testing create_raster_summary()...")
        try:
            result = functions['create_raster_summary'](elevation_path)

            if isinstance(result, dict):
                print("  ✅ Returns a dictionary")

                if 'raster_path' in result and result['raster_path'] == elevation_path:
                    print("  ✅ Includes correct raster path")

                # Check for main sections
                sections = ['file_info', 'statistics', 'extent']
                found_sections = [s for s in sections if s in result]

                if found_sections:
                    print(f"  ✅ Found summary sections: {found_sections}")
                else:
                    print("  ⚠️  No main sections found (file_info, statistics, extent)")

            else:
                print(f"  ❌ Should return a dict, got {type(result)}")

        except Exception as e:
            print(f"  ❌ Error running function: {e}")
            print("     💡 Check that you're calling your other functions correctly")

def main():
    """Main test runner."""
    print("🧪 RASTERIO ASSIGNMENT TEST RUNNER")
    print("=" * 60)
    print("This script will test your functions as you implement them.")
    print("Don't worry if some tests fail at first - that's normal!")
    print("Implement each function step by step and re-run this script.")

    # Create sample data
    try:
        elevation_path, satellite_path = create_sample_data()
    except Exception as e:
        print(f"❌ Could not create test data: {e}")
        return

    # Test Part 1: Raster Basics
    basic_functions = test_function_import('raster_basics',
                                         ['read_raster_info', 'get_raster_stats', 'get_raster_extent'])
    if basic_functions:
        test_raster_basics(basic_functions, elevation_path)

    # Test Part 2: Band Math
    math_functions = test_function_import('band_math',
                                        ['calculate_ndvi', 'analyze_vegetation'])
    if math_functions:
        test_band_math(math_functions, satellite_path)

    # Test Part 3: Applications
    app_functions = test_function_import('applications',
                                       ['sample_raster_at_points', 'create_raster_summary'])
    if app_functions:
        test_applications(app_functions, elevation_path)

    # Final summary
    print(f"\n🎉 TEST SUMMARY")
    print("=" * 60)
    print("If you see ✅ marks, those parts are working!")
    print("If you see ❌ marks, check the hints and fix those functions.")
    print("If you see ⚠️ marks, the function works but might need tweaking.")
    print("\nKeep working through the functions one by one.")
    print("Run this script again after making changes to see your progress!")
    print("\n💡 Need help? Check the README.md and function comments for guidance.")

if __name__ == "__main__":
    main()
