-- ===================================================================
-- Query 2: Column Selection and Aliases (2 points)
-- ===================================================================
--
-- OBJECTIVE: Learn to select specific columns and use column aliases
--
-- TASK: Select NAME, STATE_CODE, and ELEVATION_FT from the cities table
--       Use these aliases: 'City Name', 'State', and 'Elevation (feet)'
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations example)
-- 2. The example selects station_name, install_year, active with aliases
-- 3. You need to select name, state_code, elevation_ft with different aliases
-- 4. Fill in the blanks below with the correct column names and aliases
--
-- EXPECTED RESULT:
-- You should see all cities with three columns showing:
-- - "City Name" (instead of just "name")
-- - "State" (instead of "state_code")
-- - "Elevation (feet)" (instead of "elevation_ft")
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Use "column_name AS 'Alias Name'" for each column
--       Separate multiple columns with commas

SELECT _____________ AS 'City Name',
       _____________ AS 'State',
       _____________ AS 'Elevation (feet)'
FROM _____________;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT with three specific column names (not SELECT *)
-- ☐ name AS 'City Name'
-- ☐ state_code AS 'State'
-- ☐ elevation_ft AS 'Elevation (feet)'
-- ☐ FROM cities
-- ☐ Commas between each column selection
-- ☐ Semicolon at the end
-- ===================================================================
