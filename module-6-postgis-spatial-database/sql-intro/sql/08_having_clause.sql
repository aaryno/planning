-- ===================================================================
-- Query 8: HAVING Clause (2 points)
-- ===================================================================
--
-- OBJECTIVE: Filter grouped results using HAVING clause
--
-- TASK: Find states that have MORE THAN 4 CITIES in the database
--       Show STATE_CODE, CITY COUNT, and AVERAGE POPULATION
--       Use aliases: 'State', 'Number of Cities', 'Average Population'
--       Sort by number of cities (most cities first)
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations with JOIN)
-- 2. Your task is simpler - just work with cities table (no JOIN needed)
-- 3. The example shows GROUP BY, HAVING COUNT(*) > 2, ORDER BY COUNT(*)
-- 4. You need to:
--    - SELECT state_code, COUNT(*), AVG(population)
--    - FROM cities (just one table)
--    - GROUP BY state_code
--    - HAVING COUNT(*) > 4 (only states with more than 4 cities)
--    - ORDER BY COUNT(*) DESC (most cities first)
-- 5. Fill in the blanks below
--
-- EXPECTED RESULT:
-- You should see only states that have more than 4 cities
-- Results should show: state code, count of cities, average population
-- States with 4 or fewer cities should be excluded from results
-- Results sorted with states having the most cities first
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: HAVING filters groups AFTER they are created by GROUP BY
--       WHERE filters individual rows BEFORE grouping
--       Use HAVING COUNT(*) > 4 to filter groups

SELECT _____________ AS 'State',
       _________(*) AS 'Number of Cities',
       _________(____________) AS 'Average Population'
FROM _____________
GROUP BY _____________
HAVING _________(*) > _____
ORDER BY _________(*) _______;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT state_code, COUNT(*), AVG(population)
-- ☐ FROM cities (single table, no JOIN needed)
-- ☐ GROUP BY state_code (creates groups for each state)
-- ☐ HAVING COUNT(*) > 4 (filters to states with more than 4 cities)
-- ☐ ORDER BY COUNT(*) DESC (most cities first)
-- ☐ Descriptive aliases using AS 'Name'
-- ☐ HAVING comes after GROUP BY, not WHERE
-- ☐ Semicolon at the end
-- ===================================================================
