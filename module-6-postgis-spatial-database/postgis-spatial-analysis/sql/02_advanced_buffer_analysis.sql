-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 2
-- Advanced Buffer Analysis - Facility Accessibility
-- ===================================================================
--
-- OBJECTIVE: Perform advanced buffer analysis to determine facility
-- accessibility and identify underserved areas using multiple buffer
-- distances and spatial aggregation techniques.
--
-- BUSINESS CONTEXT: Park managers need to assess visitor facility
-- accessibility from transportation networks and identify areas where
-- additional facilities may be needed to improve visitor services.
--
-- LEARNING GOALS:
-- - Master ST_Buffer() with multiple distance parameters
-- - Use ST_DWithin() for efficient distance-based queries
-- - Apply ST_Union() for aggregating buffer geometries
-- - Combine buffers with spatial joins for complex analysis
--
-- POINTS: 5 (Advanced buffer operations and accessibility analysis)
-- ===================================================================

-- Your Task: Complete the advanced buffer analysis below
-- Create service areas around facilities, analyze transportation
-- accessibility, and identify gaps in facility coverage.

WITH facility_buffers AS (
    SELECT
        f.facility_id,
        f.name AS facility_name,
        f.facility_type,
        f.elevation_ft,

        -- TODO: Create a 1-mile buffer around each facility
        -- HINT: Use ST_Buffer() with geometry transformed to meters (3857)
        -- CONVERSION: 1 mile = 1609.34 meters
        ST_Transform(
            ST_Buffer(ST_Transform(f.geometry, 3857), _____________),
            4326
        ) AS service_area_1mile,

        -- TODO: Create a 5-mile buffer for extended service area
        -- HINT: 5 miles = 8046.7 meters
        ST_Transform(
            ST_Buffer(ST_Transform(f.geometry, 3857), _____________),
            4326
        ) AS service_area_5mile,

        -- Keep original facility location
        f.geometry AS facility_location

    FROM facilities f
    WHERE f.facility_type IN ('Visitor Center', 'Campground', 'Ranger Station')
),

transportation_accessibility AS (
    SELECT
        fb.facility_id,
        fb.facility_name,
        fb.facility_type,

        -- TODO: Count transportation routes within 1 mile of facility
        -- HINT: Use COUNT() with ST_Intersects() on service_area_1mile
        COUNT(CASE WHEN ST_Intersects(tn.geometry, fb._____________)
              THEN 1 END) AS routes_within_1mile,

        -- TODO: Count transportation routes within 5 miles of facility
        COUNT(CASE WHEN ST_Intersects(tn.geometry, fb._____________)
              THEN 1 END) AS routes_within_5miles,

        -- TODO: Find the closest transportation route distance
        -- HINT: Use MIN() with ST_Distance() between facility and routes
        ROUND(
            MIN(ST_Distance(
                ST_Transform(fb.facility_location, 3857),
                ST_Transform(tn.geometry, 3857)
            ))::NUMERIC / _____________, 2  -- Convert meters to miles
        ) AS closest_route_miles,

        -- Buffer geometries for further analysis
        fb.service_area_1mile,
        fb.service_area_5mile

    FROM facility_buffers fb
    CROSS JOIN transportation_network tn
    WHERE tn.route_type IN ('Interstate Highway', 'US Highway', 'Scenic Highway')
    GROUP BY fb.facility_id, fb.facility_name, fb.facility_type,
             fb.service_area_1mile, fb.service_area_5mile, fb.facility_location
)

SELECT
    ta.facility_name,
    ta.facility_type,
    ta.routes_within_1mile,
    ta.routes_within_5miles,
    ta.closest_route_miles,

    -- TODO: Calculate how many monitoring stations are served by this facility
    -- HINT: Count monitoring stations within the 5-mile service area
    (SELECT COUNT(*)
     FROM monitoring_stations ms
     WHERE ST_Intersects(ms.geometry, ta._____________)) AS stations_served,

    -- TODO: Calculate service area coverage in square miles
    -- HINT: Use ST_Area() on the 1-mile buffer, convert to square miles
    -- CONVERSION: 1 square mile = 2,589,988 square meters
    ROUND(
        (ST_Area(ST_Transform(ta.service_area_1mile, 3857)) / _____________)::NUMERIC,
        2
    ) AS service_area_sq_miles,

    -- TODO: Determine if facility has good transportation access
    -- HINT: Use CASE statement - good access = within 2 miles of major route
    CASE
        WHEN ta.closest_route_miles <= _____________ THEN 'Excellent Access'
        WHEN ta.closest_route_miles <= 5.0 THEN 'Good Access'
        WHEN ta.closest_route_miles <= 10.0 THEN 'Limited Access'
        ELSE 'Remote Location'
    END AS accessibility_rating,

    -- TODO: Calculate facility density score based on nearby facilities
    -- HINT: Count other facilities within 10 miles
    (SELECT COUNT(*) - 1  -- Subtract 1 to exclude self
     FROM facilities f2
     WHERE f2.facility_id != ta.facility_id
     AND ST_DWithin(
         ST_Transform(f2.geometry, 3857),
         ST_Transform((SELECT geometry FROM facilities WHERE facility_id = ta.facility_id), 3857),
         _____________ -- 10 miles in meters
     )) AS nearby_facilities_count

FROM transportation_accessibility ta

-- TODO: Filter to show only facilities with limited transportation access
-- HINT: Use WHERE clause with closest_route_miles > certain threshold
WHERE ta.closest_route_miles > _____________

-- TODO: Order by accessibility (most remote first)
ORDER BY ta._____________ DESC;

-- ===================================================================
-- EXPECTED RESULTS:
-- Your query should return facilities with limited transportation
-- access, showing:
-- - Transportation route accessibility within different buffer zones
-- - Service area coverage and monitoring station accessibility
-- - Facility isolation scores and accessibility ratings
-- - Priority locations for improving transportation infrastructure
-- ===================================================================

-- ADDITIONAL ANALYSIS QUERY:
-- Uncomment and complete this query to find underserved areas

/*
-- Find areas more than 10 miles from any visitor facility
SELECT
    'Underserved Area Analysis' AS analysis_type,
    ST_Area(ST_Transform(underserved_areas, 3857)) / 2589988 AS underserved_sq_miles
FROM (
    SELECT
        -- TODO: Create geometry of areas NOT covered by facility buffers
        -- HINT: Use ST_Difference() between study area and ST_Union() of buffers
        ST_Difference(
            study_area.geometry,
            ST_Union(ST_Buffer(ST_Transform(f.geometry, 3857), _____________))
        ) AS underserved_areas
    FROM
        (SELECT ST_SetSRID(ST_MakeBox2D(
            ST_Point(-109.0, 37.0),
            ST_Point(-104.0, 41.0)), 4326) AS geometry
        ) AS study_area
    CROSS JOIN facilities f
    WHERE f.facility_type = 'Visitor Center'
) AS analysis;
*/

-- ===================================================================
-- KEYWORDS TO USE:
-- ST_Buffer, ST_DWithin, ST_Intersects, ST_Distance, ST_Transform,
-- ST_Union, ST_Area, WITH, CASE, COUNT, MIN, CROSS JOIN

-- HINTS:
-- 1. Always transform to projected coordinates (3857) for accurate distance calculations
-- 2. 1 mile = 1609.34 meters, 1 square mile = 2,589,988 square meters
-- 3. Use ST_DWithin() for efficient "within distance" queries vs ST_Distance()
-- 4. Buffer operations can be expensive - consider indexing and query optimization
-- 5. Common Transportation Accessibility Standards: < 2 miles = excellent, < 5 miles = good
-- ===================================================================
