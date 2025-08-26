# Sample Spatial Datasets

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


### Cities Dataset
- **Features**: 30
- **Geometry Type**: Point
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Global coverage
- **Attributes**: Population, country, continent data

### Countries Dataset
- **Features**: 15
- **Geometry Type**: Polygon
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Global coverage (simplified boundaries)
- **Attributes**: Area, population by country

### Roads Dataset
- **Features**: 13
- **Geometry Type**: LineString
- **CRS**: EPSG:4326 (WGS84)
- **Extent**: Major highways across continents
- **Attributes**: Highway names, types, lengths

### Mixed Geometries Dataset
- **Features**: 9
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
print(f"Loaded {len(cities)} cities")

# Load data with issues for validation practice
cities_with_issues = gpd.read_file('data/cities/cities_with_issues.geojson')
print(f"Dataset has valid geometries: {cities_with_issues.geometry.is_valid.all()}")

# Load different projections
cities_utm = gpd.read_file('data/cities/cities_utm.geojson')
print(f"UTM CRS: {cities_utm.crs}")
```

## 🗺️ Coordinate Reference Systems

- **EPSG:4326**: WGS84 geographic coordinates (longitude, latitude)
- **EPSG:3857**: Web Mercator projection (for web mapping)
- **EPSG:32610**: UTM Zone 10N (Pacific Northwest region)

---

*These datasets are created for educational purposes and use simplified geometries.
For production analysis, use authoritative spatial data sources.*
