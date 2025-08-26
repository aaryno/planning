#!/usr/bin/env python3
"""
Student Environment Setup for GeoPandas Tutorial
===============================================

GIST 604B - Module 5: Python GIS Programming
Python GeoPandas Introduction Assignment

This script helps you set up your development environment for the GeoPandas
tutorial. Run this script after accepting the assignment and opening your
development environment.

Usage:
    python setup_student_environment.py

What this script does:
- Detects your operating system and provides appropriate guidance
- Checks that all required packages are installed
- Creates sample spatial datasets for the tutorials
- Validates your environment is ready for the assignments
- Provides troubleshooting guidance for common issues

IMPORTANT FOR WINDOWS USERS:
- This script will detect if you're on Windows
- Most spatial issues occur on Windows due to library compatibility
- We STRONGLY recommend using GitHub Codespaces instead
- Instructor cannot provide Windows-specific technical support

Requirements:
- Python 3.9 or higher
- GeoPandas and related spatial packages
- Internet connection (for some validation checks)
"""

import sys
import os
import platform
import subprocess
from pathlib import Path
import importlib.util

def print_header():
    """Print a welcome header"""
    print("🗺️" + "="*60)
    print("    GeoPandas Tutorial Environment Setup")
    print("    GIST 604B - Module 5: Python GIS Programming")
    print("="*62)
    print()

def check_operating_system():
    """Check operating system and provide Windows warning if needed"""
    print("🖥️  Checking operating system...")

    system = platform.system()
    print(f"   Operating System: {system}")

    if system == "Windows":
        print("\n" + "⚠️ " + "="*58)
        print("   ⚠️  WARNING: WINDOWS DETECTED")
        print("   ⚠️  POTENTIAL COMPATIBILITY ISSUES AHEAD")
        print("="*62)
        print()
        print("🚨 IMPORTANT FOR WINDOWS USERS:")
        print("   • Most open-source GIS tools work best on Unix systems")
        print("   • You may encounter installation and dependency issues")
        print("   • File path problems (backslash vs forward slash)")
        print("   • GDAL/GEOS library conflicts are common")
        print()
        print("✅ RECOMMENDED SOLUTION:")
        print("   1. Use GitHub Codespaces instead of local Windows")
        print("   2. Go to your assignment repository")
        print("   3. Click 'Code' → 'Create codespace on main'")
        print("   4. Everything will work perfectly in 2-3 minutes!")
        print()
        print("⚠️  SUPPORT POLICY:")
        print("   • ✅ Full support for Codespaces/Unix environments")
        print("   • ❌ NO support for Windows-specific issues")
        print("   • ❌ Instructor cannot help with Windows problems")
        print()

        response = input("Continue with Windows setup anyway? (y/N): ").lower()
        if response != 'y':
            print("\n🎯 Smart choice! Please use GitHub Codespaces instead.")
            print("   Your assignment repository → Code → Create codespace on main")
            return False
        else:
            print("\n⚠️  Proceeding with Windows setup at your own risk...")
    else:
        print(f"   ✅ {system} detected - good choice for spatial analysis!")

    return True

def check_python_version():
    """Check if Python version is adequate"""
    print("🐍 Checking Python version...")

    version = sys.version_info
    min_version = (3, 9)

    if version[:2] >= min_version:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Good!)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Too old!)")
        print(f"   💡 This tutorial requires Python {min_version[0]}.{min_version[1]} or higher")
        print("      Contact your instructor for help upgrading Python")
        return False

def check_package_installation():
    """Check if required packages are installed"""
    print("\n📦 Checking required packages...")

    required_packages = {
        'geopandas': 'GeoPandas (spatial data analysis)',
        'pandas': 'Pandas (data manipulation)',
        'numpy': 'NumPy (numerical computing)',
        'matplotlib': 'Matplotlib (plotting)',
        'shapely': 'Shapely (geometric operations)',
    }

    optional_packages = {
        'contextily': 'Contextily (basemaps)',
        'folium': 'Folium (interactive maps)',
        'jupyter': 'Jupyter (notebook environment)',
    }

    all_good = True
    installed_packages = {}

    # Check required packages
    for package, description in required_packages.items():
        try:
            spec = importlib.util.find_spec(package)
            if spec is not None:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"   ✅ {package} {version} - {description}")
                installed_packages[package] = version
            else:
                print(f"   ❌ {package} - {description} (NOT INSTALLED)")
                all_good = False
        except ImportError:
            print(f"   ❌ {package} - {description} (IMPORT ERROR)")
            all_good = False

    # Check optional packages
    print("\n📦 Checking optional packages...")
    for package, description in optional_packages.items():
        try:
            spec = importlib.util.find_spec(package)
            if spec is not None:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"   ✅ {package} {version} - {description}")
                installed_packages[package] = version
            else:
                print(f"   ⚠️  {package} - {description} (optional, not installed)")
        except ImportError:
            print(f"   ⚠️  {package} - {description} (optional, import error)")

    if not all_good:
        print("\n❌ Some required packages are missing!")
        print("\n💡 Installation suggestions:")
        print("   If using uv (recommended):")
        print('     uv add "geopandas~=0.14.1"')
        print('     uv add "matplotlib~=3.8.2"')
        print('     uv add "jupyter~=1.0.0"')
        print("\n   If using pip:")
        print('     pip install geopandas matplotlib jupyter')
        print("\n   If using conda:")
        print('     conda install -c conda-forge geopandas matplotlib jupyter')

    return all_good, installed_packages

def create_sample_data():
    """Create sample spatial data for tutorials"""
    print("\n📊 Creating sample spatial data...")

    try:
        import geopandas as gpd
        import pandas as pd
        import numpy as np
        from shapely.geometry import Point, LineString, Polygon
    except ImportError as e:
        print(f"   ❌ Cannot create sample data: {e}")
        return False

    # Create data directory
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    try:
        # Create Arizona cities data
        cities_data = {
            'name': ['Phoenix', 'Tucson', 'Mesa', 'Chandler', 'Scottsdale'],
            'population': [1608139, 548073, 504258, 275987, 241361],
            'county': ['Maricopa', 'Pima', 'Maricopa', 'Maricopa', 'Maricopa'],
            'longitude': [-112.0740, -110.9265, -111.8315, -111.8413, -111.9026],
            'latitude': [33.4484, 32.2217, 33.4152, 33.3062, 33.4942]
        }

        cities_df = pd.DataFrame(cities_data)
        geometry = [Point(xy) for xy in zip(cities_df.longitude, cities_df.latitude)]
        cities_gdf = gpd.GeoDataFrame(cities_df.drop(['longitude', 'latitude'], axis=1), geometry=geometry)
        cities_gdf.crs = 'EPSG:4326'

        # Save cities data
        cities_gdf.to_file(data_dir / 'arizona_cities.geojson', driver='GeoJSON')
        print(f"   ✅ Created arizona_cities.geojson ({len(cities_gdf)} cities)")

        # Create simple county polygons
        counties_data = []

        # Maricopa County (simplified)
        maricopa_coords = [(-113.0, 33.0), (-111.5, 33.0), (-111.5, 33.8),
                          (-112.5, 34.0), (-113.0, 33.8), (-113.0, 33.0)]
        counties_data.append({
            'name': 'Maricopa',
            'population': 4420568,
            'area_sq_miles': 9224,
            'geometry': Polygon(maricopa_coords)
        })

        # Pima County (simplified)
        pima_coords = [(-111.5, 31.8), (-110.5, 31.8), (-110.5, 32.8),
                      (-111.5, 32.8), (-111.5, 31.8)]
        counties_data.append({
            'name': 'Pima',
            'population': 1043433,
            'area_sq_miles': 9189,
            'geometry': Polygon(pima_coords)
        })

        counties_gdf = gpd.GeoDataFrame(counties_data)
        counties_gdf.crs = 'EPSG:4326'
        counties_gdf.to_file(data_dir / 'arizona_counties.geojson', driver='GeoJSON')
        print(f"   ✅ Created arizona_counties.geojson ({len(counties_gdf)} counties)")

        # Create highway line data
        highway_coords = [(-112.0740, 33.4484), (-111.6513, 35.1983)]  # Phoenix to Flagstaff
        highway_gdf = gpd.GeoDataFrame({
            'name': ['Interstate 17'],
            'type': ['Interstate'],
            'geometry': [LineString(highway_coords)]
        })
        highway_gdf.crs = 'EPSG:4326'
        highway_gdf.to_file(data_dir / 'arizona_highways.geojson', driver='GeoJSON')
        print(f"   ✅ Created arizona_highways.geojson ({len(highway_gdf)} highways)")

        # Create CSV with coordinates
        csv_data = pd.DataFrame({
            'location_name': ['Arizona Science Center', 'Phoenix Zoo', 'Desert Botanical Garden'],
            'longitude': [-112.0666, -112.0242, -111.9397],
            'latitude': [33.4483, 33.4491, 33.4619],
            'category': ['Museum', 'Zoo', 'Garden'],
            'rating': [4.5, 4.3, 4.6]
        })
        csv_data.to_csv(data_dir / 'phoenix_attractions.csv', index=False)
        print(f"   ✅ Created phoenix_attractions.csv ({len(csv_data)} attractions)")

        # Create data README
        readme_content = """# Sample Data for GeoPandas Tutorial

This directory contains sample spatial datasets for learning GeoPandas:

## Files:
- `arizona_cities.geojson` - Point data of major Arizona cities
- `arizona_counties.geojson` - Polygon data of Arizona counties
- `arizona_highways.geojson` - Line data of major highways
- `phoenix_attractions.csv` - CSV with longitude/latitude columns

## Coordinate System:
All spatial data uses WGS84 (EPSG:4326) coordinate system.

Generated by: setup_student_environment.py
"""

        with open(data_dir / 'README.md', 'w') as f:
            f.write(readme_content)
        print("   ✅ Created data/README.md")

        return True

    except Exception as e:
        print(f"   ❌ Error creating sample data: {e}")
        return False

def test_basic_functionality():
    """Test basic GeoPandas functionality"""
    print("\n🧪 Testing basic GeoPandas functionality...")

    try:
        import geopandas as gpd
        import matplotlib.pyplot as plt

        # Test loading data
        data_path = Path('data/arizona_cities.geojson')
        if data_path.exists():
            gdf = gpd.read_file(data_path)
            print(f"   ✅ Successfully loaded {len(gdf)} features from sample data")
            print(f"   ✅ CRS: {gdf.crs}")
            print(f"   ✅ Geometry types: {gdf.geometry.geom_type.iloc[0]}")

            # Test basic plotting (without showing)
            ax = gdf.plot(figsize=(10, 6), markersize=50)
            ax.set_title('Arizona Cities Test Plot')
            plt.close()  # Close without showing
            print("   ✅ Basic plotting works")

            return True
        else:
            print("   ❌ Sample data not found")
            return False

    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False

def check_notebook_environment():
    """Check if Jupyter notebook environment works"""
    print("\n📓 Checking Jupyter notebook environment...")

    try:
        import jupyter
        print(f"   ✅ Jupyter {jupyter.__version__} is available")

        # Check if we're in a notebook environment
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                print("   ✅ Running in Jupyter notebook environment")
            elif shell == 'TerminalInteractiveShell':
                print("   ℹ️  Running in IPython terminal")
            else:
                print("   ℹ️  Running in standard Python")
        except NameError:
            print("   ℹ️  Running in standard Python (not IPython/Jupyter)")

        return True

    except ImportError:
        print("   ⚠️  Jupyter not installed (you can still use Python scripts)")
        return False

def provide_next_steps(all_checks_passed):
    """Provide guidance on next steps"""
    print("\n" + "="*62)

    if all_checks_passed:
        print("🎉 ENVIRONMENT SETUP COMPLETE!")
        print("\n✅ Your environment is ready for the GeoPandas tutorial!")
        print("\n🚀 Next steps:")
        print("   1. Open notebooks/01_data_exploration.ipynb")
        print("   2. Run through the tutorial step-by-step")
        print("   3. Implement functions in src/geopandas_analysis/")
        print("   4. Test your code using the provided examples")
        print("   5. Submit your completed assignment")

        print("\n📚 Available notebooks:")
        notebook_dir = Path('notebooks')
        if notebook_dir.exists():
            for nb in sorted(notebook_dir.glob('*.ipynb')):
                print(f"   - {nb.name}")

        print("\n💡 Tips:")
        print("   - Start with the first notebook and work sequentially")
        print("   - Test your functions frequently in the notebooks")
        print("   - Use the sample data to understand spatial concepts")
        print("   - Ask for help if you get stuck!")

    else:
        print("⚠️  SETUP INCOMPLETE")
        print("\n❌ Some issues need to be resolved before you can start.")
        print("\n🛠️  Troubleshooting:")
        print("   1. Make sure all required packages are installed")
        print("   2. Verify your Python version is 3.9 or higher")
        print("   3. Check that you have internet connectivity")

        system = platform.system()
        if system == "Windows":
            print("\n🪟 FOR WINDOWS USERS:")
            print("   ❌ This is likely a Windows compatibility issue")
            print("   ✅ SOLUTION: Use GitHub Codespaces instead!")
            print("   • Go to your assignment repository")
            print("   • Click 'Code' → 'Create codespace on main'")
            print("   • All problems will disappear!")
        else:
            print("   4. Try running this setup script again")
            print("   5. Contact your instructor if problems persist")

        print("\n📞 Getting help:")
        print("   - Check the course discussion forum")
        if system != "Windows":
            print("   - Ask your instructor or TA")
        print("   - Review the assignment README.md")
        if system == "Windows":
            print("   - ⚠️  Note: No Windows-specific support available")

def main():
    """Main setup function"""
    print_header()

    # Check OS and warn Windows users
    if not check_operating_system():
        return False  # User chose not to continue on Windows

    # Track overall success
    all_checks = []

    # Run all checks
    all_checks.append(check_python_version())

    packages_ok, installed_packages = check_package_installation()
    all_checks.append(packages_ok)

    if packages_ok:  # Only create data if packages are available
        all_checks.append(create_sample_data())
        all_checks.append(test_basic_functionality())

    all_checks.append(check_notebook_environment())

    # Provide final guidance
    all_passed = all(all_checks)
    provide_next_steps(all_passed)

    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
        print("Please contact your instructor for assistance.")
        sys.exit(1)
