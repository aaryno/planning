# PostGIS Basics - Spatial Database Fundamentals

**GIST 604B - Module 6: PostGIS Spatial Databases**  
**Assignment Type:** Foundation Level (⭐⭐)  
**Points:** 20 (8 queries × 2.5 points each)  
**Estimated Time:** 2-3 hours  
**Prerequisites:** SQL Introduction Assignment

## 📖 Overview

Welcome to your first PostGIS assignment! This foundational exercise introduces you to spatial database concepts using PostGIS, the spatial extension for PostgreSQL. You'll learn to work with geographic data, perform spatial analysis, and master the essential PostGIS functions that power modern GIS applications.

### 🎯 Learning Objectives

By completing this assignment, you will:

- **Inspect spatial data** using PostGIS metadata functions
- **Create geometries** using various PostGIS constructors
- **Calculate measurements** with accurate spatial analysis functions
- **Transform coordinates** between different reference systems
- **Query spatial relationships** between geographic features
- **Perform buffer analysis** for proximity studies
- **Execute spatial joins** combining multiple spatial datasets
- **Build complex workflows** using advanced PostGIS operations

### 🏢 Professional Context

**Why These Skills Matter for Your GIS Career:**

PostGIS is the industry-standard spatial database used by:
- **Government agencies** for urban planning and environmental monitoring
- **Tech companies** for location-based services (Uber, Google Maps, Zillow)
- **Consulting firms** for spatial analysis and decision support
- **Research institutions** for geographic data science
- **Utilities** for infrastructure management and asset tracking

**Real-World Applications:**
- Finding optimal locations for new retail stores based on demographics
- Analyzing environmental impact zones around industrial facilities  
- Routing emergency services to minimize response times
- Calculating flood risk areas for insurance and planning
- Managing utility networks with spatial topology

## 🚀 Getting Started

### Prerequisites
- Completed SQL Introduction assignment (understanding of basic SQL)
- Docker installed and running
- VS Code with PostgreSQL extension (recommended)
- Basic understanding of coordinate systems and GIS concepts

### Environment Setup

**Step 1: Clone and Navigate**
```bash
cd postgis-basics
```

**Step 2: Start PostGIS Database**
```bash
# Start the PostGIS container
docker-compose up -d

# Wait for database initialization (about 30 seconds)
docker-compose logs postgres
```

**Step 3: Verify Connection**
```bash
# Test database connectivity
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -c "SELECT postgis_version();"
```

**Expected Output:**
```
                    postgis_version
----------------------------------------------------
 3.3 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
```

**Step 4: Explore the Data**
```bash
# List all spatial tables
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -c "\dt"

# Check data in cities table
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -c "SELECT name, ST_AsText(geom) FROM cities LIMIT 3;"
```

## 📊 Dataset Overview

Your PostGIS database contains five interconnected spatial tables representing various geographic features across the United States:

### `cities` Table (12 records)
Point geometries representing major US cities with population data.

**Sample data:**
```sql
SELECT name, state_code, population, ST_AsText(geom) AS location 
FROM cities 
WHERE state_code = 'CA' 
LIMIT 2;
```

**Expected result:**
```
      name      | state_code | population |          location
----------------+------------+------------+---------------------------
 San Francisco  | CA         |  873965    | POINT(-122.4194 37.7749)
 Los Angeles    | CA         |  3971883   | POINT(-118.2437 34.0522)
```

### `national_parks` Table (6 records)
Polygon geometries representing major national parks with establishment dates and areas.

**Sample data:**
```sql
SELECT name, state_code, area_sq_km, established_year 
FROM national_parks 
WHERE state_code = 'CA' 
LIMIT 1;
```

**Expected result:**
```
   name   | state_code | area_sq_km | established_year
----------+------------+------------+------------------
 Yosemite | CA         |  3027.07   |      1890
```

### `highways` Table (5 records)
LineString geometries representing major highway segments with length information.

**Sample data:**
```sql
SELECT name, highway_type, length_km 
FROM highways 
WHERE highway_type = 'Interstate' 
LIMIT 2;
```

### `weather_stations` Table (8 records)
Point geometries for weather monitoring stations with dual coordinate systems (WGS84 and UTM).

**Sample data:**
```sql
SELECT name, state_code, elevation_m, station_type 
FROM weather_stations 
WHERE state_code = 'WA' 
LIMIT 2;
```

### `states` Table (6 records)
Simplified polygon geometries representing US state boundaries.

**Sample data:**
```sql
SELECT state_name, state_code, area_sq_km 
FROM states 
WHERE state_code IN ('WA', 'CA') 
ORDER BY area_sq_km DESC;
```

## 📝 Assignment Tasks (8 Queries × 2.5 Points = 20 Points)

Complete all SQL files in the `sql/` directory by filling in the template placeholders (`_____`). Each query builds upon previous concepts while introducing new PostGIS functionality.

### Query 1: Spatial Data Inspection (2.5 points)

**File:** `sql/01_spatial_inspection.sql`

**Objective:** Learn to inspect spatial data properties using PostGIS metadata functions.

**Learning Example - Weather Station Inspection:**
```sql
-- Example: Inspect weather station geometries (different from your task)
SELECT 
    name,
    station_type,
    ST_GeometryType(geom) AS geometry_type,
    ST_SRID(geom) AS coordinate_system,
    ST_AsText(geom) AS coordinates_text
FROM weather_stations 
WHERE state_code = 'OR'
LIMIT 2;
```

**Expected Learning Example Result:**
```
      name      | station_type | geometry_type | coordinate_system |        coordinates_text
----------------+--------------+---------------+-------------------+---------------------------
 Portland Intl  | Airport      | ST_Point      |      4326         | POINT(-122.5951 45.5898)
 Crater Lake    | Lake         | ST_Point      |      4326         | POINT(-122.1685 42.8684)
```

**Your Task:** Adapt this concept to examine **cities table** geometry properties, showing the first **5 cities** with their spatial metadata.

**Key Functions to Use:**
- `ST_GeometryType()` - Returns the geometry type (ST_Point, ST_Polygon, etc.)
- `ST_SRID()` - Returns the Spatial Reference System Identifier
- `ST_AsText()` - Converts geometry to human-readable WKT format

---

### Query 2: Geometry Creation Functions (2.5 points)

**File:** `sql/02_geometry_creation.sql`

**Learning Example - Portland Location Creation:**
```sql
-- Example: Create different geometries for Portland, OR (different from your task)
SELECT 
    'Portland Point' AS geometry_name,
    ST_GeometryType(ST_SetSRID(ST_MakePoint(-122.6784, 45.5152), 4326)) AS geom_type,
    ST_AsText(ST_SetSRID(ST_MakePoint(-122.6784, 45.5152), 4326)) AS geometry_wkt

UNION ALL

SELECT 
    'Portland Square' AS geometry_name,
    ST_GeometryType(ST_GeomFromText('POLYGON((-122.78 45.41, -122.58 45.41, -122.58 45.61, -122.78 45.61, -122.78 45.41))', 4326)) AS geom_type,
    ST_AsText(ST_GeomFromText('POLYGON((-122.78 45.41, -122.58 45.41, -122.58 45.61, -122.78 45.61, -122.78 45.41))', 4326)) AS geometry_wkt

UNION ALL

SELECT 
    'Portland Buffer' AS geometry_name,
    ST_GeometryType(ST_Buffer(ST_SetSRID(ST_MakePoint(-122.6784, 45.5152), 4326), 0.05)) AS geom_type,
    ST_AsText(ST_Buffer(ST_SetSRID(ST_MakePoint(-122.6784, 45.5152), 4326), 0.05)) AS geometry_wkt;
```

**Your Task:** Create three geometries for **Denver, Colorado** using the coordinates (-104.9903, 39.7392).

**Key Functions to Master:**
- `ST_MakePoint(longitude, latitude)` - Creates point from coordinates
- `ST_GeomFromText('WKT', SRID)` - Creates geometry from Well-Known Text
- `ST_SetSRID(geometry, srid)` - Assigns spatial reference system
- `ST_Buffer(geometry, distance)` - Creates buffer zone around geometry

---

### Query 3: Spatial Measurements (2.5 points)

**File:** `sql/03_spatial_measurements.sql`

**Learning Example - Weather Station Analysis:**
```sql
-- Example: Calculate measurements for weather stations (different from your task)
SELECT 
    'Seattle to Portland Distance' AS measurement_type,
    ROUND(
        ST_Distance_Sphere(
            (SELECT geom FROM weather_stations WHERE name = 'Seattle WSFO'),
            (SELECT geom FROM weather_stations WHERE name = 'Portland Intl')
        ) / 1000, 2
    ) AS distance_km

UNION ALL

SELECT 
    'Olympic Park Area' AS measurement_type,
    ROUND(
        ST_Area(
            ST_Transform(
                (SELECT geom FROM national_parks WHERE name = 'Olympic'),
                32610  -- UTM Zone 10N for Washington
            )
        ) / 1000000, 2  -- Convert sq meters to sq kilometers
    ) AS area_sq_km;
```

**Your Task:** Calculate three different measurements:
1. Distance between **Seattle and Portland cities**
2. Area of **Yellowstone National Park**
3. Length of the **I-5 highway section**

**Key Functions for Accurate Measurements:**
- `ST_Distance_Sphere()` - Accurate geographic distance on sphere
- `ST_Area()` - Calculate area (use with ST_Transform for accuracy)
- `ST_Length()` - Calculate length of linear features
- `ST_Transform()` - Project to appropriate UTM zone for meter-based calculations

---

### Query 4: Coordinate System Transformations (2.5 points)

**File:** `sql/04_coordinate_transformation.sql`

**Learning Example - Park Coordinate Transformation:**
```sql
-- Example: Transform Yosemite park centroid coordinates (different from your task)
SELECT 
    'Yosemite Centroid' AS feature_name,
    
    -- Original WGS84 coordinates
    ROUND(ST_X(ST_Centroid((SELECT geom FROM national_parks WHERE name = 'Yosemite'))), 6) AS wgs84_longitude,
    ROUND(ST_Y(ST_Centroid((SELECT geom FROM national_parks WHERE name = 'Yosemite'))), 6) AS wgs84_latitude,
    
    -- Transformed to UTM Zone 11N coordinates (California)
    ROUND(ST_X(ST_Transform(ST_Centroid((SELECT geom FROM national_parks WHERE name = 'Yosemite')), 32611))) AS utm_easting_m,
    ROUND(ST_Y(ST_Transform(ST_Centroid((SELECT geom FROM national_parks WHERE name = 'Yosemite')), 32611))) AS utm_northing_m;
```

**Your Task:** Transform **Seattle WSFO weather station** coordinates between WGS84 and UTM Zone 10N, including verification by transforming back.

**Key Coordinate Systems:**
- **EPSG:4326** - WGS84 (longitude/latitude in degrees)
- **EPSG:32610** - UTM Zone 10N (meters, good for US West Coast)
- **EPSG:32613** - UTM Zone 13N (meters, good for Colorado/Wyoming)

**Essential Functions:**
- `ST_Transform(geometry, target_epsg)` - Convert between coordinate systems
- `ST_X()` and `ST_Y()` - Extract coordinate components
- Double transformation for accuracy verification

---

### Query 5: Spatial Relationships (2.5 points)

**File:** `sql/05_spatial_relationships.sql`

**Learning Example - Park and Station Relationships:**
```sql
-- Example: Find weather stations that are within national parks (different from your task)
SELECT 
    'Stations in Parks' AS query_type,
    ws.name AS station_name,
    p.name AS park_name,
    ROUND(ST_Distance_Sphere(ws.geom, ST_Centroid(p.geom)) / 1000, 2) AS distance_km
FROM weather_stations ws
JOIN national_parks p ON ST_Within(ws.geom, p.geom)

UNION ALL

-- Find highways that cross state boundaries  
SELECT 
    'Highway-State Intersections' AS query_type,
    h.name AS highway_name,
    s.state_name AS intersected_state,
    NULL AS distance_km
FROM highways h
JOIN states s ON ST_Intersects(h.geom, s.geom)
ORDER BY query_type, station_name, highway_name;
```

**Your Task:** Execute three spatial relationship queries:
1. Find **cities within Washington state**
2. Find **highways that intersect with national parks**
3. Find **weather stations within 100km of Seattle**

**Essential Spatial Relationship Functions:**
- `ST_Within(geom1, geom2)` - Tests if geom1 is completely inside geom2
- `ST_Intersects(geom1, geom2)` - Tests if geometries share any space
- `ST_DWithin(geom1, geom2, distance)` - Tests proximity within distance

---

### Query 6: Buffer Operations (2.5 points)

**File:** `sql/06_buffer_operations.sql`

**Learning Example - Seattle Analysis Zones:**
```sql
-- Example: Create analysis buffer around Seattle and find features (different from your task)
WITH seattle_buffer AS (
    SELECT ST_Buffer(
        ST_Transform(geom, 32610),  -- Transform to UTM for accurate distance
        75000  -- 75km = 75000 meters
    ) AS buffer_geom
    FROM cities 
    WHERE name = 'Seattle'
)
SELECT 
    'Seattle 75km Analysis Zone' AS analysis_type,
    ws.name AS station_name,
    ROUND(
        ST_Distance(
            ST_Transform((SELECT geom FROM cities WHERE name = 'Seattle'), 32610),
            ST_Transform(ws.geom, 32610)
        ) / 1000, 2
    ) AS distance_from_seattle_km
FROM weather_stations ws, seattle_buffer sb
WHERE ST_Within(
    ST_Transform(ws.geom, 32610), 
    sb.buffer_geom
)
ORDER BY distance_from_seattle_km;
```

**Your Task:** Create and analyze three buffer operations:
1. Create **50km buffer around Denver city**
2. Create **10km corridor buffer along I-5 highway**
3. Find **weather stations within Denver's buffer zone**

**Buffer Analysis Concepts:**
- **Point buffers** create circular zones for proximity analysis
- **Line buffers** create corridors for infrastructure impact studies  
- **Accurate buffering** requires UTM projection for meter-based distances
- **Common Time Zones:** Zone 10N (West Coast), Zone 13N (Colorado), Zone 14N (Texas)

---

### Query 7: Spatial Joins (2.5 points)

**File:** `sql/07_spatial_joins.sql`

**Learning Example - Park Visitor Analysis:**
```sql
-- Example: Complex spatial joins for park accessibility analysis (different from your task)
SELECT 
    'Park Accessibility Analysis' AS join_type,
    p.name AS park_name,
    COUNT(c.city_id) AS nearby_cities_count,
    ROUND(AVG(
        ST_Distance_Sphere(c.geom, ST_Centroid(p.geom)) / 1000
    ), 2) AS avg_distance_km,
    SUM(c.population) AS total_population_within_200km
FROM national_parks p
LEFT JOIN cities c ON ST_DWithin(
    ST_Transform(c.geom, 32610),
    ST_Transform(ST_Centroid(p.geom), 32610),
    200000  -- 200km = 200000 meters
)
GROUP BY p.name, p.park_id
HAVING COUNT(c.city_id) > 0
ORDER BY total_population_within_200km DESC;
```

**Your Task:** Execute three types of spatial joins:
1. **Cities to states** with population aggregation
2. **Weather stations to nearest cities** within 200km
3. **Highways to states** with length calculations per state

**Advanced Spatial Join Patterns:**
- `LEFT JOIN` with spatial conditions for aggregation analysis
- `DISTINCT ON` for nearest neighbor queries
- `ST_Intersection()` with `ST_Length()` for partial feature measurements
- Window functions for ranking spatial relationships

---

### Query 8: Complex Spatial Analysis (2.5 points)

**File:** `sql/08_complex_analysis.sql`

**Learning Example - Regional Infrastructure Analysis:**
```sql
-- Example: Multi-step infrastructure analysis (different from your task)
WITH regional_analysis AS (
    -- Step 1: Find cities near highways
    SELECT 
        c.name AS city_name,
        c.population,
        h.name AS nearest_highway,
        MIN(ST_Distance_Sphere(c.geom, h.geom)) AS highway_distance_m
    FROM cities c
    CROSS JOIN highways h
    GROUP BY c.city_id, c.name, c.population, h.name
    HAVING MIN(ST_Distance_Sphere(c.geom, h.geom)) < 50000  -- Within 50km
),
infrastructure_summary AS (
    -- Step 2: Summarize by highway
    SELECT 
        nearest_highway,
        COUNT(*) AS cities_served,
        SUM(population) AS total_population,
        AVG(highway_distance_m / 1000) AS avg_distance_km
    FROM regional_analysis
    GROUP BY nearest_highway
)
SELECT 
    is.nearest_highway AS highway_system,
    is.cities_served,
    is.total_population,
    ROUND(is.avg_distance_km, 2) AS avg_city_distance_km,
    -- Calculate service efficiency score
    ROUND((is.total_population::DECIMAL / is.avg_distance_km), 0) AS efficiency_score
FROM infrastructure_summary is
ORDER BY efficiency_score DESC;
```

**Your Task:** Build a comprehensive **tourism analysis workflow**:
1. Find **city-park pairs within 100km**
2. Identify **closest weather station** for each pair
3. Calculate **highway corridor connectivity**
4. Generate **summary statistics** for the entire analysis region

**Advanced PostGIS Workflow Concepts:**
- **WITH clauses (CTEs)** for organizing multi-step analysis
- **Window functions** for ranking and partitioning spatial data
- **ST_Union()** for combining multiple geometries
- **Complex aggregations** across spatial datasets
- **Performance optimization** with proper indexing and projections

## 🧪 Testing Your Solutions

### Test Individual SQL Files

Test a single query during development:

```bash
# Test spatial inspection query
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -f sql/01_spatial_inspection.sql

# Test geometry creation query  
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -f sql/02_geometry_creation.sql
```

### Test All Queries at Once

Run the complete test suite:

```bash
# Run all tests with detailed output
python test_assignment.py -v

# Run tests with shorter output
python test_assignment.py --tb=short
```

### Interactive Testing

Test your queries interactively in the PostGIS database:

```bash
# Connect to database for interactive testing
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals

# Example interactive commands:
gis_fundamentals=# SELECT postgis_version();
gis_fundamentals=# \dt
gis_fundamentals=# SELECT name, ST_AsText(geom) FROM cities LIMIT 2;
gis_fundamentals=# \q
```

### Automated Testing and Grading

The automated grading system tests your solutions for:

- **Template completion** (no blanks remaining)
- **SQL syntax correctness** (proper PostGIS function usage)
- **Expected results** (correct data and structure)
- **Spatial accuracy** (appropriate coordinate systems and measurements)
- **Performance** (efficient queries with proper spatial indexing)

```bash
# Generate grade report
python grading/calculate_grade.py --verbose
```

## 📋 Submission Requirements

### Files to Submit

Your completed assignment must include all SQL files with template blanks filled in:

```
sql/
├── 01_spatial_inspection.sql      ✓ Complete
├── 02_geometry_creation.sql       ✓ Complete  
├── 03_spatial_measurements.sql    ✓ Complete
├── 04_coordinate_transformation.sql ✓ Complete
├── 05_spatial_relationships.sql   ✓ Complete
├── 06_buffer_operations.sql       ✓ Complete
├── 07_spatial_joins.sql          ✓ Complete
└── 08_complex_analysis.sql       ✓ Complete
```

### Grading Breakdown (20 points total)

| Query | Description | Points | Key Skills |
|-------|-------------|---------|------------|
| 1 | Spatial Inspection | 2.5 | PostGIS metadata functions |
| 2 | Geometry Creation | 2.5 | Constructing spatial objects |
| 3 | Spatial Measurements | 2.5 | Distance, area, length calculations |
| 4 | Coordinate Transformation | 2.5 | CRS conversion and projection |
| 5 | Spatial Relationships | 2.5 | Topology and proximity queries |
| 6 | Buffer Operations | 2.5 | Zone analysis and spatial buffering |
| 7 | Spatial Joins | 2.5 | Multi-table spatial analysis |
| 8 | Complex Analysis | 2.5 | Advanced workflows and CTEs |

### Submission Process

1. **Complete all templates** (remove all `_____` placeholders)
2. **Test locally** using `python test_assignment.py -v`
3. **Generate grade report** using `python grading/calculate_grade.py`
4. **Commit and push** your completed SQL files
5. **Verify CI/CD** passes all automated tests in GitHub Actions

## 🔧 PostGIS Quick Reference

### Basic Spatial Functions

```sql
-- Geometry inspection
ST_GeometryType(geom)    -- Returns geometry type (ST_Point, ST_Polygon, etc.)
ST_SRID(geom)           -- Returns spatial reference system ID
ST_AsText(geom)         -- Returns WKT representation

-- Geometry creation
ST_MakePoint(x, y)      -- Create point from coordinates
ST_GeomFromText(wkt, srid) -- Create geometry from WKT string
ST_SetSRID(geom, srid)  -- Assign SRID to geometry

-- Measurements
ST_Distance_Sphere(geom1, geom2)  -- Geographic distance in meters
ST_Area(geom)           -- Area in square units of SRID
ST_Length(geom)         -- Length in linear units of SRID

-- Coordinate transformation
ST_Transform(geom, srid) -- Transform to different coordinate system
ST_X(geom), ST_Y(geom)  -- Extract coordinate components
```

### Common Coordinate Systems

```sql
-- Geographic coordinate systems (degrees)
EPSG:4326  -- WGS84 (Global GPS standard)

-- Projected coordinate systems (meters)
EPSG:32610 -- UTM Zone 10N (US West Coast: WA, OR, CA)
EPSG:32611 -- UTM Zone 11N (US West: CA, NV)
EPSG:32613 -- UTM Zone 13N (US Central: CO, WY, MT)
EPSG:32614 -- UTM Zone 14N (US Central: TX, OK, KS)
```

### Spatial Relationships

```sql
-- Containment
ST_Within(geom1, geom2)    -- geom1 completely inside geom2
ST_Contains(geom1, geom2)  -- geom1 completely contains geom2

-- Intersection
ST_Intersects(geom1, geom2) -- geometries share any space
ST_Crosses(geom1, geom2)    -- geometries cross each other

-- Proximity
ST_DWithin(geom1, geom2, distance) -- within specified distance
ST_Distance(geom1, geom2)           -- distance between geometries
```

### Spatial Analysis Operations

```sql
-- Buffers
ST_Buffer(geom, radius)     -- Create buffer zone
ST_Buffer(geom, radius, segments) -- Buffer with segment control

-- Overlay operations  
ST_Intersection(geom1, geom2) -- Common area of two geometries
ST_Union(geom1, geom2)        -- Combined area of geometries
ST_Difference(geom1, geom2)   -- geom1 minus geom2

-- Aggregation
ST_Union(geom_column)         -- Combine multiple geometries
ST_Collect(geom_column)       -- Collect geometries into collection
```

## 🔧 Troubleshooting

### Common PostGIS Errors

**Error: `ERROR: function st_distance_sphere(geometry, geometry) does not exist`**
- **Solution:** Use `ST_Distance_Sphere()` with correct capitalization
- **Note:** PostGIS functions are case-sensitive

**Error: `ERROR: transform: couldn't project point`**
- **Solution:** Check EPSG codes are valid and appropriate for your data region
- **Common UTM Zones:** 32610 (West Coast), 32613 (Colorado), 32614 (Texas)

**Error: `ERROR: geometry contains non-closed rings`**
- **Solution:** Ensure polygon WKT strings close properly (first point = last point)
- **Example:** `POLYGON((x1 y1, x2 y2, x3 y3, x1 y1))`

**Error: Query returns no results unexpectedly**
- **Check SRID consistency:** All geometries must have same SRID for spatial operations
- **Check coordinate order:** PostGIS uses (longitude, latitude) not (latitude, longitude)
- **Verify data extent:** Use `ST_Extent(geom)` to check geometry bounds

### Performance Optimization

**Slow spatial queries:**
```sql
-- Check if spatial indexes exist
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE indexname LIKE '%geom%';

-- Create spatial index if missing
CREATE INDEX idx_cities_geom ON cities USING GIST (geom);
```

**Improve measurement accuracy:**
```sql
-- Always transform to appropriate UTM zone for meter-based calculations
-- Example: West Coast data
ST_Area(ST_Transform(geom, 32610))  -- Good
ST_Area(geom)                       -- Less accurate for WGS84 data
```

### Docker and Database Issues

**Container won't start:**
```bash
# Check container status
docker-compose ps

# View container logs  
docker-compose logs postgres

# Restart services
docker-compose down && docker-compose up -d
```

**Database connection issues:**
```bash
# Verify PostGIS is listening on correct port
docker port postgis-basics-postgres

# Test connection manually
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -c "SELECT version();"
```

**Data not loading:**
```bash
# Check if data initialization script ran
docker exec -it postgis-basics-postgres psql -U postgres -d gis_fundamentals -c "SELECT count(*) FROM cities;"

# Manually reload data if needed
docker exec -i postgis-basics-postgres psql -U postgres -d gis_fundamentals < data/load_spatial_data.sql
```

## 📚 Learning Resources

### Essential PostGIS Documentation

- **[PostGIS Manual](https://postgis.net/docs/)** - Complete function reference
- **[PostGIS Tutorial](https://postgis.net/workshops/postgis-intro/)** - Hands-on workshop
- **[Spatial Reference Systems](https://spatialreference.org/)** - EPSG code database
- **[PostGIS FAQ](https://postgis.net/docs/PostGIS_FAQ.html)** - Common questions and solutions

### Key PostGIS Functions You'll Master

**Geometry Constructors:**
- `ST_MakePoint()` - Point creation
- `ST_GeomFromText()` - WKT parsing  
- `ST_Buffer()` - Buffer creation
- `ST_Centroid()` - Geometry center

**Spatial Analysis:**
- `ST_Distance_Sphere()` - Accurate geographic distance
- `ST_Area()` - Area calculation
- `ST_Length()` - Linear measurement
- `ST_Intersection()` - Geometric intersection

**Coordinate Systems:**
- `ST_Transform()` - CRS transformation
- `ST_SRID()` - Get spatial reference
- `ST_SetSRID()` - Set spatial reference

**Spatial Relationships:**
- `ST_Within()` - Containment testing
- `ST_Intersects()` - Intersection testing
- `ST_DWithin()` - Proximity testing

### Coordinate Reference Systems Guide

**When to Use Geographic (WGS84, EPSG:4326):**
- ✓ Data storage and exchange
- ✓ Web mapping applications  
- ✓ Global datasets
- ✗ Accurate distance/area calculations

**When to Use Projected (UTM zones):**
- ✓ Accurate measurements (distance, area, buffer)
- ✓ Engineering and surveying applications
- ✓ Local analysis and mapping
- ✗ Global datasets spanning multiple zones

**UTM Zone Selection:**
```sql
-- US West Coast: Washington, Oregon, Northern California
EPSG:32610  -- UTM Zone 10N

-- California Central Valley, Nevada  
EPSG:32611  -- UTM Zone 11N

-- Colorado, Wyoming, Montana, New Mexico
EPSG:32613  -- UTM Zone 13N

-- Texas, Oklahoma, Kansas, Nebraska
EPSG:32614  -- UTM Zone 14N
```

## 🎯 Success Criteria

### Template Completion (Required)
- [ ] All `_____` placeholders replaced with valid PostGIS functions
- [ ] All SQL files execute without syntax errors
- [ ] All queries return expected result structure

### Spatial Accuracy (Quality Indicators)
- [ ] Coordinate systems properly specified (EPSG codes)
- [ ] Measurements use appropriate projections for accuracy
- [ ] Spatial relationships use correct topology functions
- [ ] Complex analysis follows logical workflow patterns

### Professional Best Practices
- [ ] Queries follow consistent formatting and style
- [ ] Comments explain complex spatial logic
- [ ] Efficient use of spatial