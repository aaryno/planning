#!/usr/bin/env python3
"""
PostGIS Spatial Analysis Assignment - Automated Test Suite

Tests all 10 spatial analysis queries for correctness, syntax, and expected results.
Each query is worth 2 points for a total of 20 points.

Progressive difficulty structure:
- Queries 1-4: Template completion with guided examples
- Queries 5-7: Moderate challenge requiring spatial thinking
- Queries 8-10: Advanced challenges with minimal guidance

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

        # Check for incomplete work - but be lenient for progressive difficulty
        if '____' in sql_content and not any(complete_marker in sql_content.upper()
                                           for complete_marker in ['COMPLETE EXAMPLE', 'WORKING EXAMPLE']):
            # For early queries, this might be expected template work
            query_num = int(filename.split('_')[0])
            if query_num <= 4:
                raise ValueError(f"Query {query_num} template not completed - fill in the blanks (_____)")
            else:
                # For later queries, TODO items are expected but blanks suggest incomplete work
                if 'TODO' in sql_content.upper() and sql_content.count('____') > 5:
                    pytest.skip(f"Query {query_num} appears incomplete - advanced challenge not attempted")

        # Remove comments and empty lines for execution
        sql_lines = []
        in_comment_block = False

        for line in sql_content.split('\n'):
            line = line.strip()

            # Handle multi-line comments
            if '/*' in line and '*/' in line:
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

        # Skip if query is effectively empty
        if len(sql_query.strip()) < 20:
            query_num = int(filename.split('_')[0])
            if query_num <= 7:
                pytest.skip(f"Query {query_num} not implemented")
            else:
                pytest.skip(f"Advanced challenge Query {query_num} not attempted")

        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"SQL execution failed: {e}")

    def validate_spatial_result(self, results: List[Tuple], min_columns: int = 3,
                              has_geometry: bool = False) -> None:
        """Validate spatial query results."""
        assert len(results) > 0, "Query returned no results"
        assert len(results[0]) >= min_columns, f"Expected at least {min_columns} columns"

        if has_geometry:
            # Check if any column contains spatial data
            has_spatial_data = False
            for row in results[:3]:
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


class TestPostGISSpatialAnalysis(PostGISSpatialAnalysisTester):
    """Test cases for PostGIS spatial analysis queries (progressive difficulty)."""

    def test_01_spatial_inspection(self):
        """Test Query 1: Basic Spatial Data Inspection (2 points) - Complete example"""
        print("\n=== Testing Query 1: Basic Spatial Data Inspection ===")

        results = self.execute_sql_file("01_spatial_inspection.sql")

        # Should return data for 3 different datasets
        assert len(results) >= 3, "Should inspect at least 3 spatial datasets"

        # Check basic result structure
        assert len(results[0]) >= 8, "Should have comprehensive inspection columns"

        # Validate dataset information
        dataset_names = [row[0] for row in results if row[0]]
        expected_datasets = ['Protected Areas', 'Transportation Network', 'Facilities']
        found_datasets = [name for name in expected_datasets if any(name in str(dataset) for dataset in dataset_names)]
        assert len(found_datasets) >= 2, f"Should inspect expected datasets, found: {dataset_names}"

        # Check geometry types are identified
        geometry_types = [row[2] for row in results if row[2]]
        assert any('Point' in str(gt) for gt in geometry_types), "Should identify Point geometries"

        # Check coordinate systems
        coordinate_systems = [row[4] for row in results if row[4] and isinstance(row[4], int)]
        assert any(srid == 4326 for srid in coordinate_systems), "Should identify WGS84 (4326) coordinate system"

        print(f"✓ Successfully inspected {len(results)} spatial datasets")
        print(f"✓ Found geometry types: {set(str(gt) for gt in geometry_types if gt)}")

    def test_02_simple_buffers(self):
        """Test Query 2: Simple Buffer Operations (2 points) - Template completion"""
        print("\n=== Testing Query 2: Simple Buffer Operations ===")

        results = self.execute_sql_file("02_simple_buffers.sql")

        # Should return visitor centers with buffer analysis
        assert len(results) >= 1, "Should find at least 1 visitor center"

        # Check result structure
        assert len(results[0]) >= 5, "Should have facility info and buffer calculations"

        # Validate buffer calculations
        for row in results:
            facility_name = row[0]
            buffer_area = row[4] if len(row) > 4 else None
            buffer_perimeter = row[5] if len(row) > 5 else None

            assert facility_name is not None, "Facility name should not be null"

            if buffer_area is not None:
                # 1-mile buffer should be approximately π square miles (≈ 3.14)
                assert isinstance(buffer_area, (int, float)), "Buffer area should be numeric"
                assert 2.5 <= buffer_area <= 4.0, f"1-mile buffer area should be ~3.14 sq mi, got {buffer_area}"

            if buffer_perimeter is not None:
                # 1-mile buffer perimeter should be approximately 2π miles (≈ 6.28)
                assert isinstance(buffer_perimeter, (int, float)), "Buffer perimeter should be numeric"
                assert 5.5 <= buffer_perimeter <= 7.0, f"1-mile buffer perimeter should be ~6.28 miles, got {buffer_perimeter}"

        print(f"✓ Successfully created buffers for {len(results)} visitor centers")
        print(f"✓ Buffer calculations appear accurate")

    def test_03_spatial_measurements(self):
        """Test Query 3: Basic Spatial Measurements (2 points) - Guided template"""
        print("\n=== Testing Query 3: Basic Spatial Measurements ===")

        results = self.execute_sql_file("03_spatial_measurements.sql")

        # Should return measurements for ranger stations and protected areas
        assert len(results) >= 3, "Should return measurements for multiple features"

        # Check result structure
        assert len(results[0]) >= 4, "Should have comprehensive measurement columns"

        # Validate distance and area measurements
        distance_found = False
        area_found = False

        for row in results:
            # Look for distance measurements (should be positive numbers)
            if len(row) > 3 and isinstance(row[3], (int, float)) and row[3] > 0:
                distance_found = True
                distance = row[3]
                assert distance < 100, f"Distance {distance} miles seems too large for the study area"

            # Look for area measurements (should be positive numbers)
            if len(row) > 4 and isinstance(row[4], (int, float)) and row[4] > 0:
                area_found = True
                area = row[4]
                assert area < 1000, f"Area {area} sq miles seems too large for individual features"

        assert distance_found or area_found, "Should find either distance or area measurements"

        print(f"✓ Successfully calculated spatial measurements for {len(results)} features")
        print(f"✓ Distance measurements: {'found' if distance_found else 'not found'}")
        print(f"✓ Area measurements: {'found' if area_found else 'not found'}")

    def test_04_coordinate_transformations(self):
        """Test Query 4: Coordinate System Transformations (2 points) - Guided template"""
        print("\n=== Testing Query 4: Coordinate System Transformations ===")

        results = self.execute_sql_file("04_coordinate_transformations.sql")

        # Should show coordinate transformations
        assert len(results) >= 2, "Should demonstrate coordinate transformations"

        # Look for different coordinate systems
        coordinate_systems_found = []
        for row in results:
            if len(row) > 2 and isinstance(row[2], (int, float)):
                # Check for WGS84 coordinates (longitude should be negative in Colorado)
                if -110 <= row[2] <= -104:
                    coordinate_systems_found.append("WGS84")
                # Check for projected coordinates (should be much larger numbers)
                elif abs(row[2]) > 100000:
                    coordinate_systems_found.append("Projected")

        assert len(set(coordinate_systems_found)) >= 1, "Should demonstrate coordinate system transformations"

        print(f"✓ Successfully demonstrated coordinate transformations")
        print(f"✓ Coordinate systems found: {set(coordinate_systems_found)}")

    def test_05_spatial_relationships(self):
        """Test Query 5: Spatial Relationships (2 points) - Moderate challenge"""
        print("\n=== Testing Query 5: Spatial Relationships ===")

        results = self.execute_sql_file("05_spatial_relationships.sql")

        # Should find spatial relationships between features
        assert len(results) >= 2, "Should find spatial relationships between features"

        # Check for relationship analysis
        relationship_types = []
        for row in results:
            if len(row) >= 3:
                # Look for facilities within protected areas
                if 'protected' in str(row[2]).lower() or 'park' in str(row[2]).lower():
                    relationship_types.append("within_protected")
                # Look for route/watershed relationships
                elif 'watershed' in str(row[2]).lower() or 'basin' in str(row[2]).lower():
                    relationship_types.append("crosses_watershed")
                # Look for monitoring coverage
                elif 'zone' in str(row[2]).lower() or 'management' in str(row[2]).lower():
                    relationship_types.append("within_zone")

        assert len(relationship_types) >= 1, "Should identify spatial relationships"

        print(f"✓ Successfully identified spatial relationships")
        print(f"✓ Relationship types found: {set(relationship_types)}")

    def test_06_spatial_joins(self):
        """Test Query 6: Spatial Joins (2 points) - Moderate guidance"""
        print("\n=== Testing Query 6: Spatial Joins ===")

        results = self.execute_sql_file("06_spatial_joins.sql")

        # Should perform spatial joins between multiple tables
        assert len(results) >= 3, "Should perform spatial joins across multiple features"

        # Check for joined attributes from multiple tables
        multi_table_data = False
        for row in results:
            if len(row) >= 6:  # Should have attributes from multiple tables
                multi_table_data = True
                break

        assert multi_table_data, "Should combine attributes from multiple spatial tables"

        print(f"✓ Successfully performed spatial joins on {len(results)} features")

    def test_07_complex_buffer_analysis(self):
        """Test Query 7: Complex Buffer Analysis (2 points) - Minimal guidance"""
        print("\n=== Testing Query 7: Complex Buffer Analysis ===")

        try:
            results = self.execute_sql_file("07_complex_buffer_analysis.sql")

            # This is a challenging query - any meaningful result is good
            assert len(results) >= 1, "Should return some buffer analysis results"

            # Check for evidence of complex analysis
            complex_analysis = False
            for row in results:
                if len(row) >= 4:  # Multiple buffer zones or calculations
                    complex_analysis = True
                    break

            if complex_analysis:
                print(f"✓ Successfully performed complex buffer analysis")
            else:
                print(f"✓ Query executed - basic buffer analysis completed")

        except (FileNotFoundError, ValueError) as e:
            if "not implemented" in str(e).lower() or "not attempted" in str(e).lower():
                pytest.skip("Complex buffer analysis challenge not yet attempted")
            else:
                raise

    def test_08_multi_layer_intersections(self):
        """Test Query 8: Multi-Layer Intersections (2 points) - Hints only"""
        print("\n=== Testing Query 8: Multi-Layer Intersections ===")

        try:
            results = self.execute_sql_file("08_multi_layer_intersections.sql")

            # Advanced challenge - any result is success
            assert len(results) >= 1, "Should return intersection analysis results"

            print(f"✓ Successfully performed multi-layer intersection analysis")
            print(f"✓ Found {len(results)} intersection relationships")

        except (FileNotFoundError, ValueError) as e:
            if "not implemented" in str(e).lower() or "not attempted" in str(e).lower():
                pytest.skip("Multi-layer intersection challenge not yet attempted")
            else:
                raise

    def test_09_network_analysis(self):
        """Test Query 9: Network Analysis (2 points) - Problem statement only"""
        print("\n=== Testing Query 9: Network Analysis ===")

        try:
            results = self.execute_sql_file("09_network_analysis.sql")

            # This is an advanced challenge
            assert len(results) >= 1, "Should return network analysis results"

            print(f"✓ Successfully performed network analysis")
            print(f"✓ Advanced spatial analysis challenge completed")

        except (FileNotFoundError, ValueError) as e:
            if "not implemented" in str(e).lower() or "not attempted" in str(e).lower():
                pytest.skip("Network analysis challenge not yet attempted")
            else:
                raise

    def test_10_decision_analysis_challenge(self):
        """Test Query 10: Decision Analysis Challenge (2 points) - Ultimate challenge"""
        print("\n=== Testing Query 10: Multi-Criteria Decision Analysis Challenge ===")

        try:
            results = self.execute_sql_file("10_decision_analysis_challenge.sql")

            # Ultimate challenge - any meaningful result is exceptional
            assert len(results) >= 1, "Should return decision analysis results"

            print(f"✓ Successfully completed ultimate spatial analysis challenge!")
            print(f"✓ Professional-level multi-criteria decision analysis demonstrated")

        except (FileNotFoundError, ValueError) as e:
            if "not implemented" in str(e).lower() or "not attempted" in str(e).lower():
                pytest.skip("Ultimate decision analysis challenge not yet attempted")
            else:
                raise

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
            print(f"✓ {table}: {count} records")

    def test_spatial_functions_available(self):
        """Test that required PostGIS functions are available."""
        print("\n=== Testing PostGIS Functions ===")

        functions_to_test = [
            'ST_Intersects', 'ST_Intersection', 'ST_Area', 'ST_Buffer',
            'ST_Distance', 'ST_DWithin', 'ST_Transform', 'ST_GeometryType',
            'ST_SRID', 'ST_AsText', 'ST_Extent'
        ]

        for func in functions_to_test:
            self.cursor.execute(f"SELECT proname FROM pg_proc WHERE proname = '{func.lower()}' LIMIT 1;")
            result = self.cursor.fetchone()
            assert result is not None, f"PostGIS function {func} not available"

        print(f"✓ All {len(functions_to_test)} required PostGIS functions are available")


# Pytest fixtures and main execution
@pytest.fixture(scope="session")
def tester():
    """Create a tester instance for the session."""
    return PostGISSpatialAnalysisTester()


if __name__ == "__main__":
    # Run tests directly with python test_assignment.py
    import sys

    print("PostGIS Spatial Analysis Assignment - Progressive Test Suite")
    print("=" * 70)

    tester = PostGISSpatialAnalysisTester()
    test_methods = [method for method in dir(TestPostGISSpatialAnalysis) if method.startswith('test_')]

    passed = 0
    failed = 0
    skipped = 0
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

            # Award points for query tests (01-10)
            if test_method.startswith('test_') and any(f'test_{i:02d}_' in test_method for i in range(1, 11)):
                points = 2
                total_points += points
                print(f"✓ PASSED - {points} points awarded")
            else:
                print("✓ PASSED - Setup/validation test")

            passed += 1

        except pytest.skip.Exception as e:
            print(f"⏭ SKIPPED: {str(e)}")
            skipped += 1
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            failed += 1
        finally:
            tester.teardown_method()

    print("\n" + "=" * 70)
    print("POSTGIS SPATIAL ANALYSIS - TEST SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Points: {total_points}/{max_points}")
    print(f"Grade: {total_points/max_points*100:.1f}%")

    if total_points >= 18:
        print("🌟 EXCELLENT - Advanced PostGIS proficiency demonstrated!")
    elif total_points >= 16:
        print("👍 GOOD - Strong spatial analysis foundation")
    elif total_points >= 14:
        print("📚 ADEQUATE - Continue practicing advanced concepts")
    else:
        print("📖 DEVELOPING - Focus on foundational spatial concepts")

    if failed > 0:
        sys.exit(1)
