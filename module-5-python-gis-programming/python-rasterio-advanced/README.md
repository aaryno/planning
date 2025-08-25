# Python Rasterio Advanced Processing - Automated Assessment

**Course:** GIST 604B - Open Source GIS Programming  
**Assignment:** Advanced Raster Processing with Cloud-Optimized Workflows  
**Points:** 30 total  
**Estimated Time:** 12-15 hours over 2 weeks  

---

## ⚠️ IMPORTANT: Windows Users Read This First!

**This assignment involves advanced raster processing that works best in Unix-like environments (Linux/macOS).** While Python and rasterio can run on Windows, many geospatial tools and workflows in the open-source ecosystem are designed with Unix systems in mind.

**The instructor cannot provide Windows-specific troubleshooting support** for environment setup, path issues, or system-specific problems. If you're on Windows, please read the environment setup section carefully and consider using GitHub Codespaces for the best experience.

---

## 🎯 Assignment Overview

This assignment focuses on **advanced raster data processing** using Python's rasterio library, emphasizing modern cloud-based workflows with Cloud-Optimized GeoTIFFs (COGs), Spatio-Temporal Asset Catalog (STAC) integration, and efficient large-scale raster analysis. You'll build sophisticated raster processing pipelines that integrate with vector data analysis, implementing memory-efficient workflows suitable for production GIS environments.

### 🔑 Key Learning Innovation

Building on your GeoPandas spatial analysis skills, you'll learn to work with satellite imagery, digital elevation models, and other raster datasets using modern Python development practices and cloud-optimized data formats essential for contemporary remote sensing and GIS applications.

### 📋 Prerequisites

- ✅ Completed Python GeoPandas assignments
- ✅ Understanding of coordinate reference systems and map projections  
- ✅ Basic knowledge of remote sensing concepts
- ✅ Familiarity with NumPy arrays and mathematical operations

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
Accept the GitHub Classroom assignment link provided by your instructor. This will create your personal repository with the starter code and automated grading setup.

### Step 2: Choose Your Development Environment

**Option A: GitHub Codespaces (🌟 RECOMMENDED for Windows users)**
```bash
# Click "Code" → "Codespaces" → "Create codespace" in your GitHub repo
# Everything will be pre-configured and ready to use!
```

**Option B: Local Development (Advanced users, Unix systems preferred)**
```bash
# Clone your repository
git clone <your-repo-url>
cd python-rasterio-advanced

# Install uv package manager if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### Step 3: Verify Your Environment
```bash
# Test raster processing imports
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

# Run the environment setup script
uv run python setup_student_environment.py
```

---

## 🖥️ Important: Development Environment Considerations

### Windows Users - Please Read Carefully!

**The Challenge:** Advanced raster processing involves complex geospatial libraries (GDAL, PROJ, GEOS) that have intricate system dependencies. These libraries were originally designed for Unix systems and can be challenging to configure properly on Windows.

**Common Windows Issues:**
- GDAL/rasterio installation problems
- Path separator conflicts (`\` vs `/`)
- Missing system libraries (especially for COG optimization)
- Memory mapping issues with large rasters
- Network access problems for STAC APIs

### ✅ Recommended Solution: Use GitHub Codespaces

**Why Codespaces is Perfect for This Assignment:**
- ✨ **Pre-configured environment** with all geospatial libraries properly installed
- 🌐 **Cloud-based processing** ideal for working with remote satellite data
- 🔧 **Unix environment** where rasterio and GDAL work optimally
- 💾 **Persistent storage** for your code and generated raster data
- 🚀 **No installation headaches** - just click and start coding

**To use Codespaces:**
1. Go to your GitHub repository
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

### 🪟 If You Choose Local Windows Development

**You'll need to handle:**
- Complex conda/pip environment setup for geospatial packages
- Potential GDAL configuration issues
- Windows-specific path handling in your code
- Memory limitations for large raster processing
- Firewall/network configurations for STAC API access

**Windows-specific code examples:**
```python
# Use pathlib for cross-platform paths
from pathlib import Path
raster_path = Path("data") / "rasters" / "dem.tif"

# Handle Windows memory limitations
import psutil
if psutil.virtual_memory().total < 8 * 1024**3:  # Less than 8GB
    use_chunked_processing = True
```

### ⚠️ Important Disclaimer

**The instructor cannot provide Windows-specific support** for:
- rasterio/GDAL installation problems  
- Windows path or file permission issues
- Memory management problems specific to Windows
- Network/firewall configuration for STAC APIs
- Performance optimization on Windows systems

If you encounter Windows-specific issues, you have these options:
1. **Switch to Codespaces** (strongly recommended)
2. Seek help from Windows-experienced classmates
3. Use university lab computers with Linux/macOS

### 💡 Bottom Line for Windows Users

**Use Codespaces.** It will save you hours of troubleshooting and let you focus on learning advanced raster processing concepts rather than fighting with environment setup.

---

## 📁 Project Structure

Your completed project will follow this structure:
```
python-rasterio-advanced/
├── 📄 README.md                    # This file - assignment instructions
├── 📄 pyproject.toml              # Project dependencies and configuration
├── 📄 uv.lock                     # Locked dependency versions  
├── 📁 src/rasterio_analysis/      # Your main analysis modules
│   ├── 📄 __init__.py
│   ├── 📄 raster_processing.py    # Core raster operations [PART 1]
│   ├── 📄 cog_operations.py       # COG-specific functionality [PART 1] 
│   ├── 📄 stac_integration.py     # STAC API integration [PART 2]
│   ├── 📄 windowed_processing.py  # Memory-efficient processing [PART 3]
│   └── 📄 raster_vector.py        # Raster-vector integration [PART 3]
├── 📁 notebooks/                  # Interactive analysis notebooks
│   ├── 📓 01_raster_basics.ipynb           # Basic rasterio operations
│   ├── 📓 02_cog_processing.ipynb          # COG creation and validation
│   ├── 📓 03_stac_satellite_data.ipynb     # STAC API usage
│   ├── 📓 04_memory_efficient.ipynb       # Large raster processing
│   └── 📓 05_raster_vector_integration.ipynb # Combined workflows
├── 📁 data/                       # Raster and vector datasets
│   ├── 📁 raster/                # Local raster files
│   ├── 📁 vector/                # Vector data for integration
│   └── 📁 processed/             # Your processed outputs
├── 📁 tests/                     # Unit tests (auto-graded)
│   ├── 📄 test_raster_processing.py
│   ├── 📄 test_cog_operations.py
│   ├── 📄 test_stac_integration.py
│   └── 📄 test_windowed_processing.py
├── 📁 .github/workflows/         # Automated grading CI/CD
│   └── 📄 raster-analysis-pipeline.yml
└── 📄 setup_student_environment.py # Environment verification script
```

---

## 📝 Assignment Tasks

### 🗺️ Part 1: Advanced Raster Processing & COG Operations (12 points)

**What you'll implement:**
- `analyze_local_raster()` - Comprehensive raster metadata and statistics analysis
- `process_multiband_imagery()` - Vegetation indices (NDVI, EVI) from satellite data
- `process_remote_cog()` - Efficient COG reading with bbox subsetting 
- `create_optimized_cog()` - COG creation with tiling and compression
- `validate_cog()` - COG compliance checking and optimization recommendations

**Key concepts:**
- Raster metadata extraction and quality assessment
- Multispectral band mathematics and vegetation indices
- Cloud-Optimized GeoTIFF format and optimization
- Remote raster access patterns and performance

### 🛰️ Part 2: STAC Integration & Satellite Data Access (8 points)

**What you'll implement:**
- `search_satellite_imagery()` - STAC API queries with spatial/temporal/cloud filters
- `load_stac_data_as_array()` - Efficient satellite data loading with stackstac
- `analyze_vegetation_time_series()` - NDVI time series analysis and trend detection
- `compare_seasonal_changes()` - Seasonal vegetation pattern analysis

**Key concepts:**
- STAC API usage for Earth observation data discovery
- Satellite imagery processing workflows
- Time series analysis of vegetation health
- Seasonal phenology and environmental monitoring

### 🚀 Part 3: Memory-Efficient Processing & Integration (10 points)

**What you'll implement:**
- `process_large_raster_windowed()` - Windowed processing for memory efficiency
- `calculate_ndvi_safe()` - Safe NDVI calculation with error handling
- `extract_raster_values_at_points()` - Point-based raster sampling
- `zonal_statistics()` - Polygon-based raster statistics
- `environmental_impact_analysis()` - Comprehensive raster-vector workflow

**Key concepts:**
- Memory-efficient windowed raster processing
- Raster-vector integration techniques
- Zonal statistics and spatial sampling
- Production-ready error handling and optimization

---

## 🤖 Automated Grading System

### 📊 Grade Breakdown (30 points total)

- **Part 1: Raster Processing & COG (12 pts)**
  - Local raster analysis (3 pts)
  - Multiband processing & indices (3 pts)  
  - COG processing & validation (3 pts)
  - COG creation & optimization (3 pts)

- **Part 2: STAC Integration (8 pts)**
  - STAC search implementation (2 pts)
  - Satellite data loading (2 pts)
  - Time series analysis (2 pts)
  - Seasonal comparison (2 pts)

- **Part 3: Advanced Processing (10 pts)**
  - Windowed processing (3 pts)
  - Raster-vector integration (3 pts)
  - Environmental analysis workflow (4 pts)

### 🔄 Raster CI/CD Pipeline Steps

When you push code to GitHub, the automated system will:

1. **🔧 Environment Setup**
   - Install Python 3.13 and uv package manager
   - Install all geospatial dependencies (GDAL, rasterio, etc.)
   - Set up test raster datasets

2. **📊 Raster Processing Tests**
   - Test basic rasterio operations and metadata extraction
   - Validate COG creation and optimization functions
   - Check vegetation index calculations (NDVI, EVI)

3. **🛰️ STAC Integration Tests**  
   - Test STAC API connectivity and search functions
   - Validate satellite data loading and processing
   - Check time series analysis implementations

4. **🚀 Advanced Processing Tests**
   - Test windowed processing for memory efficiency
   - Validate raster-vector integration workflows
   - Check environmental analysis pipeline

5. **📈 Performance Validation**
   - Memory usage profiling for large rasters
   - Processing time benchmarks
   - COG optimization effectiveness measurement

---

## 💻 Development Workflow - The Raster Analysis Cycle

### 🧪 Interactive Development Process

1. **Start with Jupyter notebooks** to experiment and visualize
2. **Develop functions** in the source modules
3. **Test with real data** using provided raster datasets  
4. **Validate with unit tests** to ensure correctness
5. **Optimize for performance** and memory efficiency

### 🔧 Local Development Commands

```bash
# Interactive development and testing
uv run jupyter lab                    # Start Jupyter for interactive work
uv run python -m pytest tests/ -v    # Run all tests with verbose output
uv run python -m pytest tests/test_raster_processing.py -v # Test specific module

# Code quality and formatting
uv run black src/ tests/             # Format code
uv run ruff check src/ tests/        # Check code quality
uv run mypy src/                     # Type checking

# Performance profiling
uv run python -m memory_profiler scripts/profile_raster_processing.py
uv run python -c "from src.rasterio_analysis.raster_processing import analyze_local_raster; analyze_local_raster('data/raster/phoenix_dem.tif')"
```

### 📈 Interactive Workflow Example

```python
# In Jupyter notebook - experiment first
import rasterio
import numpy as np
from src.rasterio_analysis.raster_processing import analyze_local_raster

def test_raster_analysis():
    """Test raster analysis with real data."""
    result = analyze_local_raster('data/raster/phoenix_dem.tif')
    print(f"Raster dimensions: {result['dimensions']}")
    print(f"Data completeness: {result['statistics']['data_completeness']:.1f}%")
    return result

# Run and visualize
analysis_result = test_raster_analysis()
```

### 🔄 Typical Development Day

1. **Morning:** Work in Jupyter notebooks, experiment with new raster processing techniques
2. **Afternoon:** Implement functions in source modules, run unit tests  
3. **Evening:** Push to GitHub, review automated feedback, iterate

---

## 📊 Understanding Your Raster Analysis Grade

### 🎯 Grade Thresholds
- **A (90-100%):** Excellent raster processing implementation with advanced features
- **B (80-89%):** Good implementation meeting all core requirements
- **C (70-79%):** Satisfactory implementation with minor issues
- **D (60-69%):** Basic implementation with significant gaps
- **F (<60%):** Incomplete or non-functional implementation

### 📝 Reading Raster Analysis Feedback

**✅ Success indicators:**
```
✓ test_analyze_local_raster PASSED - Correct metadata extraction and statistics
✓ test_create_optimized_cog PASSED - Valid COG with proper tiling and compression  
✓ test_stac_search PASSED - Successful satellite imagery discovery
✓ test_windowed_processing PASSED - Memory-efficient large raster processing
```

**❌ Common issues and solutions:**

```
✗ test_process_multiband_imagery FAILED - Division by zero in NDVI calculation
```
**Fix:** Add proper error handling for invalid pixels:
```python
# Safe NDVI calculation
with np.errstate(divide='ignore', invalid='ignore'):
    ndvi = (nir - red) / (nir + red)
    ndvi = np.where(np.isfinite(ndvi), ndvi, np.nan)
```

```
✗ test_cog_validation FAILED - COG missing overview pyramids
```
**Fix:** Generate overviews after COG creation:
```python
with rasterio.open(cog_path, 'r+') as dst:
    overview_factors = [2, 4, 8, 16]
    dst.build_overviews(overview_factors, Resampling.average)
```

```
✗ test_stac_integration FAILED - Network timeout accessing satellite data  
```
**Fix:** Add proper error handling and retries:
```python
try:
    items = list(catalog.search(**search_params).items())
except requests.RequestException as e:
    logger.warning(f"STAC search failed: {e}")
    return {'items': [], 'error': str(e)}
```

---

## 🛠️ Troubleshooting Raster Issues

### 🪟 Windows-Specific Issues (Use Codespaces Instead!)

**Problem:** `ImportError: No module named 'rasterio._shim'`
```bash
# This indicates GDAL installation problems on Windows
# Solution: Use Codespaces or properly configure conda environment
```

**Problem:** `WindowsError: [Error 5] Access is denied` when creating COG files  
```bash
# Windows file permission issues
# Solution: Run as administrator or use different output directory
```

**Problem:** Memory errors with large rasters on Windows
```python
# Windows has different memory management than Unix
# Reduce chunk sizes or use more aggressive windowed processing
process_large_raster_windowed(raster_path, chunk_size=512)  # Smaller chunks on Windows
```

### ❓ Common Raster Problems

**Q: "My NDVI values are all nan or infinity"**

A: Check for division by zero and invalid data:
```python
def calculate_ndvi_safe(red_band, nir_band, nodata_value=None):
    """Safe NDVI calculation with proper error handling."""
    # Mask nodata values
    if nodata_value is not None:
        valid_mask = (red_band != nodata_value) & (nir_band != nodata_value)
        red_band = np.where(valid_mask, red_band, np.nan)
        nir_band = np.where(valid_mask, nir_band, np.nan)
    
    # Safe division
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        ndvi = np.where(np.isfinite(ndvi), ndvi, np.nan)
    
    return ndvi
```

**Q: "COG validation fails even though I created tiled GeoTIFF"**

A: COGs require both tiling AND overviews:
```python
def create_proper_cog(input_path, output_path):
    # Step 1: Create tiled GeoTIFF
    profile = {
        'driver': 'GTiff',
        'tiled': True,
        'blockxsize': 512,
        'blockysize': 512,
        'compress': 'lzw'
    }
    
    # Step 2: Must also build overviews
    with rasterio.open(output_path, 'r+') as dst:
        overview_factors = [2, 4, 8, 16]
        dst.build_overviews(overview_factors, Resampling.average)
```

**Q: "STAC search returns no results even though data should exist"**

A: Check your search parameters:
```python
def debug_stac_search(bbox, datetime, collections):
    """Debug STAC search issues."""
    print(f"Searching: {collections}")
    print(f"Bbox: {bbox}")
    print(f"Time: {datetime}")
    
    # Try without restrictive filters first
    search = catalog.search(bbox=bbox, collections=collections, limit=10)
    items = list(search.items())
    print(f"Found {len(items)} items without date filter")
    
    # Then add date filter
    search = catalog.search(bbox=bbox, datetime=datetime, collections=collections)
    items = list(search.items())
    print(f"Found {len(items)} items with date filter")
```

**Q: "Out of memory error processing large rasters"**

A: Use windowed processing:
```python
def process_large_raster_windowed(raster_path, window_size=1024):
    """Process large rasters in chunks to avoid memory issues."""
    with rasterio.open(raster_path) as src:
        for window in src.block_windows():
            # Process each window separately
            data = src.read(window=window)
            processed = your_processing_function(data)
            # Write results incrementally
```

### 🆘 Getting Raster Analysis Help

1. **First:** Check the automated test feedback - it often points to specific issues
2. **Second:** Review the example implementations in the notebooks
3. **Third:** Test your functions interactively in Jupyter with small datasets
4. **Fourth:** Check the course discussion forum for similar issues
5. **Last resort:** Office hours (but try Codespaces if you're on Windows!)

---

## 📤 Submission Instructions

### 🎯 Final Submission Process

Your work is automatically submitted through GitHub. **No separate upload required!**

1. **Complete all functions** in the source modules
2. **Test your implementation** locally with `uv run pytest tests/ -v`  
3. **Push your final code** to GitHub before the deadline
4. **Verify automated grading** completed successfully in the Actions tab

### ✅ Raster Analysis Checklist

Before final submission, verify:

- [ ] **All tests pass locally:** `uv run pytest tests/ -v` shows all green
- [ ] **Functions have proper docstrings** with parameters and return types documented  
- [ ] **Error handling implemented** for common raster processing issues
- [ ] **Memory efficiency considered** for large raster operations
- [ ] **COG functions create valid** Cloud-Optimized GeoTIFFs with overviews
- [ ] **STAC integration works** with real satellite data APIs
- [ ] **Code formatted with black:** `uv run black src/ tests/`
- [ ] **No hardcoded file paths** - use relative paths and pathlib
- [ ] **Jupyter notebooks demonstrate** your functions with real data  
- [ ] **GitHub Actions passes** - check the green checkmark

---

## 🎓 Professional Raster Skills Developed

### 🗺️ Core Raster Processing Capabilities
- **Advanced rasterio operations** for professional GIS workflows
- **Cloud-Optimized GeoTIFF** creation and validation for web applications
- **Satellite data integration** using modern STAC APIs
- **Memory-efficient processing** for large-scale raster analysis
- **Vegetation monitoring** and environmental assessment techniques

### 🎨 Remote Sensing and Analysis
- **Multi-spectral imagery processing** and vegetation index calculation
- **Time series analysis** of Earth observation data
- **Seasonal pattern detection** in environmental monitoring
- **Quality assessment** and cloud filtering of satellite imagery

### 🚀 Professional Development Skills  
- **Production-ready Python** with proper error handling and optimization
- **Modern geospatial workflows** using cloud-based data and processing
- **Performance profiling** and memory management for large datasets
- **Automated testing** and continuous integration for geospatial analysis

---

## 📚 Raster Analysis Resources

### 🗺️ Rasterio and Raster Processing
- [Rasterio Documentation](https://rasterio.readthedocs.io/) - Comprehensive rasterio reference
- [COG Format Specification](https://cogeo.org/) - Cloud-Optimized GeoTIFF standards
- [GDAL/OGR Documentation](https://gdal.org/) - Underlying geospatial data library

### 📊 Satellite Data and STAC
- [STAC Specification](https://stacspec.org/) - Spatio-Temporal Asset Catalog standard
- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/) - Free satellite data access
- [AWS Earth Search](https://earth-search.aws.element84.com/v1) - Landsat and Sentinel data
- [PySTAC Client Documentation](https://pystac-client.readthedocs.io/) - Python STAC API client

### 🎨 Visualization and Analysis
- [Matplotlib Basemap Tutorial](https://matplotlib.org/basemap/) - Raster visualization
- [Contextily Documentation](https://contextily.readthedocs.io/) - Web tile integration
- [Rasterstats Documentation](https://pythonhosted.org/rasterstats/) - Zonal statistics

### 📐 Advanced Raster Operations  
- [Xarray Documentation](https://docs.xarray.dev/) - N-dimensional raster arrays
- [Dask Documentation](https://docs.dask.org/) - Parallel raster processing
- [Stackstac Documentation](https://stackstac.readthedocs.io/) - STAC to xarray conversion

---

## 🏆 Success Tips for Raster Analysis

1. **🌟 Use Codespaces if you're on Windows** - It will save you hours of setup time
2. **📊 Start with small test rasters** before processing large satellite imagery
3. **🔍 Always validate COGs** with proper tools before assuming they're correct
4. **⚡ Profile your code** for memory usage when working with large rasters  
5. **🛰️ Test STAC APIs interactively** in notebooks before implementing functions
6. **📈 Visualize your results** to catch processing errors early
7. **🔄 Use version control effectively** - commit often with descriptive messages
8. **📚 Read error messages carefully** - they often contain specific solution hints
9. **🤝 Collaborate respectfully** - help classmates but don't share complete solutions
10. **⏰ Start early** - raster processing can be computationally intensive

**Remember:** This assignment builds essential skills for modern GIS and remote sensing careers. The cloud-optimized workflows and satellite data integration you'll learn are directly applicable to professional geospatial development.

**Good luck with your advanced raster processing journey! 🚀🗺️**