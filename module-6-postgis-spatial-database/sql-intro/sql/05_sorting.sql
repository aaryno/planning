-- ===================================================================
-- Query 5: Sorting with ORDER BY (2 points)
-- ===================================================================
--
-- OBJECTIVE: Sort query results in ascending and descending order
--
-- TASK: List all cities sorted by ELEVATION_FT (highest first),
--       then by NAME alphabetically for cities with same elevation
--       Show NAME, STATE_CODE, and ELEVATION_FT columns
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations example)
-- 2. The example sorts by install_year DESC, station_name ASC
-- 3. You need to sort by elevation_ft DESC, name ASC
-- 4. The example shows station_name, install_year, active columns
-- 5. You need to show name, state_code, elevation_ft columns
-- 6. Fill in the blanks below to adapt the example
--
-- EXPECTED RESULT:
-- You should see all cities with highest elevation cities first
-- (like Colorado Springs, Denver) and when cities have similar
-- elevations, they should be sorted alphabetically by name
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Use ORDER BY elevation_ft DESC, name ASC
--       DESC = highest to lowest elevation
--       ASC = alphabetical order (A to Z)

SELECT _____________,
       _____________,
       _____________
FROM _____________
ORDER BY _____________ _______, _____________ _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT name, state_code, elevation_ft (three columns)
-- ☐ FROM cities
-- ☐ ORDER BY with two sorting criteria
-- ☐ elevation_ft DESC (highest elevation first)
-- ☐ name ASC (alphabetical order for ties)
-- ☐ Comma between the two sorting criteria
-- ☐ Semicolon at the end
-- ===================================================================
