#!/usr/bin/env python3
"""
PostGIS Spatial Analysis Assignment - Automated Test Suite

Tests all 4 advanced spatial analysis queries for correctness, syntax, and expected results.
Each query is worth 5 points for a total of 20 points.

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


class PostGISSpatialAnalysisTester:
    """Test framework for PostGIS spatial analysis assignment."""

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.assignment_dir = Path(__file__).parent

    def setup_method(self):
        """Set up database connection before each test."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'spatial_analysis'),
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
        """Execute SQL file and return results."""
        sql_file = self.assignment_dir / "sql" / filename

        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_file}")

        with open(sql_file, 'r') as f:
            sql_content = f.read()

        # Remove comments and empty lines for execution
        sql_lines = []
        in_comment_block = False

        for line in sql_content.split('\n'):
            line = line.strip()

            # Handle multi-line comments
            if '/*' in line and '*/' in line:
                # Single line comment block
                continue
            elif '/*' in line:
                in_comment_block = True
                continue
            elif '*/' in line:
                in_comment_block = False
                continue
            elif in_comment_block:
                continue

            # Skip single-line comments and empty lines
            if line.startswith('--') or not line:
                continue

            sql_lines.append(line)

        sql_query = ' '.join(sql_lines)

        # Check for TODO placeholders
        if '____' in sql_query or 'TODO' in sql_query.upper():
            raise ValueError(f"Query contains unfinished TODO items or placeholder blanks (_____)")

        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"SQL execution failed: {e}")

    def validate_spatial_result(self, results: List[Tuple], expected_columns: int,
                              has_geometry: bool = False) -> None:
        """Validate spatial query results."""
        assert len(results) > 0, "Query returned no results"
        assert len(results[0]) >= expected_columns, f"Expected at least {expected_columns} columns"

        if has_geometry:
            # Check if any column contains spatial data (WKT format or binary)
            has_spatial_data = False
            for row in results[:3]:  # Check first few rows
                for col in row:
                    if col is not None and (
                        (isinstance(col, str) and any(geom_type in str(col).upper()
                         for geom_type in ['POINT', 'LINESTRING', 'POLYGON', 'MULTIPOLYGON'])) or
                        isinstance(col, (bytes, memoryview))
                    ):
                        has_spatial_data = True
                        break
                if has_spatial_data:
                    break
            assert has_spatial_data, "Query should return spatial geometry data"

    def validate_numeric_ranges(self, results: List[Tuple], column_idx: int,
                              min_val: float = None, max_val: float = None) -> None:
        """Validate numeric column ranges."""
        for row in results:
            if row[column_idx] is not None:
                value = float(row[column_idx])
                if min_val is not None:
                    assert value >= min_val, f"Value {value} below minimum {min_val}"
                if max_val is not None:
                    assert value <= max_val, f"Value {value} above maximum {max_val}"


class TestPostGISSpatialAnalysis(PostGISSpatialAnalysisTester):
    """Test cases for PostGIS spatial analysis queries."""

    def test_01_multi_layer_intersection(self):
        """Test Query 1: Multi-Layer Spatial Intersection Analysis (5 points)"""
        print("\n=== Testing Query 1: Multi-Layer Spatial Intersection ===")

        results = self.execute_sql_file("01_multi_layer_intersection.sql")

        # Validate basic structure
        self.validate_spatial_result(results, 7, has_geometry=True)

        # Check that we have meaningful intersection results
        assert len(results) >= 3, "Should find at least 3 protected area/watershed intersections"

        # Validate column structure (protected area, watershed, overlap info)
        for row in results:
            protected_area_name = row[0]
            watershed_name = row[3]
            overlap_acres = row[5]
            percent_of_protected = row[6]

            assert protected_area_name is not None, "Protected area name should not be null"
            assert watershed_name is not None, "Watershed name should not be null"
            assert isinstance(overlap_acres, (int, float)), "Overlap acres should be numeric"
            assert isinstance(percent_of_protected, (int, float)), "Percentage should be numeric"
            assert 0 <= percent_of_protected <= 100, "Percentage should be between 0-100"

        # Validate that largest overlaps come first (ordering check)
        overlap_areas = [float(row[5]) for row in results]
        assert overlap_areas == sorted(overlap_areas, reverse=True), "Results should be ordered by overlap area DESC"

        print(f"✓ Found {len(results)} protected area/watershed intersections")
        print(f"✓ Largest overlap: {max(overlap_areas):.1f} acres")

    def test_02_advanced_buffer_analysis(self):
        """Test Query 2: Advanced Buffer Analysis - Facility Accessibility (5 points)"""
        print("\n=== Testing Query 2: Advanced Buffer Analysis ===")

        results = self.execute_sql_file("02_advanced_buffer_analysis.sql")

        # Validate basic structure
        self.validate_spatial_result(results, 8)

        # Should find facilities with limited access
        assert len(results) >= 2, "Should find at least 2 facilities with limited transportation access"

        # Validate accessibility analysis results
        for row in results:
            facility_name = row[0]
            routes_1mile = row[2]
            routes_5mile = row[3]
            closest_route_miles = row[4]
            accessibility_rating = row[7]

            assert facility_name is not None, "Facility name should not be null"
            assert isinstance(routes_1mile, int), "Routes within 1 mile should be integer"
            assert isinstance(routes_5mile, int), "Routes within 5 miles should be integer"
            assert routes_5mile >= routes_1mile, "5-mile count should be >= 1-mile count"
            assert isinstance(closest_route_miles, (int, float)), "Distance should be numeric"
            assert closest_route_miles > 0, "Distance to closest route should be positive"
            assert accessibility_rating in ['Excellent Access', 'Good Access', 'Limited Access', 'Remote Location']

        # Check that results are filtered for limited access
        limited_access_count = sum(1 for row in results if row[4] > 2.0)  # closest_route_miles > 2
        assert limited_access_count >= len(results) // 2, "Most results should have limited access"

        print(f"✓ Analyzed {len(results)} facilities with limited transportation access")
        print(f"✓ Most remote facility: {max(float(row[4]) for row in results):.1f} miles from nearest route")

    def test_03_network_routing_analysis(self):
        """Test Query 3: Network Routing Analysis - Transportation Optimization (5 points)"""
        print("\n=== Testing Query 3: Network Routing Analysis ===")

        results = self.execute_sql_file("03_network_routing_analysis.sql")

        # Validate basic structure
        self.validate_spatial_result(results, 10)

        # Should find facility pairs for routing analysis
        assert len(results) >= 3, "Should find at least 3 facility pairs for routing analysis"

        # Validate routing analysis results
        routing_ratios = []
        for row in results:
            origin_name = row[0]
            destination_name = row[2]
            straight_line_miles = row[4]
            estimated_network_miles = row[5]
            routing_efficiency_ratio = row[6]
            route_difficulty = row[9]
            improvement_priority = row[10]

            assert origin_name != destination_name, "Origin and destination should be different"
            assert isinstance(straight_line_miles, (int, float)), "Straight-line distance should be numeric"
            assert isinstance(estimated_network_miles, (int, float)), "Network distance should be numeric"
            assert isinstance(routing_efficiency_ratio, (int, float)), "Efficiency ratio should be numeric"
            assert estimated_network_miles >= straight_line_miles, "Network distance should be >= straight-line"
            assert routing_efficiency_ratio >= 1.0, "Efficiency ratio should be >= 1.0"
            assert route_difficulty in ['Easy', 'Moderate', 'Difficult', 'Very Difficult']
            assert improvement_priority in ['High Priority', 'Medium Priority', 'Low Priority']

            routing_ratios.append(float(routing_efficiency_ratio))

        # Check for inefficient routes (the focus of this analysis)
        inefficient_routes = [r for r in routing_ratios if r > 2.0]
        assert len(inefficient_routes) >= 1, "Should identify at least 1 inefficient route"

        print(f"✓ Analyzed {len(results)} facility-to-facility routes")
        print(f"✓ Most inefficient route ratio: {max(routing_ratios):.2f}")

    def test_04_multi_criteria_decision_analysis(self):
        """Test Query 4: Multi-Criteria Spatial Decision Support Analysis (5 points)"""
        print("\n=== Testing Query 4: Multi-Criteria Decision Analysis ===")

        results = self.execute_sql_file("04_multi_criteria_decision_analysis.sql")

        # Validate basic structure
        self.validate_spatial_result(results, 12)

        # Should return top candidate locations (limited by LIMIT clause)
        assert len(results) >= 3, "Should return at least 3 candidate locations"
        assert len(results) <= 10, "Should limit results to top candidates"

        # Validate multi-criteria analysis results
        composite_scores = []
        for row in results:
            longitude = row[1]
            latitude = row[2]
            transport_score = row[3]
            coverage_score = row[4]
            monitoring_score = row[5]
            protected_score = row[6]
            terrain_score = row[7]
            composite_score = row[8]
            suitability = row[9]
            recommendation = row[10]

            # Validate coordinates
            assert -110 <= longitude <= -104, "Longitude should be within Colorado bounds"
            assert 36 <= latitude <= 42, "Latitude should be within Colorado bounds"

            # Validate individual scores (0-100 scale)
            for score in [transport_score, coverage_score, monitoring_score, protected_score, terrain_score]:
                assert isinstance(score, (int, float)), "Individual scores should be numeric"
                assert 0 <= score <= 100, f"Score {score} should be between 0-100"

            # Validate composite score
            assert isinstance(composite_score, (int, float)), "Composite score should be numeric"
            assert 0 <= composite_score <= 100, "Composite score should be between 0-100"

            # Validate weighted calculation (approximately)
            expected_composite = (transport_score * 0.25 + coverage_score * 0.30 +
                                monitoring_score * 0.20 + protected_score * 0.15 + terrain_score * 0.10)
            assert abs(composite_score - expected_composite) < 1.0, "Composite score calculation error"

            assert suitability in ['Excellent', 'Good', 'Fair', 'Poor'], "Invalid suitability rating"

            composite_scores.append(float(composite_score))

        # Check that results are ordered by composite score (best first)
        assert composite_scores == sorted(composite_scores, reverse=True), "Results should be ordered by composite score DESC"

        # Check that we have viable candidates (filtered results)
        viable_sites = [s for s in composite_scores if s >= 60]
        assert len(viable_sites) >= 2, "Should have at least 2 viable candidate sites"

        print(f"✓ Evaluated {len(results)} candidate locations")
        print(f"✓ Best composite score: {max(composite_scores):.1f}")
        print(f"✓ Viable sites (score ≥ 60): {len(viable_sites)}")

    def test_database_setup(self):
        """Test that PostGIS and spatial data are properly loaded."""
        print("\n=== Testing Database and PostGIS Setup ===")

        # Test PostGIS extension
        self.cursor.execute("SELECT PostGIS_Version();")
        result = self.cursor.fetchone()
        assert result is not None, "PostGIS extension not installed"
        print(f"✓ PostGIS Version: {result[0]}")

        # Test spatial data tables exist and have records
        tables = ['protected_areas', 'watersheds', 'land_use_zones',
                 'transportation_network', 'facilities', 'monitoring_stations']

        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = self.cursor.fetchone()[0]
            assert count > 0, f"Table {table} has no data"

            # Test spatial index exists
            self.cursor.execute(f"""
                SELECT COUNT(*) FROM pg_indexes
                WHERE tablename = '{table}' AND indexname LIKE '%geom%'
            """)
            spatial_index = self.cursor.fetchone()[0]
            assert spatial_index > 0, f"No spatial index found for {table}"

            print(f"✓ {table}: {count} records with spatial index")

    def test_spatial_functions_available(self):
        """Test that required PostGIS functions are available."""
        print("\n=== Testing PostGIS Functions ===")

        functions_to_test = [
            'ST_Intersects', 'ST_Intersection', 'ST_Area', 'ST_Buffer',
            'ST_Distance', 'ST_DWithin', 'ST_Transform', 'ST_ShortestLine',
            'ST_ClosestPoint', 'ST_Union', 'ST_MakePoint', 'ST_Centroid'
        ]

        for func in functions_to_test:
            self.cursor.execute(f"SELECT proname FROM pg_proc WHERE proname = '{func.lower()}' LIMIT 1;")
            result = self.cursor.fetchone()
            assert result is not None, f"PostGIS function {func} not available"

        print(f"✓ All {len(functions_to_test)} required PostGIS functions are available")

    def test_coordinate_systems(self):
        """Test that required coordinate systems are available."""
        print("\n=== Testing Coordinate Systems ===")

        required_srid = [4326, 3857, 26913]  # WGS84, Web Mercator, UTM Zone 13N

        for srid in required_srid:
            self.cursor.execute("SELECT srid FROM spatial_ref_sys WHERE srid = %s;", (srid,))
            result = self.cursor.fetchone()
            assert result is not None, f"SRID {srid} not available"
            print(f"✓ SRID {srid} available")


# Pytest fixtures for running tests
@pytest.fixture(scope="session")
def tester():
    """Create a tester instance for the session."""
    return PostGISSpatialAnalysisTester()


if __name__ == "__main__":
    # Run tests directly with python test_assignment.py
    import sys

    print("PostGIS Spatial Analysis Assignment - Test Suite")
    print("=" * 60)

    tester = PostGISSpatialAnalysisTester()
    test_methods = [method for method in dir(TestPostGISSpatialAnalysis) if method.startswith('test_')]

    passed = 0
    failed = 0
    total_points = 0
    max_points = 20

    for test_method in test_methods:
        try:
            print(f"\nRunning {test_method}...")
            tester.setup_method()
            test_instance = TestPostGISSpatialAnalysis()
            test_instance.connection = tester.connection
            test_instance.cursor = tester.cursor
            test_instance.assignment_dir = tester.assignment_dir

            # Run the test
            getattr(test_instance, test_method)()

            # Award points for query tests
            if test_method.startswith('test_0') and test_method[5].isdigit():
                points = 5
                total_points += points
                print(f"✓ PASSED - {points} points awarded")
            else:
                print("✓ PASSED - Setup/validation test")

            passed += 1

        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            failed += 1
        finally:
            tester.teardown_method()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Points: {total_points}/{max_points}")
    print(f"Grade: {total_points/max_points*100:.1f}%")

    if failed > 0:
        sys.exit(1)
