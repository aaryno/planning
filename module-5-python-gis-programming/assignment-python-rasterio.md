# Assignment: Advanced Python Rasterio and Raster Processing

## Module: Open Source GIS Programming with Python
**Points:** 20
**Due:** Two weeks after assignment
**Type:** Advanced Raster Analysis and Integration Programming

---

## Assignment Overview

This assignment focuses on advanced raster data processing using Python's rasterio library, emphasizing modern cloud-based workflows with Cloud-Optimized GeoTIFFs (COGs), Spatio-Temporal Asset Catalog (STAC) integration, and efficient large-scale raster analysis. You'll build sophisticated raster processing pipelines that integrate with vector data analysis, implementing memory-efficient workflows suitable for production GIS environments.

Building on your GeoPandas spatial analysis skills, you'll learn to work with satellite imagery, digital elevation models, and other raster datasets using modern Python development practices and cloud-optimized data formats essential for contemporary remote sensing and GIS applications.

---

## Learning Objectives

By completing this assignment, you will be able to:
- **Process** raster datasets efficiently using rasterio with modern Python 3.13 features
- **Implement** Cloud-Optimized GeoTIFF (COG) workflows for scalable raster analysis
- **Access** satellite imagery through STAC APIs for automated data discovery
- **Apply** windowed reading techniques for memory-efficient processing of large rasters
- **Integrate** raster and vector analysis in complex spatial workflows
- **Optimize** raster processing performance using advanced techniques
- **Create** professional raster analysis applications with comprehensive error handling

---

## Prerequisites

**Required Completed Work:**
- [ ] Python Package Managers lecture and exercises
- [ ] Python GIS Ecosystem lecture
- [ ] GeoPandas Vector Analysis lecture
- [ ] Rasterio Processing lecture (completed)
- [ ] Spatial Joins and Integration lecture
- [ ] Python GeoPandas Introduction assignment
- [ ] Python GeoPandas Spatial Joins assignment

**Technical Requirements:**
- [ ] uv package manager installed and configured
- [ ] Python 3.13+ environment
- [ ] Understanding of NumPy arrays and mathematical operations
- [ ] Familiarity with coordinate reference systems and map projections
- [ ] Basic understanding of remote sensing concepts

---

## Technical Setup

### Step 1: Initialize Advanced Raster Analysis Project
```bash
# Create project for comprehensive raster analysis
uv init rasterio-analysis --python 3.13
cd rasterio-analysis

# Verify Python version
uv run python --version  # Should show Python 3.13.x
```

### Step 2: Add Core Raster Processing Dependencies
```bash
# Core raster processing packages with version pinning
uv add "rasterio~=1.3.9"        # Core raster I/O
uv add "numpy~=1.26.2"          # Numerical computing
uv add "scipy~=1.11.4"          # Scientific computing
uv add "matplotlib~=3.8.2"     # Visualization
uv add "seaborn~=0.13.0"        # Statistical visualization

# Geospatial integration packages
uv add "geopandas~=0.14.1"      # Vector-raster integration
uv add "shapely~=2.0.2"         # Geometric operations
uv add "contextily~=1.4.0"      # Basemap integration

# Cloud and remote sensing packages
uv add "pystac-client~=0.7.5"   # STAC API client
uv add "planetary-computer~=0.4.9"  # Microsoft Planetary Computer
uv add "requests~=2.31.0"       # HTTP requests
uv add "aiohttp~=3.9.0"         # Async HTTP for performance

# Analysis and development tools
uv add "jupyter~=1.0.0"         # Interactive analysis
uv add "rasterstats~=0.19.0"    # Zonal statistics
uv add "dask~=2023.12.0"        # Parallel processing
uv add "xarray~=2023.12.0"      # N-dimensional arrays

# Development dependencies
uv add --dev "pytest~=7.4.0"
uv add --dev "black~=23.0.0"
uv add --dev "ruff~=0.1.8"
uv add --dev "memory-profiler~=0.61.0"  # Memory monitoring
```

### Step 3: Verify Raster Processing Environment
```bash
# Test all critical raster processing imports
uv run python -c "
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pystac_client
import rasterstats
print('✅ All raster processing packages imported successfully')
print(f'Rasterio: {rasterio.__version__}')
print(f'NumPy: {np.__version__}')
print(f'GeoPandas: {gpd.__version__}')
"
```

### Step 4: Download Course Raster Data and Vector Integration
```bash
# Download enhanced course data with raster datasets
curl -O https://raw.githubusercontent.com/[course-repo]/planning/module-5-python-gis-programming/setup_raster_data.py

# Generate raster datasets and vector integration examples
uv run python setup_raster_data.py
```

---

## Project Structure

Your completed project should follow this professional structure:
```
rasterio-analysis/
├── pyproject.toml              # Project configuration with raster dependencies
├── uv.lock                    # Locked dependency versions
├── README.md                  # Comprehensive project documentation
├── data/                      # Raster and vector datasets
│   ├── raster/               # Raster data files
│   │   ├── phoenix_dem.tif          # Digital Elevation Model
│   │   ├── phoenix_landsat.tif      # Multispectral imagery
│   │   ├── phoenix_temperature.tif  # Temperature raster
│   │   └── samples/                 # Sample COG files
│   ├── vector/               # Vector datasets for integration
│   │   ├── phoenix_boundaries.shp
│   │   ├── study_areas.shp
│   │   └── sampling_points.shp
│   └── remote/               # Remote/cloud data references
├── analysis/                  # Analysis modules
│   ├── __init__.py
│   ├── raster_processing.py  # Core raster operations
│   ├── cog_operations.py     # COG-specific functionality
│   ├── stac_integration.py   # STAC API integration
│   ├── windowed_processing.py # Memory-efficient processing
│   ├── raster_vector.py      # Raster-vector integration
│   └── performance_tools.py  # Performance optimization
├── notebooks/                # Interactive analysis notebooks
│   ├── 01_raster_basics.ipynb
│   ├── 02_cog_processing.ipynb
│   ├── 03_stac_integration.ipynb
│   ├── 04_large_scale_processing.ipynb
│   └── 05_raster_vector_integration.ipynb
├── scripts/                  # Standalone analysis scripts
│   ├── process_satellite_data.py
│   ├── generate_vegetation_index.py
│   └── environmental_analysis.py
├── output/                   # Generated results
│   ├── processed_rasters/
│   ├── maps/
│   ├── reports/
│   └── statistics/
├── tests/                    # Unit tests for raster processing
│   ├── test_raster_processing.py
│   ├── test_cog_operations.py
│   └── test_performance.py
├── config/                   # Configuration files
│   ├── processing_config.yaml
│   └── stac_endpoints.json
└── run_analysis.py           # Main analysis orchestration script
```

---

## Assignment Tasks

### Part 1: Advanced Raster Processing Fundamentals (35 points)

#### 1.1 Raster Data Access and COG Processing (20 points)

**A. Local Raster Analysis (10 points)**

Implement comprehensive raster processing for local datasets:

```python
# File: analysis/raster_processing.py
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.windows import Window
from rasterio.enums import Resampling
from pathlib import Path

def analyze_local_raster():
    """
    Comprehensive analysis of local raster datasets.
    Demonstrates fundamental rasterio operations and metadata handling.
    """
    # Load Phoenix DEM
    dem_path = Path('data/raster/phoenix_dem.tif')
    
    with rasterio.open(dem_path) as src:
        # Extract comprehensive metadata
        metadata = {
            'width': src.width,
            'height': src.height,
            'count': src.count,
            'dtype': src.dtypes[0],
            'crs': src.crs,
            'transform': src.transform,
            'bounds': src.bounds,
            'nodata': src.nodata
        }
        
        # Read full raster data
        elevation = src.read(1)
        
        # Calculate terrain statistics
        terrain_stats = {
            'min_elevation': float(np.nanmin(elevation)),
            'max_elevation': float(np.nanmax(elevation)),
            'mean_elevation': float(np.nanmean(elevation)),
            'std_elevation': float(np.nanstd(elevation)),
            'elevation_range': float(np.nanmax(elevation) - np.nanmin(elevation))
        }
        
        # YOUR IMPLEMENTATION: Add slope and aspect calculations
        # YOUR IMPLEMENTATION: Add terrain ruggedness index
        # YOUR IMPLEMENTATION: Identify flat areas and steep slopes
        
    return metadata, terrain_stats, elevation

def process_multiband_imagery():
    """
    Process multispectral imagery with band math and indices.
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

**B. Cloud-Optimized GeoTIFF Processing (10 points)**

Implement COG-specific operations for efficient remote data access:

```python
# File: analysis/cog_operations.py
import rasterio
from rasterio.session import AWSSession
import contextily as ctx

def process_remote_cog():
    """
    Process Cloud-Optimized GeoTIFF from remote source.
    Demonstrate efficient access patterns and overview usage.
    """
    # Example COG URL (replace with actual course data)
    cog_url = "https://example.com/course-data/phoenix_sentinel.tif"
    
    try:
        with rasterio.open(cog_url) as src:
            # Access COG overviews for efficient preview
            overviews = src.overviews(1)
            print(f"Available overviews: {overviews}")
            
            # Read low-resolution overview for quick visualization
            if overviews:
                # Read from first overview level
                overview_data = src.read(1, out_shape=(
                    src.height // overviews[0],
                    src.width // overviews[0]
                ), resampling=Resampling.average)
            else:
                # Read full resolution if no overviews
                overview_data = src.read(1)
            
            # Access specific window for detailed analysis
            # Define window in pixel coordinates
            window = Window(1000, 1000, 512, 512)  # x_offset, y_offset, width, height
            window_data = src.read(1, window=window)
            
            # YOUR IMPLEMENTATION: Analyze window data
            # YOUR IMPLEMENTATION: Compare full vs windowed access performance
            # YOUR IMPLEMENTATION: Process multiple windows in sequence
            
    except Exception as e:
        print(f"Error accessing remote COG: {e}")
        # YOUR IMPLEMENTATION: Fallback to local data processing
    
    return overview_data, window_data

def create_optimized_cog():
    """
    Convert regular GeoTIFF to Cloud-Optimized GeoTIFF.
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### 1.2 STAC API Integration and Satellite Data Access (15 points)

**A. STAC Search and Discovery (8 points)**

Implement satellite data discovery using STAC APIs:

```python
# File: analysis/stac_integration.py
import pystac_client
import planetary_computer as pc
from datetime import datetime, timedelta
import geopandas as gpd

def search_satellite_imagery():
    """
    Search for satellite imagery using STAC API.
    Focus on Arizona region with specific temporal and quality criteria.
    """
    # Connect to Microsoft Planetary Computer STAC API
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=pc.sign_inplace
    )
    
    # Define Arizona study area
    phoenix_bounds = [-112.5, 33.0, -111.5, 33.8]  # [west, south, east, north]
    
    # Search for recent Landsat 8-9 data
    search = catalog.search(
        collections=["landsat-c2-l2"],
        bbox=phoenix_bounds,
        datetime="2023-01-01/2023-12-31",
        query={"eo:cloud_cover": {"lt": 20}},  # Less than 20% cloud cover
        limit=10
    )
    
    # Process search results
    items = list(search.get_items())
    print(f"Found {len(items)} Landsat scenes")
    
    # Analyze available items
    scene_info = []
    for item in items:
        scene_data = {
            'id': item.id,
            'datetime': item.datetime,
            'cloud_cover': item.properties.get('eo:cloud_cover', 'unknown'),
            'bounds': item.bbox,
            'assets': list(item.assets.keys())
        }
        scene_info.append(scene_data)
    
    # YOUR IMPLEMENTATION: Filter by additional criteria
    # YOUR IMPLEMENTATION: Sort by cloud cover and date
    # YOUR IMPLEMENTATION: Select best scenes for analysis
    
    return items, scene_info

def load_stac_data_as_array():
    """
    Load STAC item data as NumPy arrays for analysis.
    """
    items, _ = search_satellite_imagery()
    if not items:
        return None
    
    # Select best item (lowest cloud cover)
    best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
    
    # Load specific bands
    try:
        import rioxarray as rxr  # May need to add this dependency
        
        # Load red and near-infrared bands for NDVI calculation
        red_url = best_item.assets['red'].href
        nir_url = best_item.assets['nir08'].href
        
        # Load as arrays
        with rasterio.open(pc.sign(red_url)) as red_src:
            red_data = red_src.read(1)
            profile = red_src.profile
            
        with rasterio.open(pc.sign(nir_url)) as nir_src:
            nir_data = nir_src.read(1)
        
        # YOUR IMPLEMENTATION: Calculate NDVI
        # YOUR IMPLEMENTATION: Mask invalid values
        # YOUR IMPLEMENTATION: Apply quality filters
        
        return red_data, nir_data, profile, best_item
        
    except Exception as e:
        print(f"Error loading STAC data: {e}")
        return None

def analyze_vegetation_time_series():
    """
    Analyze vegetation changes over time using multiple STAC items.
    """
    # YOUR IMPLEMENTATION HERE
    pass

def compare_seasonal_changes():
    """
    Compare seasonal vegetation patterns using STAC time series.
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

### Part 2: Memory-Efficient Processing and Performance Optimization (30 points)

#### 2.1 Windowed Reading and Large Dataset Processing (18 points)

**A. Windowed Processing Implementation (12 points)**

Implement memory-efficient windowed processing for large rasters:

```python
# File: analysis/windowed_processing.py
import rasterio
from rasterio.windows import Window
import numpy as np
from memory_profiler import profile
import time

def process_large_raster_windowed(input_path, output_path, window_size=1024):
    """
    Process large raster using windowed reading to manage memory usage.
    Apply processing function to each window and write results.
    """
    with rasterio.open(input_path) as src:
        # Get raster dimensions
        height, width = src.height, src.width
        profile = src.profile
        
        # Update profile for output
        profile.update(dtype=rasterio.float32)
        
        # Create output file
        with rasterio.open(output_path, 'w', **profile) as dst:
            # Process in windows
            for y in range(0, height, window_size):
                for x in range(0, width, window_size):
                    # Calculate window bounds
                    window = Window(
                        x, y,
                        min(window_size, width - x),
                        min(window_size, height - y)
                    )
                    
                    # Read window data
                    window_data = src.read(1, window=window)
                    
                    # Apply processing function
                    processed_data = process_window_function(window_data)
                    
                    # Write processed window
                    dst.write(processed_data, 1, window=window)
                    
                    # Optional: Progress reporting
                    progress = ((y // window_size) * (width // window_size) + 
                               (x // window_size)) / ((height // window_size) * (width // window_size))
                    if progress % 0.1 < 0.01:  # Report every 10%
                        print(f"Processing progress: {progress:.1%}")
    
    print(f"Windowed processing complete: {output_path}")

def calculate_ndvi_safe(red_band, nir_band):
    """
    Calculate NDVI with safe division handling.
    """
    # YOUR IMPLEMENTATION: Handle division by zero
    # YOUR IMPLEMENTATION: Apply valid data masks
    # YOUR IMPLEMENTATION: Return processed NDVI
    pass

def benchmark_processing_methods():
    """
    Compare performance of different processing approaches.
    """
    test_file = 'data/raster/phoenix_landsat.tif'
    
    # Method 1: Load entire raster into memory
    start_time = time.time()
    with rasterio.open(test_file) as src:
        full_data = src.read()
        # Process full data
        processed_full = np.sqrt(full_data)  # Simple processing example
    full_time = time.time() - start_time
    
    # Method 2: Windowed processing
    start_time = time.time()
    process_large_raster_windowed(test_file, 'output/processed_windowed.tif')
    windowed_time = time.time() - start_time
    
    # YOUR IMPLEMENTATION: Method 3 with different window sizes
    # YOUR IMPLEMENTATION: Memory usage monitoring
    
    return {
        'full_memory_time': full_time,
        'windowed_time': windowed_time,
        'memory_savings': 'measured_savings'
    }

def optimize_raster_processing():
    """
    Demonstrate various optimization techniques for raster processing.
    """
    # Optimization techniques to implement:
    # 1. Appropriate data types
    # 2. Chunking strategies
    # 3. Parallel processing with dask
    # 4. Memory mapping for large files
    
    @profile
    def monitor_memory():
        # YOUR IMPLEMENTATION: Memory-intensive operation
        # Monitor memory usage during processing
        pass
    
    # YOUR IMPLEMENTATION HERE
    pass

def parallel_raster_processing():
    """
    Implement parallel processing using dask for multiple rasters.
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

#### 2.2 Raster-Vector Integration (12 points)

**B. Advanced Raster-Vector Operations (12 points)**

Implement sophisticated raster-vector integration workflows:

```python
# File: analysis/raster_vector.py
import rasterio
import geopandas as gpd
from rasterio.mask import mask
from rasterstats import zonal_stats
import numpy as np
from shapely.geometry import Point, Polygon

def extract_raster_values_at_points():
    """
    Extract raster values at specific point locations.
    Handle coordinate system transformations and invalid points.
    """
    # Load point data
    points = gpd.read_file('data/vector/sampling_points.shp')
    
    # Load raster data
    raster_path = 'data/raster/phoenix_dem.tif'
    
    with rasterio.open(raster_path) as src:
        # Ensure CRS compatibility
        if points.crs != src.crs:
            points_transformed = points.to_crs(src.crs)
        else:
            points_transformed = points
        
        # Extract values at points
        extracted_values = []
        for idx, point in points_transformed.iterrows():
            try:
                # Get pixel coordinates
                row, col = src.index(point.geometry.x, point.geometry.y)
                
                # Read pixel value
                pixel_value = src.read(1)[row, col]
                extracted_values.append(pixel_value)
                
            except IndexError:
                # Point outside raster bounds
                extracted_values.append(np.nan)
        
        # Add extracted values to points dataframe
        points['raster_value'] = extracted_values
    
    return points

def zonal_statistics():
    """
    Calculate comprehensive zonal statistics for polygon areas.
    """
    # Load polygon data (e.g., administrative boundaries)
    polygons = gpd.read_file('data/vector/study_areas.shp')
    
    # Define rasters for analysis
    raster_files = {
        'elevation': 'data/raster/phoenix_dem.tif',
        'temperature': 'data/raster/phoenix_temperature.tif',
        'vegetation': 'data/raster/phoenix_ndvi.tif'  # Generated from earlier analysis
    }
    
    results = {}
    
    for raster_name, raster_path in raster_files.items():
        # Calculate zonal statistics
        stats = zonal_stats(
            polygons, 
            raster_path,
            stats=['count', 'min', 'max', 'mean', 'std', 'median'],
            nodata=np.nan
        )
        
        # Convert to DataFrame and merge with polygons
        stats_df = pd.DataFrame(stats)
        
        # Add statistics to polygon data with descriptive column names
        for stat in stats_df.columns:
            polygons[f'{raster_name}_{stat}'] = stats_df[stat]
        
        results[raster_name] = stats_df
    
    # YOUR IMPLEMENTATION: Add custom statistics (percentiles, variance)
    # YOUR IMPLEMENTATION: Handle areas with no data
    # YOUR IMPLEMENTATION: Calculate area-weighted statistics
    
    return polygons, results

def raster_vector_overlay_analysis():
    """
    Perform complex overlay analysis between raster and vector data.
    """
    # YOUR IMPLEMENTATION HERE
    pass

def land_cover_analysis():
    """
    Analyze land cover patterns within administrative boundaries.
    """
    # YOUR IMPLEMENTATION HERE
    pass
```

### Part 3: Advanced Applications and Integration (35 points)

#### 3.1 Comprehensive Raster-Vector Analysis Workflow (20 points)

**A. Environmental Impact Analysis (15 points)**

Create a complete environmental analysis workflow:

```python
# File: scripts/environmental_analysis.py
import rasterio
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from analysis.raster_processing import *
from analysis.raster_vector import *

def environmental_impact_analysis():
    """
    Comprehensive environmental impact analysis combining multiple data sources.
    
    Analysis components:
    1. Load and process multiple raster datasets
    2. Integrate with vector administrative boundaries
    3. Calculate environmental quality indices
    4. Identify areas of concern
    5. Generate comprehensive report
    """
    print("🌍 Starting Environmental Impact Analysis")
    
    # Step 1: Load and preprocess raster datasets
    datasets = {
        'elevation': 'data/raster/phoenix_dem.tif',
        'temperature': 'data/raster/phoenix_temperature.tif',
        'landcover': 'data/raster/phoenix_landcover.tif'
    }
    
    processed_rasters = {}
    for name, path in datasets.items():
        print(f"Processing {name} dataset...")
        
        with rasterio.open(path) as src:
            data = src.read(1)
            profile = src.profile
            
            # Apply appropriate processing for each dataset
            if name == 'elevation':
                # Calculate slope from elevation
                processed_data = calculate_slope(data, src.res[0])
            elif name == 'temperature':
                # Convert to heat index if needed
                processed_data = data  # Placeholder
            else:
                processed_data = data
            
            processed_rasters[name] = {
                'data': processed_data,
                'profile': profile,
                'src': src
            }
    
    # Step 2: Load administrative boundaries
    boundaries = gpd.read_file('data/vector/phoenix_boundaries.shp')
    
    # Step 3: Perform zonal analysis
    zonal_results = {}
    for boundary_idx, boundary in boundaries.iterrows():
        boundary_stats = {}
        
        for raster_name, raster_info in processed_rasters.items():
            # Calculate statistics for this boundary
            # YOUR IMPLEMENTATION: Mask raster by boundary polygon
            # YOUR IMPLEMENTATION: Calculate environmental metrics
            pass
        
        zonal_results[boundary['name']] = boundary_stats
    
    # Step 4: Calculate environmental quality index
    environmental_quality = assess_environmental_quality(zonal_results)
    
    # Step 5: Identify priority areas for intervention
    priority_areas = identify_priority_areas(environmental_quality)
    
    return environmental_quality, priority_areas

def assess_environmental_quality(zonal_results):
    """
    Calculate composite environmental quality index.
    """
    # YOUR IMPLEMENTATION HERE
    pass

def urban_heat_island_analysis():
    """
    Specific analysis for urban heat island effects.
    """
    # YOUR IMPLEMENTATION: Load temperature and land cover data
    # YOUR IMPLEMENTATION: Calculate heat island intensity
    # YOUR IMPLEMENTATION: Correlate with urban development patterns
    pass
```

#### 3.2 Advanced Visualization and Reporting (15 points)

**B. Integrated Mapping and Reporting (15 points)**

Create professional visualizations and reports:

```python
# File: analysis/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
import folium
from matplotlib.colors import ListedColormap

def create_integrated_maps():
    """
    Create comprehensive maps integrating raster and vector analysis results.
    """
    # Set up the plotting environment
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 3, figsize=(24, 16))
    
    # Map 1: Digital Elevation Model
    ax1 = axes[0, 0]
    with rasterio.open('data/raster/phoenix_dem.tif') as src:
        elevation = src.read(1)
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
    
    im1 = ax1.imshow(elevation, extent=extent, cmap='terrain', alpha=0.8)
    ax1.set_title('Digital Elevation Model', fontsize=14, fontweight='bold')
    plt.colorbar(im1, ax=ax1, label='Elevation (m)')
    
    # Map 2: Temperature Analysis
    ax2 = axes[0, 1]
    # YOUR IMPLEMENTATION: Temperature raster visualization
    
    # Map 3: NDVI/Vegetation
    ax3 = axes[0, 2]
    # YOUR IMPLEMENTATION: Vegetation index visualization
    
    # Map 4: Integrated Analysis Results
    ax4 = axes[1, 0]
    # YOUR IMPLEMENTATION: Environmental quality index
    
    # Map 5: Statistical Analysis
    ax5 = axes[1, 1]
    # YOUR IMPLEMENTATION: Zonal statistics visualization
    
    # Map 6: Priority Areas
    ax6 = axes[1, 2]
    # YOUR IMPLEMENTATION: Priority areas for intervention
    
    # Add basemaps using contextily
    for ax in axes.flat:
        ax.set_aspect('equal')
        # Add basemap if coordinate systems align
        try:
            ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)
        except:
            pass  # Skip if basemap can't be added
    
    plt.tight_layout()
    plt.savefig('output/maps/integrated_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('output/maps/integrated_analysis.pdf', bbox_inches='tight')
    
    return fig

def create_interactive_map():
    """
    Create interactive web map using Folium.
    """
    # Center on Phoenix
    phoenix_center = [33.4484, -112.0740]
    
    # Create base map
    m = folium.Map(location=phoenix_center, zoom_start=10)
    
    # Add raster overlays
    # YOUR IMPLEMENTATION: Add processed raster layers
    # YOUR IMPLEMENTATION: Add vector boundary overlays
    # YOUR IMPLEMENTATION: Add analysis results with popups
    
    # Save interactive map
    m.save('output/maps/interactive_analysis.html')
    
    return m

def generate_comprehensive_report():
    """
    Generate automated comprehensive analysis report.
    """
    report_content = {
        'executive_summary': '',
        'methodology': '',
        'results': '',
        'recommendations': '',
        'technical_appendix': ''
    }
    
    # YOUR IMPLEMENTATION: Generate each report section
    # YOUR IMPLEMENTATION: Include statistics and visualizations
    # YOUR IMPLEMENTATION: Export as formatted PDF
    
    return report_content
```

---

## Deliverables

### 1. Complete uv Project Directory
Submit your entire project with professional organization:

**Core Analysis Components:**
- Complete raster processing modules with comprehensive documentation
- STAC integration with error handling and fallback mechanisms
- Memory-efficient windowed processing implementations
- Advanced raster-vector integration workflows
- Performance optimization with benchmarking results

**Project Infrastructure:**
- `pyproject.toml` with comprehensive dependency specifications
- `uv.lock` ensuring reproducible environments
- Comprehensive testing suite covering edge cases
- Configuration files for different analysis scenarios
- Professional README with usage examples and troubleshooting

### 2. Technical Implementation Report (5-6 pages)
Submit comprehensive technical documentation:

**Advanced Implementation Section (35%)**
- Rasterio architecture and optimization strategies employed
- COG processing workflows and performance benefits demonstrated
- STAC integration implementation with error handling approaches
- Memory management strategies for large-scale raster processing
- Innovation in raster-vector integration methodologies

**Scientific Analysis Section (40%)**
- Environmental analysis methodology and statistical validation
- Comparison of processing approaches with performance benchmarks  
- Spatial pattern analysis results with statistical significance testing
- Quality assessment of remote sensing data integration
- Limitations analysis and uncertainty quantification

**Technical Innovation Section (25%)**
- Advanced raster processing techniques beyond basic requirements
- Novel applications of COG and STAC workflows
- Creative solutions to memory and performance challenges
- Integration innovations combining multiple data sources
- Professional deployment considerations and scalability

### 3. Reproducibility and Deployment Package
Provide complete instructions for reproducing your analysis:

**Environment Reproduction:**
```bash
# Clone project directory
cd rasterio-analysis

# Install exact environment
uv sync

# Verify installation
uv run python -c "import rasterio, geopandas, pystac_client; print('Environment ready')"
```

**Data Pipeline Execution:**
```bash
# Generate or download source data
uv run python setup_raster_data.py

# Run complete analysis pipeline
uv run python run_analysis.py

# Execute individual analysis components
uv run python scripts/environmental_analysis.py
uv run python scripts/process_satellite_data.py

# Generate all visualizations
uv run jupyter notebook notebooks/

# Run quality assurance tests
uv run pytest tests/ -v --memory-profiler
```

**Performance Validation:**
- Include benchmark results for different processing approaches
- Memory usage profiles for large dataset operations
- Timing comparisons demonstrating optimization effectiveness
- Validation of remote vs local processing strategies

---

## Evaluation Criteria

### Technical Excellence (40%)
**A-Level (36-40 points):**
- Sophisticated implementation using advanced rasterio and STAC features
- Effective memory optimization with measurable performance improvements
- Robust error handling for network, memory, and data quality issues
- Professional code architecture with comprehensive testing
- Innovation in processing workflows and optimization techniques

**B-Level (32-35 points):**
- Correct implementation of core raster processing requirements
- Basic optimization with documented performance improvements
- Adequate error handling for common failure scenarios
- Well-organized code with good documentation and testing
- Standard implementation of COG and STAC workflows

**C-Level (28-31 points):**
- Functional implementation meeting minimum requirements
- Some optimization attempts with limited performance gains
- Basic error handling with incomplete edge case coverage
- Adequate code organization with minimal documentation
- Basic raster processing without advanced features

### Spatial Analysis Quality (35%)
**A-Level (32-35 points):**
- Sophisticated environmental analysis revealing meaningful insights
- Advanced statistical validation of raster-vector integration
- Professional-quality results suitable for decision-making
- Innovative applications of remote sensing techniques
- Comprehensive uncertainty analysis and quality assessment

**B-Level (28-31 points):**
- Solid raster analysis meeting all core requirements
- Effective raster-vector integration with appropriate statistical methods
- Clear interpretation of results with adequate validation
- Professional presentation of environmental findings
- Standard remote sensing analysis techniques

**C-Level (24-27 points):**
- Basic raster analysis meeting minimum requirements
- Simple raster-vector integration with limited validation
- Adequate interpretation of results with minimal statistical analysis
- Basic environmental assessment with standard techniques
- Limited depth in spatial pattern analysis

### Innovation and Professional Development (25%)
**A-Level (23-25 points):**
- Exceptional project organization and professional documentation
- Advanced integration with cloud-based raster workflows
- Innovative solutions to complex spatial analysis challenges
- Outstanding reproducibility and deployment strategies
- Professional-quality deliverables ready for operational use

**B-Level (20-22 points):**
- Good project organization with clear documentation
- Effective use of modern Python development practices
- Creative application of raster processing techniques
- Clear reproducibility with minor setup requirements
- Professional code quality and structure

**C-Level (17-19 points):**
- Adequate project organization meeting basic requirements
- Standard use of uv package management
- Basic application of raster processing techniques
- Minimal reproducibility documentation
- Functional code with limited professional polish

---

## Professional Development Integration

### Industry-Relevant Skills Developed
- **Remote Sensing Operations**: Cloud-based satellite imagery processing
- **Big Data GIS**: Memory-efficient processing of large spatial datasets
- **API Integration**: Professional STAC and cloud data access workflows
- **Performance Engineering**: Optimization techniques for spatial processing
- **DevOps Integration**: Reproducible environments and deployment strategies

### Real-World Applications
The techniques learned directly apply to:
- **Environmental Monitoring**: Satellite-based change detection and assessment
- **Urban Planning**: Heat island analysis and development impact assessment
- **Agriculture**: Crop monitoring and yield prediction using vegetation indices
- **Emergency Response**: Rapid damage assessment using satellite imagery
- **Climate Research**: Long-term environmental trend analysis
- **Resource Management**: Land cover change monitoring and assessment

### Career Preparation
- **GIS Analyst**: Advanced raster processing and remote sensing skills
- **Data Scientist**: Large-scale spatial data processing and analysis
- **Software Developer**: Professional Python project management and testing
- **Environmental Consultant**: Quantitative environmental impact assessment
- **Research Scientist**: Reproducible spatial analysis workflows

---

## Resources and Support

### Core Documentation
- **Rasterio Documentation**: https://rasterio.readthedocs.io/en/latest/
- **STAC Specification**: https://stacspec.org/en/
- **Microsoft Planetary Computer**: https://planetarycomputer.microsoft.com/
- **Cloud-Optimized GeoTIFF**: https://www.cogeo.org/

### Advanced References
- **Raster Processing Patterns**: https://rasterio.readthedocs.io/en/latest/topics/
- **Performance Optimization**: https://docs.python.org/3.13/library/profile.html
- **Memory Management**: https://realpython.com/python-memory-management/
- **Scientific Computing**: SciPy and NumPy documentation for array operations

### Dataset Sources
- **Landsat Data**: USGS Earth Explorer and Planetary Computer
- **Sentinel Data**: Copernicus Open Access Hub and Planetary Computer
- **Digital Elevation**: USGS National Map and NASA SRTM
- **Environmental Data**: EPA and NOAA environmental datasets

### Getting Help
- **Office Hours**: Bring specific raster processing and performance questions
- **Discussion Forum**: Share code snippets and optimization strategies
- **Study Groups**: Collaborate on complex environmental analysis workflows
- **Online Communities**: Stack Overflow and GIS Stack Exchange for troubleshooting

---

## Submission Instructions

### File Organization and Submission
1. **Project Archive**: `LastName_FirstName_Rasterio_Analysis.zip`
   - Complete uv project directory with all analysis components
   - Generated outputs including processed rasters and visualizations
   - Performance benchmarks and memory usage reports
   - Test results demonstrating code quality and functionality

2. **Technical Report**: `LastName_FirstName_Raster_Report.pdf`
   - Professional formatting with embedded figures and maps
   - Complete methodology, results, and technical innovation sections
   - Performance analysis with benchmarks and optimization results
   - Professional conclusions and recommendations

### Quality Assurance Checklist
Before submission, verify all components:
- [ ] `uv sync` successfully reproduces exact environment
- [ ] All analysis scripts execute without errors: `uv run python run_analysis.py`
- [ ] Memory profiling demonstrates optimization: `uv run python -m memory_profiler scripts/process_satellite_data.py`
- [ ] Unit tests pass completely: `uv run pytest tests/ -v`
- [ ] Code formatting consistent: `uv run black analysis/ scripts/`
- [ ] Interactive notebooks run end-to-end without errors
- [ ] All output files generate correctly with expected results
- [ ] Technical report addresses all required sections comprehensively

### Performance Documentation
Include comprehensive performance analysis:
- Memory usage profiles for different dataset sizes
- Processing time comparisons for optimization techniques
- Network performance analysis for remote COG access
- Statistical validation of processing accuracy and precision

### Submission Method
- **Platform**: Course Learning Management System
- **Due Date**: [Insert specific deadline]
- **File Size**: Ensure compressed archive is under platform limits
- **Backup**: Keep local copy until grades are confirmed

---

## Course Integration and Preparation

### Building on Previous Work
This assignment directly integrates:
- **Package Management**: Advanced uv project workflows from recent lectures
- **Vector Analysis**: GeoPandas spatial operations from previous assignments
- **Spatial Joins**: Integration techniques from spatial joins assignment
- **Professional Development**: Modern Python practices throughout course

### Preparing for Future Modules
Skills developed here prepare for:
- **PostGIS Integration**: Database-backed raster storage and processing
- **Web GIS Development**: Server-side raster processing and visualization
- **Advanced Automation**: PyQGIS integration with raster workflows
- **Production Deployment**: Scalable spatial analysis system design

### Integration with Course Capstone
Raster processing skills contribute to capstone project options:
- **Environmental Monitoring System**: Real-time satellite data processing
- **Urban Analytics Platform**: Multi-source spatial data integration
- **Emergency Response Tools**: Rapid damage assessment capabilities
- **Research Data Pipeline**: Reproducible environmental analysis workflows

This assignment represents a significant advancement in spatial analysis capabilities, combining cutting-edge remote sensing techniques with professional software development practices essential for modern GIS careers. The focus on cloud-optimized workflows and scalable processing techniques prepares students for the evolving landscape of spatial data science and professional GIS development.