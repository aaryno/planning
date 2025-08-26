"""
Sample Data Creation Script for Python GeoPandas Analysis Assignment

This script creates sample spatial datasets for testing the GeoPandas analysis functions.
It generates realistic spatial data that students can use to test their implementations.

GIST 604B - Open Source GIS Programming
Module 5: Python GIS Programming
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon, LineString
from pathlib import Path
import numpy as np

def create_sample_data():
    """Create sample spatial datasets for the assignment."""

    print("🗺️ Creating sample spatial datasets...")

    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    # =========================================================================
    # 1. CITIES (Points) - Major California cities
    # =========================================================================

    cities_data = {
        'city_name': [
            'San Francisco', 'Los Angeles', 'San Diego', 'Sacramento', 'San Jose',
            'Oakland', 'Fresno', 'Long Beach', 'Santa Ana', 'Riverside'
        ],
        'population': [
            883305, 3979576, 1423851, 513624, 1021795,
            433031, 542107, 462628, 334136, 330063
        ],
        'county': [
            'San Francisco', 'Los Angeles', 'San Diego', 'Sacramento', 'Santa Clara',
            'Alameda', 'Fresno', 'Los Angeles', 'Orange', 'Riverside'
        ],
        'founded_year': [
            1776, 1781, 1769, 1848, 1777,
            1852, 1872, 1897, 1886, 1883
        ],
        'geometry': [
            Point(-122.4194, 37.7749),   # San Francisco
            Point(-118.2437, 34.0522),   # Los Angeles
            Point(-117.1611, 32.7157),   # San Diego
            Point(-121.4944, 38.5816),   # Sacramento
            Point(-121.8863, 37.3382),   # San Jose
            Point(-122.2711, 37.8044),   # Oakland
            Point(-119.7871, 36.7378),   # Fresno
            Point(-118.1937, 33.7701),   # Long Beach
            Point(-117.8677, 33.7455),   # Santa Ana
            Point(-117.3961, 33.9533)    # Riverside
        ]
    }

    cities_gdf = gpd.GeoDataFrame(cities_data, crs='EPSG:4326')
    cities_gdf.to_file(data_dir / 'cities.geojson', driver='GeoJSON')
    print(f"  ✅ Created cities.geojson with {len(cities_gdf)} cities")

    # =========================================================================
    # 2. WATERSHEDS (Polygons) - Simplified California watershed boundaries
    # =========================================================================

    watersheds = []
    watershed_names = []
    watershed_areas = []
    watershed_types = []

    # San Francisco Bay Area watersheds
    sf_bay_watershed = Polygon([
        (-122.8, 37.2), (-122.8, 38.2), (-121.8, 38.2),
        (-121.8, 37.2), (-122.8, 37.2)
    ])
    watersheds.append(sf_bay_watershed)
    watershed_names.append('San Francisco Bay')
    watershed_areas.append(4500.0)
    watershed_types.append('coastal')

    # Central Valley watershed
    central_valley_watershed = Polygon([
        (-122.0, 36.0), (-122.0, 39.0), (-119.0, 39.0),
        (-119.0, 36.0), (-122.0, 36.0)
    ])
    watersheds.append(central_valley_watershed)
    watershed_names.append('Central Valley')
    watershed_areas.append(52000.0)
    watershed_types.append('interior')

    # Los Angeles Basin watershed
    la_watershed = Polygon([
        (-119.0, 33.5), (-119.0, 34.8), (-117.5, 34.8),
        (-117.5, 33.5), (-119.0, 33.5)
    ])
    watersheds.append(la_watershed)
    watershed_names.append('Los Angeles Basin')
    watershed_areas.append(2100.0)
    watershed_types.append('coastal')

    # San Diego County watershed
    sd_watershed = Polygon([
        (-118.0, 32.2), (-118.0, 33.5), (-116.0, 33.5),
        (-116.0, 32.2), (-118.0, 32.2)
    ])
    watersheds.append(sd_watershed)
    watershed_names.append('San Diego Region')
    watershed_areas.append(1800.0)
    watershed_types.append('coastal')

    # Sierra Nevada watershed
    sierra_watershed = Polygon([
        (-120.5, 36.0), (-120.5, 39.5), (-118.5, 39.5),
        (-118.5, 36.0), (-120.5, 36.0)
    ])
    watersheds.append(sierra_watershed)
    watershed_names.append('Sierra Nevada')
    watershed_areas.append(8200.0)
    watershed_types.append('mountain')

    watersheds_data = {
        'watershed_name': watershed_names,
        'area_km2': watershed_areas,
        'basin_type': watershed_types,
        'flow_direction': ['west', 'interior', 'west', 'west', 'east'],
        'geometry': watersheds
    }

    watersheds_gdf = gpd.GeoDataFrame(watersheds_data, crs='EPSG:4326')
    watersheds_gdf.to_file(data_dir / 'watersheds.shp')
    print(f"  ✅ Created watersheds.shp with {len(watersheds_gdf)} watersheds")

    # =========================================================================
    # 3. RIVERS (LineStrings) - Major California rivers
    # =========================================================================

    rivers_data = {
        'river_name': [
            'Sacramento River',
            'San Joaquin River',
            'American River',
            'Los Angeles River',
            'Santa Ana River',
            'Russian River',
            'Salinas River'
        ],
        'length_km': [719, 560, 190, 82, 170, 177, 270],
        'flow_type': [
            'perennial', 'perennial', 'perennial',
            'intermittent', 'intermittent', 'perennial', 'intermittent'
        ],
        'discharge_cms': [650, 45, 85, 2, 8, 42, 12],
        'geometry': [
            # Sacramento River (North-South through Central Valley)
            LineString([
                (-122.0, 40.5), (-122.1, 39.8), (-121.8, 39.2),
                (-121.7, 38.8), (-121.6, 38.3), (-121.5, 37.8)
            ]),

            # San Joaquin River (East-West to Central Valley)
            LineString([
                (-119.2, 37.1), (-120.1, 37.2), (-120.8, 37.3),
                (-121.2, 37.4), (-121.5, 37.6)
            ]),

            # American River (flows to Sacramento)
            LineString([
                (-120.9, 38.8), (-121.1, 38.7), (-121.3, 38.6),
                (-121.5, 38.5)
            ]),

            # Los Angeles River
            LineString([
                (-118.3, 34.3), (-118.2, 34.1), (-118.15, 33.9),
                (-118.1, 33.7), (-118.2, 33.6)
            ]),

            # Santa Ana River
            LineString([
                (-117.0, 34.2), (-117.3, 34.0), (-117.6, 33.8),
                (-117.9, 33.7), (-118.1, 33.6)
            ]),

            # Russian River (North Coast)
            LineString([
                (-123.0, 38.9), (-123.1, 38.7), (-123.0, 38.5),
                (-122.9, 38.3), (-123.0, 38.1)
            ]),

            # Salinas River (Central Coast)
            LineString([
                (-121.0, 36.8), (-121.2, 36.5), (-121.4, 36.2),
                (-121.5, 35.9), (-121.6, 35.6)
            ])
        ]
    }

    rivers_gdf = gpd.GeoDataFrame(rivers_data, crs='EPSG:4326')
    rivers_gdf.to_file(data_dir / 'rivers.shp')
    print(f"  ✅ Created rivers.shp with {len(rivers_gdf)} rivers")

    # =========================================================================
    # 4. CREATE DATA DICTIONARY
    # =========================================================================

    data_dictionary = """# Sample Spatial Data Dictionary

This directory contains sample spatial datasets for the Python GeoPandas Analysis assignment.

## Cities (Point Features) - cities.geojson

**Description:** Major California cities with population and administrative information.

**Attributes:**
- `city_name`: Name of the city (string)
- `population`: Current population estimate (integer)
- `county`: County where city is located (string)
- `founded_year`: Year the city was founded (integer)
- `geometry`: Point coordinates in WGS84 (EPSG:4326)

**Use cases:** Buffer analysis for service areas, proximity analysis, population density studies

## Watersheds (Polygon Features) - watersheds.shp

**Description:** Simplified watershed boundaries for major California drainage basins.

**Attributes:**
- `watershed_name`: Name of the watershed/basin (string)
- `area_km2`: Area in square kilometers (float)
- `basin_type`: Type of basin - coastal, interior, or mountain (string)
- `flow_direction`: General direction of water flow (string)
- `geometry`: Polygon boundaries in WGS84 (EPSG:4326)

**Use cases:** Area calculations, overlay analysis, environmental modeling

## Rivers (Line Features) - rivers.shp

**Description:** Major California rivers and waterways with flow characteristics.

**Attributes:**
- `river_name`: Name of the river (string)
- `length_km`: Length in kilometers (float)
- `flow_type`: Flow pattern - perennial or intermittent (string)
- `discharge_cms`: Average discharge in cubic meters per second (float)
- `geometry`: LineString coordinates in WGS84 (EPSG:4326)

**Use cases:** Buffer analysis for flood zones, length calculations, network analysis

## Coordinate Reference System

All datasets use **WGS84 (EPSG:4326)** - standard geographic coordinates.

For accurate area and distance calculations, the analysis functions will automatically
reproject to appropriate UTM zones based on the geographic center of the data.

## Data Sources

This is synthesized educational data based on real California geographic features,
created specifically for learning GeoPandas spatial analysis techniques.

**Note:** While based on real locations, the specific boundaries and attribute values
are simplified and may not reflect actual measurements.
"""

    with open(data_dir / 'README.md', 'w') as f:
        f.write(data_dictionary)

    print(f"  ✅ Created data/README.md with dataset documentation")

    # =========================================================================
    # 5. SUMMARY STATISTICS
    # =========================================================================

    print(f"\n📊 Sample Data Summary:")
    print(f"  🏙️  Cities: {len(cities_gdf)} points covering California urban areas")
    print(f"  🌊 Watersheds: {len(watersheds_gdf)} polygons covering major drainage basins")
    print(f"  🏞️  Rivers: {len(rivers_gdf)} lines representing major waterways")
    print(f"  📍 All data in WGS84 (EPSG:4326) coordinate system")
    print(f"  🗂️  Files saved in 'data/' directory")

    # Show spatial extents
    cities_bounds = cities_gdf.total_bounds
    watersheds_bounds = watersheds_gdf.total_bounds
    rivers_bounds = rivers_gdf.total_bounds

    print(f"\n📐 Spatial Extents:")
    print(f"  Cities: {cities_bounds[0]:.2f}°W to {cities_bounds[2]:.2f}°W, {cities_bounds[1]:.2f}°N to {cities_bounds[3]:.2f}°N")
    print(f"  Watersheds: {watersheds_bounds[0]:.2f}°W to {watersheds_bounds[2]:.2f}°W, {watersheds_bounds[1]:.2f}°N to {watersheds_bounds[3]:.2f}°N")
    print(f"  Rivers: {rivers_bounds[0]:.2f}°W to {rivers_bounds[2]:.2f}°W, {rivers_bounds[1]:.2f}°N to {rivers_bounds[3]:.2f}°N")

    print(f"\n🎉 Sample data creation complete!")
    print(f"   Students can now test their spatial analysis functions with realistic data.")


if __name__ == '__main__':
    create_sample_data()
