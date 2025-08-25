# Lecture: Python Package Managers and Dependency Management

## Module: Open Source GIS Programming with Python
**Duration:** 50 minutes
**Format:** Interactive lecture with multimedia content

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **Differentiate** between major Python package managers: pip, conda, poetry, and uv
- **Select** appropriate package managers for different GIS project scenarios
- **Implement** version pinning and dependency management best practices
- **Create** reproducible Python environments for spatial analysis projects

---

## Lecture Outline

### I. Introduction and Context (10 minutes)
- Why package management matters in Python GIS workflows
- The evolution of Python package management
- Common dependency conflicts in geospatial libraries

### II. Core Concepts (25 minutes)
- **Package Managers Overview**
  - What package managers do
  - Virtual environments and isolation
  - Version pinning and reproducibility

- **The Big Four: pip, conda, poetry, uv**
  - pip: The standard Python package installer
  - conda: Cross-platform package and environment manager
  - poetry: Modern dependency management and packaging
  - uv: Ultra-fast Python package installer

- **Choosing the Right Tool**
  - Project types and use cases
  - Performance considerations
  - Integration with different workflows

### III. Practical Applications (10 minutes)
- Setting up a GIS project environment
- Handling complex geospatial dependencies
- Migration strategies between package managers

### IV. Summary and Next Steps (5 minutes)
- Best practices for course projects
- Recommended workflows for different scenarios
- Connection to upcoming assignments

---

## Key Concepts

### Why Package Management Matters

**The Challenge**: Python GIS libraries have complex dependencies
```python
# A typical GIS project might need:
import geopandas     # Depends on: pandas, shapely, fiona, pyproj
import rasterio      # Depends on: numpy, GDAL, affine
import matplotlib    # Depends on: numpy, pillow, kiwisolver
import jupyter       # Depends on: ipython, tornado, jinja2
```

**Without proper management:**
- Version conflicts between libraries
- "It works on my machine" problems
- Difficult to reproduce analysis results
- Time wasted troubleshooting installation issues

**With good package management:**
- Reproducible environments across machines
- Consistent results for team collaboration
- Easy project setup and deployment
- Clear documentation of dependencies

### Package Manager Comparison

| Feature | pip | conda | poetry | uv |
|---------|-----|-------|--------|-----|
| **Speed** | Moderate | Slow | Moderate | Very Fast |
| **Dependency Resolution** | Basic | Advanced | Advanced | Advanced |
| **Binary Packages** | Limited | Excellent | Limited | Good |
| **Lock Files** | ❌ | ❌ | ✅ | ✅ |
| **Virtual Environments** | Manual | Built-in | Built-in | Built-in |
| **GIS Library Support** | Good | Excellent | Good | Good |

### pip: The Python Standard

**What it is**: The default package installer that comes with Python

**Strengths:**
- Installed with Python by default
- Simple, familiar commands
- Works with any Python package on PyPI
- Lightweight and fast for basic operations

**Weaknesses:**
- Basic dependency resolution
- No built-in environment management
- Difficult binary compilation for complex packages

**Basic Usage:**
```bash
# Install packages
pip install geopandas==0.14.1

# Install with version constraints
pip install "rasterio>=1.3.0,<2.0.0"

# Install from requirements file
pip install -r requirements.txt

# Create requirements file
pip freeze > requirements.txt
```

**Version Pinning with pip:**
```txt
# requirements.txt
geopandas==0.14.1
rasterio==1.3.9
matplotlib==3.8.2
jupyter==1.0.0
numpy==1.26.2
pandas==2.1.4
```

### conda: The Scientific Computing Choice

**What it is**: Cross-platform package and environment manager, especially popular for scientific computing

**Strengths:**
- Excellent binary package distribution
- Superior handling of non-Python dependencies (GDAL, GEOS, PROJ)
- Built-in environment management
- Great for complex geospatial libraries

**Weaknesses:**
- Slower package resolution and installation
- Larger storage requirements
- Can be complex for beginners

**Basic Usage:**
```bash
# Create environment with specific Python version
conda create -n gis-env python=3.13

# Activate environment
conda activate gis-env

# Install packages with version pinning
conda install geopandas=0.14.1 rasterio=1.3.9

# Install from conda-forge (better for GIS packages)
conda install -c conda-forge geopandas=0.14.1

# Export environment
conda env export > environment.yml
```

**Environment File (environment.yml):**
```yaml
name: gis-analysis
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.13
  - geopandas=0.14.1
  - rasterio=1.3.9
  - matplotlib=3.8.2
  - jupyter=1.0.0
  - pip
  - pip:
    - some-pip-only-package==1.0.0
```

### poetry: Modern Dependency Management

**What it is**: Modern dependency management and packaging tool with advanced dependency resolution

**Strengths:**
- Excellent dependency resolution
- Lock files for reproducible installs
- Integrated build and publishing tools
- Clean project structure

**Weaknesses:**
- Additional tool to learn
- Less binary package support than conda
- Overkill for simple scripts

**Basic Usage:**
```bash
# Initialize new project
poetry init

# Add dependencies with version constraints
poetry add "geopandas>=0.14.0,<0.15.0"
poetry add "rasterio^1.3.0"

# Install all dependencies
poetry install

# Run commands in poetry environment
poetry run python analysis.py
poetry run jupyter notebook
```

**Project File (pyproject.toml):**
```toml
[tool.poetry]
name = "gis-analysis-project"
version = "0.1.0"
description = "Spatial analysis for GIST 604B"

[tool.poetry.dependencies]
python = "^3.13"
geopandas = "0.14.1"
rasterio = "1.3.9"
matplotlib = "3.8.2"
jupyter = "1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
black = "^23.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### uv: Ultra-Fast Package Management

**What it is**: Next-generation Python package installer and resolver, written in Rust for speed

**Strengths:**
- Extremely fast installation (10-100x faster than pip)
- Advanced dependency resolution
- Drop-in replacement for pip
- Built-in virtual environment support

**Weaknesses:**
- Relatively new (less mature ecosystem)
- Limited binary package ecosystem compared to conda
- Still evolving rapidly

**Installation:**
```bash
# Install uv (multiple methods)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

**Modern Project Workflow (Preferred):**
```bash
# Initialize new project
uv init gis-analysis-project
cd gis-analysis-project

# Add dependencies with version pinning
uv add "geopandas~=0.14.1"
uv add "rasterio~=1.3.9"
uv add "matplotlib~=3.8.2"

# Add development dependencies
uv add --dev "pytest~=7.4.0"
uv add --dev "black~=23.0.0"

# Run commands in project environment
uv run python analysis.py
uv run jupyter notebook

# Install all dependencies (like poetry install)
uv sync
```

**Legacy pip-compatible workflow:**
```bash
# Create virtual environment (if not using uv project)
uv venv gis-env
source gis-env/bin/activate

# Install packages with pip-style commands
uv pip install "geopandas==0.14.1"
uv pip install -r requirements.txt
```

**Performance Comparison (Installing GeoPandas + Dependencies):**
- **pip**: ~45 seconds
- **conda**: ~180 seconds  
- **poetry**: ~60 seconds
- **uv**: ~8 seconds

### Choosing the Right Package Manager

**Use pip when:**
- Working with simple, pure Python packages
- Need maximum compatibility
- Working in environments where only pip is available
- Quick prototyping and testing

**Use conda when:**
- Working with complex scientific/geospatial libraries
- Need reliable binary packages (GDAL, GEOS, PROJ)
- Managing multiple Python versions
- Working on Windows with complex dependencies

**Use poetry when:**
- Building distributable Python packages
- Need advanced dependency resolution
- Want reproducible lock files
- Working on larger, structured projects

**Use uv when:**
- Need fast package installation
- Want modern dependency resolution with lock files
- Prefer modern project structure (like poetry but faster)
- Working with large dependency sets
- Value performance in CI/CD pipelines
- Want drop-in replacement for pip with better features

### Version Pinning Strategies

**Exact Pinning (Reproducible):**
```bash
# pip/uv
uv pip install "geopandas==0.14.1"

# conda
conda install geopandas=0.14.1
```

**Compatible Range (Flexible):**
```bash
# pip/uv - compatible with 0.14.x
uv pip install "geopandas~=0.14.0"

# poetry - caret operator
poetry add "geopandas^0.14.0"
```

**Minimum Version (Permissive):**
```bash
# pip/uv
uv pip install "geopandas>=0.14.0"
```

**Best Practice for Course:**
```bash
# Pin major and minor versions, allow patch updates
uv pip install "geopandas~=0.14.1"  # Allows 0.14.x but not 0.15.x
uv pip install "rasterio~=1.3.9"    # Allows 1.3.x but not 1.4.x
```

### Virtual Environments

**Why Virtual Environments Matter:**
- Isolate project dependencies
- Prevent version conflicts between projects
- Enable different Python versions per project
- Make projects portable and reproducible

**Creating Environments with Different Tools:**
```bash
# pip + venv (built-in)
python -m venv gis-env
source gis-env/bin/activate  # Linux/Mac
gis-env\Scripts\activate     # Windows

# conda
conda create -n gis-env python=3.13
conda activate gis-env

# poetry (automatic)
poetry install  # Creates .venv automatically

# uv (modern project approach - preferred)
uv init my-gis-project
cd my-gis-project
# Environment created automatically, use: uv run python script.py

# uv (legacy venv approach)
uv venv gis-env
source gis-env/bin/activate
```

---

## Interactive Elements

### Discussion Questions

1. **Tool Selection**: You're starting a new GIS research project that will use GDAL, GeoPandas, and custom algorithms. The project needs to run on Windows, Mac, and Linux. Which package manager would you choose and why?

2. **Version Conflicts**: Your project needs GeoPandas 0.14.x (for new features) but a required dependency only supports GeoPandas 0.13.x. How would you approach resolving this with different package managers?

3. **Team Collaboration**: Your team has members using different operating systems and Python setups. What strategy would ensure everyone can reproduce the same analysis environment?

### Hands-on Activity

**Package Manager Speed Test:**
We'll time installing the same set of GIS packages with different tools:

1. **Setup test projects** with different package managers
2. **Time installations** of: `geopandas rasterio matplotlib jupyter contextily`
3. **Compare uv project workflow** vs traditional pip/conda
4. **Create reproducible lock files** with each tool
5. **Test project recreation** from saved configurations

**Demo Commands:**
```bash
# uv project approach
uv init test-gis && cd test-gis
time uv add "geopandas~=0.14.1" "rasterio~=1.3.9" "matplotlib~=3.8.2"

# pip approach
python -m venv pip-env && source pip-env/bin/activate
time pip install "geopandas~=0.14.1" "rasterio~=1.3.9" "matplotlib~=3.8.2"
```

---

## Resources

### Required Materials
- Access to terminal/command prompt in Codespaces
- Understanding of basic command-line operations
- Python 3.13 environment

### Supplementary Resources
- **uv Documentation**: https://docs.astral.sh/uv/
- **Poetry Guide**: https://python-poetry.org/docs/
- **Conda User Guide**: https://docs.conda.io/projects/conda/en/latest/user-guide/
- **pip Reference**: https://pip.pypa.io/en/stable/
- **Python Packaging Guide**: https://packaging.python.org/

### Performance Benchmarks
- **uv vs pip comparison**: https://github.com/astral-sh/uv#performance
- **Package manager comparison study**: https://lincolnloop.com/insights/python-package-manager-shootout/

---

## Preparation for Next Session

### Required Reading
- uv documentation: Getting Started section
- Review Python virtual environment concepts
- Understand semantic versioning (major.minor.patch)

### Recommended Preparation
- Install uv in your local development environment
- Practice creating virtual environments with different tools
- Review your current project dependencies

### Technical Setup
- Verify Python 3.13 availability in Codespaces
- Test uv installation and basic commands
- Prepare sample requirements.txt file

---

## Notes for Instructors

### Technical Requirements
- [ ] Codespaces with Python 3.13 support
- [ ] uv pre-installed or installation instructions
- [ ] Demo project directories for uv init workflow
- [ ] Sample GIS package requirements for timing tests
- [ ] Access to multiple package manager tools for comparison

### Common Issues
- **uv Installation**: Some environments may not have uv pre-installed - provide fallback pip instructions
- **Speed Differences**: Actual performance may vary based on network and system - focus on relative comparisons
- **conda Channels**: Students may need guidance on conda-forge channel for GIS packages
- **Virtual Environment Confusion**: Clarify when environments are active and how to check

### Timing Adjustments
- **If Running Behind**: Focus on uv and pip comparison, defer poetry/conda details
- **If Ahead**: Include hands-on environment setup with multiple tools
- **Interactive Extensions**: Let students suggest tools they've used and compare experiences

### Assessment Integration
- Connect to upcoming assignment requirements using uv
- Emphasize reproducibility for project work
- Show how proper dependency management prevents "works on my machine" issues

### Course Integration
- **Previous Knowledge**: Build on basic Python concepts from earlier modules
- **Next Sessions**: All subsequent assignments will use uv project workflow with `uv init` and `uv add`
- **Long-term Skills**: Prepare students for modern Python project management practices

### Version Pinning Philosophy
For course assignments, recommend:
- **Exact pinning** for critical GIS libraries (geopandas, rasterio)
- **Compatible range** for supporting libraries (matplotlib, pandas)
- **Document reasoning** for version choices in assignment instructions