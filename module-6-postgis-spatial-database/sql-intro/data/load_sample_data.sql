-- ===================================================================
-- SQL Introduction Assignment - Sample Data Initialization
-- ===================================================================
--
-- This script creates sample tables and loads realistic data for
-- practicing SQL fundamentals before learning PostGIS spatial functions.
--
-- Tables Created:
-- - cities: Major US cities with population and location data
-- - state_info: US state information and regional data
-- - weather_stations: Weather monitoring stations linked to cities
-- - temperature_readings: Daily temperature measurements
--
-- Usage: This script is automatically loaded by Docker initialization
-- ===================================================================

-- Drop existing tables if they exist (for clean reloads)
DROP TABLE IF EXISTS temperature_readings CASCADE;
DROP TABLE IF EXISTS weather_stations CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS state_info CASCADE;

-- ===================================================================
-- TABLE: state_info
-- Basic information about US states including regions and history
-- ===================================================================

CREATE TABLE state_info (
    state_code CHAR(2) PRIMARY KEY,
    state_name VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL,
    area_sq_miles INTEGER NOT NULL,
    statehood_year INTEGER NOT NULL,
    capital VARCHAR(50)
);

INSERT INTO state_info (state_code, state_name, region, area_sq_miles, statehood_year, capital) VALUES
('CA', 'California', 'West', 163696, 1850, 'Sacramento'),
('TX', 'Texas', 'South', 268596, 1845, 'Austin'),
('NY', 'New York', 'Northeast', 54555, 1788, 'Albany'),
('FL', 'Florida', 'South', 65758, 1845, 'Tallahassee'),
('IL', 'Illinois', 'Midwest', 57914, 1818, 'Springfield'),
('PA', 'Pennsylvania', 'Northeast', 46054, 1787, 'Harrisburg'),
('OH', 'Ohio', 'Midwest', 44826, 1803, 'Columbus'),
('GA', 'Georgia', 'South', 59425, 1788, 'Atlanta'),
('NC', 'North Carolina', 'South', 53819, 1789, 'Raleigh'),
('MI', 'Michigan', 'Midwest', 96714, 1837, 'Lansing'),
('WA', 'Washington', 'West', 71298, 1889, 'Olympia'),
('AZ', 'Arizona', 'West', 113990, 1912, 'Phoenix'),
('MA', 'Massachusetts', 'Northeast', 10554, 1788, 'Boston'),
('TN', 'Tennessee', 'South', 42144, 1796, 'Nashville'),
('IN', 'Indiana', 'Midwest', 36420, 1816, 'Indianapolis'),
('MO', 'Missouri', 'Midwest', 69707, 1821, 'Jefferson City'),
('MD', 'Maryland', 'Northeast', 12406, 1788, 'Annapolis'),
('WI', 'Wisconsin', 'Midwest', 65496, 1848, 'Madison'),
('CO', 'Colorado', 'West', 104094, 1876, 'Denver'),
('MN', 'Minnesota', 'Midwest', 86936, 1858, 'Saint Paul'),
('SC', 'South Carolina', 'South', 32020, 1788, 'Columbia'),
('AL', 'Alabama', 'South', 52420, 1819, 'Montgomery'),
('LA', 'Louisiana', 'South', 52378, 1812, 'Baton Rouge'),
('KY', 'Kentucky', 'South', 40408, 1792, 'Frankfort'),
('OR', 'Oregon', 'West', 98379, 1859, 'Salem'),
('OK', 'Oklahoma', 'South', 69899, 1907, 'Oklahoma City'),
('CT', 'Connecticut', 'Northeast', 5543, 1788, 'Hartford'),
('UT', 'Utah', 'West', 84897, 1896, 'Salt Lake City'),
('NV', 'Nevada', 'West', 110572, 1864, 'Carson City'),
('NM', 'New Mexico', 'West', 121590, 1912, 'Santa Fe');

-- ===================================================================
-- TABLE: cities
-- Major US cities with population, coordinates, and elevation data
-- ===================================================================

CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL REFERENCES state_info(state_code),
    population INTEGER NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    elevation_ft INTEGER,
    founded_year INTEGER,
    metro_population INTEGER
);

INSERT INTO cities (name, state_code, population, latitude, longitude, elevation_ft, founded_year, metro_population) VALUES
-- Large Cities (Population > 1 million)
('New York', 'NY', 8336817, 40.7128, -74.0060, 33, 1624, 20140470),
('Los Angeles', 'CA', 3979576, 34.0522, -118.2437, 285, 1781, 13200998),
('Chicago', 'IL', 2693976, 41.8781, -87.6298, 594, 1837, 9618502),
('Houston', 'TX', 2320268, 29.7604, -95.3698, 80, 1836, 7066141),
('Phoenix', 'AZ', 1680992, 33.4484, -112.0740, 1086, 1868, 4845832),
('Philadelphia', 'PA', 1584200, 39.9526, -75.1652, 39, 1682, 6102434),
('San Antonio', 'TX', 1547253, 29.4241, -98.4936, 650, 1718, 2550960),
('San Diego', 'CA', 1423851, 32.7157, -117.1611, 62, 1769, 3338330),
('Dallas', 'TX', 1343573, 32.7767, -96.7970, 430, 1841, 7637387),
('San Jose', 'CA', 1021795, 37.3382, -121.8863, 82, 1777, 7026000),

-- Medium Cities (Population 500k - 1 million)
('Austin', 'TX', 978908, 30.2672, -97.7431, 489, 1839, 2283371),
('Jacksonville', 'FL', 911507, 30.3322, -81.6557, 16, 1822, 1605848),
('Fort Worth', 'TX', 918915, 32.7555, -97.3308, 653, 1849, 2635457),
('Columbus', 'OH', 898553, 39.9612, -82.9988, 760, 1812, 2138926),
('Charlotte', 'NC', 885708, 35.2271, -80.8431, 751, 1768, 2797636),
('San Francisco', 'CA', 881549, 37.7749, -122.4194, 52, 1776, 4749008),
('Indianapolis', 'IN', 876384, 39.7684, -86.1581, 718, 1821, 2111040),
('Seattle', 'WA', 753675, 47.6062, -122.3321, 173, 1851, 4018762),
('Denver', 'CO', 715522, 39.7392, -104.9903, 5280, 1858, 2963821),
('Boston', 'MA', 694583, 42.3601, -71.0589, 141, 1630, 4873019),
('El Paso', 'TX', 695044, 31.7619, -106.4850, 3740, 1659, 868859),
('Detroit', 'MI', 670031, 42.3314, -83.0458, 574, 1701, 4392041),
('Nashville', 'TN', 695144, 36.1627, -86.7816, 597, 1779, 2012062),
('Memphis', 'TN', 633104, 35.1495, -90.0490, 337, 1819, 1348260),
('Portland', 'OR', 652503, 45.5152, -122.6784, 173, 1845, 2492412),
('Oklahoma City', 'OK', 695044, 35.4676, -97.5164, 1201, 1889, 1396445),
('Las Vegas', 'NV', 648224, 36.1699, -115.1398, 2001, 1905, 2266715),
('Louisville', 'KY', 617638, 38.2527, -85.7585, 466, 1778, 1297310),
('Baltimore', 'MD', 576498, 39.2904, -76.6122, 146, 1729, 2844510),
('Milwaukee', 'WI', 577222, 43.0389, -87.9065, 594, 1846, 1575179),

-- Smaller Cities (Population 100k - 500k)
('Albuquerque', 'NM', 560513, 35.0844, -106.6504, 5312, 1706, 916528),
('Tucson', 'AZ', 548073, 32.2226, -110.9747, 2389, 1775, 1043433),
('Fresno', 'CA', 542107, 36.7378, -119.7871, 328, 1872, 999101),
('Sacramento', 'CA', 513624, 38.5816, -121.4944, 30, 1848, 2397382),
('Kansas City', 'MO', 508090, 39.0997, -94.5786, 910, 1838, 2157990),
('Mesa', 'AZ', 504258, 33.4152, -111.8315, 1243, 1878, 4845832),
('Atlanta', 'GA', 498715, 33.7490, -84.3880, 1050, 1837, 6020364),
('Virginia Beach', 'VA', 459470, 36.8529, -75.9780, 12, 1963, 1780975),
('Omaha', 'NE', 486051, 41.2565, -95.9345, 1090, 1854, 967604),
('Colorado Springs', 'CO', 478961, 38.8339, -104.8214, 6035, 1871, 738939),
('Raleigh', 'NC', 474069, 35.7796, -78.6382, 315, 1792, 1390785),
('Miami', 'FL', 467963, 25.7617, -80.1918, 6, 1896, 6138333),
('Long Beach', 'CA', 466742, 33.7701, -118.1937, 170, 1897, 13200998),
('Oakland', 'CA', 440646, 37.8044, -122.2712, 56, 1852, 4749008),
('Minneapolis', 'MN', 429954, 44.9778, -93.2650, 830, 1867, 3690261),
('Tulsa', 'OK', 413066, 36.1540, -95.9928, 722, 1836, 998626),
('Tampa', 'FL', 399700, 27.9506, -82.4572, 48, 1824, 3175275),
('Arlington', 'TX', 398854, 32.7357, -97.1081, 616, 1876, 7637387),
('New Orleans', 'LA', 383997, 29.9511, -90.0715, -6, 1718, 1270530),
('Wichita', 'KS', 389965, 37.6872, -97.3301, 1299, 1868, 647610),
('Cleveland', 'OH', 383793, 41.4993, -81.6944, 653, 1796, 2057009),
('Bakersfield', 'CA', 383579, 35.3733, -119.0187, 404, 1869, 893119),
('Honolulu', 'HI', 350964, 21.3099, -157.8581, 18, 1850, 1016508),
('Anaheim', 'CA', 352497, 33.8366, -117.9143, 157, 1857, 13200998);

-- ===================================================================
-- TABLE: weather_stations
-- Weather monitoring stations linked to cities
-- ===================================================================

CREATE TABLE weather_stations (
    station_id SERIAL PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    city_id INTEGER REFERENCES cities(city_id),
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    install_year INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    station_type VARCHAR(20) DEFAULT 'automatic',
    elevation_ft INTEGER
);

INSERT INTO weather_stations (station_name, city_id, latitude, longitude, install_year, active, station_type, elevation_ft) VALUES
-- New York stations
('NYC_CENTRAL_PARK', 1, 40.7829, -73.9654, 2010, true, 'automatic', 132),
('NYC_LGA_AIRPORT', 1, 40.7769, -73.8740, 2012, true, 'airport', 21),
('NYC_JFK_AIRPORT', 1, 40.6413, -73.7781, 2008, true, 'airport', 13),

-- Los Angeles stations
('LA_DOWNTOWN', 2, 34.0522, -118.2437, 2008, true, 'urban', 285),
('LA_LAX_AIRPORT', 2, 33.9425, -118.4081, 2005, true, 'airport', 125),
('LA_HOLLYWOOD', 2, 34.1022, -118.3269, 2015, false, 'urban', 354),
('LA_PASADENA', 2, 34.1478, -118.1445, 2011, true, 'suburban', 864),

-- Chicago stations
('CHI_OHARE', 3, 41.9742, -87.9073, 2009, true, 'airport', 672),
('CHI_MIDWAY', 3, 41.7868, -87.7505, 2011, true, 'airport', 620),
('CHI_DOWNTOWN', 3, 41.8781, -87.6298, 2013, true, 'urban', 594),
('CHI_LAKEFRONT', 3, 41.8919, -87.6051, 2007, true, 'lakefront', 578),

-- Houston stations
('HOU_INTERCONTINENTAL', 4, 29.9844, -95.3414, 2007, true, 'airport', 97),
('HOU_HOBBY', 4, 29.6454, -95.2789, 2010, true, 'airport', 46),
('HOU_DOWNTOWN', 4, 29.7604, -95.3698, 2012, true, 'urban', 80),

-- Phoenix stations
('PHX_SKY_HARBOR', 5, 33.4373, -112.0078, 2006, true, 'airport', 1135),
('PHX_DOWNTOWN', 5, 33.4484, -112.0740, 2009, true, 'urban', 1086),
('PHX_SCOTTSDALE', 5, 33.4734, -111.9010, 2014, true, 'suburban', 1257),

-- Additional major city stations
('PHL_AIRPORT', 6, 39.8729, -75.2437, 2008, true, 'airport', 36),
('SAT_AIRPORT', 7, 29.5337, -98.4698, 2009, true, 'airport', 809),
('SD_LINDBERGH', 8, 32.7338, -117.1933, 2010, true, 'airport', 17),
('DAL_DFW', 9, 32.8998, -97.0403, 2008, true, 'airport', 603),
('SJ_AIRPORT', 10, 37.3626, -121.9291, 2011, true, 'airport', 62),

-- Medium city stations
('AUS_BERGSTROM', 11, 30.1945, -97.6699, 2012, true, 'airport', 542),
('JAX_AIRPORT', 12, 30.4941, -81.6978, 2010, true, 'airport', 30),
('FTW_MEACHAM', 13, 32.8198, -97.3624, 2009, true, 'airport', 710),
('CMH_AIRPORT', 14, 39.9980, -82.8916, 2011, true, 'airport', 815),
('CLT_AIRPORT', 15, 35.2144, -80.9431, 2007, true, 'airport', 748),
('SF_AIRPORT', 16, 37.6213, -122.3790, 2008, true, 'airport', 13),
('IND_AIRPORT', 17, 39.7173, -86.2944, 2010, true, 'airport', 797),
('SEA_TACOMA', 18, 47.4502, -122.3088, 2009, true, 'airport', 433),
('DEN_INTL', 19, 39.8561, -104.6737, 2010, true, 'airport', 5431),
('BOS_LOGAN', 20, 42.3656, -71.0096, 2008, true, 'airport', 20),

-- Additional smaller city stations
('ELP_AIRPORT', 21, 31.8072, -106.3781, 2013, true, 'airport', 3958),
('DTW_METRO', 22, 42.2162, -83.3554, 2007, true, 'airport', 645),
('BNA_AIRPORT', 23, 36.1245, -86.6782, 2009, true, 'airport', 599),
('MEM_AIRPORT', 24, 35.0424, -89.9767, 2008, true, 'airport', 341),
('PDX_AIRPORT', 25, 45.5898, -122.5951, 2011, true, 'airport', 31),
('OKC_AIRPORT', 26, 35.3931, -97.6007, 2012, true, 'airport', 1295),
('LAS_MCCARRAN', 27, 36.0840, -115.1537, 2006, true, 'airport', 2181),
('SDF_AIRPORT', 28, 38.1744, -85.7361, 2010, true, 'airport', 501),
('BWI_AIRPORT', 29, 39.1754, -76.6683, 2009, true, 'airport', 146),
('MKE_AIRPORT', 30, 42.9472, -87.8966, 2011, true, 'airport', 723),

-- Some inactive/discontinued stations for testing
('LA_BURBANK_OLD', 2, 34.2006, -118.3587, 1998, false, 'airport', 778),
('CHI_MEIGS_OLD', 3, 41.8581, -87.6078, 1995, false, 'airport', 593),
('NYC_IDLEWILD_OLD', 1, 40.6413, -73.7781, 1992, false, 'airport', 13);

-- ===================================================================
-- TABLE: temperature_readings
-- Daily temperature measurements from weather stations
-- ===================================================================

CREATE TABLE temperature_readings (
    reading_id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES weather_stations(station_id),
    reading_date DATE NOT NULL,
    temp_high_f DECIMAL(5,2) NOT NULL,
    temp_low_f DECIMAL(5,2) NOT NULL,
    humidity_percent DECIMAL(5,2),
    wind_speed_mph DECIMAL(4,1),
    precipitation_in DECIMAL(4,2) DEFAULT 0.00,
    notes VARCHAR(200)
);

-- Generate sample temperature data for the past year
-- This will create realistic temperature patterns for different regions
INSERT INTO temperature_readings (station_id, reading_date, temp_high_f, temp_low_f, humidity_percent, wind_speed_mph, precipitation_in)
SELECT
    s.station_id,
    CURRENT_DATE - (RANDOM() * 365)::INTEGER as reading_date,
    -- Temperature varies by region and season
    CASE
        WHEN c.state_code IN ('FL', 'TX', 'AZ', 'CA', 'NV') THEN (RANDOM() * 30 + 70)::DECIMAL(5,2) -- Warmer states
        WHEN c.state_code IN ('NY', 'IL', 'MI', 'WI', 'MN') THEN (RANDOM() * 40 + 40)::DECIMAL(5,2) -- Colder states
        ELSE (RANDOM() * 35 + 50)::DECIMAL(5,2) -- Moderate states
    END as temp_high_f,
    -- Low temp is typically 15-25 degrees lower than high
    CASE
        WHEN c.state_code IN ('FL', 'TX', 'AZ', 'CA', 'NV') THEN (RANDOM() * 25 + 50)::DECIMAL(5,2)
        WHEN c.state_code IN ('NY', 'IL', 'MI', 'WI', 'MN') THEN (RANDOM() * 35 + 25)::DECIMAL(5,2)
        ELSE (RANDOM() * 30 + 35)::DECIMAL(5,2)
    END as temp_low_f,
    -- Humidity varies by region
    CASE
        WHEN c.state_code IN ('FL', 'LA', 'TX') THEN (RANDOM() * 30 + 60)::DECIMAL(5,2) -- Humid states
        WHEN c.state_code IN ('AZ', 'NV', 'UT', 'CO') THEN (RANDOM() * 40 + 20)::DECIMAL(5,2) -- Dry states
        ELSE (RANDOM() * 50 + 40)::DECIMAL(5,2) -- Moderate humidity
    END as humidity_percent,
    (RANDOM() * 20 + 5)::DECIMAL(4,1) as wind_speed_mph,
    -- Occasional precipitation
    CASE WHEN RANDOM() < 0.3 THEN (RANDOM() * 2)::DECIMAL(4,2) ELSE 0.00 END as precipitation_in
FROM weather_stations s
INNER JOIN cities c ON s.city_id = c.city_id
CROSS JOIN generate_series(1, 30) -- 30 readings per active station
WHERE s.active = true;

-- Add some extreme temperature readings for testing queries
INSERT INTO temperature_readings (station_id, reading_date, temp_high_f, temp_low_f, humidity_percent, wind_speed_mph, notes) VALUES
-- Extreme heat
(15, CURRENT_DATE - 45, 118.0, 89.0, 15.5, 12.3, 'Record high temperature'),
(16, CURRENT_DATE - 120, 115.2, 92.1, 18.2, 8.7, 'Heat wave conditions'),
(27, CURRENT_DATE - 80, 112.8, 88.4, 12.8, 15.2, 'Desert heat dome'),
-- Extreme cold
(19, CURRENT_DATE - 200, -15.2, -28.6, 78.3, 25.4, 'Arctic blast'),
(22, CURRENT_DATE - 180, -8.7, -22.1, 82.1, 18.9, 'Polar vortex'),
(30, CURRENT_DATE - 160, -12.4, -25.8, 75.6, 22.1, 'Lake effect snow'),
-- Record precipitation
(18, CURRENT_DATE - 100, 58.2, 45.8, 95.2, 35.6, 'Atmospheric river event'),
(20, CURRENT_DATE - 250, 42.1, 38.9, 88.7, 42.3, 'Nor''easter storm'),
(24, CURRENT_DATE - 60, 78.5, 65.2, 92.4, 28.7, 'Thunderstorm complex');

-- ===================================================================
-- CREATE INDEXES for better query performance
-- ===================================================================

-- Primary lookup indexes
CREATE INDEX idx_cities_state_code ON cities(state_code);
CREATE INDEX idx_cities_population ON cities(population);
CREATE INDEX idx_weather_stations_city_id ON weather_stations(city_id);
CREATE INDEX idx_weather_stations_active ON weather_stations(active);
CREATE INDEX idx_temperature_readings_station_id ON temperature_readings(station_id);
CREATE INDEX idx_temperature_readings_date ON temperature_readings(reading_date);

-- Composite indexes for common query patterns
CREATE INDEX idx_cities_state_population ON cities(state_code, population);
CREATE INDEX idx_stations_city_active ON weather_stations(city_id, active);
CREATE INDEX idx_readings_station_date ON temperature_readings(station_id, reading_date);

-- ===================================================================
-- VERIFY DATA INTEGRITY
-- ===================================================================

-- Display summary statistics
DO $$
BEGIN
    RAISE NOTICE '==================================================';
    RAISE NOTICE 'SQL INTRODUCTION DATABASE - INITIALIZATION COMPLETE';
    RAISE NOTICE '==================================================';
    RAISE NOTICE 'States: % records', (SELECT COUNT(*) FROM state_info);
    RAISE NOTICE 'Cities: % records', (SELECT COUNT(*) FROM cities);
    RAISE NOTICE 'Weather Stations: % records (% active)',
        (SELECT COUNT(*) FROM weather_stations),
        (SELECT COUNT(*) FROM weather_stations WHERE active = true);
    RAISE NOTICE 'Temperature Readings: % records', (SELECT COUNT(*) FROM temperature_readings);
    RAISE NOTICE '==================================================';
    RAISE NOTICE 'Database ready for SQL Introduction assignment!';
    RAISE NOTICE 'Students can now practice SELECT, WHERE, JOIN, GROUP BY, and more.';
    RAISE NOTICE '==================================================';
END $$;

-- ===================================================================
-- SAMPLE QUERIES for testing the database setup
-- ===================================================================

-- Uncomment these lines to test the database after initialization

-- SELECT 'Database Test' as test_type, COUNT(*) as total_records FROM cities;
-- SELECT 'Large Cities' as category, COUNT(*) as count FROM cities WHERE population > 500000;
-- SELECT 'States with Cities' as category, COUNT(DISTINCT state_code) as count FROM cities;
-- SELECT 'Active Stations' as category, COUNT(*) as count FROM weather_stations WHERE active = true;
-- SELECT 'Recent Readings' as category, COUNT(*) as count FROM temperature_readings WHERE reading_date >= CURRENT_DATE - INTERVAL '30 days';
