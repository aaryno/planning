-- =====================================================
-- PostGIS Database Initialization Script
-- GIST 604B - Module 6: PostGIS Spatial Database
-- =====================================================
--
-- This script initializes the PostGIS database environment
-- for the spatial database fundamentals assignment.
--
-- It runs automatically when the Docker container starts,
-- setting up extensions, permissions, and utility functions.
--
-- Author: GIST 604B Course Materials
-- Database: gis_analysis
-- User: gis_student
-- =====================================================

-- Connect to the target database
\c gis_analysis;

-- =====================================================
-- SECTION 1: ENABLE EXTENSIONS
-- =====================================================

-- Enable PostGIS core functionality
-- This adds spatial data types (geometry, geography) and functions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable PostGIS topology support (optional, for advanced operations)
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Enable PostGIS raster support (for future raster assignments)
CREATE EXTENSION IF NOT EXISTS postgis_raster;

-- Enable hstore for key-value storage (useful for flexible attributes)
CREATE EXTENSION IF NOT EXISTS hstore;

-- Enable UUID generation (useful for unique identifiers)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable trigonometric and advanced math functions
CREATE EXTENSION IF NOT EXISTS tablefunc;

-- Display enabled extensions for verification
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('postgis', 'postgis_topology', 'postgis_raster', 'hstore')
ORDER BY extname;

-- =====================================================
-- SECTION 2: USER PERMISSIONS AND SCHEMA SETUP
-- =====================================================

-- Grant necessary permissions to the gis_student user
GRANT USAGE ON SCHEMA public TO gis_student;
GRANT CREATE ON SCHEMA public TO gis_student;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gis_student;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gis_student;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO gis_student;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL PRIVILEGES ON TABLES TO gis_student;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL PRIVILEGES ON SEQUENCES TO gis_student;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT ALL PRIVILEGES ON FUNCTIONS TO gis_student;

-- Create a dedicated schema for student work (optional)
CREATE SCHEMA IF NOT EXISTS student_work;
GRANT ALL PRIVILEGES ON SCHEMA student_work TO gis_student;
ALTER DEFAULT PRIVILEGES IN SCHEMA student_work
  GRANT ALL PRIVILEGES ON TABLES TO gis_student;

-- =====================================================
-- SECTION 3: SPATIAL REFERENCE SYSTEMS
-- =====================================================

-- Verify common spatial reference systems are available
-- EPSG:4326 (WGS 84 Geographic) - Global lat/lon system
-- EPSG:3857 (Web Mercator) - Used by Google Maps, OpenStreetMap
-- EPSG:26912 (UTM Zone 12N NAD83) - Arizona/Western US projected system

-- Check if common SRS are available
DO $$
BEGIN
    -- Check for WGS 84 (should always be available)
    IF NOT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = 4326) THEN
        RAISE EXCEPTION 'EPSG:4326 (WGS 84) not found in spatial_ref_sys table';
    END IF;

    -- Check for Web Mercator
    IF NOT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = 3857) THEN
        RAISE NOTICE 'EPSG:3857 (Web Mercator) not found - this is optional but useful';
    END IF;

    -- Check for UTM Zone 12N (Arizona)
    IF NOT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = 26912) THEN
        RAISE NOTICE 'EPSG:26912 (UTM Zone 12N NAD83) not found - useful for Arizona data';
    END IF;

    RAISE NOTICE 'Spatial reference system check completed';
END $$;

-- =====================================================
-- SECTION 4: UTILITY FUNCTIONS FOR STUDENTS
-- =====================================================

-- Function to convert area from square meters to square kilometers
-- Useful for area calculations in assignment
CREATE OR REPLACE FUNCTION area_sqm_to_sqkm(area_sqm DOUBLE PRECISION)
RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN ROUND((area_sqm / 1000000.0)::numeric, 4)::double precision;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to convert distance from meters to kilometers
-- Useful for distance calculations in assignment
CREATE OR REPLACE FUNCTION distance_m_to_km(distance_m DOUBLE PRECISION)
RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN ROUND((distance_m / 1000.0)::numeric, 3)::double precision;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to get geometry type and SRID information
-- Helpful for students to understand their spatial data
CREATE OR REPLACE FUNCTION describe_geometry(geom geometry)
RETURNS TEXT AS $$
BEGIN
    IF geom IS NULL THEN
        RETURN 'NULL geometry';
    END IF;

    RETURN format('Type: %s, SRID: %s, Dimensions: %s, Valid: %s',
                  ST_GeometryType(geom),
                  ST_SRID(geom),
                  ST_CoordDim(geom),
                  ST_IsValid(geom));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to validate and fix geometries
-- Useful for data quality checks
CREATE OR REPLACE FUNCTION fix_geometry(geom geometry)
RETURNS geometry AS $$
BEGIN
    -- If geometry is already valid, return it
    IF ST_IsValid(geom) THEN
        RETURN geom;
    END IF;

    -- Try to fix invalid geometry
    RETURN ST_MakeValid(geom);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- =====================================================
-- SECTION 5: PERFORMANCE OPTIMIZATION SETTINGS
-- =====================================================

-- Set up some performance-related settings for spatial operations
-- These help with query performance for educational datasets

-- Enable constraint exclusion (helps with partitioned tables)
SET constraint_exclusion = partition;

-- Optimize for spatial operations
SET random_page_cost = 1.1; -- SSDs are faster for random access
SET effective_io_concurrency = 200; -- Higher for SSDs

-- Set work_mem for complex spatial operations
-- This helps with sorting and hash operations in spatial queries
SET work_mem = '64MB';

-- =====================================================
-- SECTION 6: SAMPLE VALIDATION QUERIES
-- =====================================================

-- Create a view showing PostGIS configuration
CREATE OR REPLACE VIEW postgis_info AS
SELECT
    'PostGIS Version' as component,
    PostGIS_Version() as version
UNION ALL
SELECT
    'GEOS Version',
    PostGIS_GEOS_Version()
UNION ALL
SELECT
    'PROJ Version',
    PostGIS_Proj_Version()
UNION ALL
SELECT
    'GDAL Version',
    PostGIS_GDAL_Version()
UNION ALL
SELECT
    'LibXML Version',
    PostGIS_LibXML_Version();

-- Create a view showing available spatial reference systems for Arizona
CREATE OR REPLACE VIEW arizona_srs AS
SELECT
    srid,
    auth_name || ':' || auth_srid as code,
    proj4text,
    CASE
        WHEN proj4text LIKE '%+proj=longlat%' THEN 'Geographic'
        WHEN proj4text LIKE '%+proj=utm%' THEN 'UTM Projected'
        WHEN proj4text LIKE '%+proj=merc%' THEN 'Mercator Projected'
        ELSE 'Other Projected'
    END as projection_type
FROM spatial_ref_sys
WHERE
    -- Common systems for Arizona/Southwest US
    srid IN (4326, 4269, 3857, 26912, 26913, 32612, 32613)
    OR proj4text LIKE '%Arizona%'
ORDER BY srid;

-- =====================================================
-- SECTION 7: LOGGING AND MONITORING SETUP
-- =====================================================

-- Create a simple log table for tracking student database operations
-- This is optional but can help instructors monitor usage
CREATE TABLE IF NOT EXISTS student_activity_log (
    id SERIAL PRIMARY KEY,
    session_id TEXT DEFAULT encode(gen_random_bytes(16), 'hex'),
    operation_type TEXT,
    table_name TEXT,
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    notes TEXT
);

-- Grant permissions on log table
GRANT ALL PRIVILEGES ON TABLE student_activity_log TO gis_student;
GRANT ALL PRIVILEGES ON SEQUENCE student_activity_log_id_seq TO gis_student;

-- Function to log student operations (optional usage)
CREATE OR REPLACE FUNCTION log_student_operation(
    op_type TEXT,
    tbl_name TEXT DEFAULT NULL,
    success_flag BOOLEAN DEFAULT TRUE,
    operation_notes TEXT DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    INSERT INTO student_activity_log (operation_type, table_name, success, notes)
    VALUES (op_type, tbl_name, success_flag, operation_notes);
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SECTION 8: FINAL VERIFICATION AND CLEANUP
-- =====================================================

-- Verify PostGIS installation
SELECT 'PostGIS installation verified: ' || PostGIS_Full_Version() as status;

-- Create a simple test to verify spatial operations work
DO $$
DECLARE
    test_point geometry;
    test_buffer geometry;
    buffer_area double precision;
BEGIN
    -- Create a test point (Phoenix, AZ)
    test_point := ST_SetSRID(ST_MakePoint(-112.0740, 33.4484), 4326);

    -- Create a 1000m buffer around the point
    test_buffer := ST_Buffer(ST_Transform(test_point, 3857), 1000);

    -- Calculate buffer area
    buffer_area := ST_Area(test_buffer);

    -- Log success
    RAISE NOTICE 'PostGIS spatial operations test successful. Buffer area: % sq meters',
                 round(buffer_area);

    -- Log the test operation
    PERFORM log_student_operation('SYSTEM_TEST', 'spatial_operations', TRUE,
                                 'Initial PostGIS functionality verification');
END $$;

-- Set the search path to include public schema
ALTER DATABASE gis_analysis SET search_path = public, student_work;

-- Final status message
SELECT
    'Database initialization completed successfully' as message,
    CURRENT_TIMESTAMP as completed_at,
    CURRENT_USER as initialized_by;

-- Display summary of what was created
SELECT
    'Summary: PostGIS database ready for GIST 604B assignments' as summary,
    (SELECT count(*) FROM pg_extension WHERE extname LIKE 'postgis%') as postgis_extensions,
    (SELECT count(*) FROM pg_proc WHERE proname LIKE '%geometry%') as spatial_functions,
    (SELECT count(*) FROM spatial_ref_sys) as spatial_reference_systems;

-- =====================================================
-- END OF INITIALIZATION SCRIPT
-- =====================================================
