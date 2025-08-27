-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 3
-- Basic Spatial Measurements
-- ===================================================================
--
-- OBJECTIVE: Calculate distances, areas, and lengths using PostGIS
-- measurement functions with proper coordinate system transformations.
--
-- BUSINESS CONTEXT: Accurate spatial measurements are essential for
-- planning and analysis. For example, calculating distances between
-- facilities for emergency response planning, or measuring protected
-- area sizes for conservation reporting.
--
-- LEARNING GOALS:
-- - Master ST_Distance() for point-to-point measurements
-- - Use ST_Area() for polygon area calculations
-- - Apply ST_Length() for linear feature measurements
-- - Practice coordinate system transformations for accuracy
--
-- POINTS: 2 (Template with guidance)
-- ===================================================================

-- Your Task: Complete the spatial measurements analysis below
-- Calculate distances between facilities and protected area statistics

-- PART A: Distance Analysis
-- Find the distance from each ranger station to the nearest visitor center
SELECT
    r.name AS ranger_station,
    r.elevation_ft AS ranger_elevation,

    -- TODO: Find the nearest visitor center name
    -- HINT: Use a subquery with ORDER BY ST_Distance() and LIMIT 1
    (SELECT v.name
     FROM facilities v
     WHERE v.facility_type = _____
     ORDER BY ST_Distance(
         ST_Transform(r.geometry, _____),
         ST_Transform(v.geometry, _____)
     )
     LIMIT _____
    ) AS nearest_visitor_center,

    -- TODO: Calculate distance to nearest visitor center in miles
    -- HINT: Use the same subquery structure but return the distance
    ROUND(
        ((SELECT MIN(ST_Distance(
            ST_Transform(r.geometry, 3857),
            ST_Transform(v.geometry, 3857)
         ))
         FROM facilities v
         WHERE v.facility_type = 'Visitor Center'
        ) / _____)::NUMERIC, 2
    ) AS distance_miles,

    -- TODO: Classify accessibility based on distance
    -- HINT: Use CASE statement - <2 miles='Excellent', <5='Good', <10='Fair', else='Poor'
    CASE
        WHEN (SELECT MIN(ST_Distance(
            ST_Transform(r.geometry, 3857),
            ST_Transform(v.geometry, 3857)
         )) / 1609.34
         FROM facilities v
         WHERE v.facility_type = 'Visitor Center'
        ) < _____ THEN 'Excellent Access'
        WHEN (SELECT MIN(ST_Distance(
            ST_Transform(r.geometry, 3857),
            ST_Transform(v.geometry, 3857)
         )) / 1609.34
         FROM facilities v
         WHERE v.facility_type = 'Visitor Center'
        ) < 5 THEN _____
        WHEN (SELECT MIN(ST_Distance(
            ST_Transform(r.geometry, 3857),
            ST_Transform(v.geometry, 3857)
         )) / 1609.34
         FROM facilities v
         WHERE v.facility_type = 'Visitor Center'
        ) < 10 THEN 'Fair Access'
        ELSE _____
    END AS accessibility_rating

FROM facilities r
WHERE r.facility_type = _____

UNION ALL

-- PART B: Protected Area Measurements
-- Calculate area statistics for different types of protected areas
SELECT
    pa.name AS area_name,
    pa.designation AS area_type,

    -- TODO: Calculate area in square miles
    -- HINT: Transform to projected coordinates, calculate area, convert to square miles
    ROUND(
        (ST_Area(ST_Transform(pa.geometry, _____)) / _____)::NUMERIC, 2
    ) AS area_square_miles,

    -- TODO: Calculate perimeter in miles
    -- HINT: Use ST_Perimeter() with coordinate transformation
    ROUND(
        (ST_Perimeter(ST_Transform(pa.geometry, _____)) / _____)::NUMERIC, 2
    ) AS perimeter_miles,

    -- TODO: Calculate a "compactness ratio" (area/perimeter)
    -- HINT: Divide area by perimeter - more compact shapes have higher ratios
    ROUND(
        (ST_Area(ST_Transform(pa.geometry, 3857)) / 2589988) /
        (ST_Perimeter(ST_Transform(pa.geometry, 3857)) / 1609.34), 3
    ) AS compactness_ratio,

    -- Static classification for union compatibility
    CASE
        WHEN pa.area_acres > 200000 THEN 'Very Large'
        WHEN pa.area_acres > 100000 THEN 'Large'
        WHEN pa.area_acres > 50000 THEN 'Medium'
        ELSE 'Small'
    END AS size_category

FROM protected_areas pa
WHERE pa.designation IN (_____, _____)  -- TODO: Choose 'National Park', 'Wilderness Area'

-- TODO: Order results by area (largest first)
ORDER BY _____ DESC;

-- ===================================================================
-- EXPECTED RESULTS:
-- PART A should show ranger stations with:
-- - Distance to nearest visitor center in miles
-- - Accessibility ratings based on distance
-- - Most remote ranger stations should show 'Poor Access'
--
-- PART B should show protected areas with:
-- - Accurate area measurements in square miles
-- - Perimeter measurements in miles
-- - Compactness ratios (higher = more circular/compact)
-- - Size classifications
-- ===================================================================

-- KEYWORDS TO USE:
-- ST_Distance, ST_Area, ST_Perimeter, ST_Transform, MIN, CASE,
-- ORDER BY, LIMIT, subqueries

-- HINTS:
-- 1. Always use ST_Transform(geometry, 3857) for accurate measurements
-- 2. Distance conversions: meters ÷ 1609.34 = miles
-- 3. Area conversions: sq_meters ÷ 2,589,988 = sq_miles
-- 4. Use subqueries to find minimum distances
-- 5. CASE statements create categorical classifications
-- 6. Compactness ratio helps identify shape characteristics

-- MEASUREMENT REFERENCE:
-- 1 mile = 1,609.34 meters
-- 1 square mile = 2,589,988 square meters
-- EPSG:3857 (Web Mercator) provides meter-based measurements
-- EPSG:4326 (WGS84) uses degrees (not suitable for distance/area)
