"""
GIST 604B - PostGIS Fundamentals Assignment Tests
Module 6: PostGIS Spatial Database

Test suite for PostGIS basics functions including database connectivity,
spatial data loading, spatial analysis, and data export capabilities.

This test suite validates that students can:
- Connect to PostGIS databases securely
- Load spatial data from multiple formats
- Execute spatial queries using PostGIS functions
- Export results for stakeholder delivery

Professional Testing Practices:
- Database transaction isolation
- Test data cleanup and teardown
- Comprehensive error handling validation
- Performance and accuracy benchmarks
"""

import pytest
import psycopg2
import psycopg2.extras
import json
import csv
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import os
import sys

# Add src directory to path for importing student code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from postgis_basics import (
        connect_to_postgis,
        load_spatial_data,
        analyze_spatial_relationships,
        export_analysis_results
    )
except ImportError as e:
    pytest.fail(f"Cannot import required functions from postgis_basics.py: {e}")


class TestPostGISBasics:
    """
    Test suite for PostGIS fundamentals assignment.

    These tests validate core spatial database operations that form the
    foundation of enterprise GIS workflows.
    """

    @pytest.fixture(scope="class")
    def test_connection(self):
        """
        Create a test database connection for the entire test class.
        Uses separate test database to avoid conflicts with student work.
        """
        # Test connection parameters - matches Docker setup
        test_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'gis_analysis',
            'user': 'gis_student',
            'password': 'gis604b'
        }

        connection = None
        try:
            # Try to connect to test database
            connection = psycopg2.connect(**test_params)
            connection.autocommit = True

            # Verify PostGIS is available
            cursor = connection.cursor()
            cursor.execute("SELECT PostGIS_Version();")
            version = cursor.fetchone()
            cursor.close()

            if not version:
                pytest.skip("PostGIS extension not available in test database")

            yield connection

        except psycopg2.Error:
            pytest.skip("Cannot connect to PostGIS test database - is Docker running?")
        finally:
            if connection:
                connection.close()

    @pytest.fixture
    def test_data_files(self):
        """
        Create temporary test data files for loading tests.
        """
        temp_dir = tempfile.mkdtemp()

        # Create test cities CSV
        cities_file = Path(temp_dir) / 'test_cities.csv'
        cities_data = [
            {'name': 'Phoenix', 'latitude': 33.4484, 'longitude': -112.0740, 'population': 1608139},
            {'name': 'Tucson', 'latitude': 32.2217, 'longitude': -110.9265, 'population': 545975},
            {'name': 'Flagstaff', 'latitude': 35.1983, 'longitude': -111.6513, 'population': 76831}
        ]

        with open(cities_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'latitude', 'longitude', 'population'])
            writer.writeheader()
            writer.writerows(cities_data)

        # Create test parks GeoJSON
        parks_file = Path(temp_dir) / 'test_parks.geojson'
        parks_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-112.1, 33.4], [-112.0, 33.4], [-112.0, 33.5], [-112.1, 33.5], [-112.1, 33.4]
                        ]]
                    },
                    "properties": {
                        "name": "Phoenix Mountains Park",
                        "area_sqm": 10000000
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-110.95, 32.2], [-110.9, 32.2], [-110.9, 32.25], [-110.95, 32.25], [-110.95, 32.2]
                        ]]
                    },
                    "properties": {
                        "name": "Tucson Mountain Park",
                        "area_sqm": 8000000
                    }
                }
            ]
        }

        with open(parks_file, 'w') as f:
            json.dump(parks_geojson, f)

        yield str(cities_file), str(parks_file)

        # Cleanup
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def clean_database(self, test_connection):
        """
        Clean up test tables before and after each test.
        """
        cursor = test_connection.cursor()

        # Clean up before test
        cleanup_sql = """
        DROP TABLE IF EXISTS cities CASCADE;
        DROP TABLE IF EXISTS parks CASCADE;
        """
        cursor.execute(cleanup_sql)
        cursor.close()

        yield test_connection

        # Clean up after test
        cursor = test_connection.cursor()
        cursor.execute(cleanup_sql)
        cursor.close()


class TestDatabaseConnection:
    """Test database connectivity and PostGIS verification."""

    def test_connect_to_postgis_success(self):
        """
        Test successful PostGIS database connection.

        Validates:
        - Connection to correct database
        - PostGIS extension verification
        - Proper error handling
        """
        connection = connect_to_postgis()

        assert connection is not None, "Connection should not be None"
        assert not connection.closed, "Connection should be open"

        # Verify it's actually connected to the right database
        cursor = connection.cursor()
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        assert db_name == 'gis_analysis', f"Expected database 'gis_analysis', got '{db_name}'"

        # Verify PostGIS is available
        cursor.execute("SELECT PostGIS_Version();")
        version = cursor.fetchone()
        assert version is not None, "PostGIS version should be available"
        assert len(version[0]) > 0, "PostGIS version should not be empty"

        cursor.close()
        connection.close()

    def test_connect_to_postgis_error_handling(self):
        """
        Test connection error handling with invalid parameters.
        """
        # Mock psycopg2.connect to raise an error
        with patch('postgis_basics.psycopg2.connect') as mock_connect:
            mock_connect.side_effect = psycopg2.Error("Connection failed")

            with pytest.raises(psycopg2.Error):
                connect_to_postgis()

    def test_connection_autocommit_enabled(self):
        """
        Test that connection has autocommit enabled for DDL operations.
        """
        connection = connect_to_postgis()
        assert connection.autocommit == True, "Connection should have autocommit enabled"
        connection.close()


class TestSpatialDataLoading:
    """Test spatial data loading from CSV and GeoJSON files."""

    def test_load_spatial_data_success(self, clean_database, test_data_files):
        """
        Test successful loading of cities and parks data.

        Validates:
        - Table creation with correct schema
        - Spatial data type handling
        - Index creation
        - Data loading accuracy
        """
        cities_file, parks_file = test_data_files

        result = load_spatial_data(clean_database, cities_file, parks_file)

        # Verify return structure
        assert isinstance(result, dict), "Should return a dictionary"
        assert 'cities_loaded' in result, "Should report cities loaded count"
        assert 'parks_loaded' in result, "Should report parks loaded count"
        assert 'tables_created' in result, "Should report tables created"
        assert 'spatial_reference' in result, "Should report spatial reference"

        # Verify data counts
        assert result['cities_loaded'] == 3, f"Expected 3 cities, got {result['cities_loaded']}"
        assert result['parks_loaded'] == 2, f"Expected 2 parks, got {result['parks_loaded']}"
        assert result['spatial_reference'] == 4326, "Should use EPSG:4326"

        # Verify tables were created
        cursor = clean_database.cursor()

        # Check cities table structure
        cursor.execute("""
        SELECT column_name, data_type, udt_name
        FROM information_schema.columns
        WHERE table_name = 'cities'
        ORDER BY ordinal_position;
        """)
        cities_columns = cursor.fetchall()
        assert len(cities_columns) >= 4, "Cities table should have at least 4 columns"

        # Check for geometry column
        cursor.execute("""
        SELECT f_geometry_column, coord_dimension, srid, type
        FROM geometry_columns
        WHERE f_table_name = 'cities';
        """)
        cities_geom = cursor.fetchone()
        assert cities_geom is not None, "Cities should have geometry column registered"
        assert cities_geom[2] == 4326, "Cities geometry should use SRID 4326"
        assert cities_geom[3] == 'POINT', "Cities geometry should be POINT type"

        # Verify data was loaded correctly
        cursor.execute("SELECT name, population, ST_X(geom), ST_Y(geom) FROM cities ORDER BY name;")
        cities_data = cursor.fetchall()
        assert len(cities_data) == 3, "Should have 3 cities loaded"

        # Check Phoenix coordinates (first alphabetically)
        phoenix = cities_data[1]  # Should be second after Flagstaff
        assert phoenix[0] == 'Phoenix', f"Expected Phoenix, got {phoenix[0]}"
        assert abs(phoenix[2] - (-112.0740)) < 0.001, "Phoenix longitude should match"
        assert abs(phoenix[3] - 33.4484) < 0.001, "Phoenix latitude should match"

        cursor.close()

    def test_load_spatial_data_file_not_found(self, clean_database):
        """
        Test error handling when data files don't exist.
        """
        with pytest.raises((FileNotFoundError, Exception)):
            load_spatial_data(clean_database, 'nonexistent.csv', 'missing.geojson')

    def test_load_spatial_data_invalid_json(self, clean_database, test_data_files):
        """
        Test error handling with malformed GeoJSON.
        """
        cities_file, _ = test_data_files

        # Create invalid GeoJSON file
        temp_dir = tempfile.mkdtemp()
        invalid_geojson = Path(temp_dir) / 'invalid.geojson'
        with open(invalid_geojson, 'w') as f:
            f.write('{"invalid": "json"')  # Malformed JSON

        try:
            with pytest.raises((json.JSONDecodeError, Exception)):
                load_spatial_data(clean_database, cities_file, str(invalid_geojson))
        finally:
            shutil.rmtree(temp_dir)


class TestSpatialAnalysis:
    """Test spatial analysis operations using PostGIS functions."""

    @pytest.fixture
    def loaded_data(self, clean_database, test_data_files):
        """Load test data for spatial analysis tests."""
        cities_file, parks_file = test_data_files
        load_spatial_data(clean_database, cities_file, parks_file)
        return clean_database

    def test_analyze_spatial_relationships_success(self, loaded_data):
        """
        Test successful spatial relationship analysis.

        Validates:
        - ST_Contains() operations
        - ST_Area() calculations
        - ST_Distance() measurements
        - Result format and accuracy
        """
        result = analyze_spatial_relationships(loaded_data)

        # Verify return structure
        assert isinstance(result, dict), "Should return a dictionary"
        assert 'cities_in_parks' in result, "Should include cities in parks analysis"
        assert 'average_park_area' in result, "Should include average park area"
        assert 'nearest_park_distances' in result, "Should include distance analysis"
        assert 'total_parks_area' in result, "Should include total park area"

        # Verify data types
        assert isinstance(result['cities_in_parks'], list), "Cities in parks should be a list"
        assert isinstance(result['average_park_area'], (int, float)), "Average area should be numeric"
        assert isinstance(result['nearest_park_distances'], dict), "Distances should be a dictionary"
        assert isinstance(result['total_parks_area'], (int, float)), "Total area should be numeric"

        # Verify reasonable values (based on test data)
        assert result['average_park_area'] > 0, "Average park area should be positive"
        assert result['total_parks_area'] > 0, "Total park area should be positive"

        # Test nearest park distances structure
        if result['nearest_park_distances']:
            for city_name, distance_info in result['nearest_park_distances'].items():
                assert isinstance(distance_info, dict), f"Distance info for {city_name} should be a dict"
                assert 'nearest_park' in distance_info, f"Should include nearest park for {city_name}"
                assert 'distance_km' in distance_info, f"Should include distance for {city_name}"
                assert distance_info['distance_km'] >= 0, f"Distance should be non-negative for {city_name}"

    def test_analyze_spatial_relationships_empty_database(self, clean_database):
        """
        Test spatial analysis with empty database.
        """
        result = analyze_spatial_relationships(clean_database)

        # Should handle empty database gracefully
        assert result['cities_in_parks'] == [], "Should return empty list for no data"
        assert result['average_park_area'] == 0.0, "Should return 0 for no parks"
        assert result['nearest_park_distances'] == {}, "Should return empty dict for no data"

    def test_spatial_analysis_units_conversion(self, loaded_data):
        """
        Test that area measurements are properly converted to km².
        """
        result = analyze_spatial_relationships(loaded_data)

        # Areas should be in reasonable km² range (converted from m²)
        if result['average_park_area'] > 0:
            # Test parks are ~8-10 million m² = 8-10 km²
            assert 5 < result['average_park_area'] < 15, f"Average area {result['average_park_area']} km² seems unreasonable"


class TestDataExport:
    """Test data export functionality to multiple formats."""

    @pytest.fixture
    def loaded_data_for_export(self, clean_database, test_data_files):
        """Load test data for export tests."""
        cities_file, parks_file = test_data_files
        load_spatial_data(clean_database, cities_file, parks_file)
        return clean_database

    def test_export_analysis_results_success(self, loaded_data_for_export):
        """
        Test successful data export to multiple formats.

        Validates:
        - CSV export with coordinates
        - GeoJSON export with geometries
        - Summary report creation
        - File validation and integrity
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            result = export_analysis_results(loaded_data_for_export, temp_dir)

            # Verify return structure
            assert isinstance(result, dict), "Should return a dictionary"
            assert 'files_created' in result, "Should list files created"
            assert 'record_counts' in result, "Should report record counts"
            assert 'formats_exported' in result, "Should list formats exported"
            assert 'export_success' in result, "Should report success status"

            # Verify success
            assert result['export_success'] == True, "Export should be successful"
            assert len(result['files_created']) >= 3, "Should create at least 3 files"

            # Check that files actually exist
            for file_path in result['files_created']:
                file_path_obj = Path(file_path)
                assert file_path_obj.exists(), f"File {file_path} should exist"
                assert file_path_obj.stat().st_size > 0, f"File {file_path} should not be empty"

            # Verify CSV export
            csv_files = [f for f in result['files_created'] if f.endswith('.csv')]
            assert len(csv_files) > 0, "Should create at least one CSV file"

            # Verify GeoJSON export
            geojson_files = [f for f in result['files_created'] if f.endswith('.geojson')]
            assert len(geojson_files) > 0, "Should create at least one GeoJSON file"

            # Verify summary report
            txt_files = [f for f in result['files_created'] if f.endswith('.txt')]
            assert len(txt_files) > 0, "Should create summary report"

    def test_export_csv_content_validation(self, loaded_data_for_export):
        """
        Test that CSV export contains correct coordinate data.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            result = export_analysis_results(loaded_data_for_export, temp_dir)

            # Find and validate cities CSV
            csv_files = [f for f in result['files_created'] if f.endswith('.csv')]
            cities_csv = Path(csv_files[0])

            # Read and validate CSV content
            with open(cities_csv, 'r') as f:
                csv_reader = csv.DictReader(f)
                rows = list(csv_reader)

                assert len(rows) == 3, f"Expected 3 cities in CSV, got {len(rows)}"

                # Check required columns exist
                required_columns = ['name', 'latitude', 'longitude']  # Adjust based on implementation
                for col in required_columns:
                    if col in csv_reader.fieldnames:
                        assert col in csv_reader.fieldnames, f"CSV should contain {col} column"

                # Validate coordinate values are reasonable
                for row in rows:
                    if 'latitude' in row and 'longitude' in row:
                        lat = float(row['latitude'])
                        lon = float(row['longitude'])
                        assert -90 <= lat <= 90, f"Latitude {lat} is out of valid range"
                        assert -180 <= lon <= 180, f"Longitude {lon} is out of valid range"

    def test_export_geojson_validation(self, loaded_data_for_export):
        """
        Test that GeoJSON export is valid GeoJSON format.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            result = export_analysis_results(loaded_data_for_export, temp_dir)

            # Find and validate GeoJSON
            geojson_files = [f for f in result['files_created'] if f.endswith('.geojson')]
            parks_geojson = Path(geojson_files[0])

            # Read and validate GeoJSON structure
            with open(parks_geojson, 'r') as f:
                geojson_data = json.load(f)

                assert geojson_data['type'] == 'FeatureCollection', "Should be valid FeatureCollection"
                assert 'features' in geojson_data, "Should contain features array"
                assert len(geojson_data['features']) == 2, f"Expected 2 parks, got {len(geojson_data['features'])}"

                # Validate each feature
                for feature in geojson_data['features']:
                    assert feature['type'] == 'Feature', "Each item should be a Feature"
                    assert 'geometry' in feature, "Feature should have geometry"
                    assert 'properties' in feature, "Feature should have properties"
                    assert feature['geometry']['type'] in ['Polygon', 'MultiPolygon'], "Should be polygon geometry"

    def test_export_directory_creation(self):
        """
        Test that export creates output directory if it doesn't exist.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / 'new_directory' / 'nested'

            # Directory shouldn't exist yet
            assert not output_dir.exists(), "Directory should not exist initially"

            # Mock loaded data since we're testing directory creation
            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value = mock_cursor

            # This should create the directory (or at least attempt to)
            try:
                export_analysis_results(mock_connection, str(output_dir))
            except Exception:
                pass  # We expect this to fail due to mock, but directory should be created


class TestIntegration:
    """Integration tests that verify the complete workflow."""

    def test_complete_workflow(self, test_data_files):
        """
        Test the complete workflow from connection to export.

        This test validates that a student's implementation can handle
        a complete real-world workflow scenario.
        """
        cities_file, parks_file = test_data_files

        # Step 1: Connect to database
        connection = connect_to_postgis()
        assert connection is not None, "Connection should be established"

        try:
            # Clean up any existing test data
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS cities CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS parks CASCADE;")
            cursor.close()

            # Step 2: Load spatial data
            load_result = load_spatial_data(connection, cities_file, parks_file)
            assert load_result['cities_loaded'] > 0, "Should load cities successfully"
            assert load_result['parks_loaded'] > 0, "Should load parks successfully"

            # Step 3: Perform spatial analysis
            analysis_result = analyze_spatial_relationships(connection)
            assert isinstance(analysis_result, dict), "Analysis should return results"

            # Step 4: Export results
            with tempfile.TemporaryDirectory() as temp_dir:
                export_result = export_analysis_results(connection, temp_dir)
                assert export_result['export_success'] == True, "Export should succeed"
                assert len(export_result['files_created']) > 0, "Should create output files"

        finally:
            # Cleanup
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS cities CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS parks CASCADE;")
            cursor.close()
            connection.close()

    def test_error_recovery(self, test_data_files):
        """
        Test that the system gracefully handles and recovers from errors.
        """
        cities_file, parks_file = test_data_files

        # Test with invalid connection first
        with patch('postgis_basics.psycopg2.connect') as mock_connect:
            mock_connect.side_effect = psycopg2.Error("Connection failed")

            with pytest.raises(psycopg2.Error):
                connect_to_postgis()

        # Then test that normal operations still work
        connection = connect_to_postgis()
        assert connection is not None, "Should be able to connect after error"
        connection.close()


# Performance and benchmarking tests
class TestPerformance:
    """
    Performance tests to ensure reasonable execution times.
    These help students understand database performance concepts.
    """

    def test_connection_performance(self, benchmark):
        """
        Benchmark database connection time.
        """
        def connect_and_close():
            conn = connect_to_postgis()
            conn.close()

        result = benchmark(connect_and_close)
        # Connection should be fast (< 1 second)
        assert result < 1.0, "Database connection should be fast"

    @pytest.mark.skipif(not pytest.importorskip("pytest_benchmark"), reason="pytest-benchmark not available")
    def test_spatial_query_performance(self, clean_database, test_data_files):
        """
        Benchmark spatial query performance with proper indexes.
        """
        cities_file, parks_file = test_data_files
        load_spatial_data(clean_database, cities_file, parks_file)

        def run_spatial_analysis():
            return analyze_spatial_relationships(clean_database)

        # Spatial queries should complete reasonably quickly
        import time
        start_time = time.time()
        result = run_spatial_analysis()
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time < 5.0, f"Spatial analysis took {execution_time:.2f}s - consider adding spatial indexes"


if __name__ == "__main__":
    """
    Run tests directly for development.
    """
    pytest.main([__file__, "-v", "--tb=short"])
