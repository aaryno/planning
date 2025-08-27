-- ===================================================================
-- Query 2: Geometry Creation Functions (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to create new geometries using PostGIS functions
--
-- TASK: Create three different types of geometries and display their properties:
--       1. A point geometry using ST_MakePoint
--       2. A polygon geometry using ST_GeomFromText
--       3. A buffer around the point using ST_Buffer
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows creating a weather station point in Portland
-- 3. You need to create geometries for a new location in Denver, CO
-- 4. Fill in the coordinate values and function parameters below
--
-- EXPECTED RESULT:
-- You should see 3 rows showing different geometry types:
-- - Row 1: Point geometry for Denver (-104.9903, 39.7392)
-- - Row 2: Square polygon around Denver (0.1 degree buffer)
-- - Row 3: Circular buffer around Denver point (0.05 degree radius)
--
-- ===================================================================

-- TODO: Write your PostGIS geometry creation queries below
-- HINT: Denver coordinates are longitude: -104.9903, latitude: 39.7392
-- HINT: Use ST_MakePoint(longitude, latitude) for points
-- HINT: Use ST_GeomFromText('POLYGON((...))', 4326) for polygons
-- HINT: Use ST_Buffer(geometry, distance) for circular buffers
-- HINT: Use ST_SetSRID() to assign coordinate system 4326

-- Query 2a: Create a point geometry for Denver
SELECT
    'Denver Point' AS geometry_name,
    ST_GeometryType(ST_SetSRID(ST_MakePoint(_______, _______), _____)) AS geom_type,
    ST_AsText(ST_SetSRID(ST_MakePoint(_______, _______), _____)) AS geometry_wkt

UNION ALL

-- Query 2b: Create a square polygon around Denver (±0.1 degrees)
SELECT
    'Denver Square' AS geometry_name,
    ST_GeometryType(ST_GeomFromText('POLYGON((_______ _______, _______ _______, _______ _______, _______ _______, _______ _______))', _____)) AS geom_type,
    ST_AsText(ST_GeomFromText('POLYGON((_______ _______, _______ _______, _______ _______, _______ _______, _______ _______))', _____)) AS geometry_wkt

UNION ALL

-- Query 2c: Create a circular buffer around Denver point
SELECT
    'Denver Buffer' AS geometry_name,
    ST_GeometryType(ST_Buffer(ST_SetSRID(ST_MakePoint(_______, _______), _____), _____)) AS geom_type,
    ST_AsText(ST_Buffer(ST_SetSRID(ST_MakePoint(_______, _______), _____), _____)) AS geometry_wkt;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ ST_MakePoint(-104.9903, 39.7392) for Denver coordinates
-- ☐ ST_SetSRID(..., 4326) to set WGS84 coordinate system
-- ☐ POLYGON with 5 coordinate pairs (closed ring) for square
-- ☐ ST_Buffer(..., 0.05) with 0.05 degree radius for circular buffer
-- ☐ UNION ALL to combine the three geometry examples
-- ☐ Proper WKT format in ST_GeomFromText
-- ☐ Semicolon at the end
-- ===================================================================
