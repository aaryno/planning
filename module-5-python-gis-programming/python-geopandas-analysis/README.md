# Python GeoPandas Analysis - Advanced Spatial Operations

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 20 | Due: One week from assignment date**

---

## 🎯 Assignment Overview

Master **advanced spatial analysis** using Python's GeoPandas library! This assignment teaches you essential skills for geometric operations, spatial joins, and creating professional maps - the core techniques used in GIS analysis workflows.

**Prerequisites:** Complete `python-geopandas-intro` assignment first! This builds on spatial data fundamentals.

**What you'll learn:**
- Perform geometric operations (buffers, centroids, area/distance calculations)
- Execute spatial joins to combine datasets based on location
- Conduct spatial analysis workflows (intersections, aggregations, multi-criteria filtering)
- Create professional static maps and interactive visualizations
- **Advanced spatial testing** - professional GeoPandas testing practices
- **Jupyter-based development** - prototype analysis workflows interactively

**🎓 Learning Approach:**
This assignment uses **interactive Jupyter notebooks** to teach you each analysis technique step-by-step, then you implement the actual code in Python files for grading. This mirrors real-world GIS workflows where you prototype analysis interactively before writing production code!

**Time commitment:** About 4-5 hours total (includes notebook learning and implementation)

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
tests/test_spatial_analysis.py::test_calculate_geometric_properties FAILED
tests/test_spatial_analysis.py::test_create_spatial_buffers FAILED
... (This is expected - you haven't implemented the functions yet!)
```

---

## 📁 Understanding Your Files

```
python-geopandas-analysis/
├── 📖 README.md                    # This file - your assignment guide!
├── 📓 notebooks/                   # Interactive learning materials
│   ├── 01_analysis_overview.ipynb        # Start here! Analysis workflow intro
│   ├── 02_geometric_operations.ipynb     # Buffers, centroids, measurements
│   ├── 03_spatial_joins_analysis.ipynb   # Combining datasets by location
│   └── 04_mapping_visualization.ipynb    # Creating professional maps
├── 🐍 src/                         # Your implementation area
│   └── spatial_analysis.py        # Implement the 8 functions here
├── 🧪 tests/                       # Automated tests (don't modify!)
│   └── test_spatial_analysis.py   # Tests for your spatial functions
├── 📊 data/                        # Sample spatial datasets
│   ├── cities/                     # Urban areas and city points
│   ├── watersheds/                 # Environmental boundaries
│   ├── roads/                      # Transportation networks
│   ├── landcover/                  # Environmental classification data
│   └── README.md                   # Dataset descriptions and sources
└── ⚙️  Configuration files          # Project setup (uv, pytest, etc.)
```

---

## 📝 Your Assignment Tasks

You need to implement **8 advanced spatial analysis functions** organized into 3 modules:

### 📐 Module 1: Geometric Operations (3 functions - 8 points)
**Interactive Learning:** `notebooks/02_geometric_operations.ipynb`

**Function 1: `calculate_geometric_properties()`** (3 points)
- Calculate area, perimeter, and length measurements
- Generate centroids and bounding boxes
- Handle different geometry types appropriately

**Function 2: `create_spatial_buffers()`** (3 points)  
- Create buffer zones around features
- Handle different buffer distances and units
- Generate both fixed and variable-distance buffers

**Function 3: `perform_geometric_transformations()`** (2 points)
- Simplify complex geometries for visualization
- Create convex hulls around point clusters
- Transform geometries for analysis needs

### 🔗 Module 2: Spatial Joins & Analysis (3 functions - 7 points)
**Interactive Learning:** `notebooks/03_spatial_joins_analysis.ipynb`

**Function 4: `execute_spatial_intersection()`** (3 points)
- Find overlapping features between datasets
- Perform point-in-polygon analysis
- Handle different intersection scenarios

**Function 5: `aggregate_spatial_data()`** (2 points)
- Summarize attributes by spatial groups
- Calculate statistics for spatial regions
- Create spatial summaries and reports

**Function 6: `filter_by_spatial_criteria()`** (2 points)
- Apply complex spatial and attribute filters
- Select features based on spatial relationships
- Create multi-criteria selection workflows

### 🎨 Module 3: Mapping & Visualization (2 functions - 5 points)
**Interactive Learning:** `notebooks/04_mapping_visualization.ipynb`

**Function 7: `create_static_choropleth_map()`** (3 points)
- Generate professional thematic maps
- Apply appropriate color schemes and classification
- Include legends, labels, and proper cartographic elements

**Function 8: `generate_interactive_map()`** (2 points)
- Create interactive web maps using Folium
- Add multiple layers with proper controls
- Include popups and interactive features

---

## 🧪 Testing and Development Workflow

### 🎯 The Advanced Spatial Analysis Cycle

```bash
# 1. 📖 Learn interactively (start here!)
jupyter notebook notebooks/01_analysis_overview.ipynb

# 2. 🔬 Experiment with specific techniques
# Work through each notebook to understand spatial operations

# 3. 💻 Implement your functions
# Edit src/spatial_analysis.py with guided TODO comments

# 4. 🧪 Test individual functions
uv run pytest tests/test_spatial_analysis.py::test_calculate_geometric_properties -v

# 5. 🔄 Iterate until passing
# Fix issues, re-test, repeat for each function

# 6. 🎉 Run all tests
uv run pytest tests/ -v
```

### 💡 Pro Development Tips

**Start with the overview notebook!** It contains:
- Real-world spatial analysis examples
- Complete workflow demonstrations
- Common analysis patterns and approaches
- Integration examples showing how functions work together

**Development workflow:**
```bash
# Test one module at a time:
uv run pytest tests/ -k "geometric" -v    # Test geometric operations
uv run pytest tests/ -k "spatial" -v     # Test spatial joins/analysis
uv run pytest tests/ -k "mapping" -v     # Test visualization functions

# Get detailed error information:
uv run pytest tests/ -v --tb=long

# Test interactively in notebooks:
# Use notebooks to prototype before implementing in .py files
```

---

## 🤖 Automated Grading System

### 📊 Grade Breakdown (20 points total)
**Module 1: Geometric Operations (8 points)**
- calculate_geometric_properties: 3 points
- create_spatial_buffers: 3 points  
- perform_geometric_transformations: 2 points

**Module 2: Spatial Analysis (7 points)**
- execute_spatial_intersection: 3 points
- aggregate_spatial_data: 2 points
- filter_by_spatial_criteria: 2 points

**Module 3: Visualization (5 points)**
- create_static_choropleth_map: 3 points
- generate_interactive_map: 2 points

### 🔄 How Grading Works
1. **Push your code** → GitHub runs automated tests
2. **View results** → Check the "Actions" tab in your repo
3. **Get feedback** → Detailed test results show what's working
4. **Iterate** → Fix issues and push again (unlimited attempts!)

---

## 🛠️ Troubleshooting Spatial Analysis Issues

### 🪟 Windows-Specific Issues (Use Codespaces Instead!)
If you're having problems on Windows:
- **GDAL/GEOS errors** → Use Codespaces (pre-installed)
- **Shapely import failures** → Use Codespaces (configured correctly)  
- **Folium map display issues** → Use Codespaces (proper web environment)
- **Large dataset memory errors** → Use Codespaces (more RAM available)

### ❓ Common Advanced Spatial Problems

**"Topology Exception" errors:**
```python
# Usually caused by invalid geometries:
gdf = gdf[gdf.geometry.is_valid]  # Filter out invalid geometries
# OR fix them:
gdf.geometry = gdf.geometry.buffer(0)  # Often fixes invalid polygons
```

**Spatial join returns no results:**
```python
# Check CRS compatibility:
print(f"Dataset 1 CRS: {gdf1.crs}")
print(f"Dataset 2 CRS: {gdf2.crs}")
# Ensure both datasets use same CRS before joining
gdf2 = gdf2.to_crs(gdf1.crs)
```

**Buffer operations fail:**
```python
# Project to appropriate CRS before buffering:
gdf_projected = gdf.to_crs('EPSG:3857')  # or appropriate UTM zone
buffered = gdf_projected.buffer(distance_in_meters)
buffered = buffered.to_crs(gdf.crs)  # Transform back if needed
```

**Interactive maps don't display:**
```python
# Check coordinate ranges:
print(gdf.total_bounds)
# Ensure coordinates are reasonable for web mapping (EPSG:4326)
gdf = gdf.to_crs('EPSG:4326')
```

### 🆘 Getting Help

1. **Check the notebooks first** - they contain solutions to common analysis problems
2. **Read test failure messages** - they often explain exactly what's expected
3. **Use the GeoPandas documentation** - excellent examples for all operations
4. **Ask specific questions** - "My spatial intersection isn't working with these datasets..."

---

## 📤 Submission Instructions

### ✅ Before You Submit

**Test everything locally:**
```bash
# Run all tests and make sure they pass:
uv run pytest tests/ -v

# Check that all functions are implemented:
uv run python -c "from src.spatial_analysis import *; print('All functions imported successfully!')"

# Test a complete analysis workflow in notebooks
```

**Final checklist:**
- [ ] All 8 functions implemented in `src/spatial_analysis.py`
- [ ] All tests passing locally (`uv run pytest tests/ -v`)
- [ ] Functions handle different geometry types appropriately
- [ ] Proper CRS handling in all spatial operations
- [ ] Maps display correctly and include proper styling
- [ ] Code is well-commented and readable

### 🚀 Submit Your Work

**Your code is automatically submitted when you push to GitHub:**
```bash
# Save your work:
git add src/spatial_analysis.py
git commit -m "Complete advanced spatial analysis functions"
git push origin main

# Check results:
# Go to GitHub → Your repo → "Actions" tab → View test results
```

**No pull requests needed** - just push to your main branch!

---

## 🎓 Professional Spatial Analysis Skills Developed

### 🗺️ Advanced GIS Programming Capabilities
- **Geometric analysis**: Calculating spatial metrics and performing geometric operations
- **Spatial relationships**: Understanding and implementing spatial joins and intersections  
- **Buffer analysis**: Creating zones of influence around geographic features
- **Data aggregation**: Summarizing spatial information across different scales
- **Cartographic visualization**: Creating publication-quality maps and interactive displays

### 🚀 Professional Development Skills
- **Jupyter workflow**: Interactive development and analysis documentation
- **Advanced pytest**: Testing complex spatial operations and edge cases
- **Performance optimization**: Handling large spatial datasets efficiently
- **Spatial data integration**: Combining multiple datasets for comprehensive analysis

**These skills directly apply to:**
- Environmental impact analysis and monitoring
- Urban planning and development projects
- Transportation network analysis
- Market analysis and site selection
- Emergency response and disaster management
- Natural resource management

---

## 📚 Advanced Spatial Analysis Resources

### 🗺️ GeoPandas and Spatial Analysis
- [GeoPandas User Guide](https://geopandas.org/en/stable/user_guide.html) - Comprehensive analysis examples
- [Spatial Analysis Cookbook](https://geographicdata.science/book/intro.html) - Advanced spatial analysis techniques
- [PostGIS Documentation](https://postgis.net/documentation/) - Reference for spatial operations concepts

### 📊 Visualization and Cartography
- [Folium Documentation](https://python-visualization.github.io/folium/) - Interactive web mapping
- [Matplotlib Cartography](https://matplotlib.org/basemap/) - Static map production
- [ColorBrewer](https://colorbrewer2.org/) - Cartographically sound color schemes

### 🔧 Development and Testing Tools  
- [Shapely Manual](https://shapely.readthedocs.io/) - Geometric operations library
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package management

---

## 🏆 Success Tips for Advanced Spatial Analysis

1. **🎓 Master the fundamentals first** - ensure you understand basic spatial concepts
2. **🗺️ Always check your CRS** - most spatial analysis errors come from projection issues
3. **🔍 Validate your geometries** - invalid geometries cause mysterious failures
4. **📏 Use appropriate projections** - geographic CRS for display, projected for analysis
5. **🧪 Test with simple data first** - debug with small datasets before scaling up
6. **📊 Visualize intermediate results** - maps help you catch errors early
7. **⚡ Optimize for performance** - spatial operations can be slow with large datasets
8. **🌍 Think about real-world applications** - how will these techniques help actual GIS work?

**Remember:** Advanced spatial analysis is about combining multiple operations into meaningful workflows. Focus on understanding how these functions work together to solve real problems!

---

*This assignment teaches the core spatial analysis techniques used by GIS professionals daily. These skills form the foundation for environmental analysis, urban planning, business intelligence, and countless other spatial applications. Master these techniques and you'll be ready for professional GIS analysis work!* 🌟