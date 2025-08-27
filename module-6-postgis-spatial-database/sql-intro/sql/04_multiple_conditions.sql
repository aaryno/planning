-- ===================================================================
-- Query 4: Multiple Conditions and Logical Operators (2 points)
-- ===================================================================
--
-- OBJECTIVE: Use logical operators to combine multiple conditions
--
-- TASK: Find cities in FLORIDA (FL) OR ARIZONA (AZ) with population
--       BETWEEN 200,000 AND 800,000
--       Show NAME, STATE_CODE, and POPULATION columns
--
-- INSTRUCTIONS:
-- 1. Review the Learning Example in README.md (shows weather_stations example)
-- 2. The example finds active stations with install_year BETWEEN 2008 AND 2012
-- 3. You need to find cities where:
--    - State is FL OR AZ (use parentheses to group the OR condition)
--    - AND population is between 200,000 and 800,000
-- 4. Fill in the blanks below to create your query
--
-- EXPECTED RESULT:
-- You should see cities from Florida or Arizona that have populations
-- in the range of 200,000 to 800,000 (medium-sized cities)
-- Should include cities like Tampa, Tucson, etc.
--
-- ===================================================================

-- TODO: Complete the SQL query below
-- HINT: Use parentheses to group OR conditions: (state_code = 'FL' OR state_code = 'AZ')
--       Then add AND population BETWEEN 200000 AND 800000
--       Remember: text values need quotes, numbers don't

SELECT _____________,
       _____________,
       _____________
FROM _____________
WHERE (_____________ = '_____' OR _____________ = '_____')
  AND _____________ BETWEEN _____________ AND _____________;

-- ===================================================================
-- CHECKLIST - Your query should include:
-- ☐ SELECT name, state_code, population
-- ☐ FROM cities
-- ☐ WHERE with parentheses around the OR condition
-- ☐ state_code = 'FL' OR state_code = 'AZ' (with quotes around state codes)
-- ☐ AND population BETWEEN 200000 AND 800000 (no quotes around numbers)
-- ☐ Proper use of parentheses to group conditions
-- ☐ Semicolon at the end
-- ===================================================================
