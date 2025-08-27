-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 6
-- Spatial Joins and Multi-Table Analysis
-- ===================================================================
--
-- OBJECTIVE: Perform spatial joins between multiple datasets to combine
-- attributes based on geometric relationships rather than common keys.
--
-- BUSINESS CONTEXT: Spatial joins are essential for combining data from
-- different sources based on location. For example, joining facilities
-- with watersheds to determine which basin each facility drains to,
-- or joining monitoring stations with protected areas to understand
-- environmental monitoring coverage.
--
-- LEARNING GOALS:
-- - Master spatial JOIN operations using geometric relationships
-- - Combine attributes from multiple spatial tables
-- - Understand LEFT JOIN vs INNER JOIN for spatial relationships
-- - Practice complex multi-table spatial queries
--
-- POINTS: 2 (Moderate guidance - requires spatial thinking)
-- ===================================================================

-- Your Task: Complete the spatial join analysis
-- Join facilities with watersheds and protected areas to create comprehensive location profiles

-- PART A: Facilities and Their Watershed Context
-- Join each facility with the watershed it's located in
SELECT
    f.name AS facility_name,
    f.facility_type,
    f.elevation_ft,

    -- TODO: Join with watersheds using spatial relationship
    -- HINT: Use LEFT JOIN with ST_Within() or ST_Contains() in the ON clause
    w.name AS watershed_name,
    w.primary_river,
    w.drainage_area_sqmi,
    w.flow_direction,

    -- TODO: Calculate facility's distance to the watershed's main river
    -- HINT: You'll need to join transportation_network where route_type contains 'River'
    (SELECT MIN(ST_Distance(
        ST_Transform(f.geometry, 3857),
        ST_Transform(river.geometry, 3857)
    )) / 1609.34
    FROM transportation_network river
    WHERE river.route_type = _______
    AND river.name LIKE '%' || w.primary_river || '%'
    ) AS distance_to_main_river_miles,

    -- TODO: Determine if facility is in a large watershed (>20,000 sq mi)
    CASE
        WHEN w._______ > _______ THEN 'Major Watershed'
        WHEN w.drainage_area_sqmi > 10000 THEN 'Large Watershed'
        WHEN w.drainage_area_sqmi > 5000 THEN 'Medium Watershed'
        ELSE 'Small Watershed'
    END AS watershed_size_category

FROM facilities f
LEFT JOIN watersheds w ON ST_______(w.geometry, f.geometry)
WHERE f.facility_type IN ('Visitor Center', 'Ranger Station', 'Campground')

UNION ALL

-- PART B: Multi-Table Spatial Join - Facilities, Protected Areas, and Land Use
-- Create comprehensive location profiles by joining three spatial tables
SELECT
    f.name AS facility_name,
    f.facility_type,
    f.elevation_ft,

    -- TODO: Include protected area information via spatial join
    -- HINT: Some facilities may not be in protected areas - use appropriate JOIN type
    COALESCE(pa.name, 'Outside Protected Area') AS protected_area,
    COALESCE(pa.designation, 'Not Protected') AS protection_level,

    -- TODO: Include land use zone information via spatial join
    COALESCE(lz.zone_name, 'Unzoned Area') AS land_use_zone,
    COALESCE(lz.management_intensity, 'Unknown') AS management_level,
    COALESCE(lz.recreational_use, 'Unknown') AS recreation_type,

    -- TODO: Create a facility accessibility score based on multiple factors
    -- HINT: Combine elevation, protection status, and management intensity
    CASE
        WHEN f.elevation_ft > 10000 AND pa.protection_level = 'Strict Nature Reserve' THEN 'Remote - High Difficulty'
        WHEN f.elevation_ft > 8000 AND lz.management_intensity = 'Minimal' THEN 'Backcountry - Moderate Difficulty'
        WHEN pa.visitor_count_annual > 1000000 THEN 'Popular - Easy Access'
        WHEN lz.management_intensity = 'High' THEN 'Developed - Easy Access'
        ELSE 'Standard Access'
    END AS accessibility_classification

FROM facilities f
-- TODO: Add appropriate spatial joins for protected_areas and land_use_zones
-- HINT: Consider which JOIN types to use - do all facilities need to be in protected areas?
LEFT JOIN protected_areas pa ON ST_______(pa.geometry, f.geometry)
LEFT JOIN land_use_zones lz ON ST_______(lz.geometry, f.geometry)

WHERE f.capacity > _______  -- TODO: Filter for facilities with capacity > 50

UNION ALL

-- PART C: Monitoring Station Coverage Analysis via Spatial Joins
-- Join monitoring stations with facilities to analyze monitoring coverage
SELECT
    ms.name AS station_name,
    ms.monitoring_type,
    ms.elevation_ft,

    -- TODO: Find the nearest facility within 10 miles using spatial join
    -- HINT: This requires a more complex join condition with ST_DWithin()
    nearest_facility.name AS nearest_facility,
    nearest_facility.facility_type AS nearest_facility_type,
    nearest_facility.distance_miles,

    -- TODO: Count protected areas within monitoring range (15 miles)
    -- HINT: Use a subquery with COUNT() and ST_DWithin()
    (SELECT _______(*)
     FROM protected_areas pa
     WHERE ST_______(
         ST_Transform(ms.geometry, 3857),
         ST_Transform(pa.geometry, 3857),
         _______  -- 15 miles in meters
     )
    ) AS protected_areas_monitored,

    -- TODO: Determine monitoring station priority based on coverage
    CASE
        WHEN (SELECT COUNT(*)
              FROM protected_areas pa
              WHERE ST_DWithin(
                  ST_Transform(ms.geometry, 3857),
                  ST_Transform(pa.geometry, 3857),
                  24140  -- 15 miles in meters
              )) >= 3 THEN 'High Priority - Multiple Areas'
        WHEN (SELECT COUNT(*)
              FROM protected_areas pa
              WHERE ST_DWithin(
                  ST_Transform(ms.geometry, 3857),
                  ST_Transform(pa.geometry, 3857),
                  24140
              )) >= 1 THEN 'Medium Priority - Single Area'
        ELSE 'Low Priority - No Protected Areas'
    END AS monitoring_priority

FROM monitoring_stations ms
-- TODO: Complex spatial join to find nearest facility within 10 miles
JOIN LATERAL (
    SELECT f.name, f.facility_type,
           ROUND((ST_Distance(
               ST_Transform(ms.geometry, 3857),
               ST_Transform(f.geometry, 3857)
           ) / 1609.34)::NUMERIC, 2) AS distance_miles
    FROM facilities f
    WHERE ST_DWithin(
        ST_Transform(ms.geometry, 3857),
        ST_Transform(f.geometry, 3857),
        _______  -- TODO: 10 miles in meters (10 * 1609.34)
    )
    ORDER BY ST_Distance(
        ST_Transform(ms.geometry, 3857),
        ST_Transform(f.geometry, 3857)
    )
    LIMIT 1
) AS nearest_facility ON true

WHERE ms.monitoring_type IN (_______, _______)  -- TODO: Choose 'Weather', 'Air Quality'

ORDER BY facility_name, station_name;

-- ===================================================================
-- EXPECTED RESULTS:
-- PART A: Facilities with watershed information showing:
-- - Each facility matched with its containing watershed
-- - Watershed characteristics and drainage information
-- - Distance calculations to major rivers
-- - Watershed size classifications
--
-- PART B: Comprehensive facility profiles showing:
-- - Facilities with their protected area status
-- - Land use zone classifications
-- - Multi-factor accessibility assessments
-- - Some facilities may show "Outside Protected Area" or "Unzoned"
--
-- PART C: Monitoring station analysis showing:
-- - Each station with its nearest facility within 10 miles
-- - Count of protected areas within monitoring range
-- - Priority classifications based on coverage
-- ===================================================================

-- KEYWORDS TO USE:
-- JOIN, LEFT JOIN, INNER JOIN, ST_Within, ST_Contains, ST_DWithin,
-- LATERAL, COALESCE, CASE, COUNT, subqueries

-- HINTS:
-- 1. LEFT JOIN keeps all records from left table, INNER JOIN only keeps matches
-- 2. ST_DWithin(geom1, geom2, distance) tests if features are within specified distance
-- 3. LATERAL JOIN allows correlated subqueries that reference previous table columns
-- 4. COALESCE returns first non-null value - useful for handling missing spatial relationships
-- 5. Distance conversions: 10 miles = 16,093.4 meters, 15 miles = 24,140.1 meters
-- 6. Complex spatial joins may require multiple conditions in ON clause

-- SPATIAL JOIN PATTERNS:
-- Basic: FROM table1 t1 JOIN table2 t2 ON ST_Intersects(t1.geom, t2.geom)
-- Distance: FROM table1 t1 JOIN table2 t2 ON ST_DWithin(t1.geom, t2.geom, distance)
-- Nearest: Use LATERAL JOIN with ORDER BY distance and LIMIT 1
-- Multiple conditions: ON ST_Intersects(...) AND attribute_condition
