-- ===================================================================
-- Query 9: Basic JOIN Operations (2 points)
-- ===================================================================
--
-- OBJECTIVE: Combine data from multiple tables using JOIN operations
--
-- TASK: Join CITIES and WEATHER_STATIONS tables to show CITY NAME, STATE_CODE,
--       and COUNT OF STATIONS per city. Only include cities that ACTUALLY HAVE
--       weather stations (use INNER JOIN).
--       Use aliases: 'City Name', 'State', 'Number of Stations'
--       Sort by number of stations (most stations first), then by city name
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows individual station details)
-- 2. Your task is different - you need to COUNT stations per city (requires GROUP BY)
-- 3. The example shows how to JOIN cities c and weather_stations w
-- 4. The example uses ON c.city_id = w.city_id (this is the foreign key relationship)
-- 5. You need to:
--    - SELECT c.name, c.state_code, COUNT(*)
--    - FROM cities c
--    - INNER JOIN weather_stations w ON c.city_id = w.city_id
--    - GROUP BY c.city_id, c.name, c.state_code (group by city info to count stations)
--    - ORDER BY COUNT(*) DESC, c.name ASC
-- 6. Fill in the blanks below
--
-- EXPECTED RESULT:
-- You should see cities that have weather stations, showing:
-- - City name and state
-- - Count of weather stations in each city
-- Results should only include cities that actually have stations (INNER JOIN)
-- Sorted by station count (highest first), then alphabetically
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Table aliases make queries cleaner: cities c, weather_stations w
--       INNER JOIN only returns rows where both tables have matching records
--       GROUP BY is needed because you're counting stations per city

SELECT c._____________ AS 'City Name',
       c._____________ AS 'State',
       _________(*) AS 'Number of Stations'
FROM _____________ c
INNER JOIN _____________ w ON c._____________ = w._____________
GROUP BY c._____________, c._____________, c._____________
ORDER BY _________(*) _______, c._____________ _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT c.name, c.state_code, COUNT(*)
-- ☐ FROM cities c (with table alias 'c')
-- ☐ INNER JOIN weather_stations w (with table alias 'w')
-- ☐ ON c.city_id = w.city_id (foreign key relationship)
-- ☐ GROUP BY c.city_id, c.name, c.state_code (all non-aggregate columns)
-- ☐ ORDER BY COUNT(*) DESC, c.name ASC (most stations first, then alphabetical)
-- ☐ Descriptive aliases using AS 'Name'
-- ☐ Semicolon at the end
-- ===================================================================
