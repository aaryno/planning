# Spatial Analysis with PostGIS - Advanced Database Operations

## 🎯 Assignment Overview

**Ready to unlock the power of spatial analysis?** This assignment builds on your PostGIS fundamentals to teach you **advanced spatial operations** that form the core of professional GIS analysis workflows. You'll learn to perform complex spatial queries that would be difficult or impossible with traditional file-based GIS.

**Assignment:** Spatial Analysis with PostGIS  
**Points:** 20 (4 functions × 5 points each)  
**Estimated Time:** 4-5 hours  
**Prerequisites:** PostGIS Basics assignment, understanding of spatial relationships  

### 🎓 Why This Matters for Your GIS Career

Advanced spatial analysis capabilities are what separate basic GIS users from GIS analysts and developers. Understanding these operations will help you:

- **Solve Complex Problems:** Tackle multi-criteria spatial analysis that combines multiple datasets
- **Optimize Performance:** Use database-native spatial operations for faster analysis of large datasets
- **Enable Real-Time Analysis:** Build applications that can perform spatial analysis on-demand
- **Support Decision Making:** Create sophisticated models for planning, environmental analysis, and business intelligence
- **Scale Your Analysis:** Handle enterprise-level spatial analysis workflows

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
cd spatial-analysis

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
spatial-analysis/
├── README.md                          # This file - your assignment guide
├── src/
│   └── spatial_analysis.py           # 🎯 YOUR CODE GOES HERE
├── tests/
│   └── test_spatial_analysis.py      # Tests that verify your functions work
├── notebooks/
│   └── learning-spatial-analysis.ipynb # Step-by-step learning guide
├── data/
│   ├── analysis_cities.csv           # City data with demographics
│   ├── analysis_parks.geojson        # Protected areas and parks
│   ├── watersheds.geojson             # Watershed boundaries
│   └── init_analysis.sql             # Database setup script
├── docker-compose.yml                # PostGIS database setup
└── .github/workflows/test-and-grade.yml # Automated grading
```

**🎯 Focus on `src/spatial_analysis.py`** - This is where you'll implement your functions.

---

## 📝 Your Assignment Tasks

You'll implement **4 functions** that demonstrate advanced PostGIS spatial analysis. Each function is worth **5 points** and focuses on operations commonly used in professional GIS workflows.

### 🔵 Part 1: Buffer Analysis and Zone Creation (5 points)

**Function:** `create_analysis_buffers(connection, buffer_distances)`

**What you'll learn:**
- Create variable-distance buffers around features
- Dissolve overlapping buffer zones
- Calculate buffer statistics and coverage areas
- Handle coordinate system transformations for accurate measurements

**Professional context:** Buffer analysis is fundamental to proximity studies, impact assessments, and regulatory compliance analysis. You'll use these techniques for emergency planning, environmental assessments, and site selection.

```python
def create_analysis_buffers(connection, buffer_distances):
    """
    Create buffer zones around cities and parks for proximity analysis.
    
    Parameters:
        connection: Active database connection
        buffer_distances: Dict with buffer distances in meters
                         e.g., {'cities': 5000, 'parks': 2000}
        
    Returns:
        dict: Buffer analysis results including:
            - buffer_areas: Total area of buffer zones (km²)
            - overlap_analysis: Areas where buffers intersect
            - coverage_statistics: Population within buffer zones
            
    Requirements:
        - Create accurate buffers using projected coordinates
        - Handle buffer overlaps and intersections
        - Calculate precise area measurements
        - Return comprehensive buffer statistics
    """
```

### 🔗 Part 2: Advanced Spatial Joins (5 points)

**Function:** `perform_spatial_joins(connection)`

**What you'll learn:**
- Execute complex spatial joins across multiple tables
- Use various spatial relationship predicates
- Aggregate spatial data across different feature types
- Handle one-to-many spatial relationships

**Professional context:** Spatial joins are the foundation of GIS analysis, enabling you to combine datasets based on location rather than common attributes. Essential for demographic analysis, environmental modeling, and asset management.

```python
def perform_spatial_joins(connection):
    """
    Perform comprehensive spatial joins between cities, parks, and watersheds.
    
    Parameters:
        connection: Active database connection
        
    Returns:
        dict: Spatial join results including:
            - cities_per_watershed: Cities grouped by watershed
            - parks_near_cities: Parks within specified distance of cities
            - watershed_park_coverage: Park area percentage per watershed
            - cross_boundary_analysis: Features spanning multiple boundaries
            
    Requirements:
        - Join cities to watersheds using ST_Contains/ST_Within
        - Find parks within 10km of each city using ST_DWithin
        - Calculate park coverage percentage per watershed
        - Identify features that cross watershed boundaries
    """
```

### 📐 Part 3: Complex Geometric Calculations (5 points)

**Function:** `calculate_spatial_metrics(connection)`

**What you'll learn:**
- Compute advanced geometric properties and measurements
- Calculate centroids, perimeters, and shape complexity metrics
- Perform coordinate system transformations for accurate measurements
- Generate spatial statistics for comparative analysis

**Professional context:** Geometric calculations support planning decisions, environmental assessments, and spatial modeling. These metrics help quantify spatial patterns and relationships in your data.

```python
def calculate_spatial_metrics(connection):
    """
    Calculate comprehensive spatial metrics for all features.
    
    Parameters:
        connection: Active database connection
        
    Returns:
        dict: Spatial metrics including:
            - feature_centroids: Centroid coordinates for all features
            - area_perimeter_ratios: Shape complexity measurements
            - nearest_neighbor_distances: Distance to closest similar feature
            - spatial_distribution_stats: Clustering and dispersion metrics
            
    Requirements:
        - Calculate true centroids using ST_Centroid
        - Compute area-to-perimeter ratios for shape analysis
        - Find nearest neighbor distances between cities
        - Generate spatial distribution statistics
    """
```

### 🔍 Part 4: Multi-Criteria Spatial Analysis (5 points)

**Function:** `perform_site_suitability_analysis(connection, criteria)`

**What you'll learn:**
- Combine multiple spatial criteria for decision support
- Weight different factors in spatial analysis
- Create composite suitability scores
- Generate recommendations based on spatial analysis

**Professional context:** Site suitability analysis is crucial for planning applications including facility location, conservation planning, and development suitability. These techniques support evidence-based decision making.

```python
def perform_site_suitability_analysis(connection, criteria):
    """
    Perform multi-criteria site suitability analysis.
    
    Parameters:
        connection: Active database connection
        criteria: Dict with analysis criteria and weights
                 e.g., {'min_distance_to_city': 5000, 'max_distance_to_park': 2000}
        
    Returns:
        dict: Suitability analysis results including:
            - suitable_locations: Areas meeting all criteria
            - suitability_scores: Weighted composite scores
            - constraint_analysis: How each criterion affects results
            - recommendations: Top-ranked locations with justification
            
    Requirements:
        - Apply multiple spatial constraints simultaneously
        - Weight criteria based on importance
        - Calculate composite suitability scores
        - Rank and recommend optimal locations
    """
```

---

## 🧪 Professional Development Workflow

### Step 1: Learning with Notebooks

Start with the **Jupyter notebook** to learn spatial analysis concepts interactively:

```bash
# Start Jupyter server
jupyter notebook notebooks/learning-spatial-analysis.ipynb
```

The notebook covers:
- **Buffer Operations:** Understanding distance calculations and projections
- **Spatial Joins:** Complex relationship analysis between datasets  
- **Geometric Calculations:** Advanced measurements and shape analysis
- **Multi-Criteria Analysis:** Combining spatial criteria for decision support
- **Performance Optimization:** Making complex queries run efficiently

### Step 2: Implement Functions

Open `src/spatial_analysis.py` and implement each function:

1. **Start with Buffers:** Get comfortable with distance calculations and coordinate systems
2. **Progress to Joins:** Build understanding of spatial relationships
3. **Add Calculations:** Incorporate geometric analysis
4. **Finish with Analysis:** Combine everything into decision support tools

### Step 3: Test-Driven Development

Run tests frequently to guide your development:

```bash
# Test specific function
pytest tests/test_spatial_analysis.py::test_create_analysis_buffers -v

# Test all functions
pytest tests/ -v

# Get detailed test output
pytest tests/ -v --tb=short
```

### Step 4: Debug and Iterate

Use these debugging strategies:

```bash
# Check database tables and data
docker-compose exec postgis psql -U gis_student -d spatial_analysis

# View spatial data with geometry details
docker-compose exec postgis psql -U gis_student -d spatial_analysis -c "SELECT name, ST_AsText(geom) FROM cities LIMIT 3;"

# Check spatial index performance
docker-compose exec postgis psql -U gis_student -d spatial_analysis -c "EXPLAIN ANALYZE SELECT * FROM cities WHERE ST_DWithin(geom, ST_MakePoint(-112, 33), 0.1);"
```

---

## 📊 Sample Data Provided

### `analysis_cities.csv`
Extended city data including:
```csv
name,latitude,longitude,population,area_km2,median_income,growth_rate
Phoenix,33.4484,-112.0740,1608139,1344.0,65000,2.3
Tucson,32.2217,-110.9265,545975,623.1,58000,1.1
Mesa,33.4152,-111.8315,504258,358.2,72000,3.2
```

### `analysis_parks.geojson`  
Comprehensive protected areas with attributes:
- Park classification and management agency
- Area measurements and establishment dates
- Activity types and access information
- Conservation status and ecological significance

### `watersheds.geojson`
Watershed boundary data including:
- Drainage basin hierarchies
- Flow direction and accumulation
- Water quality classifications
- Land use summaries

---

## 🗄️ Database Connection Details

**Database Configuration:**
- **Host:** localhost (when using Docker)
- **Port:** 5432
- **Database:** spatial_analysis
- **Username:** gis_student
- **Password:** gis604b
- **Extensions:** PostGIS 3.4 enabled

**Connection String Example:**
```python
conn_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'spatial_analysis', 
    'user': 'gis_student',
    'password': 'gis604b'
}
```

---

## 📚 Learning Resources

### PostGIS Spatial Functions Reference
- [ST_Buffer](https://postgis.net/docs/ST_Buffer.html) - Create buffer zones around geometries
- [ST_Intersects](https://postgis.net/docs/ST_Intersects.html) - Test spatial intersection
- [ST_Within](https://postgis.net/docs/ST_Within.html) - Test containment relationships
- [ST_DWithin](https://postgis.net/docs/ST_DWithin.html) - Test proximity relationships
- [ST_Union](https://postgis.net/docs/ST_Union.html) - Combine geometries
- [ST_Area](https://postgis.net/docs/ST_Area.html) - Calculate area measurements

### Key Spatial Analysis Patterns
```sql
-- Buffer with projection for accuracy
SELECT ST_Buffer(ST_Transform(geom, 3857), 1000) 
FROM cities;

-- Spatial join with distance constraint
SELECT c.name, p.name 
FROM cities c, parks p 
WHERE ST_DWithin(c.geom, p.geom, 0.1);

-- Multi-criteria spatial query
SELECT * FROM suitable_locations 
WHERE area_score > 0.8 
AND distance_score > 0.6 
AND access_score > 0.7;

-- Aggregate spatial statistics
SELECT watershed_id, 
       COUNT(cities.id) as city_count,
       SUM(ST_Area(parks.geom)) as total_park_area
FROM watersheds w
LEFT JOIN cities ON ST_Within(cities.geom, w.geom)
LEFT JOIN parks ON ST_Intersects(parks.geom, w.geom)
GROUP BY watershed_id;
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**❌ Problem:** Buffer operations return unexpected results
```bash
# Solution: Check coordinate system and units
docker-compose exec postgis psql -U gis_student -d spatial_analysis -c "SELECT ST_SRID(geom), ST_GeometryType(geom) FROM cities LIMIT 1;"
```

**❌ Problem:** Spatial joins are too slow
```bash
# Solution: Verify spatial indexes exist
docker-compose exec postgis psql -U gis_student -d spatial_analysis -c "SELECT tablename, indexname FROM pg_indexes WHERE indexname LIKE '%_geom_%';"
```

**❌ Problem:** Distance calculations seem inaccurate
```bash
# Solution: Use appropriate coordinate system for measurements
-- For accurate distance in Arizona, use UTM Zone 12N (EPSG:26912)
SELECT ST_Distance(
    ST_Transform(geom1, 26912), 
    ST_Transform(geom2, 26912)
);
```

**❌ Problem:** Complex queries run out of memory
```bash
# Solution: Break complex operations into steps and use temporary tables
CREATE TEMP TABLE temp_buffers AS 
SELECT id, ST_Buffer(ST_Transform(geom, 3857), buffer_dist) as geom 
FROM source_table;
```

---

## 📤 Submission Requirements

### What to Submit

1. **✅ Completed `src/spatial_analysis.py`** with all 4 functions implemented
2. **✅ Passing tests** - all automated tests should pass
3. **✅ Database verification** - your functions should work with the provided PostGIS setup

### Grading Breakdown (20 points total)

| Component | Points | Requirements |
|-----------|--------|-------------|
| **Function 1:** `create_analysis_buffers()` | 5 | Creates accurate buffers and calculates comprehensive statistics |
| **Function 2:** `perform_spatial_joins()` | 5 | Executes complex spatial joins across multiple tables |
| **Function 3:** `calculate_spatial_metrics()` | 5 | Computes advanced geometric measurements and statistics |
| **Function 4:** `perform_site_suitability_analysis()` | 5 | Combines multiple criteria for decision support analysis |

### Success Checklist

- [ ] **Buffer Analysis:** Can create variable-distance buffers with overlap analysis
- [ ] **Spatial Joins:** Successfully joins multiple spatial datasets with different relationships  
- [ ] **Geometric Calculations:** Computes accurate measurements and shape metrics
- [ ] **Multi-Criteria Analysis:** Combines spatial criteria for suitability assessment
- [ ] **Tests Passing:** All automated tests complete successfully
- [ ] **Code Quality:** Functions include proper error handling and documentation
- [ ] **Performance:** Queries execute efficiently with appropriate indexes

---

## 🎓 Why This Matters for GIS

### Advanced Spatial Analysis Applications

**Urban Planning:**
- Site suitability for new developments
- Service area analysis for public facilities
- Transportation network optimization
- Growth boundary and zoning analysis

**Environmental Management:**
- Habitat connectivity analysis
- Pollution impact modeling
- Protected area effectiveness
- Species distribution modeling

**Business Intelligence:**
- Market penetration analysis
- Competitor proximity studies
- Customer catchment areas
- Supply chain optimization

**Emergency Management:**
- Evacuation zone modeling
- Resource allocation optimization
- Hazard exposure assessment
- Emergency response planning

### Real-World Impact

These spatial analysis techniques directly support:
- **Evidence-Based Decision Making:** Quantify spatial relationships to support planning decisions
- **Regulatory Compliance:** Ensure projects meet buffer and distance requirements
- **Risk Assessment:** Identify areas of concern through proximity and overlap analysis
- **Resource Optimization:** Locate facilities and services for maximum efficiency and coverage

---

## 🆘 Getting Help

### During Development
- **Read error messages carefully** - PostGIS provides detailed spatial error information
- **Test queries interactively** using the Docker PostgreSQL client
- **Use the learning notebook** for step-by-step spatial analysis guidance
- **Check PostGIS documentation** for function syntax and examples

### If You're Stuck
- **Office Hours:** Bring specific spatial queries and error messages
- **Discussion Forum:** Share challenges with spatial relationships (but not solution code)  
- **Debugging Steps:** Work through the troubleshooting section systematically
- **Professional Practice:** Learning to debug complex spatial queries is a valuable career skill

---

**🎯 Remember: This assignment teaches you the spatial analysis skills that distinguish GIS analysts from basic GIS users. Master these techniques, and you'll be able to tackle complex spatial problems that drive decision-making in professional environments.**

*Focus on understanding the spatial relationships and analysis patterns - these concepts apply to any spatial database system and will serve you throughout your GIS career.*