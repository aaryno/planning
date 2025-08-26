# Python GeoPandas Introduction - Automated Assessment

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 30 | Due: Two weeks from assignment date**

---

## ⚠️ IMPORTANT: Windows Users Read This First!

> **🪟 Windows Users:** Most open-source GIS tools work best in Unix environments (Linux/Mac). While GeoPandas can work on Windows, you may encounter installation issues, path problems, and compatibility challenges.
> 
> **✅ SOLUTION: Use GitHub Codespaces (FREE & RECOMMENDED)**
> - Click "Code" → "Create codespace on main" in your repository
> - Everything works immediately - no setup required!
> - Unix environment provided for you
> - **⚠️ Instructor cannot provide Windows-specific technical support**
> 
> **If you choose Windows local development:** You're responsible for resolving any OS-specific issues. We recommend switching to Codespaces if you encounter problems.

---

## 🎯 Assignment Overview

This assignment introduces you to **GeoPandas fundamentals** while teaching you professional spatial data analysis through **automated assessment**. You'll work with real-world geospatial datasets and create compelling visualizations while your code is continuously tested using **GitHub Actions CI/CD pipelines**.

### 🔑 Key Learning Innovation
- **Real-world Spatial Skills**: Work with actual geospatial datasets from around the world
- **Visual Results**: Create maps and visualizations that make spatial patterns clear
- **Interactive Development**: Use Jupyter notebooks to see your analysis evolve step-by-step
- **Professional Workflow**: Experience automated testing and quality assurance for GIS code
- **Immediate Feedback**: Get instant results on spatial analysis correctness and code quality

### 📋 Prerequisites
- Completion of "Python Pandas" assignment
- Basic understanding of coordinate systems and projections
- Familiarity with git/GitHub and Codespaces
- Comfort with Python basics and data manipulation

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-geopandas-intro-[your-username]`

### Step 2: Choose Your Development Environment

**🪟 Windows Users: Use GitHub Codespaces (STRONGLY Recommended)**
- ✅ **No setup required** - everything works immediately
- ✅ **No Windows compatibility issues** - Unix environment provided
- ✅ **No instructor support needed** - pre-configured and tested
- ✅ **Focus on learning GIS** - not troubleshooting OS problems

```bash
# For Windows users (and everyone else):
# 1. Go to your assignment repository on GitHub
# 2. Click "Code" → "Create codespace on main"  
# 3. Wait 2-3 minutes for automatic setup
# 4. Start learning immediately!
```

**🐧🍎 Mac/Linux Users: Choose Your Preference**

**Option A: GitHub Codespaces (Recommended for All)**
```bash
# Click "Code" → "Create codespace on main"
# GeoPandas environment will be pre-configured with all spatial libraries!
```

**Option B: Local Development (Mac/Linux Only)**
```bash
# Clone your repository
git clone https://github.com/your-org/your-assignment-repo.git
cd your-assignment-repo

# Install uv package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project with spatial dependencies
uv sync --all-extras --dev
```

### Step 3: Verify Your Environment

**In Codespaces (All Users) or Local Mac/Linux:**
```bash
# Check Python and spatial libraries
python --version  # Should be 3.13+
uv run python -c "import geopandas; print(f'GeoPandas {geopandas.__version__} ready!')"
uv run python -c "import contextily; print('Basemap support ready!')"

# Create sample data for tutorials
python setup_student_environment.py

# Start Jupyter for interactive development
uv run jupyter notebook notebooks/

# Run initial tests (these will fail until you implement functions)
uv run pytest tests/ -v
```

**Windows Local Users (Not Recommended):**
- You're on your own for setup issues
- See Windows troubleshooting section below
- Consider switching to Codespaces if you encounter problems

---

## 🖥️ Important: Development Environment Considerations

### Windows Users - Please Read Carefully! 

**The Challenge:** Most open-source GIS tools (GeoPandas, GDAL, PostGIS, etc.) were designed for Unix-like systems (Linux/Mac). While they work on Windows, you may encounter:
- Complex installation procedures
- Path-related issues (`/` vs `\`)
- Command-line differences
- Dependency conflicts

### ✅ Recommended Solution: Use GitHub Codespaces

**For Windows users, we STRONGLY recommend using GitHub Codespaces:**
- ✅ Pre-configured Unix environment with all spatial libraries
- ✅ No installation hassles or dependency issues  
- ✅ Consistent experience with course instructions
- ✅ Works from any browser - no local setup needed

```bash
# In your assignment repository:
# Click "Code" → "Create codespace on main"
# Everything will be ready in 2-3 minutes!
```

### 🪟 If You Choose Local Windows Development

**Windows users attempting local development should know:**
- Commands shown use Unix syntax (`ls`, `pwd`, etc.)
- File paths use forward slashes (`/`)
- Some spatial libraries may require additional setup

**Windows Command Equivalents:**
```powershell
# Unix → Windows PowerShell equivalents
ls                    # dir or Get-ChildItem
pwd                   # cd or Get-Location  
cat filename.txt      # type filename.txt or Get-Content filename.txt
```

**Windows-Specific Installation:**
```powershell
# Use Windows Package Manager or manual installation
# GeoPandas on Windows often requires conda/mamba:
conda install -c conda-forge geopandas
```

### ⚠️ Important Disclaimer

**Instructor Support Limitations:**
- ✅ Full support provided for Codespaces/Unix environments
- ❌ **No support available for Windows-specific issues**
- ❌ Cannot troubleshoot Windows path problems, DLL issues, etc.
- ❌ Cannot help with Windows-specific package installation

**Why This Policy?**
- Ensures consistent learning experience for all students
- Instructor expertise focused on GIS concepts, not OS troubleshooting  
- Codespaces provides standardized environment for everyone

### 💡 Bottom Line for Windows Users

1. **Use Codespaces** - It's free, fast, and eliminates all OS issues
2. **If you use Windows locally** - You're on your own for technical issues
3. **Focus on learning GIS** - Don't let OS problems distract from spatial analysis!

---

## 📁 Project Structure

```
your-assignment-repo/
├── 📜 README.md                           # This file
├── 📜 pyproject.toml                      # Spatial dependencies configuration
├── 🔧 uv.lock                             # Dependency lock file
├── 📁 .github/
│   ├── 📁 workflows/
│   │   └── 📜 automated-grading.yml       # Spatial analysis CI/CD pipeline ⚙️
│   └── 📁 scripts/
│       └── 📜 calculate_grade.py          # Geospatial grading logic
├── 📁 src/geopandas_analysis/             # 👈 YOUR SPATIAL CODE GOES HERE
│   ├── 📜 __init__.py
│   ├── 📜 spatial_data_loading.py         # 🗺️  Part 1: Load & explore spatial data
│   ├── 📜 geometric_operations.py         # 📐 Part 2: Spatial geometry operations
│   ├── 📜 spatial_joins_analysis.py       # 🔗 Part 3: Spatial relationships & joins
│   └── 📜 visualization_mapping.py        # 🎨 Part 4: Maps & interactive visualizations
├── 📁 notebooks/                          # 🧪 YOUR INTERACTIVE DEVELOPMENT
│   ├── 📜 01_data_exploration.ipynb       # 🔍 Explore datasets interactively
│   ├── 📜 02_spatial_operations.ipynb     # 📊 Test geometric operations
│   ├── 📜 03_analysis_workflow.ipynb      # 🔬 Develop spatial analysis
│   └── 📜 04_visualization_gallery.ipynb  # 🎭 Create and refine visualizations
├── 📁 tests/                              # ✅ Automated spatial tests (DON'T EDIT)
│   ├── 📜 test_spatial_data_loading.py    # Tests for data loading functions
│   ├── 📜 test_geometric_operations.py    # Tests for spatial operations
│   ├── 📜 test_spatial_joins.py           # Tests for spatial relationship analysis
│   ├── 📜 test_visualization.py           # Tests for mapping functions
│   └── 📜 test_fixtures.py                # Spatial test data and utilities
├── 📁 benchmarks/                         # ⚡ Spatial performance tests (DON'T EDIT)
│   └── 📜 spatial_performance_tests.py    # Speed tests for large spatial datasets
├── 📁 data/                               # 📊 Sample spatial datasets (PROVIDED)
│   ├── 📜 world_cities.geojson            # Global cities with population
│   ├── 📜 natural_earth_countries.shp     # World country boundaries
│   ├── 📜 us_states.geojson               # US state boundaries
│   └── 📜 sample_points.csv               # Point data with coordinates
└── 📁 output/                             # 🖼️  Generated maps and analysis results
    ├── 📜 maps/                           # Your generated static maps
    └── 📜 interactive/                    # Interactive HTML maps
```

---

## 📝 Assignment Tasks

You need to implement **4 spatial analysis modules** with specific functions that will be automatically tested:

### 🗺️  Part 1: Spatial Data Loading & Exploration (8 points)
**File:** `src/geopandas_analysis/spatial_data_loading.py`

**Interactive Development:** `notebooks/01_data_exploration.ipynb`

Implement these functions:
- `load_spatial_dataset()` - Load data from various formats (Shapefile, GeoJSON, etc.)
- `explore_spatial_properties()` - Analyze CRS, bounds, geometry types
- `validate_spatial_data()` - Check for invalid geometries and data quality issues
- `standardize_crs()` - Reproject data to appropriate coordinate systems

**What you'll learn:**
- Loading spatial data from different file formats
- Understanding coordinate reference systems (CRS)
- Identifying and fixing common spatial data issues
- Working with geometry types (points, lines, polygons)

### 📐 Part 2: Geometric Operations (10 points)  
**File:** `src/geopandas_analysis/geometric_operations.py`

**Interactive Development:** `notebooks/02_spatial_operations.ipynb`

Implement these functions:
- `calculate_spatial_metrics()` - Area, length, perimeter calculations
- `create_buffers_and_zones()` - Generate buffer zones around features
- `geometric_transformations()` - Centroids, convex hulls, simplification
- `proximity_analysis()` - Distance calculations and nearest neighbor analysis

**What you'll learn:**
- Measuring spatial properties (area, distance, perimeter)
- Creating buffer zones for analysis
- Transforming and simplifying geometries
- Analyzing spatial proximity and relationships

### 🔗 Part 3: Spatial Joins & Analysis (7 points)
**File:** `src/geopandas_analysis/spatial_joins_analysis.py`  

**Interactive Development:** `notebooks/03_analysis_workflow.ipynb`

Implement these functions:
- `spatial_intersection_analysis()` - Find overlapping features
- `point_in_polygon_analysis()` - Determine spatial containment
- `spatial_aggregation()` - Summarize attributes by spatial groups
- `multi_criteria_spatial_filter()` - Complex spatial and attribute filtering

**What you'll learn:**
- Performing spatial joins (intersects, contains, within)
- Aggregating data based on spatial relationships
- Combining spatial and attribute-based analysis
- Creating complex spatial queries

### 🎨 Part 4: Visualization & Interactive Mapping (5 points)
**File:** `src/geopandas_analysis/visualization_mapping.py`

**Interactive Development:** `notebooks/04_visualization_gallery.ipynb`

Implement these functions:
- `create_choropleth_map()` - Thematic maps with color-coded data
- `multi_layer_visualization()` - Combine multiple spatial datasets
- `interactive_web_map()` - Create interactive Folium maps
- `export_publication_maps()` - Generate high-quality static maps

**What you'll learn:**
- Creating professional static maps with proper symbology
- Building interactive web maps for data exploration
- Combining multiple spatial layers effectively
- Exporting maps for reports and publications

---

## 🤖 Automated Grading System

Every time you **push code** to GitHub, the automated grading system tests your spatial analysis:

### 📊 Grade Breakdown (30 points total)

| Component | Points | What's Tested |
|-----------|--------|---------------|
| **Spatial Correctness** | 15 | Spatial operations produce correct results |
| **Performance** | 5 | Speed with large spatial datasets |  
| **Code Quality** | 5 | Formatting, linting, spatial best practices |
| **Visualization Quality** | 5 | Maps are properly formatted and informative |

### 🔄 Spatial CI/CD Pipeline Steps

1. **Spatial Environment Setup**
   - Install GDAL, GEOS, PROJ spatial libraries
   - Configure GeoPandas with all dependencies
   - Verify spatial operations work correctly

2. **Code Quality Checks**
   - Black formatting for readable code
   - Ruff linting with spatial-specific rules
   - MyPy type checking for spatial objects
   - Spatial best practices validation

3. **Spatial Correctness Testing**
   - Geometric operation accuracy tests
   - CRS transformation validation
   - Spatial join correctness verification
   - Data integrity and topology checks

4. **Performance Benchmarks**
   - Large dataset processing speed
   - Memory efficiency with spatial data
   - Optimization of spatial indexing
   - Visualization rendering performance

5. **Map Quality Assessment**
   - Visual output validation
   - Proper symbology and legends
   - Interactive map functionality
   - Export format verification

---

## 💻 Development Workflow - The Spatial Analysis Cycle

### 🧪 Interactive Development Process

The key to success in this assignment is using the **interactive notebook workflow**:

1. **Explore in Jupyter** (`notebooks/` directory)
2. **Implement in Source** (`src/` directory)  
3. **Test Automatically** (push to GitHub)
4. **Refine and Repeat**

### 🔧 Local Development Commands

```bash
# Start interactive development environment
uv run jupyter notebook notebooks/

# Test specific spatial functions while developing
uv run pytest tests/test_spatial_data_loading.py -v
uv run pytest tests/test_geometric_operations.py -v

# Check code quality for spatial code
uv run black src/ tests/ notebooks/
uv run ruff check src/ tests/
uv run mypy src/

# Run spatial performance benchmarks
uv run pytest benchmarks/ --benchmark-only

# Test map generation and visualization
uv run python -c "from src.geopandas_analysis.visualization_mapping import *; test_visualization()"
```

### 📈 Interactive Workflow Example

**Step 1: Explore in Notebook**
```python
# In notebooks/01_data_exploration.ipynb
import geopandas as gpd
from geodatasets import get_path

# Load sample data interactively
world = gpd.read_file(get_path('naturalearth.land'))
world.head()
world.plot()  # See what it looks like!
```

**Step 2: Implement in Source File**
```python
# In src/geopandas_analysis/spatial_data_loading.py
def load_spatial_dataset(file_path: str) -> gpd.GeoDataFrame:
    """Load and validate spatial dataset."""
    # Copy your working code from the notebook
    return gpd.read_file(file_path)
```

**Step 3: Test Implementation**
```bash
# Run tests to verify your function works
uv run pytest tests/test_spatial_data_loading.py::test_load_spatial_dataset -v
```

**Step 4: Push and Get Feedback**
```bash
git add .
git commit -m "Implement spatial data loading function"
git push origin main
# Check GitHub Actions for automated feedback!
```

### 🔄 Typical Development Day

1. **Morning**: Open Jupyter, explore new spatial datasets
2. **Mid-day**: Transfer working code to source files
3. **Afternoon**: Run local tests, fix issues
4. **Evening**: Push code, review automated feedback, plan next day

---

## 📊 Understanding Your Spatial Analysis Grade

### 🎯 Grade Thresholds

| Grade | Total Score | Percentage | Spatial Skills Level |
|-------|-------------|------------|---------------------|
| **A** | 27-30 | 90-100% | ✅ Advanced spatial analyst |
| **B** | 24-26 | 80-89% | ✅ Competent GIS programmer |  
| **C** | 21-23 | 70-79% | ✅ Basic spatial analysis skills |
| **D** | 18-20 | 60-69% | ⚠️ Needs spatial skills improvement |
| **F** | < 18 | < 60% | ❌ Insufficient spatial knowledge |

### 📝 Reading Spatial Analysis Feedback

**✅ Example Excellent Spatial Analysis:**
```
🎉 Spatial Analysis Score: 28/30 (93.3%)

Component Scores:
✅ Spatial Operations: 14/15 (93%) - Excellent geometric calculations
✅ Performance: 5/5 (100%) - Efficient spatial indexing used
✅ Code Quality: 4/5 (80%) - Good spatial coding practices
✅ Visualizations: 5/5 (100%) - Outstanding maps with proper symbology

💡 Spatial Feedback:
✅ Perfect CRS handling and transformations
🗺️  Beautiful, informative choropleth maps
⚡ Excellent use of spatial indexing for performance
📐 All geometric operations mathematically correct
🎨 Interactive maps work perfectly with good UX
```

**❌ Example Needs Improvement:**
```
❌ Spatial Analysis Score: 16/30 (53.3%)

Component Scores:
❌ Spatial Operations: 8/15 (53%) - Geometric calculations incorrect
❌ Performance: 2/5 (40%) - Not using spatial indexes efficiently
✅ Code Quality: 4/5 (80%) - Code style is good
❌ Visualizations: 2/5 (40%) - Maps missing legends, poor colors

💡 Spatial Feedback:
🔧 Buffer calculations using wrong units (check CRS!)
🗺️  Maps need proper legends and color schemes
⚡ Use .sindex for spatial joins to improve performance
📐 Double-check area calculations - using degrees instead of meters?
🎨 Interactive maps not loading due to coordinate issues
```

---

## 🛠️ Troubleshooting Spatial Issues

### 🪟 Windows-Specific Issues (Use Codespaces Instead!)

**If you're experiencing issues on Windows, the solution is simple: Use GitHub Codespaces!**

**Common Windows Problems We Cannot Help With:**
- ❌ `ModuleNotFoundError` for spatial packages
- ❌ DLL loading errors with GDAL/GEOS
- ❌ Path issues with backslashes vs forward slashes
- ❌ Permission errors during package installation
- ❌ Conda/pip environment conflicts
- ❌ Windows-specific command syntax errors

**Windows Solution:**
```bash
# Instead of struggling with Windows setup:
# 1. Go to your GitHub repository
# 2. Click "Code" → "Create codespace on main"
# 3. Wait 2-3 minutes for setup
# 4. Start working immediately!
```

**Remember:** Instructor cannot provide Windows support. Save time and frustration by using Codespaces!

---

### ❓ Common Spatial Problems

**🌍 Coordinate Reference System (CRS) Issues**
```bash
# Debug CRS problems in notebook
import geopandas as gpd
gdf = gpd.read_file('data/sample.shp')
print(f"CRS: {gdf.crs}")
print(f"Bounds: {gdf.bounds}")
gdf.plot()  # Does it look right?

# Fix CRS issues
gdf_projected = gdf.to_crs('EPSG:3857')  # Web Mercator
```

**📐 Geometric Operation Errors**
```bash
# Check for invalid geometries
invalid_geoms = ~gdf.geometry.is_valid
print(f"Invalid geometries: {invalid_geoms.sum()}")

# Fix invalid geometries
gdf['geometry'] = gdf.geometry.buffer(0)
```

**🗺️  Visualization Problems**
```python
# Debug visualization in notebook
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', alpha=0.7)
plt.show()  # Does it appear?

# Add basemap context
import contextily as ctx
gdf_web_mercator = gdf.to_crs(epsg=3857)
ax = gdf_web_mercator.plot(figsize=(10, 10), alpha=0.5)
ctx.add_basemap(ax, crs=gdf_web_mercator.crs, source=ctx.providers.OpenStreetMap.Mapnik)
```

**⚡ Performance Issues**
```python
# Use spatial indexing for faster operations
gdf_indexed = gdf.copy()
spatial_index = gdf.sindex

# Faster spatial joins
result = gpd.sjoin(gdf1, gdf2, how='inner', predicate='intersects')
```

**💥 Import and Environment Errors**
```bash
# Verify spatial libraries
uv run python -c "import geopandas, fiona, pyproj, shapely; print('All spatial libs OK!')"

# Reinstall if needed
uv sync --all-extras --dev
```

**🪟 For Windows Users Having Local Issues:**
```bash
# Step 1: Stop struggling with Windows!
# Step 2: Use GitHub Codespaces instead
# Step 3: Focus on learning spatial analysis, not OS troubleshooting

# If you absolutely insist on Windows local development:
# - You're on your own for technical issues
# - Use conda/mamba instead of pip when possible
# - Expect path and dependency problems
# - Consider WSL2 (Windows Subsystem for Linux)
```

---

### 🆘 Getting Spatial Analysis Help

1. **Check your notebooks first** - The interactive environment shows exactly what's happening
2. **Visualize your data** - Always plot your spatial data to see if it looks right
3. **Check CRS and units** - Most spatial errors are CRS-related
4. **Read the automated feedback** - It often identifies the specific spatial issue
5. **Post on discussion forum** with your notebook output
6. **Attend office hours** for complex spatial analysis debugging

---

## 📤 Submission Instructions

### 🎯 Final Submission Process

1. **Complete all spatial functions:**
   ```bash
   uv run pytest tests/ -v
   # All spatial tests should pass
   ```

2. **Verify your notebooks work:**
   ```bash
   # Run all notebooks to ensure they execute completely
   uv run jupyter nbconvert --to notebook --execute notebooks/*.ipynb
   ```

3. **Check your maps and visualizations:**
   - Static maps in `output/maps/` should be high quality
   - Interactive maps in `output/interactive/` should load properly
   - All maps should have legends, proper colors, and clear symbology

4. **Final automated grade check:**
   ```bash
   python .github/scripts/calculate_grade.py
   # Should show ≥18 points (60%)
   ```

5. **Push your final code:**
   ```bash
   git add .
   git commit -m "Final spatial analysis submission - all tests passing"
   git push origin main
   ```

6. **Submit on Canvas:**
   - Your **GitHub repository URL**
   - **Screenshots of your best maps** (3-4 images)
   - **Final automated grade screenshot**

### ✅ Spatial Analysis Checklist

- [ ] All 4 spatial modules implemented with proper functions
- [ ] All geometric operations produce mathematically correct results
- [ ] Proper CRS handling and transformations throughout
- [ ] Static maps with legends, proper symbology, and clear design
- [ ] Interactive maps that load and function correctly
- [ ] Performance benchmarks meeting spatial efficiency requirements
- [ ] All Jupyter notebooks run completely without errors
- [ ] Final automated grade ≥ 18/30 points (60%)
- [ ] Repository includes sample output maps and visualizations

---

## 🎓 Professional Spatial Skills Developed

### 🗺️  Core GIS Programming Capabilities
- **Spatial Data Management**: Loading, validating, and transforming geospatial datasets
- **Geometric Analysis**: Calculating areas, distances, and spatial relationships
- **Coordinate Systems**: Understanding and applying CRS transformations
- **Spatial Joins**: Combining datasets based on geographic relationships
- **Performance Optimization**: Using spatial indexing for efficient operations

### 🎨 Cartography and Visualization
- **Static Mapping**: Creating publication-quality maps with proper design
- **Interactive Web Maps**: Building user-friendly web-based spatial interfaces  
- **Multi-layer Visualization**: Combining different spatial datasets effectively
- **Symbology Design**: Choosing appropriate colors, symbols, and legends

### 🚀 Professional Development Skills
- **Automated Testing**: Writing reliable spatial analysis code
- **Version Control**: Managing spatial analysis projects with git
- **Documentation**: Creating clear, reproducible spatial workflows
- **Performance Analysis**: Optimizing code for large spatial datasets
- **Quality Assurance**: Following spatial data best practices

---

## 📚 Spatial Analysis Resources

### 🗺️  GeoPandas and Spatial Analysis
- [GeoPandas Documentation](https://geopandas.org/en/stable/)
- [Spatial Analysis Guide](https://geopandas.org/en/stable/docs/user_guide.html)
- [GeoPandas Examples Gallery](https://geopandas.org/en/stable/gallery/index.html)

### 📊 Spatial Datasets and Data Sources  
- [GeoPandas Datasets](https://geopandas.org/en/stable/docs/reference/datasets.html)
- [Natural Earth Data](https://www.naturalearthdata.com/)
- [OpenStreetMap Data](https://planet.openstreetmap.org/)
- [US Census TIGER Files](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

### 🎨 Spatial Visualization
- [Matplotlib Geographic Plotting](https://matplotlib.org/basemap/)  
- [Contextily for Basemaps](https://contextily.readthedocs.io/)
- [Folium Interactive Maps](https://python-visualization.github.io/folium/)
- [Cartographic Design Principles](https://www.axismaps.com/guide/)

### 📐 Spatial Operations and Analysis
- [Shapely Geometric Operations](https://shapely.readthedocs.io/)
- [Spatial Indexing with Rtree](https://rtree.readthedocs.io/)
- [Coordinate Reference Systems](https://pyproj4.github.io/pyproj/)
- [GDAL/OGR Python Bindings](https://gdal.org/python/)

---

## 🏆 Success Tips for Spatial Analysis

1. **🪟 Windows Users: Use Codespaces!** Don't waste time on Windows setup issues - click "Code" → "Create codespace on main"
2. **Visualize Early and Often**: Always plot your spatial data to understand what you're working with
3. **Master CRS Management**: Most spatial errors come from coordinate system confusion
4. **Use the Interactive Workflow**: Develop in notebooks, then move working code to source files
5. **Start Simple**: Begin with basic operations, then build complexity
6. **Check Your Math**: Spatial calculations should make geographic sense
7. **Design Good Maps**: Invest time in proper legends, colors, and layout
8. **Test with Real Data**: Use the provided datasets that represent real-world challenges
9. **Monitor Performance**: Large spatial datasets require efficient algorithms
10. **Document Your Process**: Future you (and your instructor) will appreciate clear documentation
11. **Ask Spatial Questions**: Every function should solve a real geographic problem

---

**Ready to become a spatial analyst? 🗺️ This assignment will teach you the fundamental skills for professional GIS programming while creating beautiful, informative visualizations of real-world geographic data.**

**Remember: The goal isn't perfect code - it's developing spatial thinking and creating compelling visualizations that reveal geographic patterns and relationships! 🚀**