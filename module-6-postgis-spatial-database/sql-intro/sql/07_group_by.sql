-- ===================================================================
-- Query 7: GROUP BY Clause (2 points)
-- ===================================================================
--
-- OBJECTIVE: Group data and calculate aggregate statistics for each group
--
-- TASK: Show the NUMBER OF CITIES and AVERAGE ELEVATION_FT for each STATE_CODE
--       Sort by AVERAGE ELEVATION (highest first)
--       Use aliases: 'State', 'Number of Cities', 'Average Elevation (ft)'
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations with JOIN)
-- 2. Your task is simpler - just group cities by state_code (no JOIN needed)
-- 3. The example shows COUNT(*) and AVG() with GROUP BY
-- 4. You need to:
--    - SELECT state_code, COUNT(*), AVG(elevation_ft)
--    - FROM cities (just one table, no JOIN)
--    - GROUP BY state_code
--    - ORDER BY AVG(elevation_ft) DESC (highest elevation states first)
-- 5. Fill in the blanks below
--
-- EXPECTED RESULT:
-- You should see one row per state showing:
-- - State code
-- - Count of cities in that state
-- - Average elevation for cities in that state
-- Results sorted with highest-elevation states first
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: GROUP BY creates separate "buckets" for each unique state_code
--       Aggregate functions (COUNT, AVG) then work within each group

SELECT _____________ AS 'State',
       _________(*) AS 'Number of Cities',
       _________(____________) AS 'Average Elevation (ft)'
FROM _____________
GROUP BY _____________
ORDER BY _________(____________) _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT state_code, COUNT(*), AVG(elevation_ft)
-- ☐ FROM cities (single table, no JOIN needed)
-- ☐ GROUP BY state_code (creates groups for each state)
-- ☐ ORDER BY AVG(elevation_ft) DESC (highest average elevation first)
-- ☐ Descriptive aliases using AS 'Name'
-- ☐ Commas between each selected item
-- ☐ Semicolon at the end
-- ===================================================================
