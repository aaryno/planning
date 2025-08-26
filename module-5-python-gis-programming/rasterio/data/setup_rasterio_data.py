#!/usr/bin/env python3
"""
GIST 604B - Rasterio Learning Environment Setup with UV
======================================================

This script prepares your computer for authentic geospatial data analysis using
modern Python package management with UV. It will:

1. Check for UV package manager installation
2. Set up virtual environment and install dependencies
3. Download real NASA/USGS datasets
4. Create fallback synthetic data if needed
5. Validate your learning environment

Run this once before starting the rasterio notebooks.

Usage:
    uv run python data/setup_rasterio_data.py

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
import shutil

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
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

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

def check_uv_installed():
    """Check if UV package manager is installed."""
    print_info("Checking for UV package manager...")

    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"UV found: {version}")
            return True
        else:
            print_error("UV command failed")
            return False
    except FileNotFoundError:
        print_error("UV not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print_error("UV check timed out")
        return False
    except Exception as e:
        print_error(f"Error checking UV: {e}")
        return False

def install_uv():
    """Guide user to install UV."""
    print_header("UV INSTALLATION REQUIRED")

    print_info("UV is a fast Python package manager required for this assignment.")
    print()
    print("📥 Installation options:")
    print()

    # Platform-specific installation instructions
    system = platform.system().lower()

    if system == "windows":
        print("🪟 Windows:")
        print("   Option 1 (Recommended): Use GitHub Codespaces")
        print("   Option 2: Install via PowerShell:")
        print("     powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        print("   Option 3: Use pip:")
        print("     pip install uv")

    elif system == "darwin":  # macOS
        print("🍎 macOS:")
        print("   Option 1 (Recommended): Homebrew:")
        print("     brew install uv")
        print("   Option 2: Install script:")
        print("     curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   Option 3: Use pip:")
        print("     pip install uv")

    else:  # Linux and others
        print("🐧 Linux:")
        print("   Option 1 (Recommended): Install script:")
        print("     curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   Option 2: Use pip:")
        print("     pip install uv")

    print()
    print("After installation:")
    print("1. Restart your terminal")
    print("2. Run this setup script again")
    print()
    print_warning("⚠️  Installation required before continuing!")

    return False

def check_python_version():
    """Check if Python version is adequate."""
    print_info("Checking Python version...")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python {version.major}.{version.minor} detected.")
        print_error("Python 3.11 or higher is required for this assignment.")
        print_info("Consider using GitHub Codespaces for pre-configured environment.")
        return False

    print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
    return True

def setup_uv_environment():
    """Set up UV virtual environment and install dependencies."""
    print_header("SETTING UP UV ENVIRONMENT")

    # Find project root (directory with pyproject.toml)
    current_dir = Path.cwd()
    project_root = None

    # Look for pyproject.toml in current dir and parent dirs
    for path in [current_dir] + list(current_dir.parents):
        if (path / "pyproject.toml").exists():
            project_root = path
            break

    if not project_root:
        print_error("Could not find pyproject.toml file")
        print_info("Make sure you're running this from the rasterio assignment directory")
        return False

    print_info(f"Project root: {project_root}")

    try:
        # Change to project root
        original_cwd = os.getcwd()
        os.chdir(project_root)

        # Sync dependencies with UV
        print_info("Installing dependencies with UV...")
        result = subprocess.run(
            ["uv", "sync", "--group", "test", "--group", "dev", "--group", "download"],
            capture_output=False,  # Show output in real-time
            text=True,
            timeout=300  # 5 minutes
        )

        if result.returncode == 0:
            print_success("Dependencies installed successfully!")
        else:
            print_warning("Some dependencies may not have installed correctly")
            print_info("This might still work - continuing...")

        # Restore original directory
        os.chdir(original_cwd)

        return True

    except subprocess.TimeoutExpired:
        print_error("Dependency installation timed out")
        return False
    except Exception as e:
        print_error(f"Error setting up environment: {e}")
        return False
    finally:
        # Always restore directory
        try:
            os.chdir(original_cwd)
        except:
            pass

def test_uv_environment():
    """Test that key packages work with UV."""
    print_header("TESTING UV ENVIRONMENT")

    # Test imports using UV
    test_imports = [
        ('rasterio', 'import rasterio; print(f"Rasterio {rasterio.__version__}")'),
        ('geopandas', 'import geopandas; print(f"GeoPandas {geopandas.__version__}")'),
        ('numpy', 'import numpy; print(f"NumPy {numpy.__version__}")'),
        ('requests', 'import requests; print(f"Requests {requests.__version__}")'),
        ('tqdm', 'import tqdm; print(f"TQDM {tqdm.__version__}")'),
    ]

    success_count = 0

    for package, test_code in test_imports:
        try:
            print_info(f"Testing {package}...")
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

        except subprocess.TimeoutExpired:
            print_error(f"✗ {package} test timed out")
        except Exception as e:
            print_error(f"✗ {package} test error: {e}")

    if success_count >= 4:  # At least 4/5 packages working
        print_success(f"Environment test passed! ({success_count}/5 packages working)")
        return True
    else:
        print_warning(f"Environment test had issues ({success_count}/5 packages working)")
        print_info("You may still be able to proceed with limited functionality")
        return success_count > 0

def setup_data_directory():
    """Ensure data directory structure exists."""
    print_header("SETTING UP DATA DIRECTORIES")

    # Find the data directory
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent  # Go up to rasterio root

    data_dirs = [
        script_dir,  # data/ directory (where this script is)
        script_dir / "raster",
        script_dir / "vector",
        script_dir / "downloads",
        script_dir / "processed"
    ]

    for directory in data_dirs:
        directory.mkdir(exist_ok=True, parents=True)
        print_success(f"Directory ready: {directory.relative_to(base_dir)}")

    return True

def download_real_data():
    """Run the data download script with UV."""
    print_header("DOWNLOADING REAL GEOSPATIAL DATA")

    script_path = Path(__file__).parent / "create_sample_data.py"

    if not script_path.exists():
        print_error(f"Data creation script not found: {script_path}")
        print_info("Looking for create_sample_data.py in the data directory...")
        return False

    try:
        print_info("Starting real geospatial data download...")
        print_info("This uses NASA, USGS, and NOAA data sources")
        print_info("Download time: 5-15 minutes depending on internet connection")
        print_info("Will create high-quality synthetic data if downloads fail")
        print()

        # Run the data creation script with UV
        result = subprocess.run(
            ["uv", "run", "python", str(script_path)],
            capture_output=False,  # Show output in real-time
            text=True,
            cwd=script_path.parent,
            timeout=1800  # 30 minutes max
        )

        if result.returncode == 0:
            print_success("Data setup completed successfully!")
            return True
        else:
            print_warning("Data setup completed with some warnings")
            print_info("You should still be able to use the assignment data")
            return True  # Still continue - synthetic fallbacks should work

    except subprocess.TimeoutExpired:
        print_error("Data download timed out after 30 minutes")
        print_info("Try running the data creation script separately")
        return False
    except FileNotFoundError:
        print_error("UV command not found - is UV properly installed?")
        return False
    except Exception as e:
        print_error(f"Error running data download: {e}")
        return False

def validate_final_environment():
    """Final validation that everything is working."""
    print_header("FINAL ENVIRONMENT VALIDATION")

    validation_passed = True

    # Check 1: UV environment working
    print_info("Testing UV command execution...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", "print('UV environment working!')"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print_success("✓ UV environment working")
        else:
            print_error("✗ UV environment failed")
            validation_passed = False
    except:
        print_error("✗ UV command failed")
        validation_passed = False

    # Check 2: Data files exist
    print_info("Checking for data files...")
    data_dir = Path(__file__).parent

    expected_dirs = ["raster", "vector"]
    for dir_name in expected_dirs:
        dir_path = data_dir / dir_name
        if dir_path.exists() and any(dir_path.iterdir()):
            files = list(dir_path.glob("*"))
            print_success(f"✓ {dir_name}/ directory has {len(files)} files")
        else:
            print_warning(f"✗ {dir_name}/ directory missing or empty")

    # Check 3: Can load a raster file
    raster_files = list((data_dir / "raster").glob("*.tif")) if (data_dir / "raster").exists() else []

    if raster_files:
        print_info("Testing raster data loading...")
        test_file = raster_files[0]
        try:
            test_code = f"""
import rasterio
import numpy as np

with rasterio.open(r'{test_file}') as src:
    data = src.read(1)
    print(f'Successfully loaded: {test_file.name}')
    print(f'Shape: {{data.shape}}')
    print(f'Data type: {{data.dtype}}')
    print(f'CRS: {{src.crs}}')
    print(f'Valid data range: {{np.nanmin(data):.2f}} to {{np.nanmax(data):.2f}}')
"""

            result = subprocess.run(
                ["uv", "run", "python", "-c", test_code],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print_success("✓ Raster data loading test passed")
                # Print some of the output
                for line in result.stdout.strip().split('\n')[:5]:
                    print(f"  {line}")
            else:
                print_error("✗ Raster data loading failed")
                print_error(f"Error: {result.stderr}")
                validation_passed = False

        except Exception as e:
            print_error(f"✗ Raster test error: {e}")
            validation_passed = False
    else:
        print_warning("✗ No raster files found for testing")

    return validation_passed

def show_next_steps():
    """Show students what to do next."""
    print_header("🎉 READY TO START LEARNING!")

    data_dir = Path(__file__).parent
    project_root = data_dir.parent

    print_success("Your rasterio learning environment is ready!")
    print()
    print("📚 Next Steps:")
    print("   1. Open Jupyter: uv run jupyter notebook")
    print("   2. Start with: notebooks/00_start_here_overview.ipynb")
    print("   3. Or try: notebooks/01_function_load_and_explore_raster.ipynb")
    print()
    print("🧪 Quick Test Commands:")
    print("   # Test your setup")
    print("   uv run python -c \"import rasterio; print('Rasterio ready!')\"")
    print()
    print("   # Load real data")
    print("   uv run python -c \"")
    print("   import rasterio")
    print("   with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:")
    print("       print(f'DEM loaded: {src.shape} pixels')")
    print("   \"")
    print()
    print("🗂️  Your Data:")

    if (data_dir / "raster").exists():
        raster_files = list((data_dir / "raster").glob("*.tif"))
        for raster_file in raster_files[:3]:  # Show first 3
            size_mb = raster_file.stat().st_size / (1024 * 1024)
            print(f"   🌍 {raster_file.name} ({size_mb:.1f} MB)")

    if (data_dir / "vector").exists():
        vector_files = list((data_dir / "vector").glob("*.geojson"))
        for vector_file in vector_files[:2]:  # Show first 2
            size_kb = vector_file.stat().st_size / 1024
            print(f"   📍 {vector_file.name} ({size_kb:.1f} KB)")

    print()
    print("🆘 Need Help?")
    print("   - Check data/README.md for dataset documentation")
    print("   - Review notebooks/00_start_here_overview.ipynb")
    print("   - Test with: uv run pytest tests/ -v")
    print("   - Ask your instructor or TA")
    print()
    print("🚀 Running Assignment:")
    print("   # Run tests as you work")
    print("   uv run pytest tests/ -k 'test_load_and_explore_raster' -v")
    print()
    print("   # Run all tests when complete")
    print("   uv run pytest tests/ -v")
    print()
    print(f"{Colors.OKGREEN}{Colors.BOLD}Happy Learning with Real Geospatial Data! 🌍✨{Colors.ENDC}")

def main():
    """Main setup process."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("🌍 GIST 604B - Rasterio Real Data Setup with UV")
    print("=" * 70)
    print("🎓 University of Arizona - School of Geography")
    print("📡 Setting up real NASA/USGS data with modern Python tools")
    print("🔧 Using UV for fast, reliable package management")
    print(f"{Colors.ENDC}")

    success = True

    # Step 1: Check UV installation
    if not check_uv_installed():
        return install_uv()

    # Step 2: Check Python version
    if not check_python_version():
        print_error("❌ Python version check failed")
        print_info("Consider using GitHub Codespaces for compatible environment")
        return False

    # Step 3: Set up UV environment
    if not setup_uv_environment():
        print_error("❌ UV environment setup failed")
        return False

    # Step 4: Test UV environment
    if not test_uv_environment():
        print_warning("⚠️ Environment testing had issues")
        print_info("Continuing anyway - some features may not work")
        success = False

    # Step 5: Set up directories
    if not setup_data_directory():
        print_error("❌ Directory setup failed")
        return False

    # Step 6: Download real geospatial data
    if not download_real_data():
        print_warning("⚠️ Data download had issues")
        print_info("Assignment may still work with synthetic fallback data")
        success = False

    # Step 7: Final validation
    if not validate_final_environment():
        print_warning("⚠️ Final validation had issues")
        print_info("Check the messages above and try to resolve problems")
        success = False

    # Step 8: Show next steps
    show_next_steps()

    # Final status
    if success:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Setup completed successfully!{Colors.ENDC}")
        print("You're ready to start learning with real geospatial data!")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  Setup completed with warnings{Colors.ENDC}")
        print("You should still be able to complete the assignment.")
        print("Check any error messages above and ask for help if needed.")

    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        print("Please report this error to your instructor.")
        sys.exit(1)
