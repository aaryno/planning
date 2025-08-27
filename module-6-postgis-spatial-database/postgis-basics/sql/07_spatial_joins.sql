-- ===================================================================
-- Query 7: Spatial Joins (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to perform complex spatial joins between multiple datasets
--
-- TASK: Execute advanced spatial joins to analyze relationships between datasets:
--       1. Join cities to their containing states with population summary
--       2. Join weather stations to their nearest cities within 200km
--       3. Join highways to all states they intersect with length calculations
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows joining parks to overlapping highways
-- 3. You need to create more complex multi-table spatial joins
-- 4. Fill in the join conditions and aggregation functions below
--
-- EXPECTED RESULT:
-- You should see results for three different spatial join operations:
-- - Cities grouped by state with total population per state
-- - Weather stations matched to their nearest major cities
-- - Highway segments with total length per state they traverse
--
-- ===================================================================

-- TODO: Write your PostGIS spatial join queries below
-- HINT: Use ST_Within() for containment joins (cities in states)
-- HINT: Use ST_DWithin() with DISTINCT ON for nearest neighbor joins
-- HINT: Use ST_Intersects() for intersection joins (highways crossing states)
-- HINT: Use GROUP BY for aggregation joins
-- HINT: Use ST_Length() with ST_Transform() for accurate length calculations

-- Query 7a: Spatial join cities to states with population aggregation
SELECT
    'Cities by State Population' AS join_type,
    s.state_name,
    s.state_code,
    COUNT(c.city_id) AS cities_count,
    SUM(c.population) AS total_population,
    ROUND(AVG(c.population)) AS avg_population
FROM _____ s
LEFT JOIN _____ c ON ST_Within(_____.geom, _____.geom)
GROUP BY s.state_name, s.state_code
HAVING COUNT(c.city_id) > 0  -- Only show states with cities
ORDER BY total_population DESC

UNION ALL

-- Query 7b: Spatial join weather stations to nearest cities within 200km
SELECT DISTINCT ON (ws.station_id)
    'Stations to Nearest Cities' AS join_type,
    ws.name AS station_name,
    c.name AS nearest_city,
    ROUND(
        ST_Distance_Sphere(ws.geom, c.geom) / 1000, 1
    )::TEXT AS distance_km,
    NULL::INTEGER AS cities_count,  -- Match column structure
    c.population,
    NULL::INTEGER AS avg_population  -- Match column structure
FROM _______________ ws
JOIN _____ c ON ST_DWithin(
    ST_Transform(ws.geom, 32610),
    ST_Transform(c.geom, 32610),
    _____  -- 200km = 200000 meters
)
ORDER BY ws.station_id, ST_Distance_Sphere(ws.geom, c.geom)

UNION ALL

-- Query 7c: Spatial join highways to states with length calculation
SELECT
    'Highway Length by State' AS join_type,
    s.state_name,
    h.name AS highway_name,
    ROUND(
        ST_Length(
            ST_Transform(
                ST_Intersection(h.geom, s.geom),
                CASE
                    WHEN s.state_code = 'WA' THEN 32610  -- UTM Zone 10N
                    WHEN s.state_code = 'CA' THEN 32610  -- UTM Zone 10N
                    WHEN s.state_code = 'TX' THEN 32614  -- UTM Zone 14N
                    ELSE 32610  -- Default to Zone 10N
                END
            )
        ) / 1000, 2
    )::TEXT AS highway_length_km,
    1 AS cities_count,  -- Match column structure
    NULL::INTEGER AS total_population,  -- Match column structure
    NULL::INTEGER AS avg_population  -- Match column structure
FROM _____ s
JOIN _______ h ON ST_Intersects(_____.geom, _____.geom)
WHERE ST_Length(ST_Intersection(h.geom, s.geom)) > 0  -- Only show actual intersections
ORDER BY s.state_name, h.name;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ LEFT JOIN cities c ON ST_Within(c.geom, s.geom) for city-state containment
-- ☐ GROUP BY s.state_name, s.state_code with population aggregations
-- ☐ COUNT(c.city_id), SUM(c.population), AVG(c.population) functions
-- ☐ DISTINCT ON (ws.station_id) for nearest neighbor selection
-- ☐ ST_DWithin() with 200000 meter distance for station-city proximity
-- ☐ ST_Distance_Sphere() for accurate geographic distance calculation
-- ☐ ST_Intersects(h.geom, s.geom) for highway-state intersection
-- ☐ ST_Intersection() with ST_Length() for highway segment lengths
-- ☐ FROM states, cities, weather_stations, highways tables
-- ☐ Proper UTM zone selection based on state location
-- ☐ HAVING clause to filter states with cities
-- ☐ ORDER BY clauses for logical result organization
-- ☐ UNION ALL to combine the three join examples
-- ☐ Semicolon at the end
-- ===================================================================
