-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Advanced Spatial Data
-- ===================================================================
--
-- This script creates comprehensive spatial datasets for advanced
-- PostGIS spatial analysis operations and workflows.
--
-- Dataset Theme: Colorado Rocky Mountain Region
-- Focus: National Parks, Transportation, Environmental Monitoring
--
-- Tables Created:
-- - protected_areas: National parks and wilderness areas (POLYGONS)
-- - transportation_network: Roads, trails, waterways (LINESTRINGS)
-- - facilities: Visitor centers, campgrounds, ranger stations (POINTS)
-- - monitoring_stations: Environmental and weather monitoring (POINTS)
-- - land_use_zones: Management and zoning areas (POLYGONS)
-- - watersheds: River basins and drainage areas (POLYGONS)
--
-- Coordinate Systems:
-- - WGS84 (EPSG:4326) for latitude/longitude data
-- - Colorado State Plane Central (EPSG:3501) for projected analysis
-- - UTM Zone 13N (EPSG:26913) for metric measurements
--
-- Usage: Automatically loaded by Docker initialization
-- ===================================================================

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Drop existing tables if they exist (for clean reloads)
DROP TABLE IF EXISTS monitoring_stations CASCADE;
DROP TABLE IF EXISTS facilities CASCADE;
DROP TABLE IF EXISTS transportation_network CASCADE;
DROP TABLE IF EXISTS land_use_zones CASCADE;
DROP TABLE IF EXISTS watersheds CASCADE;
DROP TABLE IF EXISTS protected_areas CASCADE;

-- ===================================================================
-- TABLE: protected_areas
-- National parks, wilderness areas, and protected lands (POLYGONS)
-- ===================================================================

CREATE TABLE protected_areas (
    area_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    established_year INTEGER,
    area_acres DECIMAL(12,2),
    management_agency VARCHAR(100),
    protection_level VARCHAR(30),
    visitor_count_annual INTEGER,
    geometry GEOMETRY(MULTIPOLYGON, 4326)
);

-- Create spatial index
CREATE INDEX idx_protected_areas_geom ON protected_areas USING GIST (geometry);

INSERT INTO protected_areas (name, designation, established_year, area_acres, management_agency, protection_level, visitor_count_annual, geometry) VALUES
-- Rocky Mountain National Park
('Rocky Mountain National Park', 'National Park', 1915, 265807, 'National Park Service', 'Strict Nature Reserve', 4400000,
 ST_GeomFromText('MULTIPOLYGON(((-105.6 40.15, -105.4 40.15, -105.4 40.45, -105.6 40.45, -105.6 40.15)))', 4326)),

-- Great Sand Dunes National Park
('Great Sand Dunes National Park', 'National Park', 2004, 107341, 'National Park Service', 'Strict Nature Reserve', 450000,
 ST_GeomFromText('MULTIPOLYGON(((-105.6 37.65, -105.4 37.65, -105.4 37.85, -105.6 37.85, -105.6 37.65)))', 4326)),

-- Mesa Verde National Park
('Mesa Verde National Park', 'National Park', 1906, 52485, 'National Park Service', 'Cultural Heritage', 530000,
 ST_GeomFromText('MULTIPOLYGON(((-108.6 37.15, -108.3 37.15, -108.3 37.35, -108.6 37.35, -108.6 37.15)))', 4326)),

-- Black Canyon of the Gunnison National Park
('Black Canyon of Gunnison National Park', 'National Park', 1999, 30779, 'National Park Service', 'Strict Nature Reserve', 310000,
 ST_GeomFromText('MULTIPOLYGON(((-107.8 38.5, -107.6 38.5, -107.6 38.7, -107.8 38.7, -107.8 38.5)))', 4326)),

-- Indian Peaks Wilderness
('Indian Peaks Wilderness', 'Wilderness Area', 1978, 76711, 'US Forest Service', 'Wilderness', 250000,
 ST_GeomFromText('MULTIPOLYGON(((-105.7 39.95, -105.5 39.95, -105.5 40.15, -105.7 40.15, -105.7 39.95)))', 4326)),

-- Mount Evans Wilderness
('Mount Evans Wilderness', 'Wilderness Area', 1980, 74401, 'US Forest Service', 'Wilderness', 180000,
 ST_GeomFromText('MULTIPOLYGON(((-105.7 39.55, -105.5 39.55, -105.5 39.75, -105.7 39.75, -105.7 39.55)))', 4326)),

-- Dinosaur National Monument
('Dinosaur National Monument', 'National Monument', 1915, 210278, 'National Park Service', 'Natural Monument', 220000,
 ST_GeomFromText('MULTIPOLYGON(((-109.1 40.35, -108.7 40.35, -108.7 40.65, -109.1 40.65, -109.1 40.35)))', 4326)),

-- Colorado National Monument
('Colorado National Monument', 'National Monument', 1911, 20454, 'National Park Service', 'Natural Monument', 400000,
 ST_GeomFromText('MULTIPOLYGON(((-108.8 39.0, -108.6 39.0, -108.6 39.2, -108.8 39.2, -108.8 39.0)))', 4326));

-- ===================================================================
-- TABLE: watersheds
-- River basins and drainage areas (POLYGONS)
-- ===================================================================

CREATE TABLE watersheds (
    watershed_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    basin_type VARCHAR(30) NOT NULL,
    drainage_area_sqmi DECIMAL(10,2),
    avg_elevation_ft INTEGER,
    primary_river VARCHAR(50),
    flow_direction VARCHAR(20),
    geometry GEOMETRY(MULTIPOLYGON, 4326)
);

CREATE INDEX idx_watersheds_geom ON watersheds USING GIST (geometry);

INSERT INTO watersheds (name, basin_type, drainage_area_sqmi, avg_elevation_ft, primary_river, flow_direction, geometry) VALUES
-- Colorado River Basin
('Upper Colorado River Basin', 'Major Basin', 17800, 7200, 'Colorado River', 'Southwest',
 ST_GeomFromText('MULTIPOLYGON(((-109.2 39.0, -107.0 39.0, -107.0 41.0, -109.2 41.0, -109.2 39.0)))', 4326)),

-- South Platte River Basin
('South Platte River Basin', 'Major Basin', 24300, 6800, 'South Platte River', 'Northeast',
 ST_GeomFromText('MULTIPOLYGON(((-106.5 39.0, -104.0 39.0, -104.0 41.2, -106.5 41.2, -106.5 39.0)))', 4326)),

-- Arkansas River Basin
('Arkansas River Basin', 'Major Basin', 25000, 8100, 'Arkansas River', 'Southeast',
 ST_GeomFromText('MULTIPOLYGON(((-109.0 37.0, -102.0 37.0, -102.0 39.5, -109.0 39.5, -109.0 37.0)))', 4326)),

-- Rio Grande Basin
('Rio Grande Basin', 'Major Basin', 8000, 8900, 'Rio Grande', 'South',
 ST_GeomFromText('MULTIPOLYGON(((-107.5 37.0, -105.5 37.0, -105.5 38.0, -107.5 38.0, -107.5 37.0)))', 4326));

-- ===================================================================
-- TABLE: land_use_zones
-- Management zones and land use classifications (POLYGONS)
-- ===================================================================

CREATE TABLE land_use_zones (
    zone_id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    zone_type VARCHAR(50) NOT NULL,
    management_intensity VARCHAR(30),
    recreational_use VARCHAR(50),
    area_acres DECIMAL(10,2),
    elevation_range_ft VARCHAR(20),
    geometry GEOMETRY(MULTIPOLYGON, 4326)
);

CREATE INDEX idx_land_use_zones_geom ON land_use_zones USING GIST (geometry);

INSERT INTO land_use_zones (zone_name, zone_type, management_intensity, recreational_use, area_acres, elevation_range_ft, geometry) VALUES
-- High Elevation Alpine Zones
('Alpine Tundra Zone', 'Ecological Zone', 'Minimal', 'Hiking Only', 125000, '11000-14000',
 ST_GeomFromText('MULTIPOLYGON(((-105.8 40.0, -105.2 40.0, -105.2 40.4, -105.8 40.4, -105.8 40.0)))', 4326)),

-- Forest Management Areas
('Subalpine Forest Zone', 'Forest Management', 'Moderate', 'Multiple Use', 320000, '9000-11000',
 ST_GeomFromText('MULTIPOLYGON(((-106.0 39.5, -105.0 39.5, -105.0 40.5, -106.0 40.5, -106.0 39.5)))', 4326)),

-- Recreation Management Areas
('Front Range Recreation Area', 'Recreation Management', 'High', 'Heavy Recreation', 85000, '5500-9000',
 ST_GeomFromText('MULTIPOLYGON(((-105.5 39.0, -104.5 39.0, -104.5 40.0, -105.5 40.0, -105.5 39.0)))', 4326)),

-- Wildlife Habitat Areas
('Critical Wildlife Habitat', 'Wildlife Management', 'Minimal', 'Seasonal Restrictions', 180000, '7000-10000',
 ST_GeomFromText('MULTIPOLYGON(((-107.0 38.0, -106.0 38.0, -106.0 39.0, -107.0 39.0, -107.0 38.0)))', 4326)),

-- Desert Ecosystem Areas
('Desert Shrubland Zone', 'Ecosystem Management', 'Low', 'Limited Recreation', 220000, '4000-7000',
 ST_GeomFromText('MULTIPOLYGON(((-108.5 37.0, -107.0 37.0, -107.0 38.5, -108.5 38.5, -108.5 37.0)))', 4326));

-- ===================================================================
-- TABLE: transportation_network
-- Roads, trails, and waterways (LINESTRINGS)
-- ===================================================================

CREATE TABLE transportation_network (
    route_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    route_type VARCHAR(30) NOT NULL,
    surface_type VARCHAR(30),
    difficulty_level VARCHAR(20),
    length_miles DECIMAL(8,2),
    elevation_gain_ft INTEGER,
    seasonal_closure BOOLEAN DEFAULT FALSE,
    maintenance_agency VARCHAR(50),
    geometry GEOMETRY(MULTILINESTRING, 4326)
);

CREATE INDEX idx_transportation_geom ON transportation_network USING GIST (geometry);

INSERT INTO transportation_network (name, route_type, surface_type, difficulty_level, length_miles, elevation_gain_ft, seasonal_closure, maintenance_agency, geometry) VALUES
-- Major Highways
('Interstate 70', 'Interstate Highway', 'Paved', 'Easy', 424, 5200, FALSE, 'Colorado Department of Transportation',
 ST_GeomFromText('MULTILINESTRING((-109.0 39.1, -107.5 39.3, -106.0 39.7, -104.0 39.8))', 4326)),

('US Highway 6', 'US Highway', 'Paved', 'Moderate', 180, 8500, TRUE, 'Colorado Department of Transportation',
 ST_GeomFromText('MULTILINESTRING((-105.8 39.6, -105.4 39.7, -105.0 39.6, -104.2 39.5))', 4326)),

-- Scenic Drives
('Trail Ridge Road', 'Scenic Highway', 'Paved', 'Challenging', 48, 4100, TRUE, 'National Park Service',
 ST_GeomFromText('MULTILINESTRING((-105.6 40.2, -105.5 40.25, -105.4 40.3, -105.35 40.32))', 4326)),

-- Hiking Trails
('Continental Divide Trail', 'Long Distance Trail', 'Natural Surface', 'Very Difficult', 760, 89000, TRUE, 'US Forest Service',
 ST_GeomFromText('MULTILINESTRING((-105.7 40.4, -105.6 40.0, -105.8 39.5, -106.0 39.0, -106.2 38.5, -106.5 38.0, -107.0 37.5))', 4326)),

('Colorado Trail', 'Long Distance Trail', 'Natural Surface', 'Difficult', 486, 76000, TRUE, 'Colorado Trail Foundation',
 ST_GeomFromText('MULTILINESTRING((-105.0 39.0, -105.3 39.2, -105.7 39.5, -106.0 39.8, -106.5 40.0, -107.0 40.2))', 4326)),

('Longs Peak Trail', 'Day Hike Trail', 'Natural Surface', 'Very Difficult', 14.5, 5100, TRUE, 'National Park Service',
 ST_GeomFromText('MULTILINESTRING((-105.55 40.25, -105.52 40.28, -105.48 40.30, -105.46 40.32))', 4326)),

-- Waterways
('Colorado River', 'Major River', 'Water', 'N/A', 225, 0, FALSE, 'US Bureau of Reclamation',
 ST_GeomFromText('MULTILINESTRING((-105.8 40.1, -106.2 39.9, -106.8 39.5, -107.5 39.2, -108.2 39.0, -109.0 39.1))', 4326)),

('South Platte River', 'Major River', 'Water', 'N/A', 180, 0, FALSE, 'Colorado Water Conservation Board',
 ST_GeomFromText('MULTILINESTRING((-105.4 39.3, -105.0 39.4, -104.5 39.6, -104.0 39.8))', 4326));

-- ===================================================================
-- TABLE: facilities
-- Visitor centers, campgrounds, ranger stations (POINTS)
-- ===================================================================

CREATE TABLE facilities (
    facility_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    facility_type VARCHAR(50) NOT NULL,
    capacity INTEGER,
    seasonal_operation BOOLEAN DEFAULT TRUE,
    elevation_ft INTEGER,
    amenities TEXT[],
    contact_phone VARCHAR(15),
    operating_agency VARCHAR(50),
    geometry GEOMETRY(POINT, 4326)
);

CREATE INDEX idx_facilities_geom ON facilities USING GIST (geometry);

INSERT INTO facilities (name, facility_type, capacity, seasonal_operation, elevation_ft, amenities, contact_phone, operating_agency, geometry) VALUES
-- Visitor Centers
('Rocky Mountain National Park Visitor Center', 'Visitor Center', 500, FALSE, 7522,
 ARRAY['Exhibits', 'Gift Shop', 'Restrooms', 'Information Desk', 'Theater'], '970-586-1206', 'National Park Service',
 ST_GeomFromText('POINT(-105.5211 40.3428)', 4326)),

('Great Sand Dunes Visitor Center', 'Visitor Center', 200, FALSE, 8175,
 ARRAY['Exhibits', 'Bookstore', 'Restrooms', 'Junior Ranger Program'], '719-378-6395', 'National Park Service',
 ST_GeomFromText('POINT(-105.5086 37.7307)', 4326)),

('Mesa Verde Visitor Center', 'Visitor Center', 300, FALSE, 7100,
 ARRAY['Archaeological Exhibits', 'Research Library', 'Restrooms', 'Guided Tours'], '970-529-4465', 'National Park Service',
 ST_GeomFromText('POINT(-108.4618 37.1850)', 4326)),

-- Campgrounds
('Moraine Park Campground', 'Campground', 244, TRUE, 8160,
 ARRAY['Tent Sites', 'RV Sites', 'Restrooms', 'Showers', 'Fire Rings', 'Picnic Tables'], '877-444-6777', 'National Park Service',
 ST_GeomFromText('POINT(-105.5192 40.3614)', 4326)),

('Glacier Basin Campground', 'Campground', 150, TRUE, 8590,
 ARRAY['Tent Sites', 'RV Sites', 'Restrooms', 'Fire Rings', 'Food Storage'], '877-444-6777', 'National Park Service',
 ST_GeomFromText('POINT(-105.5567 40.3089)', 4326)),

('Pinyon Flats Campground', 'Campground', 88, TRUE, 8175,
 ARRAY['Tent Sites', 'RV Sites', 'Restrooms', 'Group Sites'], '877-444-6777', 'National Park Service',
 ST_GeomFromText('POINT(-105.5214 37.7389)', 4326)),

-- Ranger Stations
('Bear Lake Ranger Station', 'Ranger Station', 10, TRUE, 9475,
 ARRAY['Permits', 'Information', 'First Aid', 'Emergency Phone'], '970-586-1206', 'National Park Service',
 ST_GeomFromText('POINT(-105.6444 40.3131)', 4326)),

('Kawuneeche Valley Ranger Station', 'Ranger Station', 8, TRUE, 8720,
 ARRAY['Permits', 'Information', 'Emergency Services'], '970-627-3471', 'National Park Service',
 ST_GeomFromText('POINT(-105.8231 40.2533)', 4326)),

-- Mountain Huts
('Colorado Mountain Club Hut', 'Mountain Hut', 16, TRUE, 10200,
 ARRAY['Sleeping Quarters', 'Kitchen', 'Emergency Shelter'], '303-279-3080', 'Colorado Mountain Club',
 ST_GeomFromText('POINT(-105.6125 40.0889)', 4326)),

-- Research Stations
('Niwot Ridge Research Station', 'Research Station', 20, FALSE, 10056,
 ARRAY['Laboratory', 'Weather Monitoring', 'Research Equipment'], '303-492-5487', 'University of Colorado',
 ST_GeomFromText('POINT(-105.5864 40.0528)', 4326));

-- ===================================================================
-- TABLE: monitoring_stations
-- Environmental and weather monitoring stations (POINTS)
-- ===================================================================

CREATE TABLE monitoring_stations (
    station_id SERIAL PRIMARY KEY,
    station_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    monitoring_type VARCHAR(50) NOT NULL,
    installation_date DATE,
    elevation_ft INTEGER,
    measurement_frequency VARCHAR(30),
    parameters_monitored TEXT[],
    data_quality_rating VARCHAR(20),
    operating_agency VARCHAR(50),
    last_maintenance DATE,
    geometry GEOMETRY(POINT, 4326)
);

CREATE INDEX idx_monitoring_stations_geom ON monitoring_stations USING GIST (geometry);

INSERT INTO monitoring_stations (station_code, name, monitoring_type, installation_date, elevation_ft, measurement_frequency, parameters_monitored, data_quality_rating, operating_agency, last_maintenance, geometry) VALUES
-- Weather Monitoring
('RMNP001', 'Rocky Mountain NP Alpine Station', 'Weather', '2010-05-15', 11400, 'Continuous',
 ARRAY['Temperature', 'Precipitation', 'Wind Speed', 'Snow Depth', 'Solar Radiation'], 'High Quality', 'National Weather Service', '2024-08-15',
 ST_GeomFromText('POINT(-105.6458 40.2742)', 4326)),

('GSDNP002', 'Great Sand Dunes Climate Station', 'Weather', '2008-03-20', 8200, 'Hourly',
 ARRAY['Temperature', 'Humidity', 'Wind Speed', 'Barometric Pressure'], 'High Quality', 'National Weather Service', '2024-07-22',
 ST_GeomFromText('POINT(-105.5439 37.7275)', 4326)),

-- Air Quality Monitoring
('AQ_FOCO01', 'Fort Collins Air Quality', 'Air Quality', '2005-09-10', 5003, 'Continuous',
 ARRAY['PM2.5', 'PM10', 'Ozone', 'NO2', 'SO2', 'CO'], 'High Quality', 'Colorado Department of Health', '2024-06-30',
 ST_GeomFromText('POINT(-105.0178 40.5853)', 4326)),

('AQ_DEN01', 'Denver Metro Air Quality', 'Air Quality', '2002-01-15', 5280, 'Continuous',
 ARRAY['PM2.5', 'PM10', 'Ozone', 'NO2', 'Visibility'], 'High Quality', 'Colorado Department of Health', '2024-09-10',
 ST_GeomFromText('POINT(-105.0178 39.7392)', 4326)),

-- Water Quality Monitoring
('WQ_CR001', 'Colorado River Water Quality', 'Water Quality', '2012-06-01', 7200, 'Daily',
 ARRAY['Temperature', 'pH', 'Dissolved Oxygen', 'Turbidity', 'Conductivity'], 'High Quality', 'US Geological Survey', '2024-08-05',
 ST_GeomFromText('POINT(-106.8331 39.5347)', 4326)),

('WQ_SP001', 'South Platte River Water Quality', 'Water Quality', '2009-04-12', 5100, 'Daily',
 ARRAY['Temperature', 'pH', 'Nitrates', 'Phosphorus', 'E. coli'], 'High Quality', 'US Geological Survey', '2024-07-18',
 ST_GeomFromText('POINT(-104.7581 39.7347)', 4326)),

-- Seismic Monitoring
('SEIS_RMNP', 'Rocky Mountain Seismic Station', 'Seismic', '2015-10-01', 8900, 'Continuous',
 ARRAY['Ground Motion', 'Seismic Waves', 'Earthquake Detection'], 'Research Quality', 'US Geological Survey', '2024-05-20',
 ST_GeomFromText('POINT(-105.6042 40.3156)', 4326)),

-- Wildlife Monitoring
('WL_ELK001', 'Elk Population Monitor', 'Wildlife', '2018-08-15', 9200, 'Seasonal',
 ARRAY['Population Count', 'Migration Tracking', 'Habitat Use'], 'Research Quality', 'Colorado Parks and Wildlife', '2024-09-01',
 ST_GeomFromText('POINT(-105.7167 40.1833)', 4326)),

-- Snow Monitoring
('SNTL_001', 'Niwot Ridge SNOTEL', 'Snow', '1990-11-01', 10056, 'Daily',
 ARRAY['Snow Depth', 'Snow Water Equivalent', 'Temperature', 'Precipitation'], 'High Quality', 'Natural Resources Conservation Service', '2024-10-01',
 ST_GeomFromText('POINT(-105.5864 40.0528)', 4326)),

-- Stream Gauge
('USGS_001', 'Big Thompson Creek Gauge', 'Stream Flow', '1985-07-01', 7900, 'Continuous',
 ARRAY['Stream Flow', 'Water Level', 'Water Temperature'], 'High Quality', 'US Geological Survey', '2024-08-28',
 ST_GeomFromText('POINT(-105.5156 40.3789)', 4326));

-- ===================================================================
-- SPATIAL INDEXES AND CONSTRAINTS
-- ===================================================================

-- Add spatial constraints
ALTER TABLE protected_areas ADD CONSTRAINT enforce_dims_protected_areas CHECK (ST_NDims(geometry) = 2);
ALTER TABLE protected_areas ADD CONSTRAINT enforce_srid_protected_areas CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE protected_areas ADD CONSTRAINT enforce_geotype_protected_areas CHECK (GeometryType(geometry) = 'MULTIPOLYGON');

ALTER TABLE watersheds ADD CONSTRAINT enforce_dims_watersheds CHECK (ST_NDims(geometry) = 2);
ALTER TABLE watersheds ADD CONSTRAINT enforce_srid_watersheds CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE watersheds ADD CONSTRAINT enforce_geotype_watersheds CHECK (GeometryType(geometry) = 'MULTIPOLYGON');

ALTER TABLE land_use_zones ADD CONSTRAINT enforce_dims_land_use_zones CHECK (ST_NDims(geometry) = 2);
ALTER TABLE land_use_zones ADD CONSTRAINT enforce_srid_land_use_zones CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE land_use_zones ADD CONSTRAINT enforce_geotype_land_use_zones CHECK (GeometryType(geometry) = 'MULTIPOLYGON');

ALTER TABLE transportation_network ADD CONSTRAINT enforce_dims_transportation CHECK (ST_NDims(geometry) = 2);
ALTER TABLE transportation_network ADD CONSTRAINT enforce_srid_transportation CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE transportation_network ADD CONSTRAINT enforce_geotype_transportation CHECK (GeometryType(geometry) = 'MULTILINESTRING');

ALTER TABLE facilities ADD CONSTRAINT enforce_dims_facilities CHECK (ST_NDims(geometry) = 2);
ALTER TABLE facilities ADD CONSTRAINT enforce_srid_facilities CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE facilities ADD CONSTRAINT enforce_geotype_facilities CHECK (GeometryType(geometry) = 'POINT');

ALTER TABLE monitoring_stations ADD CONSTRAINT enforce_dims_monitoring CHECK (ST_NDims(geometry) = 2);
ALTER TABLE monitoring_stations ADD CONSTRAINT enforce_srid_monitoring CHECK (ST_SRID(geometry) = 4326);
ALTER TABLE monitoring_stations ADD CONSTRAINT enforce_geotype_monitoring CHECK (GeometryType(geometry) = 'POINT');

-- ===================================================================
-- ANALYSIS HELPER VIEWS
-- ===================================================================

-- Create view for high elevation facilities (above 10,000 ft)
CREATE VIEW high_elevation_facilities AS
SELECT facility_id, name, facility_type, elevation_ft, geometry
FROM facilities
WHERE elevation_ft > 10000;

-- Create view for protected areas with high visitation
CREATE VIEW popular_protected_areas AS
SELECT area_id, name, designation, visitor_count_annual, geometry
FROM protected_areas
WHERE visitor_count_annual > 400000;

-- Create view for seasonal transportation routes
CREATE VIEW seasonal_routes AS
SELECT route_id, name, route_type, length_miles, elevation_gain_ft, geometry
FROM transportation_network
WHERE seasonal_closure = TRUE;

-- ===================================================================
-- DATA SUMMARY AND STATISTICS
-- ===================================================================

-- Display summary statistics
SELECT 'Data Loading Summary' as info;

SELECT 'Protected Areas' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM protected_areas
UNION ALL
SELECT 'Watersheds' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM watersheds
UNION ALL
SELECT 'Land Use Zones' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM land_use_zones
UNION ALL
SELECT 'Transportation Network' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM transportation_network
UNION ALL
SELECT 'Facilities' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM facilities
UNION ALL
SELECT 'Monitoring Stations' as table_name, COUNT(*) as record_count,
       ST_Union(geometry) as combined_geometry
FROM monitoring_stations;

-- Display coordinate system information
SELECT 'Coordinate System Check' as info;
SELECT 'EPSG:4326 (WGS84)' as crs_info,
       'All geometries stored in geographic coordinates' as description;

COMMIT;

-- ===================================================================
-- ASSIGNMENT READY: Advanced Spatial Analysis Dataset
--
-- This dataset enables complex spatial analysis exercises including:
-- 1. Multi-layer spatial joins and intersections
-- 2. Buffer analysis across different geometry types
-- 3. Network analysis and routing concepts
-- 4. Environmental impact assessment workflows
-- 5. Multi-criteria spatial decision making
-- 6. Coordinate system transformations
-- 7. Spatial aggregation and statistical analysis
-- 8. Advanced geometric operations and validation
-- 9. Performance optimization with spatial indexing
-- 10. Real-world GIS problem solving scenarios
-- ===================================================================
