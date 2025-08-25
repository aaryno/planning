#!/usr/bin/env python3
"""
Create Sample Raster Data for Rasterio Tutorial
===============================================

This script creates sample raster datasets for students to use in their
Rasterio learning exercises. The data represents realistic geographic
features and satellite imagery for the Phoenix, Arizona area.

Run this script to populate the data/ directory with sample raster files.

Usage:
    python create_sample_data.py
"""

import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.enums import Resampling
from pathlib import Path
import json
import warnings
import tempfile
import os
from datetime import datetime, timezone

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="rasterio")

def create_data_directory():
    """Create the data directory structure if it doesn't exist"""
    base_dir = Path(__file__).parent

    # Create subdirectories for different data types
    directories = [
        'raster',
        'vector',  # For raster-vector integration exercises
        'processed',
        'cog'
    ]

    for dir_name in directories:
        (base_dir / dir_name).mkdir(exist_ok=True)

    return base_dir

def create_phoenix_dem():
    """Create a sample Digital Elevation Model for the Phoenix area."""
    print("🏔️  Creating Phoenix DEM...")

    # Define Phoenix area bounds (rough extent)
    bounds = (-112.5, 33.0, -111.5, 34.0)  # West, South, East, North
    width, height = 800, 600

    # Create coordinate grids
    x = np.linspace(bounds[0], bounds[2], width)
    y = np.linspace(bounds[1], bounds[3], height)
    X, Y = np.meshgrid(x, y)

    # Create realistic elevation data for Phoenix area
    # Phoenix sits in the Sonoran Desert with mountain ranges
    base_elevation = 1100  # Phoenix avg elevation in feet

    # Add mountain ranges (simplified)
    mountains = (
        200 * np.exp(-((X + 112.2)**2 + (Y - 33.7)**2) / 0.05) +  # South Mountain
        300 * np.exp(-((X + 112.0)**2 + (Y - 33.5)**2) / 0.03) +  # Camelback area
        150 * np.exp(-((X + 112.3)**2 + (Y - 33.2)**2) / 0.04)    # Sierra Estrella
    )

    # Add random terrain variation
    np.random.seed(42)  # For reproducible results
    terrain_noise = 30 * np.random.random((height, width))

    # Combine elevation components
    elevation = base_elevation + mountains + terrain_noise
    elevation = elevation.astype(np.float32)

    # Add some realistic nodata areas (water bodies, urban areas with no data)
    elevation[100:120, 200:250] = np.nan  # Salt River area
    elevation[400:420, 500:520] = np.nan  # Small lake

    # Create transform and profile
    transform = from_bounds(*bounds, width, height)
    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:4326',
        'transform': transform,
        'nodata': np.nan,
        'compress': 'lzw',
        'tiled': False  # Will be made into COG later
    }

    # Write DEM
    dem_path = Path('data/raster/phoenix_dem.tif')
    with rasterio.open(dem_path, 'w', **profile) as dst:
        dst.write(elevation, 1)

        # Add metadata
        dst.update_tags(
            AREA_OR_POINT='Point',
            TIFFTAG_IMAGEDESCRIPTION='Phoenix Area Digital Elevation Model - Sample Data',
            TIFFTAG_SOFTWARE='GIST 604B Sample Data Generator'
        )

    print(f"   ✅ Created DEM: {dem_path}")
    return dem_path

def create_landsat_like_imagery():
    """Create Landsat-like multispectral imagery."""
    print("🛰️  Creating Landsat-like imagery...")

    bounds = (-112.3, 33.2, -111.8, 33.7)  # Smaller area for imagery
    width, height = 500, 400
    bands = 6  # Blue, Green, Red, NIR, SWIR1, SWIR2

    # Set random seed for reproducible results
    np.random.seed(123)

    # Create realistic spectral signatures
    # Urban areas: higher reflectance in visible, lower in NIR
    # Vegetation: lower visible, higher NIR
    # Desert: moderate across all bands

    # Create base land cover pattern
    urban_mask = np.zeros((height, width))
    vegetation_mask = np.zeros((height, width))
    desert_mask = np.ones((height, width))

    # Urban areas (Phoenix metro)
    urban_centers = [
        (200, 250, 60),  # Downtown Phoenix area
        (150, 180, 40),  # Scottsdale area
        (300, 200, 30),  # Tempe area
    ]

    for x, y, size in urban_centers:
        xx, yy = np.ogrid[:height, :width]
        mask = (xx - y)**2 + (yy - x)**2 < size**2
        urban_mask[mask] = 1
        desert_mask[mask] = 0

    # Vegetation along rivers and parks
    vegetation_mask[150:170, :] = 1  # River corridor
    vegetation_mask[300:320, 100:200] = 1  # Large park area
    desert_mask[vegetation_mask > 0] = 0

    # Initialize bands array
    imagery = np.zeros((bands, height, width), dtype=np.uint16)

    # Band 1: Blue (0.45-0.52 μm)
    blue_urban = np.random.normal(1200, 200, (height, width))
    blue_veg = np.random.normal(800, 150, (height, width))
    blue_desert = np.random.normal(1000, 100, (height, width))
    imagery[0] = (blue_urban * urban_mask + blue_veg * vegetation_mask +
                  blue_desert * desert_mask).clip(0, 4000).astype(np.uint16)

    # Band 2: Green (0.52-0.60 μm)
    green_urban = np.random.normal(1400, 250, (height, width))
    green_veg = np.random.normal(1000, 200, (height, width))
    green_desert = np.random.normal(1200, 150, (height, width))
    imagery[1] = (green_urban * urban_mask + green_veg * vegetation_mask +
                  green_desert * desert_mask).clip(0, 4500).astype(np.uint16)

    # Band 3: Red (0.63-0.69 μm)
    red_urban = np.random.normal(1600, 300, (height, width))
    red_veg = np.random.normal(900, 200, (height, width))
    red_desert = np.random.normal(1400, 200, (height, width))
    imagery[2] = (red_urban * urban_mask + red_veg * vegetation_mask +
                  red_desert * desert_mask).clip(0, 5000).astype(np.uint16)

    # Band 4: NIR (0.77-0.90 μm) - vegetation shows up bright
    nir_urban = np.random.normal(2000, 300, (height, width))
    nir_veg = np.random.normal(3500, 500, (height, width))  # High NIR for vegetation
    nir_desert = np.random.normal(2200, 250, (height, width))
    imagery[3] = (nir_urban * urban_mask + nir_veg * vegetation_mask +
                  nir_desert * desert_mask).clip(0, 6000).astype(np.uint16)

    # Band 5: SWIR1 (1.55-1.75 μm)
    swir1_urban = np.random.normal(1800, 200, (height, width))
    swir1_veg = np.random.normal(1200, 300, (height, width))
    swir1_desert = np.random.normal(1600, 150, (height, width))
    imagery[4] = (swir1_urban * urban_mask + swir1_veg * vegetation_mask +
                  swir1_desert * desert_mask).clip(0, 4000).astype(np.uint16)

    # Band 6: SWIR2 (2.08-2.35 μm)
    swir2_urban = np.random.normal(1200, 150, (height, width))
    swir2_veg = np.random.normal(800, 200, (height, width))
    swir2_desert = np.random.normal(1100, 100, (height, width))
    imagery[5] = (swir2_urban * urban_mask + swir2_veg * vegetation_mask +
                  swir2_desert * desert_mask).clip(0, 3000).astype(np.uint16)

    # Add some clouds and shadows
    cloud_mask = np.zeros((height, width))
    cloud_mask[50:80, 200:280] = 1  # Cloud area
    shadow_mask = np.zeros((height, width))
    shadow_mask[85:115, 205:285] = 1  # Shadow area

    # Apply cloud and shadow effects
    for band in range(bands):
        imagery[band][cloud_mask > 0] = np.random.randint(4000, 6000,
                                                         size=np.sum(cloud_mask > 0))
        imagery[band][shadow_mask > 0] *= 0.3  # Darken shadows

    # Add nodata areas (could be outside scene boundary)
    nodata_value = 0
    imagery[:, :20, :] = nodata_value  # Top edge
    imagery[:, -20:, :] = nodata_value  # Bottom edge

    # Create transform and profile
    transform = from_bounds(*bounds, width, height)
    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': bands,
        'dtype': 'uint16',
        'crs': 'EPSG:32612',  # UTM Zone 12N (Arizona)
        'transform': transform,
        'nodata': nodata_value,
        'compress': 'lzw',
        'tiled': False
    }

    # Write multispectral imagery
    imagery_path = Path('data/raster/phoenix_landsat_2024.tif')
    with rasterio.open(imagery_path, 'w', **profile) as dst:
        for i in range(bands):
            dst.write(imagery[i], i + 1)

        # Set band descriptions
        band_names = ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2']
        for i, name in enumerate(band_names):
            dst.set_band_description(i + 1, name)

        # Add metadata
        dst.update_tags(
            SENSOR='Landsat-like simulation',
            DATE_ACQUIRED='2024-03-15',
            CLOUD_COVERAGE='15',
            SUN_ELEVATION='60.5',
            TIFFTAG_IMAGEDESCRIPTION='Phoenix Area Landsat-like Multispectral Imagery - Sample Data'
        )

    print(f"   ✅ Created Landsat imagery: {imagery_path}")
    return imagery_path

def create_temperature_raster():
    """Create a sample temperature raster for environmental analysis."""
    print("🌡️  Creating temperature raster...")

    bounds = (-112.4, 33.1, -111.6, 33.8)
    width, height = 400, 350

    # Create coordinate grids
    x = np.linspace(bounds[0], bounds[2], width)
    y = np.linspace(bounds[1], bounds[3], height)
    X, Y = np.meshgrid(x, y)

    # Create temperature pattern (higher in urban areas, lower in elevated areas)
    base_temp = 35.0  # Base temperature in Celsius (Phoenix summer)

    # Urban heat island effect
    urban_heat = 5 * np.exp(-((X + 112.0)**2 + (Y - 33.4)**2) / 0.02)

    # Elevation cooling (approximate)
    elevation_cooling = -0.006 * np.maximum(0,
        300 * np.exp(-((X + 112.2)**2 + (Y - 33.7)**2) / 0.05))  # Simplified elevation

    # Daily variation and random noise
    np.random.seed(456)
    daily_variation = 3 * np.sin(np.linspace(0, 2*np.pi, width*height)).reshape(height, width)
    noise = np.random.normal(0, 1, (height, width))

    # Combine temperature components
    temperature = base_temp + urban_heat + elevation_cooling + daily_variation + noise
    temperature = temperature.astype(np.float32)

    # Create profile
    transform = from_bounds(*bounds, width, height)
    profile = {
        'driver': 'GTiff',
        'width': width,
        'height': height,
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:4326',
        'transform': transform,
        'nodata': -9999.0,
        'compress': 'lzw'
    }

    # Write temperature data
    temp_path = Path('data/raster/phoenix_temperature_2024.tif')
    with rasterio.open(temp_path, 'w', **profile) as dst:
        dst.write(temperature, 1)
        dst.update_tags(
            UNITS='Celsius',
            PARAMETER='Air Temperature',
            DATE='2024-07-15T14:00:00Z',
            TIFFTAG_IMAGEDESCRIPTION='Phoenix Area Temperature Data - Sample Data'
        )

    print(f"   ✅ Created temperature raster: {temp_path}")
    return temp_path

def create_sample_vector_data():
    """Create sample vector data for raster-vector integration exercises."""
    print("📍 Creating vector sampling points...")

    try:
        import geopandas as gpd
        from shapely.geometry import Point, Polygon

        # Create sampling points
        np.random.seed(789)
        bounds = (-112.3, 33.2, -111.8, 33.7)

        # Generate random points within bounds
        n_points = 50
        lons = np.random.uniform(bounds[0], bounds[2], n_points)
        lats = np.random.uniform(bounds[1], bounds[3], n_points)

        points_gdf = gpd.GeoDataFrame({
            'point_id': range(1, n_points + 1),
            'type': np.random.choice(['urban', 'suburban', 'rural'], n_points),
            'elevation_est': np.random.uniform(1000, 1500, n_points).round(1),
            'geometry': [Point(lon, lat) for lon, lat in zip(lons, lats)]
        }, crs='EPSG:4326')

        # Save sampling points
        points_path = Path('data/vector/sampling_points.shp')
        points_gdf.to_file(points_path)
        print(f"   ✅ Created sampling points: {points_path}")

        # Create study area polygons
        study_areas = gpd.GeoDataFrame({
            'area_id': [1, 2, 3],
            'name': ['Downtown Phoenix', 'Scottsdale', 'Tempe'],
            'area_type': ['urban_core', 'suburban', 'mixed'],
            'geometry': [
                Polygon([(-112.1, 33.4), (-112.0, 33.4), (-112.0, 33.5), (-112.1, 33.5)]),
                Polygon([(-111.9, 33.5), (-111.8, 33.5), (-111.8, 33.6), (-111.9, 33.6)]),
                Polygon([(-111.95, 33.35), (-111.85, 33.35), (-111.85, 33.45), (-111.95, 33.45)])
            ]
        }, crs='EPSG:4326')

        study_areas_path = Path('data/vector/study_areas.shp')
        study_areas.to_file(study_areas_path)
        print(f"   ✅ Created study areas: {study_areas_path}")

        return True

    except ImportError:
        print("   ⚠️  GeoPandas not available - skipping vector data creation")
        return False

def create_sample_metadata():
    """Create sample metadata files for STAC integration testing."""
    print("📋 Creating sample metadata...")

    # STAC-like metadata for the imagery
    stac_metadata = {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": "phoenix_landsat_sample_2024",
        "properties": {
            "datetime": "2024-03-15T18:30:00Z",
            "title": "Phoenix Area Landsat-like Sample Imagery",
            "description": "Sample multispectral imagery for GIST 604B rasterio exercises",
            "instruments": ["sample_sensor"],
            "platform": "sample_satellite",
            "gsd": 30.0,
            "created": datetime.now(timezone.utc).isoformat(),
            "updated": datetime.now(timezone.utc).isoformat(),
            "eo:cloud_cover": 15.0,
            "eo:bands": [
                {"name": "blue", "common_name": "blue", "center_wavelength": 0.485, "full_width_half_max": 0.07},
                {"name": "green", "common_name": "green", "center_wavelength": 0.56, "full_width_half_max": 0.08},
                {"name": "red", "common_name": "red", "center_wavelength": 0.66, "full_width_half_max": 0.06},
                {"name": "nir", "common_name": "nir", "center_wavelength": 0.835, "full_width_half_max": 0.13},
                {"name": "swir16", "common_name": "swir16", "center_wavelength": 1.65, "full_width_half_max": 0.2},
                {"name": "swir22", "common_name": "swir22", "center_wavelength": 2.215, "full_width_half_max": 0.27}
            ]
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-112.3, 33.2],
                [-111.8, 33.2],
                [-111.8, 33.7],
                [-112.3, 33.7],
                [-112.3, 33.2]
            ]]
        },
        "bbox": [-112.3, 33.2, -111.8, 33.7],
        "assets": {
            "data": {
                "href": "./raster/phoenix_landsat_2024.tif",
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "title": "Multispectral imagery",
                "roles": ["data"],
                "eo:bands": [0, 1, 2, 3, 4, 5]
            }
        },
        "links": []
    }

    # Write STAC metadata
    metadata_path = Path('data/phoenix_sample_stac.json')
    with open(metadata_path, 'w') as f:
        json.dump(stac_metadata, f, indent=2)

    print(f"   ✅ Created STAC metadata: {metadata_path}")

    # Create data inventory
    inventory = {
        "created": datetime.now(timezone.utc).isoformat(),
        "description": "Sample raster datasets for GIST 604B Python Rasterio Assignment",
        "datasets": {
            "phoenix_dem.tif": {
                "type": "elevation",
                "bands": 1,
                "dtype": "float32",
                "units": "feet",
                "description": "Digital Elevation Model for Phoenix area"
            },
            "phoenix_landsat_2024.tif": {
                "type": "multispectral",
                "bands": 6,
                "dtype": "uint16",
                "units": "digital_numbers",
                "description": "Landsat-like multispectral imagery"
            },
            "phoenix_temperature_2024.tif": {
                "type": "environmental",
                "bands": 1,
                "dtype": "float32",
                "units": "celsius",
                "description": "Surface temperature data"
            }
        },
        "usage_notes": [
            "All datasets use realistic coordinate systems and bounds",
            "Nodata values are properly set for each dataset",
            "Data is suitable for COG optimization exercises",
            "Vector data available for integration exercises"
        ]
    }

    inventory_path = Path('data/data_inventory.json')
    with open(inventory_path, 'w') as f:
        json.dump(inventory, f, indent=2)

    print(f"   ✅ Created data inventory: {inventory_path}")
    return metadata_path, inventory_path

def create_readme():
    """Create README file explaining the sample datasets."""
    readme_content = """# Sample Raster Data for Rasterio Tutorial

This directory contains sample raster datasets for learning Rasterio and advanced raster processing techniques.

## Datasets

### 1. Phoenix DEM (`raster/phoenix_dem.tif`)
- **Type**: Digital Elevation Model
- **Extent**: Phoenix, Arizona metropolitan area
- **Resolution**: ~1km pixels
- **Data Type**: Float32
- **Units**: Feet above sea level
- **CRS**: EPSG:4326 (WGS84)
- **Nodata**: NaN (for water bodies)

**Use Cases**: Basic raster reading, statistics calculation, visualization

### 2. Landsat-like Imagery (`raster/phoenix_landsat_2024.tif`)
- **Type**: Multispectral satellite imagery simulation
- **Bands**: 6 (Blue, Green, Red, NIR, SWIR1, SWIR2)
- **Data Type**: UInt16
- **Units**: Digital Numbers (typical Landsat scaling)
- **CRS**: EPSG:32612 (UTM Zone 12N)
- **Nodata**: 0

**Use Cases**: Multiband processing, NDVI calculation, band math, COG creation

### 3. Temperature Data (`raster/phoenix_temperature_2024.tif`)
- **Type**: Environmental/Climate data
- **Data Type**: Float32
- **Units**: Degrees Celsius
- **CRS**: EPSG:4326
- **Nodata**: -9999

**Use Cases**: Environmental analysis, raster-vector integration, zonal statistics

### 4. Vector Integration Data (`vector/`)
- **sampling_points.shp**: Point locations for sampling raster values
- **study_areas.shp**: Polygon boundaries for zonal statistics

## Sample Workflows

### Basic Raster Analysis
```python
import rasterio
import numpy as np

# Read DEM
with rasterio.open('data/raster/phoenix_dem.tif') as src:
    elevation = src.read(1)
    profile = src.profile

# Calculate statistics
valid_data = elevation[~np.isnan(elevation)]
print(f"Mean elevation: {np.mean(valid_data):.1f} feet")
```

### NDVI Calculation
```python
with rasterio.open('data/raster/phoenix_landsat_2024.tif') as src:
    red = src.read(3).astype(float)    # Band 3
    nir = src.read(4).astype(float)    # Band 4

    # Calculate NDVI
    ndvi = (nir - red) / (nir + red)
    ndvi[np.isnan(ndvi) | np.isinf(ndvi)] = -1
```

### COG Creation
```python
from rio_cogeo.cogeo import cog_translate

cog_translate(
    'data/raster/phoenix_landsat_2024.tif',
    'data/cog/phoenix_landsat_cog.tif',
    profile='lzw',
    overview_resampling='average'
)
```

## Data Generation

This data was generated using the `create_sample_data.py` script and represents realistic but synthetic geographic features. The datasets are designed to:

- Provide meaningful examples for learning raster processing
- Include common edge cases (nodata values, different data types)
- Support multiple coordinate reference systems
- Enable realistic COG and STAC workflow exercises

## File Sizes

The sample datasets are intentionally kept small for educational use:
- DEM: ~2 MB
- Multispectral imagery: ~6 MB
- Temperature: ~1 MB
- Vector data: <1 MB

For production workflows, students will work with much larger datasets using the memory-efficient techniques learned in this course.

## Attribution

Sample data created for GIST 604B - Open Source GIS Programming
University of Arizona, School of Geography, Development & Environment
"""

    readme_path = Path('data/README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"   ✅ Created README: {readme_path}")
    return readme_path

def main():
    """Main function to create all sample datasets."""
    print("🌵 Creating Sample Raster Data for GIST 604B")
    print("=" * 50)

    try:
        # Create directory structure
        base_dir = create_data_directory()
        print(f"📁 Using data directory: {base_dir.absolute()}")

        # Create datasets
        datasets_created = []

        # Raster datasets
        datasets_created.append(create_phoenix_dem())
        datasets_created.append(create_landsat_like_imagery())
        datasets_created.append(create_temperature_raster())

        # Vector data (optional, for integration exercises)
        if create_sample_vector_data():
            print("   📍 Vector data created successfully")

        # Metadata and documentation
        metadata_files = create_sample_metadata()
        datasets_created.extend(metadata_files)
        datasets_created.append(create_readme())

        print("\n" + "=" * 50)
        print("✅ Sample data creation completed!")
        print(f"📊 Created {len(datasets_created)} files")
        print("\n📋 Next steps:")
        print("   1. Run 'python setup_student_environment.py' to validate environment")
        print("   2. Open Jupyter notebooks to start learning rasterio")
        print("   3. Try loading data with: rasterio.open('data/raster/phoenix_dem.tif')")

        return True

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        print("   Check that you have rasterio and numpy installed")
        print("   For vector integration: pip install geopandas")
        return False

if __name__ == "__main__":
    main()
