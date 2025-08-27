# Data Dictionary - Environmental Monitoring Datasets

This document explains the datasets provided for the Pandas Basics assignment. Understanding your data is the first step in any analysis!

---

## 📊 Overview

You have **two related datasets** that can be joined together:

1. **`weather_stations.csv`** - Information about monitoring station locations
2. **`temperature_readings.csv`** - Daily temperature and humidity measurements

These represent a realistic scenario where you have **reference data** (station locations) and **measurement data** (sensor readings) that need to be combined for analysis.

---

## 🌡️ weather_stations.csv

This file contains information about 15 environmental monitoring stations located throughout New York City.

| Column | Data Type | Description | Example Values |
|--------|-----------|-------------|----------------|
| `station_id` | Text | Unique identifier for each station | STN_001, STN_002, STN_003 |
| `station_name` | Text | Human-readable name of the station | "Central Park Weather Station" |
| `latitude` | Number | North-south position in decimal degrees | 40.7829 (North of equator) |
| `longitude` | Number | East-west position in decimal degrees | -73.9654 (West of Greenwich) |
| `elevation_m` | Number | Height above sea level in meters | 35, 10, 25 |
| `station_type` | Text | Type of monitoring equipment | "meteorological", "air_quality" |

### 📝 Important Notes:
- **Coordinates**: All locations are in New York City area
- **Elevation**: Ranges from 3m (near water) to 85m (higher ground)
- **Station Types**: 
  - `meteorological` - Full weather monitoring (temp, humidity, pressure, etc.)
  - `air_quality` - Focused on air pollution and basic weather

---

## 📈 temperature_readings.csv

This file contains 95 daily measurements from the monitoring stations over a one-week period (Jan 15-21, 2023).

| Column | Data Type | Description | Example Values |
|--------|-----------|-------------|----------------|
| `station_id` | Text | Links to station in weather_stations.csv | STN_001, STN_002, STN_003 |
| `date` | Text | When measurement was taken | "2023-01-15", "2023-01-16" |
| `temperature_c` | Number | Air temperature in degrees Celsius | 22.5, 23.1, 35.2 |
| `humidity_percent` | Number | Relative humidity as percentage | 65.2, 68.4, 45.1 |
| `data_quality` | Text | Quality assessment of the reading | "good", "fair", "poor" |

### 📝 Important Notes:
- **Temperature Range**: Most values 15-30°C, but some extreme readings exist
- **Data Quality Meanings**:
  - `good` - Reliable measurement, use for analysis
  - `fair` - Acceptable but may have minor issues
  - `poor` - Questionable reading, consider excluding from analysis
- **Missing Data**: None in this dataset, but real-world data often has gaps

---

## 🔗 How the Datasets Connect

The datasets are connected through the **`station_id`** column:

```
weather_stations.csv          temperature_readings.csv
├── station_id: "STN_001"  ←→ station_id: "STN_001"
├── station_name: "Central Park"  temperature_c: 22.5
├── latitude: 40.7829           humidity_percent: 65.2
└── longitude: -73.9654         data_quality: "good"
```

When you **join** these datasets, you can answer questions like:
- What was the temperature at Central Park on January 15th?
- Which station (by name and location) recorded the highest temperature?
- Are stations at higher elevations generally cooler?

---

## 🎯 Common Analysis Questions

Here are some questions you can answer with this data:

### 📊 Basic Statistics
- What's the average temperature across all stations?
- Which station has the most consistent readings?
- How does humidity vary by location?

### 🔍 Data Quality Analysis
- How many readings have "good" vs "fair" vs "poor" quality?
- Should we exclude poor quality data from analysis?
- Are certain stations more reliable than others?

### 🗺️ Geographic Analysis
- Do stations closer to water have different temperatures?
- Is there a relationship between elevation and temperature?
- Which neighborhoods had the warmest/coolest readings?

### ⚠️ Data Validation
- Are there any suspicious temperature readings?
- Do all readings have corresponding station information?
- Are there any missing or duplicate measurements?

---

## 🛠️ Tips for Working with This Data

### Data Types to Check
```python
# Load the data and check types
df = pd.read_csv('data/temperature_readings.csv')
print(df.dtypes)

# You might need to convert dates:
df['date'] = pd.to_datetime(df['date'])
```

### Common Filters
```python
# Good quality readings only
good_data = df[df['data_quality'] == 'good']

# Reasonable temperature range
normal_temps = df[(df['temperature_c'] >= 10) & (df['temperature_c'] <= 35)]

# Specific date range
jan_15_data = df[df['date'] == '2023-01-15']
```

### Useful Groupings
```python
# By station
station_stats = df.groupby('station_id')['temperature_c'].mean()

# By data quality
quality_counts = df['data_quality'].value_counts()

# By date
daily_averages = df.groupby('date')['temperature_c'].mean()
```

---

## 🚨 Data Quality Issues to Watch For

### Temperature Anomalies
- **Very High**: 35.2°C reading might be a sensor error
- **Very Low**: Any readings below 10°C in January might be suspect

### Data Quality Flags
- **"poor" readings**: Consider excluding from analysis
- **Consistent patterns**: If one station always has "poor" data, investigate why

### Missing Relationships
- **Orphaned readings**: Measurements with station_ids not in the stations file
- **Unused stations**: Stations with no corresponding measurements

---

## 🎓 Educational Value

This dataset structure mirrors real-world GIS scenarios:

**Environmental Consulting**: Combining sensor data with station metadata
**Urban Planning**: Analyzing measurements by neighborhood characteristics  
**Climate Research**: Correlating weather patterns with geographic features
**Asset Management**: Tracking equipment performance and data quality

The skills you learn manipulating this data directly apply to professional GIS work!

---

## 📞 Questions?

If you're confused about any aspect of the data:
1. **Explore it**: Use `df.head()`, `df.describe()`, `df.info()` 
2. **Visualize it**: Create simple plots to understand distributions
3. **Ask for help**: Use the course discussion forum or office hours

Remember: Understanding your data is just as important as analyzing it! 🚀