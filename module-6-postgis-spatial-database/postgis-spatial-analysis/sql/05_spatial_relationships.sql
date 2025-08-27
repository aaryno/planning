-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 5
-- Spatial Relationships
-- ===================================================================
--
-- OBJECTIVE: Use spatial relationship functions to find features that
-- intersect, contain, or are within other features.
--
-- BUSINESS CONTEXT: Spatial relationships are fundamental for analysis
-- such as finding facilities within protected areas, transportation
-- routes that cross wilderness boundaries, or monitoring stations
-- that fall within specific watersheds.
--
-- LEARNING GOALS:
-- - Master ST_Intersects(), ST_Contains(), ST_Within()
-- - Understand spatial relationship logic and applications
-- - Practice combining spatial relationships with attribute filters
-- - Learn to count and summarize spatial relationship results
--
-- POINTS: 2 (Less guidance - moderate challenge)
-- ===================================================================

-- Your Task: Complete the spatial relationship analysis
-- Find facilities within protected areas and transportation routes that intersect watersheds

-- PART A: Facilities Within Protected Areas
-- Find all facilities that are located within any protected area
SELECT
    f.name AS facility_name,
    f.facility_type,
    f.elevation_ft,

    -- TODO: Find the name of the protected area containing this facility
    -- HINT: Use a subquery with ST_Contains() or ST_Within()
    (SELECT pa.name
     FROM protected_areas pa
     WHERE ST________(pa.geometry, f.geometry)
     LIMIT 1
    ) AS containing_protected_area,

    -- TODO: Find the designation type (National Park, Wilderness Area, etc.)
    (SELECT pa._______
     FROM protected_areas pa
     WHERE ST_Contains(pa.geometry, f.geometry)
     LIMIT 1
    ) AS protection_designation,

    -- TODO: Calculate distance to protected area boundary in miles
    -- HINT: If facility is inside, distance should be 0 or very small
    ROUND(
        (ST_Distance(
            ST_Transform(f.geometry, 3857),
            ST_Transform((SELECT ST_Boundary(pa.geometry)
                         FROM protected_areas pa
                         WHERE ST_Contains(pa.geometry, f.geometry)
                         LIMIT 1), 3857)
        ) / _______)::NUMERIC, 2
    ) AS distance_to_boundary_miles

FROM facilities f
WHERE EXISTS (
    SELECT 1 FROM protected_areas pa
    WHERE ST________(pa.geometry, f.geometry)  -- TODO: Choose appropriate relationship function
)

UNION ALL

-- PART B: Transportation Routes Crossing Watersheds
-- Find transportation routes that intersect with watershed boundaries
SELECT
    tn.name AS route_name,
    tn.route_type,
    tn.length_miles,

    -- TODO: Count how many watersheds this route crosses
    -- HINT: Use a subquery with COUNT() and ST_Intersects()
    (SELECT _______(*)
     FROM watersheds w
     WHERE ST________(tn.geometry, w.geometry)
    ) AS watersheds_crossed,

    -- TODO: List the names of watersheds this route crosses
    -- HINT: Use STRING_AGG() to combine multiple watershed names
    (SELECT _______(w.name, ', ')
     FROM watersheds w
     WHERE ST_Intersects(tn.geometry, w.geometry)
    ) AS watershed_names,

    -- TODO: Determine if this route crosses a major river basin
    -- HINT: Use CASE with drainage_area_sqmi > 20000 as "major"
    CASE
        WHEN EXISTS (
            SELECT 1 FROM watersheds w
            WHERE ST_Intersects(tn.geometry, w.geometry)
            AND w._______ > _______
        ) THEN 'Major Basin Route'
        WHEN EXISTS (
            SELECT 1 FROM watersheds w
            WHERE ST_Intersects(tn.geometry, w.geometry)
        ) THEN 'Minor Basin Route'
        ELSE 'No Basin Crossing'
    END AS basin_classification

FROM transportation_network tn
WHERE tn.route_type IN (_______, _______)  -- TODO: Choose 'Interstate Highway', 'US Highway'

UNION ALL

-- PART C: Monitoring Stations and Land Use Analysis
-- Find monitoring stations within specific land use zones
SELECT
    ms.name AS station_name,
    ms.monitoring_type,
    ms.elevation_ft,

    -- TODO: Find the land use zone containing this station
    (SELECT lz._______
     FROM land_use_zones lz
     WHERE ST________(lz.geometry, ms.geometry)
     LIMIT 1
    ) AS land_use_zone,

    -- TODO: Get the management intensity of the containing zone
    (SELECT lz._______
     FROM land_use_zones lz
     WHERE ST_Contains(lz.geometry, ms.geometry)
     LIMIT 1
    ) AS management_intensity,

    -- TODO: Check if station is in a high elevation zone (>9000 ft elevation range)
    -- HINT: Parse elevation_range_ft field or use elevation_ft > 9000
    CASE
        WHEN ms._______ > _______ THEN 'High Elevation Station'
        WHEN ms.elevation_ft > 7000 THEN 'Medium Elevation Station'
        ELSE 'Low Elevation Station'
    END AS elevation_category

FROM monitoring_stations ms
WHERE EXISTS (
    SELECT 1 FROM land_use_zones lz
    WHERE ST________(lz.geometry, ms.geometry)
)

-- TODO: Order all results by facility/route/station name
ORDER BY _______,  _______,  _______;

-- ===================================================================
-- EXPECTED RESULTS:
-- PART A: Facilities within protected areas showing:
-- - Facility names and types inside protected boundaries
-- - Which protected area contains each facility
-- - Distance to boundary (should be 0 or very small for contained facilities)
--
-- PART B: Transportation routes crossing watersheds showing:
-- - Route names and how many watersheds they cross
-- - Names of watersheds each route intersects
-- - Classification as major or minor basin routes
--
-- PART C: Monitoring stations within land use zones showing:
-- - Station names and their containing land use zones
-- - Management intensity levels
-- - Elevation classifications
-- ===================================================================

-- KEYWORDS TO USE:
-- ST_Intersects, ST_Contains, ST_Within, ST_Boundary, EXISTS,
-- COUNT, STRING_AGG, CASE, subqueries

-- HINTS:
-- 1. ST_Contains(A, B) - A contains B
-- 2. ST_Within(A, B) - A is within B (opposite of contains)
-- 3. ST_Intersects(A, B) - A and B overlap or touch
-- 4. EXISTS is efficient for checking if relationships exist
-- 5. Use subqueries to get related attribute information
-- 6. STRING_AGG combines multiple text values with a separator
-- 7. ST_Boundary() gets the border/edge of a polygon

-- SPATIAL RELATIONSHIP LOGIC:
-- - Contains: Polygon completely surrounds a point/feature
-- - Within: Point/feature is completely inside a polygon
-- - Intersects: Features overlap, touch, or one contains the other
-- - Use appropriate relationship for your analysis goal
