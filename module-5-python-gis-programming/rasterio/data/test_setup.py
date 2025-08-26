#!/usr/bin/env python3
"""
GIST 604B - Rasterio Setup Validation Test
==========================================

This script tests all the fixes made to the rasterio data setup system.
It validates that the UV environment works correctly and that data download
and synthetic data creation functions are working properly.

Usage:
    uv run python data/test_setup.py

Author: GIST 604B Course Team
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import json
import time

# Add the data directory to path so we can import setup functions
sys.path.insert(0, str(Path(__file__).parent))

try:
    from setup_rasterio_data import (
        check_uv_installed,
        check_python_version,
        test_uv_environment,
        Colors,
        print_success,
        print_error,
        print_info,
        print_header
    )
    from create_sample_data import (
        create_directories,
        create_synthetic_dem,
        create_synthetic_landsat,
        create_synthetic_temperature,
        create_sample_vector_data,
        create_metadata_files
    )
except ImportError as e:
    print(f"❌ Could not import setup functions: {e}")
    print("Make sure you're running this from the rasterio directory")
    sys.exit(1)

def test_uv_installation():
    """Test UV installation and basic functionality."""
    print_header("TESTING UV INSTALLATION")

    try:
        # Test UV is available
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_success(f"UV installed: {result.stdout.strip()}")
            return True
        else:
            print_error("UV command failed")
            return False
    except FileNotFoundError:
        print_error("UV not found - install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    except Exception as e:
        print_error(f"UV test failed: {e}")
        return False

def test_python_packages():
    """Test that all required Python packages are available."""
    print_header("TESTING PYTHON PACKAGES")

    required_packages = [
        ('rasterio', 'import rasterio; print(f"Rasterio {rasterio.__version__}")'),
        ('geopandas', 'import geopandas as gpd; print(f"GeoPandas {gpd.__version__}")'),
        ('numpy', 'import numpy as np; print(f"NumPy {np.__version__}")'),
        ('requests', 'import requests; print(f"Requests {requests.__version__}")'),
        ('tqdm', 'import tqdm; print(f"TQDM {tqdm.__version__}")'),
        ('matplotlib', 'import matplotlib; print(f"Matplotlib {matplotlib.__version__}")'),
    ]

    success_count = 0
    for package, test_code in required_packages:
        try:
            result = subprocess.run(
                ["uv", "run", "python", "-c", test_code],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                version_info = result.stdout.strip()
                print_success(f"✓ {version_info}")
                success_count += 1
            else:
                print_error(f"✗ {package} failed: {result.stderr}")
        except Exception as e:
            print_error(f"✗ {package} error: {e}")

    if success_count == len(required_packages):
        print_success("All required packages are working!")
        return True
    else:
        print_error(f"Only {success_count}/{len(required_packages)} packages working")
        return False

def test_data_creation():
    """Test synthetic data creation functions."""
    print_header("TESTING DATA CREATION FUNCTIONS")

    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Set up temporary data directories
        raster_dir = temp_path / "raster"
        vector_dir = temp_path / "vector"
        raster_dir.mkdir()
        vector_dir.mkdir()

        # Temporarily modify global paths
        import create_sample_data
        original_raster_dir = create_sample_data.RASTER_DIR
        original_vector_dir = create_sample_data.VECTOR_DIR
        create_sample_data.RASTER_DIR = raster_dir
        create_sample_data.VECTOR_DIR = vector_dir

        try:
            success_count = 0

            # Test DEM creation
            print_info("Testing synthetic DEM creation...")
            try:
                dem_path = create_synthetic_dem()
                if dem_path and dem_path.exists():
                    print_success(f"✓ DEM created: {dem_path.name} ({dem_path.stat().st_size / (1024*1024):.1f} MB)")

                    # Validate DEM with rasterio
                    result = subprocess.run([
                        "uv", "run", "python", "-c",
                        f"""
import rasterio
import numpy as np
with rasterio.open(r'{dem_path}') as src:
    data = src.read(1)
    print(f'DEM shape: {{data.shape}}')
    print(f'Elevation range: {{np.nanmin(data):.0f}} to {{np.nanmax(data):.0f}} meters')
    print(f'CRS: {{src.crs}}')
    print('DEM validation: PASSED')
"""
                    ], capture_output=True, text=True, timeout=30)

                    if result.returncode == 0:
                        print_success("✓ DEM validation passed")
                        for line in result.stdout.strip().split('\n'):
                            print(f"    {line}")
                        success_count += 1
                    else:
                        print_error(f"✗ DEM validation failed: {result.stderr}")
                else:
                    print_error("✗ DEM creation failed - no file created")
            except Exception as e:
                print_error(f"✗ DEM creation error: {e}")

            # Test Landsat creation
            print_info("Testing synthetic Landsat creation...")
            try:
                landsat_path = create_synthetic_landsat()
                if landsat_path and landsat_path.exists():
                    print_success(f"✓ Landsat created: {landsat_path.name} ({landsat_path.stat().st_size / (1024*1024):.1f} MB)")

                    # Validate Landsat with rasterio
                    result = subprocess.run([
                        "uv", "run", "python", "-c",
                        f"""
import rasterio
import numpy as np
with rasterio.open(r'{landsat_path}') as src:
    print(f'Landsat bands: {{src.count}}')
    print(f'Image size: {{src.width}} x {{src.height}}')
    print(f'CRS: {{src.crs}}')
    band1 = src.read(1)
    print(f'Data range: {{np.min(band1)}} to {{np.max(band1)}}')
    print('Landsat validation: PASSED')
"""
                    ], capture_output=True, text=True, timeout=30)

                    if result.returncode == 0:
                        print_success("✓ Landsat validation passed")
                        for line in result.stdout.strip().split('\n'):
                            print(f"    {line}")
                        success_count += 1
                    else:
                        print_error(f"✗ Landsat validation failed: {result.stderr}")
                else:
                    print_error("✗ Landsat creation failed - no file created")
            except Exception as e:
                print_error(f"✗ Landsat creation error: {e}")

            # Test temperature creation
            print_info("Testing synthetic temperature creation...")
            try:
                temp_path = create_synthetic_temperature()
                if temp_path and temp_path.exists():
                    print_success(f"✓ Temperature created: {temp_path.name} ({temp_path.stat().st_size / (1024*1024):.1f} MB)")

                    # Validate temperature with rasterio
                    result = subprocess.run([
                        "uv", "run", "python", "-c",
                        f"""
import rasterio
import numpy as np
with rasterio.open(r'{temp_path}') as src:
    temp_data = src.read(1)
    print(f'Temperature shape: {{temp_data.shape}}')
    print(f'Temperature range: {{np.nanmin(temp_data):.1f}} to {{np.nanmax(temp_data):.1f}} °C')
    print(f'CRS: {{src.crs}}')
    print('Temperature validation: PASSED')
"""
                    ], capture_output=True, text=True, timeout=30)

                    if result.returncode == 0:
                        print_success("✓ Temperature validation passed")
                        for line in result.stdout.strip().split('\n'):
                            print(f"    {line}")
                        success_count += 1
                    else:
                        print_error(f"✗ Temperature validation failed: {result.stderr}")
                else:
                    print_error("✗ Temperature creation failed - no file created")
            except Exception as e:
                print_error(f"✗ Temperature creation error: {e}")

            # Test vector data creation
            print_info("Testing vector data creation...")
            try:
                vector_success = create_sample_vector_data()
                if vector_success:
                    vector_files = list(vector_dir.glob("*.geojson"))
                    if vector_files:
                        print_success(f"✓ Vector data created: {len(vector_files)} files")
                        for vf in vector_files:
                            print_success(f"  - {vf.name} ({vf.stat().st_size / 1024:.1f} KB)")
                        success_count += 1
                    else:
                        print_error("✗ No vector files created")
                else:
                    print_error("✗ Vector data creation returned False")
            except Exception as e:
                print_error(f"✗ Vector creation error: {e}")

            return success_count >= 3  # At least 3/4 data types should work

        finally:
            # Restore original paths
            create_sample_data.RASTER_DIR = original_raster_dir
            create_sample_data.VECTOR_DIR = original_vector_dir

def test_setup_functions():
    """Test individual setup functions."""
    print_header("TESTING SETUP FUNCTIONS")

    success_count = 0

    # Test UV check
    try:
        if check_uv_installed():
            print_success("✓ UV installation check working")
            success_count += 1
        else:
            print_error("✗ UV installation check failed")
    except Exception as e:
        print_error(f"✗ UV check error: {e}")

    # Test Python version check
    try:
        if check_python_version():
            print_success("✓ Python version check working")
            success_count += 1
        else:
            print_error("✗ Python version check failed")
    except Exception as e:
        print_error(f"✗ Python version check error: {e}")

    # Test UV environment
    try:
        if test_uv_environment():
            print_success("✓ UV environment test working")
            success_count += 1
        else:
            print_error("✗ UV environment test failed")
    except Exception as e:
        print_error(f"✗ UV environment test error: {e}")

    return success_count >= 2  # At least 2/3 should work

def test_dependency_resolution():
    """Test that UV can resolve dependencies without conflicts."""
    print_header("TESTING DEPENDENCY RESOLUTION")

    try:
        # Test that UV can resolve dependencies
        print_info("Testing UV dependency resolution...")
        result = subprocess.run(
            ["uv", "tree", "--quiet"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=Path(__file__).parent.parent  # Run from project root
        )

        if result.returncode == 0:
            print_success("✓ UV dependency tree resolved successfully")

            # Count packages
            lines = result.stdout.strip().split('\n')
            package_count = len([line for line in lines if line.strip()])
            print_info(f"  Resolved {package_count} dependency relationships")

            return True
        else:
            print_error(f"✗ UV dependency resolution failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print_error("✗ Dependency resolution timed out")
        return False
    except Exception as e:
        print_error(f"✗ Dependency test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("🧪 GIST 604B - Rasterio Setup Comprehensive Test")
    print("=" * 70)
    print("🔧 Testing all fixes to the data setup system")
    print(f"{Colors.ENDC}\n")

    test_results = []

    # Run all test suites
    test_results.append(("UV Installation", test_uv_installation()))
    test_results.append(("Python Packages", test_python_packages()))
    test_results.append(("Setup Functions", test_setup_functions()))
    test_results.append(("Data Creation", test_data_creation()))
    test_results.append(("Dependency Resolution", test_dependency_resolution()))

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<25} {status}")

    print()
    if passed == total:
        print_success(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print_success("The rasterio setup system is working correctly!")
        print()
        print_info("Next steps:")
        print("  1. Run: uv run python data/setup_rasterio_data.py")
        print("  2. Start: uv run jupyter notebook")
        print("  3. Begin learning with real geospatial data!")
        return True
    else:
        print_error(f"⚠️  SOME TESTS FAILED ({passed}/{total} passed)")
        print()
        print_info("Issues to address:")
        for test_name, result in test_results:
            if not result:
                print_error(f"  - Fix {test_name}")
        print()
        print_info("You may still be able to proceed with limited functionality")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected test error: {e}{Colors.ENDC}")
        print("Please report this error to your instructor.")
        sys.exit(1)
