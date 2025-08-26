# Python Rasterio for GIS Raster Analysis

**GIST 604B - Module 5: Python GIS Programming**  
**Assignment Points:** 20 points total  
**Due:** [See Canvas for deadline]

---

## 🎯 Assignment Overview

Master essential **rasterio** skills by working with satellite imagery and elevation data! You'll learn to load, analyze, and visualize raster datasets using professional Python workflows.

**What you'll learn:**
- Loading and exploring raster files (GeoTIFF, NetCDF)
- Extracting metadata and coordinate information  
- Calculating band statistics and analyzing pixel values
- Creating spatial subsets and windowed reads
- Visualizing raster data with maps and plots

**Real-world applications:** Satellite image analysis, elevation modeling, climate data processing, land cover classification, and environmental monitoring.

**🎓 Professional Skills:** This assignment teaches the notebook → code → testing workflow used by data scientists and GIS professionals worldwide.

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
Click the GitHub Classroom link provided in Canvas to create your personal repository.

### Step 2: Choose Your Development Environment

**Option A: GitHub Codespaces (Recommended)**
- Click the green "Code" button → "Codespaces" → "Create codespace on main"
- Everything is pre-configured with rasterio, matplotlib, and sample data
- Works in your web browser - no local installation needed

**Option B: Local Development**
```bash
# Clone your repository
git clone [your-repo-url]
cd python-rasterio

# Create environment and install dependencies
uv sync

# Activate environment
uv shell

# Test installation
uv run python -c "import rasterio; print('✅ Rasterio ready!')"
```

**Option C: Conda/Mamba (Alternative)**
```bash
# Create environment
conda env create -f environment.yml
conda activate rasterio-env

# Test installation
python -c "import rasterio; print('✅ Rasterio ready!')"
```

### Step 3: Verify Your Environment
Run this test to confirm everything works:

```bash
# Test core functionality
uv run pytest tests/ --collect-only

# Should show 4 test functions without errors
```

**✅ Success indicators:**
- No import errors
- Sample data files load correctly  
- Matplotlib creates plots
- Tests collect successfully

---

## 📁 Understanding Your Assignment Files

```
python-rasterio/
├── notebooks/                    # 📚 Interactive learning materials
│   ├── 00_start_here_overview.ipynb           # Start here!
│   ├── 01_function_load_and_explore_raster.ipynb
│   ├── 02_function_calculate_raster_statistics.ipynb  
│   ├── 03_function_extract_raster_subset.ipynb
│   └── 04_function_visualize_raster_data.ipynb
│
├── src/
│   └── rasterio_basics.py        # 🎯 Your implementation code
│
├── tests/
│   └── test_rasterio_basics.py   # 🧪 Unit tests (pre-written)
│
├── data/                         # 📊 Sample datasets
│   ├── elevation_dem.tif         # Digital Elevation Model
│   ├── landsat_sample.tif        # Multispectral satellite image
│   └── data_dictionary.md        # Dataset documentation
│
├── output/                       # 📁 Generated files and plots
└── README.md                     # 📖 This file
```

**🎯 Your main task:** Learn from the notebooks, then implement the functions in `src/rasterio_basics.py` to pass all unit tests.

---

## 📝 Your Assignment Tasks

You need to implement **4 functions** in the file `src/rasterio_basics.py`. Each function has a corresponding Jupyter notebook that teaches you how to build it step by step.

**📚 Learning Process:**
1. **Learn**: Open the notebook for each function to understand how it works
2. **Implement**: Write your code in `src/rasterio_basics.py` (replace the TODO comments)
3. **Test**: Run pytest to verify your implementation works correctly

**🎯 Your Task:** The notebooks show you HOW to build each function, but you must implement the actual code in `src/rasterio_basics.py` to pass the unit tests. The notebooks are for learning - the assignment requires working code in the .py file!

### 🗺️ Part 1: Load and Explore Raster Data (5 points)
**Function:** `load_and_explore_raster(raster_path)`  
📚 **Learning Notebook:** `notebooks/01_function_load_and_explore_raster.ipynb`

**What to implement in `src/rasterio_basics.py`:**
1. Use `rasterio.open()` to load a raster file
2. Extract basic metadata (dimensions, bands, CRS, nodata value)
3. Get spatial extent and pixel resolution
4. Display summary information clearly
5. Handle file errors and invalid paths
6. Return a dictionary with raster properties

**Test your function:**
```bash
uv run pytest tests/test_rasterio_basics.py::test_load_and_explore_raster -v
```

**Example output:**
```
Raster file loaded successfully!
Dimensions: 1024 x 768 pixels (3 bands)
Coordinate System: EPSG:4326 (WGS84)
Extent: -120.5 to -119.5 longitude, 35.0 to 36.0 latitude
Pixel Size: 0.001 x 0.001 degrees
NoData Value: -9999
```

### 📊 Part 2: Calculate Raster Statistics (5 points)
**Function:** `calculate_raster_statistics(raster_path, band_number=1)`  
📚 **Learning Notebook:** `notebooks/02_function_calculate_raster_statistics.ipynb`

**What to implement in `src/rasterio_basics.py`:**
1. Read a specific band from the raster file
2. Handle NoData values properly by masking them out
3. Calculate min, max, mean, and standard deviation
4. Count valid vs. NoData pixels
5. Find percentiles (25th, 50th, 75th) for data distribution
6. Return statistics as a formatted dictionary

**Test your function:**
```bash
uv run pytest tests/test_rasterio_basics.py::test_calculate_raster_statistics -v
```

**Example output:**
```
Band 1 Statistics:
Valid pixels: 786,432 (100.0%)
NoData pixels: 0
Min: 1,247 meters    Max: 4,421 meters
Mean: 2,834.2 meters  Std Dev: 623.1 meters
Percentiles: 25%=2,401m, 50%=2,798m, 75%=3,267m
```

### ✂️ Part 3: Extract Raster Subset (5 points)
**Function:** `extract_raster_subset(raster_path, window_bounds, output_path=None)`  
📚 **Learning Notebook:** `notebooks/03_function_extract_raster_subset.ipynb`

**What to implement in `src/rasterio_basics.py`:**
1. Define a spatial window using coordinate bounds
2. Convert geographic bounds to pixel coordinates  
3. Use windowed reading to extract subset efficiently
4. Preserve original CRS and metadata in subset
5. Optionally save subset to new file
6. Return the subset array and updated metadata

**Test your function:**
```bash
uv run pytest tests/test_rasterio_basics.py::test_extract_raster_subset -v
```

**Example output:**
```
Extracting subset...
Original: 1024 x 768 pixels
Window bounds: -120.2 to -119.8, 35.3 to 35.7
Subset: 400 x 300 pixels extracted
Memory saved: 67% (windowed read vs. full file)
```

### 📈 Part 4: Visualize Raster Data (3 points)
**Function:** `visualize_raster_data(raster_path, band_number=1, output_path=None)`  
📚 **Learning Notebook:** `notebooks/04_function_visualize_raster_data.ipynb`

**What to implement in `src/rasterio_basics.py`:**
1. Load and display a raster band with proper scaling
2. Create a color-mapped plot with colorbar and labels
3. Add geographic coordinates if possible
4. Handle different data ranges appropriately
5. Save plot to file if output_path provided
6. Return matplotlib figure object

**Test your function:**
```bash
uv run pytest tests/test_rasterio_basics.py::test_visualize_raster_data -v
```

**Example output:**
```
Creating raster visualization...
Data range: 1,247 to 4,421 meters
Colormap: terrain (appropriate for elevation data)
Plot saved: output/elevation_visualization.png
```

### Code Quality (2 points)
Clean, readable code following the patterns shown in the notebooks, with proper error handling and documentation.

---

## 🧪 Professional Development Workflow

**Important Learning Objective**: This assignment teaches you professional development practices including unit testing and the notebook-to-code workflow used in industry.

### Step 1: Learning with Notebooks

```bash
# Navigate to the notebooks directory
cd notebooks/

# Open Jupyter in your browser (if using local setup)
uv run jupyter notebook

# In Codespaces, notebooks open directly in VS Code
```

**Work through notebooks in order:**
1. `00_start_here_overview.ipynb` ← **Start here for complete workflow**
2. `01_function_load_and_explore_raster.ipynb`
3. `02_function_calculate_raster_statistics.ipynb`  
4. `03_function_extract_raster_subset.ipynb`
5. `04_function_visualize_raster_data.ipynb`

### Step 2: Implement Functions

Open `src/rasterio_basics.py` and replace each `TODO` section with working code:

```python
def load_and_explore_raster(raster_path):
    """Your implementation here"""
    # TODO: Follow the notebook examples
    # TODO: Load raster with rasterio.open()
    # TODO: Extract metadata and properties  
    # TODO: Return dictionary with results
    pass
```

### Step 3: Test-Driven Development

Test each function as you implement it:

```bash
# Test individual functions
uv run pytest tests/test_rasterio_basics.py::test_load_and_explore_raster -v
uv run pytest tests/test_rasterio_basics.py::test_calculate_raster_statistics -v

# Test all functions
uv run pytest tests/ -v

# Get detailed output with print statements
uv run pytest tests/ -v -s
```

### Step 4: Debug and Iterate

**Common issues and solutions:**
- **Import errors** → Check environment setup (`uv sync`)
- **File not found** → Verify data files exist in `data/` directory
- **Memory errors** → Use windowed reading for large files  
- **CRS issues** → Check coordinate system of input data

### Step 5: Final Validation

```bash
# Full test suite
uv run pytest tests/ -v --tb=short

# Should show all PASSED for full credit
```

---

## 📊 Sample Data Provided

### `elevation_dem.tif`
- **Content:** Digital Elevation Model (DEM) of mountainous terrain
- **Resolution:** 30-meter pixels
- **Extent:** Small region in Colorado Rocky Mountains
- **Bands:** 1 (elevation in meters above sea level)
- **Use:** Practice with single-band analysis and terrain visualization

### `landsat_sample.tif`
- **Content:** Landsat 8 satellite imagery subset
- **Resolution:** 30-meter pixels  
- **Extent:** Agricultural region in California Central Valley
- **Bands:** 4 (Red, Green, Blue, Near-Infrared)
- **Use:** Multi-band analysis and false-color visualization

**🔍 Data exploration:** Use the notebooks to understand these datasets before implementing your functions!

---

## 📚 Learning Resources

### Rasterio Basics
- **Official Tutorial:** https://rasterio.readthedocs.io/en/latest/quickstart.html
- **Windowed Reading:** https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html
- **CRS and Transforms:** https://rasterio.readthedocs.io/en/latest/topics/coordinate-systems.html

### Key Functions You'll Use
```python
# Core rasterio functions
rasterio.open(path)          # Open raster file
src.read(band_number)        # Read band data
src.bounds, src.crs          # Spatial properties
rasterio.windows.Window()    # Define spatial windows

# NumPy for analysis
np.mean(), np.std()          # Statistics  
np.percentile()              # Distribution analysis
np.ma.masked_equal()         # Handle NoData

# Matplotlib for visualization  
plt.imshow()                 # Display raster
plt.colorbar()               # Add color scale
plt.savefig()                # Save plots
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**🔧 Environment Issues**
```bash
# Problem: Import errors
# Solution: Reinstall dependencies
uv sync --reinstall

# Problem: Missing rasterio
# Solution: Install GDAL properly
uv add rasterio[complete]
```

**📂 File Path Issues**  
```bash
# Problem: FileNotFoundError
# Check if files exist
ls -la data/

# Problem: Path separator issues  
# Use pathlib for cross-platform compatibility
from pathlib import Path
raster_path = Path("data") / "elevation_dem.tif"
```

**🖥️ Memory Issues**
```python
# Problem: Large files cause memory errors
# Solution: Use windowed reading
with rasterio.open(path) as src:
    window = rasterio.windows.Window(0, 0, 512, 512)  # Smaller chunk
    data = src.read(1, window=window)
```

**📊 Visualization Issues**
```python
# Problem: Plots don't display properly
# Solution: Set backend and show explicitly  
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))
plt.imshow(data, cmap='terrain')
plt.show()
```

**Need more help?**
- Check the error message carefully - it tells you exactly what's wrong
- Review the corresponding notebook for working examples
- Test with small subsets first before processing large files
- Ask on the course forum with specific error messages

---

## 📤 Submission Requirements

### What to Submit
Your GitHub repository must contain:

1. **✅ Completed `src/rasterio_basics.py`** with all 4 functions implemented
2. **✅ All tests passing** when running `uv run pytest tests/ -v`
3. **✅ Generated output files** in the `output/` directory (plots, subset files)
4. **✅ Updated notebooks** showing your learning process (optional but recommended)

### Grading Breakdown (20 points total)

- **Function 1:** Load and Explore Raster (5 points)
- **Function 2:** Calculate Raster Statistics (5 points)  
- **Function 3:** Extract Raster Subset (5 points)
- **Function 4:** Visualize Raster Data (3 points)
- **Code Quality:** Clean, documented code (2 points)

### Success Checklist

Before submitting, verify:

- [ ] **All tests pass:** `uv run pytest tests/ -v` shows 4/4 PASSED
- [ ] **Code is complete:** No TODO comments remain in `src/rasterio_basics.py`
- [ ] **Functions work independently:** Each function can be called without errors
- [ ] **Output files generated:** Plots and subset files created in `output/`
- [ ] **Code is clean:** Proper formatting, meaningful variable names
- [ ] **Repository is current:** Latest changes committed and pushed to GitHub

---

## 🎓 Why This Matters for GIS

### 🌍 Real-World Applications

**Environmental Monitoring:**
- Analyze satellite imagery for deforestation tracking
- Process climate data for temperature trend analysis  
- Monitor water quality using multispectral sensors

**Urban Planning:**
- Extract building footprints from high-resolution imagery
- Analyze land use changes over time
- Create elevation models for flood risk assessment

**Agriculture & Natural Resources:**
- Calculate vegetation indices from satellite data
- Monitor crop health and yield prediction
- Analyze soil moisture and irrigation needs

**Scientific Research:**
- Process meteorological station data
- Analyze ice sheet changes from radar imagery
- Study ecosystem changes using time series data

### 🚀 Career Preparation

**Technical Skills You're Building:**
- **Spatial Data Processing** - Core skill for any GIS role
- **Python Programming** - Most in-demand GIS skill
- **Data Analysis Workflows** - Professional development practices
- **Scientific Computing** - NumPy, matplotlib, and scientific Python ecosystem

**Professional Workflows:**
- **Test-Driven Development** - Industry standard for reliable code
- **Documentation** - Essential for collaborative projects
- **Version Control** - Using Git/GitHub professionally
- **Problem-Solving** - Breaking complex geospatial problems into manageable steps

---

## 🆘 Getting Help

### 📞 When You Need Support

**First Steps:**
1. **Check the error message** - Python tells you exactly what went wrong
2. **Review the relevant notebook** - Working examples are provided
3. **Test with simpler data** - Start small before processing large files
4. **Check file paths** - Verify your data files exist and are accessible

**Course Resources:**
- **📧 Course Forum:** Ask specific questions with error messages
- **🕐 Office Hours:** Get personalized help with complex issues  
- **📚 Course Materials:** Review lecture slides and readings
- **👥 Study Groups:** Work through problems with classmates

**Online Resources:**
- **Rasterio Documentation:** https://rasterio.readthedocs.io/
- **Stack Overflow:** Search for specific error messages
- **GIS Stack Exchange:** Geospatial-specific programming help

**💡 How to Ask for Help Effectively:**
1. **Include the specific error message** you're seeing
2. **Describe what you were trying to do** when the error occurred  
3. **Share the relevant code** that's causing problems
4. **Mention what you've already tried** to solve the issue

Remember: Every professional geospatial programmer started as a beginner. Take your time, be patient with yourself, and don't hesitate to ask for help when you need it!

**🎉 You've got the tools, you've got the data, you've got the support - now go build something amazing with Python and rasterio!**