# Rasterio Analysis Assignment - Advanced Raster Processing and Analysis

## 🎯 Assignment Overview

Welcome to the **Rasterio Analysis** assignment! This advanced assignment will teach you professional-level raster processing and analysis techniques used in environmental monitoring, natural hazard assessment, and modern geospatial workflows.

You'll implement **5 comprehensive analytical functions** that demonstrate real-world applications of raster data processing:

1. **`calculate_topographic_metrics`** - Terrain analysis (slope, aspect, hillshade)
2. **`analyze_vegetation_indices`** - Remote sensing analysis (NDVI, EVI, vegetation health)
3. **`sample_raster_at_locations`** - Spatial sampling with interpolation methods
4. **`process_cloud_optimized_geotiff`** - Efficient cloud-based data processing
5. **`query_stac_and_analyze`** - Modern data discovery and temporal analysis

### 🌟 Why This Assignment Matters

These skills are essential for:
- **Environmental Monitoring:** Track vegetation health and land cover changes
- **Natural Hazard Analysis:** Assess slope stability and flood risk
- **Climate Research:** Analyze temporal patterns in satellite data
- **Urban Planning:** Evaluate terrain suitability and accessibility
- **Agricultural Applications:** Monitor crop health and yield prediction

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- GitHub Codespaces (recommended) or local Python environment
- Basic understanding of raster data concepts

### Environment Setup

**Option 1: GitHub Codespaces (Recommended)**
1. Click the green "Code" button → "Codespaces" → "Create codespace on main"
2. Wait for the environment to initialize (2-3 minutes)
3. Open a terminal and run: `python -m pip install --upgrade pip`

**Option 2: Local Development**
```bash
# Install dependencies
pip install rasterio numpy matplotlib geopandas shapely
pip install pystac pystac-client requests aiohttp
pip install pytest pytest-cov pytest-html

# Clone and navigate to assignment
git clone <your-repo-url>
cd rasterio-analysis
```

### Verify Your Setup

```bash
# Test imports
python -c "import rasterio, numpy as np, matplotlib.pyplot as plt, pystac; print('✅ All packages imported successfully!')"

# Run a quick test
pytest tests/ -v --tb=short
```

## 📁 Understanding Your Files

```
rasterio-analysis/
├── src/
│   └── rasterio_analysis.py      # 🎯 YOUR MAIN WORK FILE
├── notebooks/                    # 📚 Learning materials
│   ├── 01_topographic_metrics.ipynb
│   ├── 02_vegetation_indices.ipynb
│   ├── 03_spatial_sampling.ipynb
│   ├── 04_cloud_optimized_geotiffs.ipynb
│   └── 05_stac_integration.ipynb
├── tests/                        # 🧪 Automated tests
│   ├── test_topographic_metrics.py
│   ├── test_vegetation_indices.py
│   ├── test_spatial_sampling.py
│   ├── test_cog_processing.py
│   └── test_stac_analysis.py
├── data/                         # 📊 Sample datasets
└── README.md                     # 📖 This file
```

## 📝 Your Assignment Tasks

### Function 1: `calculate_topographic_metrics` (5 points)

**Purpose:** Calculate comprehensive topographic metrics from Digital Elevation Models (DEMs)

**What You'll Learn:**
- Slope and aspect calculation using gradient methods
- Hillshade generation for terrain visualization  
- Terrain classification based on slope thresholds
- Edge effect handling in raster processing

**Key Requirements:**
- Calculate slope in degrees using `np.gradient()`
- Calculate aspect in 0-360° compass bearing
- Generate hillshade with customizable sun position
- Classify terrain: flat, gentle, moderate, steep, very steep
- Handle nodata values and edge effects properly

**📓 Learning Notebook:** `notebooks/01_topographic_metrics.ipynb`

### Function 2: `analyze_vegetation_indices` (5 points)

**Purpose:** Calculate and analyze vegetation indices from multispectral imagery

**What You'll Learn:**
- NDVI and EVI calculation and interpretation
- Vegetation health assessment techniques
- Land cover classification from spectral indices
- Remote sensing data quality evaluation

**Key Requirements:**
- Calculate NDVI: `(NIR - Red) / (NIR + Red)`
- Calculate EVI: `2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))`
- Classify vegetation health and density
- Create land cover masks (water, vegetation, bare soil)
- Handle division by zero and invalid spectral values

**📓 Learning Notebook:** `notebooks/02_vegetation_indices.ipynb`

### Function 3: `sample_raster_at_locations` (5 points)

**Purpose:** Extract raster values at specific geographic locations with various sampling methods

**What You'll Learn:**
- Point sampling with different interpolation methods
- Buffered sampling for area-based extraction
- Coordinate transformation between CRS systems
- Statistical analysis of sampled data

**Key Requirements:**
- Support point sampling (buffer_radius=0) and buffered sampling
- Implement nearest neighbor and bilinear interpolation
- Handle coordinate transformation automatically
- Calculate buffer statistics (mean, std, min, max)
- Manage locations outside raster bounds gracefully

**📓 Learning Notebook:** `notebooks/03_spatial_sampling.ipynb`

### Function 4: `process_cloud_optimized_geotiff` (5 points)

**Purpose:** Efficiently process Cloud Optimized GeoTIFFs with modern techniques

**What You'll Learn:**
- COG structure analysis and optimization benefits
- Windowed reading for efficient data access
- Overview level selection for different resolutions
- Performance metrics and data transfer optimization

**Key Requirements:**
- Analyze COG structure (tiling, overviews, compression)
- Implement efficient windowed reading
- Select optimal overview levels based on resolution/bounds
- Calculate processing efficiency metrics
- Support both local and remote COG access

**📓 Learning Notebook:** `notebooks/04_cloud_optimized_geotiffs.ipynb`

### Function 5: `query_stac_and_analyze` (5 points)

**Purpose:** Query STAC catalogs and perform temporal analysis on satellite imagery

**What You'll Learn:**
- STAC catalog structure and search capabilities
- Temporal data analysis and time series creation
- Change detection methodologies
- Cloud-based satellite data workflows

**Key Requirements:**
- Use `pystac_client` to search STAC catalogs
- Filter by spatial, temporal, and collection criteria
- Implement NDVI time series analysis
- Assess data quality and coverage gaps
- Handle network errors and missing data gracefully

**📓 Learning Notebook:** `notebooks/05_stac_integration.ipynb`

## 🧪 Testing and Development Workflow

### Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific function tests
pytest tests/test_topographic_metrics.py -v
pytest tests/test_vegetation_indices.py -v
pytest tests/test_spatial_sampling.py -v
pytest tests/test_cog_processing.py -v
pytest tests/test_stac_analysis.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Understanding Test Results

- ✅ **GREEN (PASSED):** Your function works correctly
- ❌ **RED (FAILED):** Function has issues - check the error message
- ⚪ **YELLOW (SKIPPED):** Test requires resources not available

### GitHub Actions Grading

Every time you push code, automated tests run and calculate your grade:

- **Total Points:** 25 (5 per function)
- **Grade Scale:** A (90%+), B (80%+), C (70%+), D (60%+), F (<60%)
- **Test Categories:** Each function has comprehensive test coverage

## 📊 Sample Data and Resources

### Built-in Test Data
The assignment includes synthetic test data for all functions. Real-world examples are provided in the notebooks.

### External Data Sources
- **USGS 3DEP:** Digital Elevation Models
- **Landsat/Sentinel:** Multispectral imagery
- **Microsoft Planetary Computer:** STAC catalog
- **AWS Open Data:** Cloud Optimized GeoTIFFs

### Working with Large Datasets
```python
# Example: Process a large DEM efficiently
result = calculate_topographic_metrics('large_dem.tif', output_dir='outputs/')

# Example: Sample Landsat data at field locations  
locations = [(-120.5, 37.8), (-121.0, 37.5)]
samples = sample_raster_at_locations('landsat8.tif', locations, buffer_radius=100)

# Example: Query recent Sentinel-2 data
bbox = (-120.5, 37.5, -120.0, 38.0)
results = query_stac_and_analyze(
    'https://earth-search.aws.element84.com/v1',
    bbox, '2023-01-01/2023-12-31', ['sentinel-2-l2a']
)
```

## 🛠️ Troubleshooting

### Common Issues

**ImportError: Cannot import function**
```bash
# Make sure you're in the right directory
cd rasterio-analysis
python -c "import sys; print(sys.path)"
```

**GDAL/Rasterio installation issues**
```bash
# In Codespaces, restart the container
# Locally, reinstall with conda:
conda install -c conda-forge rasterio gdal
```

**Tests failing with "Function not implemented"**
- Check that your function returns a dictionary with all required keys
- Make sure function names match exactly: `calculate_topographic_metrics`
- Verify your function handles edge cases and invalid inputs

**Memory issues with large rasters**
- Use windowed reading: `rasterio.windows.from_bounds()`
- Process data in chunks rather than loading entire raster
- Consider using appropriate overview levels for COGs

### Getting Help

1. **Read the error messages carefully** - they contain valuable debugging information
2. **Check the Jupyter notebooks** - they contain step-by-step examples
3. **Review the test files** - they show exactly what your functions should return
4. **Use the discussion forum** for assignment-related questions
5. **Attend office hours** for personalized help

## 📤 Submission Requirements

### What Gets Graded
- **Automated Tests (100%):** Your functions must pass the comprehensive test suite
- **Code Quality:** Functions should be well-documented and handle errors gracefully
- **Performance:** Efficient processing of raster data

### Submission Checklist
- [ ] All 5 functions implemented in `src/rasterio_analysis.py`
- [ ] Functions pass local tests: `pytest tests/ -v`
- [ ] GitHub Actions workflow shows passing tests
- [ ] Code is well-commented and follows good practices

### Final Push
```bash
git add .
git commit -m "Complete rasterio analysis assignment - all functions implemented"
git push origin main
```

Check your GitHub Actions tab to see your final grade!

## 🎓 Professional Skills Assessment

This assignment evaluates your proficiency in:

### Technical Skills
- **Advanced Raster Processing:** Complex analytical operations on geospatial data
- **Remote Sensing Applications:** Vegetation monitoring and change detection
- **Spatial Analysis:** Point sampling, buffering, and interpolation techniques
- **Modern GIS Workflows:** COG processing and STAC catalog integration
- **Performance Optimization:** Efficient handling of large geospatial datasets

### Professional Competencies  
- **Problem Solving:** Implementing complex analytical algorithms
- **Code Quality:** Writing maintainable, well-documented functions
- **Error Handling:** Robust data processing with graceful failure modes
- **Testing:** Understanding and working with comprehensive test suites
- **Documentation:** Clear communication of technical concepts

## 🌍 Real-World Applications

Upon completion, you'll be able to:

### Environmental Monitoring
- Monitor vegetation health across landscapes using satellite imagery
- Track changes in forest cover and agricultural productivity
- Assess environmental impacts of development projects

### Natural Hazard Analysis  
- Calculate slope stability and landslide susceptibility
- Model flood risk using terrain analysis
- Evaluate fire risk based on topographic exposure

### Climate Research
- Analyze long-term trends in satellite observations
- Create time series of environmental indicators
- Assess impacts of climate change on ecosystems

### Urban and Regional Planning
- Evaluate terrain suitability for development
- Plan infrastructure based on topographic constraints
- Optimize placement of renewable energy installations

## 📚 Additional Resources

### Documentation
- [Rasterio Documentation](https://rasterio.readthedocs.io/)
- [STAC Specification](https://stacspec.org/)
- [Cloud Optimized GeoTIFF](https://cogeo.org/)

### Professional Development
- [GDAL/OGR Documentation](https://gdal.org/)
- [Remote Sensing Tutorial](https://www.earthdatascience.org/)
- [Modern Geospatial Workflows](https://guide.cloudnativegeo.org/)

### Data Sources
- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- [AWS Open Data](https://aws.amazon.com/opendata/)
- [Google Earth Engine](https://earthengine.google.com/)

---

## 🎉 Ready to Begin?

Start with the **Jupyter notebooks** to understand each function, then implement them in `src/rasterio_analysis.py`. Remember: this assignment represents **professional-level geospatial analysis skills** that are highly valued in environmental science, remote sensing, and GIS industries.

**Good luck, and enjoy exploring the power of advanced raster analysis! 🗻🛰️📊**