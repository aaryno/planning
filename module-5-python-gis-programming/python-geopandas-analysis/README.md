# Python GeoPandas Analysis - Essential Spatial Operations

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 18 | Due: One week from assignment date**

---

## 🎯 Assignment Overview

Master **essential spatial analysis** using Python's GeoPandas library! This assignment teaches you the core skills for working with spatial data - loading, analyzing geometric properties, and performing proximity analysis.

**Prerequisites:** Complete `python-geopandas-intro` assignment first! This builds on spatial data fundamentals.

**What you'll learn:**
- Load and explore spatial datasets (shapefiles, GeoJSON, etc.)
- Calculate geometric properties (areas, perimeters, centroids)
- Create buffer zones for proximity analysis
- Handle coordinate reference systems (CRS) properly
- **Professional spatial data workflows** - interactive development then implementation
- **Jupyter-based spatial analysis** - prototype with maps then implement functions

**🎓 Learning Approach:**
This assignment uses **interactive Jupyter notebooks** to teach you each spatial technique step-by-step, then you implement simplified versions in Python files for grading. This mirrors real-world spatial analysis workflows!

**Time commitment:** About 2-3 hours total (includes notebook learning and implementation)

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-python-geopandas-analysis-[your-username]`

### Step 2: Choose Your Development Environment

**🪟 Windows Users: Use GitHub Codespaces (STRONGLY Recommended)**
- ✅ **No setup required** - everything works immediately
- ✅ **No Windows spatial library issues** - Unix environment provided
- ✅ **No GDAL/GEOS installation problems** - pre-configured geospatial environment
- ✅ **Focus on learning spatial analysis** - not troubleshooting installations

```bash
# For Windows users (and everyone else):
# 1. Go to your assignment repository on GitHub
# 2. Click "Code" → "Create codespace on main"  
# 3. Wait 2-3 minutes for automatic setup
# 4. Start spatial analysis immediately!
```

**🐧 Linux/Mac Users: Your Choice**
```bash
# Option 1: GitHub Codespaces (recommended - same as above)
# Option 2: Local development (if you prefer)
git clone [your-repo-url]
cd python-geopandas-analysis
uv sync --group test --group dev
```

### Step 3: Verify Your Environment
```bash
# Test that everything works:
uv run python -c "import geopandas; print(f'GeoPandas {geopandas.__version__} ready!')"
uv run python -c "import folium; print('Folium mapping ready!')"
uv run pytest tests/ -v --tb=short
```

You should see something like:
```
GeoPandas 0.14.1 ready!
Folium mapping ready!
======================= test session starts =======================
tests/test_spatial_analysis.py::test_load_and_explore_spatial_data FAILED
tests/test_spatial_analysis.py::test_calculate_basic_spatial_metrics FAILED
tests/test_spatial_analysis.py::test_create_spatial_buffer_analysis FAILED
... (This is expected - you haven't implemented the functions yet!)
```

---

## 📁 Understanding Your Assignment Files

```
python-geopandas-analysis/
├── 📖 README.md                    # This file - your assignment guide!
├── 📓 notebooks/                   # Interactive learning materials
│   ├── 00_start_here_overview.ipynb                    # Start here! Complete workflow guide
│   ├── 01_function_load_and_explore_spatial_data.ipynb # Learn to load and explore spatial files
│   ├── 02_function_calculate_basic_spatial_metrics.ipynb # Learn geometric calculations
│   └── 03_function_create_spatial_buffer_analysis.ipynb # Learn proximity analysis
├── 🐍 src/                         # Your implementation area
│   └── spatial_analysis.py        # Implement the 3 functions here
├── 🧪 tests/                       # Automated tests (don't modify!)
│   └── test_spatial_analysis.py   # Tests for your spatial functions
├── 📊 data/                        # Sample spatial datasets
│   ├── cities.geojson             # City point locations
│   ├── watersheds.shp             # Watershed polygon boundaries
│   ├── rivers.shp                 # River line features  
│   └── README.md                  # Dataset descriptions and sources
└── ⚙️  Configuration files          # Project setup (uv, pytest, etc.)
```

---

## 📝 Your Assignment Tasks

You need to implement **3 core spatial analysis functions** in the file `src/spatial_analysis.py`. Each function has a corresponding Jupyter notebook that teaches you how to build it step by step.

**📚 Learning Process:**
1. **Learn**: Open the notebook for each function to understand how it works
2. **Implement**: Write your code in `src/spatial_analysis.py` (replace the TODO comments)
3. **Test**: Run pytest to verify your implementation works correctly

**🎯 Your Task:** The notebooks show you HOW to build each function, but you must implement the actual code in `src/spatial_analysis.py` to pass the unit tests. The notebooks are for learning - the assignment requires working code in the .py file!

### 🗺️ Part 1: Load and Explore Spatial Data (6 points)
**Function:** `load_and_explore_spatial_data(file_path)`  
📚 **Learning Notebook:** `notebooks/01_function_load_and_explore_spatial_data.ipynb`

**What to implement in `src/spatial_analysis.py`:**
1. Use `gpd.read_file()` to load spatial data (shapefile, GeoJSON, etc.)
2. Display basic spatial information (CRS, geometry types, bounds)
3. Show the first few features and their attributes
4. Check for spatial data quality issues (invalid geometries, missing CRS)
5. Handle file loading errors and unsupported formats
6. Return the loaded GeoDataFrame

**Test your function:**
```bash
uv run pytest tests/test_spatial_analysis.py::test_load_and_explore_spatial_data -v
```

**Example output:**
```
Spatial dataset loaded successfully!
File: data/cities.geojson
CRS: EPSG:4326 (WGS84)
Geometry type: Point
Bounds: [-180.0, -85.0, 180.0, 85.0]
Features: 150 cities

First 3 features:
     city_name  population    geometry
0   Sacramento     500000   POINT(...)
1   San Diego    1400000   POINT(...)
...
```

### 📐 Part 2: Calculate Basic Spatial Metrics (6 points)
**Function:** `calculate_basic_spatial_metrics(gdf)`  
📚 **Learning Notebook:** `notebooks/02_function_calculate_basic_spatial_metrics.ipynb`

**What to implement in `src/spatial_analysis.py`:**
1. Calculate areas for polygon features (using appropriate projected CRS)
2. Calculate perimeters for polygon features
3. Generate centroid points for all geometry types
4. Handle different geometry types (points, lines, polygons)
5. Convert between geographic and projected coordinate systems
6. Return a dictionary with calculated metrics

**Test your function:**
```bash
uv run pytest tests/test_spatial_analysis.py::test_calculate_basic_spatial_metrics -v
```

**Example output:**
```
Calculating spatial metrics for 25 watersheds...
Reprojecting to UTM Zone 10N for accurate measurements...

Metrics calculated:
- Total area: 15,847.23 km²
- Average area: 633.89 km²
- Total perimeter: 2,156.78 km
- All centroids generated successfully
```

### 🎯 Part 3: Create Spatial Buffer Analysis (6 points)
**Function:** `create_spatial_buffer_analysis(gdf, buffer_distance)`  
📚 **Learning Notebook:** `notebooks/03_function_create_spatial_buffer_analysis.ipynb`

**What to implement in `src/spatial_analysis.py`:**
1. Create buffer zones around spatial features
2. Handle coordinate system requirements for accurate distances
3. Calculate buffer statistics (total buffered area, overlap analysis)
4. Create a simple visualization showing original features and buffers
5. Return both the buffered GeoDataFrame and analysis summary
6. Handle edge cases (empty geometries, invalid distances)

**Test your function:**
```bash
uv run pytest tests/test_spatial_analysis.py::test_create_spatial_buffer_analysis -v
```

**Example output:**
```
Creating 1000m buffers around 50 cities...
Reprojecting to appropriate UTM zone for buffer analysis...

Buffer analysis complete:
- Created 50 buffer zones
- Total buffered area: 157.08 km²
- Average buffer area: 3.14 km²
- Buffer overlaps detected: 8 cases
```

---

## 🧪 Professional Development Workflow

### Step 1: Learning with Notebooks

**🎯 Start with the overview:** Open `notebooks/00_start_here_overview.ipynb`
- Understand the complete spatial analysis workflow
- See how the 3 functions work together
- Learn about coordinate systems and spatial data formats

### Step 2: Function-by-Function Learning

**📚 Work through each notebook in order:**

1. **Spatial Data Loading** → `01_function_load_and_explore_spatial_data.ipynb`
2. **Geometric Calculations** → `02_function_calculate_basic_spatial_metrics.ipynb` 
3. **Buffer Analysis** → `03_function_create_spatial_buffer_analysis.ipynb`

### Step 3: Implement Functions

**💻 Edit `src/spatial_analysis.py`:**
```python
def load_and_explore_spatial_data(file_path):
    # TODO: Replace this with your implementation
    # Use the notebook examples as a guide
    pass
```

### Step 4: Test-Driven Development

**🧪 Test each function as you implement it:**
```bash
# Test individual functions
uv run pytest tests/test_spatial_analysis.py::test_load_and_explore_spatial_data -v
uv run pytest tests/test_spatial_analysis.py::test_calculate_basic_spatial_metrics -v
uv run pytest tests/test_spatial_analysis.py::test_create_spatial_buffer_analysis -v

# Get detailed feedback
uv run pytest tests/ -v --tb=long
```

### Step 5: Debug and Iterate

**🔍 Use test results to improve:**
- **PASSED** ✅ = Function works correctly!
- **FAILED** ❌ = Check error message for specific issues
- **ERROR** ⚠️ = Usually syntax error or import problem

### Step 6: Final Validation

**✨ Ensure everything works together:**
```bash
# Run complete test suite
uv run pytest tests/ -v

# Test imports work
uv run python -c "from src.spatial_analysis import *; print('All functions imported!')"
```

---

## 📊 Sample Data Provided

### `cities.geojson`
Point dataset containing major cities with population data. Perfect for learning point geometry operations and coordinate systems.

**Attributes:** city_name, population, state, country  
**Geometry:** Point locations in WGS84 (EPSG:4326)

### `watersheds.shp` (Shapefile)
Polygon dataset showing watershed boundaries for hydrological analysis.

**Attributes:** watershed_name, area_km2, basin_type  
**Geometry:** Complex polygons in projected coordinates

### `rivers.shp` (Shapefile) 
Line dataset representing major river networks and tributaries.

**Attributes:** river_name, length_km, flow_type  
**Geometry:** LineString features in projected coordinates

---

## 📚 Learning Resources

### GeoPandas Essentials
- [GeoPandas User Guide](https://geopandas.org/en/stable/user_guide.html) - Official documentation
- [Loading Spatial Data](https://geopandas.org/en/stable/docs/user_guide/io.html) - File formats and loading
- [Geometric Operations](https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html) - Areas, buffers, centroids

### Key Functions You'll Use
```python
# Loading spatial data
gpd.read_file()       # Load shapefiles, GeoJSON, etc.
gdf.head()            # Display first few features
gdf.crs               # Check coordinate reference system
gdf.total_bounds      # Get spatial extent

# Geometric calculations  
gdf.area              # Calculate areas (for polygons)
gdf.length            # Calculate perimeters/lengths
gdf.centroid          # Generate centroid points
gdf.to_crs()          # Reproject to different CRS

# Buffer analysis
gdf.buffer()          # Create buffer zones
gdf.overlay()         # Analyze spatial overlaps
gdf.plot()            # Create simple maps
```

### Coordinate Reference Systems (CRS)
- **Geographic CRS (EPSG:4326)**: Latitude/longitude coordinates - good for display
- **Projected CRS (UTM zones)**: Meter-based coordinates - required for accurate measurements
- **Web Mercator (EPSG:3857)**: Common for web mapping applications

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**"CRS warning" or projection issues:**
```python
# Check current CRS
print(f"Current CRS: {gdf.crs}")

# Reproject to UTM for measurements (example for California)
gdf_utm = gdf.to_crs('EPSG:32610')  # UTM Zone 10N

# Reproject to geographic for display
gdf_geo = gdf.to_crs('EPSG:4326')   # WGS84
```

**"File not found" errors:**
```bash
# Check if file exists and path is correct
ls data/
# Make sure you're running from the project root directory
pwd
```

**Buffer results look wrong:**
```python
# Ensure you're using projected coordinates for buffer distance
print(f"CRS before buffer: {gdf.crs}")
if gdf.crs.to_string().startswith('EPSG:4326'):
    print("Converting to projected CRS for accurate buffering")
    gdf = gdf.to_crs('EPSG:3857')  # or appropriate UTM zone
```

**Import errors:**
```bash
# Reinstall dependencies if needed
uv sync --group test --group dev
# Test individual imports
uv run python -c "import geopandas; print('OK')"
```

### 🪟 Windows-Specific Issues
If you encounter problems on Windows:
- **GDAL/GEOS installation issues** → Use GitHub Codespaces
- **Shapefile reading problems** → Use GitHub Codespaces  
- **Coordinate system errors** → Use GitHub Codespaces

**Codespaces provides a pre-configured Unix environment with all spatial libraries working perfectly!**

---

## 📤 Submission Requirements

### What to Submit

Your assignment is automatically submitted when you push code to GitHub. **No pull requests needed!**

**Required deliverables:**
- `src/spatial_analysis.py` with all 3 functions implemented
- All tests passing (verified through GitHub Actions)
- Clean, well-commented code following the examples from notebooks

### Grading Breakdown (18 points total)

**Function 1: Load and Explore Spatial Data (6 points)**
- Correctly loads spatial files: 3 points
- Displays comprehensive spatial information: 2 points  
- Handles errors appropriately: 1 point

**Function 2: Calculate Basic Spatial Metrics (6 points)**
- Calculates areas and perimeters accurately: 3 points
- Generates centroids correctly: 2 points
- Handles coordinate system conversions: 1 point

**Function 3: Create Spatial Buffer Analysis (6 points)**
- Creates accurate buffer zones: 3 points
- Performs buffer analysis calculations: 2 points
- Returns proper results format: 1 point

### Success Checklist

Before submitting, verify:

- [ ] **Environment setup complete** - all imports work without errors
- [ ] **All 3 functions implemented** - no TODO comments remaining  
- [ ] **Tests passing locally** - `uv run pytest tests/ -v` shows all PASSED
- [ ] **Functions handle edge cases** - empty data, invalid inputs, etc.
- [ ] **Coordinate systems handled properly** - geographic vs projected as needed
- [ ] **Code is clean and commented** - easy to understand your implementation

**Final test:**
```bash
# This should run without errors and show all tests passing
uv run pytest tests/ -v

# This should work without import errors  
uv run python -c "from src.spatial_analysis import *; print('Ready for submission!')"
```

---

## 🎓 Why This Matters for GIS

### 🌍 Real-World Applications

**Environmental Management:**
- Calculate watershed areas and analyze drainage patterns
- Create buffer zones around protected areas or pollution sources
- Monitor habitat connectivity and wildlife corridors

**Urban Planning:**
- Analyze service areas around schools, hospitals, fire stations
- Calculate building footprint areas and density metrics
- Plan transportation networks and accessibility zones

**Emergency Response:**
- Create evacuation buffer zones around hazard areas
- Calculate affected population areas for disaster planning
- Analyze emergency service coverage and response times

### 🚀 Professional Skills You're Building

- **Spatial data management** - loading, validating, and organizing geographic datasets
- **Geometric analysis** - calculating areas, distances, and spatial relationships
- **Coordinate system expertise** - understanding when and how to reproject spatial data
- **Quality assurance** - testing spatial operations and validating results
- **Professional workflows** - prototype → implement → test → deploy

**These skills are essential for:**
- GIS Analyst positions
- Environmental consulting
- Urban planning roles
- Spatial data science careers
- Geospatial software development

---

## 🆘 Getting Help

1. **📖 Start with the notebooks** - they contain complete working examples for each function
2. **🧪 Read test error messages carefully** - they tell you exactly what's expected vs. what your code returned
3. **📊 Test with the sample data first** - use the provided datasets before trying your own
4. **🗺️ Check coordinate systems** - many spatial issues are CRS-related
5. **💬 Ask specific questions** - "My area calculation returns negative values..." is better than "it doesn't work"

**Course resources:**
- Office hours for personalized debugging help
- Course forum for sharing solutions to common problems
- Peer study groups for collaborative learning

---

*This assignment builds the foundation for advanced spatial analysis! These core GeoPandas skills will prepare you for complex spatial modeling, web mapping, and spatial data science applications.* 🌟