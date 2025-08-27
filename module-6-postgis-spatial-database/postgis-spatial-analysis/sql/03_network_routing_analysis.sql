-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 3
-- Network Routing Analysis - Transportation Optimization
-- ===================================================================
--
-- OBJECTIVE: Analyze transportation network connectivity and routing
-- efficiency between facilities using advanced spatial network analysis
-- techniques without requiring specialized routing extensions.
--
-- BUSINESS CONTEXT: Park managers need to optimize transportation
-- routes for emergency services, maintenance vehicles, and visitor
-- shuttles between facilities while considering network constraints
-- and elevation changes.
--
-- LEARNING GOALS:
-- - Master ST_Length() for accurate network distance calculations
-- - Use ST_ClosestPoint() for network connection analysis
-- - Apply ST_ShortestLine() for direct routing visualization
-- - Combine linear analysis with elevation and accessibility factors
--
-- POINTS: 5 (Advanced network analysis and routing optimization)
-- ===================================================================

-- Your Task: Complete the network routing analysis below
-- Analyze transportation efficiency between facilities and identify
-- optimal routing strategies for different vehicle types and purposes.

WITH facility_pairs AS (
    -- Generate all possible facility-to-facility combinations
    SELECT
        f1.facility_id AS origin_id,
        f1.name AS origin_name,
        f1.facility_type AS origin_type,
        f1.elevation_ft AS origin_elevation,
        f1.geometry AS origin_geom,

        f2.facility_id AS destination_id,
        f2.name AS destination_name,
        f2.facility_type AS destination_type,
        f2.elevation_ft AS destination_elevation,
        f2.geometry AS destination_geom

    FROM facilities f1
    CROSS JOIN facilities f2
    WHERE f1.facility_id < f2.facility_id  -- Avoid duplicates and self-pairs
    AND f1.facility_type IN ('Visitor Center', 'Ranger Station', 'Campground')
    AND f2.facility_type IN ('Visitor Center', 'Ranger Station', 'Campground')
),

route_analysis AS (
    SELECT
        fp.*,

        -- TODO: Calculate straight-line distance between facilities
        -- HINT: Use ST_Distance() with transformed geometries for meters
        ROUND(
            (ST_Distance(
                ST_Transform(fp.origin_geom, 3857),
                ST_Transform(fp.destination_geom, 3857)
            ) / 1609.34)::NUMERIC, 2
        ) AS straight_line_miles,

        -- TODO: Calculate elevation difference between facilities
        -- HINT: Use ABS() to get absolute elevation change
        ABS(fp._____________ - fp._____________) AS elevation_change_ft,

        -- TODO: Create the shortest line geometry between facilities
        -- HINT: Use ST_ShortestLine() to connect the two points
        _____________(fp.origin_geom, fp.destination_geom) AS direct_route_geom,

        -- Find the closest transportation route to each facility
        (SELECT
            tn1.name
         FROM transportation_network tn1
         ORDER BY ST_Distance(ST_Transform(fp.origin_geom, 3857),
                              ST_Transform(tn1.geometry, 3857))
         LIMIT 1
        ) AS closest_route_to_origin,

        (SELECT
            tn2.name
         FROM transportation_network tn2
         ORDER BY ST_Distance(ST_Transform(fp.destination_geom, 3857),
                              ST_Transform(tn2.geometry, 3857))
         LIMIT 1
        ) AS closest_route_to_destination

    FROM facility_pairs fp
),

network_connectivity AS (
    SELECT
        ra.*,

        -- TODO: Find transportation routes that intersect with the direct line
        -- HINT: Use STRING_AGG() to concatenate intersecting route names
        (SELECT STRING_AGG(tn.name, ', ' ORDER BY tn.name)
         FROM transportation_network tn
         WHERE ST_Intersects(tn.geometry, ST_Buffer(ra.direct_route_geom, 0.01))
        ) AS intersecting_routes,

        -- TODO: Count how many routes intersect the direct path
        -- HINT: Use COUNT() with ST_Intersects() and a small buffer
        (SELECT COUNT(*)
         FROM transportation_network tn
         WHERE ST_Intersects(tn.geometry,
                            ST_Buffer(ra.direct_route_geom, _____________))
        ) AS route_intersections,

        -- TODO: Calculate network distance approximation
        -- HINT: Find closest points on transportation network and sum distances
        (SELECT
            ROUND(((
                -- Distance from origin to closest point on nearest route
                ST_Distance(
                    ST_Transform(ra.origin_geom, 3857),
                    ST_Transform(ST_ClosestPoint(tn1.geometry, ra.origin_geom), 3857)
                ) +
                -- Distance from destination to closest point on nearest route
                ST_Distance(
                    ST_Transform(ra.destination_geom, 3857),
                    ST_Transform(ST_ClosestPoint(tn2.geometry, ra.destination_geom), 3857)
                ) +
                -- Approximate network distance (straight-line * detour factor)
                ST_Distance(
                    ST_Transform(ra.origin_geom, 3857),
                    ST_Transform(ra.destination_geom, 3857)
                ) * 1.4  -- 40% detour factor for network routing
            ) / 1609.34)::NUMERIC, 2
        ) AS estimated_network_miles

        FROM transportation_network tn1, transportation_network tn2
        WHERE tn1.name = ra.closest_route_to_origin
        AND tn2.name = ra.closest_route_to_destination
        LIMIT 1

    FROM route_analysis ra
)

SELECT
    nc.origin_name,
    nc.origin_type,
    nc.destination_name,
    nc.destination_type,
    nc.straight_line_miles,
    nc.estimated_network_miles,

    -- TODO: Calculate routing efficiency (network vs straight-line ratio)
    -- HINT: Lower ratios indicate more direct/efficient routes
    ROUND(
        (nc.estimated_network_miles /
         CASE WHEN nc.straight_line_miles = 0 THEN 1
              ELSE nc._____________ END)::NUMERIC, 2
    ) AS routing_efficiency_ratio,

    nc.elevation_change_ft,
    nc.route_intersections,
    nc.intersecting_routes,

    -- TODO: Determine route difficulty based on distance, elevation, and network access
    -- HINT: Use CASE statement considering multiple factors
    CASE
        WHEN nc.straight_line_miles < 5
             AND nc.elevation_change_ft < 1000
             AND nc.route_intersections > 0 THEN 'Easy'
        WHEN nc.straight_line_miles < _____________
             AND nc.elevation_change_ft < 2000
             AND nc.route_intersections > 0 THEN 'Moderate'
        WHEN nc.straight_line_miles < 20
             AND nc.elevation_change_ft < 3000 THEN 'Difficult'
        ELSE 'Very Difficult'
    END AS route_difficulty,

    -- TODO: Identify priority routes for infrastructure improvement
    -- HINT: Routes with high traffic potential but poor efficiency
    CASE
        WHEN (nc.origin_type = 'Visitor Center' OR nc.destination_type = 'Visitor Center')
             AND nc.routing_efficiency_ratio > _____________
             AND nc.route_intersections < 2 THEN 'High Priority'
        WHEN nc.routing_efficiency_ratio > 2.0
             AND nc.straight_line_miles > 5 THEN 'Medium Priority'
        ELSE 'Low Priority'
    END AS improvement_priority,

    -- TODO: Calculate estimated travel time (assuming 25 mph average on network routes)
    -- HINT: Convert miles to hours, add extra time for elevation changes
    ROUND(
        (nc.estimated_network_miles / 25.0 +
         nc.elevation_change_ft / 1000.0 * 0.1  -- 6 minutes per 1000 ft elevation change
        )::NUMERIC, 2
    ) AS estimated_travel_hours

FROM network_connectivity nc

-- TODO: Filter to show only routes that need analysis
-- HINT: Focus on longer routes or those with poor network connectivity
WHERE nc.straight_line_miles > _____________
   OR nc.route_intersections = 0
   OR nc.routing_efficiency_ratio > 2.5

-- TODO: Order by improvement priority and routing efficiency
-- HINT: Show highest priority and least efficient routes first
ORDER BY
    CASE nc.improvement_priority
        WHEN 'High Priority' THEN 1
        WHEN 'Medium Priority' THEN 2
        ELSE 3
    END,
    nc._____________ DESC;

-- ===================================================================
-- EXPECTED RESULTS:
-- Your query should return facility-to-facility routing analysis showing:
-- - Transportation efficiency between key facilities
-- - Network connectivity and route intersection analysis
-- - Infrastructure improvement priorities
-- - Travel time estimates for different route types
-- - Identification of isolated facilities needing better access
-- ===================================================================

-- SUPPLEMENTAL ANALYSIS: Emergency Response Optimization
-- Uncomment and complete this query for emergency routing analysis

/*
WITH emergency_scenarios AS (
    SELECT
        f.name AS facility_name,
        f.facility_type,
        ms.name AS station_name,
        ms.monitoring_type,

        -- TODO: Calculate emergency response distance
        -- HINT: Straight-line distance for helicopter/direct response
        ROUND((ST_Distance(
            ST_Transform(f.geometry, 3857),
            ST_Transform(ms.geometry, 3857)
        ) / 1609.34)::NUMERIC, 2) AS response_distance_miles,

        -- TODO: Determine if facility can serve as emergency staging area
        -- HINT: Consider facility type and proximity to multiple monitoring stations
        CASE
            WHEN f.facility_type = 'Ranger Station'
                 AND (SELECT COUNT(*) FROM monitoring_stations ms2
                      WHERE ST_DWithin(ST_Transform(f.geometry, 3857),
                                       ST_Transform(ms2.geometry, 3857), _____________)) > 2
            THEN 'Primary Emergency Hub'
            WHEN f.facility_type IN ('Visitor Center', 'Ranger Station')
            THEN 'Secondary Emergency Hub'
            ELSE 'Support Facility'
        END AS emergency_role

    FROM facilities f
    CROSS JOIN monitoring_stations ms
    WHERE ms.monitoring_type IN ('Weather', 'Air Quality', 'Seismic')
)
SELECT * FROM emergency_scenarios
WHERE response_distance_miles < 15
ORDER BY emergency_role, response_distance_miles;
*/

-- ===================================================================
-- KEYWORDS TO USE:
-- ST_Distance, ST_ShortestLine, ST_ClosestPoint, ST_Intersects,
-- STRING_AGG, CROSS JOIN, ABS, CASE, ORDER BY, ROUND

-- HINTS:
-- 1. Network routing without pgRouting requires approximation techniques
-- 2. Use detour factors (typically 1.2-1.6) to estimate network vs straight-line distances
-- 3. Consider elevation changes in travel time calculations
-- 4. ST_Buffer() with small distances can help detect route intersections
-- 5. Emergency response often uses straight-line distances (helicopter access)
-- ===================================================================
