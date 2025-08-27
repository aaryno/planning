-- ===================================================================
-- Query 1: Spatial Data Inspection (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to inspect spatial data and understand geometry properties
--
-- TASK: Explore the spatial properties of the cities table and display basic
--       geometry information for the first 5 cities
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows how to inspect weather station geometries
-- 3. You need to adapt it to examine cities table geometry properties
-- 4. Replace the table name and column selections below
--
-- EXPECTED RESULT:
-- You should see 5 rows showing:
-- - city_id, name, state_code
-- - geometry_type (should be "ST_Point")
-- - coordinate_system (should be 4326 for WGS84)
-- - coordinates_text (readable coordinate format)
--
-- ===================================================================

-- TODO: Write your PostGIS query below
-- HINT: Use ST_GeometryType() to get geometry type
-- HINT: Use ST_SRID() to get spatial reference system ID
-- HINT: Use ST_AsText() to get human-readable coordinates
-- HINT: SELECT the city info plus the three spatial functions

SELECT
    city_id,
    name,
    state_code,
    ST_GeometryType(_______) AS geometry_type,
    ST_SRID(_______) AS coordinate_system,
    ST_AsText(_______) AS coordinates_text
FROM __________
LIMIT _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT city_id, name, state_code (basic city information)
-- ☐ ST_GeometryType(geom) AS geometry_type (shows "ST_Point")
-- ☐ ST_SRID(geom) AS coordinate_system (shows 4326)
-- ☐ ST_AsText(geom) AS coordinates_text (shows "POINT(lon lat)")
-- ☐ FROM cities (correct table name)
-- ☐ LIMIT 5 (exactly 5 rows)
-- ☐ Semicolon at the end
-- ===================================================================
