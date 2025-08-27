# PostGIS Fundamentals - Spatial Database Basics

## 🎯 Assignment Overview

**Welcome to the world of spatial databases!** This assignment introduces you to **PostGIS**, the spatial extension for PostgreSQL that powers enterprise GIS applications worldwide. You'll learn when and why to use spatial databases, how to set up a PostGIS environment, and perform fundamental spatial operations using SQL.

**Assignment:** PostGIS Fundamentals - Database Setup and Basic Queries  
**Points:** 20 (4 functions × 5 points each)  
**Estimated Time:** 3-4 hours  
**Prerequisites:** Basic SQL knowledge, Python fundamentals  

### 🎓 Why This Matters for Your GIS Career

Spatial databases are the backbone of enterprise GIS systems. Understanding PostGIS will help you:

- **Scale Beyond Desktop:** Handle datasets too large for traditional GIS software
- **Enable Multi-User Access:** Allow teams to work with the same data simultaneously  
- **Integrate with Applications:** Connect GIS data to web apps, mobile apps, and business systems
- **Optimize Performance:** Use spatial indexes for lightning-fast queries on massive datasets
- **Ensure Data Integrity:** Maintain consistent, validated spatial data across your organization

---

## 🚀 Getting Started

### Step 1: Accept the Assignment

1. Click the assignment link provided by your instructor
2. Accept the GitHub Classroom assignment  
3. Clone your personal repository to your development environment

### Step 2: Choose Your Development Environment

#### 🌟 **Recommended: GitHub Codespaces (Cloud-Based)**

```bash
# Click "Code" → "Open with Codespaces" → "New codespace"
# Wait for environment to load, then run setup:
docker-compose up -d
python -m pip install -e .
```

#### 🖥️ **Alternative: Local Development**

**Requirements:**
- Docker Desktop installed and running
- Python 3.11 or higher
- Git for version control

```bash
# Clone your repository
git clone <your-repo-url>
cd postgis-basics

# Start PostGIS database
docker-compose up -d

# Install Python dependencies  
pip install -e .
```

### Step 3: Verify Your Environment

#### Database Connection Test
```bash
# Test database is running
docker-compose ps

# Test Python connection
python -c "import psycopg2; print('✅ Database libraries ready!')"
```

#### Run Initial Tests
```bash
# Should show 4 failing tests (expected!)
pytest tests/ -v
```

**✅ Success Indicators:**
- Docker shows PostGIS container running
- Python imports work without errors
- Tests run (even if failing) - this confirms your environment is set up correctly

---

## 📁 Understanding Your Assignment Files

```
postgis-basics/
├── README.md                          # This file - your assignment guide
├── src/
│   └── postgis_basics.py             # 🎯 YOUR CODE GOES HERE
├── tests/
│   └── test_postgis_basics.py        # Tests that verify your functions work
├── notebooks/
│   └── learning-postgis-basics.ipynb  # Step-by-step learning guide
├── data/
│   ├── sample_cities.csv             # City data for loading
│   ├── sample_parks.geojson          # Park boundaries
│   └── init.sql                      # Database initialization script
├── docker-compose.yml                # PostGIS database setup
└── .github/workflows/test-and-grade.yml # Automated grading
```

**🎯 Focus on `src/postgis_basics.py`** - This is where you'll implement your functions.

---

## 📝 Your Assignment Tasks

You'll implement **4 functions** that demonstrate fundamental PostGIS operations. Each function is worth **5 points** and focuses on core database skills you'll use in professional GIS work.

### 🔌 Part 1: Database Connection and Setup (5 points)

**Function:** `connect_to_postgis()`

**What you'll learn:**
- How to connect to PostGIS databases programmatically
- Database connection best practices and error handling
- Environment-based configuration for different deployment scenarios

**Professional context:** Every GIS application that uses databases needs reliable connection management. You'll use these patterns in web apps, automated processing scripts, and data integration workflows.

```python
def connect_to_postgis():
    """
    Connect to the PostGIS database and verify the connection.
    
    Returns:
        psycopg2.connection: Active database connection
        
    Requirements:
        - Connect to localhost:5432, database 'gis_analysis'
        - Username: 'gis_student', Password: 'gis604b'
        - Verify PostGIS extension is available
        - Handle connection errors gracefully
    """
```

### 📊 Part 2: Load Spatial Data (5 points) 

**Function:** `load_spatial_data(connection, cities_file, parks_file)`

**What you'll learn:**
- Import CSV and GeoJSON data into PostGIS tables
- Create appropriate spatial data types and constraints
- Handle coordinate system specifications and transformations

**Professional context:** Data loading is a daily task for GIS database administrators. You'll learn techniques used in ETL (Extract, Transform, Load) processes that keep enterprise databases up-to-date.

```python
def load_spatial_data(connection, cities_file, parks_file):
    """
    Load city and park data into PostGIS tables.
    
    Parameters:
        connection: Active database connection
        cities_file: Path to cities CSV file (with lat/lon columns)
        parks_file: Path to parks GeoJSON file
        
    Returns:
        dict: Summary of loaded data (row counts, table info)
        
    Requirements:
        - Create 'cities' table with Point geometry (EPSG:4326)
        - Create 'parks' table with Polygon geometry (EPSG:4326)
        - Include spatial indexes for performance
        - Return summary statistics of loaded data
    """
```

### 🔍 Part 3: Basic Spatial Queries (5 points)

**Function:** `analyze_spatial_relationships(connection)`

**What you'll learn:**
- Execute spatial queries using PostGIS functions
- Find spatial relationships (contains, intersects, distance)
- Aggregate spatial data for summary statistics

**Professional context:** These query patterns form the foundation of spatial analysis workflows. You'll use similar queries for site selection, impact analysis, and proximity studies.

```python
def analyze_spatial_relationships(connection):
    """
    Perform spatial analysis using PostGIS functions.
    
    Parameters:
        connection: Active database connection
        
    Returns:
        dict: Analysis results including:
            - cities_in_parks: List of cities within park boundaries
            - average_park_area: Average park area in square kilometers
            - nearest_park_distances: Distance from each city to nearest park
            
    Requirements:
        - Use ST_Contains() to find cities within parks
        - Use ST_Area() to calculate park areas (convert to km²)
        - Use ST_Distance() to find nearest park to each city
        - Return results in organized dictionary format
    """
```

### 💾 Part 4: Export and Validate Results (5 points)

**Function:** `export_analysis_results(connection, output_directory)`

**What you'll learn:**
- Export spatial data to multiple formats (CSV, GeoJSON, Shapefile)
- Validate data integrity and spatial accuracy
- Create summary reports for stakeholders

**Professional context:** Data export is crucial for sharing results with stakeholders, integrating with other systems, and creating deliverables. You'll learn formats used across different GIS platforms.

```python
def export_analysis_results(connection, output_directory):
    """
    Export analysis results to multiple formats.
    
    Parameters:
        connection: Active database connection
        output_directory: Directory path for output files
        
    Returns:
        dict: Export summary with file paths and record counts
        
    Requirements:
        - Export cities table to CSV with coordinates
        - Export parks table to GeoJSON format
        - Create a summary report (TXT file) with analysis statistics
        - Validate exported data matches database content
        - Return summary of exported files and record counts
    """
```

---

## 🧪 Professional Development Workflow

### Step 1: Learning with Notebooks

Start with the **Jupyter notebook** to learn PostGIS concepts interactively:

```bash
# Start Jupyter server
jupyter notebook notebooks/learning-postgis-basics.ipynb
```

The notebook covers:
- **Database Connection Basics:** Understanding connection parameters and security
- **PostGIS Functions Overview:** Key spatial functions and their use cases  
- **Spatial Data Types:** Points, lines, polygons, and coordinate systems
- **Query Optimization:** Using spatial indexes for better performance
- **Real-World Examples:** See how these techniques solve actual GIS problems

### Step 2: Implement Functions

Open `src/postgis_basics.py` and implement each function:

1. **Start Simple:** Get basic connectivity working first
2. **Test Incrementally:** Run tests after each function to catch issues early
3. **Use PostGIS Documentation:** Reference official PostGIS function documentation
4. **Follow SQL Best Practices:** Use parameterized queries and proper error handling

### Step 3: Test-Driven Development

Run tests frequently to guide your development:

```bash
# Test specific function
pytest tests/test_postgis_basics.py::test_connect_to_postgis -v

# Test all functions
pytest tests/ -v

# Get detailed test output
pytest tests/ -v --tb=short
```

### Step 4: Debug and Iterate

Use these debugging strategies:

```bash
# Check database connection manually
docker-compose exec postgis psql -U gis_student -d gis_analysis

# View table contents
docker-compose exec postgis psql -U gis_student -d gis_analysis -c "SELECT * FROM cities LIMIT 5;"

# Check PostGIS functions
docker-compose exec postgis psql -U gis_student -d gis_analysis -c "SELECT PostGIS_Version();"
```

### Step 5: Final Validation

```bash
# Run complete test suite
pytest tests/ -v --cov=src

# Verify all data exports
ls -la outputs/

# Check database performance
pytest tests/ --benchmark-only
```

---

## 📊 Sample Data Provided

### `sample_cities.csv`
```csv
name,latitude,longitude,population
Phoenix,33.4484,-112.0740,1608139
Tucson,32.2217,-110.9265,545975
Flagstaff,35.1983,-111.6513,76831
```

### `sample_parks.geojson`  
Contains park boundary polygons around Arizona cities with attributes including:
- Park name and type
- Area in square meters
- Management agency
- Establishment year

---

## 🗄️ Database Connection Details

**Database Configuration:**
- **Host:** localhost (when using Docker)
- **Port:** 5432
- **Database:** gis_analysis
- **Username:** gis_student
- **Password:** gis604b
- **Extensions:** PostGIS 3.4 enabled

**Connection String Example:**
```python
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'gis_analysis', 
    'user': 'gis_student',
    'password': 'gis604b'
}
```

---

## 📚 Learning Resources

### PostGIS Documentation
- [PostGIS Reference](https://postgis.net/documentation/) - Official function documentation
- [PostGIS Tutorial](https://postgis.net/workshops/postgis-intro/) - Comprehensive learning guide
- [Spatial SQL Cookbook](https://postgis.net/docs/using_postgis_dbmanagement.html) - Common query patterns

### Key PostGIS Functions You'll Use
```sql
-- Geometry creation and conversion
ST_GeomFromText()     -- Create geometry from Well-Known Text
ST_MakePoint()        -- Create point from coordinates  
ST_AsGeoJSON()        -- Export geometry as GeoJSON

-- Spatial relationships
ST_Contains()         -- Test if geometry A contains B
ST_Intersects()       -- Test if geometries overlap
ST_Distance()         -- Calculate distance between geometries

-- Measurements
ST_Area()             -- Calculate polygon area
ST_Length()           -- Calculate line length
ST_Perimeter()        -- Calculate polygon perimeter

-- Indexing and performance
CREATE INDEX ON table USING GIST (geom);  -- Spatial index
```

### Python Database Libraries
- **psycopg2:** Industry-standard PostgreSQL adapter for Python
- **SQLAlchemy:** Object-relational mapping (ORM) for complex applications  
- **GeoAlchemy2:** Spatial extensions for SQLAlchemy

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**❌ Problem:** Docker container won't start
```bash
# Solution: Check Docker Desktop is running, then restart services
docker-compose down
docker-compose up -d --build
```

**❌ Problem:** Can't connect to database
```bash
# Solution: Verify container is running and ports are available
docker-compose ps
docker-compose logs postgis
```

**❌ Problem:** PostGIS functions not found
```bash
# Solution: Verify PostGIS extension is installed
docker-compose exec postgis psql -U gis_student -d gis_analysis -c "SELECT PostGIS_Version();"
```

**❌ Problem:** Spatial index errors
```bash
# Solution: Check geometry column exists and has valid SRID
docker-compose exec postgis psql -U gis_student -d gis_analysis -c "SELECT Find_SRID('public', 'cities', 'geom');"
```

**❌ Problem:** Python import errors
```bash
# Solution: Reinstall dependencies
pip install -e .
# or with uv
uv sync
```

---

## 📤 Submission Requirements

### What to Submit

1. **✅ Completed `src/postgis_basics.py`** with all 4 functions implemented
2. **✅ Passing tests** - all automated tests should pass
3. **✅ Database verification** - your functions should work with the provided PostGIS setup

### Grading Breakdown (20 points total)

| Component | Points | Requirements |
|-----------|--------|-------------|
| **Function 1:** `connect_to_postgis()` | 5 | Successfully connects to PostGIS and verifies extensions |
| **Function 2:** `load_spatial_data()` | 5 | Loads data with proper spatial types and indexes |
| **Function 3:** `analyze_spatial_relationships()` | 5 | Executes spatial queries and returns correct results |
| **Function 4:** `export_analysis_results()` | 5 | Exports data to multiple formats with validation |

### Success Checklist

- [ ] **Database Connection:** Can connect to PostGIS without errors
- [ ] **Data Loading:** Successfully imports both CSV and GeoJSON data  
- [ ] **Spatial Queries:** Executes spatial analysis functions correctly
- [ ] **Data Export:** Creates valid output files in specified formats
- [ ] **Tests Passing:** All automated tests complete successfully
- [ ] **Code Quality:** Functions include proper error handling and documentation
- [ ] **Docker Environment:** Database starts and runs consistently

---

## 🎓 Why This Matters for GIS

### When to Use Spatial Databases vs. Files

**✅ Use PostGIS When You Need:**
- **Multi-user editing:** Teams working on the same datasets
- **Complex analysis:** Advanced spatial operations with SQL
- **Large datasets:** Millions of features with fast query performance  
- **Data integrity:** Validation rules and transaction safety
- **Web applications:** Backend data for mapping applications
- **Enterprise integration:** Connection to business systems and workflows

**📄 Use Files When You Have:**
- **Simple projects:** Basic desktop GIS workflows
- **Small datasets:** Under 100MB of spatial data
- **Single user:** Individual analysis projects
- **Visualization focus:** Primary goal is making maps

### Real-World Applications

**Urban Planning:** Query all properties within 500m of proposed transit stations
**Environmental Analysis:** Find endangered species habitats intersecting development zones  
**Emergency Management:** Identify evacuation routes avoiding flood-prone areas
**Asset Management:** Track infrastructure assets with spatial and temporal queries
**Business Intelligence:** Analyze customer locations relative to service territories

---

## 🆘 Getting Help

### During Development
- **Read error messages carefully** - PostgreSQL provides detailed error information
- **Test database connections manually** using the Docker commands provided
- **Use the learning notebook** for interactive exploration of PostGIS concepts
- **Check PostGIS documentation** for function syntax and examples

### If You're Stuck
- **Office Hours:** Bring specific error messages and your attempted solutions
- **Discussion Forum:** Share challenges with classmates (but not solution code)  
- **Debugging Steps:** Work through the troubleshooting section systematically
- **Professional Practice:** Learning to debug database issues is a valuable career skill

---

**🎯 Remember: This assignment builds the foundation for enterprise-level GIS workflows. The database skills you learn here will serve you throughout your career in positions requiring scalable, multi-user geospatial data management.**

*Focus on understanding the concepts and patterns - these techniques will apply to any spatial database system you encounter in your professional work.*