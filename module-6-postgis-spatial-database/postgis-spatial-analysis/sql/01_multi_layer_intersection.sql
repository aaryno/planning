-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 1
-- Multi-Layer Spatial Intersection Analysis
-- ===================================================================
--
-- OBJECTIVE: Perform complex spatial intersections between multiple
-- layers to analyze protected area coverage within watersheds
--
-- BUSINESS CONTEXT: Environmental planners need to understand how
-- protected areas are distributed across different watersheds to
-- assess conservation coverage and identify gaps in protection.
--
-- LEARNING GOALS:
-- - Master ST_Intersects() for spatial relationship queries
-- - Use ST_Intersection() to calculate overlap geometries
-- - Apply ST_Area() for precise area calculations
-- - Combine multiple spatial functions in complex workflows
--
-- POINTS: 5 (Advanced spatial intersection analysis)
-- ===================================================================

-- Your Task: Complete the multi-layer intersection analysis below
-- Find all protected areas that intersect with major river basins,
-- calculate the overlapping area, and determine what percentage
-- of each protected area falls within each watershed.

SELECT
    -- Protected area information
    pa.name AS protected_area_name,
    pa.designation AS protection_type,
    pa.area_acres AS total_protected_acres,

    -- Watershed information
    ws.name AS watershed_name,
    ws.primary_river AS main_river,

    -- TODO: Calculate the intersection geometry between protected areas and watersheds
    -- HINT: Use ST_Intersection(pa.geometry, ws.geometry)
    _____________ AS overlap_geometry,

    -- TODO: Calculate the area of overlap in acres
    -- HINT: Use ST_Area() on the intersection geometry, convert from square meters to acres
    -- CONVERSION: 1 acre = 4047 square meters
    ROUND(
        (ST_Area(ST_Transform(_____________, 3857)) / _____________)::NUMERIC,
        2
    ) AS overlap_acres,

    -- TODO: Calculate what percentage of the protected area is within this watershed
    -- HINT: (overlap_area / total_protected_area) * 100
    ROUND(
        (ST_Area(ST_Transform(_____________, 3857)) /
         ST_Area(ST_Transform(pa.geometry, 3857))) * 100,
        2
    ) AS percent_of_protected_area,

    -- TODO: Calculate what percentage of the watershed contains protected areas
    -- HINT: (overlap_area / total_watershed_area) * 100
    ROUND(
        (ST_Area(ST_Transform(_____________, 3857)) /
         ST_Area(ST_Transform(_____________, 3857))) * 100,
        2
    ) AS percent_of_watershed

FROM protected_areas pa
INNER JOIN watersheds ws ON
    -- TODO: Add the spatial intersection condition
    -- HINT: Use ST_Intersects() to find overlapping areas
    _____________

-- TODO: Filter to only show significant overlaps (more than 1000 acres)
-- HINT: Use HAVING clause with the overlap_acres calculation
WHERE ST_Area(ST_Transform(ST_Intersection(pa.geometry, ws.geometry), 3857)) / 4047 > _____________

-- TODO: Order results by overlap area (largest first)
-- HINT: Use ORDER BY with the overlap_acres calculation
ORDER BY _____________ DESC;

-- ===================================================================
-- EXPECTED RESULTS:
-- Your query should return protected areas and watersheds that have
-- significant spatial overlap, showing:
-- - Which protected areas span multiple watersheds
-- - How much of each protected area is in each watershed
-- - Conservation coverage within each major river basin
-- - Priority areas for watershed-based conservation planning
-- ===================================================================

-- KEYWORDS TO USE:
-- ST_Intersects, ST_Intersection, ST_Area, ST_Transform, INNER JOIN,
-- HAVING, ORDER BY, ROUND

-- HINTS:
-- 1. Use ST_Transform() to convert to a projected coordinate system (3857) for accurate area calculations
-- 2. Convert square meters to acres by dividing by 4047
-- 3. ST_Intersects() tests if geometries overlap (returns true/false)
-- 4. ST_Intersection() returns the actual overlapping geometry
-- 5. Filter out small overlaps to focus on significant conservation areas
