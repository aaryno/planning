-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 1
-- Basic Spatial Data Inspection (COMPLETE EXAMPLE)
-- ===================================================================
--
-- OBJECTIVE: Inspect spatial data to understand geometry types,
-- coordinate systems, and basic spatial properties of our dataset.
--
-- BUSINESS CONTEXT: Before performing any spatial analysis, GIS
-- professionals must understand their data - what types of geometries
-- they're working with, what coordinate systems are used, and basic
-- spatial characteristics.
--
-- LEARNING GOALS:
-- - Explore spatial data structure using PostGIS inspection functions
-- - Understand geometry types (POINT, LINESTRING, POLYGON)
-- - Learn coordinate system identification
-- - Practice basic PostGIS functions
--
-- POINTS: 2 (Complete example provided)
-- ===================================================================

-- This is a COMPLETE WORKING EXAMPLE for you to study and understand
-- Your task: Run this query and understand what each function does

SELECT
    -- Basic table information
    'Protected Areas' AS dataset_name,
    COUNT(*) AS total_features,

    -- Geometry type inspection
    ST_GeometryType(geometry) AS geometry_type,
    COUNT(ST_GeometryType(geometry)) AS type_count,

    -- Coordinate system information
    ST_SRID(geometry) AS coordinate_system,

    -- Spatial extent (bounding box)
    ROUND(ST_XMin(ST_Extent(geometry))::NUMERIC, 4) AS min_longitude,
    ROUND(ST_XMax(ST_Extent(geometry))::NUMERIC, 4) AS max_longitude,
    ROUND(ST_YMin(ST_Extent(geometry))::NUMERIC, 4) AS min_latitude,
    ROUND(ST_YMax(ST_Extent(geometry))::NUMERIC, 4) AS max_latitude,

    -- Sample geometry as text (first record only)
    (SELECT ST_AsText(geometry) FROM protected_areas LIMIT 1) AS sample_geometry_wkt

FROM protected_areas
GROUP BY ST_GeometryType(geometry), ST_SRID(geometry)

UNION ALL

-- Transportation network inspection
SELECT
    'Transportation Network' AS dataset_name,
    COUNT(*) AS total_features,
    ST_GeometryType(geometry) AS geometry_type,
    COUNT(ST_GeometryType(geometry)) AS type_count,
    ST_SRID(geometry) AS coordinate_system,
    ROUND(ST_XMin(ST_Extent(geometry))::NUMERIC, 4) AS min_longitude,
    ROUND(ST_XMax(ST_Extent(geometry))::NUMERIC, 4) AS max_longitude,
    ROUND(ST_YMin(ST_Extent(geometry))::NUMERIC, 4) AS min_latitude,
    ROUND(ST_YMax(ST_Extent(geometry))::NUMERIC, 4) AS max_latitude,
    (SELECT ST_AsText(geometry) FROM transportation_network LIMIT 1) AS sample_geometry_wkt

FROM transportation_network
GROUP BY ST_GeometryType(geometry), ST_SRID(geometry)

UNION ALL

-- Facilities inspection
SELECT
    'Facilities' AS dataset_name,
    COUNT(*) AS total_features,
    ST_GeometryType(geometry) AS geometry_type,
    COUNT(ST_GeometryType(geometry)) AS type_count,
    ST_SRID(geometry) AS coordinate_system,
    ROUND(ST_XMin(ST_Extent(geometry))::NUMERIC, 4) AS min_longitude,
    ROUND(ST_XMax(ST_Extent(geometry))::NUMERIC, 4) AS max_longitude,
    ROUND(ST_YMin(ST_Extent(geometry))::NUMERIC, 4) AS min_latitude,
    ROUND(ST_YMax(ST_Extent(geometry))::NUMERIC, 4) AS max_latitude,
    (SELECT ST_AsText(geometry) FROM facilities LIMIT 1) AS sample_geometry_wkt

FROM facilities
GROUP BY ST_GeometryType(geometry), ST_SRID(geometry)

ORDER BY dataset_name, geometry_type;

-- ===================================================================
-- EXPECTED RESULTS:
-- You should see three different geometry types:
-- - ST_MultiPolygon (protected areas - complex boundary shapes)
-- - ST_MultiLineString (transportation - roads and trails)
-- - ST_Point (facilities - specific locations)
--
-- All geometries should be in EPSG:4326 (WGS84 geographic coordinates)
-- Coordinates should be in longitude/latitude format for Colorado region
-- ===================================================================

-- KEY POSTGIS FUNCTIONS DEMONSTRATED:
-- ST_GeometryType() - Returns the geometry type (POINT, LINESTRING, etc.)
-- ST_SRID() - Returns the Spatial Reference System ID (coordinate system)
-- ST_AsText() - Converts geometry to Well-Known Text format for reading
-- ST_Extent() - Calculates bounding box of all geometries
-- ST_XMin/XMax/YMin/YMax() - Extract coordinates from bounding boxes

-- WHAT YOU'LL LEARN:
-- 1. How to inspect spatial data before analysis
-- 2. Understanding different geometry types in PostGIS
-- 3. Coordinate system identification (SRID)
-- 4. Spatial extent calculation for data bounds
-- 5. Converting geometries to readable text format
