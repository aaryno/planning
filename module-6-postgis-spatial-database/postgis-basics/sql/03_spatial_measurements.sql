-- ===================================================================
-- Query 3: Spatial Measurements (2.5 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to measure distances, areas, and lengths using PostGIS
--
-- TASK: Calculate spatial measurements for different geometry types:
--       1. Distance between Seattle and Portland cities
--       2. Area of Yellowstone National Park in square kilometers
--       3. Length of the I-5 highway section in kilometers
--
-- INSTRUCTIONS:
-- 1. Look at the Learning Example in the README.md file
-- 2. The example shows measuring distance between weather stations
-- 3. You need to adapt it to measure different spatial features
-- 4. Fill in the function names and table references below
--
-- EXPECTED RESULT:
-- You should see 3 rows showing different measurements:
-- - Distance between Seattle and Portland (about 280 km)
-- - Area of Yellowstone National Park (8983.18 sq km)
-- - Length of I-5 Washington section (444.52 km)
--
-- ===================================================================

-- TODO: Write your PostGIS spatial measurement queries below
-- HINT: Use ST_Distance() to calculate distance between two points
-- HINT: Use ST_Area() to calculate area of polygons
-- HINT: Use ST_Length() to calculate length of linestrings
-- HINT: For geographic calculations, use ST_Distance_Sphere() or transform to UTM

-- Query 3a: Calculate distance between Seattle and Portland
SELECT
    'Seattle to Portland Distance' AS measurement_type,
    ROUND(
        ST_Distance_Sphere(
            (SELECT geom FROM _____ WHERE name = '_____'),
            (SELECT geom FROM _____ WHERE name = '_____')
        ) / 1000, 2
    ) AS distance_km

UNION ALL

-- Query 3b: Calculate area of Yellowstone National Park
SELECT
    'Yellowstone Park Area' AS measurement_type,
    ROUND(
        ST_Area(
            ST_Transform(
                (SELECT geom FROM ____________ WHERE name = '_________'),
                32613  -- UTM Zone 13N for Wyoming
            )
        ) / 1000000, 2  -- Convert sq meters to sq kilometers
    ) AS area_sq_km

UNION ALL

-- Query 3c: Calculate length of I-5 highway section
SELECT
    'I-5 Highway Length' AS measurement_type,
    ROUND(
        ST_Length(
            ST_Transform(
                (SELECT geom FROM _______ WHERE name = '______________'),
                32610  -- UTM Zone 10N for Washington
            )
        ) / 1000, 2  -- Convert meters to kilometers
    ) AS length_km;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ ST_Distance_Sphere() for accurate geographic distance calculation
-- ☐ SELECT from cities table with WHERE name = 'Seattle' and 'Portland'
-- ☐ ST_Area() with ST_Transform() for accurate area calculation
-- ☐ SELECT from national_parks table with WHERE name = 'Yellowstone'
-- ☐ ST_Length() with ST_Transform() for accurate length calculation
-- ☐ SELECT from highways table with WHERE name = 'I-5 (WA Section)'
-- ☐ Proper unit conversions (divide by 1000 for km, 1000000 for sq km)
-- ☐ ROUND() function with 2 decimal places for clean output
-- ☐ UNION ALL to combine the three measurement examples
-- ☐ Semicolon at the end
-- ===================================================================
