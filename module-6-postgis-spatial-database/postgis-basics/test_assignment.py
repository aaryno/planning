#!/usr/bin/env python3
"""
PostGIS Basics Assignment Testing Framework

This module tests student SQL solutions for PostGIS spatial database fundamentals.
Tests verify spatial queries, PostGIS functions, and expected result structures.

Author: GIST 604B Module 6 - PostGIS Fundamentals
"""

import os
import sys
import psycopg2
import pytest
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostGISAssignmentTester:
    """Test framework for PostGIS spatial database assignments"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def setup_method(self):
        """Setup database connection before each test method"""
        try:
            self.connection = psycopg2.connect(
                host='localhost',
                port=5433,  # PostGIS container port
                database='gis_fundamentals',
                user='postgres',
                password='postgres'
            )
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to PostGIS database")
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to PostGIS database: {e}")
            raise

    def teardown_method(self):
        """Cleanup database connection after each test method"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_sql_file(self, file_path: str) -> List[Tuple]:
        """
        Execute SQL file and return results

        Args:
            file_path: Path to SQL file

        Returns:
            List of result tuples

        Raises:
            Exception: If SQL execution fails
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"SQL file not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()

            # Remove comments and empty lines for cleaner execution
            sql_lines = [line.strip() for line in sql_content.split('\n')
                        if line.strip() and not line.strip().startswith('--')]
            sql_query = '\n'.join(sql_lines)

            if not sql_query.strip():
                raise ValueError(f"No executable SQL found in {file_path}")

            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            self.connection.commit()

            logger.info(f"Successfully executed {file_path}: {len(results)} rows returned")
            return results

        except (psycopg2.Error, Exception) as e:
            logger.error(f"Error executing SQL file {file_path}: {e}")
            if self.connection:
                self.connection.rollback()
            raise

    def get_column_names(self) -> List[str]:
        """Get column names from last query execution"""
        if self.cursor.description:
            return [desc[0] for desc in self.cursor.description]
        return []


class TestPostGISQueries:
    """Test class for PostGIS spatial query assignments"""

    def setup_method(self):
        """Setup test environment"""
        self.tester = PostGISAssignmentTester()
        self.tester.setup_method()

    def teardown_method(self):
        """Cleanup test environment"""
        self.tester.teardown_method()

    def test_01_spatial_inspection(self):
        """Test Query 1: Spatial Data Inspection"""
        results = self.tester.execute_sql_file('sql/01_spatial_inspection.sql')
        columns = self.tester.get_column_names()

        # Verify basic structure
        assert len(results) == 5, f"Expected 5 rows, got {len(results)}"

        # Verify required columns exist
        expected_columns = ['city_id', 'name', 'state_code', 'geometry_type', 'coordinate_system', 'coordinates_text']
        for col in expected_columns:
            assert col in columns, f"Missing required column: {col}"

        # Verify PostGIS function results
        for row in results:
            row_dict = dict(zip(columns, row))
            assert row_dict['geometry_type'] == 'ST_Point', f"Expected ST_Point, got {row_dict['geometry_type']}"
            assert row_dict['coordinate_system'] == 4326, f"Expected EPSG:4326, got {row_dict['coordinate_system']}"
            assert 'POINT(' in row_dict['coordinates_text'], f"Expected POINT geometry in WKT: {row_dict['coordinates_text']}"

        logger.info("✅ Query 1: Spatial inspection test passed")

    def test_02_geometry_creation(self):
        """Test Query 2: Geometry Creation Functions"""
        results = self.tester.execute_sql_file('sql/02_geometry_creation.sql')
        columns = self.tester.get_column_names()

        # Verify three geometry types created
        assert len(results) == 3, f"Expected 3 geometry examples, got {len(results)}"

        # Verify column structure
        expected_columns = ['geometry_name', 'geom_type', 'geometry_wkt']
        for col in expected_columns:
            assert col in columns, f"Missing required column: {col}"

        # Verify geometry types and content
        geometry_types = {dict(zip(columns, row))['geom_type'] for row in results}
        assert 'ST_Point' in geometry_types, "Missing ST_Point geometry type"
        assert 'ST_Polygon' in geometry_types, "Missing ST_Polygon geometry type"

        # Verify Denver coordinates present in results
        all_wkt = ' '.join([dict(zip(columns, row))['geometry_wkt'] for row in results])
        assert '-104.99' in all_wkt or '-104.9903' in all_wkt, "Denver longitude not found in results"
        assert '39.73' in all_wkt or '39.7392' in all_wkt, "Denver latitude not found in results"

        logger.info("✅ Query 2: Geometry creation test passed")

    def test_03_spatial_measurements(self):
        """Test Query 3: Spatial Measurements"""
        results = self.tester.execute_sql_file('sql/03_spatial_measurements.sql')
        columns = self.tester.get_column_names()

        # Verify three measurements calculated
        assert len(results) == 3, f"Expected 3 measurement examples, got {len(results)}"

        # Verify measurement types present
        measurement_types = {dict(zip(columns, row))['measurement_type'] for row in results}
        expected_types = {'Seattle to Portland Distance', 'Yellowstone Park Area', 'I-5 Highway Length'}

        for expected in expected_types:
            assert any(expected.lower() in mt.lower() for mt in measurement_types), f"Missing measurement: {expected}"

        # Verify reasonable measurement values
        for row in results:
            row_dict = dict(zip(columns, row))
            measurement_value = None

            # Find the numeric measurement value (different column names possible)
            for key, value in row_dict.items():
                if isinstance(value, (int, float)) and value > 0:
                    measurement_value = value
                    break

            assert measurement_value is not None, f"No valid measurement found in row: {row_dict}"
            assert measurement_value > 0, f"Measurement should be positive: {measurement_value}"

        logger.info("✅ Query 3: Spatial measurements test passed")

    def test_04_coordinate_transformation(self):
        """Test Query 4: Coordinate System Transformations"""
        results = self.tester.execute_sql_file('sql/04_coordinate_transformation.sql')
        columns = self.tester.get_column_names()

        # Verify one station transformation result
        assert len(results) == 1, f"Expected 1 transformation example, got {len(results)}"

        # Verify coordinate transformation columns
        row_dict = dict(zip(columns, results[0]))

        # Check for WGS84 coordinates (should be around Seattle)
        assert 'wgs84_longitude' in row_dict, "Missing WGS84 longitude column"
        assert 'wgs84_latitude' in row_dict, "Missing WGS84 latitude column"

        wgs84_lon = row_dict['wgs84_longitude']
        wgs84_lat = row_dict['wgs84_latitude']

        # Seattle coordinates should be approximately -122.3, 47.4
        assert -123 < wgs84_lon < -122, f"Seattle longitude out of range: {wgs84_lon}"
        assert 47 < wgs84_lat < 48, f"Seattle latitude out of range: {wgs84_lat}"

        # Check for UTM coordinates (should be much larger numbers)
        assert 'utm_easting_m' in row_dict, "Missing UTM easting column"
        assert 'utm_northing_m' in row_dict, "Missing UTM northing column"

        utm_easting = row_dict['utm_easting_m']
        utm_northing = row_dict['utm_northing_m']

        assert 500000 < utm_easting < 600000, f"UTM easting out of expected range: {utm_easting}"
        assert 5200000 < utm_northing < 5300000, f"UTM northing out of expected range: {utm_northing}"

        logger.info("✅ Query 4: Coordinate transformation test passed")

    def test_05_spatial_relationships(self):
        """Test Query 5: Spatial Relationships"""
        results = self.tester.execute_sql_file('sql/05_spatial_relationships.sql')
        columns = self.tester.get_column_names()

        # Verify multiple relationship results
        assert len(results) >= 2, f"Expected at least 2 relationship results, got {len(results)}"

        # Verify relationship query types present
        query_types = {dict(zip(columns, row))['query_type'] for row in results}

        expected_relationships = ['cities in washington', 'highway-park intersections', 'stations near seattle']
        for expected in expected_relationships:
            assert any(expected.lower() in qt.lower() for qt in query_types), f"Missing relationship query: {expected}"

        # Verify spatial relationship results make sense
        for row in results:
            row_dict = dict(zip(columns, row))
            query_type = row_dict['query_type'].lower()

            if 'washington' in query_type:
                # Should find Seattle in Washington
                assert any('seattle' in str(value).lower() for value in row_dict.values()), "Seattle should be found in Washington"

        logger.info("✅ Query 5: Spatial relationships test passed")

    def test_06_buffer_operations(self):
        """Test Query 6: Buffer Operations"""
        results = self.tester.execute_sql_file('sql/06_buffer_operations.sql')
        columns = self.tester.get_column_names()

        # Verify buffer analysis results
        assert len(results) >= 2, f"Expected at least 2 buffer results, got {len(results)}"

        # Verify buffer analysis types
        analysis_types = {dict(zip(columns, row))['analysis_type'] for row in results}

        expected_buffers = ['denver', 'i-5', 'highway', 'corridor', 'buffer']
        buffer_found = any(any(expected in at.lower() for expected in expected_buffers) for at in analysis_types)
        assert buffer_found, f"No buffer analysis types found in: {analysis_types}"

        # Verify numeric results exist (areas, lengths, distances)
        numeric_found = False
        for row in results:
            row_dict = dict(zip(columns, row))
            for value in row_dict.values():
                if isinstance(value, (int, float)) and value > 0:
                    numeric_found = True
                    break

        assert numeric_found, "No numeric measurements found in buffer results"

        logger.info("✅ Query 6: Buffer operations test passed")

    def test_07_spatial_joins(self):
        """Test Query 7: Spatial Joins"""
        results = self.tester.execute_sql_file('sql/07_spatial_joins.sql')
        columns = self.tester.get_column_names()

        # Verify spatial join results
        assert len(results) >= 3, f"Expected at least 3 spatial join results, got {len(results)}"

        # Verify join types present
        join_types = {dict(zip(columns, row))['join_type'] for row in results if 'join_type' in columns}

        if join_types:  # Only check if join_type column exists
            expected_joins = ['cities by state', 'stations to nearest', 'highway length']
            for expected in expected_joins:
                assert any(expected.lower() in jt.lower() for jt in join_types), f"Missing join type: {expected}"

        # Verify aggregation results (should have counts, sums, averages)
        has_aggregation = False
        for row in results:
            row_dict = dict(zip(columns, row))
            for key, value in row_dict.items():
                if ('count' in key.lower() or 'total' in key.lower() or 'avg' in key.lower()) and isinstance(value, (int, float)):
                    has_aggregation = True
                    break

        assert has_aggregation, "No aggregation results found in spatial joins"

        logger.info("✅ Query 7: Spatial joins test passed")

    def test_08_complex_analysis(self):
        """Test Query 8: Complex Spatial Analysis"""
        results = self.tester.execute_sql_file('sql/08_complex_analysis.sql')
        columns = self.tester.get_column_names()

        # Verify complex analysis results
        assert len(results) >= 1, f"Expected at least 1 complex analysis result, got {len(results)}"

        # Verify comprehensive column structure
        expected_elements = ['city', 'park', 'distance', 'station', 'analysis']
        column_text = ' '.join(columns).lower()

        found_elements = sum(1 for element in expected_elements if element in column_text)
        assert found_elements >= 3, f"Expected at least 3 analysis elements in columns, found {found_elements} in: {columns}"

        # Verify complex analysis produces meaningful results
        for row in results:
            row_dict = dict(zip(columns, row))

            # Should have city and park names
            has_location_data = any('city' in key.lower() and value for key, value in row_dict.items())
            assert has_location_data, f"Missing city location data in: {row_dict}"

            # Should have distance measurements
            has_distance_data = any('distance' in key.lower() and isinstance(value, (int, float)) for key, value in row_dict.items())
            assert has_distance_data, f"Missing distance measurements in: {row_dict}"

        logger.info("✅ Query 8: Complex spatial analysis test passed")


class TestQuerySyntax:
    """Test class for SQL file syntax and template completion"""

    def read_sql_file(self, file_path: str) -> str:
        """Read SQL file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            pytest.fail(f"SQL file not found: {file_path}")
        except Exception as e:
            pytest.fail(f"Error reading SQL file {file_path}: {e}")

    def test_query_files_exist(self):
        """Test that all required SQL query files exist"""
        required_files = [
            'sql/01_spatial_inspection.sql',
            'sql/02_geometry_creation.sql',
            'sql/03_spatial_measurements.sql',
            'sql/04_coordinate_transformation.sql',
            'sql/05_spatial_relationships.sql',
            'sql/06_buffer_operations.sql',
            'sql/07_spatial_joins.sql',
            'sql/08_complex_analysis.sql'
        ]

        for file_path in required_files:
            assert os.path.exists(file_path), f"Required SQL file missing: {file_path}"

        logger.info("✅ All required SQL files exist")

    def test_syntax_requirements(self):
        """Test that SQL files meet basic syntax and completion requirements"""
        sql_files = [
            'sql/01_spatial_inspection.sql',
            'sql/02_geometry_creation.sql',
            'sql/03_spatial_measurements.sql',
            'sql/04_coordinate_transformation.sql',
            'sql/05_spatial_relationships.sql',
            'sql/06_buffer_operations.sql',
            'sql/07_spatial_joins.sql',
            'sql/08_complex_analysis.sql'
        ]

        for file_path in sql_files:
            content = self.read_sql_file(file_path)

            # Check that templates have been completed (no blank underscores)
            assert '____' not in content, f"Incomplete template found in {file_path} (contains ____)"

            # Check for basic SQL syntax requirements
            assert 'SELECT' in content.upper(), f"Missing SELECT statement in {file_path}"
            assert 'FROM' in content.upper(), f"Missing FROM clause in {file_path}"
            assert content.strip().endswith(';'), f"Missing semicolon at end of {file_path}"

            # Check for PostGIS function usage
            postgis_functions = ['ST_', 'postgis']
            has_postgis = any(func.lower() in content.lower() for func in postgis_functions)
            assert has_postgis, f"No PostGIS functions found in {file_path}"

        logger.info("✅ All SQL files meet syntax requirements")


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
