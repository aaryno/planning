-- ===================================================================
-- Query 4: Coordinate System Transformations (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to transform geometries between coordinate reference systems
--
-- TASK: Transform weather station geometries between different coordinate systems:
--       1. Transform from WGS84 (EPSG:4326) to UTM Zone 10N (EPSG:32610)
--       2. Transform from UTM back to WGS84 for verification
--       3. Calculate the difference in coordinates to understand precision
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows transforming park boundaries to State Plane
-- 3. You need to work with weather station point geometries
-- 4. Fill in the EPSG codes and function names below
--
-- EXPECTED RESULT:
-- You should see coordinates for Seattle WSFO station in:
-- - Original WGS84: POINT(-122.3015 47.4502)
-- - UTM Zone 10N: POINT(550000-ish 5250000-ish) [projected meters]
-- - Back to WGS84: Should match original (within rounding precision)
--
-- ===================================================================

-- TODO: Write your PostGIS coordinate transformation queries below
-- HINT: Use ST_Transform(geometry, target_epsg_code)
-- HINT: EPSG:4326 = WGS84 (longitude/latitude in degrees)
-- HINT: EPSG:32610 = UTM Zone 10N (meters, good for US West Coast)
-- HINT: Use ST_X() and ST_Y() to extract coordinate values
-- HINT: Use ROUND() to clean up coordinate precision

SELECT
    name AS station_name,

    -- Original WGS84 coordinates
    ROUND(ST_X(geom), 6) AS wgs84_longitude,
    ROUND(ST_Y(geom), 6) AS wgs84_latitude,

    -- Transformed to UTM Zone 10N coordinates
    ROUND(ST_X(ST_Transform(geom, _____))) AS utm_easting_m,
    ROUND(ST_Y(ST_Transform(geom, _____))) AS utm_northing_m,

    -- Transform back to WGS84 to verify accuracy
    ROUND(ST_X(ST_Transform(ST_Transform(geom, _____), _____)), 6) AS verify_longitude,
    ROUND(ST_Y(ST_Transform(ST_Transform(geom, _____), _____)), 6) AS verify_latitude,

    -- Calculate coordinate difference (should be very small)
    ROUND(ABS(ST_X(geom) - ST_X(ST_Transform(ST_Transform(geom, _____), _____))), 8) AS longitude_diff,
    ROUND(ABS(ST_Y(geom) - ST_Y(ST_Transform(ST_Transform(geom, _____), _____))), 8) AS latitude_diff

FROM _______________
WHERE name = '______________'
LIMIT 1;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ ST_Transform(geom, 32610) to transform WGS84 to UTM Zone 10N
-- ☐ ST_Transform(geom, 4326) to transform back to WGS84
-- ☐ ST_X() and ST_Y() to extract coordinate components
-- ☐ FROM weather_stations table
-- ☐ WHERE name = 'Seattle WSFO' to get specific station
-- ☐ ROUND() functions with appropriate decimal places
-- ☐ Double transformation to verify accuracy
-- ☐ Coordinate difference calculations using ABS()
-- ☐ LIMIT 1 to get exactly one row
-- ☐ Semicolon at the end
-- ===================================================================
