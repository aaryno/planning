-- ===================================================================
-- Query 10: Complex Query with Subquery (2 points)
-- ===================================================================
--
-- OBJECTIVE: Combine multiple SQL concepts including subqueries to answer complex questions
--
-- TASK: Find cities that have ABOVE-AVERAGE ELEVATION_FT AND have AT LEAST ONE
--       weather station (active or inactive). Show CITY NAME, ELEVATION_FT, and
--       COUNT OF TOTAL STATIONS per city.
--       Use aliases: 'City Name', 'Elevation (ft)', 'Number of Stations'
--       Sort by elevation (highest first)
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows stations in above-average population cities)
-- 2. The example uses: WHERE c.population > (SELECT AVG(population) FROM cities)
-- 3. Your task is similar but different:
--    - Use WHERE c.elevation_ft > (SELECT AVG(elevation_ft) FROM cities)
--    - The example shows individual stations; you need to COUNT stations per city
--    - This means you need GROUP BY like in Query 9
-- 4. Combine these concepts:
--    - Subquery to calculate average elevation
--    - INNER JOIN to connect cities and weather_stations
--    - WHERE clause with subquery condition
--    - GROUP BY to count stations per city
--    - ORDER BY elevation (highest first)
-- 5. Fill in the blanks below
--
-- EXPECTED RESULT:
-- You should see cities that meet BOTH conditions:
-- 1. Elevation is above the average elevation of all cities
-- 2. City has at least one weather station (any type)
-- Results show: city name, elevation, count of stations
-- Sorted by elevation (highest first)
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Start with the JOIN structure from Query 9, then add the subquery WHERE condition
--       The subquery calculates average elevation: (SELECT AVG(elevation_ft) FROM cities)
--       Remember to GROUP BY city information since you're counting stations

SELECT c._____________ AS 'City Name',
       c._____________ AS 'Elevation (ft)',
       _________(*) AS 'Number of Stations'
FROM _____________ c
INNER JOIN _____________ w ON c._____________ = w._____________
WHERE c._____________ > (SELECT _________(____________) FROM _____________)
GROUP BY c._____________, c._____________, c._____________
ORDER BY c._____________ _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT c.name, c.elevation_ft, COUNT(*)
-- ☐ FROM cities c (with table alias 'c')
-- ☐ INNER JOIN weather_stations w ON c.city_id = w.city_id
-- ☐ WHERE c.elevation_ft > (SELECT AVG(elevation_ft) FROM cities)
-- ☐ Subquery in parentheses that calculates average elevation
-- ☐ GROUP BY c.city_id, c.name, c.elevation_ft (all non-aggregate columns)
-- ☐ ORDER BY c.elevation_ft DESC (highest elevation first)
-- ☐ Descriptive aliases using AS 'Name'
-- ☐ Semicolon at the end
-- ===================================================================
