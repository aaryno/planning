#!/usr/bin/env python3
"""
PostGIS Basics Assignment - Environment Validation Script

This script verifies that your PostGIS environment is properly configured
and that all required spatial data has been loaded successfully.

Usage:
    python validate_setup.py
    python validate_setup.py --verbose
    python validate_setup.py --port 5433

Author: GIST 604B Module 6 - PostGIS Fundamentals
"""

import psycopg2
import sys
import argparse
from typing import Dict, List, Tuple, Any
import json

class PostGISValidator:
    """Validates PostGIS database setup and spatial data availability."""

    def __init__(self, host='localhost', port=5433, database='gis_fundamentals',
                 user='postgres', password='postgres', verbose=False):
        self.connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.verbose = verbose
        self.connection = None
        self.cursor = None

        # Expected spatial tables and their minimum record counts
        self.expected_tables = {
            'cities': 10,
            'national_parks': 5,
            'highways': 3,
            'weather_stations': 6,
            'states': 5
        }

        # Test results storage
        self.test_results = {
            'connection': False,
            'postgis_extension': False,
            'postgis_version': None,
            'tables_loaded': {},
            'spatial_indexes': {},
            'geometry_validity': {},
            'coordinate_systems': {},
            'sample_queries': {},
            'overall_status': 'FAILED'
        }

    def log(self, message: str, level: str = 'INFO'):
        """Log message with optional verbose output."""
        if level == 'ERROR':
            print(f"❌ {message}")
        elif level == 'SUCCESS':
            print(f"✅ {message}")
        elif level == 'WARNING':
            print(f"⚠️  {message}")
        elif self.verbose or level == 'ALWAYS':
            print(f"ℹ️  {message}")

    def connect_database(self) -> bool:
        """Establish connection to PostGIS database."""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()

            # Test basic connectivity
            self.cursor.execute("SELECT version();")
            pg_version = self.cursor.fetchone()[0]

            self.test_results['connection'] = True
            self.log("Successfully connected to PostgreSQL database", "SUCCESS")
            self.log(f"PostgreSQL Version: {pg_version[:50]}...", "ALWAYS")

            return True

        except psycopg2.Error as e:
            self.test_results['connection'] = False
            self.log(f"Database connection failed: {e}", "ERROR")
            self.log("Check that PostGIS container is running: docker-compose up -d", "ERROR")
            return False
        except Exception as e:
            self.test_results['connection'] = False
            self.log(f"Unexpected connection error: {e}", "ERROR")
            return False

    def check_postgis_extension(self) -> bool:
        """Verify PostGIS extension is installed and get version."""
        try:
            # Check if PostGIS extension exists
            self.cursor.execute("""
                SELECT EXISTS(
                    SELECT 1 FROM pg_extension WHERE extname = 'postgis'
                );
            """)

            has_postgis = self.cursor.fetchone()[0]

            if not has_postgis:
                self.log("PostGIS extension not found!", "ERROR")
                self.log("PostGIS should be automatically installed with postgis/postgis image", "ERROR")
                return False

            # Get PostGIS version
            self.cursor.execute("SELECT postgis_version();")
            postgis_version = self.cursor.fetchone()[0]

            self.test_results['postgis_extension'] = True
            self.test_results['postgis_version'] = postgis_version
            self.log("PostGIS extension is installed", "SUCCESS")
            self.log(f"PostGIS Version: {postgis_version}", "ALWAYS")

            # Check for additional useful extensions
            self.cursor.execute("""
                SELECT extname FROM pg_extension
                WHERE extname IN ('postgis_topology', 'fuzzystrmatch', 'postgis_tiger_geocoder');
            """)

            additional_extensions = [row[0] for row in self.cursor.fetchall()]
            if additional_extensions:
                self.log(f"Additional extensions available: {', '.join(additional_extensions)}")

            return True

        except psycopg2.Error as e:
            self.test_results['postgis_extension'] = False
            self.log(f"Error checking PostGIS extension: {e}", "ERROR")
            return False

    def validate_spatial_tables(self) -> bool:
        """Check that all required spatial tables exist with expected data."""
        all_tables_valid = True

        for table_name, min_records in self.expected_tables.items():
            try:
                # Check if table exists
                self.cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_name = %s AND table_schema = 'public'
                    );
                """, (table_name,))

                table_exists = self.cursor.fetchone()[0]

                if not table_exists:
                    self.test_results['tables_loaded'][table_name] = {
                        'exists': False,
                        'record_count': 0,
                        'has_geometry': False,
                        'status': 'MISSING'
                    }
                    self.log(f"Table '{table_name}' does not exist", "ERROR")
                    all_tables_valid = False
                    continue

                # Check record count
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                record_count = self.cursor.fetchone()[0]

                # Check for geometry column
                self.cursor.execute("""
                    SELECT column_name, udt_name
                    FROM information_schema.columns
                    WHERE table_name = %s AND udt_name = 'geometry';
                """, (table_name,))

                geometry_columns = self.cursor.fetchall()
                has_geometry = len(geometry_columns) > 0

                # Store results
                status = 'OK' if record_count >= min_records and has_geometry else 'INCOMPLETE'
                self.test_results['tables_loaded'][table_name] = {
                    'exists': True,
                    'record_count': record_count,
                    'expected_minimum': min_records,
                    'has_geometry': has_geometry,
                    'geometry_columns': [col[0] for col in geometry_columns],
                    'status': status
                }

                if status == 'OK':
                    self.log(f"Table '{table_name}': {record_count} records with geometry ✓", "SUCCESS")
                else:
                    self.log(f"Table '{table_name}': {record_count} records (expected ≥{min_records}), geometry: {has_geometry}", "WARNING")
                    all_tables_valid = False

            except psycopg2.Error as e:
                self.test_results['tables_loaded'][table_name] = {
                    'exists': False,
                    'error': str(e),
                    'status': 'ERROR'
                }
                self.log(f"Error checking table '{table_name}': {e}", "ERROR")
                all_tables_valid = False

        return all_tables_valid

    def check_spatial_indexes(self) -> bool:
        """Verify that spatial indexes exist for geometry columns."""
        indexes_ok = True

        for table_name in self.expected_tables.keys():
            try:
                self.cursor.execute("""
                    SELECT indexname, indexdef
                    FROM pg_indexes
                    WHERE tablename = %s
                    AND indexdef LIKE '%%USING gist%%'
                    AND indexdef LIKE '%%geom%%';
                """, (table_name,))

                spatial_indexes = self.cursor.fetchall()

                self.test_results['spatial_indexes'][table_name] = {
                    'index_count': len(spatial_indexes),
                    'indexes': [idx[0] for idx in spatial_indexes],
                    'has_spatial_index': len(spatial_indexes) > 0
                }

                if len(spatial_indexes) > 0:
                    self.log(f"Spatial index found for '{table_name}': {spatial_indexes[0][0]}")
                else:
                    self.log(f"No spatial index found for '{table_name}' (performance may be slow)", "WARNING")

            except psycopg2.Error as e:
                self.log(f"Error checking spatial indexes for '{table_name}': {e}", "ERROR")
                indexes_ok = False

        return indexes_ok

    def validate_geometry_data(self) -> bool:
        """Test geometry validity and coordinate systems."""
        geometry_valid = True

        for table_name in self.expected_tables.keys():
            try:
                # Check geometry validity
                self.cursor.execute(f"""
                    SELECT
                        COUNT(*) as total_geoms,
                        COUNT(CASE WHEN ST_IsValid(geom) THEN 1 END) as valid_geoms,
                        ST_SRID(geom) as srid,
                        ST_GeometryType(geom) as geom_type
                    FROM {table_name}
                    WHERE geom IS NOT NULL
                    GROUP BY ST_SRID(geom), ST_GeometryType(geom)
                    LIMIT 5;
                """)

                geometry_stats = self.cursor.fetchall()

                table_stats = []
                for stats in geometry_stats:
                    total, valid, srid, geom_type = stats
                    table_stats.append({
                        'total_geometries': total,
                        'valid_geometries': valid,
                        'srid': srid,
                        'geometry_type': geom_type,
                        'validity_rate': (valid / total) * 100 if total > 0 else 0
                    })

                    if valid == total:
                        self.log(f"All {total} {geom_type} geometries in '{table_name}' are valid (SRID: {srid})")
                    else:
                        self.log(f"Geometry validity issue in '{table_name}': {valid}/{total} valid", "WARNING")
                        geometry_valid = False

                self.test_results['geometry_validity'][table_name] = table_stats

            except psycopg2.Error as e:
                self.log(f"Error validating geometry in '{table_name}': {e}", "ERROR")
                geometry_valid = False

        return geometry_valid

    def test_coordinate_systems(self) -> bool:
        """Test coordinate system handling and transformations."""
        crs_tests_passed = True

        try:
            # Test basic coordinate system functions
            test_queries = {
                'wgs84_point': "SELECT ST_AsText(ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326));",
                'utm_transform': "SELECT ST_AsText(ST_Transform(ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326), 32610));",
                'srid_check': "SELECT DISTINCT ST_SRID(geom) FROM cities;",
                'extent_check': "SELECT ST_AsText(ST_Extent(geom)) FROM cities;"
            }

            for test_name, query in test_queries.items():
                try:
                    self.cursor.execute(query)
                    result = self.cursor.fetchone()[0]

                    self.test_results['coordinate_systems'][test_name] = {
                        'query': query,
                        'result': str(result),
                        'status': 'SUCCESS'
                    }

                    self.log(f"CRS test '{test_name}': {str(result)[:50]}...")

                except psycopg2.Error as e:
                    self.test_results['coordinate_systems'][test_name] = {
                        'query': query,
                        'error': str(e),
                        'status': 'FAILED'
                    }
                    self.log(f"CRS test '{test_name}' failed: {e}", "ERROR")
                    crs_tests_passed = False

        except Exception as e:
            self.log(f"Error in coordinate system tests: {e}", "ERROR")
            crs_tests_passed = False

        return crs_tests_passed

    def run_sample_queries(self) -> bool:
        """Execute sample PostGIS queries to verify functionality."""
        queries_passed = True

        sample_queries = {
            'basic_select': {
                'query': "SELECT name, ST_AsText(geom) FROM cities LIMIT 3;",
                'description': 'Basic spatial data selection'
            },
            'distance_calculation': {
                'query': """
                    SELECT
                        c1.name, c2.name,
                        ROUND(ST_Distance_Sphere(c1.geom, c2.geom) / 1000, 2) as distance_km
                    FROM cities c1, cities c2
                    WHERE c1.name = 'Seattle' AND c2.name = 'Portland'
                    LIMIT 1;
                """,
                'description': 'Distance calculation between cities'
            },
            'spatial_join': {
                'query': """
                    SELECT c.name, s.state_name
                    FROM cities c
                    JOIN states s ON ST_Within(c.geom, s.geom)
                    LIMIT 3;
                """,
                'description': 'Spatial join between cities and states'
            },
            'buffer_analysis': {
                'query': """
                    SELECT
                        name,
                        ST_Area(ST_Buffer(ST_Transform(geom, 32610), 10000)) / 1000000 as buffer_area_sq_km
                    FROM cities
                    WHERE name = 'Seattle'
                    LIMIT 1;
                """,
                'description': '10km buffer analysis around Seattle'
            }
        }

        for query_name, query_info in sample_queries.items():
            try:
                self.cursor.execute(query_info['query'])
                results = self.cursor.fetchall()

                self.test_results['sample_queries'][query_name] = {
                    'description': query_info['description'],
                    'query': query_info['query'],
                    'result_count': len(results),
                    'sample_result': str(results[0]) if results else 'No results',
                    'status': 'SUCCESS'
                }

                self.log(f"Sample query '{query_name}': {len(results)} results", "SUCCESS")

            except psycopg2.Error as e:
                self.test_results['sample_queries'][query_name] = {
                    'description': query_info['description'],
                    'query': query_info['query'],
                    'error': str(e),
                    'status': 'FAILED'
                }
                self.log(f"Sample query '{query_name}' failed: {e}", "ERROR")
                queries_passed = False

        return queries_passed

    def cleanup(self):
        """Close database connections."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        # Determine overall status
        critical_checks = [
            self.test_results['connection'],
            self.test_results['postgis_extension'],
            len([t for t in self.test_results['tables_loaded'].values() if t.get('status') == 'OK']) >= 4
        ]

        self.test_results['overall_status'] = 'PASSED' if all(critical_checks) else 'FAILED'

        # Add summary statistics
        self.test_results['summary'] = {
            'total_tables_checked': len(self.expected_tables),
            'tables_loaded_successfully': len([t for t in self.test_results['tables_loaded'].values() if t.get('status') == 'OK']),
            'spatial_indexes_found': sum(1 for idx in self.test_results['spatial_indexes'].values() if idx.get('has_spatial_index')),
            'sample_queries_passed': len([q for q in self.test_results['sample_queries'].values() if q.get('status') == 'SUCCESS']),
            'validation_timestamp': __import__('datetime').datetime.now().isoformat()
        }

        return self.test_results

    def run_validation(self) -> bool:
        """Execute complete validation workflow."""
        print("🚀 Starting PostGIS Environment Validation...")
        print("=" * 60)

        try:
            # Step 1: Database Connection
            print("\n📡 Testing Database Connection...")
            if not self.connect_database():
                return False

            # Step 2: PostGIS Extension
            print("\n🌍 Checking PostGIS Extension...")
            self.check_postgis_extension()

            # Step 3: Spatial Tables
            print("\n📊 Validating Spatial Data Tables...")
            self.validate_spatial_tables()

            # Step 4: Spatial Indexes
            print("\n🔍 Checking Spatial Indexes...")
            self.check_spatial_indexes()

            # Step 5: Geometry Validation
            print("\n📐 Validating Geometry Data...")
            self.validate_geometry_data()

            # Step 6: Coordinate Systems
            print("\n🗺️  Testing Coordinate Systems...")
            self.test_coordinate_systems()

            # Step 7: Sample Queries
            print("\n🧪 Running Sample PostGIS Queries...")
            self.run_sample_queries()

            # Generate final report
            report = self.generate_validation_report()

            # Print summary
            print("\n" + "=" * 60)
            print("📋 VALIDATION SUMMARY")
            print("=" * 60)

            if report['overall_status'] == 'PASSED':
                print("🎉 PostGIS Environment: READY FOR ASSIGNMENT")
            else:
                print("⚠️  PostGIS Environment: NEEDS ATTENTION")

            print(f"✅ Tables loaded: {report['summary']['tables_loaded_successfully']}/{report['summary']['total_tables_checked']}")
            print(f"🔍 Spatial indexes: {report['summary']['spatial_indexes_found']}/{report['summary']['total_tables_checked']}")
            print(f"🧪 Sample queries: {report['summary']['sample_queries_passed']}/4")
            print(f"🌍 PostGIS version: {report['postgis_version']}")

            if report['overall_status'] == 'FAILED':
                print("\n💡 To fix issues:")
                print("   1. Ensure PostGIS container is running: docker-compose up -d")
                print("   2. Wait for data initialization (30-60 seconds)")
                print("   3. Check container logs: docker-compose logs postgres")
                print("   4. Reload data if needed: docker exec -i postgis-basics-postgres psql -U postgres -d gis_fundamentals < data/load_spatial_data.sql")

            return report['overall_status'] == 'PASSED'

        except Exception as e:
            self.log(f"Unexpected error during validation: {e}", "ERROR")
            return False

        finally:
            self.cleanup()

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Validate PostGIS environment setup')
    parser.add_argument('--host', default='localhost', help='Database host (default: localhost)')
    parser.add_argument('--port', type=int, default=5433, help='Database port (default: 5433)')
    parser.add_argument('--database', default='gis_fundamentals', help='Database name (default: gis_fundamentals)')
    parser.add_argument('--user', default='postgres', help='Database user (default: postgres)')
    parser.add_argument('--password', default='postgres', help='Database password (default: postgres)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--output', help='Save validation report to JSON file')

    args = parser.parse_args()

    # Create validator
    validator = PostGISValidator(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password,
        verbose=args.verbose
    )

    # Run validation
    success = validator.run_validation()

    # Save report if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(validator.test_results, f, indent=2, default=str)
            print(f"📄 Validation report saved to: {args.output}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
