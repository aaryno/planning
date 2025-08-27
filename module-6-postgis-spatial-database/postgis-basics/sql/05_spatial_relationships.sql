-- ===================================================================
-- Query 5: Spatial Relationships (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to query spatial relationships between different geometries
--
-- TASK: Use spatial relationship functions to answer location questions:
--       1. Find cities that are within Washington state
--       2. Find highways that intersect with national parks
--       3. Find weather stations within 100km of Seattle
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows finding parks that contain weather stations
-- 3. You need to adapt it to find different spatial relationships
-- 4. Fill in the spatial relationship functions and conditions below
--
-- EXPECTED RESULT:
-- You should see results for three different relationship queries:
-- - Washington cities: Seattle, Portland (if data crosses border)
-- - Highway-Park intersections: highways that cross park boundaries
-- - Weather stations near Seattle: stations within 100km radius
--
-- ===================================================================

-- TODO: Write your PostGIS spatial relationship queries below
-- HINT: Use ST_Within(geometry1, geometry2) for containment
-- HINT: Use ST_Intersects(geometry1, geometry2) for intersection
-- HINT: Use ST_DWithin(geometry1, geometry2, distance) for proximity
-- HINT: Use ST_Distance_Sphere() for accurate distance calculations
-- HINT: Join tables using spatial relationships in WHERE clauses

-- Query 5a: Find cities within Washington state
SELECT
    'Cities in Washington' AS query_type,
    c.name AS city_name,
    c.population,
    s.state_name
FROM _____ c
JOIN _____ s ON ST_Within(_____.geom, _____.geom)
WHERE s.state_code = '_____'

UNION ALL

-- Query 5b: Find highways that intersect with national parks
SELECT
    'Highway-Park Intersections' AS query_type,
    h.name AS highway_name,
    p.name AS park_name,
    NULL AS population  -- NULL to match column structure
FROM _______ h
JOIN _____________ p ON ST_Intersects(_____.geom, _____.geom)

UNION ALL

-- Query 5c: Find weather stations within 100km of Seattle
SELECT
    'Stations Near Seattle' AS query_type,
    ws.name AS station_name,
    ROUND(
        ST_Distance_Sphere(
            (SELECT geom FROM _____ WHERE name = '_____'),
            ws.geom
        ) / 1000, 1
    )::TEXT AS distance_km,
    NULL AS state_name  -- NULL to match column structure
FROM _______________ ws
WHERE ST_DWithin(
    ST_Transform(ws.geom, 32610),  -- Transform to meters for accurate distance
    ST_Transform((SELECT geom FROM _____ WHERE name = '_____'), 32610),
    _____  -- 100km = 100000 meters
)
AND ws.name != '_____'  -- Exclude Seattle itself
ORDER BY query_type, city_name, highway_name, station_name;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ ST_Within(c.geom, s.geom) to find cities within states
-- ☐ JOIN cities c with states s using spatial relationship
-- ☐ WHERE s.state_code = 'WA' to filter Washington state
-- ☐ ST_Intersects(h.geom, p.geom) to find highway-park intersections
-- ☐ JOIN highways h with national_parks p using spatial relationship
-- ☐ ST_DWithin() with transformed coordinates for 100km proximity
-- ☐ FROM weather_stations with spatial distance filtering
-- ☐ WHERE name = 'Seattle' to find Seattle city
-- ☐ Distance parameter: 100000 (100km in meters)
-- ☐ UNION ALL to combine the three relationship queries
-- ☐ ORDER BY clause to organize results
-- ☐ Semicolon at the end
-- ===================================================================
