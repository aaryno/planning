-- ===================================================================
-- Query 6: Aggregate Functions (2 points)
-- ===================================================================
--
-- OBJECTIVE: Calculate summary statistics using aggregate functions
--
-- TASK: Calculate the TOTAL NUMBER OF CITIES, AVERAGE POPULATION,
--       MINIMUM POPULATION, and MAXIMUM ELEVATION_FT
--       Use descriptive aliases for each calculation
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations example)
-- 2. The example calculates COUNT, AVG, MIN, MAX on weather_stations table
-- 3. You need to calculate similar statistics on the cities table:
--    - COUNT(*) for total number of cities
--    - AVG(population) for average population
--    - MIN(population) for smallest city population
--    - MAX(elevation_ft) for highest elevation
-- 4. Use descriptive aliases like 'Total Cities', 'Average Population', etc.
-- 5. Fill in the blanks below to adapt the example
--
-- EXPECTED RESULT:
-- You should see one row with four columns showing:
-- - Total number of cities in the database
-- - Average population across all cities
-- - Population of the smallest city
-- - Highest elevation among all cities
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Apply the same aggregate functions (COUNT, AVG, MIN, MAX) from the example
--       but change the table name and column names to match cities table

SELECT _________(*) AS 'Total Cities',
       _________(____________) AS 'Average Population',
       _________(____________) AS 'Minimum Population',
       _________(____________) AS 'Maximum Elevation (ft)'
FROM _____________;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ COUNT(*) to count all cities
-- ☐ AVG(population) to calculate average population
-- ☐ MIN(population) to find smallest population
-- ☐ MAX(elevation_ft) to find highest elevation
-- ☐ FROM cities (not weather_stations like the example)
-- ☐ Descriptive aliases using AS 'Description'
-- ☐ Commas between each aggregate function
-- ☐ Semicolon at the end
-- ===================================================================
