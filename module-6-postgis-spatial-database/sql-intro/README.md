# SQL Introduction - Database Fundamentals

**Course**: GIST 604B - Open Source GIS Programming  
**Module**: 6 - PostGIS Spatial Database  
**Assignment**: SQL Introduction (Foundation Level)  
**Points**: 20 (10 queries × 2 points each)  
**Time Estimate**: 3-4 hours

## 📖 Overview

This assignment introduces you to SQL (Structured Query Language) fundamentals using PostgreSQL. You'll learn essential database querying skills by working with GIS-related datasets stored in traditional relational tables. **This foundation is critical before learning PostGIS spatial functions.**

### 🎯 Learning Objectives

By completing this assignment, you will be able to:
- **Connect** to PostgreSQL databases and execute basic SQL queries
- **Write** SELECT statements to retrieve data with proper syntax
- **Filter** data using WHERE clauses with various conditions
- **Sort** query results using ORDER BY clauses
- **Calculate** summary statistics using aggregate functions (COUNT, SUM, AVG)
- **Group** data and perform aggregations using GROUP BY and HAVING
- **Join** multiple tables together to combine related data
- **Write** subqueries for complex data retrieval
- **Combine** multiple SQL concepts to answer business questions

### 🏢 Professional Context

These SQL skills are fundamental for ALL database roles and directly prepare you for:
- **GIS Database Administrator**: Managing any type of database system
- **Data Analyst**: Extracting insights from organizational databases
- **GIS Developer**: Building applications that query databases
- **Business Intelligence Specialist**: Creating reports and dashboards

**Critical Note**: Every PostGIS spatial query uses these same SQL fundamentals - you just add spatial functions on top!

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Basic understanding of tabular data (like spreadsheets)
- **No prior SQL experience required!**

### Environment Setup

1. **Start the PostgreSQL Environment**
   ```bash
   # Navigate to assignment directory
   cd sql-intro
   
   # Start PostgreSQL container
   docker-compose up -d
   
   # Verify container is running
   docker-compose ps
   ```

2. **Load Sample Data**
   ```bash
   # Load the sample datasets
   docker-compose exec postgres psql -U postgres -d gis_intro -f /docker-entrypoint-initdb.d/load_sample_data.sql
   
   # Verify data loaded successfully
   docker-compose exec postgres psql -U postgres -d gis_intro -c "\dt"
   ```

3. **Test Database Connection**
   ```bash
   # Connect to database using psql
   docker-compose exec postgres psql -U postgres -d gis_intro
   
   # Test basic query
   SELECT 'Hello, SQL!' as message;
   
   # Exit psql
   \q
   ```

---

## 📊 Dataset Overview

This assignment uses four related tables with GIS data stored as regular attributes:

### `cities` Table (50 records)
- `city_id` (integer, primary key) - Unique identifier
- `name` (text) - City name
- `state_code` (text) - 2-letter state abbreviation
- `population` (integer) - City population
- `latitude` (decimal) - Latitude coordinate
- `longitude` (decimal) - Longitude coordinate  
- `elevation_ft` (integer) - Elevation in feet

### `weather_stations` Table (75 records)
- `station_id` (integer, primary key) - Unique identifier
- `station_name` (text) - Station identifier/name
- `city_id` (integer) - Foreign key to cities table
- `latitude` (decimal) - Station latitude
- `longitude` (decimal) - Station longitude
- `install_year` (integer) - Year station was installed
- `active` (boolean) - Whether station is currently active

### `temperature_readings` Table (2,500+ records)
- `reading_id` (integer, primary key) - Unique identifier
- `station_id` (integer) - Foreign key to weather_stations
- `reading_date` (date) - Date of measurement
- `temp_high_f` (decimal) - Daily high temperature (Fahrenheit)
- `temp_low_f` (decimal) - Daily low temperature (Fahrenheit)
- `humidity_percent` (decimal) - Relative humidity percentage

### `state_info` Table (50 records)
- `state_code` (text, primary key) - 2-letter state code
- `state_name` (text) - Full state name
- `region` (text) - US geographic region
- `area_sq_miles` (integer) - State area in square miles
- `statehood_year` (integer) - Year state joined union

---

## 📝 Assignment Tasks (10 Queries × 2 Points = 20 Points)

Complete the following 10 SQL queries. Each query builds on previous concepts and is worth 2 points.

### Query 1: Basic SELECT Statement (2 points)
**File**: [`sql/01_basic_select.sql`](sql/01_basic_select.sql)

**Objective**: Write your first SQL query using basic SELECT syntax.

**Learning Example**: Here's how you would select all columns from a table:
```sql
-- Example: Show all columns from weather_stations, limited to 5 rows
SELECT *
FROM weather_stations
LIMIT 5;
```

**Your Task**: Select all columns from the **cities** table and limit results to **8 rows**.

**Keywords to Use**: `SELECT`, `FROM`, `LIMIT`
**Hint**: Replace the table name and row count from the example above.

**Complete Example Solution**:
```sql
SELECT *
FROM cities
LIMIT 10;
```

**Step-by-Step Hints**:
1. **SELECT**: Use `SELECT *` to get all columns (the asterisk means "all columns")
2. **FROM**: Use `FROM cities` to specify which table to query
3. **LIMIT**: Use `LIMIT 10` to restrict results to first 10 rows
4. **Semicolon**: Don't forget the semicolon (`;`) at the end!

**Expected Result**: You should see 10 rows with columns like city_id, name, state_code, population, latitude, longitude, elevation_ft.

**What You'll Learn**: This is the foundation of all SQL queries - every query starts with SELECT and FROM!

---

### Query 2: Column Selection and Aliases (2 points)
**File**: [`sql/02_column_selection.sql`](sql/02_column_selection.sql)

**Objective**: Learn to select specific columns and use column aliases.

**Learning Example**: Here's how you select specific columns with aliases:
```sql
-- Example: Select specific columns from weather_stations with readable names
SELECT station_name AS 'Station Name',
       install_year AS 'Year Installed',
       active AS 'Currently Active'
FROM weather_stations;
```

**Your Task**: Select **name**, **state_code**, and **elevation_ft** from the cities table. Use aliases: 'City Name', 'State', and 'Elevation (feet)'.

**Keywords to Use**: `SELECT`, `AS`, `FROM`
**Hint**: List the column names separated by commas, and use AS to create descriptive aliases.

**Complete Example Solution**:
```sql
SELECT name AS 'City Name',
       state_code AS 'State',
       population AS 'Population'
FROM cities;
```

**Step-by-Step Hints**:
1. **Specific Columns**: List column names separated by commas instead of using `*`
2. **Aliases**: Use `column_name AS 'New Name'` to create readable column headers
3. **Quotes**: Use single quotes around alias names that contain spaces
4. **Formatting**: Put each column on its own line for readability

**What to Try**: Experiment with different alias names like 'City Name', 'State Code', 'Total Population', etc.

**Expected Result**: Three columns with your custom headers showing all cities and their information.

**Why This Matters**: Column aliases make your query results more professional and easier to understand in reports.

---

### Query 3: WHERE Clause Basics (2 points)
**File**: [`sql/03_where_clause.sql`](sql/03_where_clause.sql)

**Objective**: Filter data using WHERE clauses with comparison operators.

**Learning Example**: Here's how you filter data with WHERE:
```sql
-- Example: Find weather stations installed after 2010
SELECT station_name, install_year, active
FROM weather_stations
WHERE install_year > 2010;
```

**Your Task**: Find all cities with population **greater than 750,000**, showing **name**, **state_code**, and **population**.

**Keywords to Use**: `WHERE`, `>` (greater than operator)
**Hint**: Use the same structure as the example, but change the table, columns, and filter condition.

**Complete Example Solution**:
```sql
SELECT name,
       state_code,
       population
FROM cities
WHERE population > 500000;
```

**Step-by-Step Hints**:
1. **SELECT**: Choose specific columns (name, state_code, population)
2. **WHERE**: Add `WHERE` clause after `FROM` to filter rows
3. **Comparison**: Use `>` (greater than) to find cities with population over 500,000
4. **Numbers**: Don't put quotes around numbers - use `500000` not `'500000'`

**Try These Variations**:
- `WHERE population >= 500000` (greater than or equal to)
- `WHERE population < 100000` (less than)
- `WHERE elevation_ft > 1000` (high elevation cities)

**Expected Result**: Should show major cities like New York, Los Angeles, Chicago, Houston, Phoenix, etc.

**SQL Power**: WHERE lets you find exactly the data you need instead of looking through all records!

---

### Query 4: Multiple Conditions and Logical Operators (2 points)
**File**: [`sql/04_multiple_conditions.sql`](sql/04_multiple_conditions.sql)

**Objective**: Use logical operators to combine multiple conditions.

**Learning Example**: Here's how you combine multiple conditions:
```sql
-- Example: Find active weather stations installed between 2008 and 2012
SELECT station_name, install_year, active
FROM weather_stations
WHERE active = true 
  AND install_year BETWEEN 2008 AND 2012
ORDER BY install_year;
```

**Your Task**: Find cities in **Florida (FL) OR Arizona (AZ)** with population **between 200,000 and 800,000**.

**Keywords to Use**: `WHERE`, `OR`, `BETWEEN`, `AND`
**Hint**: Use parentheses to group the OR condition: `(state_code = 'FL' OR state_code = 'AZ')`

**Complete Example Solution**:
```sql
SELECT name,
       state_code,
       population
FROM cities
WHERE (state_code = 'CA' OR state_code = 'TX')
  AND population BETWEEN 100000 AND 1000000
ORDER BY state_code, population DESC;
```

**Alternative Using IN**:
```sql
SELECT name,
       state_code,
       population
FROM cities
WHERE state_code IN ('CA', 'TX')
  AND population BETWEEN 100000 AND 1000000
ORDER BY state_code, population DESC;
```

**Step-by-Step Hints**:
1. **Parentheses**: Use `()` to group OR conditions: `(state_code = 'CA' OR state_code = 'TX')`
2. **Text Values**: Put single quotes around text: `'CA'` and `'TX'`
3. **BETWEEN**: Use `BETWEEN 100000 AND 1000000` for range filtering
4. **AND**: Use `AND` to require BOTH conditions to be true
5. **IN Alternative**: `state_code IN ('CA', 'TX')` is cleaner than multiple ORs

**Logical Operators**:
- `AND`: Both conditions must be true
- `OR`: Either condition can be true  
- `BETWEEN`: Value must be in the range (inclusive)
- `IN`: Value must match one of the listed options

**Expected Result**: Medium-sized cities in California and Texas like Sacramento, Austin, Fresno, etc.

---

### Query 5: Sorting with ORDER BY (2 points)
**File**: [`sql/05_sorting.sql`](sql/05_sorting.sql)

**Objective**: Sort query results in ascending and descending order.

**Learning Example**: Here's how you sort results:
```sql
-- Example: Sort weather stations by installation year (newest first), then by name
SELECT station_name, install_year, active
FROM weather_stations
ORDER BY install_year DESC, station_name ASC;
```

**Your Task**: List all cities sorted by **elevation_ft (highest first)**, then by **name alphabetically**.

**Keywords to Use**: `ORDER BY`, `DESC`, `ASC`
**Hint**: Use DESC for highest-to-lowest elevation, and ASC for alphabetical names.

**Complete Example Solution**:
```sql
SELECT name,
       state_code,
       population
FROM cities
ORDER BY population DESC, name ASC;
```

**Step-by-Step Hints**:
1. **ORDER BY**: Goes at the end of your query, after WHERE (if present)
2. **DESC**: Use `DESC` for descending (largest to smallest, Z to A)
3. **ASC**: Use `ASC` for ascending (smallest to largest, A to Z) - this is the default
4. **Multiple Columns**: Separate with commas - first column is primary sort, second is tiebreaker
5. **Sort Priority**: `population DESC, name ASC` means sort by population first, then by name for ties

**Try These Variations**:
```sql
-- Sort by state, then by population within each state
ORDER BY state_code ASC, population DESC;

-- Sort by elevation (highest cities first)
ORDER BY elevation_ft DESC;

-- Sort alphabetically by city name
ORDER BY name ASC;
```

**Expected Result**: New York, Los Angeles, Chicago at the top (highest population), with alphabetical names for cities with similar populations.

**Real-World Use**: Sorting is essential for reports - you almost always want your data in a logical order!

---

### Query 6: Aggregate Functions (2 points)
**File**: [`sql/06_aggregates.sql`](sql/06_aggregates.sql)

**Objective**: Calculate summary statistics using aggregate functions.

**Learning Example**: Here's how you calculate summary statistics:
```sql
-- Example: Calculate statistics about weather stations
SELECT COUNT(*) AS 'Total Stations',
       AVG(install_year) AS 'Average Install Year',
       MIN(install_year) AS 'Oldest Station Year',
       MAX(install_year) AS 'Newest Station Year'
FROM weather_stations;
```

**Your Task**: Calculate the **total number of cities**, **average population**, **minimum population**, and **maximum elevation_ft**.

**Keywords to Use**: `COUNT()`, `AVG()`, `MIN()`, `MAX()`, `AS`
**Hint**: Apply the same aggregate functions but change the column names to match the cities table.

**Complete Example Solution**:
```sql
SELECT COUNT(*) AS 'Total Cities',
       AVG(population) AS 'Average Population',
       MIN(elevation_ft) AS 'Minimum Elevation (ft)',
       MAX(elevation_ft) AS 'Maximum Elevation (ft)'
FROM cities;
```

**Step-by-Step Hints**:
1. **COUNT(*)**: Counts all rows in the table
2. **AVG()**: Calculates average of a numeric column
3. **MIN()**: Finds the smallest value
4. **MAX()**: Finds the largest value
5. **Aliases**: Use descriptive aliases to make results readable
6. **One Row Result**: Aggregate functions return just one summary row

**Other Useful Aggregates**:
```sql
-- SUM example (if you had a budget column)
SELECT SUM(population) AS 'Total Population Across All Cities';

-- COUNT with conditions
SELECT COUNT(*) AS 'Large Cities' FROM cities WHERE population > 500000;

-- Multiple stats at once
SELECT COUNT(*) AS cities,
       AVG(population) AS avg_pop,
       MIN(population) AS smallest_city,
       MAX(population) AS largest_city
FROM cities;
```

**Expected Result**: One row showing total count (~50), average population (~400,000), lowest elevation (-6 ft), highest elevation (~6,000+ ft).

**Business Value**: Aggregate functions answer "big picture" questions about your entire dataset!

---

### Query 7: GROUP BY Clause (2 points)
**File**: [`sql/07_group_by.sql`](sql/07_group_by.sql)

**Objective**: Group data and calculate aggregate statistics for each group.

**Learning Example**: Here's how you group data and calculate statistics:
```sql
-- Example: Count weather stations by state and show average installation year
SELECT c.state_code AS 'State',
       COUNT(*) AS 'Number of Stations',
       AVG(w.install_year) AS 'Average Install Year'
FROM weather_stations w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.state_code
ORDER BY AVG(w.install_year) DESC;
```

**Your Task**: Show the **number of cities** and **average elevation_ft** for each **state_code**, sorted by **average elevation (highest first)**.

**Keywords to Use**: `GROUP BY`, `COUNT()`, `AVG()`, `ORDER BY`, `DESC`
**Hint**: Group by state_code, then calculate count and average elevation for each group.

**Complete Example Solution**:
```sql
SELECT state_code AS 'State',
       COUNT(*) AS 'Number of Cities',
       AVG(population) AS 'Average Population'
FROM cities
GROUP BY state_code
ORDER BY AVG(population) ASC;
```

**Step-by-Step Hints**:
1. **GROUP BY**: Creates separate "buckets" for each unique state_code
2. **SELECT Rules**: You can only SELECT:
   - Columns in the GROUP BY clause (state_code)
   - Aggregate functions (COUNT, AVG, etc.)
3. **COUNT(*)**: Now counts cities per state instead of total cities
4. **AVG()**: Now calculates average population per state
5. **ORDER BY**: Can sort by the same aggregates used in SELECT

**Key Understanding**: 
- Without GROUP BY: Aggregates work on ALL rows (one result)
- With GROUP BY: Aggregates work on each GROUP separately (one result per group)

**Try These Variations**:
```sql
-- Group by region (need to join with state_info table later)
-- Find states with the most cities
SELECT state_code, COUNT(*) as city_count
FROM cities 
GROUP BY state_code
ORDER BY COUNT(*) DESC;

-- Average elevation by state
SELECT state_code, 
       COUNT(*) as cities,
       AVG(elevation_ft) as avg_elevation
FROM cities
GROUP BY state_code
ORDER BY AVG(elevation_ft) DESC;
```

**Expected Result**: One row per state showing state code, how many cities, and average population for that state.

**Real-World Power**: GROUP BY lets you analyze patterns - "Which states have the most large cities?" "What's the average income by department?" etc.

---

### Query 8: HAVING Clause (2 points)
**File**: [`sql/08_having_clause.sql`](sql/08_having_clause.sql)

**Objective**: Filter grouped results using HAVING clause.

**Learning Example**: Here's how you filter groups with HAVING:
```sql
-- Example: Find states with more than 2 weather stations
SELECT c.state_code AS 'State',
       COUNT(*) AS 'Number of Stations',
       AVG(w.install_year) AS 'Average Install Year'
FROM weather_stations w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.state_code
HAVING COUNT(*) > 2
ORDER BY COUNT(*) DESC;
```

**Your Task**: Find states that have **more than 4 cities**, showing **state_code**, **city count**, and **average population**.

**Keywords to Use**: `GROUP BY`, `HAVING`, `COUNT()`, `AVG()`
**Hint**: Use HAVING instead of WHERE because you're filtering groups, not individual rows.

**Complete Example Solution**:
```sql
SELECT state_code AS 'State',
       COUNT(*) AS 'Number of Cities',
       AVG(population) AS 'Average Population'
FROM cities
GROUP BY state_code
HAVING COUNT(*) > 3
ORDER BY COUNT(*) DESC;
```

**Step-by-Step Hints**:
1. **Start with GROUP BY**: Build on Query 7 by adding HAVING
2. **HAVING vs WHERE**: 
   - WHERE filters individual ROWS before grouping
   - HAVING filters GROUPS after grouping
3. **HAVING Syntax**: Use same aggregate functions as in SELECT
4. **Common Pattern**: `HAVING COUNT(*) > 3` means "groups with more than 3 items"

**CRITICAL DIFFERENCE - WHERE vs HAVING**:
```sql
-- WHERE filters cities before grouping (wrong for this task)
SELECT state_code, COUNT(*)
FROM cities  
WHERE COUNT(*) > 3  -- ❌ ERROR! Can't use COUNT in WHERE
GROUP BY state_code;

-- HAVING filters state groups after counting (correct!)
SELECT state_code, COUNT(*)
FROM cities
GROUP BY state_code
HAVING COUNT(*) > 3;  -- ✅ CORRECT! Filter groups by count
```

**SQL Execution Order**:
1. FROM cities (get the data)
2. WHERE (filter individual rows - if present)  
3. GROUP BY state_code (create groups)
4. HAVING COUNT(*) > 3 (filter groups)
5. SELECT (choose columns to display)
6. ORDER BY (sort final results)

**Try These Variations**:
```sql
-- States with high average population
HAVING AVG(population) > 500000

-- States with both many cities AND high average population  
HAVING COUNT(*) > 2 AND AVG(population) > 300000
```

**Expected Result**: Only states like CA, TX, FL that have more than 3 cities in our database.

**Business Use**: "Which departments have more than 10 employees?" "Which products have generated more than $1M in sales?" etc.

---

### Query 9: Basic JOIN Operations (2 points)
**File**: [`sql/09_joins.sql`](sql/09_joins.sql)

**Objective**: Combine data from multiple tables using JOIN operations.

**Learning Example**: Here's how you join tables:
```sql
-- Example: Join cities and weather_stations to show station details with city info
SELECT c.name AS 'City',
       c.state_code AS 'State',
       w.station_name AS 'Station Name',
       w.install_year AS 'Year Installed'
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
WHERE w.active = true
ORDER BY c.name;
```

**Your Task**: Join cities and weather_stations to show **city name**, **state_code**, and **count of stations** per city. Only include cities that **actually have weather stations**.

**Keywords to Use**: `INNER JOIN`, `GROUP BY`, `COUNT()`, `ON`
**Hint**: You'll need to GROUP BY city information to count stations per city.

**Complete Example Solution**:
```sql
SELECT c.name AS 'City Name',
       c.state_code AS 'State',
       COUNT(*) AS 'Number of Stations'
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
GROUP BY c.city_id, c.name, c.state_code
ORDER BY COUNT(*) DESC, c.name ASC;
```

**Alternative with LEFT JOIN (shows ALL cities)**:
```sql
SELECT c.name AS 'City Name',
       c.state_code AS 'State',
       COUNT(w.station_id) AS 'Number of Stations'
FROM cities c
LEFT JOIN weather_stations w ON c.city_id = w.city_id
GROUP BY c.city_id, c.name, c.state_code
ORDER BY COUNT(w.station_id) DESC, c.name ASC;
```

**Step-by-Step Hints**:
1. **Table Aliases**: Use `c` for cities, `w` for weather_stations to make query readable
2. **JOIN Condition**: `ON c.city_id = w.city_id` links tables via foreign key relationship
3. **Ambiguous Columns**: Use `c.name` and `c.state_code` to specify which table
4. **GROUP BY All**: Must include all non-aggregate SELECT columns in GROUP BY
5. **COUNT Difference**: 
   - `COUNT(*)` with INNER JOIN counts matching rows
   - `COUNT(w.station_id)` with LEFT JOIN counts actual stations (ignores NULLs)

**JOIN Types Explained**:
```sql
-- INNER JOIN: Only cities that HAVE weather stations
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id

-- LEFT JOIN: ALL cities, whether they have stations or not  
FROM cities c  
LEFT JOIN weather_stations w ON c.city_id = w.city_id
```

**Understanding the Relationship**:
- cities table has: city_id (primary key)
- weather_stations table has: city_id (foreign key pointing to cities)
- One city can have multiple weather stations
- Some cities might have no weather stations

**Try This Experiment**:
```sql
-- See the relationship without GROUP BY
SELECT c.name, c.state_code, w.station_name
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
ORDER BY c.name;
```

**Expected Result**: Cities like New York, Los Angeles, Chicago with their weather station counts. INNER JOIN shows only cities that have stations.

**Real-World Power**: JOINs let you combine related data - "customers and their orders", "employees and their departments", "products and their reviews", etc.

---

### Query 10: Complex Query with Subquery (2 points)
**File**: [`sql/10_complex_query.sql`](sql/10_complex_query.sql)

**Objective**: Combine multiple SQL concepts including subqueries to answer complex questions.

**Learning Example**: Here's how you use subqueries for complex analysis:
```sql
-- Example: Find weather stations in cities with above-average population
SELECT c.name AS 'City',
       c.population AS 'Population',
       w.station_name AS 'Station Name'
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
WHERE c.population > (SELECT AVG(population) FROM cities)
  AND w.active = true
ORDER BY c.population DESC;
```

**Your Task**: Find cities that have **above-average elevation_ft** AND have **at least one weather station** (active or inactive). Show **city name**, **elevation_ft**, and **count of total stations**.

**Keywords to Use**: Subquery with `SELECT AVG()`, `INNER JOIN`, `GROUP BY`, `WHERE`
**Hint**: Use a subquery to calculate average elevation, then join with weather_stations and group by city.

**Complete Example Solution**:
```sql
SELECT c.name AS 'City Name',
       c.population AS 'Population',
       COUNT(*) AS 'Active Stations'
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
WHERE c.population > (SELECT AVG(population) FROM cities)
  AND w.active = true
GROUP BY c.city_id, c.name, c.population
HAVING COUNT(*) >= 1
ORDER BY c.population DESC, c.name ASC;
```

**Step-by-Step Hints**:
1. **Subquery**: `(SELECT AVG(population) FROM cities)` calculates average population
2. **Complex WHERE**: Two conditions with AND:
   - Population above average (using subquery result)
   - Only active weather stations
3. **Boolean Filter**: `w.active = true` filters for active stations
4. **Multiple Concepts**: Combines JOIN, WHERE, subquery, GROUP BY, HAVING, ORDER BY

**Understanding the Subquery**:
```sql
-- The subquery runs first and returns a single number
SELECT AVG(population) FROM cities;  -- Returns something like 445000

-- Then the main query uses that number
WHERE c.population > 445000  -- (the subquery result)
```

**Alternative Approach with CTE (Common Table Expression)**:
```sql
WITH average_pop AS (
    SELECT AVG(population) as avg_population
    FROM cities
)
SELECT c.name AS 'City Name',
       c.population AS 'Population',
       COUNT(*) AS 'Active Stations'
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id
CROSS JOIN average_pop ap
WHERE c.population > ap.avg_population
  AND w.active = true
GROUP BY c.city_id, c.name, c.population
ORDER BY c.population DESC;
```

**Query Breakdown - What Each Part Does**:
1. **Subquery**: Finds average population across all cities
2. **JOIN**: Links cities to their weather stations  
3. **WHERE**: Filters for above-average cities with active stations
4. **GROUP BY**: Groups by city (since one city can have multiple stations)
5

---

## 🧪 Testing Your Solutions

### Test Individual SQL Files

Test each query individually to verify it works:

```bash
# Test Query 1
docker-compose exec postgres psql -U postgres -d gis_intro -f sql/01_basic_select.sql

# Test Query 2
docker-compose exec postgres psql -U postgres -d gis_intro -f sql/02_column_selection.sql

# Test any specific query (replace XX with query number)
docker-compose exec postgres psql -U postgres -d gis_intro -f sql/XX_query_name.sql
```

### Test All Queries at Once

```bash
# Run all queries in sequence
for file in sql/*.sql; do
  echo "Testing $file..."
  docker-compose exec postgres psql -U postgres -d gis_intro -f "$file"
done
```

### Interactive Testing

Connect to the database and test queries interactively:

```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d gis_intro

# Explore the data
SELECT * FROM cities LIMIT 3;
SELECT * FROM weather_stations LIMIT 3;

# Show table structure
\d cities
\d weather_stations

# Exit when done
\q
```

### Automated Testing and Grading

```bash
# Run automated test suite
python test_assignment.py -v

# Run grading script
python grading/calculate_grade.py

# View grade results
cat grade-report.json
```

---

## 📋 Submission Requirements

### Files to Submit
- [ ] `sql/01_basic_select.sql` - Basic SELECT statement
- [ ] `sql/02_column_selection.sql` - Column selection and aliases
- [ ] `sql/03_where_clause.sql` - WHERE clause filtering  
- [ ] `sql/04_multiple_conditions.sql` - Multiple conditions and logical operators
- [ ] `sql/05_sorting.sql` - ORDER BY sorting
- [ ] `sql/06_aggregates.sql` - Aggregate functions
- [ ] `sql/07_group_by.sql` - GROUP BY clause
- [ ] `sql/08_having_clause.sql` - HAVING clause
- [ ] `sql/09_joins.sql` - JOIN operations
- [ ] `sql/10_complex_query.sql` - Complex query with subquery

### Grading (2 points each = 20 total)

Each query is evaluated on:
- **Correctness (70%)**: Query produces expected results
- **SQL Syntax (20%)**: Proper SQL structure and formatting
- **Performance (10%)**: Query executes efficiently

### Submission Process
1. Complete all 10 SQL files
2. Test each file individually using the commands above
3. Run automated tests to verify correctness
4. Commit and push to your GitHub repository
5. Verify GitHub Actions CI/CD passes all tests

---

## 🔧 SQL Quick Reference

### Basic Query Structure
```sql
-- Comments start with double dashes
SELECT column1, column2, column3    -- What to retrieve
FROM table_name                     -- Which table
WHERE condition                     -- Filter rows (optional)
GROUP BY column                     -- Group for aggregation (optional)
HAVING group_condition              -- Filter groups (optional)
ORDER BY column ASC/DESC           -- Sort results (optional)
LIMIT number;                      -- Limit result count (optional)
```

### Common Operators
```sql
-- Comparison: =, <>, !=, <, >, <=, >=
-- Logical: AND, OR, NOT
-- Pattern: LIKE 'pattern%'
-- Range: BETWEEN value1 AND value2
-- List: IN (value1, value2, value3)
-- NULL: IS NULL, IS NOT NULL
```

### Aggregate Functions
```sql
COUNT(*)        -- Count all rows
COUNT(column)   -- Count non-null values  
SUM(column)     -- Sum numeric values
AVG(column)     -- Average of numeric values
MIN(column)     -- Minimum value
MAX(column)     -- Maximum value
```

### JOIN Syntax
```sql
-- INNER JOIN (only matching records)
SELECT c.name, w.station_name
FROM cities c
INNER JOIN weather_stations w ON c.city_id = w.city_id;

-- LEFT JOIN (all records from left table)
SELECT c.name, w.station_name  
FROM cities c
LEFT JOIN weather_stations w ON c.city_id = w.city_id;
```

---

## 🔧 Troubleshooting

### Common SQL Errors

**Syntax Error: Missing Semicolon**
```sql
-- Wrong
SELECT * FROM cities

-- Correct  
SELECT * FROM cities;
```

**Column Not Found Error**
```sql
-- Check table structure first
\d table_name

-- Verify column names match exactly (case-sensitive)
SELECT city_name FROM cities;  -- Wrong if column is 'name'
SELECT name FROM cities;       -- Correct
```

**Aggregation Error**
```sql
-- Wrong: Can't mix aggregate and non-aggregate without GROUP BY
SELECT state_code, COUNT(*) FROM cities;

-- Correct: Use GROUP BY
SELECT state_code, COUNT(*) FROM cities GROUP BY state_code;
```

### PostgreSQL Commands
```sql
\dt          -- List all tables
\d cities    -- Show table structure  
\q           -- Quit psql
\c           -- Show current database
\i file.sql  -- Execute SQL file
```

---

## 🎯 Success Criteria

After completing this assignment, you should be able to:

- [ ] Write basic SELECT statements with proper syntax
- [ ] Filter data using WHERE clauses with multiple conditions
- [ ] Sort results using ORDER BY with multiple columns
- [ ] Calculate summary statistics using aggregate functions
- [ ] Group data and filter groups appropriately
- [ ] Join related tables to combine information
- [ ] Write subqueries for complex data retrieval
- [ ] Combine multiple SQL concepts in complex queries

### Preparation for Next Assignments

This SQL foundation directly prepares you for:
- **PostGIS Basics**: Adding spatial functions (`ST_Area`, `ST_Distance`) to these SQL skills
- **Advanced Spatial Analysis**: Complex PostGIS queries building on these fundamentals
- **Professional GIS Database Work**: Essential skills for any spatial database role

### Key Insight
**Every PostGIS query starts with these SQL fundamentals!** Master SELECT, WHERE, JOIN, and GROUP BY first, then adding `ST_Area()`, `ST_Distance()`, and other spatial functions becomes much easier.

---

## 📚 Learning Resources

### Essential References
- **PostgreSQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html
- **W3Schools SQL**: https://www.w3schools.com/sql/ (great for practicing concepts)
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

### Practice Tips
1. **Start Simple**: Get each query working with basic syntax first
2. **Build Gradually**: Add complexity one piece at a time
3. **Test Frequently**: Run queries often to catch errors early
4. **Read Error Messages**: PostgreSQL provides helpful error information
5. **Use LIMIT**: Add `LIMIT 5` to test queries with large result sets

*This assignment provides the essential SQL foundation that makes all future database work - including PostGIS spatial queries - much easier to understand and master.*