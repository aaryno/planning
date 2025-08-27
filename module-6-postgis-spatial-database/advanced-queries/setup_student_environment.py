#!/usr/bin/env python3
"""
Student Environment Setup Script
Python Rasterio Advanced Processing Assignment

This script sets up the development environment for students by:
1. Verifying all required packages are installed and working
2. Creating necessary directory structure
3. Generating realistic test datasets for development and testing
4. Providing feedback on environment status and potential issues

Author: GIST 604B Course Staff
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import sys
import os
import warnings
from pathlib import Path
import tempfile
import logging
from typing import Dict, List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Verify Python version meets requirements."""
    print("🐍 Checking Python version...")

    version = sys.version_info
    if version.major == 3 and version.minor >= 13:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Good!")
        return True
    else:
        print(f"⚠️  Python {version.major}.{version.minor}.{version.micro} - "
              "Python 3.13+ recommended")
        return False


def check_required_packages() -> Dict[str, bool]:
    """Check if all required packages are available and working."""
    print("\n📦 Checking required packages...")

    package_status = {}

    # Core packages
    required_packages = {
        'numpy': 'NumPy for numerical computing',
        'rasterio': 'Rasterio for raster I/O operations',
        'geopandas': 'GeoPandas for vector-raster integration',
        'pandas': 'Pandas for data manipulation',
        'matplotlib': 'Matplotlib for visualization',
        'scipy': 'SciPy for scientific computing',
    }

    # Optional but recommended packages
    optional_packages = {
        'xarray': 'Xarray for N-dimensional arrays',
        'dask': 'Dask for parallel processing',
        'pystac_client': 'PySTAC Client for STAC API access',
        'planetary_computer': 'Microsoft Planetary Computer SDK',
        'stackstac': 'Stackstac for STAC to xarray conversion',
        'rasterstats': 'Rasterstats for zonal statistics',
        'contextily': 'Contextily for basemap tiles',
        'folium': 'Folium for interactive maps',
    }

    all_packages = {**required_packages, **optional_packages}

    for package_name, description in all_packages.items():
        try:
            module = __import__(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package_name} ({version}) - {description}")
            package_status[package_name] = True
        except ImportError:
            print(f"❌ {package_name} - Missing: {description}")
            package_status[package_name] = False

    # Special check for GDAL (through rasterio)
    if package_status.get('rasterio', False):
        try:
            import rasterio
            from osgeo import gdal
            print(f"✅ GDAL ({gdal.__version__}) - Geospatial data abstraction library")
            package_status['gdal'] = True
        except ImportError:
            print("❌ GDAL - Missing geospatial data library")
            package_status['gdal'] = False

    return package_status


def create_directory_structure():
    """Create the required directory structure."""
    print("\n📁 Creating directory structure...")

    directories = [
        'data',
        'data/raster',
        'data/vector',
        'data/processed',
        'output',
        'output/maps',
        'output/cogs',
        'output/analysis',
        'notebooks',
        'scripts',
    ]

    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📂 Created: {directory}")

    print("✅ Directory structure created successfully!")


def generate_sample_dem_data():
    """Generate realistic DEM (Digital Elevation Model) data for Phoenix area."""
    print("\n🗻 Generating sample DEM data...")

    try:
        import numpy as np
        import rasterio
        from rasterio.transform import from_bounds
        from rasterio.crs import CRS

        # Phoenix area bounds
        bounds = (-112.5, 33.0, -111.5, 34.0)  # minx, miny, maxx, maxy
        width, height = 1000, 800

        # Generate realistic elevation surface
        x = np.linspace(0, width, width)
        y = np.linspace(0, height, height)
        X, Y = np.meshgrid(x, y)

        # Create elevation surface with:
        # - Base elevation around 1000ft (Phoenix average)
        # - Mountain ranges (South Mountain, Camelback)
        # - Desert valleys
        base_elevation = 350  # meters (Phoenix elevation)

        # Add topographic features
        elevation = (
            base_elevation +
            200 * np.sin(X / 200) * np.cos(Y / 150) +  # Rolling hills
            150 * np.exp(-((X - width/3)**2 + (Y - height/2)**2) / 20000) +  # Mountain peak
            100 * np.exp(-((X - 2*width/3)**2 + (Y - height/4)**2) / 15000) +  # Another peak
            50 * np.random.random((height, width)) - 25  # Random noise
        )

        # Ensure realistic elevation range
        elevation = np.clip(elevation, 200, 800)  # 200m to 800m elevation
        elevation = elevation.astype(np.float32)

        # Add some nodata areas (lakes, urban areas)
        elevation[50:80, 100:150] = np.nan  # Simulate water body
        elevation[200:220, 300:350] = np.nan  # Urban area

        transform = from_bounds(*bounds, width, height)

        # Write DEM
        dem_path = Path('data/raster/phoenix_dem.tif')
        with rasterio.open(
            dem_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=elevation.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            nodata=np.nan,
            compress='lzw'
        ) as dst:
            dst.write(elevation, 1)

            # Add metadata
            dst.update_tags(
                title='Phoenix Area Digital Elevation Model',
                description='Synthetic DEM for educational purposes',
                source='GIST 604B Course - Generated Data',
                units='meters'
            )

        print(f"✅ Created DEM: {dem_path}")
        print(f"   Dimensions: {width} x {height}")
        print(f"   Elevation range: {np.nanmin(elevation):.1f} - {np.nanmax(elevation):.1f} meters")

        return True

    except Exception as e:
        print(f"❌ Failed to create DEM: {e}")
        return False


def generate_sample_satellite_imagery():
    """Generate realistic multispectral satellite imagery."""
    print("\n🛰️ Generating sample satellite imagery...")

    try:
        import numpy as np
        import rasterio
        from rasterio.transform import from_bounds
        from rasterio.crs import CRS

        # Smaller area for detailed analysis
        bounds = (-112.2, 33.2, -111.8, 33.6)
        width, height = 500, 400

        np.random.seed(42)  # Reproducible data

        # Simulate Landsat-8 like bands (scaled to uint16)
        # Typical reflectance values scaled to 0-10000 range

        # Blue band (coastal/aerosol areas)
        blue = np.random.randint(800, 1500, (height, width)).astype(np.uint16)

        # Green band
        green = np.random.randint(900, 1800, (height, width)).astype(np.uint16)

        # Red band
        red = np.random.randint(1000, 2200, (height, width)).astype(np.uint16)

        # Near Infrared (NIR) - higher for vegetation
        nir = np.random.randint(2000, 5000, (height, width)).astype(np.uint16)

        # SWIR bands
        swir1 = np.random.randint(1500, 3500, (height, width)).astype(np.uint16)
        swir2 = np.random.randint(1000, 3000, (height, width)).astype(np.uint16)

        # Add spatial patterns for realism
        x = np.linspace(0, 10, width)
        y = np.linspace(0, 8, height)
        X, Y = np.meshgrid(x, y)

        # Vegetation patterns (higher NIR)
        vegetation_mask = np.sin(X/2) * np.cos(Y/3) > 0.3
        nir[vegetation_mask] = nir[vegetation_mask] * 1.5
        red[vegetation_mask] = red[vegetation_mask] * 0.8

        # Water bodies (lower NIR, higher blue)
        water_mask = ((X - 5)**2 + (Y - 4)**2) < 4  # Circular water body
        nir[water_mask] = nir[water_mask] * 0.3
        blue[water_mask] = blue[water_mask] * 1.4
        swir1[water_mask] = swir1[water_mask] * 0.2
        swir2[water_mask] = swir2[water_mask] * 0.1

        # Urban areas (similar reflectance across bands)
        urban_mask = (X > 7) & (Y < 2)
        red[urban_mask] = red[urban_mask] * 1.2
        green[urban_mask] = green[urban_mask] * 1.2
        blue[urban_mask] = blue[urban_mask] * 1.1
        nir[urban_mask] = nir[urban_mask] * 0.9

        # Stack all bands
        imagery = np.stack([blue, green, red, nir, swir1, swir2])

        # Add cloud shadows and nodata
        cloud_mask = ((X - 2)**2 + (Y - 6)**2) < 1.5
        imagery[:, cloud_mask] = 0  # Clouds/shadows as nodata

        transform = from_bounds(*bounds, width, height)

        # Write multispectral image
        landsat_path = Path('data/raster/phoenix_landsat.tif')
        with rasterio.open(
            landsat_path, 'w',
            driver='GTiff',
            height=height, width=width, count=6,
            dtype=imagery.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            nodata=0,
            compress='lzw'
        ) as dst:

            band_descriptions = ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2']

            for i in range(6):
                dst.write(imagery[i], i + 1)
                dst.set_band_description(i + 1, band_descriptions[i])

            dst.update_tags(
                title='Phoenix Area Multispectral Imagery',
                description='Synthetic Landsat-like imagery for educational purposes',
                source='GIST 604B Course - Generated Data',
                acquisition_date='2023-07-15',
                cloud_cover='5%'
            )

        print(f"✅ Created multispectral imagery: {landsat_path}")
        print(f"   Dimensions: {width} x {height} x 6 bands")
        print(f"   Bands: Blue, Green, Red, NIR, SWIR1, SWIR2")

        return True

    except Exception as e:
        print(f"❌ Failed to create satellite imagery: {e}")
        return False


def generate_sample_temperature_data():
    """Generate sample temperature raster for environmental analysis."""
    print("\n🌡️ Generating sample temperature data...")

    try:
        import numpy as np
        import rasterio
        from rasterio.transform import from_bounds
        from rasterio.crs import CRS

        bounds = (-112.3, 33.1, -111.7, 33.7)
        width, height = 600, 500

        # Generate realistic temperature surface for Phoenix summer
        x = np.linspace(0, width, width)
        y = np.linspace(0, height, height)
        X, Y = np.meshgrid(x, y)

        # Base temperature (Phoenix summer average ~40°C)
        base_temp = 40.0

        # Urban heat island effect
        urban_center_x, urban_center_y = width/2, height/2
        urban_heat = 8 * np.exp(-((X - urban_center_x)**2 + (Y - urban_center_y)**2) / 50000)

        # Elevation cooling (higher elevation = cooler)
        elevation_effect = -0.006 * (200 + 300 * np.sin(X/200) * np.cos(Y/150))  # ~6°C per 1000m

        # Time of day variation
        daily_variation = 3 * np.sin(X/100)  # Simulate time gradient

        # Random noise
        noise = 2 * np.random.random((height, width)) - 1

        temperature = base_temp + urban_heat + elevation_effect + daily_variation + noise
        temperature = temperature.astype(np.float32)

        # Add some missing data areas
        temperature[100:120, 200:250] = np.nan

        transform = from_bounds(*bounds, width, height)

        temp_path = Path('data/raster/phoenix_temperature.tif')
        with rasterio.open(
            temp_path, 'w',
            driver='GTiff',
            height=height, width=width, count=1,
            dtype=temperature.dtype,
            crs=CRS.from_epsg(4326),
            transform=transform,
            nodata=np.nan,
            compress='lzw'
        ) as dst:
            dst.write(temperature, 1)

            dst.update_tags(
                title='Phoenix Area Surface Temperature',
                description='Synthetic temperature data for educational purposes',
                source='GIST 604B Course - Generated Data',
                units='Celsius',
                date='2023-07-15T14:00:00Z'
            )

        print(f"✅ Created temperature raster: {temp_path}")
        print(f"   Temperature range: {np.nanmin(temperature):.1f} - {np.nanmax(temperature):.1f}°C")

        return True

    except Exception as e:
        print(f"❌ Failed to create temperature data: {e}")
        return False


def generate_sample_vector_data():
    """Generate sample vector data for raster-vector integration."""
    print("\n📍 Generating sample vector data...")

    try:
        import geopandas as gpd
        import pandas as pd
        from shapely.geometry import Point, Polygon
        import numpy as np

        # Phoenix area bounds
        bounds = (-112.5, 33.0, -111.5, 34.0)

        # 1. Generate sample points (monitoring stations)
        np.random.seed(123)
        n_points = 50

        lons = np.random.uniform(bounds[0], bounds[2], n_points)
        lats = np.random.uniform(bounds[1], bounds[3], n_points)

        points = [Point(lon, lat) for lon, lat in zip(lons, lats)]

        # Add attributes
        station_types = np.random.choice(['weather', 'air_quality', 'water'], n_points,
                                       p=[0.4, 0.4, 0.2])
        station_ids = [f"STN_{i:03d}" for i in range(n_points)]
        elevations = np.random.uniform(300, 600, n_points)  # Estimated elevations

        points_gdf = gpd.GeoDataFrame({
            'station_id': station_ids,
            'station_type': station_types,
            'elevation_m': elevations,
            'active': np.random.choice([True, False], n_points, p=[0.8, 0.2]),
            'geometry': points
        }, crs='EPSG:4326')

        points_path = Path('data/vector/sampling_points.shp')
        points_gdf.to_file(points_path)
        print(f"✅ Created sampling points: {points_path} ({len(points_gdf)} points)")

        # 2. Generate study area polygons
        study_areas = []

        # Central Phoenix urban area
        central_poly = Polygon([
            (-112.2, 33.3),
            (-111.9, 33.3),
            (-111.9, 33.6),
            (-112.2, 33.6),
            (-112.2, 33.3)
        ])

        # Suburban area
        suburban_poly = Polygon([
            (-112.4, 33.1),
            (-112.1, 33.1),
            (-112.1, 33.3),
            (-112.4, 33.3),
            (-112.4, 33.1)
        ])

        # Desert preserve area
        desert_poly = Polygon([
            (-111.8, 33.4),
            (-111.5, 33.4),
            (-111.5, 33.7),
            (-111.8, 33.7),
            (-111.8, 33.4)
        ])

        study_areas_gdf = gpd.GeoDataFrame({
            'area_id': ['CENTRAL', 'SUBURBAN', 'DESERT'],
            'area_name': ['Central Phoenix', 'Suburban West', 'Desert Preserve'],
            'land_use': ['urban', 'residential', 'natural'],
            'area_km2': [45.2, 38.7, 67.3],
            'population': [125000, 89000, 0],
            'geometry': [central_poly, suburban_poly, desert_poly]
        }, crs='EPSG:4326')

        study_areas_path = Path('data/vector/study_areas.shp')
        study_areas_gdf.to_file(study_areas_path)
        print(f"✅ Created study areas: {study_areas_path} ({len(study_areas_gdf)} polygons)")

        # 3. Generate administrative boundaries
        phoenix_boundary = Polygon([
            (-112.5, 33.0),
            (-111.5, 33.0),
            (-111.5, 34.0),
            (-112.5, 34.0),
            (-112.5, 33.0)
        ])

        boundaries_gdf = gpd.GeoDataFrame({
            'boundary_id': ['PHX_001'],
            'name': ['Phoenix Study Region'],
            'type': ['study_boundary'],
            'established': ['2023-01-01'],
            'geometry': [phoenix_boundary]
        }, crs='EPSG:4326')

        boundaries_path = Path('data/vector/phoenix_boundary.shp')
        boundaries_gdf.to_file(boundaries_path)
        print(f"✅ Created boundaries: {boundaries_path}")

        return True

    except Exception as e:
        print(f"❌ Failed to create vector data: {e}")
        return False


def test_raster_operations():
    """Test basic raster operations to ensure everything works."""
    print("\n🧪 Testing basic raster operations...")

    try:
        import rasterio
        import numpy as np

        # Test reading the DEM we created
        dem_path = Path('data/raster/phoenix_dem.tif')
        if dem_path.exists():
            with rasterio.open(dem_path) as src:
                # Read a small window
                data = src.read(1, window=rasterio.windows.Window(0, 0, 100, 100))

                print(f"✅ Successfully read DEM data")
                print(f"   Shape: {data.shape}")
                print(f"   Data type: {data.dtype}")
                print(f"   Value range: {np.nanmin(data):.1f} - {np.nanmax(data):.1f}")

        # Test reading multispectral data
        landsat_path = Path('data/raster/phoenix_landsat.tif')
        if landsat_path.exists():
            with rasterio.open(landsat_path) as src:
                # Calculate simple NDVI
                red = src.read(3)  # Red band
                nir = src.read(4)  # NIR band

                # Safe NDVI calculation
                with np.errstate(divide='ignore', invalid='ignore'):
                    ndvi = (nir - red) / (nir + red)
                    ndvi = np.where(np.isfinite(ndvi), ndvi, np.nan)

                valid_ndvi = ndvi[~np.isnan(ndvi)]
                if len(valid_ndvi) > 0:
                    print(f"✅ NDVI calculation successful")
                    print(f"   NDVI range: {np.min(valid_ndvi):.3f} - {np.max(valid_ndvi):.3f}")
                    print(f"   Mean NDVI: {np.mean(valid_ndvi):.3f}")

        return True

    except Exception as e:
        print(f"❌ Raster operations test failed: {e}")
        return False


def test_vector_raster_integration():
    """Test vector-raster integration capabilities."""
    print("\n🔗 Testing vector-raster integration...")

    try:
        import geopandas as gpd
        import rasterio
        from rasterstats import zonal_stats

        # Test loading vector data
        points_path = Path('data/vector/sampling_points.shp')
        if points_path.exists():
            points_gdf = gpd.read_file(points_path)
            print(f"✅ Loaded {len(points_gdf)} sampling points")

        # Test zonal statistics
        dem_path = Path('data/raster/phoenix_dem.tif')
        study_areas_path = Path('data/vector/study_areas.shp')

        if dem_path.exists() and study_areas_path.exists():
            study_areas = gpd.read_file(study_areas_path)

            # Calculate elevation statistics for each study area
            stats = zonal_stats(study_areas, str(dem_path),
                              stats=['min', 'max', 'mean', 'std'])

            print(f"✅ Zonal statistics calculation successful")
            for i, (area, stat) in enumerate(zip(study_areas.area_name, stats)):
                if stat['mean'] is not None:
                    print(f"   {area}: {stat['mean']:.1f}m avg elevation")

        return True

    except Exception as e:
        print(f"❌ Vector-raster integration test failed: {e}")
        return False


def create_sample_notebooks():
    """Create sample Jupyter notebooks for students."""
    print("\n📓 Creating sample notebooks...")

    notebooks = {
        '01_raster_basics.ipynb': '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Raster Basics with Rasterio\\n",
    "\\n",
    "This notebook demonstrates basic raster operations using the sample data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import rasterio\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "from pathlib import Path\\n",
    "\\n",
    "# Import your functions\\n",
    "from src.rasterio_analysis.raster_processing import analyze_local_raster\\n",
    "\\n",
    "print('Raster processing environment ready!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Test with sample DEM\\n",
    "dem_path = 'data/raster/phoenix_dem.tif'\\n",
    "\\n",
    "if Path(dem_path).exists():\\n",
    "    result = analyze_local_raster(dem_path)\\n",
    "    print(f\\"DEM Analysis Results:\\")\\n",
    "    print(f\\"Dimensions: {result['dimensions']}\\")\\n",
    "    print(f\\"Elevation range: {result['statistics']['min']:.1f} - {result['statistics']['max']:.1f}m\\")\\n",
    "else:\\n",
    "    print('Run setup_student_environment.py first to create sample data')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
''',

        '02_cog_processing.ipynb': '''
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Cloud-Optimized GeoTIFF Processing\\n",
    "\\n",
    "Learn to create and validate COGs for efficient raster processing."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from src.rasterio_analysis.cog_operations import create_optimized_cog, validate_cog\\n",
    "from pathlib import Path\\n",
    "\\n",
    "# Create a COG from sample DEM\\n",
    "input_path = 'data/raster/phoenix_dem.tif'\\n",
    "output_path = 'data/processed/phoenix_dem_cog.tif'\\n",
    "\\n",
    "if Path(input_path).exists():\\n",
    "    result = create_optimized_cog(input_path, output_path)\\n",
    "    print(f\\"COG created with {result['overview_count']} overviews\\")\\n",
    "    \\n",
    "    # Validate the COG\\n",
    "    validation = validate_cog(output_path)\\n",
    "    print(f\\"Valid COG: {validation['is_valid_cog']}\\")\\n",
    "else:\\n",
    "    print('Sample data not found. Run setup_student_environment.py first.')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.13.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
'''
    }

    try:
        for notebook_name, content in notebooks.items():
            notebook_path = Path('notebooks') / notebook_name
            with open(notebook_path, 'w') as f:
                f.write(content.strip())
            print(f"✅ Created: {notebook_path}")

        return True

    except Exception as e:
        print(f"❌ Failed to create notebooks: {e}")
        return False


def print_environment_summary(package_status: Dict[str, bool]):
    """Print a summary of the environment status."""
    print("\n" + "="*60)
    print("🎯 ENVIRONMENT SETUP SUMMARY")
    print("="*60)

    # Count package status
    total_packages = len(package_status)
    working_packages = sum(package_status.values())

    print(f"📦 Packages: {working_packages}/{total_packages} working")

    # Critical packages
    critical_packages = ['rasterio', 'numpy', 'geopandas', 'matplotlib']
    critical_working = sum(1 for pkg in critical_packages if package_status.get(pkg, False))

    if critical_working == len(critical_packages):
        print("✅ All critical packages working!")
    else:
        print(f"⚠️  {critical_working}/{len(critical_packages)} critical packages working")
        missing_critical = [pkg for pkg in critical_packages if not package_status.get(pkg, False)]
        print(f"   Missing critical: {', '.join(missing_critical)}")

    # Check data files
    data_files = [
        'data/raster/phoenix_dem.tif',
        'data/raster/phoenix_landsat.tif',
        'data/vector/sampling_points.shp'
    ]

    existing_files = [f for f in data_files if Path(f).exists()]
    print(f"📊 Sample data: {len(existing_files)}/{len(data_files)} files created")

    # Next steps
    print("\n🚀 NEXT STEPS:")

    if critical_working == len(critical_packages) and len(existing_files) >= 2:
        print("1. 📓 Open Jupyter Lab: uv run jupyter lab")
        print("2. 🧪 Start with notebooks/01_raster_basics.ipynb")
        print("3. 💻 Implement functions in src/rasterio_analysis/")
        print("4. 🧪 Run tests: uv run pytest tests/ -v")
        print("5. 📤 Push your code to GitHub for automated grading")
        print("\n✅ Your environment is ready for advanced raster processing!")
    else:
        print("1. 🔧 Fix missing packages with: uv sync")
        print("2. 🔄 Re-run this setup script")
        print("3. 💡 Consider using GitHub Codespaces if issues persist")
        print("\n⚠️  Environment needs attention before starting assignment")


def main():
    """Main setup function that orchestrates the environment setup."""
    print("🗺️" + "="*58)
    print("    Python Rasterio Advanced Processing - Environment Setup")
    print("    GIST 604B - Open Source GIS Programming")
    print("="*60)
    print()

    # Check if we're on Windows and warn about potential issues
    import platform
    if platform.system() == "Windows":
        print("⚠️  Windows detected. Consider using GitHub Codespaces")
        print("   for the best experience with geospatial libraries.")
        print()

    success_flags = []

    # Step 1: Check Python version
    success_flags.append(check_python_version())

    # Step 2: Check package installation
    package_status = check_required_packages()
    critical_packages = ['rasterio', 'numpy', 'geopandas', 'matplotlib']
    critical_working = all(package_status.get(pkg, False) for pkg in critical_packages)
    success_flags.append(critical_working)

    # Step 3: Create directory structure
    try:
        create_directory_structure()
        success_flags.append(True)
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        success_flags.append(False)

    # Step 4: Generate sample data (only if core packages work)
    if critical_working:
        print("\n📊 Generating sample datasets...")

        data_success = []
        data_success.append(generate_sample_dem_data())
        data_success.append(generate_sample_satellite_imagery())
        data_success.append(generate_sample_temperature_data())
        data_success.append(generate_sample_vector_data())

        success_flags.append(any(data_success))  # At least one dataset created

        # Step 5: Create sample notebooks
        success_flags.append(create_sample_notebooks())

        # Step 6: Test functionality
        if any(data_success):
            print("\n🔬 Testing raster processing capabilities...")
            success_flags.append(test_raster_operations())
            success_flags.append(test_vector_raster_integration())
    else:
        print("\n⚠️  Skipping data generation due to missing core packages")
        success_flags.extend([False, False, False, False])

    # Final summary
    print_environment_summary(package_status)

    # Return success status
    return all(success_flags)


if __name__ == "__main__":
    """Entry point for the setup script."""
    try:
        # Suppress warnings for cleaner output
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)

        success = main()

        if success:
            print("\n🎉 Setup completed successfully!")
            print("You're ready to start the advanced raster processing assignment.")
            sys.exit(0)
        else:
            print("\n⚠️  Setup completed with some issues.")
            print("Review the messages above and address any problems.")
            print("Consider using GitHub Codespaces for the best experience.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error during setup: {e}")
        print("Please check your Python environment and try again.")
        print("If problems persist, use GitHub Codespaces or contact your instructor.")
        sys.exit(1)
