#!/usr/bin/env python3
"""
Create Sample Spatial Data for GeoPandas Tutorial
=================================================

This script creates sample spatial datasets for students to use in their
GeoPandas learning exercises. The data represents realistic geographic
features for the southwestern United States.

Run this script to populate the data/ directory with sample files.

Usage:
    python create_sample_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
import json

def create_data_directory():
    """Create the data directory if it doesn't exist"""
    data_dir = Path(__file__).parent
    data_dir.mkdir(exist_ok=True)
    return data_dir

def create_arizona_cities():
    """Create sample city points for Arizona"""
    # Arizona cities with realistic coordinates and attributes
    cities_data = {
        'name': [
            'Phoenix', 'Tucson', 'Mesa', 'Chandler', 'Scottsdale',
            'Glendale', 'Gilbert', 'Tempe', 'Peoria', 'Surprise',
            'Yuma', 'Avondale', 'Flagstaff', 'Goodyear', 'Buckeye'
        ],
        'population': [
            1608139, 548073, 504258, 275987, 241361,
            248325, 267918, 195805, 190985, 141664,
            95548, 87931, 76831, 95294, 85421
        ],
        'county': [
            'Maricopa', 'Pima', 'Maricopa', 'Maricopa', 'Maricopa',
            'Maricopa', 'Maricopa', 'Maricopa', 'Maricopa', 'Maricopa',
            'Yuma', 'Maricopa', 'Coconino', 'Maricopa', 'Maricopa'
        ],
        'elevation_ft': [
            1086, 2389, 1243, 1201, 1257,
            1152, 1243, 1158, 1216, 1178,
            138, 1084, 6910, 1012, 888
        ],
        'longitude': [
            -112.0740, -110.9265, -111.8315, -111.8413, -111.9026,
            -112.1860, -111.7890, -111.9391, -112.2374, -112.3332,
            -114.6276, -112.3496, -111.6513, -112.3581, -112.5837
        ],
        'latitude': [
            33.4484, 32.2217, 33.4152, 33.3062, 33.4942,
            33.5387, 33.3528, 33.4255, 33.5806, 33.6292,
            32.6927, 33.4355, 35.1983, 33.4355, 33.3703
        ]
    }

    return pd.DataFrame(cities_data)

def create_arizona_counties():
    """Create simplified county polygons for Arizona"""
    # Simplified county boundaries (approximate)
    counties_data = []

    # Maricopa County (Phoenix metro area)
    maricopa_coords = [
        (-113.0, 33.0), (-111.5, 33.0), (-111.5, 33.8),
        (-112.5, 34.0), (-113.0, 33.8), (-113.0, 33.0)
    ]
    counties_data.append({
        'name': 'Maricopa',
        'area_sq_miles': 9224,
        'population': 4420568,
        'seat': 'Phoenix',
        'geometry': Polygon(maricopa_coords)
    })

    # Pima County (Tucson area)
    pima_coords = [
        (-111.5, 31.8), (-110.5, 31.8), (-110.5, 32.8),
        (-111.5, 32.8), (-111.5, 31.8)
    ]
    counties_data.append({
        'name': 'Pima',
        'area_sq_miles': 9189,
        'population': 1043433,
        'seat': 'Tucson',
        'geometry': Polygon(pima_coords)
    })

    # Coconino County (Flagstaff area)
    coconino_coords = [
        (-112.5, 34.5), (-111.0, 34.5), (-111.0, 36.5),
        (-113.5, 36.5), (-113.5, 34.8), (-112.5, 34.5)
    ]
    counties_data.append({
        'name': 'Coconino',
        'area_sq_miles': 18661,
        'population': 145101,
        'seat': 'Flagstaff',
        'geometry': Polygon(coconino_coords)
    })

    # Yuma County
    yuma_coords = [
        (-114.8, 32.3), (-113.8, 32.3), (-113.8, 33.5),
        (-114.8, 33.5), (-114.8, 32.3)
    ]
    counties_data.append({
        'name': 'Yuma',
        'area_sq_miles': 5519,
        'population': 203881,
        'seat': 'Yuma',
        'geometry': Polygon(yuma_coords)
    })

    return pd.DataFrame(counties_data)

def create_arizona_highways():
    """Create sample highway lines for Arizona"""
    highways_data = []

    # I-17 (Phoenix to Flagstaff)
    i17_coords = [
        (-112.0740, 33.4484),  # Phoenix
        (-112.0500, 33.8000),  # North Phoenix
        (-111.9000, 34.2000),  # Toward Flagstaff
        (-111.6513, 35.1983)   # Flagstaff
    ]
    highways_data.append({
        'name': 'Interstate 17',
        'type': 'Interstate',
        'number': 17,
        'length_miles': 146,
        'geometry': LineString(i17_coords)
    })

    # I-10 (Phoenix to Tucson)
    i10_coords = [
        (-112.0740, 33.4484),  # Phoenix
        (-111.8000, 33.2000),  # Southeast
        (-111.0000, 32.5000),  # Toward Tucson
        (-110.9265, 32.2217)   # Tucson
    ]
    highways_data.append({
        'name': 'Interstate 10',
        'type': 'Interstate',
        'number': 10,
        'length_miles': 147,
        'geometry': LineString(i10_coords)
    })

    # US-60 (East-West through Phoenix)
    us60_coords = [
        (-113.0000, 33.4000),  # West
        (-112.0740, 33.4484),  # Phoenix
        (-111.0000, 33.5000),  # East
    ]
    highways_data.append({
        'name': 'US Highway 60',
        'type': 'US Highway',
        'number': 60,
        'length_miles': 125,
        'geometry': LineString(us60_coords)
    })

    # State Route 87
    sr87_coords = [
        (-111.8315, 33.4152),  # Mesa
        (-111.7000, 33.8000),  # Northeast
        (-111.5000, 34.3000),  # Further northeast
    ]
    highways_data.append({
        'name': 'State Route 87',
        'type': 'State Route',
        'number': 87,
        'length_miles': 85,
        'geometry': LineString(sr87_coords)
    })

    return pd.DataFrame(highways_data)

def create_arizona_parks():
    """Create sample park/protected area polygons"""
    parks_data = []

    # Grand Canyon National Park (simplified)
    grand_canyon_coords = [
        (-112.5, 36.0), (-112.0, 36.0), (-112.0, 36.3),
        (-112.5, 36.3), (-112.5, 36.0)
    ]
    parks_data.append({
        'name': 'Grand Canyon National Park',
        'type': 'National Park',
        'area_acres': 1217262,
        'established': 1919,
        'visitors_annual': 5974411,
        'geometry': Polygon(grand_canyon_coords)
    })

    # Saguaro National Park (East)
    saguaro_east_coords = [
        (-110.7, 32.2), (-110.5, 32.2), (-110.5, 32.4),
        (-110.7, 32.4), (-110.7, 32.2)
    ]
    parks_data.append({
        'name': 'Saguaro National Park East',
        'type': 'National Park',
        'area_acres': 67292,
        'established': 1994,
        'visitors_annual': 1020226,
        'geometry': Polygon(saguaro_east_coords)
    })

    # McDowell Mountain Regional Park
    mcdowell_coords = [
        (-111.7, 33.6), (-111.6, 33.6), (-111.6, 33.7),
        (-111.7, 33.7), (-111.7, 33.6)
    ]
    parks_data.append({
        'name': 'McDowell Mountain Regional Park',
        'type': 'Regional Park',
        'area_acres': 21099,
        'established': 1954,
        'visitors_annual': 250000,
        'geometry': Polygon(mcdowell_coords)
    })

    # Camelback Mountain
    camelback_coords = [
        (-112.02, 33.52), (-111.98, 33.52), (-111.98, 33.54),
        (-112.02, 33.54), (-112.02, 33.52)
    ]
    parks_data.append({
        'name': 'Camelback Mountain',
        'type': 'City Park',
        'area_acres': 145,
        'established': 1965,
        'visitors_annual': 300000,
        'geometry': Polygon(camelback_coords)
    })

    return pd.DataFrame(parks_data)

def create_sample_csv_data():
    """Create sample CSV data with coordinates for testing coordinate loading"""
    csv_data = {
        'id': range(1, 11),
        'location_name': [
            'Arizona Science Center', 'Phoenix Zoo', 'Desert Botanical Garden',
            'Heard Museum', 'Musical Instrument Museum', 'Papago Park',
            'South Mountain Park', 'Camelback Mountain', 'Piestewa Peak',
            'Phoenix Art Museum'
        ],
        'longitude': [
            -112.0666, -112.0242, -111.9397, -112.0725, -111.9784,
            -111.9483, -112.0808, -111.9728, -112.0211, -112.0736
        ],
        'latitude': [
            33.4483, 33.4491, 33.4619, 33.4734, 33.6676,
            33.4551, 33.3928, 33.5225, 33.5403, 33.4668
        ],
        'category': [
            'Museum', 'Zoo', 'Garden', 'Museum', 'Museum',
            'Park', 'Park', 'Recreation', 'Recreation', 'Museum'
        ],
        'rating': [4.5, 4.3, 4.6, 4.4, 4.7, 4.2, 4.4, 4.8, 4.3, 4.1],
        'annual_visitors': [
            500000, 1400000, 400000, 250000, 200000,
            750000, 2000000, 300000, 200000, 150000
        ]
    }
    return pd.DataFrame(csv_data)

def save_sample_datasets():
    """Save all sample datasets to files"""
    data_dir = create_data_directory()
    print(f"🗺️ Creating sample spatial data in {data_dir}")

    # Create point data (cities)
    print("  📍 Creating Arizona cities...")
    cities_df = create_arizona_cities()
    cities_gdf = pd.DataFrame(cities_df)

    # Convert to GeoDataFrame
    geometry = [Point(xy) for xy in zip(cities_df.longitude, cities_df.latitude)]
    import geopandas as gpd
    cities_gdf = gpd.GeoDataFrame(cities_df.drop(['longitude', 'latitude'], axis=1), geometry=geometry)
    cities_gdf.crs = 'EPSG:4326'

    # Save as different formats
    cities_gdf.to_file(data_dir / 'arizona_cities.geojson', driver='GeoJSON')
    cities_gdf.to_file(data_dir / 'arizona_cities.shp')

    # Create county polygons
    print("  🏛️ Creating Arizona counties...")
    counties_gdf = gpd.GeoDataFrame(create_arizona_counties())
    counties_gdf.crs = 'EPSG:4326'
    counties_gdf.to_file(data_dir / 'arizona_counties.geojson', driver='GeoJSON')
    counties_gdf.to_file(data_dir / 'arizona_counties.shp')

    # Create highway lines
    print("  🛣️ Creating Arizona highways...")
    highways_gdf = gpd.GeoDataFrame(create_arizona_highways())
    highways_gdf.crs = 'EPSG:4326'
    highways_gdf.to_file(data_dir / 'arizona_highways.geojson', driver='GeoJSON')
    highways_gdf.to_file(data_dir / 'arizona_highways.shp')

    # Create parks/protected areas
    print("  🏞️ Creating Arizona parks...")
    parks_gdf = gpd.GeoDataFrame(create_arizona_parks())
    parks_gdf.crs = 'EPSG:4326'
    parks_gdf.to_file(data_dir / 'arizona_parks.geojson', driver='GeoJSON')
    parks_gdf.to_file(data_dir / 'arizona_parks.shp')

    # Create CSV with coordinates
    print("  📊 Creating sample CSV data...")
    csv_data = create_sample_csv_data()
    csv_data.to_csv(data_dir / 'phoenix_attractions.csv', index=False)

    # Create a simple README
    readme_content = """# Sample Data for GeoPandas Tutorial

This directory contains sample spatial datasets for learning GeoPandas:

## Files:
- `arizona_cities.*` - Point data of major Arizona cities
- `arizona_counties.*` - Polygon data of Arizona counties
- `arizona_highways.*` - Line data of major highways
- `arizona_parks.*` - Polygon data of parks and protected areas
- `phoenix_attractions.csv` - CSV with longitude/latitude columns

## Data Sources:
All datasets are simplified, educational versions created for tutorial purposes.
Real-world analysis should use authoritative data sources.

## Coordinate System:
All spatial data uses WGS84 (EPSG:4326) coordinate system.
"""

    with open(data_dir / 'README.md', 'w') as f:
        f.write(readme_content)

    print("✅ Sample data created successfully!")
    print("\nFiles created:")
    for file_path in sorted(data_dir.glob('*')):
        if file_path.is_file():
            print(f"  📄 {file_path.name}")

if __name__ == "__main__":
    try:
        import geopandas as gpd
        save_sample_datasets()
    except ImportError:
        print("❌ GeoPandas is required to run this script.")
        print("Install it with: pip install geopandas")

        # Create basic CSV data at minimum
        data_dir = create_data_directory()
        print("\n📊 Creating CSV data only...")
        csv_data = create_sample_csv_data()
        csv_data.to_csv(data_dir / 'phoenix_attractions.csv', index=False)
        print("✅ CSV data created!")
