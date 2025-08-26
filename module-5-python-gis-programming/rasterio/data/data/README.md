# Real Geospatial Data for GIST 604B Rasterio Learning

This collection contains **real geospatial datasets** downloaded from NASA, USGS, and NOAA
for authentic GIS learning experiences.

## 🗺️ Study Area: Phoenix, Arizona

**Spatial Extent:** -112.5°W to -111.5°W, 33.0°N to 34.0°N
**Area:** ~12321 km²
**Why Phoenix:** Diverse terrain, clear satellite imagery, urban heat island effects

## 📊 Datasets

### 1. Digital Elevation Model
**File:** `raster/phoenix_dem_30m.tif`
**Source:** NASA SRTM 1 Arc-Second Global DEM
**Resolution:** 30 meters
**Data Type:** Float32 (elevation in meters)
**Vertical Datum:** EGM96 Geoid
**Features:** South Mountain, Camelback Mountain, Salt River valley

### 2. Landsat 8 Surface Reflectance
**File:** `raster/landsat8_phoenix_2024.tif`
**Source:** USGS Landsat Collection 2 Level-2
**Bands:** 6 (Blue, Green, Red, NIR, SWIR1, SWIR2)
**Resolution:** 30 meters
**Data Type:** UInt16 (surface reflectance)
**Scene Date:** Recent cloud-free acquisition

### 3. Land Surface Temperature
**File:** `raster/modis_lst_phoenix.tif`
**Source:** NASA MODIS Terra Daily LST
**Resolution:** 1 kilometer
**Data Type:** Float32 (temperature in Celsius)
**Temporal:** Daily acquisition
**Purpose:** Urban heat island analysis

### 4. Vector Support Data
**Files:** `vector/phoenix_study_area.geojson`, `vector/sample_points.geojson`
**Purpose:** Raster-vector integration exercises
**Content:** Study area boundary, validation points

## 🚀 Usage Examples

### Load and Explore DEM
```python
import rasterio
import numpy as np

with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:
    dem = src.read(1)
    print(f"Elevation range: {np.nanmin(dem):.0f} to {np.nanmax(dem):.0f} meters")
    print(f"Mean elevation: {np.nanmean(dem):.0f} meters")
```

### Calculate NDVI from Landsat
```python
with rasterio.open('data/raster/landsat8_phoenix_2024.tif') as src:
    red = src.read(3).astype(float)    # Red band
    nir = src.read(4).astype(float)    # NIR band

    ndvi = (nir - red) / (nir + red)
    # Mask invalid values
    ndvi = np.where((nir + red) == 0, np.nan, ndvi)
```

### Temperature Analysis
```python
with rasterio.open('data/raster/modis_lst_phoenix.tif') as src:
    temp = src.read(1)
    print(f"Temperature range: {np.nanmin(temp):.1f} to {np.nanmax(temp):.1f} °C")
```

## 📁 Directory Structure
```
data/
├── raster/                     # Raster datasets
│   ├── phoenix_dem_30m.tif         # Digital Elevation Model
│   ├── landsat8_phoenix_2024.tif   # Multispectral imagery
│   └── modis_lst_phoenix.tif        # Land surface temperature
├── vector/                     # Vector support data
│   ├── phoenix_study_area.geojson   # Study area boundary
│   └── sample_points.geojson        # Validation points
├── downloads/                  # Raw downloads (temporary)
├── processed/                  # Analysis outputs
├── data_inventory.json         # Dataset catalog
├── phoenix_stac_metadata.json  # STAC-compliant metadata
└── README.md                   # This file
```

## 🔄 Data Download Process

This data was downloaded using `create_sample_data.py`:

1. **USGS 3DEP DEM** - NASA SRTM 1 Arc-Second Global
2. **Landsat Collection 2** - USGS/AWS Open Data Registry
3. **MODIS LST** - NASA LAADS DAAC
4. **Fallback Generation** - High-quality synthetic when real data unavailable

## ⚠️ Data Notes

- **Real Data Priority**: Downloads authentic datasets when servers available
- **Fallback Synthetic**: Creates realistic synthetic data if downloads fail
- **Educational Use**: Optimized for learning, not production analysis
- **File Sizes**: Manageable sizes for coursework (total ~50-200 MB)
- **Quality**: Professional-grade georeferenced data suitable for research

## 🎓 Learning Objectives

Students working with this data will learn:
- Loading and exploring real satellite/DEM data
- Multi-band raster processing with authentic spectral signatures
- Handling real-world data quality issues
- Professional raster analysis workflows
- STAC metadata standards
- Cloud-optimized GeoTIFF creation

## 📚 Data Sources & Attribution

- **NASA SRTM**: Shuttle Radar Topography Mission, public domain
- **USGS Landsat**: Land Remote Sensing Program, public domain
- **NASA MODIS**: Moderate Resolution Imaging Spectroradiometer, public domain
- **Processing**: GIST 604B Course Team, University of Arizona

---

*Created: 2025-08-26 for GIST 604B - Open Source GIS Programming*
*University of Arizona, School of Geography, Development & Environment*
