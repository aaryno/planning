# PostGIS Spatial Analysis - Advanced Database Operations

**GIST 604B - Module 6: PostGIS Spatial Databases**  
**Assignment Type:** Application Level (⭐⭐⭐)  
**Points:** 20 (4 queries × 5 points each)  
**Estimated Time:** 4-5 hours  
**Prerequisites:** SQL Introduction Assignment, PostGIS Basics Assignment

## 📖 Overview

Welcome to your advanced PostGIS spatial analysis assignment! This application-level exercise challenges you to perform sophisticated spatial operations that form the backbone of professional GIS workflows. You'll tackle real-world spatial analysis problems using complex queries that combine multiple PostGIS functions, spatial relationships, and decision-support methodologies.

### 🎯 Learning Objectives

By completing this assignment, you will:

- **Master multi-layer spatial analysis** using complex intersection operations
- **Implement advanced buffer analysis** with distance-based accessibility modeling
- **Develop network routing concepts** for transportation optimization
- **Apply multi-criteria decision analysis** for spatial planning and site selection
- **Integrate multiple spatial datasets** in comprehensive analytical workflows
- **Optimize spatial queries** for performance with large datasets
- **Build professional-grade spatial analysis solutions** for real-world problems

### 🏢 Professional Context

**Why These Skills Matter for Your GIS Career:**

Advanced spatial analysis capabilities are what distinguish GIS professionals from basic users. These skills are essential for:

- **Urban Planners** analyzing optimal locations for new facilities and infrastructure
- **Environmental Consultants** conducting impact assessments and conservation planning
- **Emergency Management** professionals optimizing response strategies and resource allocation
- **Transportation Engineers** designing efficient routing and accessibility solutions
- **Business Intelligence** analysts performing location-based market analysis
- **Research Scientists** conducting complex spatial modeling and decision support

**Real-World Applications:**
- Site selection for new hospitals based on population coverage and accessibility
- Environmental impact analysis for proposed development projects
- Emergency response optimization with multi-criteria facility placement
- Transportation network analysis for public transit planning
- Conservation priority mapping using ecological and economic factors
- Retail location analysis combining demographics, competition, and accessibility

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

**Key Columns:**
- `geometry`: Protected area boundaries (MULTIPOLYGON, EPSG:4326)
- `area_acres`: Precise area calculations
- `visitor_count_annual`: Annual visitation data
- `protection_level`: Conservation status

#### `watersheds` Table (4 records - MULTIPOLYGON)
Major river basin boundaries including:
- Upper Colorado River Basin (17,800 sq mi, avg elevation 7,200 ft)
- South Platte River Basin (24,300 sq mi, flows northeast)
- Arkansas River Basin (25,000 sq mi, highest elevation basin)
- Rio Grande Basin (8,000 sq mi, flows south)

**Key Columns:**
- `geometry`: Watershed boundaries (MULTIPOLYGON, EPSG:4326)
- `drainage_area_sqmi`: Basin area in square miles
- `primary_river`: Main river system
- `flow_direction`: Regional drainage pattern

#### `transportation_network` Table (8 records - MULTILINESTRING)
Roads, trails, and waterways including:
- Interstate 70 (424 miles, major east-west corridor)
- Trail Ridge Road (48 miles, seasonal alpine highway)
- Continental Divide Trail (760 miles, long-distance hiking)
- Colorado Trail (486 miles, multi-use recreation)
- Major rivers and scenic routes

**Key Columns:**
- `geometry`: Route alignments (MULTILINESTRING, EPSG:4326)
- `route_type`: Highway, trail, river classification
- `length_miles`: Accurate distance measurements
- `seasonal_closure`: Winter accessibility restrictions

#### `facilities` Table (12 records - POINT)
Visitor services and operational facilities including:
- Visitor centers with exhibits and education programs
- Campgrounds with varying capacity (88-244 sites)
- Ranger stations for emergency services
- Research stations and mountain huts

**Key Columns:**
- `geometry`: Facility locations (POINT, EPSG:4326)
- `facility_type`: Service classification
- `capacity`: Visitor or operational capacity
- `elevation_ft`: Altitude for accessibility planning

#### `monitoring_stations` Table (10 records - POINT)
Environmental and safety monitoring network including:
- Weather stations (alpine and valley locations)
- Air quality monitors (PM2.5, ozone, visibility)
- Water quality sensors (temperature, pH, dissolved oxygen)
- Seismic monitoring and stream gauges

**Key Columns:**
- `geometry`: Station locations (POINT, EPSG:4326)
- `monitoring_type`: Data collection focus
- `parameters_monitored`: Specific measurements
- `operating_agency`: Responsible organization

#### `land_use_zones` Table (5 records - MULTIPOLYGON)
Management and ecological zones including:
- Alpine Tundra Zone (125,000 acres, minimal management)
- Subalpine Forest Zone (320,000 acres, multiple use)
- Critical Wildlife Habitat (180,000 acres, seasonal restrictions)
- Recreation Management Areas (varying intensity levels)

**Key Columns:**
- `geometry`: Zone boundaries (MULTIPOLYGON, EPSG:4326)
- `management_intensity`: Conservation vs. use balance
- `recreational_use`: Permitted activities
- `elevation_range_ft`: Altitudinal characteristics

### Coordinate Systems Used
- **WGS84 (EPSG:4326)**: Geographic coordinates for global compatibility
- **Web Mercator (EPSG:3857)**: Projected coordinates for accurate area/distance calculations
- **UTM Zone 13N (EPSG:26913)**: Regional projection for precision measurements

## 📝 Assignment Tasks (4 Queries × 5 Points = 20 Points)

Complete the following 4 advanced spatial analysis queries. Each query demonstrates sophisticated PostGIS operations essential for professional GIS work.

### Query 1: Multi-Layer Spatial Intersection Analysis (5 points)
**File**: [`sql/01_multi_layer_intersection.sql`](sql/01_multi_layer_intersection.sql)

**Objective**: Perform complex spatial intersections between protected areas and watersheds to analyze conservation coverage and identify protection gaps.

**Professional Context**: Environmental planners need to understand how protected areas are distributed across different watersheds to assess conservation coverage, identify gaps in protection, and prioritize areas for additional conservation measures.

**Learning Example**: Here's how you might find simple overlaps between two spatial layers:
```sql
-- Example: Find parks that intersect with a specific watershed
SELECT pa.name, ws.name
FROM protected_areas pa, watersheds ws
WHERE ST_Intersects(pa.geometry, ws.geometry)
  AND ws.name = 'Upper Colorado River Basin';
```

**Your Task**: Create a comprehensive intersection analysis that calculates:
- **Overlap geometries** between protected areas and watersheds
- **Precise area calculations** for overlapping regions (in acres)
- **Percentage coverage** of protected areas within each watershed
- **Percentage of watersheds** that contain protected areas
- **Filtering** to show only significant overlaps (>1000 acres)
- **Ranking** by overlap area (largest coverage first)

**Keywords to Use**: `ST_Intersects`, `ST_Intersection`, `ST_Area`, `ST_Transform`, `INNER JOIN`, `HAVING`, `ORDER BY`, `ROUND`

**Expected Results**: Your query should identify which protected areas span multiple watersheds, how much of each protected area falls within different river basins, and help prioritize watershed-based conservation planning.

---

### Query 2: Advanced Buffer Analysis - Facility Accessibility (5 points)
**File**: [`sql/02_advanced_buffer_analysis.sql`](sql/02_advanced_buffer_analysis.sql)

**Objective**: Perform advanced buffer analysis to determine facility accessibility from transportation networks and identify underserved areas requiring additional infrastructure.

**Professional Context**: Park managers need to assess visitor facility accessibility and identify areas where additional facilities may be needed. This analysis helps improve visitor services while ensuring emergency response capabilities.

**Learning Example**: Here's how you might create a basic buffer around facilities:
```sql
-- Example: Create 1-mile buffer around visitor centers
SELECT f.name,
       ST_Buffer(ST_Transform(f.geometry, 3857), 1609.34) as one_mile_buffer
FROM facilities f
WHERE f.facility_type = 'Visitor Center';
```

**Your Task**: Develop a comprehensive accessibility analysis that includes:
- **Multiple buffer distances** (1-mile and 5-mile service areas)
- **Transportation route counting** within buffer zones
- **Distance calculations** to nearest major transportation routes
- **Service area coverage** in square miles
- **Accessibility ratings** based on transportation proximity
- **Facility density analysis** showing isolation or clustering
- **Filtering** for facilities with limited access (>2 miles from major routes)

**Keywords to Use**: `ST_Buffer`, `ST_DWithin`, `ST_Intersects`, `ST_Distance`, `ST_Transform`, `ST_Union`, `WITH`, `CASE`, `COUNT`

**Expected Results**: Your analysis should identify facilities with limited transportation access, quantify service area coverage, and help prioritize areas for infrastructure improvement.

---

### Query 3: Network Routing Analysis - Transportation Optimization (5 points)
**File**: [`sql/03_network_routing_analysis.sql`](sql/03_network_routing_analysis.sql)

**Objective**: Analyze transportation network connectivity and routing efficiency between facilities to optimize emergency services, maintenance operations, and visitor transportation.

**Professional Context**: Emergency responders and park operations need efficient transportation routes between facilities. This analysis identifies optimal routing strategies considering distance, elevation, and network constraints.

**Learning Example**: Here's how you might calculate straight-line distances between facilities:
```sql
-- Example: Find distance between two specific facilities
SELECT f1.name as origin, f2.name as destination,
       ST_Distance(
         ST_Transform(f1.geometry, 3857),
         ST_Transform(f2.geometry, 3857)
       ) / 1609.34 as miles
FROM facilities f1, facilities f2
WHERE f1.name = 'Rocky Mountain National Park Visitor Center'
  AND f2.name = 'Bear Lake Ranger Station';
```

**Your Task**: Build a comprehensive routing analysis that evaluates:
- **Facility-to-facility routing** for all key combinations
- **Straight-line vs. network distance** comparisons
- **Routing efficiency ratios** (network/straight-line distance)
- **Elevation change calculations** between facilities
- **Route difficulty classifications** based on distance, elevation, and access
- **Infrastructure improvement priorities** for inefficient routes
- **Travel time estimates** considering elevation and route constraints

**Keywords to Use**: `ST_Distance`, `ST_ShortestLine`, `ST_ClosestPoint`, `ST_Intersects`, `CROSS JOIN`, `ABS`, `CASE`, `STRING_AGG`

**Expected Results**: Your analysis should identify the most and least efficient routes between facilities, prioritize infrastructure improvements, and provide travel time estimates for operational planning.

---

### Query 4: Multi-Criteria Spatial Decision Support Analysis (5 points)
**File**: [`sql/04_multi_criteria_decision_analysis.sql`](sql/04_multi_criteria_decision_analysis.sql)

**Objective**: Implement comprehensive multi-criteria decision analysis (MCDA) to identify optimal locations for a new emergency response facility using weighted spatial factors and composite scoring.

**Professional Context**: Park authorities need to establish a new emergency response facility to improve visitor safety and environmental monitoring response times. The location must optimize multiple competing factors including accessibility, coverage, operational efficiency, and cost considerations.

**Learning Example**: Here's how you might score a location based on a single criterion:
```sql
-- Example: Score locations based on distance to transportation
SELECT candidate_location,
       CASE 
         WHEN min_transport_distance < 2 THEN 100
         WHEN min_transport_distance < 5 THEN 75
         WHEN min_transport_distance < 10 THEN 50
         ELSE 25
       END as transport_accessibility_score
FROM candidate_analysis;
```

**Your Task**: Develop a sophisticated decision support system that includes:
- **Candidate location grid** across the study area
- **Transportation accessibility scoring** (25% weight)
- **Facility coverage gap analysis** (30% weight)
- **Monitoring station response coverage** (20% weight)
- **Protected area service potential** (15% weight)
- **Terrain suitability assessment** (10% weight)
- **Weighted composite scoring** combining all criteria
- **Site suitability rankings** with implementation recommendations

**Keywords to Use**: `ST_MakePoint`, `generate_series`, `ST_DWithin`, `ST_Intersection`, `ST_Buffer`, `CASE`, `AVG`, `COUNT`, `SUM`, `ORDER BY`, `LIMIT`

**Expected Results**: Your analysis should return the top 5 candidate locations for a new emergency response facility, showing weighted composite scores, individual criterion performance, and specific implementation recommendations.

## 🧪 Testing Your Solutions

### Test Individual SQL Files
```bash
# Test a specific query
python test_assignment.py::TestPostGISSpatialAnalysis::test_01_multi_layer_intersection -v

# Test all queries
python test_assignment.py -v
```

### Interactive Testing
```bash
# Connect to database and test queries manually
docker exec -it postgis-spatial-analysis-postgres psql -U postgres -d spatial_analysis

# Run your SQL file
\i sql/01_multi_layer_intersection.sql
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
Your submission must include all 4 completed SQL files:
- `sql/01_multi_layer_intersection.sql` - Multi-layer intersection analysis
- `sql/02_advanced_buffer_analysis.sql` - Advanced buffer and accessibility analysis
- `sql/03_network_routing_analysis.sql` - Network routing and transportation optimization
- `sql/04_multi_criteria_decision_analysis.sql` - Multi-criteria decision support analysis

### Grading Criteria (5 points each = 20 total)

Each query is evaluated on:
- **Query Execution (2 points)**: SQL runs without errors and returns valid results
- **Spatial Analysis Accuracy (2 points)**: Correct use of PostGIS functions and spatial operations
- **Results Quality (1 point)**: Appropriate filtering, ordering, and result formatting

**Grade Scale:**
- **18-20 points (90-100%)**: Advanced spatial analysis proficiency - ready for professional GIS work
- **16-17 points (80-89%)**: Good spatial analysis skills - minor refinements needed
- **14-15 points (70-79%)**: Adequate spatial analysis foundation - review complex operations
- **Below 14 points (<70%)**: Needs significant improvement in spatial analysis concepts

### Submission Process
1. Complete all 4 SQL query files
2. Test your queries using the automated test suite
3. Verify results using the grading script
4. Submit via your course management system or version control

## 🔧 PostGIS Quick Reference

### Essential Spatial Functions
```sql
-- Spatial Relationships
ST_Intersects(geom1, geom2)      -- Test if geometries intersect
ST_Contains(geom1, geom2)        -- Test if geom1 contains geom2
ST_DWithin(geom1, geom2, distance) -- Test if within distance

-- Spatial Operations
ST_Intersection(geom1, geom2)    -- Return intersection geometry
ST_Buffer(geometry, radius)      -- Create buffer around geometry
ST_Union(geometry_set)           -- Combine multiple geometries

-- Measurements
ST_Area(geometry)                -- Calculate area
ST_Length(geometry)              -- Calculate length
ST_Distance(geom1, geom2)        -- Calculate distance
ST_Perimeter(geometry)           -- Calculate perimeter

-- Coordinate Transformations
ST_Transform(geometry, srid)     -- Transform coordinate system
ST_SetSRID(geometry, srid)       -- Set spatial reference

-- Geometry Construction
ST_MakePoint(x, y)               -- Create point geometry
ST_ShortestLine(geom1, geom2)    -- Shortest line between geometries
ST_ClosestPoint(geom1, geom2)    -- Closest point on geometry

-- Spatial Indexing (automatic with GIST indexes)
CREATE INDEX idx_table_geom ON table USING GIST (geometry);
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

**"ERROR: GEOS operation xxx"**
- **Solution**: Try `ST_MakeValid(geometry)` to fix geometry issues
- Check for self-intersecting or degenerate geometries

### Performance Optimization

**Slow spatial queries**
```sql
-- Check spatial indexes exist
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE indexname LIKE '%geom%' OR indexname LIKE '%gist%';

-- Verify index usage
EXPLAIN ANALYZE SELECT ... WHERE ST_Intersects(geom1, geom2);
```

**Memory issues with large calculations**
```sql
-- Use simpler geometries when possible
ST_Simplify(geometry, tolerance)

-- Transform only when necessary
-- Bad: ST_Area(ST_Transform(geometry, 3857)) in WHERE clause
-- Good: Transform once in subquery or WITH clause
```

### Database Connection Issues

**Connection refused**
```bash
# Check if container is running
docker-compose ps

# Restart if necessary
docker-compose down && docker-compose up -d

# Check logs
docker-compose logs postgres
```

## 🎯 Success Criteria

### Technical Proficiency Indicators
- [ ] All 4 spatial analysis queries execute without errors
- [ ] Proper use of coordinate transformations for accurate measurements
- [ ] Efficient spatial joins using appropriate indexes
- [ ] Complex spatial operations combining multiple PostGIS functions
- [ ] Meaningful filtering and ordering of spatial results

### Professional Readiness Markers
- [ ] Understanding of multi-criteria spatial decision processes
- [ ] Ability to optimize spatial queries for performance
- [ ] Knowledge of real-world applications for each analysis type
- [ ] Skill in interpreting and validating spatial analysis results
- [ ] Confidence with advanced PostGIS functions and workflows

### Preparation for Advanced GIS Work
Upon successful completion, you will be prepared for:
- **Enterprise spatial database development** with large, complex datasets
- **Advanced GIS analysis projects** requiring custom spatial algorithms
- **Spatial decision support systems** for planning and management
- **Performance optimization** of spatial queries and workflows
- **Integration** of PostGIS with web mapping and desktop GIS applications

### Key Insight
*"Advanced spatial analysis is not just about knowing the right PostGIS functions—it's about understanding how to combine them intelligently to solve complex real-world problems while considering performance, accuracy, and decision-making requirements."*

## 📚 Learning Resources

### Essential References
- [PostGIS Documentation](https://postgis.net/documentation/) - Comprehensive function reference
- [PostGIS Cookbook](https://postgis.net/workshops/) - Practical examples and workflows
- [Spatial Analysis Methods](https://www.spatialanalysisonline.com/) - Theoretical background
- [QGIS Training Manual](https://docs.qgis.org/latest/en/docs/training_manual/) - Desktop GIS integration

### Practice Recommendations
1. **Experiment** with different buffer sizes and see how they affect accessibility analysis
2. **Visualize** your query results in QGIS to verify spatial logic
3. **Optimize** queries by testing different approaches and comparing performance
4. **Research** real-world applications of each analysis type in your field of interest
5. **Practice** explaining your analysis methods and results to non-technical audiences

---

**🎓 Ready to tackle professional-level spatial analysis? Your expertise in advanced PostGIS operations will set you apart in the GIS profession!**