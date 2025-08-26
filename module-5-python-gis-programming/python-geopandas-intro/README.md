# Python GeoPandas Introduction - Spatial Data Fundamentals

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 15 | Due: One week from assignment date**

---

## 🎯 Assignment Overview

Master the **fundamentals of spatial data** using Python's GeoPandas library! This assignment teaches you essential skills for loading, exploring, and preparing spatial datasets - the foundation of all GIS programming workflows.

**What you'll learn:**
- Load spatial data from common formats (Shapefiles, GeoJSON, etc.) into Python
- Explore spatial properties like coordinate systems, boundaries, and geometry types
- Identify and fix common spatial data quality issues
- Transform data between different coordinate reference systems (CRS)
- **Professional spatial data workflows** - industry best practices for data preparation
- **Unit testing with pytest** - professional testing practices used in spatial analysis

**🎓 Learning Approach:**
This assignment uses **interactive Jupyter notebooks** to teach you each spatial concept step-by-step, then you implement the actual code in Python files for grading. This mirrors real-world GIS workflows where you explore data interactively before writing production analysis code!

**Time commitment:** About 3-4 hours total (includes notebook learning and testing)

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-python-geopandas-intro-[your-username]`

### Step 2: Choose Your Development Environment

**🪟 Windows Users: Use GitHub Codespaces (STRONGLY Recommended)**
- ✅ **No setup required** - everything works immediately
- ✅ **No Windows spatial library issues** - Unix environment provided
- ✅ **No GDAL/GEOS installation problems** - pre-configured geospatial environment
- ✅ **Focus on learning spatial concepts** - not troubleshooting installations
- ✅ **Same environment as instructor** - guaranteed compatibility

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
cd python-geopandas-intro
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
tests/test_spatial_basics.py::test_load_spatial_dataset FAILED
tests/test_spatial_basics.py::test_explore_spatial_properties FAILED
... (This is expected - you haven't implemented the functions yet!)
```

---

## 📁 Understanding Your Files

```
python-geopandas-intro/
├── 📖 README.md                    # This file - your assignment guide!
├── 📓 notebooks/                   # Interactive learning materials
│   ├── 01_spatial_data_overview.ipynb    # Start here! Spatial data intro
│   ├── 02_load_spatial_data.ipynb        # Loading different spatial formats
│   ├── 03_explore_properties.ipynb       # CRS, bounds, geometry analysis
│   ├── 04_validate_data.ipynb            # Finding and fixing spatial issues
│   └── 05_coordinate_systems.ipynb       # Working with different projections
├── 🐍 src/                         # Your implementation area
│   └── spatial_basics.py          # Implement the 4 functions here
├── 🧪 tests/                       # Automated tests (don't modify!)
│   └── test_spatial_basics.py     # Tests for your spatial functions
├── 📊 data/                        # Sample spatial datasets
│   ├── cities/                     # World cities point data
│   ├── countries/                  # Country boundary polygons  
│   ├── roads/                      # Road network lines
│   └── README.md                   # Dataset descriptions
└── ⚙️  Configuration files          # Project setup (uv, pytest, etc.)
```

---

## 📝 Your Assignment Tasks

You need to implement **4 essential spatial data functions** that will be automatically tested:

### 🗺️ Function 1: `load_spatial_dataset()` (4 points)
**Interactive Learning:** `notebooks/02_load_spatial_data.ipynb`

**What it does:** Load spatial data from different file formats (Shapefile, GeoJSON, etc.) and handle various loading scenarios.

**Skills you'll learn:**
- Loading shapefiles, GeoJSON, and other vector formats
- Handling different encoding issues  
- Reading spatial data from URLs
- Working with compressed spatial data files

### 🔍 Function 2: `explore_spatial_properties()` (4 points)  
**Interactive Learning:** `notebooks/03_explore_properties.ipynb`

**What it does:** Analyze the spatial characteristics of your dataset - coordinate systems, spatial extent, geometry types, and attribute information.

**Skills you'll learn:**
- Understanding coordinate reference systems (CRS)
- Calculating spatial bounds and extent
- Identifying geometry types (Point, LineString, Polygon)
- Exploring spatial and attribute data together

### ✅ Function 3: `validate_spatial_data()` (4 points)
**Interactive Learning:** `notebooks/04_validate_data.ipynb`

**What it does:** Identify and fix common spatial data quality issues like invalid geometries, missing coordinates, and projection problems.

**Skills you'll learn:**
- Detecting invalid or corrupted geometries
- Finding missing or null spatial data
- Identifying coordinate system mismatches
- Cleaning and repairing spatial datasets

### 🌍 Function 4: `standardize_crs()` (3 points)
**Interactive Learning:** `notebooks/05_coordinate_systems.ipynb`

**What it does:** Transform spatial data between different coordinate reference systems for analysis and visualization.

**Skills you'll learn:**
- Understanding when and why to reproject data
- Converting between geographic and projected coordinate systems
- Working with common CRS like WGS84, Web Mercator, and UTM zones
- Handling CRS transformations for different analysis needs

---

## 🧪 Testing and Development Workflow

### 🎯 The Spatial Data Learning Cycle

```bash
# 1. 📖 Learn interactively (start here!)
jupyter notebook notebooks/01_spatial_data_overview.ipynb

# 2. 🔬 Experiment with concepts
# Work through each notebook to understand spatial operations

# 3. 💻 Implement your functions
# Edit src/spatial_basics.py with guided TODO comments

# 4. 🧪 Test your implementation
uv run pytest tests/test_spatial_basics.py::test_load_spatial_dataset -v

# 5. 🔄 Iterate until passing
# Fix issues, re-test, repeat for each function

# 6. 🎉 Run all tests
uv run pytest tests/ -v
```

### 💡 Pro Development Tips

**Start with the notebooks!** They contain:
- Step-by-step explanations of spatial concepts
- Working code examples you can modify
- Real spatial datasets to experiment with
- Common error solutions and debugging tips

**Development workflow:**
```bash
# Test one function at a time:
uv run pytest tests/ -k "test_load_spatial_dataset" -v

# Get detailed error information:
uv run pytest tests/ -v --tb=long

# Test your code interactively:
uv run python -c "from src.spatial_basics import *; test_your_function()"
```

---

## 🤖 Automated Grading System

### 📊 Grade Breakdown (15 points total)
- **Function 1** (load_spatial_dataset): 4 points
- **Function 2** (explore_spatial_properties): 4 points  
- **Function 3** (validate_spatial_data): 4 points
- **Function 4** (standardize_crs): 3 points

### 🔄 How Grading Works
1. **Push your code** → GitHub runs automated tests
2. **View results** → Check the "Actions" tab in your repo
3. **Get feedback** → Detailed test results show what's working
4. **Iterate** → Fix issues and push again (unlimited attempts!)

---

## 🛠️ Troubleshooting Spatial Issues

### 🪟 Windows-Specific Issues (Use Codespaces Instead!)
If you're having problems on Windows:
- **GDAL installation errors** → Use Codespaces (pre-installed)
- **Fiona import failures** → Use Codespaces (configured correctly)  
- **Shapely geometry errors** → Use Codespaces (proper spatial libraries)
- **Projection database issues** → Use Codespaces (complete PROJ setup)

### ❓ Common Spatial Problems

**"No module named 'geopandas'" error:**
```bash
# Make sure you're in the right environment:
uv run python -c "import geopandas"  # Use 'uv run'
```

**CRS/Projection errors:**
```python
# Check your CRS:
print(gdf.crs)
# Common CRS codes: 4326 (WGS84), 3857 (Web Mercator)
```

**Invalid geometry errors:**
```python
# Check for invalid geometries:
invalid = gdf[~gdf.geometry.is_valid]
print(f"Found {len(invalid)} invalid geometries")
```

**File loading problems:**
```python
# Check file paths and formats:
import os
print(f"File exists: {os.path.exists('data/cities/cities.shp')}")
```

### 🆘 Getting Help

1. **Check the notebooks first** - they contain solutions to common problems
2. **Read test failure messages** - they often explain exactly what's wrong
3. **Use the spatial data documentation** - GeoPandas has excellent examples
4. **Ask specific questions** - "My CRS transformation isn't working with this dataset..."

---

## 📤 Submission Instructions

### ✅ Before You Submit

**Test everything locally:**
```bash
# Run all tests and make sure they pass:
uv run pytest tests/ -v

# Check that all functions are implemented:
uv run python -c "from src.spatial_basics import *; print('All functions imported successfully!')"
```

**Final checklist:**
- [ ] All 4 functions implemented in `src/spatial_basics.py`
- [ ] All tests passing locally (`uv run pytest tests/ -v`)
- [ ] Code is well-commented and readable
- [ ] No errors when importing your functions

### 🚀 Submit Your Work

**Your code is automatically submitted when you push to GitHub:**
```bash
# Save your work:
git add src/spatial_basics.py
git commit -m "Complete spatial data functions implementation"
git push origin main

# Check results:
# Go to GitHub → Your repo → "Actions" tab → View test results
```

**No pull requests needed** - just push to your main branch!

---

## 🎓 Professional Spatial Skills Developed

### 🗺️ Core GIS Programming Capabilities
- **Spatial data formats**: Working with industry-standard vector formats
- **Coordinate systems**: Understanding and transforming between projections  
- **Data quality**: Identifying and fixing spatial data problems
- **GeoPandas workflows**: Using Python's primary spatial analysis library

### 🚀 Professional Development Skills
- **pytest testing**: Industry-standard Python testing framework
- **Jupyter notebooks**: Interactive development and documentation
- **Git workflow**: Version control for spatial analysis projects
- **uv package management**: Modern Python dependency management

**These skills directly apply to:**
- Spatial data preprocessing for GIS analysis
- Building robust geospatial data pipelines
- Quality assurance for spatial datasets
- Professional GIS software development

---

## 📚 Spatial Data Resources

### 🗺️ GeoPandas and Spatial Analysis
- [GeoPandas Documentation](https://geopandas.org/) - Official docs with examples
- [Coordinate Reference Systems](https://spatialreference.org/) - CRS database and definitions
- [Shapely Documentation](https://shapely.readthedocs.io/) - Geometric operations library

### 📊 Spatial Datasets and Testing
- [Natural Earth Data](https://www.naturalearthdata.com/) - Free global spatial datasets
- [OpenStreetMap](https://www.openstreetmap.org/) - Crowd-sourced spatial data

### 🔧 Development Tools  
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package management

---

## 🏆 Success Tips for Spatial Analysis

1. **🎓 Start with the overview notebook** - understand spatial data concepts first
2. **🔬 Experiment interactively** - use notebooks to test ideas before implementing
3. **📏 Test with small datasets** - easier to debug with simple examples
4. **🗺️ Understand your coordinate systems** - many spatial errors come from CRS mismatches  
5. **✅ Validate your data early** - check for issues before analysis
6. **🔄 Run tests frequently** - catch problems early in development
7. **📖 Read error messages carefully** - spatial libraries provide helpful debugging info
8. **🌍 Think about real-world applications** - how will you use these skills in GIS work?

**Remember:** Spatial data analysis is a skill that improves with practice. Focus on understanding the concepts, and the implementation will follow!

---

*This assignment is designed to build practical spatial data skills you'll use throughout your GIS career. Every function you implement here solves real problems that spatial analysts face daily.*