-- ===================================================================
-- Query 3: WHERE Clause Basics (2 points)
-- ===================================================================
--
-- OBJECTIVE: Filter data using WHERE clauses with comparison operators
--
-- TASK: Find all cities with population GREATER THAN 750,000
--       Show NAME, STATE_CODE, and POPULATION columns
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations example)
-- 2. The example finds stations where install_year > 2010
-- 3. You need to find cities where population > 750000
-- 4. The example shows station_name, install_year, active
-- 5. You need to show name, state_code, population
-- 6. Fill in the blanks below to adapt the example
--
-- EXPECTED RESULT:
-- You should see only cities with population > 750,000
-- Results should show three columns: name, state_code, population
-- Large cities like New York, Los Angeles, Chicago should appear
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Use the same structure as the README example, but change:
--       - Table name (from weather_stations to cities)
--       - Column names (name, state_code, population)
--       - WHERE condition (population > 750000)

SELECT _____________,
       _____________,
       _____________
FROM _____________
WHERE _____________ > _____________;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT with three column names: name, state_code, population
-- ☐ FROM cities (not weather_stations like the example)
-- ☐ WHERE population > 750000 (not install_year like the example)
-- ☐ Greater than operator (>)
-- ☐ No quotes around the number 750000
-- ☐ Semicolon at the end
-- ===================================================================
