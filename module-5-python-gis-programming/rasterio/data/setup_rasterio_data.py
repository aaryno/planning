#!/usr/bin/env python3
"""
GIST 604B - Rasterio Learning Environment Setup
==============================================

This script prepares your computer for authentic geospatial data analysis by:
1. Checking required Python packages
2. Downloading real NASA/USGS datasets
3. Creating fallback synthetic data if needed
4. Validating your learning environment

Run this once before starting the rasterio notebooks.

Usage:
    python setup_rasterio_data.py

Author: GIST 604B Course Team
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path
import platform
import time
import json

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a colored header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message in green."""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message in yellow."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text):
    """Print error message in red."""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message in blue."""
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

# Required packages with version requirements
REQUIRED_PACKAGES = {
    'rasterio': '1.3.0',
    'geopandas': '0.14.0',
    'numpy': '1.21.0',
    'pandas': '2.0.0',
    'matplotlib': '3.5.0',
    'requests': '2.28.0',
    'tqdm': '4.64.0',
    'shapely': '2.0.0'
}

# Optional packages that enhance the experience
OPTIONAL_PACKAGES = {
    'rio_cogeo': '3.5.0',
    'contextily': '1.4.0',
    'xarray': '2023.1.0',
    'jupyter': '1.0.0'
}

def check_python_version():
    """Check if Python version is adequate."""
    print_info("Checking Python version...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python {version.major}.{version.minor} detected.")
        print_error("Python 3.8 or higher is required for geospatial packages.")
        print_error("Please upgrade Python and try again.")
        return False

    print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
    return True

def check_package_installed(package_name, min_version=None):
    """Check if a package is installed with minimum version."""
    try:
        module = importlib.import_module(package_name)

        if hasattr(module, '__version__'):
            installed_version = module.__version__
        elif hasattr(module, 'version'):
            installed_version = module.version
        else:
            installed_version = "unknown"

        if min_version and installed_version != "unknown":
            # Simple version comparison (works for most cases)
            from packaging import version
            if version.parse(installed_version) < version.parse(min_version):
                return False, installed_version

        return True, installed_version

    except ImportError:
        return False, None
    except Exception as e:
        print_warning(f"Could not check {package_name} version: {e}")
        return False, None

def install_package(package_name, version=None):
    """Install a package using pip."""
    try:
        if version:
            package_spec = f"{package_name}>={version}"
        else:
            package_spec = package_name

        print_info(f"Installing {package_spec}...")

        # Try different installation methods
        install_commands = [
            [sys.executable, "-m", "pip", "install", package_spec],
            [sys.executable, "-m", "pip", "install", "--user", package_spec]
        ]

        for cmd in install_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    print_success(f"Successfully installed {package_name}")
                    return True
                else:
                    print_warning(f"Installation attempt failed: {result.stderr}")
            except subprocess.TimeoutExpired:
                print_warning(f"Installation timeout for {package_name}")
            except Exception as e:
                print_warning(f"Installation error: {e}")

        # Try conda as fallback
        try:
            conda_cmd = ["conda", "install", "-c", "conda-forge", "-y", package_name]
            result = subprocess.run(conda_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print_success(f"Successfully installed {package_name} via conda")
                return True
        except:
            pass

        return False

    except Exception as e:
        print_error(f"Failed to install {package_name}: {e}")
        return False

def check_and_install_packages():
    """Check all required packages and install missing ones."""
    print_header("CHECKING PYTHON PACKAGES")

    missing_packages = []
    outdated_packages = []

    # Check required packages
    print_info("Checking required packages...")
    for package, min_version in REQUIRED_PACKAGES.items():
        is_installed, current_version = check_package_installed(package, min_version)

        if not is_installed:
            if current_version is None:
                print_warning(f"{package}: Not installed")
                missing_packages.append((package, min_version))
            else:
                print_warning(f"{package}: {current_version} < {min_version} (outdated)")
                outdated_packages.append((package, min_version))
        else:
            print_success(f"{package}: {current_version} ✓")

    # Check optional packages
    print_info("\nChecking optional packages...")
    optional_missing = []
    for package, min_version in OPTIONAL_PACKAGES.items():
        is_installed, current_version = check_package_installed(package, min_version)

        if not is_installed:
            if current_version is None:
                print_info(f"{package}: Not installed (optional)")
                optional_missing.append((package, min_version))
            else:
                print_info(f"{package}: {current_version} (optional, could be updated)")
        else:
            print_success(f"{package}: {current_version} ✓")

    # Install missing packages
    if missing_packages or outdated_packages:
        print_header("INSTALLING MISSING PACKAGES")

        all_to_install = missing_packages + outdated_packages
        print_info(f"Need to install/update {len(all_to_install)} packages...")

        failed_installs = []
        for package, version in all_to_install:
            if not install_package(package, version):
                failed_installs.append(package)
                print_error(f"Failed to install {package}")
            time.sleep(1)  # Brief pause between installations

        if failed_installs:
            print_error(f"\nFailed to install: {', '.join(failed_installs)}")
            print_info("You may need to install these manually:")
            for pkg in failed_installs:
                print(f"  pip install {pkg}>={REQUIRED_PACKAGES.get(pkg, 'latest')}")
            return False

    print_success("All required packages are available!")
    return True

def setup_data_directory():
    """Ensure data directory structure exists."""
    print_header("SETTING UP DATA DIRECTORIES")

    base_dir = Path(__file__).parent
    data_dirs = [
        base_dir / "data",
        base_dir / "data" / "raster",
        base_dir / "data" / "vector",
        base_dir / "data" / "downloads",
        base_dir / "data" / "processed"
    ]

    for directory in data_dirs:
        directory.mkdir(exist_ok=True, parents=True)
        print_success(f"Directory ready: {directory.relative_to(base_dir)}")

    return True

def download_real_data():
    """Run the data download script."""
    print_header("DOWNLOADING REAL GEOSPATIAL DATA")

    script_path = Path(__file__).parent / "create_sample_data.py"

    if not script_path.exists():
        print_error(f"Data creation script not found: {script_path}")
        return False

    try:
        print_info("Starting data download process...")
        print_info("This may take 5-15 minutes depending on your internet connection...")

        # Run the data creation script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,  # Show output in real-time
            text=True,
            cwd=script_path.parent,
            timeout=1800  # 30 minutes max
        )

        if result.returncode == 0:
            print_success("Data download completed successfully!")
            return True
        else:
            print_warning("Data download had some issues but may have succeeded")
            return True  # Still try to continue

    except subprocess.TimeoutExpired:
        print_error("Data download timed out")
        return False
    except Exception as e:
        print_error(f"Error running data download: {e}")
        return False

def validate_environment():
    """Validate that the environment is working correctly."""
    print_header("VALIDATING LEARNING ENVIRONMENT")

    validation_passed = True

    # Test 1: Import key packages
    print_info("Testing package imports...")
    test_imports = ['rasterio', 'geopandas', 'numpy', 'pandas', 'matplotlib']

    for package in test_imports:
        try:
            importlib.import_module(package)
            print_success(f"✓ {package}")
        except ImportError as e:
            print_error(f"✗ {package}: {e}")
            validation_passed = False

    # Test 2: Check if data files exist
    print_info("\nChecking for data files...")
    data_dir = Path(__file__).parent / "data"

    expected_files = [
        "data/README.md",
        "data/data_inventory.json"
    ]

    raster_files = list((data_dir / "raster").glob("*.tif")) if (data_dir / "raster").exists() else []
    vector_files = list((data_dir / "vector").glob("*.geojson")) if (data_dir / "vector").exists() else []

    if raster_files:
        print_success(f"✓ Found {len(raster_files)} raster files")
    else:
        print_warning("✗ No raster files found")
        validation_passed = False

    if vector_files:
        print_success(f"✓ Found {len(vector_files)} vector files")
    else:
        print_warning("✗ No vector files found")

    # Test 3: Try loading a raster file
    if raster_files:
        print_info("\nTesting raster data loading...")
        try:
            import rasterio
            test_file = raster_files[0]

            with rasterio.open(test_file) as src:
                data = src.read(1)
                print_success(f"✓ Successfully loaded {test_file.name}")
                print_success(f"  - Shape: {data.shape}")
                print_success(f"  - Data type: {data.dtype}")
                print_success(f"  - CRS: {src.crs}")

        except Exception as e:
            print_error(f"✗ Failed to load raster data: {e}")
            validation_passed = False

    return validation_passed

def show_next_steps():
    """Show students what to do next."""
    print_header("READY TO START LEARNING!")

    data_dir = Path(__file__).parent / "data"

    print_info("Your rasterio learning environment is ready! 🎉")
    print()
    print("📚 Next Steps:")
    print("   1. Open the notebook: 01_function_load_and_explore_raster.ipynb")
    print("   2. Start with the overview: 00_start_here_overview.ipynb")
    print("   3. Check your data: look in data/README.md")
    print()
    print("🗂️  Available Data:")

    if (data_dir / "raster").exists():
        raster_files = list((data_dir / "raster").glob("*.tif"))
        for raster_file in raster_files[:3]:  # Show first 3
            print(f"   📊 {raster_file.name}")

    if (data_dir / "vector").exists():
        vector_files = list((data_dir / "vector").glob("*.geojson"))
        for vector_file in vector_files[:2]:  # Show first 2
            print(f"   📍 {vector_file.name}")

    print()
    print("🧪 Quick Test:")
    print("   import rasterio")
    print("   with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:")
    print("       print(f'DEM shape: {src.shape}')")
    print("       print(f'CRS: {src.crs}')")
    print()
    print("🆘 Need Help?")
    print("   - Check data/README.md for examples")
    print("   - Review notebook 00_start_here_overview.ipynb")
    print("   - Ask your instructor or TA")
    print()
    print(f"{Colors.OKGREEN}{Colors.BOLD}Happy Learning! 🚀{Colors.ENDC}")

def main():
    """Main setup process."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("🌍 GIST 604B - Rasterio Learning Environment Setup")
    print("=" * 60)
    print("🎓 University of Arizona - School of Geography")
    print("📡 Preparing real geospatial data for authentic learning")
    print(f"{Colors.ENDC}")

    # Check system requirements
    if not check_python_version():
        print_error("❌ Python version check failed")
        return False

    # Set up directories
    if not setup_data_directory():
        print_error("❌ Directory setup failed")
        return False

    # Install/check packages
    if not check_and_install_packages():
        print_error("❌ Package installation failed")
        print_info("Try running: pip install -r requirements.txt")
        return False

    # Download data
    if not download_real_data():
        print_warning("⚠️ Data download had issues, but continuing...")

    # Validate environment
    if not validate_environment():
        print_warning("⚠️ Environment validation had issues")
        print_info("You may still be able to proceed with available data")

    # Show next steps
    show_next_steps()

    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{Colors.OKGREEN}🎉 Setup completed successfully!{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.WARNING}⚠️  Setup completed with warnings{Colors.ENDC}")
            print("Check the messages above and try to resolve any issues.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        print("Please report this error to your instructor.")
        sys.exit(1)
