-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 4
-- Coordinate System Transformations
-- ===================================================================
--
-- OBJECTIVE: Master coordinate system transformations to ensure
-- accurate spatial analysis across different projection systems.
--
-- BUSINESS CONTEXT: Different coordinate systems are used for different
-- purposes - geographic coordinates (lat/lon) for global positioning,
-- projected coordinates for accurate distance/area measurements, and
-- local coordinate systems for regional analysis.
--
-- LEARNING GOALS:
-- - Master ST_Transform() for coordinate system conversions
-- - Understand when to use different coordinate systems (4326, 3857, 26913)
-- - Compare measurements across coordinate systems
-- - Practice SRID (Spatial Reference ID) management
--
-- POINTS: 2 (Guided template - moderate difficulty)
-- ===================================================================

-- Your Task: Complete the coordinate transformation analysis
-- Compare the same measurements in different coordinate systems

-- PART A: Coordinate System Information
-- Show how the same point appears in different coordinate systems
SELECT
    f.name AS facility_name,
    f.facility_type,

    -- Original coordinates (WGS84 Geographic - EPSG:4326)
    ST_SRID(f.geometry) AS original_srid,
    ROUND(ST_X(f.geometry)::NUMERIC, 6) AS longitude_wgs84,
    ROUND(ST_Y(f.geometry)::NUMERIC, 6) AS latitude_wgs84,

    -- TODO: Transform to Web Mercator (EPSG:3857) and show coordinates
    -- HINT: Use ST_Transform(geometry, 3857), then ST_X() and ST_Y()
    ROUND(ST_X(ST_Transform(f.geometry, _____))::NUMERIC, 2) AS x_web_mercator,
    ROUND(ST_Y(ST_Transform(f.geometry, _____))::NUMERIC, 2) AS y_web_mercator,

    -- TODO: Transform to UTM Zone 13N (EPSG:26913) for Colorado
    -- HINT: UTM provides meter-based coordinates for regional accuracy
    ROUND(ST_X(ST_Transform(f.geometry, _____))::NUMERIC, 2) AS x_utm_zone13n,
    ROUND(ST_Y(ST_Transform(f.geometry, _____))::NUMERIC, 2) AS y_utm_zone13n

FROM facilities f
WHERE f.facility_type = 'Visitor Center'
ORDER BY f.name

UNION ALL

-- PART B: Distance Comparison Across Coordinate Systems
-- Show how distance calculations vary by coordinate system
SELECT
    'Distance Analysis' AS facility_name,
    'System Comparison' AS facility_type,

    -- Reference point coordinates (first visitor center)
    (SELECT ST_SRID(geometry) FROM facilities WHERE facility_type = 'Visitor Center' LIMIT 1) AS original_srid,
    (SELECT ROUND(ST_X(geometry)::NUMERIC, 6) FROM facilities WHERE facility_type = 'Visitor Center' LIMIT 1) AS longitude_wgs84,
    (SELECT ROUND(ST_Y(geometry)::NUMERIC, 6) FROM facilities WHERE facility_type = 'Visitor Center' LIMIT 1) AS latitude_wgs84,

    -- TODO: Calculate average distance between visitor centers using WGS84 (degrees)
    -- HINT: This will be WRONG for distance - geographic coordinates give degree units
    (SELECT ROUND(AVG(ST_Distance(v1.geometry, v2.geometry))::NUMERIC, 6)
     FROM facilities v1, facilities v2
     WHERE v1.facility_type = 'Visitor Center'
     AND v2.facility_type = 'Visitor Center'
     AND v1.facility_id < v2.facility_id
    ) AS avg_distance_degrees_wgs84,

    -- TODO: Calculate average distance using Web Mercator (meters) - convert to miles
    -- HINT: Transform both geometries to 3857, calculate distance, convert to miles
    (SELECT ROUND((AVG(ST_Distance(
        ST_Transform(v1.geometry, _____),
        ST_Transform(v2.geometry, _____)
    )) / _____)::NUMERIC, 2)
     FROM facilities v1, facilities v2
     WHERE v1.facility_type = 'Visitor Center'
     AND v2.facility_type = 'Visitor Center'
     AND v1.facility_id < v2.facility_id
    ) AS avg_distance_miles_web_mercator

UNION ALL

-- PART C: Area Comparison Across Coordinate Systems
-- Compare protected area calculations in different systems
SELECT
    pa.name AS facility_name,
    'Area Comparison' AS facility_type,

    ST_SRID(pa.geometry) AS original_srid,

    -- TODO: Calculate area in WGS84 (will be in square degrees - not useful!)
    ROUND(ST_Area(pa.geometry)::NUMERIC, 8) AS area_square_degrees,

    -- TODO: Calculate area in Web Mercator and convert to square miles
    -- HINT: ST_Area(ST_Transform(geometry, 3857)) / 2589988
    ROUND((ST_Area(ST_Transform(pa.geometry, _____)) / _____)::NUMERIC, 2) AS area_square_miles_web_mercator,

    -- TODO: Calculate area in UTM Zone 13N and convert to square miles
    -- HINT: UTM often provides the most accurate measurements for regional data
    ROUND((ST_Area(ST_Transform(pa.geometry, _____)) / _____)::NUMERIC, 2) AS area_square_miles_utm,

    -- TODO: Calculate percentage difference between Web Mercator and UTM measurements
    -- HINT: ABS((web_mercator - utm) / utm) * 100
    ROUND(ABS(
        ((ST_Area(ST_Transform(pa.geometry, 3857)) / 2589988) -
         (ST_Area(ST_Transform(pa.geometry, 26913)) / 2589988)) /
        (ST_Area(ST_Transform(pa.geometry, 26913)) / 2589988) * 100
    )::NUMERIC, 2) AS percent_difference

FROM protected_areas pa
WHERE pa.designation = 'National Park'
ORDER BY pa.area_acres DESC
LIMIT 3;

-- ===================================================================
-- EXPECTED RESULTS:
-- PART A: Same points in different coordinate systems
-- - WGS84: Longitude/latitude in degrees (e.g., -105.1234, 40.5678)
-- - Web Mercator: X/Y in meters (e.g., -11712345, 4887654)
-- - UTM Zone 13N: Easting/Northing in meters (e.g., 456789, 4487654)
--
-- PART B: Distance comparisons showing
-- - WGS84 distances in degrees (meaningless for real distance)
-- - Web Mercator distances in miles (meaningful measurements)
--
-- PART C: Area comparisons showing
-- - Square degrees (meaningless)
-- - Square miles from Web Mercator and UTM (should be very similar)
-- - Small percentage differences between Web Mercator and UTM
-- ===================================================================

-- KEYWORDS TO USE:
-- ST_Transform, ST_SRID, ST_X, ST_Y, ST_Distance, ST_Area,
-- coordinate system IDs (4326, 3857, 26913)

-- HINTS:
-- 1. EPSG:4326 = WGS84 Geographic (latitude/longitude in degrees)
-- 2. EPSG:3857 = Web Mercator (meters, global but distorted)
-- 3. EPSG:26913 = UTM Zone 13N (meters, accurate for Colorado region)
-- 4. Always transform to projected coordinates for distance/area calculations
-- 5. Geographic coordinates (4326) should NEVER be used for measurements
-- 6. UTM zones provide the most accurate measurements for regional data

-- COORDINATE SYSTEM REFERENCE:
-- - Geographic (4326): Global coverage, degrees, NOT for measurements
-- - Web Mercator (3857): Web mapping standard, meters, global coverage
-- - UTM Zone 13N (26913): Regional accuracy for Colorado, meters
-- - Distance conversions: meters ÷ 1609.34 = miles
-- - Area conversions: sq_meters ÷ 2,589,988 = sq_miles

-- WHY THIS MATTERS:
-- Using the wrong coordinate system can result in:
-- - Wildly incorrect distance/area calculations
-- - Analysis errors in planning and decision making
-- - Professional credibility issues
-- Always transform to appropriate projected coordinates for measurements!
