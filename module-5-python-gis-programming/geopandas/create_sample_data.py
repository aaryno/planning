#!/usr/bin/env python3
"""
GIST 604B - Python GeoPandas Introduction
Sample Spatial Data Generator

This script creates realistic sample spatial datasets for the GeoPandas introduction
assignment. It generates cities, countries, and roads data with various spatial
data characteristics and some intentional quality issues for learning purposes.

Generated datasets include:
- World cities (points) - major cities with population data
- Country boundaries (polygons) - simplified country shapes
- Road networks (lines) - highway connections between cities
- Mixed quality data - datasets with validation challenges

Author: GIST 604B Course Team
Usage: python create_sample_data.py
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely import wkt
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def create_cities_data():
    """Create world cities point dataset with population data."""

    # Major world cities with realistic coordinates and population data
    cities_data = {
        'name': [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'London', 'Paris', 'Berlin', 'Madrid', 'Rome',
            'Tokyo', 'Seoul', 'Beijing', 'Shanghai', 'Mumbai',
            'São Paulo', 'Mexico City', 'Buenos Aires', 'Lima', 'Bogotá',
            'Cairo', 'Lagos', 'Johannesburg', 'Cape Town', 'Nairobi',
            'Sydney', 'Melbourne', 'Perth', 'Auckland', 'Wellington'
        ],
        'country': [
            'USA', 'USA', 'USA', 'USA', 'USA',
            'UK', 'France', 'Germany', 'Spain', 'Italy',
            'Japan', 'South Korea', 'China', 'China', 'India',
            'Brazil', 'Mexico', 'Argentina', 'Peru', 'Colombia',
            'Egypt', 'Nigeria', 'South Africa', 'South Africa', 'Kenya',
            'Australia', 'Australia', 'Australia', 'New Zealand', 'New Zealand'
        ],
        'continent': [
            'North America', 'North America', 'North America', 'North America', 'North America',
            'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
            'Asia', 'Asia', 'Asia', 'Asia', 'Asia',
            'South America', 'North America', 'South America', 'South America', 'South America',
            'Africa', 'Africa', 'Africa', 'Africa', 'Africa',
            'Oceania', 'Oceania', 'Oceania', 'Oceania', 'Oceania'
        ],
        'population': [
            8336817, 3979576, 2693976, 2320268, 1680992,
            8982000, 2161000, 3669491, 3223334, 2872800,
            13960000, 9776000, 21540000, 24870000, 12442373,
            12325232, 9209944, 2890151, 9752000, 7412566,
            9540000, 13463000, 4434827, 4618000, 4397073,
            5312163, 5078193, 2059484, 1695200, 418500
        ],
        'latitude': [
            40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
            51.5074, 48.8566, 52.5200, 40.4168, 41.9028,
            35.6762, 37.5665, 39.9042, 31.2304, 19.0760,
            -23.5505, 19.4326, -34.6037, -12.0464, 4.7110,
            30.0444, 6.5244, -26.2041, -33.9249, -1.2921,
            -33.8688, -37.8136, -31.9505, -36.8485, -41.2865
        ],
        'longitude': [
            -74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
            -0.1278, 2.3522, 13.4050, -3.7038, 12.4964,
            139.6503, 126.9780, 116.4074, 121.4737, 72.8777,
            -46.6333, -99.1332, -58.3816, -77.0428, -74.0721,
            31.2357, 3.3792, 28.0473, 18.4241, 36.8219,
            151.2093, 144.9631, 115.8605, 174.7633, 174.7762
        ]
    }

    # Create geometries from coordinates
    geometries = [Point(lon, lat) for lat, lon in zip(cities_data['latitude'], cities_data['longitude'])]

    # Create GeoDataFrame
    cities_gdf = gpd.GeoDataFrame(cities_data, geometry=geometries, crs='EPSG:4326')

    return cities_gdf


def create_cities_with_issues():
    """Create cities dataset with various spatial data quality issues."""

    # Start with clean cities data
    cities_clean = create_cities_data()

    # Create a subset with issues
    problem_cities = cities_clean.head(10).copy()

    # Introduce various issues:

    # 1. Missing geometry (row 2)
    problem_cities.loc[2, 'geometry'] = None

    # 2. Invalid coordinates - longitude out of range (row 4)
    problem_cities.loc[4, 'geometry'] = Point(190.0, 45.0)  # Invalid longitude

    # 3. Invalid coordinates - latitude out of range (row 5)
    problem_cities.loc[5, 'geometry'] = Point(-120.0, 95.0)  # Invalid latitude

    # 4. Empty geometry (row 7)
    problem_cities.loc[7, 'geometry'] = wkt.loads('POINT EMPTY')

    # 5. Remove CRS to create CRS issues
    problem_cities_no_crs = problem_cities.copy()
    problem_cities_no_crs.crs = None

    return problem_cities, problem_cities_no_crs


def create_countries_data():
    """Create simplified country polygons."""

    # Simplified country boundaries (very basic rectangles/polygons)
    countries_data = {
        'name': ['USA', 'Canada', 'Mexico', 'Brazil', 'Argentina',
                'UK', 'France', 'Germany', 'Spain', 'Italy',
                'Russia', 'China', 'India', 'Australia', 'Japan'],
        'continent': ['North America', 'North America', 'North America', 'South America', 'South America',
                     'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
                     'Asia/Europe', 'Asia', 'Asia', 'Oceania', 'Asia'],
        'area_km2': [9834000, 9985000, 1964000, 8515000, 2780000,
                    243000, 672000, 357000, 506000, 301000,
                    17100000, 9597000, 3287000, 7692000, 378000],
        'population': [331900000, 38000000, 128900000, 212600000, 45200000,
                      67900000, 67400000, 83200000, 47350000, 59550000,
                      145900000, 1440000000, 1380000000, 25700000, 125800000]
    }

    # Create simple bounding box polygons for countries (simplified)
    country_bounds = {
        'USA': (-125, 25, -66, 49),
        'Canada': (-140, 42, -53, 83),
        'Mexico': (-117, 14, -86, 32),
        'Brazil': (-74, -34, -35, 5),
        'Argentina': (-74, -55, -53, -22),
        'UK': (-8, 50, 2, 59),
        'France': (-5, 42, 8, 51),
        'Germany': (6, 47, 15, 55),
        'Spain': (-9, 36, 3, 44),
        'Italy': (7, 36, 18, 47),
        'Russia': (20, 42, 170, 82),
        'China': (74, 18, 135, 54),
        'India': (68, 7, 97, 37),
        'Australia': (113, -44, 154, -10),
        'Japan': (130, 31, 146, 46)
    }

    geometries = []
    for country in countries_data['name']:
        bounds = country_bounds[country]
        minx, miny, maxx, maxy = bounds

        # Create simple rectangle for each country
        polygon = Polygon([
            (minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)
        ])
        geometries.append(polygon)

    countries_gdf = gpd.GeoDataFrame(countries_data, geometry=geometries, crs='EPSG:4326')

    return countries_gdf


def create_roads_data():
    """Create highway/road network connecting major cities."""

    # Major highway connections (simplified)
    roads_data = {
        'highway_name': [
            'I-5 West Coast', 'I-10 Southern', 'I-95 East Coast',
            'Trans-Canada Highway', 'Pan-American Highway',
            'A1 Autostrada (Italy)', 'Autobahn A7 (Germany)',
            'M1 Motorway (UK)', 'A4 Autoroute (France)',
            'Tokyo-Osaka Expressway', 'Beijing-Shanghai Highway',
            'Pacific Highway (Australia)', 'State Highway 1 (NZ)'
        ],
        'country': [
            'USA', 'USA', 'USA', 'Canada', 'Multiple',
            'Italy', 'Germany', 'UK', 'France',
            'Japan', 'China', 'Australia', 'New Zealand'
        ],
        'highway_type': [
            'Interstate', 'Interstate', 'Interstate', 'Trans-National', 'International',
            'Autostrada', 'Autobahn', 'Motorway', 'Autoroute',
            'Expressway', 'National Highway', 'Highway', 'State Highway'
        ],
        'length_km': [
            2400, 3900, 3000, 7800, 48000,
            750, 960, 660, 580,
            350, 1200, 1000, 2000
        ]
    }

    # Create simple line geometries connecting major points
    road_coordinates = [
        # I-5 West Coast (LA to Seattle area)
        [(-118.2437, 34.0522), (-122.4194, 37.7749), (-122.3328, 47.6061)],
        # I-10 Southern (LA to Houston area)
        [(-118.2437, 34.0522), (-112.0740, 33.4484), (-95.3698, 29.7604)],
        # I-95 East Coast (Miami to Boston area)
        [(-80.1918, 25.7617), (-74.0060, 40.7128), (-71.0589, 42.3601)],
        # Trans-Canada Highway
        [(-123.1207, 49.2827), (-106.3468, 52.1579), (-75.6972, 45.4215)],
        # Pan-American Highway (Mexico to South America)
        [(-99.1332, 19.4326), (-84.0907, 9.9281), (-58.3816, -34.6037)],
        # Italy A1
        [(12.4964, 41.9028), (11.2558, 43.7696), (9.1900, 45.4642)],
        # German Autobahn A7
        [(9.9937, 53.5511), (11.5820, 48.1351)],
        # UK M1
        [(-0.1278, 51.5074), (-1.5491, 53.8008)],
        # French A4
        [(2.3522, 48.8566), (7.7521, 48.5734)],
        # Tokyo-Osaka
        [(139.6503, 35.6762), (135.5023, 34.6937)],
        # Beijing-Shanghai
        [(116.4074, 39.9042), (121.4737, 31.2304)],
        # Australian Pacific Highway
        [(151.2093, -33.8688), (153.0251, -27.4698)],
        # New Zealand SH1
        [(174.7633, -36.8485), (174.7762, -41.2865)]
    ]

    geometries = [LineString(coords) for coords in road_coordinates]

    roads_gdf = gpd.GeoDataFrame(roads_data, geometry=geometries, crs='EPSG:4326')

    return roads_gdf


def create_mixed_geometry_dataset():
    """Create a dataset with mixed geometry types for testing."""

    mixed_data = {
        'feature_name': [
            'Seattle Center', 'Portland Downtown', 'Vancouver Harbor',  # Points
            'I-5 Corridor', 'Columbia River', 'Fraser River',  # Lines
            'Washington State', 'Oregon State', 'British Columbia'  # Polygons
        ],
        'feature_type': [
            'Point of Interest', 'City Center', 'Port',
            'Highway', 'River', 'River',
            'State/Province', 'State/Province', 'Province'
        ],
        'country': [
            'USA', 'USA', 'Canada',
            'USA', 'USA/Canada', 'Canada',
            'USA', 'USA', 'Canada'
        ]
    }

    # Mixed geometries
    geometries = [
        # Points
        Point(-122.3328, 47.6061),  # Seattle
        Point(-122.6784, 45.5152),  # Portland
        Point(-123.1207, 49.2827),  # Vancouver

        # Lines
        LineString([(-122.3328, 47.6061), (-122.6784, 45.5152)]),  # I-5 segment
        LineString([(-121.7113, 45.3311), (-123.9351, 46.2619)]),  # Columbia River
        LineString([(-123.1207, 49.2827), (-121.9944, 50.2265)]),  # Fraser River

        # Polygons (simplified state/province boundaries)
        Polygon([(-124.7, 45.5), (-116.9, 45.5), (-116.9, 49.0), (-124.7, 49.0), (-124.7, 45.5)]),  # Washington
        Polygon([(-124.6, 42.0), (-116.5, 42.0), (-116.5, 46.3), (-124.6, 46.3), (-124.6, 42.0)]),  # Oregon
        Polygon([(-139.1, 48.3), (-114.0, 48.3), (-114.0, 60.0), (-139.1, 60.0), (-139.1, 48.3)])   # BC
    ]

    mixed_gdf = gpd.GeoDataFrame(mixed_data, geometry=geometries, crs='EPSG:4326')

    return mixed_gdf


def save_datasets():
    """Generate and save all sample datasets."""

    # Create data directory structure
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    cities_dir = data_dir / 'cities'
    countries_dir = data_dir / 'countries'
    roads_dir = data_dir / 'roads'

    cities_dir.mkdir(exist_ok=True)
    countries_dir.mkdir(exist_ok=True)
    roads_dir.mkdir(exist_ok=True)

    print("🌍 Generating sample spatial datasets...")

    # 1. Cities datasets
    print("  📍 Creating cities data...")
    cities = create_cities_data()
    cities_problems, cities_no_crs = create_cities_with_issues()

    # Save cities in multiple formats
    cities.to_file(cities_dir / 'world_cities.geojson', driver='GeoJSON')
    cities.to_file(cities_dir / 'world_cities.shp')
    cities_problems.to_file(cities_dir / 'cities_with_issues.geojson', driver='GeoJSON')
    cities_no_crs.to_file(cities_dir / 'cities_no_crs.geojson', driver='GeoJSON')

    # Save a small subset for quick testing
    cities.head(5).to_file(cities_dir / 'sample_cities.geojson', driver='GeoJSON')

    print(f"    ✅ Saved {len(cities)} cities to multiple formats")
    print(f"    ⚠️  Saved {len(cities_problems)} cities with data quality issues")

    # 2. Countries dataset
    print("  🗺️  Creating countries data...")
    countries = create_countries_data()
    countries.to_file(countries_dir / 'world_countries.geojson', driver='GeoJSON')
    countries.to_file(countries_dir / 'world_countries.shp')

    print(f"    ✅ Saved {len(countries)} country boundaries")

    # 3. Roads dataset
    print("  🛣️  Creating roads data...")
    roads = create_roads_data()
    roads.to_file(roads_dir / 'major_highways.geojson', driver='GeoJSON')
    roads.to_file(roads_dir / 'major_highways.shp')

    print(f"    ✅ Saved {len(roads)} highway segments")

    # 4. Mixed geometry dataset
    print("  🔀 Creating mixed geometry data...")
    mixed = create_mixed_geometry_dataset()
    mixed.to_file(data_dir / 'mixed_geometries.geojson', driver='GeoJSON')

    print(f"    ✅ Saved {len(mixed)} mixed geometry features")

    # 5. Create datasets with different CRS for testing
    print("  🗺️  Creating datasets with different projections...")

    # Web Mercator version of cities
    cities_web_mercator = cities.to_crs('EPSG:3857')
    cities_web_mercator.to_file(cities_dir / 'cities_web_mercator.geojson', driver='GeoJSON')

    # UTM version (for Pacific Northwest region)
    cities_utm = cities.to_crs('EPSG:32610')  # UTM Zone 10N
    cities_utm.to_file(cities_dir / 'cities_utm.geojson', driver='GeoJSON')

    print("    ✅ Created datasets in multiple coordinate systems")

    # 6. Create data documentation
    create_data_documentation(data_dir, cities, countries, roads, mixed)

    print("\n🎉 Sample spatial datasets created successfully!")
    print(f"📁 Data saved in: {data_dir.absolute()}")

    return data_dir


def create_data_documentation(data_dir, cities, countries, roads, mixed):
    """Create README documentation for the datasets."""

    readme_content = """# Sample Spatial Datasets

This directory contains realistic sample spatial datasets for learning GeoPandas fundamentals.

## 📂 Dataset Overview

### 🏙️ Cities Data (`cities/`)
- **world_cities.geojson/shp**: 30 major world cities with population data
- **sample_cities.geojson**: Subset of 5 cities for quick testing
- **cities_with_issues.geojson**: Cities with spatial data quality problems
- **cities_no_crs.geojson**: Cities without coordinate reference system
- **cities_web_mercator.geojson**: Cities in Web Mercator projection (EPSG:3857)
- **cities_utm.geojson**: Cities in UTM Zone 10N projection (EPSG:32610)

**Fields**: name, country, continent, population, latitude, longitude, geometry

### 🌍 Countries Data (`countries/`)
- **world_countries.geojson/shp**: 15 simplified country boundaries
- **Fields**: name, continent, area_km2, population, geometry

### 🛣️ Roads Data (`roads/`)
- **major_highways.geojson/shp**: 13 major highway segments worldwide
- **Fields**: highway_name, country, highway_type, length_km, geometry

### 🔀 Mixed Geometries (`mixed_geometries.geojson`)
- Points, lines, and polygons in one dataset
- **Fields**: feature_name, feature_type, country, geometry

## 🎯 Learning Objectives

These datasets are designed to help you practice:

1. **Loading Different Formats**: GeoJSON, Shapefile, multiple CRS
2. **Exploring Properties**: CRS, bounds, geometry types, attributes
3. **Data Quality Issues**: Missing geometries, invalid coordinates, CRS problems
4. **CRS Transformations**: Geographic, Web Mercator, UTM projections
5. **Mixed Geometry Types**: Points, lines, polygons in analysis

## 📊 Dataset Statistics

"""

    # Add statistics for each dataset
    stats = f"""
### Cities Dataset
- **Features**: {len(cities)}
- **Geometry Type**: Point
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Global coverage
- **Attributes**: Population, country, continent data

### Countries Dataset
- **Features**: {len(countries)}
- **Geometry Type**: Polygon
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Global coverage (simplified boundaries)
- **Attributes**: Area, population by country

### Roads Dataset
- **Features**: {len(roads)}
- **Geometry Type**: LineString
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Major highways across continents
- **Attributes**: Highway names, types, lengths

### Mixed Geometries Dataset
- **Features**: {len(mixed)}
- **Geometry Types**: Point, LineString, Polygon
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Pacific Northwest region
- **Attributes**: Feature names and types

## 🔧 Data Quality Notes

### Clean Data
Most datasets contain high-quality, valid spatial data suitable for analysis.

### Intentional Issues (for validation practice)
- **cities_with_issues.geojson**: Contains missing geometries, invalid coordinates
- **cities_no_crs.geojson**: Missing coordinate reference system
- These files help you practice data validation and cleaning

## 💡 Usage Examples

```python
import geopandas as gpd

# Load cities data
cities = gpd.read_file('data/cities/world_cities.geojson')
print(f"Loaded {{len(cities)}} cities")

# Load data with issues for validation practice
cities_with_issues = gpd.read_file('data/cities/cities_with_issues.geojson')
print(f"Dataset has valid geometries: {{cities_with_issues.geometry.is_valid.all()}}")

# Load different projections
cities_utm = gpd.read_file('data/cities/cities_utm.geojson')
print(f"UTM CRS: {{cities_utm.crs}}")
```

## 🗺️ Coordinate Reference Systems

- **EPSG:4326**: WGS84 geographic coordinates (longitude, latitude)
- **EPSG:3857**: Web Mercator projection (for web mapping)
- **EPSG:32610**: UTM Zone 10N (Pacific Northwest region)

---

*These datasets are created for educational purposes and use simplified geometries.
For production analysis, use authoritative spatial data sources.*
"""

    readme_content += stats

    # Write README file
    with open(data_dir / 'README.md', 'w') as f:
        f.write(readme_content)

    print("    📝 Created comprehensive data documentation")


if __name__ == '__main__':
    """Generate all sample spatial datasets."""
    try:
        data_directory = save_datasets()
        print(f"\n🚀 Ready for spatial analysis!")
        print(f"   Start with: jupyter notebook notebooks/01_spatial_data_overview.ipynb")
        print(f"   Test loading: python -c \"import geopandas as gpd; gdf = gpd.read_file('{data_directory}/cities/world_cities.geojson'); print('Loaded', len(gdf), 'cities successfully!')\"")

    except Exception as e:
        print(f"❌ Error creating datasets: {e}")
        print("   Make sure you have geopandas, shapely, and pandas installed")
        print("   Run: uv add geopandas shapely pandas")
