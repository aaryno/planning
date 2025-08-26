#!/usr/bin/env python3
"""
Quick Course Data Setup for GIST 604B Students
Download Arizona spatial datasets for GeoPandas spatial analysis exercises

Requirements: Python 3.13+ with uv package manager
Usage:
  1. uv init gis-analysis --python 3.13
  2. cd gis-analysis
  3. uv add "geopandas~=0.14.1" "matplotlib~=3.8.2"
  4. uv run python setup_course_data.py

This script creates sample Arizona GIS data for uv-managed projects.
Run this after initializing your uv project and adding dependencies.

Recommended uv project dependencies:
- geopandas~=0.14.1
- pandas~=2.1.4
- numpy~=1.26.2
- matplotlib~=3.8.2
- jupyter~=1.0.0
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import os
from pathlib import Path
from shapely.geometry import Point, Polygon

def create_pyproject_template():
    """Create a pyproject.toml template if none exists"""
    pyproject_path = Path('pyproject.toml')

    if not pyproject_path.exists():
        print("📝 Creating pyproject.toml template...")
        template = """[project]
name = "gis-analysis"
version = "0.1.0"
description = "GIST 604B Spatial Analysis Project"
requires-python = ">=3.13"
dependencies = [
    "geopandas~=0.14.1",
    "matplotlib~=3.8.2",
    "jupyter~=1.0.0",
    "contextily~=1.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest~=7.4.0",
    "black~=23.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""
        with open(pyproject_path, 'w') as f:
            f.write(template)
        print("   ✓ Created pyproject.toml template")
    else:
        print("   ✓ pyproject.toml already exists")

def setup_sample_data():
    """Create sample Arizona datasets for course exercises"""

    print("🗺️  Setting up Arizona GIS datasets for GIST 604B...")
    print("📦 For uv projects, ensure you have added:")
    print("   uv add \"geopandas~=0.14.1\"")
    print("   uv add \"matplotlib~=3.8.2\"")
    print("   uv add \"jupyter~=1.0.0\"")
    print()

    # Create pyproject.toml template if it doesn't exist
    create_pyproject_template()

    # Create data directory
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    # Set random seed for reproducible data
    np.random.seed(42)

    # 1. Create Phoenix area census tracts
    print("  📊 Creating census tracts...")
    phoenix_bounds = (-112.3, 33.2, -111.7, 33.7)  # Phoenix metro area
    tract_size = 0.08  # degrees (~5 miles)

    tracts = []
    tract_id = 1

    for x in np.arange(phoenix_bounds[0], phoenix_bounds[2], tract_size):
        for y in np.arange(phoenix_bounds[1], phoenix_bounds[3], tract_size):
            # Create square tract
            coords = [(x, y), (x + tract_size, y),
                     (x + tract_size, y + tract_size), (x, y + tract_size)]

            tracts.append({
                'tract_id': f'T{tract_id:03d}',
                'total_population': np.random.randint(2000, 8000),
                'median_income': np.random.randint(35000, 95000),
                'percent_poverty': round(np.random.uniform(8, 25), 1),
                'geometry': Polygon(coords)
            })
            tract_id += 1

    census_tracts = gpd.GeoDataFrame(tracts, crs='EPSG:4326')
    census_tracts.to_file(data_dir / 'phoenix_census_tracts.shp')

    # 2. Create schools within census tracts
    print("  🏫 Creating schools...")
    schools = []
    school_types = ['Elementary', 'Middle', 'High School']

    for idx, tract in census_tracts.iterrows():
        # 1-2 schools per tract based on population
        n_schools = 1 if tract['total_population'] < 4000 else 2

        for i in range(n_schools):
            # Random point within tract
            bounds = tract.geometry.bounds
            while True:
                x = np.random.uniform(bounds[0], bounds[2])
                y = np.random.uniform(bounds[1], bounds[3])
                point = Point(x, y)
                if tract.geometry.contains(point):
                    break

            schools.append({
                'school_id': f'SCH_{len(schools):03d}',
                'name': f'{np.random.choice(["Roosevelt", "Lincoln", "Washington", "Jefferson", "Adams", "Madison"])} {np.random.choice(school_types)}',
                'type': np.random.choice(school_types, p=[0.6, 0.25, 0.15]),
                'enrollment': np.random.randint(200, 1800),
                'district': f'District {np.random.randint(1, 6)}',
                'geometry': point
            })

    schools_gdf = gpd.GeoDataFrame(schools, crs='EPSG:4326')
    schools_gdf.to_file(data_dir / 'phoenix_schools.shp')

    # 3. Create business locations
    print("  🏢 Creating businesses...")
    business_types = ['Restaurant', 'Retail', 'Office', 'Medical', 'Service']
    businesses = []

    for i in range(150):
        lon = np.random.uniform(phoenix_bounds[0], phoenix_bounds[2])
        lat = np.random.uniform(phoenix_bounds[1], phoenix_bounds[3])
        biz_type = np.random.choice(business_types)

        businesses.append({
            'business_id': f'BIZ_{i:03d}',
            'name': f'{biz_type} {i+1}',
            'type': biz_type,
            'employees': np.random.randint(5, 100),
            'geometry': Point(lon, lat)
        })

    businesses_gdf = gpd.GeoDataFrame(businesses, crs='EPSG:4326')
    businesses_gdf.to_file(data_dir / 'phoenix_businesses.shp')

    # 4. Create parks
    print("  🌳 Creating parks...")
    parks = []

    for i in range(20):
        center_x = np.random.uniform(phoenix_bounds[0], phoenix_bounds[2])
        center_y = np.random.uniform(phoenix_bounds[1], phoenix_bounds[3])
        size = np.random.uniform(0.01, 0.04)  # Park size in degrees

        # Create square park
        coords = [(center_x - size/2, center_y - size/2),
                 (center_x + size/2, center_y - size/2),
                 (center_x + size/2, center_y + size/2),
                 (center_x - size/2, center_y + size/2)]

        parks.append({
            'park_id': f'PARK_{i:03d}',
            'name': f'{np.random.choice(["Sunset", "Desert", "Mountain", "Valley", "Cactus", "Phoenix"])} Park',
            'type': np.random.choice(['City Park', 'Regional Park', 'Community Park']),
            'area_acres': round(size * 6400, 1),  # Rough conversion to acres
            'geometry': Polygon(coords)
        })

    parks_gdf = gpd.GeoDataFrame(parks, crs='EPSG:4326')
    parks_gdf.to_file(data_dir / 'phoenix_parks.shp')

    # 5. Create ZIP codes (larger areas)
    print("  📮 Creating ZIP codes...")
    zip_size = 0.12  # degrees
    zip_codes = []
    zip_start = 85001

    zip_counter = 0
    for x in np.arange(phoenix_bounds[0], phoenix_bounds[2], zip_size):
        for y in np.arange(phoenix_bounds[1], phoenix_bounds[3], zip_size):
            coords = [(x, y), (x + zip_size, y),
                     (x + zip_size, y + zip_size), (x, y + zip_size)]

            zip_codes.append({
                'zip_code': str(zip_start + zip_counter),
                'neighborhood': f'District {zip_counter % 5 + 1}',
                'population': np.random.randint(15000, 40000),
                'geometry': Polygon(coords)
            })
            zip_counter += 1

    zip_codes_gdf = gpd.GeoDataFrame(zip_codes, crs='EPSG:4326')
    zip_codes_gdf.to_file(data_dir / 'phoenix_zip_codes.shp')

    # Create usage examples file
    print("  📝 Creating example code...")
    examples = """# GIST 604B Spatial Analysis Examples
# Example code using the course datasets
# Run with: uv run python examples.py

import geopandas as gpd
import matplotlib.pyplot as plt

# Load datasets
schools = gpd.read_file('data/phoenix_schools.shp')
census_tracts = gpd.read_file('data/phoenix_census_tracts.shp')
businesses = gpd.read_file('data/phoenix_businesses.shp')
parks = gpd.read_file('data/phoenix_parks.shp')
zip_codes = gpd.read_file('data/phoenix_zip_codes.shp')

print("📋 Package versions in use:")
print(f"   - Python: {__import__('sys').version}")
print(f"   - geopandas: {gpd.__version__}")
print(f"   - pandas: {__import__('pandas').__version__}")
print(f"   - numpy: {__import__('numpy').__version__}")

print("Datasets loaded successfully!")
print(f"Schools: {len(schools)} records")
print(f"Census tracts: {len(census_tracts)} records")
print(f"Businesses: {len(businesses)} records")
print(f"Parks: {len(parks)} records")
print(f"ZIP codes: {len(zip_codes)} records")

# Example 1: Spatial join - schools to census tracts
schools_with_demographics = gpd.sjoin(schools, census_tracts, predicate='within')
print(f"\\nSchools joined to census tracts: {len(schools_with_demographics)} matches")

# Example 2: Buffer analysis - businesses near parks
parks_buffer = parks.buffer(0.02)  # ~1 mile buffer
businesses_near_parks = gpd.sjoin(businesses, parks_buffer, predicate='within')
print(f"Businesses within 1 mile of parks: {len(businesses_near_parks)}")

# Example 3: Basic visualization
fig, ax = plt.subplots(figsize=(12, 8))
census_tracts.plot(ax=ax, color='lightblue', alpha=0.7, edgecolor='white')
schools.plot(ax=ax, color='red', markersize=20, alpha=0.8)
parks.plot(ax=ax, color='green', alpha=0.6)
ax.set_title('Phoenix Area: Schools, Census Tracts, and Parks')
plt.savefig('phoenix_overview_map.png', dpi=300, bbox_inches='tight')
plt.show()

# Example: Run Jupyter notebook
# uv run jupyter notebook
"""

    with open(data_dir / 'examples.py', 'w') as f:
        f.write(examples)

    # Create README
    readme = """# Course Data - Arizona GIS Examples

This directory contains spatial datasets for GIST 604B spatial analysis exercises.

## uv Project Setup:
If you haven't already, set up your uv project:
```bash
uv init gis-analysis --python 3.13
cd gis-analysis
uv add "geopandas~=0.14.1" "matplotlib~=3.8.2" "jupyter~=1.0.0"
```

## Files Created:
- `phoenix_census_tracts.shp` - Census tract boundaries with demographic data
- `phoenix_schools.shp` - School locations with enrollment info
- `phoenix_businesses.shp` - Business locations by type
- `phoenix_parks.shp` - Park boundaries and information
- `phoenix_zip_codes.shp` - ZIP code boundaries
- `examples.py` - Sample code to get you started

## Quick Start:
```bash
# Run Python in uv environment
uv run python -c "
import geopandas as gpd
schools = gpd.read_file('data/phoenix_schools.shp')
schools.plot()
print(f'Loaded {len(schools)} schools')
"

# Or run example script
uv run python data/examples.py

# Start Jupyter notebook
uv run jupyter notebook
```

All datasets use WGS84 (EPSG:4326) coordinate system.
Data is synthetic and created for educational purposes.
"""

    with open(data_dir / 'README.md', 'w') as f:
        f.write(readme)

    print("✅ Course data setup complete!")
    print(f"📁 Created {len(list(data_dir.glob('*.shp')))} shapefiles in 'data/' directory")
    print("🚀 Test your setup with: uv run python data/examples.py")
    print("\n💡 If missing packages, add them with:")
    print("   uv add \"geopandas~=0.14.1\" \"matplotlib~=3.8.2\" \"jupyter~=1.0.0\"")
    print("\n📚 Datasets ready for spatial analysis exercises!")

def main():
    """Main function"""
    try:
        setup_sample_data()
    except Exception as e:
        print(f"\n❌ Error setting up data: {e}")
        print("💡 Ensure you have a uv project with required packages:")
        print("   uv init gis-analysis --python 3.13")
        print("   cd gis-analysis")
        print("   uv add \"geopandas~=0.14.1\" \"matplotlib~=3.8.2\" \"jupyter~=1.0.0\"")
        print("   uv run python setup_course_data.py")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
