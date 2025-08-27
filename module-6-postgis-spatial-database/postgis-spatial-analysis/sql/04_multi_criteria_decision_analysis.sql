-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 4
-- Multi-Criteria Spatial Decision Support Analysis
-- ===================================================================
--
-- OBJECTIVE: Implement comprehensive multi-criteria decision analysis
-- (MCDA) to identify optimal locations for new emergency response
-- facilities using weighted spatial factors and composite scoring.
--
-- BUSINESS CONTEXT: Park authorities need to establish a new emergency
-- response facility to improve visitor safety and environmental
-- monitoring response times. The location must optimize multiple
-- competing factors including accessibility, coverage, cost, and
-- operational efficiency.
--
-- LEARNING GOALS:
-- - Master weighted multi-criteria spatial analysis techniques
-- - Use ST_Centroid() and ST_ConvexHull() for geometric analysis
-- - Apply complex spatial scoring and ranking systems
-- - Combine multiple spatial relationships in decision frameworks
--
-- POINTS: 5 (Advanced multi-criteria spatial decision analysis)
-- ===================================================================

-- Your Task: Complete the multi-criteria analysis below
-- Identify the top 3 optimal locations for a new emergency response
-- facility using weighted scoring of multiple spatial criteria.

WITH analysis_grid AS (
    -- Create a grid of candidate locations across the study area
    SELECT
        row_number() OVER() AS candidate_id,
        ST_SetSRID(ST_MakePoint(
            -109.0 + (x * 0.5),    -- Longitude spacing
            37.0 + (y * 0.4)       -- Latitude spacing
        ), 4326) AS candidate_location
    FROM generate_series(0, 10) AS x,
         generate_series(0, 10) AS y
),

accessibility_scores AS (
    SELECT
        ag.candidate_id,
        ag.candidate_location,

        -- CRITERIA 1: Transportation Accessibility (Weight: 25%)
        -- TODO: Calculate average distance to major transportation routes
        -- HINT: Use AVG() with ST_Distance() to transportation network
        (SELECT AVG(ST_Distance(
            ST_Transform(ag.candidate_location, 3857),
            ST_Transform(tn.geometry, 3857)
        )) / 1609.34  -- Convert to miles
         FROM transportation_network tn
         WHERE tn.route_type IN ('Interstate Highway', 'US Highway')
        ) AS avg_transport_distance,

        -- TODO: Score transportation accessibility (closer = higher score)
        -- HINT: Use CASE to assign scores: <2 miles=100, <5=75, <10=50, >10=25
        CASE
            WHEN (SELECT AVG(ST_Distance(
                ST_Transform(ag.candidate_location, 3857),
                ST_Transform(tn.geometry, 3857)
            )) / 1609.34
             FROM transportation_network tn
             WHERE tn.route_type IN ('Interstate Highway', 'US Highway')
            ) < _____________ THEN 100
            WHEN (SELECT AVG(ST_Distance(
                ST_Transform(ag.candidate_location, 3857),
                ST_Transform(tn.geometry, 3857)
            )) / 1609.34
             FROM transportation_network tn
             WHERE tn.route_type IN ('Interstate Highway', 'US Highway')
            ) < _____________ THEN 75
            WHEN (SELECT AVG(ST_Distance(
                ST_Transform(ag.candidate_location, 3857),
                ST_Transform(tn.geometry, 3857)
            )) / 1609.34
             FROM transportation_network tn
             WHERE tn.route_type IN ('Interstate Highway', 'US Highway')
            ) < 10 THEN 50
            ELSE 25
        END AS transport_accessibility_score

    FROM analysis_grid ag
),

coverage_scores AS (
    SELECT
        asc.candidate_id,
        asc.candidate_location,
        asc.transport_accessibility_score,

        -- CRITERIA 2: Facility Coverage Gap Analysis (Weight: 30%)
        -- TODO: Calculate distance to nearest existing emergency facility
        -- HINT: Use MIN() with ST_Distance() to ranger stations
        (SELECT MIN(ST_Distance(
            ST_Transform(asc.candidate_location, 3857),
            ST_Transform(f.geometry, 3857)
        )) / 1609.34
         FROM facilities f
         WHERE f.facility_type = 'Ranger Station'
        ) AS nearest_facility_miles,

        -- TODO: Score coverage gap (larger gaps = higher priority = higher score)
        -- HINT: Inverse relationship - farther from existing = higher score
        CASE
            WHEN (SELECT MIN(ST_Distance(
                ST_Transform(asc.candidate_location, 3857),
                ST_Transform(f.geometry, 3857)
            )) / 1609.34
             FROM facilities f
             WHERE f.facility_type = 'Ranger Station'
            ) > _____________ THEN 100  -- Major coverage gap
            WHEN (SELECT MIN(ST_Distance(
                ST_Transform(asc.candidate_location, 3857),
                ST_Transform(f.geometry, 3857)
            )) / 1609.34
             FROM facilities f
             WHERE f.facility_type = 'Ranger Station'
            ) > 10 THEN 75
            WHEN (SELECT MIN(ST_Distance(
                ST_Transform(asc.candidate_location, 3857),
                ST_Transform(f.geometry, 3857)
            )) / 1609.34
             FROM facilities f
             WHERE f.facility_type = 'Ranger Station'
            ) > 5 THEN 50
            ELSE 25
        END AS coverage_gap_score

    FROM accessibility_scores asc
),

monitoring_proximity AS (
    SELECT
        cs.candidate_id,
        cs.candidate_location,
        cs.transport_accessibility_score,
        cs.coverage_gap_score,

        -- CRITERIA 3: Monitoring Station Response Coverage (Weight: 20%)
        -- TODO: Count monitoring stations within 15-mile response radius
        -- HINT: Use COUNT() with ST_DWithin() for efficient distance queries
        (SELECT COUNT(*)
         FROM monitoring_stations ms
         WHERE ST_DWithin(
            ST_Transform(cs.candidate_location, 3857),
            ST_Transform(ms.geometry, 3857),
            _____________ -- 15 miles in meters
         )
        ) AS stations_within_15miles,

        -- TODO: Score monitoring station coverage (more stations = higher score)
        -- HINT: More monitoring stations in range = higher emergency response value
        CASE
            WHEN (SELECT COUNT(*)
                 FROM monitoring_stations ms
                 WHERE ST_DWithin(
                    ST_Transform(cs.candidate_location, 3857),
                    ST_Transform(ms.geometry, 3857),
                    24140.2  -- 15 miles in meters
                 )) >= _____________ THEN 100
            WHEN (SELECT COUNT(*)
                 FROM monitoring_stations ms
                 WHERE ST_DWithin(
                    ST_Transform(cs.candidate_location, 3857),
                    ST_Transform(ms.geometry, 3857),
                    24140.2
                 )) >= 3 THEN 75
            WHEN (SELECT COUNT(*)
                 FROM monitoring_stations ms
                 WHERE ST_DWithin(
                    ST_Transform(cs.candidate_location, 3857),
                    ST_Transform(ms.geometry, 3857),
                    24140.2
                 )) >= 1 THEN 50
            ELSE 25
        END AS monitoring_coverage_score

    FROM coverage_scores cs
),

protected_area_analysis AS (
    SELECT
        mp.candidate_id,
        mp.candidate_location,
        mp.transport_accessibility_score,
        mp.coverage_gap_score,
        mp.monitoring_coverage_score,

        -- CRITERIA 4: Protected Area Service Potential (Weight: 15%)
        -- TODO: Calculate total protected area within 20-mile service radius
        -- HINT: Use ST_Area() with ST_Intersection() and SUM() for total coverage
        (SELECT COALESCE(SUM(
            ST_Area(ST_Transform(
                ST_Intersection(
                    pa.geometry,
                    ST_Buffer(ST_Transform(mp.candidate_location, 3857), _____________ ) -- 20 miles
                ), 3857
            )) / 4047  -- Convert to acres
        ), 0)
         FROM protected_areas pa
         WHERE ST_Intersects(
            pa.geometry,
            ST_Transform(ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9), 4326)
         )
        ) AS protected_acres_served,

        -- TODO: Score protected area coverage
        -- HINT: More protected area coverage = higher conservation value
        CASE
            WHEN (SELECT COALESCE(SUM(
                ST_Area(ST_Transform(
                    ST_Intersection(
                        pa.geometry,
                        ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9)
                    ), 3857
                )) / 4047
            ), 0)
             FROM protected_areas pa
             WHERE ST_Intersects(
                pa.geometry,
                ST_Transform(ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9), 4326)
             )) > _____________ THEN 100  -- Serves large protected areas
            WHEN (SELECT COALESCE(SUM(
                ST_Area(ST_Transform(
                    ST_Intersection(
                        pa.geometry,
                        ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9)
                    ), 3857
                )) / 4047
            ), 0)
             FROM protected_areas pa
             WHERE ST_Intersects(
                pa.geometry,
                ST_Transform(ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9), 4326)
             )) > 50000 THEN 75
            WHEN (SELECT COALESCE(SUM(
                ST_Area(ST_Transform(
                    ST_Intersection(
                        pa.geometry,
                        ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9)
                    ), 3857
                )) / 4047
            ), 0)
             FROM protected_areas pa
             WHERE ST_Intersects(
                pa.geometry,
                ST_Transform(ST_Buffer(ST_Transform(mp.candidate_location, 3857), 32186.9), 4326)
             )) > 10000 THEN 50
            ELSE 25
        END AS protected_area_score

    FROM monitoring_proximity mp
),

terrain_constraints AS (
    SELECT
        paa.candidate_id,
        paa.candidate_location,
        paa.transport_accessibility_score,
        paa.coverage_gap_score,
        paa.monitoring_coverage_score,
        paa.protected_area_score,

        -- CRITERIA 5: Terrain Suitability (Weight: 10%)
        -- TODO: Estimate elevation at candidate location based on nearby facilities
        -- HINT: Use weighted average of elevations from nearby facilities
        (SELECT AVG(f.elevation_ft)
         FROM facilities f
         WHERE ST_DWithin(
            ST_Transform(paa.candidate_location, 3857),
            ST_Transform(f.geometry, 3857),
            8046.7  -- Within 5 miles
         )
        ) AS estimated_elevation_ft,

        -- TODO: Score terrain suitability (moderate elevations preferred for accessibility)
        -- HINT: Very high or very low elevations have logistical challenges
        CASE
            WHEN (SELECT AVG(f.elevation_ft)
                 FROM facilities f
                 WHERE ST_DWithin(
                    ST_Transform(paa.candidate_location, 3857),
                    ST_Transform(f.geometry, 3857),
                    8046.7
                 )) BETWEEN _____________ AND _____________ THEN 100  -- Optimal elevation range
            WHEN (SELECT AVG(f.elevation_ft)
                 FROM facilities f
                 WHERE ST_DWithin(
                    ST_Transform(paa.candidate_location, 3857),
                    ST_Transform(f.geometry, 3857),
                    8046.7
                 )) BETWEEN 6000 AND 10000 THEN 75
            WHEN (SELECT AVG(f.elevation_ft)
                 FROM facilities f
                 WHERE ST_DWithin(
                    ST_Transform(paa.candidate_location, 3857),
                    ST_Transform(f.geometry, 3857),
                    8046.7
                 )) BETWEEN 5000 AND 11000 THEN 50
            ELSE 25
        END AS terrain_suitability_score

    FROM protected_area_analysis paa
    WHERE (SELECT COUNT(*) FROM facilities f
           WHERE ST_DWithin(
              ST_Transform(paa.candidate_location, 3857),
              ST_Transform(f.geometry, 3857),
              8046.7)) > 0  -- Only include locations near existing facilities
)

SELECT
    tc.candidate_id,
    ROUND(ST_X(tc.candidate_location)::NUMERIC, 4) AS longitude,
    ROUND(ST_Y(tc.candidate_location)::NUMERIC, 4) AS latitude,

    -- Individual criterion scores
    tc.transport_accessibility_score,
    tc.coverage_gap_score,
    tc.monitoring_coverage_score,
    tc.protected_area_score,
    tc.terrain_suitability_score,

    -- TODO: Calculate weighted composite score
    -- HINT: Sum of (score × weight) for each criterion
    -- Weights: Transport=25%, Coverage=30%, Monitoring=20%, Protected=15%, Terrain=10%
    ROUND(
        (tc.transport_accessibility_score * _____________ +
         tc.coverage_gap_score * _____________ +
         tc.monitoring_coverage_score * _____________ +
         tc.protected_area_score * _____________ +
         tc.terrain_suitability_score * _____________
        )::NUMERIC, 1
    ) AS composite_score,

    -- TODO: Assign priority ranking based on composite score
    -- HINT: Use CASE statement with score thresholds
    CASE
        WHEN (tc.transport_accessibility_score * 0.25 +
              tc.coverage_gap_score * 0.30 +
              tc.monitoring_coverage_score * 0.20 +
              tc.protected_area_score * 0.15 +
              tc.terrain_suitability_score * 0.10) >= _____________ THEN 'Excellent'
        WHEN (tc.transport_accessibility_score * 0.25 +
              tc.coverage_gap_score * 0.30 +
              tc.monitoring_coverage_score * 0.20 +
              tc.protected_area_score * 0.15 +
              tc.terrain_suitability_score * 0.10) >= 70 THEN 'Good'
        WHEN (tc.transport_accessibility_score * 0.25 +
              tc.coverage_gap_score * 0.30 +
              tc.monitoring_coverage_score * 0.20 +
              tc.protected_area_score * 0.15 +
              tc.terrain_suitability_score * 0.10) >= 60 THEN 'Fair'
        ELSE 'Poor'
    END AS site_suitability,

    -- TODO: Generate implementation recommendation
    -- HINT: Consider top scores and specific criterion strengths
    CASE
        WHEN tc.transport_accessibility_score >= 75 AND tc.coverage_gap_score >= 75
        THEN 'Priority Site - Immediate Development'
        WHEN tc.coverage_gap_score >= 75
        THEN 'High Need Area - Requires Infrastructure Investment'
        WHEN tc.transport_accessibility_score >= 75
        THEN 'Accessible Site - Good for Specialized Operations'
        ELSE 'Consider Alternative Locations'
    END AS implementation_recommendation

FROM terrain_constraints tc

-- TODO: Filter to show only viable candidate locations
-- HINT: Exclude locations with very low composite scores
WHERE (tc.transport_accessibility_score * 0.25 +
       tc.coverage_gap_score * 0.30 +
       tc.monitoring_coverage_score * 0.20 +
       tc.protected_area_score * 0.15 +
       tc.terrain_suitability_score * 0.10) >= _____________

-- TODO: Order by composite score (best locations first)
ORDER BY
    (tc.transport_accessibility_score * 0.25 +
     tc.coverage_gap_score * 0.30 +
     tc.monitoring_coverage_score * 0.20 +
     tc.protected_area_score * 0.15 +
     tc.terrain_suitability_score * 0.10) DESC

-- TODO: Limit to top 5 candidate locations
LIMIT _____________;

-- ===================================================================
-- EXPECTED RESULTS:
-- Your query should return the top 5 candidate locations for a new
-- emergency response facility, showing:
-- - Weighted composite scores based on multiple spatial criteria
-- - Individual criterion performance for each location
-- - Site suitability rankings and implementation recommendations
-- - Optimal locations balancing accessibility, coverage, and operational efficiency
-- ===================================================================

-- SUPPLEMENTAL ANALYSIS: Sensitivity Analysis
-- Uncomment and modify weights to test different prioritization scenarios

/*
-- Alternative weighting scenario: Conservation-focused (higher weight on protected areas)
-- Weights: Transport=20%, Coverage=25%, Monitoring=15%, Protected=30%, Terrain=10%

-- Alternative weighting scenario: Accessibility-focused (higher weight on transportation)
-- Weights: Transport=40%, Coverage=25%, Monitoring=15%, Protected=15%, Terrain=5%
*/

-- ===================================================================
-- KEYWORDS TO USE:
-- ST_MakePoint, ST_Distance, ST_DWithin, ST_Intersection, ST_Buffer,
-- ST_Area, generate_series, CASE, AVG, MIN, COUNT, SUM, COALESCE,
-- ORDER BY, LIMIT, ROUND

-- HINTS:
-- 1. Multi-criteria analysis requires normalizing different measurement scales
-- 2. Weight assignment should total 100% across all criteria
-- 3. Consider trade-offs between competing objectives (cost vs coverage)
-- 4. Validate results by testing different weight scenarios
-- 5. Real MCDA often uses more sophisticated techniques (AHP, TOPSIS)
-- ===================================================================
