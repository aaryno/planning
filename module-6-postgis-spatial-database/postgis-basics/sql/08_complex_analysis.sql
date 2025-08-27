-- ===================================================================
-- Query 8: Complex Spatial Analysis (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Combine multiple PostGIS functions for comprehensive spatial analysis
--
-- TASK: Execute a complex multi-step spatial analysis that combines concepts from all previous queries:
--       1. Find cities within 100km of national parks
--       2. For each city-park pair, find the closest weather station
--       3. Create 25km buffer corridors along highways connecting cities to parks
--       4. Calculate total analysis area and provide summary statistics
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows a tourism analysis combining multiple spatial datasets
-- 3. You need to create a comprehensive analysis using CTEs and spatial joins
-- 4. Fill in the complex spatial functions and multi-table relationships below
--
-- EXPECTED RESULT:
-- You should see results for a complex spatial analysis including:
-- - City-park pairs within 100km with distances
-- - Closest weather station to each pair with climate data access
-- - Highway corridor analysis with buffer areas
-- - Summary statistics for the entire analysis region
--
-- ===================================================================

-- TODO: Write your complex PostGIS spatial analysis below
-- HINT: Use WITH clauses (CTEs) to break complex analysis into steps
-- HINT: Combine ST_DWithin(), ST_Distance_Sphere(), and ST_Buffer()
-- HINT: Use window functions like ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)
-- HINT: Use ST_Union() to combine multiple buffer geometries
-- HINT: Use ST_Area() and ST_Length() for comprehensive measurements

-- Step 1: Find city-park pairs within 100km
WITH city_park_pairs AS (
    SELECT
        c.name AS city_name,
        c.population,
        c.geom AS city_geom,
        p.name AS park_name,
        p.area_sq_km AS park_area,
        p.geom AS park_geom,
        ROUND(ST_Distance_Sphere(c.geom, p.geom) / 1000, 2) AS distance_km
    FROM _____ c
    CROSS JOIN _____________ p
    WHERE ST_DWithin(
        ST_Transform(c.geom, 32610),
        ST_Transform(p.geom, 32610),
        _____  -- 100km = 100000 meters
    )
),

-- Step 2: Find closest weather station for each city-park pair
city_park_weather AS (
    SELECT
        cpp.*,
        ws.name AS closest_station,
        ws.elevation_m,
        ws.station_type,
        ROUND(
            ST_Distance_Sphere(
                ST_Centroid(ST_MakeLine(cpp.city_geom, ST_Centroid(cpp.park_geom))),
                ws.geom
            ) / 1000, 2
        ) AS station_distance_km,
        ROW_NUMBER() OVER (
            PARTITION BY cpp.city_name, cpp.park_name
            ORDER BY ST_Distance_Sphere(
                ST_Centroid(ST_MakeLine(cpp.city_geom, ST_Centroid(cpp.park_geom))),
                ws.geom
            )
        ) AS station_rank
    FROM city_park_pairs cpp
    CROSS JOIN _______________ ws
),

-- Step 3: Create highway corridors connecting analysis regions
highway_corridors AS (
    SELECT
        h.name AS highway_name,
        ST_Buffer(
            ST_Transform(h.geom, 32610),
            _____  -- 25km = 25000 meters
        ) AS corridor_buffer,
        ROUND(
            ST_Length(ST_Transform(h.geom, 32610)) / 1000, 2
        ) AS highway_length_km
    FROM _______ h
    WHERE ST_Intersects(
        h.geom,
        (SELECT ST_Union(ST_Buffer(city_geom, 0.5)) FROM city_park_pairs)
    )
    OR ST_Intersects(
        h.geom,
        (SELECT ST_Union(ST_Buffer(ST_Centroid(park_geom), 0.5)) FROM city_park_pairs)
    )
),

-- Step 4: Calculate comprehensive analysis statistics
analysis_summary AS (
    SELECT
        COUNT(DISTINCT cpw.city_name) AS total_cities,
        COUNT(DISTINCT cpw.park_name) AS total_parks,
        COUNT(DISTINCT cpw.closest_station) AS total_stations,
        ROUND(AVG(cpw.distance_km), 2) AS avg_city_park_distance_km,
        ROUND(AVG(cpw.station_distance_km), 2) AS avg_station_distance_km,
        ROUND(SUM(cpw.park_area), 2) AS total_park_area_sq_km,
        SUM(cpw.population) AS total_population_served,
        ROUND(
            ST_Area(
                ST_Transform(
                    ST_Union(
                        ST_Buffer(ST_Union(cpw.city_geom), 0.5)
                    ),
                    32610
                )
            ) / 1000000, 2
        ) AS analysis_region_area_sq_km
    FROM city_park_weather cpw
    WHERE cpw.station_rank = 1
)

-- Final Results: Complex spatial analysis output
SELECT
    'Tourism Analysis Results' AS analysis_type,
    cpw.city_name,
    cpw.population,
    cpw.park_name,
    cpw.park_area,
    cpw.distance_km AS city_park_distance_km,
    cpw.closest_station,
    cpw.elevation_m AS station_elevation_m,
    cpw.station_distance_km,
    -- Add highway corridor information
    (SELECT STRING_AGG(hc.highway_name, ', ')
     FROM highway_corridors hc
     WHERE ST_Intersects(
         ST_Buffer(ST_Transform(cpw.city_geom, 32610), 50000),
         hc.corridor_buffer
     )) AS nearby_highways,
    -- Add analysis summary
    (SELECT total_cities FROM analysis_summary) AS total_cities_in_analysis,
    (SELECT total_parks FROM analysis_summary) AS total_parks_in_analysis,
    (SELECT analysis_region_area_sq_km FROM analysis_summary) AS total_analysis_area_sq_km
FROM city_park_weather cpw
WHERE cpw.station_rank = 1  -- Only closest station per city-park pair
ORDER BY cpw.distance_km, cpw.population DESC;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ WITH clauses (CTEs) to organize complex multi-step analysis
-- ☐ ST_DWithin() with 100000 meter distance for city-park proximity
-- ☐ CROSS JOIN between cities and national_parks tables
-- ☐ ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) for ranking
-- ☐ ST_Distance_Sphere() for accurate geographic distance calculations
-- ☐ ST_Centroid() and ST_MakeLine() for geometric calculations
-- ☐ ST_Buffer() with 25000 meter distance for highway corridors
-- ☐ ST_Transform() to UTM (32610) for accurate meter-based calculations
-- ☐ ST_Union() to combine multiple geometries for region analysis
-- ☐ ST_Area() and ST_Length() for comprehensive measurements
-- ☐ Multiple table joins (cities, national_parks, weather_stations, highways)
-- ☐ Aggregate functions (COUNT, AVG, SUM) for summary statistics
-- ☐ STRING_AGG() for text aggregation of highway names
-- ☐ Subqueries to incorporate analysis summary data
-- ☐ ORDER BY for logical result organization
-- ☐ Semicolon at the end
-- ===================================================================
