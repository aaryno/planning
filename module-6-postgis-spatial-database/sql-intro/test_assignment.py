#!/usr/bin/env python3
"""
SQL Introduction Assignment - Automated Test Suite

Tests all 10 SQL queries for correctness, syntax, and expected results.
Each query is worth 2 points for a total of 20 points.

Usage:
    python test_assignment.py -v
    pytest test_assignment.py -v --tb=short
"""

import pytest
import psycopg2
import os
import re
from pathlib import Path
from typing import List, Tuple, Any, Optional


class SQLAssignmentTester:
    """Test framework for SQL introduction assignment."""

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.assignment_dir = Path(__file__).parent

    def setup_method(self):
        """Set up database connection before each test."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'gis_intro'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASS', 'postgres'),
                port=os.getenv('DB_PORT', 5432)
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            pytest.fail(f"Database connection failed: {e}")

    def teardown_method(self):
        """Clean up database connection after each test."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_sql_file(self, filename: str) -> List[Tuple[Any, ...]]:
        """Execute SQL file and return results (only if template is completed)."""
        sql_file = self.assignment_dir / 'sql' / filename
        if not sql_file.exists():
            pytest.fail(f"SQL file not found: {filename}")

        try:
            with open(sql_file, 'r') as f:
                sql_content = f.read()

            # Check if template has been completed (no blanks remaining)
            if '_____' in sql_content or '________' in sql_content:
                pytest.skip(f"Template not completed for {filename} - contains blanks to fill in")

            # Remove comments and empty lines for execution
            sql_statements = []
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--') and not line.startswith('TODO'):
                    sql_statements.append(line)

            sql_query = ' '.join(sql_statements)

            # Skip if query is empty or just contains placeholder text
            if not sql_query or len(sql_query.strip()) < 10:
                pytest.skip(f"No executable SQL found in {filename}")

            # Execute the query
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            return results

        except psycopg2.Error as e:
            pytest.fail(f"SQL execution error in {filename}: {e}")
        except Exception as e:
            pytest.fail(f"File reading error for {filename}: {e}")

    def get_column_names(self) -> List[str]:
        """Get column names from last executed query."""
        if self.cursor.description:
            return [desc[0] for desc in self.cursor.description]
        return []


class TestSQLQueries(SQLAssignmentTester):
    """Test suite for all 10 SQL queries."""

    def test_01_basic_select(self):
        """Test Query 1: Basic SELECT statement (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '01_basic_select.sql'
        assert sql_file.exists(), "Query 1 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 1 should contain SELECT"
        assert 'FROM' in content, "Query 1 should contain FROM"
        assert 'LIMIT' in content, "Query 1 should contain LIMIT"
        assert 'CITIES' in content, "Query 1 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('01_basic_select.sql')
            columns = self.get_column_names()

            # Should return exactly 8 rows (as per new requirements)
            assert len(results) == 8, f"Expected 8 rows, got {len(results)}"

            # Should include all city columns
            expected_columns = ['city_id', 'name', 'state_code', 'population', 'latitude', 'longitude', 'elevation_ft']
            for expected_col in expected_columns:
                assert expected_col in columns, f"Missing expected column: {expected_col}"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_02_column_selection(self):
        """Test Query 2: Column selection and aliases (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '02_column_selection.sql'
        assert sql_file.exists(), "Query 2 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 2 should contain SELECT"
        assert 'AS' in content, "Query 2 should contain AS for aliases"
        assert 'FROM' in content, "Query 2 should contain FROM"
        assert 'CITIES' in content, "Query 2 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('02_column_selection.sql')
            columns = self.get_column_names()

            # Should have exactly 3 columns
            assert len(columns) == 3, f"Expected 3 columns, got {len(columns)}"

            # Check for aliases (case insensitive)
            column_names_lower = [col.lower() for col in columns]
            assert 'city name' in column_names_lower or 'name' in column_names_lower, "Missing city name column"
            assert 'state' in column_names_lower or 'state_code' in column_names_lower, "Missing state column"
            assert 'elevation' in column_names_lower, "Missing elevation column"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_03_where_clause(self):
        """Test Query 3: WHERE clause basics (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '03_where_clause.sql'
        assert sql_file.exists(), "Query 3 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 3 should contain SELECT"
        assert 'WHERE' in content, "Query 3 should contain WHERE"
        assert 'FROM' in content, "Query 3 should contain FROM"
        assert 'CITIES' in content, "Query 3 should query the cities table"
        assert '>' in content, "Query 3 should use greater than operator"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('03_where_clause.sql')

            # Should return some cities but not all (for population > 750,000)
            assert 3 <= len(results) <= 15, f"Expected 3-15 large cities, got {len(results)}"

            # Verify all returned cities have population > 750,000
            for row in results:
                population = row[2]  # Population is third column
                assert population > 750000, f"City {row[0]} has population {population}, should be > 750,000"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_04_multiple_conditions(self):
        """Test Query 4: Multiple conditions and logical operators (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '04_multiple_conditions.sql'
        assert sql_file.exists(), "Query 4 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 4 should contain SELECT"
        assert 'WHERE' in content, "Query 4 should contain WHERE"
        assert ('AND' in content or 'OR' in content), "Query 4 should contain AND or OR"
        assert 'BETWEEN' in content, "Query 4 should contain BETWEEN"
        assert 'FROM' in content, "Query 4 should contain FROM"
        assert 'CITIES' in content, "Query 4 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('04_multiple_conditions.sql')

            # Should return some cities (FL or AZ with population 200k-800k)
            assert 2 <= len(results) <= 12, f"Expected 2-12 medium cities in FL/AZ, got {len(results)}"

            # Verify all cities meet both conditions
            for row in results:
                name, state_code, population = row[0], row[1], row[2]
                # Must be FL or AZ
                assert state_code in ['FL', 'AZ'], f"City {name} is in state {state_code}, should be FL or AZ"
                # Population must be between 200,000 and 800,000
                assert 200000 <= population <= 800000, \
                    f"City {name} has population {population}, should be between 200,000 and 800,000"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_05_sorting(self):
        """Test Query 5: Sorting with ORDER BY (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '05_sorting.sql'
        assert sql_file.exists(), "Query 5 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 5 should contain SELECT"
        assert 'ORDER BY' in content, "Query 5 should contain ORDER BY"
        assert 'DESC' in content, "Query 5 should contain DESC for descending order"
        assert 'ASC' in content, "Query 5 should contain ASC for ascending order"
        assert 'FROM' in content, "Query 5 should contain FROM"
        assert 'CITIES' in content, "Query 5 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('05_sorting.sql')

            # Should return all cities
            assert len(results) >= 40, f"Expected at least 40 cities, got {len(results)}"

            # Verify sorting by elevation (descending)
            elevations = [row[2] for row in results]  # elevation_ft is third column
            for i in range(len(elevations) - 1):
                assert elevations[i] >= elevations[i + 1], \
                    f"Elevation not sorted correctly: {elevations[i]} should be >= {elevations[i + 1]}"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_06_aggregates(self):
        """Test Query 6: Aggregate functions (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '06_aggregates.sql'
        assert sql_file.exists(), "Query 6 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 6 should contain SELECT"
        assert 'COUNT' in content, "Query 6 should contain COUNT"
        assert 'AVG' in content, "Query 6 should contain AVG"
        assert 'MIN' in content, "Query 6 should contain MIN"
        assert 'MAX' in content, "Query 6 should contain MAX"
        assert 'FROM' in content, "Query 6 should contain FROM"
        assert 'CITIES' in content, "Query 6 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('06_aggregates.sql')
            columns = self.get_column_names()

            # Should return exactly 1 row with 4 aggregate values
            assert len(results) == 1, f"Expected 1 aggregate row, got {len(results)}"
            assert len(columns) == 4, f"Expected 4 aggregate columns, got {len(columns)}"

            row = results[0]
            total_cities, avg_population, min_population, max_elevation = row

            # Validate aggregate results
            assert isinstance(total_cities, int) and total_cities >= 40, \
                f"Total cities should be integer >= 40, got {total_cities}"
            assert isinstance(avg_population, (int, float)) and avg_population > 0, \
                f"Average population should be positive, got {avg_population}"
            assert isinstance(min_population, (int, float)) and min_population > 0, \
                f"Minimum population should be positive, got {min_population}"
            assert isinstance(max_elevation, (int, float)), \
                f"Maximum elevation should be numeric, got {max_elevation}"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_07_group_by(self):
        """Test Query 7: GROUP BY clause (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '07_group_by.sql'
        assert sql_file.exists(), "Query 7 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 7 should contain SELECT"
        assert 'GROUP BY' in content, "Query 7 should contain GROUP BY"
        assert 'COUNT' in content, "Query 7 should contain COUNT"
        assert 'AVG' in content, "Query 7 should contain AVG"
        assert 'ORDER BY' in content, "Query 7 should contain ORDER BY"
        assert 'FROM' in content, "Query 7 should contain FROM"
        assert 'CITIES' in content, "Query 7 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('07_group_by.sql')
            columns = self.get_column_names()

            # Should return one row per state
            assert 10 <= len(results) <= 50, f"Expected 10-50 state groups, got {len(results)}"
            assert len(columns) == 3, f"Expected 3 columns (state, count, avg), got {len(columns)}"

            # Verify each row has correct structure
            state_codes = set()
            for row in results:
                state_code, city_count, avg_elevation = row

                # Check for duplicate states (shouldn't happen with proper GROUP BY)
                assert state_code not in state_codes, f"Duplicate state code: {state_code}"
                state_codes.add(state_code)

                # Validate data types and ranges
                assert isinstance(city_count, int) and city_count >= 1, \
                    f"City count for {state_code} should be integer >= 1, got {city_count}"
                assert isinstance(avg_elevation, (int, float)), \
                    f"Average elevation for {state_code} should be numeric, got {avg_elevation}"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass

    def test_08_having_clause(self):
        """Test Query 8: HAVING clause (2 points)."""
        # Test file exists and contains required concepts
        sql_file = self.assignment_dir / 'sql' / '08_having_clause.sql'
        assert sql_file.exists(), "Query 8 SQL file not found"

        with open(sql_file, 'r') as f:
            content = f.read().upper()

        # Check for required SQL concepts
        assert 'SELECT' in content, "Query 8 should contain SELECT"
        assert 'GROUP BY' in content, "Query 8 should contain GROUP BY"
        assert 'HAVING' in content, "Query 8 should contain HAVING"
        assert 'COUNT' in content, "Query 8 should contain COUNT"
        assert 'AVG' in content, "Query 8 should contain AVG"
        assert 'ORDER BY' in content, "Query 8 should contain ORDER BY"
        assert 'FROM' in content, "Query 8 should contain FROM"
        assert 'CITIES' in content, "Query 8 should query the cities table"

        # Try to execute if template is completed
        try:
            results = self.execute_sql_file('08_having_clause.sql')

            # Should return fewer states than total (only those with >4 cities)
            assert 1 <= len(results) <= 8, f"Expected 1-8 states with >4 cities, got {len(results)}"

            # Verify all returned states have more than 4 cities
            for row in results:
                state_code, city_count, avg_population = row
                assert city_count > 4, f"State {state_code} has {city_count} cities, should be > 4"

                # Validate data types
                assert isinstance(city_count, int), f"City count should be integer, got {type(city_count)}"
                assert isinstance(avg_population, (int, float)), f"Average population should be numeric"

        except pytest.skip.Exception:
            # Template not completed - that's okay, just check syntax requirements
            pass


                next_name = results[i + 1][0]
                assert current_name <= next_name, \
                    f"Cities with same station count not sorted alphabetically: {current_name} > {next_name}"
            else:
                # Different station counts, should be descending
                assert current_count >= next_count, \
                    f"Station counts not sorted correctly: {current_count} < {next_count}"

    def test_10_complex_query(self):
        """Test Query 10: Complex query with subquery (2 points)."""
        results = self.execute_sql_file('10_complex_query.sql')
        columns = self.get_column_names()

        # Should have 3 columns: city name, population, active station count
        assert len(columns) == 3, f"Expected 3 columns, got {len(columns)}"

        # Should return some cities but not too many (above-average + active stations is restrictive)
        assert 2 <= len(results) <= 20, f"Expected 2-20 cities meeting criteria, got {len(results)}"

        # First, get the average population to validate subquery logic
        self.cursor.execute("SELECT AVG(population) FROM cities")
        avg_population = self.cursor.fetchone()[0]

        # Verify all returned cities meet both conditions
        for row in results:
            city_name, population, active_station_count = row

            # Population must be above average
            assert population > avg_population, \
                f"City {city_name} has population {population}, should be > {avg_population:.0f} (average)"

            # Must have at least 1 active station
            assert isinstance(active_station_count, int) and active_station_count >= 1, \
                f"City {city_name} should have at least 1 active station, got {active_station_count}"

        # Verify sorting by population (descending)
        populations = [row[1] for row in results]
        for i in range(len(populations) - 1):
            assert populations[i] >= populations[i + 1], \
                f"Population not sorted correctly: {populations[i]} should be >= {populations[i + 1]}"


class TestQuerySyntax(SQLAssignmentTester):
    """Test SQL syntax and required concepts in each query file."""

    def read_sql_file(self, filename: str) -> str:
        """Read SQL file content as string."""
        # Handle both sql/filename and just filename formats
        if filename.startswith('sql/'):
            sql_file = self.assignment_dir / filename
        else:
            sql_file = self.assignment_dir / 'sql' / filename
        if not sql_file.exists():
            pytest.fail(f"SQL file not found: {sql_file}")

        with open(sql_file, 'r') as f:
            return f.read().upper()

    def test_query_files_exist(self):
        """Verify all 10 SQL query files exist."""
        expected_files = [
            '01_basic_select.sql',
            '02_column_selection.sql',
            '03_where_clause.sql',
            '04_multiple_conditions.sql',
            '05_sorting.sql',
            '06_aggregates.sql',
            '07_group_by.sql',
            '08_having_clause.sql',
            '09_joins.sql',
            '10_complex_query.sql'
        ]

        for filename in expected_files:
            filepath = self.assignment_dir / 'sql' / filename
            assert filepath.exists(), f"Missing required SQL file: sql/{filename}"

    def test_syntax_requirements(self):
        """Test that each query uses required SQL concepts."""

        # Query 1: Should use SELECT, FROM, LIMIT
        content = self.read_sql_file('sql/01_basic_select.sql')
        assert 'SELECT' in content and 'FROM' in content and 'LIMIT' in content

        # Query 2: Should use AS for aliases
        content = self.read_sql_file('sql/02_column_selection.sql')
        assert 'AS' in content

        # Query 3: Should use WHERE
        content = self.read_sql_file('sql/03_where_clause.sql')
        assert 'WHERE' in content

        # Query 4: Should use AND/OR and BETWEEN or IN
        content = self.read_sql_file('sql/04_multiple_conditions.sql')
        assert ('AND' in content or 'OR' in content) and ('BETWEEN' in content or 'IN' in content)

        # Query 5: Should use ORDER BY
        content = self.read_sql_file('sql/05_sorting.sql')
        assert 'ORDER BY' in content

        # Query 6: Should use aggregate functions
        content = self.read_sql_file('sql/06_aggregates.sql')
        aggregates = ['COUNT', 'AVG', 'MIN', 'MAX', 'SUM']
        assert any(agg in content for agg in aggregates)

        # Query 7: Should use GROUP BY
        content = self.read_sql_file('sql/07_group_by.sql')
        assert 'GROUP BY' in content

        # Query 8: Should use HAVING
        content = self.read_sql_file('sql/08_having_clause.sql')
        assert 'HAVING' in content

        # Query 9: Should use JOIN
        content = self.read_sql_file('sql/09_joins.sql')
        assert 'JOIN' in content

        # Query 10: Should use subquery (parentheses with SELECT)
        content = self.read_sql_file('sql/10_complex_query.sql')
        assert '(SELECT' in content or '( SELECT' in content


if __name__ == '__main__':
    # Run tests when script is executed directly
    pytest.main([__file__, '-v', '--tb=short'])
