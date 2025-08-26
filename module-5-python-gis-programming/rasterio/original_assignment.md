all files should go in planning. In the module 5: combine the assignments python geopandas intro and join and create a directory for associated files that includes automated tests. The assignment should be automatically graded in CI/CD. Remember that these students are not advanced programmers and are barely python programmers. The assignments should largely guide the students into getting this assignment done. Use the assignment-python-pandas as a model (and the assignment-python-files as a model) 

# Assignment: Python GeoPandas Introduction

## Module: Open Source GIS Programming with Python
**Points:** 10
**Due:** One week after assignment
**Type:** Hands-on Programming with Spatial Data

---

## Assignment Overview

This assignment introduces you to GeoPandas, the premier Python library for working with geospatial vector data. You'll learn to load, manipulate, analyze, and visualize spatial data programmatically using modern Python project management with uv. This builds foundational skills for automated GIS workflows and spatial data science.

---

## Learning Objectives

By completing this assignment, you will be able to:
- **Initialize** and manage Python GIS projects using uv package manager
- **Load** spatial data from various formats using GeoPandas
- **Manipulate** geospatial data programmatically with pandas-style operations
- **Perform** basic spatial operations including buffering, intersection, and union
- **Visualize** spatial data using GeoPandas plotting capabilities
- **Export** processed spatial data to different file formats
- **Create** reproducible geospatial analysis environments

---

## Prerequisites

Before starting this assignment:
- [ ] Complete Python Package Managers lecture from this module
- [ ] Complete Python Pandas assignment from this module
- [ ] Have uv package manager installed
- [ ] Basic understanding of pandas DataFrames and operations
- [ ] Access to Codespaces or local development environment with Python 3.13+

---

## Technical Setup

### Step 1: Initialize uv Project
```bash
# Create new uv project for this assignment
uv init geopandas-intro --python 3.13
cd geopandas-intro

# Verify Python version
uv run python --version  # Should show Python 3.13.x
```

### Step 2: Add Required Dependencies
```bash
# Core geospatial packages with version pinning
uv add "geopandas~=0.14.1"
uv add "matplotlib~=3.8.2"
uv add "contextily~=1.4.0"
uv add "folium~=0.15.0"

# Development and analysis tools
uv add "jupyter~=1.0.0"
uv add "pandas~=2.1.4"
uv add "numpy~=1.26.2"

# Optional: Add development dependencies
uv add --dev "black~=23.0.0"
uv add --dev "pytest~=7.4.0"
```

### Step 3: Verify Installation
```bash
# Check project dependencies
uv tree

# Test GeoPandas import
uv run python -c "import geopandas as gpd; print(f'GeoPandas {gpd.__version__} ready!')"
```

### Step 4: Download Course Data
```bash
# Download the course data setup script
curl -O https://raw.githubusercontent.com/[course-repo]/planning/module-5-python-gis-programming/setup_course_data.py

# Run data setup in uv environment
uv run python setup_course_data.py
```

---

## Project Structure

Your uv project should have the following structure:
```
geopandas-intro/
├── pyproject.toml          # uv project configuration
├── uv.lock                # Locked dependency versions
├── data/                  # Course spatial datasets
│   ├── phoenix_schools.shp
│   ├── phoenix_census_tracts.shp
│   └── ... (other course data)
├── analysis_notebook.ipynb # Main assignment notebook
├── analysis_scripts/      # Python scripts
│   ├── data_exploration.py
│   ├── spatial_operations.py
│   └── visualization.py
├── output/                # Generated maps and exports
├── setup_course_data.py   # Data setup script
└── README.md             # Project documentation
```

---

## Assignment Tasks

### Part 1: Project Setup and Data Exploration (25 points)

#### 1.1 Environment Configuration (10 points)
- Create `pyproject.toml` with proper dependencies and metadata
- Document Python 3.13 compatibility requirements
- Set up development dependencies for code quality
- Create virtual environment isolation demonstration
- Generate `uv.lock` file for reproducible installs

**Example pyproject.toml section:**
```toml
[project]
name = "geopandas-intro-analysis"
version = "0.1.0"
description = "GIST 604B GeoPandas Introduction Assignment"
requires-python = ">=3.13"
dependencies = [
    "geopandas~=0.14.1",
    "matplotlib~=3.8.2",
    "contextily~=1.4.0",
    "folium~=0.15.0",
    "jupyter~=1.0.0",
]
```

#### 1.2 Data Loading and Exploration (15 points)
- Load course datasets using `gpd.read_file()` in uv environment
- Display dataset information using `.info()`, `.head()`, `.crs`
- Create data quality assessment for each dataset
- Document data sources, formats, and coordinate systems
- Generate summary statistics for spatial and attribute data

**Required Analysis:**
```python
# Run with: uv run python data_exploration.py
import geopandas as gpd
import matplotlib.pyplot as plt

# Load datasets
schools = gpd.read_file('data/phoenix_schools.shp')
census_tracts = gpd.read_file('data/phoenix_census_tracts.shp')
parks = gpd.read_file('data/phoenix_parks.shp')

# Analysis code here...
```

### Part 2: Spatial Operations and Analysis (35 points)

#### 2.1 Geometric Operations (20 points)
- Create 1-mile buffers around schools using appropriate projection
- Calculate area statistics for parks in square kilometers
- Find centroids of census tracts and measure distances
- Perform geometric validation and fix any invalid geometries
- Compare results across different coordinate reference systems

**Implementation Requirements:**
```bash
# Create spatial operations script
uv run python analysis_scripts/spatial_operations.py
```

#### 2.2 Spatial Relationships and Joins (15 points)
- Perform spatial join to find which census tract contains each school
- Identify parks within 500m of schools (proximity analysis)
- Calculate demographic statistics for school service areas
- Find overlapping features using spatial predicates
- Create summary tables of spatial relationship results

**Expected Output:**
- Spatial join results with demographic data attached to schools
- Proximity analysis results showing school-park relationships
- Statistical summary of service area characteristics

### Part 3: Data Processing and Transformation (25 points)

#### 3.1 Coordinate Reference System Management (10 points)
- Reproject all datasets to appropriate Arizona State Plane coordinate system
- Compare area calculations before and after projection
- Document CRS transformations and their impact on analysis
- Handle CRS mismatches between datasets programmatically
- Create functions for automated CRS management

**Required CRS Operations:**
```python
# Example: Project to Arizona Central State Plane (EPSG:2223)
arizona_crs = 'EPSG:2223'  # Arizona Central, US Feet
schools_projected = schools.to_crs(arizona_crs)
```

#### 3.2 Attribute Data Processing (10 points)
- Filter datasets based on multiple criteria
- Create new calculated fields (population density, school capacity ratios)
- Apply conditional logic for categorical classifications
- Handle missing values and data type conversions
- Implement data validation and quality checks

#### 3.3 Performance Optimization (5 points)
- Use spatial indexing for large dataset operations
- Implement memory-efficient processing techniques
- Time operations and document performance improvements
- Compare uv vs pip installation and execution speeds
- Optimize code for Python 3.13 performance features

### Part 4: Visualization and Export (15 points)

#### 4.1 Static Mapping (10 points)
- Create choropleth map of census tracts colored by population density
- Generate multi-layer maps showing schools, parks, and demographics
- Add proper legends, scale bars, and north arrows
- Export high-resolution maps (300 DPI) in multiple formats
- Create figure layouts with multiple subplots

**Map Requirements:**
```python
# Run with: uv run python analysis_scripts/visualization.py
fig, ax = plt.subplots(figsize=(15, 10))
# Map creation code...
plt.savefig('output/phoenix_analysis_map.png', dpi=300, bbox_inches='tight')
```

#### 4.2 Interactive Visualization and Export (5 points)
- Create interactive Folium map with multiple layers
- Add popups with detailed attribute information
- Export processed data to GeoPackage and GeoJSON formats
- Create web-ready interactive map as HTML
- Document export settings and format considerations

---

## Deliverables

### 1. Complete uv Project Directory
Submit your entire project directory containing:

#### Project Configuration Files:
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Locked dependency versions for reproducibility
- `README.md` - Project overview and usage instructions

#### Analysis Components:
- `analysis_notebook.ipynb` - Main Jupyter notebook with complete analysis
- `analysis_scripts/` - Modular Python scripts for each analysis component
- `output/` - Generated maps, charts, and processed datasets

#### Documentation:
- Code comments and docstrings throughout
- Markdown cells explaining each analysis step
- Technical decisions and methodology documentation

### 2. Analysis Report (Separate PDF)
Submit a **3-4 page technical report** containing:

#### Technical Implementation (40%)
- uv project setup and dependency management approach
- Spatial analysis methodology and coordinate system choices
- Code organization and modular design decisions
- Performance optimization strategies implemented
- Challenges encountered and solutions developed

#### Spatial Analysis Results (40%)
- Key findings from demographic and spatial analysis
- Interesting patterns discovered in Phoenix area data
- Statistical summaries and spatial relationship insights
- Limitations of the analysis and data quality issues
- Recommendations for further analysis or data collection

#### Modern Python Workflow Evaluation (20%)
- Comparison of uv vs traditional pip/conda workflows
- Benefits and challenges of version pinning and lock files
- Python 3.13 compatibility considerations and new features utilized
- Team collaboration and reproducibility advantages
- Recommendations for professional GIS project management

### 3. Reproducibility Test
Include instructions for complete project reproduction:

```bash
# Clone or download project
# Navigate to project directory
uv sync                    # Install exact dependencies
uv run jupyter notebook    # Start analysis environment
# OR
uv run python analysis_scripts/run_full_analysis.py
```

---

## Evaluation Criteria

### Technical Excellence (40%)
- **A (90-100%)**: Advanced uv usage, optimized code, Python 3.13 features utilized
- **B (80-89%)**: Correct uv project structure, good spatial analysis implementation
- **C (70-79%)**: Basic requirements met, functional code, minor technical issues
- **D/F (<70%)**: Significant technical problems, incomplete implementation

### Spatial Analysis Quality (35%)
- **A (90-100%)**: Sophisticated analysis, appropriate methods, meaningful insights
- **B (80-89%)**: Solid analysis with proper spatial operations and interpretation
- **C (70-79%)**: Basic spatial analysis requirements met adequately
- **D/F (<70%)**: Poor analysis quality, inappropriate methods, unclear results

### Project Management and Documentation (25%)
- **A (90-100%)**: Excellent project structure, comprehensive documentation, reproducible
- **B (80-89%)**: Good organization and documentation with minor gaps
- **C (70-79%)**: Adequate project structure and documentation
- **D/F (<70%)**: Poor organization, insufficient documentation, not reproducible

---

## Resources and References

### uv Package Manager
- [uv Documentation](https://docs.astral.sh/uv/)
- [uv Project Management Guide](https://docs.astral.sh/uv/guides/projects/)
- [Python 3.13 Compatibility Guide](https://docs.python.org/3.13/whatsnew/)

### GeoPandas and Spatial Analysis
- [GeoPandas Documentation](https://geopandas.org/en/stable/)
- [GeoPandas User Guide](https://geopandas.org/en/stable/docs/user_guide.html)
- [Spatial Analysis Examples](https://geopandas.org/en/stable/gallery/index.html)

### Python 3.13 New Features
- [Performance Improvements](https://docs.python.org/3.13/whatsnew/3.13.html#performance-improvements)
- [Type System Enhancements](https://docs.python.org/3.13/whatsnew/3.13.html#typing)
- [GIS-relevant Standard Library Updates](https://docs.python.org/3.13/whatsnew/3.13.html#improved-modules)

---

## Professional Development

### Skills Developed
- **Modern Python Project Management**: Using uv for dependency management and project isolation
- **Reproducible Research**: Creating shareable, version-controlled spatial analysis projects
- **Performance Optimization**: Leveraging Python 3.13 performance improvements for GIS workflows
- **Code Organization**: Structuring projects for maintainability and collaboration
- **Documentation**: Creating professional-level project documentation

### Industry Relevance
- **GIS Development**: Modern Python workflows are standard in professional GIS development
- **Data Science**: uv and modern package management are becoming industry standard
- **DevOps Integration**: Project structure supports CI/CD and automated deployment
- **Team Collaboration**: Reproducible environments essential for collaborative GIS projects

---

## Submission Instructions

### 1. Project Archive
- Create zip file: `LastName_FirstName_GeoPandas_Project.zip`
- Include complete uv project directory
- Ensure `uv.lock` file is included for dependency reproduction
- Test unzip and `uv sync` before submission

### 2. Analysis Report
- File name: `LastName_FirstName_GeoPandas_Report.pdf`
- Include all required sections and analysis
- Professional formatting with figures and tables

### 3. Verification Checklist
Before submission, verify:
- [ ] `uv sync` successfully reproduces environment
- [ ] `uv run jupyter notebook` starts without errors
- [ ] All analysis scripts run with `uv run python script.py`
- [ ] Output files generate correctly
- [ ] Project structure matches requirements

### 4. Submission Method
- Upload files to course LMS assignment dropbox
- Include brief cover note with any special instructions
- **Due Date**: [Insert specific due date]

---

## Getting Help

### Course Support
- **Office Hours**: Schedule code review sessions for uv workflow questions
- **Email**: aaryn@email.arizona.edu for technical troubleshooting
- **Discussion Forum**: Post uv and GeoPandas questions with code snippets
- **Study Groups**: Collaborate on project structure and spatial analysis approaches

### Troubleshooting Common Issues

#### uv Installation Problems
```bash
# Install uv if not available
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Verify installation
uv --version
```

#### Dependency Resolution Issues
```bash
# Clear cache and retry
uv cache clean
uv sync --refresh

# Check for conflicts
uv tree --show-duplicates
```

#### Python 3.13 Compatibility
```bash
# Ensure Python 3.13 is available
uv python list
uv python install 3.13

# Force Python 3.13 usage
uv init --python 3.13 project-name
```

#### GeoPandas Import Errors
```bash
# Verify installation in uv environment
uv run python -c "import geopandas; print('Success!')"

# Check for missing system dependencies
uv run python -c "import fiona, pyproj, shapely; print('All deps OK!')"
```

This assignment bridges traditional GIS analysis with modern Python development practices, preparing you for professional geospatial software development and data science careers. Focus on creating reproducible, well-documented analysis that demonstrates both spatial analysis skills and modern Python project management proficiency.