#!/usr/bin/env python3
"""
Course Data Preparation Script for GIST 604B Module 5
Spatial Analysis with GeoPandas and Pandas

This script downloads and prepares Arizona spatial datasets for course examples.
Creates clean, small-scale datasets with known spatial relationships for
predictable educational outcomes. Generates uv-compatible project structure
with Python 3.13 support and version-pinned dependencies.

Requirements: Python 3.13+, uv package manager
Author: Course Development Team
License: Educational Use
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import zipfile
import os
from pathlib import Path
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CourseDataPreparator:
    """Prepare Arizona spatial datasets for GIST 604B course examples with uv project structure"""

    def __init__(self, output_dir='gis-course-data'):
        """Initialize with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"Output directory: {self.output_dir.absolute()}")

    def download_census_boundaries(self):
        """Download and prepare Census administrative boundaries"""
        logger.info("Downloading Census administrative boundaries...")

        try:
            # Arizona counties
            counties_url = "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip"
            counties = gpd.read_file(counties_url)
            az_counties = counties[counties.STATEFP == '04'].copy()  # Arizona FIPS code

            # Clean up county data
            az_counties = az_counties[['GEOID', 'NAME', 'geometry']].rename(columns={
                'GEOID': 'county_id',
                'NAME': 'county_name'
            })

            # Add sample demographic data
            np.random.seed(42)
            az_counties['total_population'] = np.random.randint(50000, 2500000, len(az_counties))
            az_counties['median_income'] = np.random.randint(35000, 85000, len(az_counties))

            az_counties.to_file(self.output_dir / 'arizona_counties.shp')
            logger.info(f"Saved {len(az_counties)} Arizona counties")

            # Census tracts for Phoenix metro area (Maricopa County)
            tracts_url = "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_04_tract_500k.zip"
            tracts = gpd.read_file(tracts_url)
            maricopa_tracts = tracts[tracts.COUNTYFP == '013'].copy()  # Maricopa County

            # Clean up tract data
            maricopa_tracts = maricopa_tracts[['GEOID', 'geometry']].rename(columns={
                'GEOID': 'tract_id'
            })

            # Add realistic demographic data
            maricopa_tracts['total_population'] = np.random.randint(1000, 8000, len(maricopa_tracts))
            maricopa_tracts['median_income'] = np.random.randint(25000, 120000, len(maricopa_tracts))
            maricopa_tracts['percent_poverty'] = np.random.uniform(5, 35, len(maricopa_tracts))
            maricopa_tracts['housing_units'] = (maricopa_tracts['total_population'] /
                                              np.random.uniform(2.2, 3.1, len(maricopa_tracts))).astype(int)

            maricopa_tracts.to_file(self.output_dir / 'phoenix_census_tracts.shp')
            logger.info(f"Saved {len(maricopa_tracts)} Phoenix area census tracts")

            return az_counties, maricopa_tracts

        except Exception as e:
            logger.error(f"Error downloading census boundaries: {e}")
            return None, None

    def create_sample_schools(self, census_tracts=None):
        """Create sample school locations with realistic distribution"""
        logger.info("Creating sample school locations...")

        if census_tracts is not None:
            # Distribute schools within census tract boundaries
            schools_data = []

            for idx, tract in census_tracts.iterrows():
                # Number of schools roughly proportional to population
                n_schools = max(1, int(tract['total_population'] / 4000))

                # Generate random points within tract boundary
                bounds = tract.geometry.bounds
                for i in range(n_schools):
                    while True:
                        x = np.random.uniform(bounds[0], bounds[2])
                        y = np.random.uniform(bounds[1], bounds[3])
                        point = Point(x, y)
                        if tract.geometry.contains(point):
                            break

                    schools_data.append({
                        'school_id': f"SCH_{len(schools_data):03d}",
                        'name': f"School {len(schools_data) + 1}",
                        'type': np.random.choice(['Elementary', 'Middle', 'High'],
                                               p=[0.6, 0.25, 0.15]),
                        'enrollment': np.random.randint(150, 2000),
                        'district_id': f"DIST_{int(tract['tract_id'][-3:]) // 10}",
                        'geometry': point
                    })
        else:
            # Create schools for Phoenix metro area if no census tracts provided
            phoenix_bounds = (-112.5, 33.0, -111.5, 33.8)
            schools_data = []

            np.random.seed(42)
            n_schools = 75

            for i in range(n_schools):
                lon = np.random.uniform(phoenix_bounds[0], phoenix_bounds[2])
                lat = np.random.uniform(phoenix_bounds[1], phoenix_bounds[3])

                schools_data.append({
                    'school_id': f"SCH_{i:03d}",
                    'name': f"School {i + 1}",
                    'type': np.random.choice(['Elementary', 'Middle', 'High'],
                                           p=[0.6, 0.25, 0.15]),
                    'enrollment': np.random.randint(150, 2000),
                    'district_id': f"DIST_{i // 10}",
                    'geometry': Point(lon, lat)
                })

        schools = gpd.GeoDataFrame(schools_data, crs='EPSG:4326')
        schools.to_file(self.output_dir / 'arizona_schools.shp')
        logger.info(f"Created {len(schools)} sample schools")

        return schools

    def create_sample_businesses(self):
        """Create sample business/POI locations"""
        logger.info("Creating sample business locations...")

        # Phoenix metro area
        phoenix_bounds = (-112.5, 33.0, -111.5, 33.8)
        business_types = ['Restaurant', 'Retail', 'Office', 'Healthcare', 'Service']

        np.random.seed(123)
        n_businesses = 200

        businesses_data = []
        for i in range(n_businesses):
            lon = np.random.uniform(phoenix_bounds[0], phoenix_bounds[2])
            lat = np.random.uniform(phoenix_bounds[1], phoenix_bounds[3])
            business_type = np.random.choice(business_types)

            businesses_data.append({
                'business_id': f"BIZ_{i:03d}",
                'name': f"{business_type} {i + 1}",
                'type': business_type,
                'employees': np.random.randint(1, 150),
                'annual_revenue': np.random.randint(100000, 5000000),
                'geometry': Point(lon, lat)
            })

        businesses = gpd.GeoDataFrame(businesses_data, crs='EPSG:4326')
        businesses.to_file(self.output_dir / 'arizona_businesses.shp')
        logger.info(f"Created {len(businesses)} sample businesses")

        return businesses

    def create_transportation_network(self):
        """Create simplified transportation network"""
        logger.info("Creating transportation network...")

        # Major highways through Phoenix area
        highway_coords = [
            # I-10 (east-west)
            [(-112.4, 33.45), (-111.6, 33.45)],
            # I-17 (north-south)
            [(-112.08, 33.2), (-112.08, 33.7)],
            # Loop 101 (partial)
            [(-112.3, 33.6), (-111.8, 33.6), (-111.8, 33.2), (-112.1, 33.2)],
            # US-60 (diagonal)
            [(-112.3, 33.3), (-111.7, 33.5)]
        ]

        highways_data = []
        for i, coords in enumerate(highway_coords):
            line = LineString(coords)
            highways_data.append({
                'highway_id': f"HWY_{i:02d}",
                'name': ['I-10', 'I-17', 'Loop 101', 'US-60'][i],
                'type': 'Interstate' if i < 2 else 'Highway',
                'lanes': np.random.randint(4, 8),
                'geometry': line
            })

        highways = gpd.GeoDataFrame(highways_data, crs='EPSG:4326')
        highways.to_file(self.output_dir / 'arizona_highways.shp')
        logger.info(f"Created {len(highways)} highway segments")

        return highways

    def create_parks_recreation(self):
        """Create parks and recreation areas"""
        logger.info("Creating parks and recreation areas...")

        phoenix_bounds = (-112.5, 33.0, -111.5, 33.8)

        np.random.seed(456)
        n_parks = 30

        parks_data = []
        for i in range(n_parks):
            # Create random polygon for park
            center_lon = np.random.uniform(phoenix_bounds[0], phoenix_bounds[2])
            center_lat = np.random.uniform(phoenix_bounds[1], phoenix_bounds[3])

            # Create square park with random size
            size = np.random.uniform(0.005, 0.03)  # degrees
            park_coords = [
                (center_lon - size/2, center_lat - size/2),
                (center_lon + size/2, center_lat - size/2),
                (center_lon + size/2, center_lat + size/2),
                (center_lon - size/2, center_lat + size/2)
            ]

            parks_data.append({
                'park_id': f"PARK_{i:03d}",
                'name': f"Park {i + 1}",
                'type': np.random.choice(['City Park', 'Regional Park', 'Neighborhood Park']),
                'area_acres': size * 111000 * 111000 * 0.000247105,  # rough conversion
                'facilities': np.random.choice(['Playground', 'Sports Fields', 'Trails', 'Pool']),
                'geometry': Polygon(park_coords)
            })

        parks = gpd.GeoDataFrame(parks_data, crs='EPSG:4326')
        parks.to_file(self.output_dir / 'arizona_parks.shp')
        logger.info(f"Created {len(parks)} parks")

        return parks

    def create_zip_codes(self, counties=None):
        """Create simplified ZIP code boundaries"""
        logger.info("Creating ZIP code boundaries...")

        if counties is not None:
            # Use Maricopa County bounds
            maricopa = counties[counties.county_name == 'Maricopa']
            if not maricopa.empty:
                bounds = maricopa.total_bounds
            else:
                bounds = [-112.5, 33.0, -111.5, 33.8]
        else:
            bounds = [-112.5, 33.0, -111.5, 33.8]  # Phoenix metro default

        # Create grid of ZIP code areas
        zip_size = 0.15  # degrees
        zip_codes_data = []
        zip_counter = 85001

        x_coords = np.arange(bounds[0], bounds[2], zip_size)
        y_coords = np.arange(bounds[1], bounds[3], zip_size)

        for x in x_coords:
            for y in y_coords:
                zip_coords = [
                    (x, y), (x + zip_size, y),
                    (x + zip_size, y + zip_size), (x, y + zip_size)
                ]

                zip_codes_data.append({
                    'zip_code': str(zip_counter),
                    'city': 'Phoenix' if zip_counter % 3 == 0 else 'Scottsdale',
                    'population': np.random.randint(15000, 45000),
                    'geometry': Polygon(zip_coords)
                })
                zip_counter += 1

        zip_codes = gpd.GeoDataFrame(zip_codes_data, crs='EPSG:4326')
        zip_codes.to_file(self.output_dir / 'arizona_zip_codes.shp')
        logger.info(f"Created {len(zip_codes)} ZIP code areas")

        return zip_codes

    def create_uv_project_files(self):
        """Create uv project configuration files"""
        logger.info("Creating uv project configuration...")

        # Create pyproject.toml
        pyproject_content = """[project]
name = "gist-604b-course-data"
version = "1.0.0"
description = "Arizona spatial datasets for GIST 604B spatial analysis"
requires-python = ">=3.13"
dependencies = [
    "geopandas~=0.14.1",
    "matplotlib~=3.8.2",
    "contextily~=1.4.0",
    "jupyter~=1.0.0",
    "pandas~=2.1.4",
    "numpy~=1.26.2",
]

[project.optional-dependencies]
dev = [
    "pytest~=7.4.0",
    "black~=23.0.0",
    "ruff~=0.1.8",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 88
target-version = ['py313']

[tool.ruff]
target-version = "py313"
line-length = 88
"""

        with open(self.output_dir / 'pyproject.toml', 'w') as f:
            f.write(pyproject_content)

        logger.info("Created pyproject.toml")

    def create_README(self):
        """Create documentation for the datasets"""
        readme_content = """# GIST 604B Course Data - Arizona Spatial Analysis Examples

This directory contains spatial datasets for Module 5: Python GIS Programming.
All datasets are created for educational purposes and contain synthetic data
where appropriate. This is a complete uv project ready for spatial analysis.

## Quick Start with uv

### Setup Project Environment
```bash
# Clone or download this project directory
cd gis-course-data

# Install dependencies with uv (Python 3.13+)
uv sync

# Verify installation
uv run python -c "import geopandas as gpd; print(f'GeoPandas {gpd.__version__} ready!')"

# Start Jupyter notebook
uv run jupyter notebook
```

### Alternative Setup
```bash
# Create new project based on this template
uv init my-gis-analysis --python 3.13
cd my-gis-analysis

# Add the same dependencies
uv add "geopandas~=0.14.1" "matplotlib~=3.8.2" "contextily~=1.4.0" "jupyter~=1.0.0"

# Copy data files to your project
cp -r ../gis-course-data/data/ ./
```

## Datasets Overview

### Administrative Boundaries
- `data/arizona_counties.shp` - Arizona county boundaries with population data
- `data/phoenix_census_tracts.shp` - Census tracts for Phoenix metro (Maricopa County)
- `data/arizona_zip_codes.shp` - ZIP code boundaries for Phoenix area

### Points of Interest
- `data/arizona_schools.shp` - Sample school locations with enrollment data
- `data/arizona_businesses.shp` - Sample business locations with type and size info

### Infrastructure
- `data/arizona_highways.shp` - Major highway network for Phoenix area
- `data/arizona_parks.shp` - Parks and recreation areas

## Data Sources
- Census boundaries: U.S. Census Bureau TIGER/Line files
- Sample points: Generated for educational purposes
- Demographic data: Simulated realistic values

## Coordinate Reference System
All datasets use WGS84 (EPSG:4326) for consistency.

## Usage Examples

### Basic Spatial Join
```python
# Run with: uv run python analysis.py
import geopandas as gpd

schools = gpd.read_file('data/arizona_schools.shp')
census_tracts = gpd.read_file('data/phoenix_census_tracts.shp')

# Find which census tract contains each school
schools_with_demographics = gpd.sjoin(schools, census_tracts, predicate='within')
```

### Multi-dataset Analysis
```python
# Find schools within 1 mile of highways
highways = gpd.read_file('data/arizona_highways.shp')
highway_buffer = highways.buffer(0.01)  # ~1 mile in degrees
schools_near_highways = gpd.sjoin(schools, highway_buffer, predicate='within')
```

### Interactive Analysis
```python
# Start interactive session
# uv run python -i
import geopandas as gpd
import matplotlib.pyplot as plt

# Load and visualize data
schools = gpd.read_file('data/arizona_schools.shv')
schools.plot()
plt.show()
```

## Project Structure
```
gis-course-data/
├── pyproject.toml      # uv project configuration
├── uv.lock            # Locked dependencies (created after uv sync)
├── data/              # Spatial datasets
│   ├── *.shp          # Shapefiles with supporting files
│   └── examples.py    # Sample analysis code
├── README.md          # This file
└── analysis/          # Create your analysis scripts here
```

## System Requirements
- Python 3.13+
- uv package manager
- ~50MB disk space for datasets

## File Sizes
Each dataset is kept under 5MB for efficient use in cloud environments.

## Version Information
All dependencies are version-pinned for reproducible analysis:
- geopandas~=0.14.1 (compatible with Shapely 2.0+)
- matplotlib~=3.8.2 (Python 3.13 compatible)
- pandas~=2.1.4 (latest stable with NumPy 1.26+)

## Created by
GIST 604B Course Development Team
University of Arizona

## License
Educational Use - datasets created for teaching purposes
"""

        with open(self.output_dir / 'README.md', 'w') as f:
            f.write(readme_content)

        logger.info("Created README.md documentation")

    def run_all(self):
        """Execute complete data preparation workflow with uv project setup"""
        logger.info("Starting complete data preparation workflow...")

        # Create uv project structure first
        self.create_uv_project_files()

        # Create data subdirectory
        data_dir = self.output_dir / 'data'
        data_dir.mkdir(exist_ok=True)

        # Temporarily change output to data subdirectory for dataset creation
        original_output = self.output_dir
        self.output_dir = data_dir

        try:
            # Download real census data
            counties, census_tracts = self.download_census_boundaries()

            # Create sample datasets
            schools = self.create_sample_schools(census_tracts)
            businesses = self.create_sample_businesses()
            highways = self.create_transportation_network()
            parks = self.create_parks_recreation()
            zip_codes = self.create_zip_codes(counties)

        finally:
            # Restore original output directory
            self.output_dir = original_output

        # Create project documentation
        self.create_README()

        # Create example analysis script
        analysis_dir = self.output_dir / 'analysis'
        analysis_dir.mkdir(exist_ok=True)

        example_script = """#!/usr/bin/env python3
\"\"\"
Example spatial analysis script for GIST 604B course data
Run with: uv run python analysis/example_analysis.py
\"\"\"

import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    \"\"\"Run example spatial analysis\"\"\"
    print("🗺️  GIST 604B Example Spatial Analysis")

    # Load datasets
    data_dir = Path('data')
    schools = gpd.read_file(data_dir / 'arizona_schools.shp')
    census_tracts = gpd.read_file(data_dir / 'phoenix_census_tracts.shp')

    print(f"Loaded {len(schools)} schools and {len(census_tracts)} census tracts")

    # Spatial join example
    schools_with_tracts = gpd.sjoin(schools, census_tracts, predicate='within')
    print(f"Spatial join result: {len(schools_with_tracts)} schools matched to census tracts")

    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    census_tracts.plot(ax=ax, color='lightblue', alpha=0.7, edgecolor='white')
    schools.plot(ax=ax, color='red', markersize=20, alpha=0.8)
    ax.set_title('Phoenix Area: Schools and Census Tracts')
    plt.savefig('phoenix_example_map.png', dpi=300, bbox_inches='tight')
    print("📊 Map saved as 'phoenix_example_map.png'")

    print("✅ Example analysis complete!")

if __name__ == "__main__":
    main()
"""

        with open(analysis_dir / 'example_analysis.py', 'w') as f:
            f.write(example_script)

        # Summary report
        logger.info("\n" + "="*50)
        logger.info("UV PROJECT PREPARATION COMPLETE")
        logger.info("="*50)
        logger.info(f"Project directory: {self.output_dir.absolute()}")

        # List all created files
        data_files = list((self.output_dir / 'data').glob('*.shp'))
        logger.info(f"\nCreated {len(data_files)} shapefiles in data/ directory:")
        for shp_file in sorted(data_files):
            gdf = gpd.read_file(shp_file)
            logger.info(f"  {shp_file.name}: {len(gdf)} features")

        # List project files
        project_files = ['pyproject.toml', 'README.md']
        logger.info(f"\nProject files created:")
        for proj_file in project_files:
            if (self.output_dir / proj_file).exists():
                logger.info(f"  {proj_file}")

        logger.info(f"\nTotal disk usage: {sum(f.stat().st_size for f in self.output_dir.rglob('*') if f.is_file()) / 1024 / 1024:.1f} MB")
        logger.info("\n🚀 uv project ready for course use!")
        logger.info(f"Next steps:")
        logger.info(f"  cd {self.output_dir.name}")
        logger.info(f"  uv sync")
        logger.info(f"  uv run jupyter notebook")

def main():
    """Main execution function"""
    print("GIST 604B Course Data Preparation with uv")
    print("Creating Arizona spatial datasets for GeoPandas examples...\n")
    print("Requirements: Python 3.13+, uv package manager\n")

    # Initialize data preparator
    preparator = CourseDataPreparator()

    # Run complete workflow
    try:
        preparator.run_all()
        print("\n✓ uv project preparation completed successfully!")
        print(f"📁 Project created in: {preparator.output_dir.absolute()}")
        print("\n🚀 To use the project:")
        print(f"   cd {preparator.output_dir.name}")
        print("   uv sync")
        print("   uv run python analysis/example_analysis.py")
        print("   uv run jupyter notebook")

    except Exception as e:
        logger.error(f"Data preparation failed: {e}")
        print(f"\n✗ Error: {e}")
        print("\n💡 Requirements:")
        print("   - Python 3.13+")
        print("   - uv package manager (curl -LsSf https://astral.sh/uv/install.sh | sh)")
        print("   - Internet connection for downloading Census data")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
