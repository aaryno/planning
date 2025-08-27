# PostGIS Spatial Analysis - Advanced Database Operations

**GIST 604B - Module 6: PostGIS Spatial Databases**  
**Assignment Type:** Foundation Level (⭐⭐)  
**Points:** 20 (10 queries × 2 points each)  
**Estimated Time:** 3-4 hours  
**Prerequisites:** SQL Introduction Assignment, PostGIS Basics Assignment

## 📖 Overview

Welcome to your advanced PostGIS spatial analysis assignment! This foundation-level exercise builds systematically from guided examples to independent challenges, teaching you sophisticated spatial operations essential for professional GIS work. You'll progress from basic spatial inspection to complex multi-criteria decision analysis, developing the analytical skills that distinguish GIS professionals from basic users.

### 🎯 Learning Objectives

By completing this assignment, you will:

- **Master advanced spatial analysis workflows** from data inspection to complex decision modeling
- **Develop progressive PostGIS expertise** through scaffolded learning from examples to challenges  
- **Apply coordinate system transformations** for accurate spatial measurements and analysis
- **Implement multi-layer spatial analysis** combining multiple datasets in comprehensive workflows
- **Create professional-grade spatial analysis solutions** suitable for real-world applications
- **Build confidence in spatial problem-solving** through guided practice and independent challenges

### 🏢 Professional Context

**Why Progressive Spatial Analysis Skills Matter:**

This assignment mirrors how GIS professionals develop expertise - starting with foundational concepts and progressing to complex problem-solving. These progressive skills prepare you for:

- **Environmental Consulting**: Impact assessments requiring multi-layer spatial analysis
- **Urban and Regional Planning**: Site selection using multi-criteria decision analysis
- **Emergency Management**: Network analysis for response optimization and coverage modeling
- **Conservation Biology**: Habitat connectivity analysis and protected area management
- **Business Intelligence**: Location analysis combining demographic, competitive, and accessibility factors
- **Transportation Engineering**: Route optimization and accessibility planning

**Real-World Applications:**
- Hospital site selection using accessibility, population, and service gap analysis
- Environmental impact assessment for proposed developments
- Emergency facility placement using multi-criteria decision frameworks
- Transportation network analysis for public transit optimization
- Conservation priority mapping using ecological and socioeconomic factors

### 📈 Progressive Learning Design

This assignment uses **scaffolded learning** where each query provides less guidance than the previous one:

- **Queries 1-2**: Complete examples and guided templates
- **Queries 3-4**: Templates with moderate guidance  
- **Queries 5-6**: Reduced guidance requiring spatial thinking
- **Queries 7-8**: Minimal guidance with strategic hints
- **Queries 9-10**: Challenge problems with problem statements only

This progression builds confidence while developing independent spatial analysis capabilities.

## 🚀 Getting Started

### Prerequisites
- Completed SQL Introduction assignment (foundational SQL skills)
- Completed PostGIS Basics assignment (spatial functions and relationships)
- Understanding of coordinate systems and spatial analysis concepts
- Docker installed and running
- VS Code with PostgreSQL extension (recommended)

### Environment Setup

**Step 1: Start the PostGIS Database**
```bash
# Navigate to assignment directory
cd path/to/postgis-spatial-analysis

# Start PostGIS database with sample data
docker-compose up -d

# Verify database is running
docker-compose ps
```

**Step 2: Connect to Database**

**Option A: VS Code (Recommended)**
1. Install PostgreSQL extension in VS Code
2. Add new connection with these settings:
   - **Host:** localhost
   - **Database:** spatial_analysis
   - **Username:** postgres
   - **Password:** postgres
   - **Port:** 5432

**Option B: Command Line**
```bash
# Connect via psql
docker exec -it postgis-spatial-analysis-postgres psql -U postgres -d spatial_analysis

# Test PostGIS installation
SELECT PostGIS_Version();
```

**Step 3: Verify Data Setup**
```sql
-- Check that all spatial tables have data
SELECT 'protected_areas' as table_name, COUNT(*) as records FROM protected_areas
UNION ALL
SELECT 'watersheds', COUNT(*) FROM watersheds
UNION ALL
SELECT 'transportation_network', COUNT(*) FROM transportation_network
UNION ALL
SELECT 'facilities', COUNT(*) FROM facilities
UNION ALL
SELECT 'monitoring_stations', COUNT(*) FROM monitoring_stations
UNION ALL
SELECT 'land_use_zones', COUNT(*) FROM land_use_zones;
```

## 📊 Dataset Overview - Colorado Rocky Mountain Region

This assignment uses a comprehensive spatial dataset focused on Colorado's Rocky Mountain region, designed to simulate real-world conservation and recreational planning scenarios.

### Spatial Tables

#### `protected_areas` Table (8 records - MULTIPOLYGON)
National parks, wilderness areas, and protected lands including:
- Rocky Mountain National Park (265,807 acres, 4.4M annual visitors)
- Great Sand Dunes National Park (107,341 acres)
- Mesa Verde National Park (52,485 acres, cultural heritage site)
- Indian Peaks Wilderness (76,711 acres)
- Multiple national monuments and wilderness areas

#### `watersheds` Table (4 records - MULTIPOLYGON)
Major river basin boundaries including:
- Upper Colorado River Basin (17,800 sq mi, avg elevation 7,200 ft)
- South Platte River Basin (24,300 sq mi, flows northeast)
- Arkansas River Basin (25,000 sq mi, highest elevation basin)
- Rio Grande Basin (8,000 sq mi, flows south)

#### `transportation_network` Table (8 records - MULTILINESTRING)
Roads, trails, and waterways including:
- Interstate 70 (424 miles, major east-west corridor)
- Trail Ridge Road (48 miles, seasonal alpine highway)
- Continental Divide Trail (760 miles, long-distance hiking)
- Colorado Trail (486 miles, multi-use recreation)
- Major rivers and scenic routes

#### `facilities` Table (12 records - POINT)
Visitor services and operational facilities including:
- Visitor centers with exhibits and education programs
- Campgrounds with varying capacity (88-244 sites)
- Ranger stations for emergency services
- Research stations and mountain huts

#### `monitoring_stations` Table (10 records - POINT)
Environmental and safety monitoring network including:
- Weather stations (alpine and valley locations)
- Air quality monitors (PM2.5, ozone, visibility)
- Water quality sensors (temperature, pH, dissolved oxygen)
- Seismic monitoring and stream gauges

#### `land_use_zones` Table (5 records - MULTIPOLYGON)
Management and ecological zones including:
- Alpine Tundra Zone (125,000 acres, minimal management)
- Subalpine Forest Zone (320,000 acres, multiple use)
- Critical Wildlife Habitat (180,000 acres, seasonal restrictions)
- Recreation Management Areas (varying intensity levels)

### Coordinate Systems Used
- **WGS84 (EPSG:4326)**: Geographic coordinates for global compatibility
- **Web Mercator (EPSG:3857)**: Projected coordinates for accurate area/distance calculations  
- **UTM Zone 13N (EPSG:26913)**: Regional projection for precision measurements

## 📝 Assignment Tasks (10 Queries × 2 Points = 20 Points)

Complete the following 10 spatial analysis queries with **progressive difficulty**. Early queries provide complete examples, while later queries require independent problem-solving.

### Query 1: Basic Spatial Data Inspection (2 points)
**File**: [`sql/01_spatial_inspection.sql`](sql/01_spatial_inspection.sql)  
**Difficulty**: ⭐ (Complete example provided)

**Objective**: Inspect spatial data to understand geometry types, coordinate systems, and basic spatial properties.

**What You Get**: A complete working example demonstrating PostGIS inspection functions.
**What You Learn**: Data exploration, geometry types, coordinate systems, spatial extents.

---

### Query 2: Simple Buffer Operations (2 points)
**File**: [`sql/02_simple_buffers.sql`](sql/02_simple_buffers.sql)  
**Difficulty**: ⭐ (Example with blanks to fill)

**Objective**: Create buffers around spatial features and calculate buffer areas and perimeters.

**What You Get**: Working example with clear blanks to complete for visitor centers.
**What You Learn**: ST_Buffer(), coordinate transformations, area calculations.

---

### Query 3: Basic Spatial Measurements (2 points)
**File**: [`sql/03_spatial_measurements.sql`](sql/03_spatial_measurements.sql)  
**Difficulty**: ⭐⭐ (Template with guidance)

**Objective**: Calculate distances, areas, and lengths using PostGIS measurement functions.

**What You Get**: Structured template with TODO items and helpful hints.
**What You Learn**: ST_Distance(), ST_Area(), ST_Length(), distance classifications.

---

### Query 4: Coordinate System Transformations (2 points)
**File**: [`sql/04_coordinate_transformations.sql`](sql/04_coordinate_transformations.sql)  
**Difficulty**: ⭐⭐ (Guided template)

**Objective**: Master coordinate system transformations for accurate measurements across different projections.

**What You Get**: Guided template with coordinate system comparisons.
**What You Learn**: ST_Transform(), SRID management, measurement accuracy.

---

### Query 5: Spatial Relationships (2 points)
**File**: [`sql/05_spatial_relationships.sql`](sql/05_spatial_relationships.sql)  
**Difficulty**: ⭐⭐ (Less guidance - moderate challenge)

**Objective**: Use spatial relationship functions to find features that intersect, contain, or are within other features.

**What You Get**: Partial templates requiring spatial thinking.
**What You Learn**: ST_Intersects(), ST_Contains(), ST_Within(), EXISTS clauses.

---

### Query 6: Spatial Joins and Multi-Table Analysis (2 points)
**File**: [`sql/06_spatial_joins.sql`](sql/06_spatial_joins.sql)  
**Difficulty**: ⭐⭐ (Moderate guidance - requires spatial thinking)

**Objective**: Perform spatial joins between multiple datasets to combine attributes based on geometric relationships.

**What You Get**: Strategic hints and partial examples.
**What You Learn**: Spatial JOINs, LATERAL joins, multi-table spatial queries.

---

### Query 7: Complex Buffer Analysis and Service Area Modeling (2 points)
**File**: [`sql/07_complex_buffer_analysis.sql`](sql/07_complex_buffer_analysis.sql)  
**Difficulty**: ⭐⭐⭐ (Minimal guidance - requires independent spatial thinking)

**Objective**: Perform advanced buffer operations including multi-distance buffers, buffer intersections, and service area analysis.

**What You Get**: Problem outline with analysis requirements only.
**What You Learn**: Multi-zone buffers, overlap analysis, service gap identification.

---

### Query 8: Multi-Layer Spatial Intersections (2 points)
**File**: [`sql/08_multi_layer_intersections.sql`](sql/08_multi_layer_intersections.sql)  
**Difficulty**: ⭐⭐⭐ (Hints only - significant independent work required)

**Objective**: Perform complex multi-layer intersection analysis to understand how different spatial datasets overlap and interact.

**What You Get**: Strategic hints and function suggestions only.
**What You Learn**: Complex intersections, environmental impact analysis, multi-layer workflows.

---

### Query 9: Transportation Network Analysis and Accessibility Modeling (2 points)
**File**: [`sql/09_network_analysis.sql`](sql/09_network_analysis.sql)  
**Difficulty**: ⭐⭐⭐⭐ (Problem statement and strategic hints only)

**Objective**: Analyze transportation network connectivity and accessibility to model optimal routing and identify infrastructure gaps.

**What You Get**: Problem statement with strategic approach suggestions.
**What You Learn**: Network analysis, accessibility modeling, routing efficiency.

---

### Query 10: Multi-Criteria Spatial Decision Analysis Challenge (2 points)
**File**: [`sql/10_decision_analysis_challenge.sql`](sql/10_decision_analysis_challenge.sql)  
**Difficulty**: ⭐⭐⭐⭐⭐ (Ultimate challenge - problem statement only)

**Objective**: Implement a comprehensive multi-criteria decision analysis system to solve a complex real-world spatial planning problem.

**What You Get**: Business problem statement and requirements only.
**What You Learn**: MCDA methodology, spatial decision frameworks, professional analysis workflows.

## 🧪 Testing Your Solutions

### Test Individual SQL Files
```bash
# Test a specific query
python test_assignment.py::TestPostGISSpatialAnalysis::test_01_spatial_inspection -v

# Run individual query in database
docker exec -it postgis-spatial-analysis-postgres psql -U postgres -d spatial_analysis -f sql/01_spatial_inspection.sql
```

### Test All Queries
```bash
# Run complete test suite
python test_assignment.py -v

# Run all completed queries in sequence
for i in {01..10}; do
  echo "Testing query $i..."
  docker exec -it postgis-spatial-analysis-postgres psql -U postgres -d spatial_analysis -f sql/${i}_*.sql
done
```

### Interactive Testing
```bash
# Connect to database and test queries manually
docker exec -it postgis-spatial-analysis-postgres psql -U postgres -d spatial_analysis

# Run your SQL file
\i sql/01_spatial_inspection.sql
```

### Automated Grading
```bash
# Run complete grading suite
python grading/calculate_grade.py --verbose

# Generate JSON report
python grading/calculate_grade.py --json-output grade-report.json
```

## 📋 Submission Requirements

### Files to Submit
Your submission must include all completed SQL files:
- `sql/01_spatial_inspection.sql` - Basic spatial data inspection
- `sql/02_simple_buffers.sql` - Simple buffer operations  
- `sql/03_spatial_measurements.sql` - Basic spatial measurements
- `sql/04_coordinate_transformations.sql` - Coordinate system transformations
- `sql/05_spatial_relationships.sql` - Spatial relationships
- `sql/06_spatial_joins.sql` - Spatial joins and multi-table analysis
- `sql/07_complex_buffer_analysis.sql` - Complex buffer analysis
- `sql/08_multi_layer_intersections.sql` - Multi-layer spatial intersections
- `sql/09_network_analysis.sql` - Transportation network analysis
- `sql/10_decision_analysis_challenge.sql` - Multi-criteria decision analysis

### Grading Criteria (2 points each = 20 total)

Each query is evaluated on:
- **Query Execution (1 point)**: SQL runs without errors and returns valid results
- **Spatial Analysis Accuracy (1 point)**: Correct use of PostGIS functions and logical results

**Progressive Difficulty Expectations:**
- **Queries 1-4**: Focus on correct completion of templates and understanding of concepts
- **Queries 5-7**: Emphasis on spatial thinking and problem-solving approach
- **Queries 8-10**: Advanced analysis demonstrating independent PostGIS mastery

**Grade Scale:**
- **18-20 points (90-100%)**: Advanced PostGIS proficiency - ready for professional spatial analysis
- **16-17 points (80-89%)**: Good spatial analysis foundation - minor refinements needed  
- **14-15 points (70-79%)**: Adequate progress - focus on later challenges for improvement
- **12-13 points (60-69%)**: Basic competency - review spatial concepts and practice
- **Below 12 points (<60%)**: Needs significant improvement - consider additional study

### Submission Process
1. Complete SQL query files working progressively from Query 1 to Query 10
2. Test your queries using the automated test suite
3. Verify results using the grading script  
4. Submit via your course management system or version control

## 🔧 PostGIS Quick Reference

### Essential Spatial Functions
```sql
-- Spatial Relationships
ST_Intersects(geom1, geom2)      -- Test if geometries intersect
ST_Contains(geom1, geom2)        -- Test if geom1 contains geom2
ST_Within(geom1, geom2)          -- Test if geom1 is within geom2
ST_DWithin(geom1, geom2, distance) -- Test if within distance

-- Spatial Operations  
ST_Buffer(geometry, radius)      -- Create buffer around geometry
ST_Intersection(geom1, geom2)    -- Return intersection geometry
ST_Union(geometry_set)           -- Combine multiple geometries
ST_Difference(geom1, geom2)      -- Return geom1 minus geom2

-- Measurements
ST_Area(geometry)                -- Calculate area
ST_Length(geometry)              -- Calculate length  
ST_Distance(geom1, geom2)        -- Calculate distance
ST_Perimeter(geometry)           -- Calculate perimeter

-- Coordinate Transformations
ST_Transform(geometry, srid)     -- Transform coordinate system
ST_SRID(geometry)                -- Get spatial reference ID

-- Data Inspection
ST_GeometryType(geometry)        -- Get geometry type
ST_AsText(geometry)              -- Convert to Well-Known Text
ST_Extent(geometry_set)          -- Calculate bounding box
```

### Common Coordinate Systems
- **EPSG:4326** - WGS84 Geographic (longitude/latitude)
- **EPSG:3857** - Web Mercator (meters, good for web maps)
- **EPSG:26913** - UTM Zone 13N (meters, accurate for Colorado)

### Distance and Area Conversions
```sql
-- Distance conversions
meters_to_miles = meters / 1609.34
meters_to_feet = meters * 3.28084

-- Area conversions  
sq_meters_to_acres = sq_meters / 4047
sq_meters_to_sq_miles = sq_meters / 2589988
```

## 🔧 Troubleshooting

### Common PostGIS Errors

**"function st_intersects does not exist"**
- **Solution**: Ensure PostGIS extension is installed: `CREATE EXTENSION postgis;`

**"transform: couldn't project point"**
- **Solution**: Check SRID values and ensure coordinates are within valid bounds
- Verify coordinate system definitions in `spatial_ref_sys` table

**"parse error - invalid geometry"**
- **Solution**: Check for valid geometry construction
- Use `ST_IsValid(geometry)` to test geometry validity

### Performance Tips

**For large datasets:**
- Always use spatial indexes (created automatically with GIST)
- Transform to projected coordinates (3857 or 26913) for distance/area calculations
- Use ST_DWithin() instead of ST_Distance() for "within distance" queries

**Query optimization:**
- Place most selective conditions first in WHERE clauses
- Use LIMIT when testing queries on large datasets
- Consider using ST_Simplify() for complex geometries when appropriate

## 🎯 Success Criteria

### Technical Proficiency Indicators
- [ ] All completed queries execute without errors
- [ ] Proper use of coordinate transformations for accurate measurements
- [ ] Logical progression from guided examples to independent analysis
- [ ] Appropriate spatial functions chosen for each analysis goal
- [ ] Evidence of spatial thinking and problem-solving development

### Professional Readiness Markers
- [ ] Understanding of when and why to use different PostGIS functions
- [ ] Ability to interpret and validate spatial analysis results
- [ ] Progression from template completion to original analysis design
- [ ] Confidence with both basic and advanced PostGIS operations
- [ ] Readiness for complex professional spatial analysis projects

### Learning Journey Assessment
- **Queries 1-4**: Demonstrate understanding of fundamental spatial concepts
- **Queries 5-7**: Show ability to adapt concepts to new problems
- **Queries 8-10**: Exhibit independent spatial analysis capability

## 📚 Learning Resources

### Essential References
- [PostGIS Documentation](https://postgis.net/documentation/) - Comprehensive function reference
- [PostGIS Tutorial](https://postgis.net/workshops/postgis-intro/) - Hands-on learning
- [Spatial Analysis Concepts](https://www.spatialanalysisonline.com/) - Theoretical background
- [QGIS Training Manual](https://docs.qgis.org/latest/en/docs/training_manual/) - Desktop GIS integration

### Practice Recommendations
1. **Start with examples** - Understand each provided example completely before adapting
2. **Test frequently** - Run queries often during development to catch errors early
3. **Visualize results** - Use QGIS to map your query results when possible
4. **Progress gradually** - Master each query level before moving to the next
5. **Seek help appropriately** - Early queries should focus on concept understanding, later queries on problem-solving approach

### Support Strategy
- **Queries 1-4**: Focus on understanding the PostGIS functions and spatial concepts
- **Queries 5-7**: Emphasize spatial thinking and logical problem decomposition
- **Queries 8-10**: Develop independent analysis skills and creative problem-solving

---

**🎓 Ready to master advanced PostGIS spatial analysis? This progressive journey will build your expertise from basic concepts to professional-level spatial analysis capabilities!**