"""
GIST 604B - PostGIS Fundamentals Assignment
Module 6: PostGIS Spatial Database

Student Name: [Your Name Here]
Date: [Assignment Date]

This module contains functions for basic PostGIS database operations.
Complete the TODO sections to implement each function according to the
requirements in the README.md file.

Learning Objectives:
- Connect to PostGIS databases programmatically
- Load spatial data from CSV and GeoJSON files
- Execute basic spatial queries using PostGIS functions
- Export results in multiple formats

Professional Skills:
- Database connection management
- Spatial data type handling
- SQL query construction
- Error handling and validation
"""

import psycopg2
import psycopg2.extras
import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_postgis() -> psycopg2.extensions.connection:
    """
    Connect to the PostGIS database and verify the connection.

    This function demonstrates professional database connection practices
    including error handling, connection validation, and PostGIS verification.

    Returns:
        psycopg2.connection: Active database connection with PostGIS enabled

    Requirements:
        - Connect to localhost:5432, database 'gis_analysis'
        - Username: 'gis_student', Password: 'gis604b'
        - Verify PostGIS extension is available
        - Handle connection errors gracefully
        - Return active connection object

    Professional Notes:
        - In production, use environment variables for credentials
        - Always verify PostGIS is available before spatial operations
        - Implement connection pooling for web applications
    """

    # TODO: Define connection parameters
    # Use a dictionary to organize connection parameters clearly
    conn_params = {
        # TODO: Fill in the connection parameters
        'host': None,  # Replace with correct host
        'port': None,  # Replace with correct port
        'database': None,  # Replace with correct database name
        'user': None,  # Replace with correct username
        'password': None  # Replace with correct password
    }

    connection = None

    try:
        # TODO: Establish database connection
        # Use psycopg2.connect() with the parameters above
        # connection = psycopg2.connect(**conn_params)

        # TODO: Test the connection with a simple query
        # Create a cursor and execute "SELECT version();" to verify connectivity

        # TODO: Verify PostGIS extension is available
        # Execute "SELECT PostGIS_Version();" to confirm spatial functions work
        # Print the PostGIS version for debugging

        # TODO: Set connection autocommit mode
        # Use connection.autocommit = True for simpler transaction handling

        logger.info("✅ Successfully connected to PostGIS database")
        return connection

    except psycopg2.Error as e:
        # TODO: Handle database connection errors
        # Log the error and re-raise with helpful message
        # Consider specific error types: authentication, network, etc.
        logger.error(f"❌ Database connection failed: {e}")
        raise

    except Exception as e:
        # TODO: Handle other unexpected errors
        logger.error(f"❌ Unexpected error during connection: {e}")
        raise


def load_spatial_data(connection: psycopg2.extensions.connection,
                     cities_file: str,
                     parks_file: str) -> Dict[str, Any]:
    """
    Load city and park data into PostGIS tables with proper spatial types.

    This function demonstrates ETL (Extract, Transform, Load) processes
    commonly used in GIS data management workflows.

    Parameters:
        connection: Active database connection
        cities_file: Path to cities CSV file (with lat/lon columns)
        parks_file: Path to parks GeoJSON file

    Returns:
        dict: Summary of loaded data including:
            - cities_loaded: Number of city records loaded
            - parks_loaded: Number of park records loaded
            - tables_created: List of table names created
            - spatial_reference: SRID used for geometries

    Requirements:
        - Create 'cities' table with Point geometry (EPSG:4326)
        - Create 'parks' table with Polygon geometry (EPSG:4326)
        - Include spatial indexes for performance
        - Load data from provided CSV and GeoJSON files
        - Return comprehensive summary statistics

    Professional Notes:
        - Always create spatial indexes for performance
        - Use consistent SRID across all spatial tables
        - Validate geometry before insertion
        - Consider data type constraints and validation rules
    """

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    summary = {
        'cities_loaded': 0,
        'parks_loaded': 0,
        'tables_created': [],
        'spatial_reference': 4326  # EPSG:4326 (WGS 84)
    }

    try:
        # TODO: Create cities table
        create_cities_table = """
        -- TODO: Write SQL to create cities table
        -- Include columns: id (serial), name (varchar), population (integer), geom (geometry)
        -- Set geometry type to POINT with SRID 4326
        """

        # TODO: Execute cities table creation
        # cursor.execute(create_cities_table)

        # TODO: Create spatial index on cities geometry
        create_cities_index = """
        -- TODO: Write SQL to create spatial index
        -- Use GIST index type for spatial data
        """

        # TODO: Execute index creation
        # cursor.execute(create_cities_index)

        # TODO: Create parks table
        create_parks_table = """
        -- TODO: Write SQL to create parks table
        -- Include columns: id (serial), name (varchar), area_sqm (float), geom (geometry)
        -- Set geometry type to POLYGON with SRID 4326
        """

        # TODO: Execute parks table creation and index

        # TODO: Load cities data from CSV
        # Read the CSV file and insert each city as a POINT geometry
        # Use ST_MakePoint(longitude, latitude) to create geometries
        # Remember: longitude first, then latitude in ST_MakePoint()

        with open(cities_file, 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                # TODO: Extract city data from CSV row
                # name = row['name']
                # latitude = float(row['latitude'])
                # longitude = float(row['longitude'])
                # population = int(row['population'])

                # TODO: Insert city into database
                # Use ST_SetSRID(ST_MakePoint(lng, lat), 4326) for proper spatial reference
                insert_city = """
                -- TODO: Write INSERT statement with spatial geometry
                """

                # cursor.execute(insert_city, (name, population, longitude, latitude))
                # summary['cities_loaded'] += 1
                pass

        # TODO: Load parks data from GeoJSON
        with open(parks_file, 'r') as f:
            geojson_data = json.load(f)

            for feature in geojson_data['features']:
                # TODO: Extract park data from GeoJSON feature
                # properties = feature['properties']
                # geometry = feature['geometry']

                # TODO: Convert GeoJSON geometry to PostGIS format
                # Use ST_GeomFromGeoJSON() to convert geometry
                # Calculate area using ST_Area() if not provided

                insert_park = """
                -- TODO: Write INSERT statement for park data
                -- Use ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326) for geometry
                """

                # cursor.execute(insert_park, (name, area, json.dumps(geometry)))
                # summary['parks_loaded'] += 1
                pass

        # TODO: Update summary information
        summary['tables_created'] = ['cities', 'parks']

        connection.commit()
        logger.info(f"✅ Data loading completed: {summary}")
        return summary

    except Exception as e:
        # TODO: Handle errors and rollback transaction
        connection.rollback()
        logger.error(f"❌ Data loading failed: {e}")
        raise

    finally:
        cursor.close()


def analyze_spatial_relationships(connection: psycopg2.extensions.connection) -> Dict[str, Any]:
    """
    Perform spatial analysis using PostGIS functions.

    This function demonstrates common spatial analysis patterns used in
    professional GIS workflows including containment, proximity, and measurement.

    Parameters:
        connection: Active database connection

    Returns:
        dict: Analysis results including:
            - cities_in_parks: List of cities within park boundaries
            - average_park_area: Average park area in square kilometers
            - nearest_park_distances: Distance from each city to nearest park (km)
            - total_parks_area: Total area of all parks combined (km²)

    Requirements:
        - Use ST_Contains() to find cities within parks
        - Use ST_Area() to calculate park areas (convert to km²)
        - Use ST_Distance() to find nearest park to each city
        - Convert all distance/area measurements to metric units
        - Return organized results dictionary

    Professional Notes:
        - Always specify units for measurements
        - Use ST_Distance_Sphere() for accurate Earth distances
        - Consider projection effects when measuring areas
        - Index spatial tables before running complex queries
    """

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    results = {
        'cities_in_parks': [],
        'average_park_area': 0.0,
        'nearest_park_distances': {},
        'total_parks_area': 0.0
    }

    try:
        # TODO: Find cities within park boundaries
        cities_in_parks_query = """
        -- TODO: Write SQL query using ST_Contains()
        -- Select city name and park name where park contains city
        -- JOIN cities and parks tables spatially
        """

        # TODO: Execute query and process results
        # cursor.execute(cities_in_parks_query)
        # for row in cursor.fetchall():
        #     results['cities_in_parks'].append({
        #         'city': row['city_name'],
        #         'park': row['park_name']
        #     })

        # TODO: Calculate average park area in square kilometers
        average_area_query = """
        -- TODO: Write SQL to calculate average park area
        -- Use ST_Area() and convert to square kilometers
        -- Remember: ST_Area() returns square meters for EPSG:4326 approximation
        -- Convert to km² by dividing by 1,000,000
        """

        # TODO: Execute and store average area
        # cursor.execute(average_area_query)
        # results['average_park_area'] = cursor.fetchone()[0] or 0.0

        # TODO: Calculate total parks area
        total_area_query = """
        -- TODO: Write SQL to sum all park areas
        -- Use SUM(ST_Area()) and convert to km²
        """

        # TODO: Find nearest park distance for each city
        nearest_park_query = """
        -- TODO: Write SQL to find nearest park to each city
        -- Use ST_Distance_Sphere() for accurate Earth distances
        -- Consider using DISTINCT ON or window functions
        -- Convert distance to kilometers (ST_Distance_Sphere returns meters)
        """

        # TODO: Execute and process nearest park results
        # cursor.execute(nearest_park_query)
        # for row in cursor.fetchall():
        #     results['nearest_park_distances'][row['city_name']] = {
        #         'nearest_park': row['park_name'],
        #         'distance_km': round(row['distance_m'] / 1000, 2)
        #     }

        logger.info(f"✅ Spatial analysis completed: {len(results['cities_in_parks'])} spatial relationships found")
        return results

    except Exception as e:
        logger.error(f"❌ Spatial analysis failed: {e}")
        raise

    finally:
        cursor.close()


def export_analysis_results(connection: psycopg2.extensions.connection,
                          output_directory: str) -> Dict[str, Any]:
    """
    Export analysis results to multiple formats for stakeholder delivery.

    This function demonstrates data export patterns used in professional
    GIS workflows to share results with different audiences and systems.

    Parameters:
        connection: Active database connection
        output_directory: Directory path for output files

    Returns:
        dict: Export summary including:
            - files_created: List of output file paths
            - record_counts: Number of records in each export
            - formats_exported: List of formats created
            - export_success: Boolean indicating overall success

    Requirements:
        - Export cities table to CSV with coordinates
        - Export parks table to GeoJSON format
        - Create summary report (TXT file) with analysis statistics
        - Validate exported data matches database content
        - Create output directory if it doesn't exist

    Professional Notes:
        - Always validate exports against source data
        - Include metadata and coordinate system information
        - Consider file size limits for different formats
        - Document export parameters for reproducibility
    """

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # TODO: Create output directory if it doesn't exist
    # Use pathlib.Path for cross-platform compatibility
    output_path = Path(output_directory)
    # output_path.mkdir(parents=True, exist_ok=True)

    export_summary = {
        'files_created': [],
        'record_counts': {},
        'formats_exported': [],
        'export_success': False
    }

    try:
        # TODO: Export cities to CSV with coordinates
        cities_csv_path = output_path / 'cities_export.csv'

        # TODO: Query cities with coordinates
        cities_query = """
        -- TODO: Write SQL to select cities with lat/lng coordinates
        -- Use ST_X() and ST_Y() to extract coordinates from geometry
        -- Include all city attributes plus extracted coordinates
        """

        # TODO: Execute query and write CSV
        # cursor.execute(cities_query)
        # cities_data = cursor.fetchall()

        # with open(cities_csv_path, 'w', newline='') as csvfile:
        #     if cities_data:
        #         writer = csv.DictWriter(csvfile, fieldnames=cities_data[0].keys())
        #         writer.writeheader()
        #         for row in cities_data:
        #             writer.writerow(row)

        # export_summary['record_counts']['cities'] = len(cities_data)
        # export_summary['files_created'].append(str(cities_csv_path))

        # TODO: Export parks to GeoJSON
        parks_geojson_path = output_path / 'parks_export.geojson'

        parks_query = """
        -- TODO: Write SQL to export parks as GeoJSON
        -- Use ST_AsGeoJSON() to convert geometry
        -- Include all park attributes
        """

        # TODO: Execute query and build GeoJSON structure
        # cursor.execute(parks_query)
        # parks_data = cursor.fetchall()

        # geojson_output = {
        #     "type": "FeatureCollection",
        #     "features": []
        # }

        # for row in parks_data:
        #     feature = {
        #         "type": "Feature",
        #         "geometry": json.loads(row['geojson']),
        #         "properties": {
        #             "name": row['name'],
        #             "area_sqm": row['area_sqm']
        #         }
        #     }
        #     geojson_output["features"].append(feature)

        # with open(parks_geojson_path, 'w') as f:
        #     json.dump(geojson_output, f, indent=2)

        # TODO: Create summary report
        summary_path = output_path / 'analysis_summary.txt'

        # TODO: Query database statistics
        stats_queries = {
            'total_cities': "SELECT COUNT(*) FROM cities",
            'total_parks': "SELECT COUNT(*) FROM parks",
            'total_park_area': "SELECT SUM(ST_Area(geom))/1000000 as area_km2 FROM parks"
        }

        summary_stats = {}
        # for stat_name, query in stats_queries.items():
        #     cursor.execute(query)
        #     summary_stats[stat_name] = cursor.fetchone()[0]

        # TODO: Write summary report
        summary_content = f"""
PostGIS Analysis Summary Report
Generated: {os.getcwd()}
Database: gis_analysis

=== DATA OVERVIEW ===
Total Cities: {summary_stats.get('total_cities', 0)}
Total Parks: {summary_stats.get('total_parks', 0)}
Total Park Area: {summary_stats.get('total_park_area', 0):.2f} km²

=== EXPORT FILES ===
Cities CSV: {cities_csv_path}
Parks GeoJSON: {parks_geojson_path}

=== COORDINATE SYSTEM ===
EPSG:4326 (WGS 84 Geographic)
Units: Degrees (coordinates), Square meters (area)

=== ANALYSIS NOTES ===
- All distances calculated using spherical Earth model
- Area calculations are approximate for geographic coordinates
- For precise measurements, consider projected coordinate systems
        """

        # with open(summary_path, 'w') as f:
        #     f.write(summary_content)

        # TODO: Validate exports
        # Check file sizes, record counts match database

        # TODO: Update export summary
        export_summary['formats_exported'] = ['CSV', 'GeoJSON', 'TXT']
        export_summary['files_created'].extend([
            str(parks_geojson_path),
            str(summary_path)
        ])
        export_summary['export_success'] = True

        logger.info(f"✅ Export completed: {len(export_summary['files_created'])} files created")
        return export_summary

    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
        export_summary['export_success'] = False
        raise

    finally:
        cursor.close()


# Helper functions for common operations
def _validate_connection(connection: psycopg2.extensions.connection) -> bool:
    """
    Validate that a database connection is active and working.

    Parameters:
        connection: Database connection to validate

    Returns:
        bool: True if connection is valid, False otherwise
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        return True
    except:
        return False


def _format_area_km2(area_m2: float) -> float:
    """
    Convert square meters to square kilometers with appropriate precision.

    Parameters:
        area_m2: Area in square meters

    Returns:
        float: Area in square kilometers, rounded to 2 decimal places
    """
    if area_m2 is None:
        return 0.0
    return round(area_m2 / 1_000_000, 2)


def _format_distance_km(distance_m: float) -> float:
    """
    Convert meters to kilometers with appropriate precision.

    Parameters:
        distance_m: Distance in meters

    Returns:
        float: Distance in kilometers, rounded to 2 decimal places
    """
    if distance_m is None:
        return 0.0
    return round(distance_m / 1000, 2)


if __name__ == "__main__":
    """
    Test the functions locally during development.
    This section won't run during automated testing.
    """

    print("🧪 Testing PostGIS functions locally...")

    try:
        # Test database connection
        conn = connect_to_postgis()
        print("✅ Database connection successful")

        # Test data loading (if data files exist)
        # Uncomment when you have sample data files
        # summary = load_spatial_data(conn, 'data/sample_cities.csv', 'data/sample_parks.geojson')
        # print(f"✅ Data loading: {summary}")

        # Test spatial analysis
        # analysis = analyze_spatial_relationships(conn)
        # print(f"✅ Spatial analysis: {analysis}")

        # Test export
        # export_result = export_analysis_results(conn, 'output')
        # print(f"✅ Export: {export_result}")

        conn.close()
        print("✅ All tests completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 This is normal during initial development - implement the TODO sections!")
