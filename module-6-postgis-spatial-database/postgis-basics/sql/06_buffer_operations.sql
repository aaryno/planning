-- ===================================================================
-- Query 6: Buffer Operations (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to create and use buffer zones for spatial analysis
--
-- TASK: Create buffer zones around different geometry types and use them for analysis:
--       1. Create a 50km buffer around Denver city
--       2. Create a 10km buffer corridor along I-5 highway
--       3. Find all weather stations within the Denver buffer zone
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows creating safety buffers around weather stations
-- 3. You need to create buffers around cities and highways
-- 4. Fill in the buffer distances and spatial analysis functions below
--
-- EXPECTED RESULT:
-- You should see results for three different buffer operations:
-- - Denver city with 50km circular buffer area
-- - I-5 highway with 10km corridor buffer length
-- - Weather stations found within Denver's buffer zone
--
-- ===================================================================

-- TODO: Write your PostGIS buffer operation queries below
-- HINT: Use ST_Buffer(geometry, distance_in_degrees) for geographic buffers
-- HINT: Use ST_Transform() to project to UTM for accurate meter-based buffers
-- HINT: Use ST_Area() and ST_Length() to measure buffer sizes
-- HINT: Use ST_Within() to find features inside buffer zones
-- HINT: 50km ≈ 0.45 degrees, 10km ≈ 0.09 degrees in geographic coordinates

-- Query 6a: Create 50km buffer around Denver and calculate its area
SELECT
    'Denver 50km Buffer' AS analysis_type,
    c.name AS city_name,
    ROUND(
        ST_Area(
            ST_Transform(
                ST_Buffer(
                    ST_Transform(c.geom, 32613),  -- Transform to UTM Zone 13N for Colorado
                    _____  -- 50km = 50000 meters
                ),
                4326
            )
        ) * 111319.5 * 111319.5, 2  -- Convert sq degrees to sq meters approximation
    ) AS buffer_area_sq_m,
    ST_AsText(ST_Buffer(c.geom, _____)) AS buffer_wkt  -- 50km ≈ 0.45 degrees
FROM _____ c
WHERE c.name = '_____'

UNION ALL

-- Query 6b: Create 10km corridor buffer along I-5 highway
SELECT
    'I-5 Highway 10km Corridor' AS analysis_type,
    h.name AS highway_name,
    ROUND(
        ST_Length(
            ST_Transform(
                ST_Buffer(
                    ST_Transform(h.geom, 32610),  -- Transform to UTM Zone 10N for I-5
                    _____  -- 10km = 10000 meters
                ),
                4326
            )
        ) * 111319.5, 2  -- Convert degrees to meters approximation
    ) AS corridor_length_m,
    LEFT(ST_AsText(ST_Buffer(h.geom, _____)), 100) || '...' AS buffer_wkt_sample  -- 10km ≈ 0.09 degrees
FROM _______ h
WHERE h.name = '_______________';

-- Query 6c: Find weather stations within 50km buffer of Denver
WITH denver_buffer AS (
    SELECT ST_Buffer(
        ST_Transform(geom, 32613),  -- Transform to UTM for accurate distance
        _____  -- 50km = 50000 meters
    ) AS buffer_geom
    FROM _____
    WHERE name = '_____'
)
SELECT
    'Stations in Denver Buffer' AS analysis_type,
    ws.name AS station_name,
    ws.elevation_m,
    ROUND(
        ST_Distance(
            ST_Transform((SELECT geom FROM _____ WHERE name = '_____'), 32613),
            ST_Transform(ws.geom, 32613)
        ) / 1000, 2
    ) AS distance_from_denver_km
FROM _______________ ws, denver_buffer db
WHERE ST_Within(
    ST_Transform(ws.geom, 32613),
    db.buffer_geom
)
ORDER BY distance_from_denver_km;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ ST_Buffer() with accurate meter-based distances using ST_Transform()
-- ☐ ST_Buffer(ST_Transform(geom, 32613), 50000) for 50km Denver buffer
-- ☐ FROM cities table with WHERE name = 'Denver'
-- ☐ ST_Buffer(ST_Transform(geom, 32610), 10000) for 10km I-5 corridor
-- ☐ FROM highways table with WHERE name = 'I-5 (WA Section)'
-- ☐ ST_Area() and ST_Length() to measure buffer sizes
-- ☐ WITH clause (CTE) to create denver_buffer for reuse
-- ☐ ST_Within() to find weather stations inside Denver buffer
-- ☐ ST_Distance() to calculate exact distances from Denver
-- ☐ FROM weather_stations with spatial filtering
-- ☐ UTM projections (32613 for Colorado, 32610 for Washington)
-- ☐ ORDER BY distance for logical result ordering
-- ☐ Semicolon at the end
-- ===================================================================
