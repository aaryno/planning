-- ===================================================================
-- PostGIS Basics - Spatial Data Initialization
-- ===================================================================
--
-- This script initializes a PostGIS database with spatial data
-- for learning fundamental PostGIS operations and spatial SQL
--
-- ===================================================================

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- ===================================================================
-- TABLE 1: US CITIES (Point Geometries in WGS84)
-- ===================================================================

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    population INTEGER,
    geom GEOMETRY(POINT, 4326)
);

INSERT INTO cities (name, state_code, population, geom) VALUES
    ('Seattle', 'WA', 753675, ST_GeomFromText('POINT(-122.3321 47.6062)', 4326)),
    ('Portland', 'OR', 650380, ST_GeomFromText('POINT(-122.6765 45.5152)', 4326)),
    ('San Francisco', 'CA', 873965, ST_GeomFromText('POINT(-122.4194 37.7749)', 4326)),
    ('Los Angeles', 'CA', 3971883, ST_GeomFromText('POINT(-118.2437 34.0522)', 4326)),
    ('Denver', 'CO', 715522, ST_GeomFromText('POINT(-104.9903 39.7392)', 4326)),
    ('Phoenix', 'AZ', 1608139, ST_GeomFromText('POINT(-112.0740 33.4484)', 4326)),
    ('Austin', 'TX', 964254, ST_GeomFromText('POINT(-97.7431 30.2672)', 4326)),
    ('Chicago', 'IL', 2705994, ST_GeomFromText('POINT(-87.6298 41.8781)', 4326)),
    ('New York', 'NY', 8336817, ST_GeomFromText('POINT(-74.0060 40.7128)', 4326)),
    ('Miami', 'FL', 470914, ST_GeomFromText('POINT(-80.1918 25.7617)', 4326)),
    ('Boston', 'MA', 692600, ST_GeomFromText('POINT(-71.0589 42.3601)', 4326)),
    ('Atlanta', 'GA', 498715, ST_GeomFromText('POINT(-84.3880 33.7490)', 4326));

-- ===================================================================
-- TABLE 2: NATIONAL PARKS (Polygon Geometries in WGS84)
-- ===================================================================

CREATE TABLE national_parks (
    park_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    area_sq_km NUMERIC(10,2),
    established_year INTEGER,
    geom GEOMETRY(POLYGON, 4326)
);

INSERT INTO national_parks (name, state_code, area_sq_km, established_year, geom) VALUES
    ('Yellowstone', 'WY', 8983.18, 1872, ST_GeomFromText('POLYGON((-111.1 44.1, -109.9 44.1, -109.9 45.1, -111.1 45.1, -111.1 44.1))', 4326)),
    ('Grand Canyon', 'AZ', 4927.16, 1919, ST_GeomFromText('POLYGON((-112.3 36.0, -111.9 36.0, -111.9 36.3, -112.3 36.3, -112.3 36.0))', 4326)),
    ('Yosemite', 'CA', 3027.07, 1890, ST_GeomFromText('POLYGON((-119.9 37.5, -119.2 37.5, -119.2 38.1, -119.9 38.1, -119.9 37.5))', 4326)),
    ('Great Smoky Mountains', 'TN', 2110.40, 1934, ST_GeomFromText('POLYGON((-83.9 35.4, -83.1 35.4, -83.1 35.8, -83.9 35.8, -83.9 35.4))', 4326)),
    ('Olympic', 'WA', 3733.81, 1938, ST_GeomFromText('POLYGON((-124.5 47.5, -123.2 47.5, -123.2 48.0, -124.5 48.0, -124.5 47.5))', 4326)),
    ('Everglades', 'FL', 6106.61, 1947, ST_GeomFromText('POLYGON((-81.1 25.2, -80.2 25.2, -80.2 25.8, -81.1 25.8, -81.1 25.2))', 4326));

-- ===================================================================
-- TABLE 3: MAJOR HIGHWAYS (LineString Geometries in WGS84)
-- ===================================================================

CREATE TABLE highways (
    highway_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    highway_type VARCHAR(20),
    length_km NUMERIC(10,2),
    geom GEOMETRY(LINESTRING, 4326)
);

INSERT INTO highways (name, highway_type, length_km, geom) VALUES
    ('I-5 (WA Section)', 'Interstate', 444.52, ST_GeomFromText('LINESTRING(-122.3 47.6, -122.4 47.0, -122.9 46.5, -123.1 46.0)', 4326)),
    ('I-10 (TX Section)', 'Interstate', 881.49, ST_GeomFromText('LINESTRING(-106.5 31.8, -104.0 31.0, -101.5 30.5, -99.0 30.0)', 4326)),
    ('Route 101 (CA Coast)', 'US Highway', 1055.18, ST_GeomFromText('LINESTRING(-122.4 37.8, -121.9 36.6, -121.0 35.8, -120.6 34.9)', 4326)),
    ('I-95 (East Coast)', 'Interstate', 1925.74, ST_GeomFromText('LINESTRING(-74.0 40.7, -75.2 39.9, -76.6 39.3, -77.0 38.9)', 4326)),
    ('Route 66 (Historic)', 'US Highway', 3945.21, ST_GeomFromText('LINESTRING(-87.6 41.9, -90.2 39.8, -94.6 39.1, -97.5 35.5)', 4326));

-- ===================================================================
-- TABLE 4: WEATHER STATIONS (Points with Elevation in State Plane)
-- ===================================================================

CREATE TABLE weather_stations (
    station_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_code CHAR(2),
    elevation_m INTEGER,
    station_type VARCHAR(30),
    geom GEOMETRY(POINT, 4326),
    geom_utm GEOMETRY(POINT, 32610)  -- UTM Zone 10N for Western US examples
);

INSERT INTO weather_stations (name, state_code, elevation_m, station_type, geom, geom_utm) VALUES
    ('Seattle WSFO', 'WA', 184, 'Airport', ST_GeomFromText('POINT(-122.3015 47.4502)', 4326), ST_Transform(ST_GeomFromText('POINT(-122.3015 47.4502)', 4326), 32610)),
    ('Portland Intl', 'OR', 9, 'Airport', ST_GeomFromText('POINT(-122.5951 45.5898)', 4326), ST_Transform(ST_GeomFromText('POINT(-122.5951 45.5898)', 4326), 32610)),
    ('San Francisco Intl', 'CA', 4, 'Airport', ST_GeomFromText('POINT(-122.3748 37.6213)', 4326), ST_Transform(ST_GeomFromText('POINT(-122.3748 37.6213)', 4326), 32610)),
    ('Mount Rainier', 'WA', 4392, 'Mountain', ST_GeomFromText('POINT(-121.7269 46.8523)', 4326), ST_Transform(ST_GeomFromText('POINT(-121.7269 46.8523)', 4326), 32610)),
    ('Crater Lake', 'OR', 1883, 'Lake', ST_GeomFromText('POINT(-122.1685 42.8684)', 4326), ST_Transform(ST_GeomFromText('POINT(-122.1685 42.8684)', 4326), 32610)),
    ('Death Valley', 'CA', -86, 'Desert', ST_GeomFromText('POINT(-117.0794 36.5054)', 4326), ST_Transform(ST_GeomFromText('POINT(-117.0794 36.5054)', 4326), 32610)),
    ('Yosemite Valley', 'CA', 1219, 'Valley', ST_GeomFromText('POINT(-119.5383 37.7456)', 4326), ST_Transform(ST_GeomFromText('POINT(-119.5383 37.7456)', 4326), 32610)),
    ('Olympic Peninsula', 'WA', 548, 'Coastal', ST_GeomFromText('POINT(-123.4307 47.8021)', 4326), ST_Transform(ST_GeomFromText('POINT(-123.4307 47.8021)', 4326), 32610));

-- ===================================================================
-- TABLE 5: US STATES (Simple Polygon Boundaries)
-- ===================================================================

CREATE TABLE states (
    state_id SERIAL PRIMARY KEY,
    state_code CHAR(2) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    area_sq_km NUMERIC(12,2),
    geom GEOMETRY(POLYGON, 4326)
);

-- Simplified state boundaries for educational purposes
INSERT INTO states (state_code, state_name, area_sq_km, geom) VALUES
    ('WA', 'Washington', 184661.0, ST_GeomFromText('POLYGON((-124.8 45.5, -116.9 45.5, -116.9 49.0, -124.8 49.0, -124.8 45.5))', 4326)),
    ('OR', 'Oregon', 254799.0, ST_GeomFromText('POLYGON((-124.6 42.0, -116.5 42.0, -116.5 46.3, -124.6 46.3, -124.6 42.0))', 4326)),
    ('CA', 'California', 423967.0, ST_GeomFromText('POLYGON((-124.5 32.5, -114.1 32.5, -114.1 42.0, -124.5 42.0, -124.5 32.5))', 4326)),
    ('TX', 'Texas', 695662.0, ST_GeomFromText('POLYGON((-106.6 25.8, -93.5 25.8, -93.5 36.5, -106.6 36.5, -106.6 25.8))', 4326)),
    ('FL', 'Florida', 170312.0, ST_GeomFromText('POLYGON((-87.6 24.5, -80.0 24.5, -80.0 31.0, -87.6 31.0, -87.6 24.5))', 4326)),
    ('NY', 'New York', 141297.0, ST_GeomFromText('POLYGON((-79.8 40.5, -71.9 40.5, -71.9 45.0, -79.8 45.0, -79.8 40.5))', 4326));

-- ===================================================================
-- CREATE SPATIAL INDEXES (Performance Optimization)
-- ===================================================================

CREATE INDEX idx_cities_geom ON cities USING GIST (geom);
CREATE INDEX idx_parks_geom ON national_parks USING GIST (geom);
CREATE INDEX idx_highways_geom ON highways USING GIST (geom);
CREATE INDEX idx_stations_geom ON weather_stations USING GIST (geom);
CREATE INDEX idx_stations_utm_geom ON weather_stations USING GIST (geom_utm);
CREATE INDEX idx_states_geom ON states USING GIST (geom);

-- ===================================================================
-- CREATE SAMPLE ANALYSIS VIEW (Shows Spatial Joins)
-- ===================================================================

CREATE VIEW cities_in_states AS
SELECT
    c.name AS city_name,
    c.population,
    s.state_name,
    s.state_code
FROM cities c
JOIN states s ON ST_Within(c.geom, s.geom);

-- ===================================================================
-- UPDATE TABLE STATISTICS FOR QUERY OPTIMIZATION
-- ===================================================================

ANALYZE cities;
ANALYZE national_parks;
ANALYZE highways;
ANALYZE weather_stations;
ANALYZE states;

-- ===================================================================
-- VERIFICATION QUERIES (Check data loaded correctly)
-- ===================================================================

-- Display row counts for verification
DO $$
BEGIN
    RAISE NOTICE 'PostGIS Basics Database Initialization Complete:';
    RAISE NOTICE '- Cities: % rows', (SELECT COUNT(*) FROM cities);
    RAISE NOTICE '- National Parks: % rows', (SELECT COUNT(*) FROM national_parks);
    RAISE NOTICE '- Highways: % rows', (SELECT COUNT(*) FROM highways);
    RAISE NOTICE '- Weather Stations: % rows', (SELECT COUNT(*) FROM weather_stations);
    RAISE NOTICE '- States: % rows', (SELECT COUNT(*) FROM states);
    RAISE NOTICE 'PostGIS Version: %', postgis_version();
END$$;
