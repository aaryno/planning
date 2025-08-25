# Lecture: Rasterio Raster Processing

## Module: Open Source GIS Programming with Python
**Duration:** 50 minutes
**Format:** Interactive lecture with multimedia content

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **Understand** raster data structure and how it differs from vector data in Python
- **Read and manipulate** raster datasets using rasterio and numpy arrays
- **Apply** Cloud-Optimized GeoTIFF (COG) concepts for efficient raster processing
- **Implement** windowed reading techniques for large-scale raster analysis

---

## Lecture Outline

### I. Introduction and Context (10 minutes)
- Transition from vector (GeoPandas) to raster (rasterio) analysis
- Raster data in the modern GIS workflow
- Cloud-based remote sensing and big data challenges

### II. Core Concepts (25 minutes)
- **Raster Data Structure and NumPy Integration**
  - Understanding pixels as arrays
  - Coordinate systems and geotransforms
  - Multi-band imagery concepts

- **Modern Raster Standards**
  - Cloud-Optimized GeoTIFFs (COGs)
  - Spatio-Temporal Asset Catalog (STAC)
  - Windowed reading for performance

- **Essential Raster Operations**
  - Reading metadata and bands
  - Extracting values and statistics
  - Coordinate transformations

### III. Practical Applications (10 minutes)
- Satellite imagery analysis workflow
- Integration with vector data (raster-vector operations)
- Performance optimization strategies

### IV. Summary and Next Steps (5 minutes)
- Key raster processing concepts recap
- Connection to upcoming assignments
- Preparation for advanced raster analysis

---

## Key Concepts

### From Vector to Raster: Fundamental Differences

**Vector Data (GeoPandas) vs. Raster Data (Rasterio):**

```python
# Vector: Discrete features with attributes
gdf = gpd.read_file('cities.shp')
print(gdf.geometry.area)  # Calculate areas of polygons

# Raster: Continuous grid of values
import rasterio
with rasterio.open('elevation.tif') as src:
    elevation_data = src.read(1)  # Read first band as numpy array
    print(elevation_data.mean())  # Calculate mean elevation
```

**Key Conceptual Shifts:**
- **Vector:** Features with attributes → **Raster:** Grid of values
- **Vector:** Precise geometry → **Raster:** Resolution-dependent
- **Vector:** Attributes in table → **Raster:** Values in pixels
- **Vector:** Unlimited precision → **Raster:** Fixed grid size

### Raster Data Structure in Python

**The Three Essential Components:**
1. **Data Array** (numpy array): The actual pixel values
2. **Geotransform**: How to convert pixel coordinates to geographic coordinates
3. **Coordinate Reference System**: Geographic projection information

```python
import rasterio
import numpy as np

with rasterio.open('satellite_image.tif') as src:
    # 1. Data as numpy array
    data = src.read()  # Shape: (bands, height, width)
    
    # 2. Geotransform: pixel → geographic coordinates
    transform = src.transform
    
    # 3. Coordinate system
    crs = src.crs
    
    # Metadata about the raster
    print(f"Shape: {data.shape}")
    print(f"Data type: {data.dtype}")
    print(f"CRS: {crs}")
```

**Working with Multi-band Imagery:**
```python
# RGB satellite image (3 bands)
red_band = src.read(1)    # Band 1: Red
green_band = src.read(2)  # Band 2: Green  
blue_band = src.read(3)   # Band 3: Blue

# Calculate NDVI using red and near-infrared bands
nir_band = src.read(4)    # Band 4: Near-infrared
ndvi = (nir_band - red_band) / (nir_band + red_band)
```

### Cloud-Optimized GeoTIFFs (COGs)

**Why COGs Matter:**
Traditional GeoTIFFs require downloading entire files before analysis. COGs are structured to enable:
- **Streaming access**: Read only the data you need
- **Progressive resolution**: Load overview levels for faster preview
- **HTTP range requests**: Access remote data without full download

**COG Structure:**
- **Tiled organization**: Data organized in small tiles (e.g., 512x512 pixels)
- **Internal overviews**: Pre-computed lower resolution versions
- **Optimized metadata**: Headers organized for quick access

**Working with COGs:**
```python
import rasterio

# Open COG directly from URL (no download needed)
cog_url = "https://example.com/satellite_data.tif"

with rasterio.open(cog_url) as src:
    # Read just a small window - only downloads needed tiles
    window = rasterio.windows.Window(1000, 1000, 256, 256)
    data = src.read(1, window=window)
    
    # Access overview levels for quick preview
    overviews = src.overviews(1)  # Available overview levels
    overview_data = src.read(1, out_shape=(100, 100))  # Resample to smaller size
```

### Windowed Reading for Large Datasets

**The Challenge**: Satellite imagery files can be gigabytes in size - too large for memory.

**The Solution**: Process data in small windows (chunks) rather than loading entire datasets.

```python
import rasterio
from rasterio.windows import Window

# Process large raster in 1024x1024 pixel chunks
def process_large_raster(input_path, output_path):
    with rasterio.open(input_path) as src:
        # Define processing window size
        window_size = 1024
        
        # Get raster dimensions
        height, width = src.height, src.width
        
        # Copy metadata for output file
        profile = src.profile
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            # Process in windows
            for i in range(0, height, window_size):
                for j in range(0, width, window_size):
                    # Define window bounds
                    window = Window(j, i, 
                                  min(window_size, width - j),
                                  min(window_size, height - i))
                    
                    # Read window data
                    data = src.read(1, window=window)
                    
                    # Process data (example: multiply by 2)
                    processed = data * 2
                    
                    # Write processed window
                    dst.write(processed, 1, window=window)
```

**Memory Management Benefits:**
- Process 100GB+ files on standard computers
- Consistent memory usage regardless of file size
- Parallel processing potential

### Spatio-Temporal Asset Catalog (STAC)

**STAC Purpose**: Standardized way to describe and discover satellite imagery and other spatio-temporal data.

**Key STAC Concepts:**
- **Item**: Individual dataset (e.g., one Landsat scene)
- **Collection**: Group of related items (e.g., all Landsat 8 data)
- **Catalog**: Hierarchical structure of collections

**Finding Satellite Data with STAC:**
```python
import pystac_client

# Connect to Microsoft Planetary Computer STAC API
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1"
)

# Search for Landsat data over Arizona
search = catalog.search(
    collections=["landsat-c2-l2"],
    bbox=[-114.8, 31.3, -109.0, 37.0],  # Arizona bounding box
    datetime="2023-01-01/2023-12-31",
    limit=10
)

# Get search results
items = search.get_items()
for item in items:
    print(f"Date: {item.datetime}")
    print(f"Cloud cover: {item.properties['eo:cloud_cover']}%")
```

### Raster-Vector Integration

**Common Workflows:**
1. **Extract raster values at vector points** (sampling)
2. **Mask raster data by vector boundaries** (clipping)
3. **Calculate zonal statistics** (summarize raster by vector regions)

```python
import rasterio
import geopandas as gpd
from rasterio.mask import mask

# Clip raster by vector boundary
vector_data = gpd.read_file('study_area.shp')
vector_data = vector_data.to_crs('EPSG:4326')  # Match CRS

with rasterio.open('elevation.tif') as src:
    # Clip raster to vector boundaries
    clipped_data, clipped_transform = mask(
        src, vector_data.geometry, crop=True
    )
    
    # Update metadata for clipped raster
    clipped_profile = src.profile
    clipped_profile.update({
        'height': clipped_data.shape[1],
        'width': clipped_data.shape[2],
        'transform': clipped_transform
    })
```

---

## Interactive Elements

### Discussion Questions

1. **Data Strategy**: You need to analyze vegetation health across all of Arizona using monthly satellite imagery for 5 years. What data access and processing strategies would you use?

2. **Performance Trade-offs**: When would you choose to download entire raster files versus using windowed reading from cloud sources?

3. **Integration Challenge**: A city planning department wants to combine demographic data (vector) with satellite-derived land cover (raster). What analysis approaches would you recommend?

### Hands-on Activity

**Raster Processing Demonstration:**
Using Arizona satellite data, we'll demonstrate:
1. Opening and exploring raster metadata
2. Reading specific bands and calculating NDVI
3. Implementing windowed reading for memory efficiency
4. Masking raster data using vector boundaries
5. Basic visualization with matplotlib

---

## Resources

### Required Materials
- Rasterio documentation: https://rasterio.readthedocs.io/
- Cloud-Optimized GeoTIFF guide: https://www.cogeo.org/
- STAC specification: https://stacspec.org/
- Sample Arizona Landsat data (provided in Codespaces)

### Supplementary Resources
- **Tutorial:** Earth Lab Rasterio lessons: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/
- **Reference:** NumPy array manipulation: https://numpy.org/doc/stable/user/basics.html
- **Data Source:** Microsoft Planetary Computer: https://planetarycomputer.microsoft.com/
- **Performance:** Dask for large-scale raster processing: https://docs.dask.org/en/latest/array.html

---

## Preparation for Next Session

### Required Reading
- Rasterio documentation sections on "Reading Raster Data" and "Windowed Reading and Writing"
- Review NumPy array operations (indexing, slicing, mathematical operations)

### Recommended Preparation
- Explore STAC browser: https://radiantearth.github.io/stac-browser/
- Practice basic NumPy array manipulations
- Familiarize yourself with common satellite data formats

### Technical Setup
- Verify rasterio, numpy, matplotlib packages in Codespaces
- Test basic raster reading operations
- Ensure sufficient disk space for sample datasets

---

## Notes for Instructors

### Technical Requirements
- [ ] Codespaces with rasterio, numpy, matplotlib, pystac-client installed
- [ ] Sample datasets: Landsat scene, DEM, vector boundaries
- [ ] Internet access for COG and STAC demonstrations
- [ ] Backup local datasets in case of connectivity issues

### Common Issues
- **Memory Problems:** Students may try to load entire large rasters. Emphasize windowed reading early
- **CRS Mismatches:** Raster-vector integration requires careful CRS alignment
- **Array Indexing:** NumPy array indexing (y, x) vs. geographic coordinates (x, y) confusion
- **Data Types:** Integer vs. float arrays affect calculations (especially division operations)

### Timing Adjustments
- **If Running Behind:** Focus on basic raster reading and COG concepts, defer advanced windowed reading
- **If Ahead:** Introduce rasterstats library for zonal statistics and more complex raster-vector operations
- **Interactive Extensions:** Let students explore different satellite data sources through STAC

### Assessment Integration
- Connect examples to upcoming rasterio assignment requirements
- Emphasize reproducible workflows and documentation practices
- Use Arizona-specific examples that students can relate to locally

### Progression Notes
- **From GeoPandas:** Show how raster analysis complements vector analysis
- **To Next Topics:** Prepare foundation for raster-vector integration and PyQGIS automation
- **Skills Building:** Emphasize problem-solving approaches for large-data challenges