# GIST 604B - Rasterio Real Data Setup with UV

Welcome to authentic geospatial learning! This setup downloads **real satellite imagery and elevation data** from NASA, USGS, and NOAA using modern Python package management with **UV**.

## 🌍 What You'll Get

Instead of synthetic data, you'll work with:

- **Real NASA SRTM Digital Elevation Model** (30m resolution)
- **Real Landsat 8 Surface Reflectance imagery** (6-band multispectral)
- **Real MODIS Land Surface Temperature** (1km daily data)
- **Professional metadata** (STAC-compliant)
- **Supporting vector datasets**

All focused on **Phoenix, Arizona** - an ideal study area with diverse terrain, clear imagery, and interesting urban heat island effects.

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-python-rasterio-[your-username]`

### Step 2: Choose Your Development Environment

**🪟 Windows Users: Use GitHub Codespaces (STRONGLY Recommended)**
- ✅ **No setup required** - everything works immediately
- ✅ **No Windows compatibility issues** - Unix environment provided  
- ✅ **No conda/pip problems** - pre-configured with UV
- ✅ **Focus on learning** - not troubleshooting installation issues
- ✅ **Same environment as instructor** - guaranteed compatibility

```bash
# For Windows users (and everyone else):
# 1. Go to your assignment repository on GitHub
# 2. Click "Code" → "Create codespace on main"  
# 3. Wait 2-3 minutes for automatic setup
# 4. Start coding immediately!
```

**🐧🍎 Mac/Linux Users: Choose Your Preference**

**Option A: GitHub Codespaces (Recommended for All)**
```bash
# Click "Code" → "Create codespace on main"
# Rasterio environment will be pre-configured and ready!
```

**Option B: Local Development (Mac/Linux Only)**
```bash
# Clone your repository
git clone https://github.com/your-org/your-assignment-repo.git
cd your-assignment-repo

# Install UV (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up environment and download real data
uv run python data/setup_rasterio_data.py
```

### Step 3: Verify Your Environment

**Test that UV and packages are working:**
```bash
# Test UV environment
uv run python -c "import rasterio; print(f'Rasterio {rasterio.__version__} ready!')"
uv run python -c "import geopandas; print(f'GeoPandas {geopandas.__version__} ready!')"

# Quick data test
uv run python -c "
import rasterio
with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:
    print(f'DEM loaded: {src.shape} pixels, CRS: {src.crs}')
"
```

## 🛠️ Complete Setup Process

The automated setup handles everything:

```bash
# Run the complete setup (one command!)
uv run python data/setup_rasterio_data.py
```

This will:
1. ✅ Check UV installation
2. ✅ Set up virtual environment with all dependencies  
3. ✅ Download real NASA/USGS datasets
4. ✅ Create fallback synthetic data if needed
5. ✅ Validate your learning environment
6. ✅ Show you next steps

## 📊 Expected Data After Setup

```
data/
├── raster/
│   ├── phoenix_dem_30m.tif           # NASA SRTM Digital Elevation Model
│   ├── landsat8_phoenix_2024.tif     # USGS Landsat 8 (6 bands)
│   └── modis_lst_phoenix.tif         # NASA MODIS Temperature
├── vector/
│   ├── phoenix_study_area.geojson    # Study area boundary
│   └── sample_points.geojson         # Validation points
├── downloads/                        # Raw downloads (temporary)
├── processed/                        # Your analysis outputs
├── data_inventory.json               # Dataset catalog
├── phoenix_stac_metadata.json        # STAC metadata
└── README.md                         # Dataset documentation
```

**Total size:** ~50-200 MB (manageable for coursework)

## 🧪 Working with Your Assignment

### Running Jupyter Notebooks
```bash
# Start Jupyter with UV environment
uv run jupyter notebook

# Or JupyterLab
uv run jupyter lab
```

### Testing Your Functions
```bash
# Test individual functions as you work
uv run pytest tests/ -k "test_load_and_explore_raster" -v

# Run all tests
uv run pytest tests/ -v

# Get test coverage report
uv run pytest tests/ --cov=src --cov-report=html
```

### Working with Real Data
```python
# Your code will work with real geospatial data!
import rasterio
import numpy as np

# Load real NASA DEM data
with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:
    dem = src.read(1)
    print(f"Real elevation data: {np.nanmin(dem):.0f} to {np.nanmax(dem):.0f} meters")

# Load real Landsat multispectral data  
with rasterio.open('data/raster/landsat8_phoenix_2024.tif') as src:
    bands = src.read()  # 6 real spectral bands
    # Calculate real NDVI from real satellite data!
    ndvi = (bands[3] - bands[2]) / (bands[3] + bands[2])
```

## 🔄 How Real Data Download Works

1. **Real Data First:** Downloads from official sources
   - NASA SRTM DEM from OpenTopography
   - Landsat 8 from USGS/AWS Open Data Registry  
   - MODIS LST from NASA LAADS DAAC

2. **Smart Fallbacks:** If downloads fail, creates realistic synthetic data
   - Based on real geographic patterns
   - Maintains authentic data characteristics
   - Still suitable for professional learning

3. **Quality Validation:** All data is properly georeferenced and tested

## 🛠️ Troubleshooting

### "UV not found"
**Install UV first:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: pip install uv
pip install uv
```

### "Package installation failed"
```bash
# Try updating UV
uv self update

# Clear cache and retry
uv cache clean
uv sync --group test --group dev --group download
```

### "Data download failed"
- **Check internet connection**
- **Try running setup again:** `uv run python data/setup_rasterio_data.py`
- **Still works!** - Creates synthetic fallbacks automatically

### "No raster files found"
```bash
# Re-run just the data creation
uv run python data/create_sample_data.py

# Check what was created
ls -la data/raster/
```

### "Import errors in Jupyter"
```bash
# Make sure to use uv run
uv run jupyter notebook

# Or restart kernel and try again
```

## 📚 Assignment Structure

```
rasterio-assignment/
├── README.md                     # Main assignment instructions
├── pyproject.toml               # UV dependencies and config
├── uv.lock                      # Locked dependency versions
├── src/
│   └── rasterio_basics.py       # 👈 YOUR CODE GOES HERE (4 functions)
├── tests/
│   └── test_rasterio_basics.py  # 🧪 Unit tests - professional testing!
├── notebooks/
│   ├── 00_start_here_overview.ipynb           # Assignment overview
│   ├── 01_function_load_and_explore_raster.ipynb
│   ├── 02_function_calculate_raster_statistics.ipynb  
│   ├── 03_function_extract_raster_subset.ipynb
│   └── 04_function_visualize_raster_data.ipynb
├── data/
│   ├── setup_rasterio_data.py   # Automated setup script
│   ├── create_sample_data.py    # Real data downloader
│   └── [datasets created here]
└── output/                      # Your analysis results
```

## 🎓 Learning Workflow

1. **Setup:** Run `uv run python data/setup_rasterio_data.py` (once)
2. **Learn:** Work through notebooks with `uv run jupyter notebook`
3. **Code:** Implement functions in `src/rasterio_basics.py`
4. **Test:** Validate with `uv run pytest tests/ -v`
5. **Submit:** Push your completed code to GitHub

## 🌟 Why UV + Real Data?

**Modern Package Management:**
- ✅ **Faster** than pip/conda - dependencies install in seconds
- ✅ **Reliable** - locked versions prevent "works on my machine" issues  
- ✅ **Professional** - UV is used by major Python projects
- ✅ **Consistent** - same environment for everyone

**Authentic Geospatial Data:**
- 🌍 **Real NASA/USGS datasets** - same data scientists use
- 🎯 **Professional skills** - industry-standard workflows
- 🔧 **Real challenges** - handling actual data quality issues
- 📊 **STAC metadata** - learn current geospatial standards

## 🆘 Getting Help

1. **Check setup logs:** Setup scripts show detailed messages
2. **Read documentation:** `data/README.md` has dataset examples  
3. **Test environment:** Run `uv run python data/setup_rasterio_data.py` again
4. **Ask for help:** Contact your instructor or TA with specific error messages

## 🎯 Next Steps

Once setup is complete:

1. **Start learning:** `uv run jupyter notebook`
2. **Read overview:** Open `notebooks/00_start_here_overview.ipynb`
3. **Explore data:** Check `data/README.md` for dataset details
4. **Test loading:** Try the code examples above
5. **Begin assignment:** Work through the function notebooks

---

**Ready to start?** Run `uv run python data/setup_rasterio_data.py` and begin your journey with real geospatial data! 🚀

*Questions? Check with your GIST 604B instructor or TA.*