-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 2
-- Simple Buffer Operations
-- ===================================================================
--
-- OBJECTIVE: Create buffers around spatial features to analyze
-- proximity and service areas using ST_Buffer() function.
--
-- BUSINESS CONTEXT: Buffers are fundamental to spatial analysis,
-- used for proximity analysis, service area definition, and
-- impact zone modeling. For example, creating 1-mile buffers
-- around facilities to determine service coverage areas.
--
-- LEARNING GOALS:
-- - Master ST_Buffer() function for creating circular buffers
-- - Understand coordinate system transformations for accurate distances
-- - Practice distance unit conversions (miles to meters)
-- - Learn buffer area calculations
--
-- POINTS: 2 (Example provided with blanks to complete)
-- ===================================================================

-- Your Task: Complete the buffer analysis below by filling in the blanks
-- Create 1-mile buffers around all visitor centers and calculate their areas

-- LEARNING EXAMPLE: Here's how you create a 0.5-mile buffer around facilities:
/*
SELECT
    name AS facility_name,
    facility_type,
    -- Transform to Web Mercator (meters) for accurate buffer
    ST_Transform(
        ST_Buffer(
            ST_Transform(geometry, 3857),  -- Transform to meters first
            804.67                         -- 0.5 miles in meters (0.5 * 1609.34)
        ),
        4326                              -- Transform back to WGS84
    ) AS buffer_geometry,
    -- Calculate buffer area in square miles
    ROUND(
        (ST_Area(ST_Transform(
            ST_Buffer(ST_Transform(geometry, 3857), 804.67),
        3857)) / 2589988)::NUMERIC, 2     -- Convert sq meters to sq miles
    ) AS buffer_area_sq_miles
FROM facilities
WHERE facility_type = 'Campground';
*/

-- YOUR TASK: Adapt the example above for visitor centers with 1-mile buffers
SELECT
    name AS facility_name,
    facility_type,
    elevation_ft,

    -- TODO: Create 1-mile buffer geometry (transform to 3857, buffer, transform back to 4326)
    -- HINT: 1 mile = 1609.34 meters
    ST_Transform(
        ST_Buffer(
            ST_Transform(geometry, _____),  -- Transform to Web Mercator for accuracy
            _____                          -- 1 mile in meters
        ),
        _____                             -- Transform back to WGS84
    ) AS buffer_geometry,

    -- TODO: Calculate buffer area in square miles
    -- HINT: 1 square mile = 2,589,988 square meters
    ROUND(
        (ST_Area(ST_Transform(
            ST_Buffer(ST_Transform(geometry, 3857), _____),
        3857)) / _____)::NUMERIC, 2
    ) AS buffer_area_sq_miles,

    -- TODO: Calculate buffer perimeter in miles
    -- HINT: Use ST_Perimeter() and convert meters to miles (÷ 1609.34)
    ROUND(
        (ST_Perimeter(ST_Transform(
            ST_Buffer(ST_Transform(geometry, 3857), 1609.34),
        3857)) / _____)::NUMERIC, 2
    ) AS buffer_perimeter_miles

FROM facilities
WHERE facility_type = _____           -- TODO: Filter for 'Visitor Center'

-- TODO: Order results by elevation (highest first)
ORDER BY _____ DESC;

-- ===================================================================
-- EXPECTED RESULTS:
-- You should see visitor centers with their 1-mile buffers showing:
-- - Buffer geometry for mapping/visualization
-- - Buffer area (should be close to π square miles ≈ 3.14 sq mi)
-- - Buffer perimeter (should be close to 2π miles ≈ 6.28 miles)
-- - Results ordered by facility elevation
-- ===================================================================

-- KEYWORDS TO USE:
-- ST_Buffer, ST_Transform, ST_Area, ST_Perimeter, WHERE, ORDER BY

-- HINTS:
-- 1. Always transform to a projected coordinate system (3857) before buffering
-- 2. 1 mile = 1609.34 meters
-- 3. 1 square mile = 2,589,988 square meters
-- 4. Buffer area formula: π × radius² (for 1-mile buffer ≈ 3.14 sq mi)
-- 5. Buffer perimeter formula: 2π × radius (for 1-mile buffer ≈ 6.28 miles)

-- DISTANCE CONVERSIONS:
-- meters_to_miles = meters ÷ 1609.34
-- miles_to_meters = miles × 1609.34
-- sq_meters_to_sq_miles = sq_meters ÷ 2589988
