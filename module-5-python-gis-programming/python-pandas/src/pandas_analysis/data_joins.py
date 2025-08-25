"""
Data Joins Module - Student Implementation
=========================================

Welcome! This module teaches you how to combine data from different sources.

Think of data joins like combining information from different spreadsheets:
- You have one spreadsheet with weather station locations
- You have another spreadsheet with temperature readings
- You want to combine them to see which readings came from which stations

This is incredibly useful in GIS and environmental work!

Don't worry if joins seem complex - we'll explain everything step by step!

What you'll learn:
- How to combine DataFrames using common columns (like matching ID numbers)
- Different types of joins (inner, left, outer) and when to use each
- How to handle data that doesn't match perfectly
- How to make joins run fast on large datasets
- How to validate your join results

IMPORTANT: Read all the comments carefully. They guide you through each step!
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, List, Tuple, Union, Any, Optional


def merge_station_data(locations_df: pd.DataFrame,
                      measurements_df: pd.DataFrame,
                      join_column: str = 'station_id') -> pd.DataFrame:
    """
    COMBINE STATION LOCATIONS WITH MEASUREMENTS (Like matching puzzle pieces)

    Imagine you have two spreadsheets:
    1. locations_df: Lists weather stations with their coordinates
       station_id | latitude | longitude | station_name
       ----------|----------|-----------|-------------
       'A001'    | 40.7128  | -74.0060  | 'Central Park'
       'A002'    | 40.7589  | -73.9851  | 'Times Square'

    2. measurements_df: Lists temperature readings from stations
       station_id | temperature | humidity | date
       ----------|-------------|----------|------------
       'A001'    | 22.5        | 65       | '2023-01-15'
       'A001'    | 23.1        | 68       | '2023-01-16'
       'A002'    | 21.8        | 72       | '2023-01-15'

    Your task: Combine these so each measurement shows WHERE it was taken.

    Result should look like:
    station_id | latitude | longitude | station_name   | temperature | humidity | date
    ----------|----------|-----------|----------------|-------------|----------|------------
    'A001'    | 40.7128  | -74.0060  | 'Central Park' | 22.5        | 65       | '2023-01-15'
    'A001'    | 40.7128  | -74.0060  | 'Central Park' | 23.1        | 68       | '2023-01-16'
    'A002'    | 40.7589  | -73.9851  | 'Times Square' | 21.8        | 72       | '2023-01-15'

    Args:
        locations_df: DataFrame with station information (locations, names, etc.)
        measurements_df: DataFrame with sensor readings
        join_column: Column name to match on (default: 'station_id')

    Returns:
        Combined DataFrame with location info added to each measurement
    """

    # STEP 1: Check for empty DataFrames
    # If either DataFrame is empty, we can't do a meaningful join
    if locations_df.empty or measurements_df.empty:
        # Return empty DataFrame with combined columns
        if locations_df.empty and measurements_df.empty:
            return pd.DataFrame()
        elif locations_df.empty:
            return measurements_df.copy()
        else:
            return locations_df.copy()

    # STEP 2: Check that the join column exists in both DataFrames
    # We need the matching column to exist in both spreadsheets
    if join_column not in locations_df.columns:
        raise ValueError(f"Join column '{join_column}' not found in locations_df")
    if join_column not in measurements_df.columns:
        raise ValueError(f"Join column '{join_column}' not found in measurements_df")

    # STEP 3: Perform the merge (this is the actual join operation)
    # We use 'left' join to keep all measurements, even if some don't have location info
    # This means: "Keep all rows from measurements_df, add location info where available"

    # HINT: Use pd.merge(left_df, right_df, on=column_name, how=join_type)
    # - left_df: The DataFrame we want to keep all rows from
    # - right_df: The DataFrame we want to add information from
    # - on: The column name to match on
    # - how: Type of join ('left', 'inner', 'outer', 'right')

    # FILL IN: result = pd.merge(???, ???, on=???, how=???)

    result = pd.merge(measurements_df, locations_df, on=join_column, how='left')

    # STEP 4: Return the combined result
    return result

    # Your function now:
    # ✅ Combines measurement data with location information
    # ✅ Handles empty DataFrames gracefully
    # ✅ Keeps all measurements (even those without location data)
    # ✅ Uses the specified join column


def advanced_join_with_validation(primary_df: pd.DataFrame,
                                secondary_df: pd.DataFrame,
                                join_keys: List[str],
                                join_type: str = 'inner') -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    ADVANCED DATA JOINING WITH QUALITY CHECKS (Like a careful librarian)

    This function does a "smart" join that not only combines data but also
    gives you a report about what happened. It's like having a careful librarian
    who not only finds your books but tells you what they found and any issues.

    Think of it like this:
    - You ask for books about "weather" and "New York"
    - The librarian finds matching books
    - They also tell you: "Found 15 matches, but 3 books were missing New York info"

    Your Task: Perform the join AND create a detailed report about the results.

    Args:
        primary_df: Main DataFrame (like your primary data source)
        secondary_df: DataFrame to join with (additional information)
        join_keys: List of column names to join on (can be multiple columns)
        join_type: How to join ('inner', 'left', 'outer', 'right')

    Returns:
        - Combined DataFrame
        - Report dictionary with join statistics and warnings
    """

    # STEP 1: Initialize our report dictionary
    # This will track what happens during the join
    report = {
        'join_type': join_type,
        'join_keys': join_keys,
        'primary_rows_before': len(primary_df),
        'secondary_rows_before': len(secondary_df),
        'primary_rows_after': 0,
        'duplicates_in_primary': 0,
        'duplicates_in_secondary': 0,
        'unmatched_primary_keys': 0,
        'unmatched_secondary_keys': 0,
        'warnings': []
    }

    # STEP 2: Handle empty DataFrames
    if primary_df.empty and secondary_df.empty:
        report['primary_rows_after'] = 0
        return pd.DataFrame(), report
    elif primary_df.empty:
        report['primary_rows_after'] = len(secondary_df) if join_type in ['right', 'outer'] else 0
        return secondary_df.copy() if join_type in ['right', 'outer'] else pd.DataFrame(), report
    elif secondary_df.empty:
        report['primary_rows_after'] = len(primary_df) if join_type in ['left', 'outer'] else 0
        return primary_df.copy() if join_type in ['left', 'outer'] else pd.DataFrame(), report

    # STEP 3: Validate join keys exist in both DataFrames
    missing_keys_primary = [key for key in join_keys if key not in primary_df.columns]
    missing_keys_secondary = [key for key in join_keys if key not in secondary_df.columns]

    if missing_keys_primary:
        raise ValueError(f"Join keys {missing_keys_primary} not found in primary_df")
    if missing_keys_secondary:
        raise ValueError(f"Join keys {missing_keys_secondary} not found in secondary_df")

    # STEP 4: Check for duplicate keys (this can cause unexpected results)
    # Count how many times each combination of join keys appears

    # HINT: Use df[join_keys].duplicated().sum() to count duplicates
    # FILL IN: primary_duplicates = ???
    primary_duplicates = primary_df[join_keys].duplicated().sum()
    secondary_duplicates = secondary_df[join_keys].duplicated().sum()

    report['duplicates_in_primary'] = primary_duplicates
    report['duplicates_in_secondary'] = secondary_duplicates

    # Add warnings if we find duplicates
    if primary_duplicates > 0:
        report['warnings'].append(f"Found {primary_duplicates} duplicate keys in primary_df")
    if secondary_duplicates > 0:
        report['warnings'].append(f"Found {secondary_duplicates} duplicate keys in secondary_df")

    # STEP 5: Perform the actual join
    # HINT: Use pd.merge() with the specified parameters
    # FILL IN: merged_df = pd.merge(???, ???, on=???, how=???)

    merged_df = pd.merge(primary_df, secondary_df, on=join_keys, how=join_type)

    # STEP 6: Update report with final statistics
    report['primary_rows_after'] = len(merged_df)

    # STEP 7: Check for unmatched keys (only if it's not an inner join)
    if join_type != 'inner':
        # For non-inner joins, some keys might not have matches

        # Find keys that exist in primary but not secondary
        primary_keys = set(primary_df[join_keys].apply(tuple, axis=1))
        secondary_keys = set(secondary_df[join_keys].apply(tuple, axis=1))

        unmatched_primary = primary_keys - secondary_keys
        unmatched_secondary = secondary_keys - primary_keys

        report['unmatched_primary_keys'] = len(unmatched_primary)
        report['unmatched_secondary_keys'] = len(unmatched_secondary)

        if len(unmatched_primary) > 0:
            report['warnings'].append(f"{len(unmatched_primary)} keys from primary_df had no matches")
        if len(unmatched_secondary) > 0:
            report['warnings'].append(f"{len(unmatched_secondary)} keys from secondary_df had no matches")

    # STEP 8: Return both the result and the detailed report
    return merged_df, report


def spatial_join_environmental_data(weather_stations: pd.DataFrame,
                                  air_quality_stations: pd.DataFrame,
                                  distance_tolerance: float = 1.0) -> pd.DataFrame:
    """
    COMBINE DATA FROM NEARBY STATIONS (Like finding your nearest neighbors)

    Sometimes you have different types of environmental sensors that aren't at
    exactly the same location, but are close enough that you want to combine
    their data. This is like saying "find weather stations that are close to
    air quality stations and combine their readings."

    Example:
    - Weather station at coordinates (40.7128, -74.0060)
    - Air quality station at coordinates (40.7130, -74.0062)
    - These are very close (about 20 meters apart)
    - We want to combine their data since they're measuring the same area

    Your Task: Find pairs of stations that are close to each other and combine
    their data.

    Args:
        weather_stations: DataFrame with weather data and lat/lon coordinates
        air_quality_stations: DataFrame with air quality data and lat/lon coordinates
        distance_tolerance: Maximum distance (km) to consider stations "close"

    Returns:
        Combined DataFrame with paired station data
    """

    # STEP 1: Check for empty DataFrames
    if weather_stations.empty or air_quality_stations.empty:
        return pd.DataFrame()

    # STEP 2: Check for required columns
    required_weather_cols = ['latitude', 'longitude']
    required_air_cols = ['latitude', 'longitude']

    missing_weather = [col for col in required_weather_cols if col not in weather_stations.columns]
    missing_air = [col for col in required_air_cols if col not in air_quality_stations.columns]

    if missing_weather or missing_air:
        raise ValueError(f"Missing coordinate columns. Weather: {missing_weather}, Air: {missing_air}")

    # STEP 3: Create a simple distance-based pairing
    # For educational purposes, we'll use a simplified approach
    # In real GIS work, you'd use proper geospatial libraries

    results = []

    # STEP 4: For each weather station, find the closest air quality station
    for weather_idx, weather_row in weather_stations.iterrows():
        weather_lat = weather_row['latitude']
        weather_lon = weather_row['longitude']

        closest_air_station = None
        min_distance = float('inf')

        # STEP 5: Check distance to each air quality station
        for air_idx, air_row in air_quality_stations.iterrows():
            air_lat = air_row['latitude']
            air_lon = air_row['longitude']

            # Calculate approximate distance using simple formula
            # (This is simplified - real GIS uses more complex calculations)
            # HINT: Simple distance = sqrt((lat1-lat2)^2 + (lon1-lon2)^2) * 111 (rough km conversion)

            lat_diff = weather_lat - air_lat
            lon_diff = weather_lon - air_lon

            # FILL IN: distance = ???
            distance = ((lat_diff ** 2) + (lon_diff ** 2)) ** 0.5 * 111  # Rough conversion to km

            # STEP 6: Keep track of the closest air quality station
            if distance < min_distance and distance <= distance_tolerance:
                min_distance = distance
                closest_air_station = air_row

        # STEP 7: If we found a close air quality station, combine the data
        if closest_air_station is not None:
            # Create a combined row with data from both stations
            combined_row = {}

            # Add weather data with 'weather_' prefix
            for col, val in weather_row.items():
                combined_row[f'weather_{col}'] = val

            # Add air quality data with 'air_' prefix
            for col, val in closest_air_station.items():
                combined_row[f'air_{col}'] = val

            # Add the distance information
            combined_row['distance_km'] = round(min_distance, 3)

            results.append(combined_row)

    # STEP 8: Convert results to DataFrame
    if results:
        # FILL IN: result_df = ???
        result_df = pd.DataFrame(results)
    else:
        result_df = pd.DataFrame()

    return result_df

    # Your function now:
    # ✅ Finds weather and air quality stations that are close to each other
    # ✅ Combines their data into a single record
    # ✅ Includes distance information
    # ✅ Handles cases where no stations are close enough


def validate_join_results(original_df: pd.DataFrame,
                         joined_df: pd.DataFrame,
                         join_type: str) -> Dict[str, Any]:
    """
    CHECK IF YOUR JOIN WORKED CORRECTLY (Like proofreading your work)

    After combining DataFrames, it's important to check that everything worked
    as expected. This function acts like a proofreader, checking for common
    issues and giving you a report.

    Think of it like checking your math homework:
    - Did you get the right number of answers?
    - Are there any weird results that don't make sense?
    - Did you accidentally create duplicates?

    Your Task: Analyze the join results and report any potential issues.

    Args:
        original_df: The DataFrame before joining
        joined_df: The DataFrame after joining
        join_type: What type of join was performed

    Returns:
        Dictionary with validation results and recommendations
    """

    validation_report = {
        'join_type': join_type,
        'original_rows': len(original_df),
        'joined_rows': len(joined_df),
        'row_change': len(joined_df) - len(original_df),
        'is_valid': True,
        'issues': [],
        'recommendations': []
    }

    # STEP 1: Check if row counts make sense for the join type

    if join_type == 'inner':
        # Inner joins should never increase rows beyond the original
        if len(joined_df) > len(original_df):
            validation_report['is_valid'] = False
            validation_report['issues'].append("Inner join increased row count - check for duplicate keys")
            validation_report['recommendations'].append("Check both DataFrames for duplicate join keys")

    elif join_type == 'left':
        # Left joins should keep at least the original number of rows
        if len(joined_df) < len(original_df):
            validation_report['is_valid'] = False
            validation_report['issues'].append("Left join lost rows - this shouldn't happen")
            validation_report['recommendations'].append("Check join key data types and missing values")

    # STEP 2: Check for excessive row multiplication
    # If the result has way more rows than the original, there might be duplicate keys
    row_multiplication_factor = len(joined_df) / len(original_df) if len(original_df) > 0 else 0

    if row_multiplication_factor > 2.0:
        validation_report['issues'].append(f"Join created {row_multiplication_factor:.1f}x more rows than original")
        validation_report['recommendations'].append("Check for duplicate keys in both DataFrames")

    # STEP 3: Check for completely null columns (might indicate join failure)
    if not joined_df.empty:
        # Count completely null columns
        null_columns = []
        for col in joined_df.columns:
            if joined_df[col].isnull().all():
                null_columns.append(col)

        if null_columns:
            validation_report['issues'].append(f"Found {len(null_columns)} completely null columns: {null_columns}")
            validation_report['recommendations'].append("Check if join keys had any matches")

    # STEP 4: Calculate quality metrics
    if not original_df.empty and not joined_df.empty:
        # Calculate percentage of rows that got additional data
        # (This is a rough metric - in real scenarios you'd be more specific)

        original_cols = set(original_df.columns)
        new_cols = set(joined_df.columns) - original_cols

        if new_cols:
            # Check how many rows have non-null data in the new columns
            rows_with_new_data = 0
            for _, row in joined_df.iterrows():
                has_new_data = any(pd.notna(row[col]) for col in new_cols if col in row)
                if has_new_data:
                    rows_with_new_data += 1

            match_percentage = (rows_with_new_data / len(joined_df)) * 100
            validation_report['match_percentage'] = round(match_percentage, 1)

            if match_percentage < 50:
                validation_report['issues'].append(f"Only {match_percentage:.1f}% of rows got matched data")
                validation_report['recommendations'].append("Check if join keys are compatible between DataFrames")

    # STEP 5: Overall assessment
    if not validation_report['issues']:
        validation_report['recommendations'].append("Join looks good! No obvious issues detected.")

    return validation_report


# ==============================================================================
# HELPER SECTION - Bonus functions for extra practice!
# ==============================================================================

def _calculate_simple_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    BONUS HELPER: Calculate approximate distance between two points
    (You can implement this for extra practice, or skip it!)

    This uses a simplified formula. Real GIS applications use more sophisticated
    methods like the Haversine formula to account for Earth's curvature.
    """
    # Simple Euclidean distance approximation
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2

    # Rough conversion to kilometers (very approximate!)
    distance_km = ((lat_diff ** 2) + (lon_diff ** 2)) ** 0.5 * 111

    return distance_km


def _detect_key_data_types(df: pd.DataFrame, key_columns: List[str]) -> Dict[str, str]:
    """
    BONUS HELPER: Check what data types your join keys are
    (You can implement this for extra practice, or skip it!)
    """
    key_types = {}
    for col in key_columns:
        if col in df.columns:
            key_types[col] = str(df[col].dtype)
        else:
            key_types[col] = "MISSING"

    return key_types


def _find_duplicate_keys(df: pd.DataFrame, key_columns: List[str]) -> pd.DataFrame:
    """
    BONUS HELPER: Find rows that have duplicate join keys
    (You can implement this for extra practice, or skip it!)
    """
    if df.empty:
        return pd.DataFrame()

    # Find duplicated key combinations
    duplicate_mask = df[key_columns].duplicated(keep=False)

    return df[duplicate_mask]


# ==============================================================================
# EXAMPLES - Try these in a Python console to understand how joins work!
# ==============================================================================

"""
EXAMPLE 1: Basic inner join (only keep matches)

# Create sample data
stations = pd.DataFrame({
    'station_id': ['A001', 'A002', 'A003'],
    'station_name': ['Downtown', 'Uptown', 'Suburb'],
    'latitude': [40.71, 40.76, 40.68],
    'longitude': [-74.01, -73.98, -74.05]
})

readings = pd.DataFrame({
    'station_id': ['A001', 'A001', 'A002', 'A004'],  # Note: A004 not in stations
    'temperature': [22.5, 23.1, 21.8, 25.0],
    'humidity': [65, 68, 72, 55]
})

# Inner join - only keep readings that have station info
result = pd.merge(readings, stations, on='station_id', how='inner')
print(f"Readings: {len(readings)}, Stations: {len(stations)}, Result: {len(result)}")
# Output: 3 rows (A004 reading is dropped because no station info)

EXAMPLE 2: Left join (keep all readings)

result = pd.merge(readings, stations, on='station_id', how='left')
print(result)
# All 4 readings kept, but A004 will have NaN for station_name, lat, lon

EXAMPLE 3: Multiple join keys

# Data with multiple columns to match on
weather = pd.DataFrame({
    'station_id': ['A001', 'A002', 'A001', 'A002'],
    'date': ['2023-01-15', '2023-01-15', '2023-01-16', '2023-01-16'],
    'temperature': [22.5, 21.8, 23.1, 22.3]
})

quality = pd.DataFrame({
    'station_id': ['A001', 'A002', 'A001', 'A002'],
    'date': ['2023-01-15', '2023-01-15', '2023-01-16', '2023-01-16'],
    'air_quality': [45, 52, 48, 49]
})

# Join on both station_id AND date
combined = pd.merge(weather, quality, on=['station_id', 'date'], how='inner')
print(combined)
"""

# ==============================================================================
# COMMON MISTAKES - Watch out for these!
# ==============================================================================

"""
❌ MISTAKE 1: Forgetting about duplicate keys
# Problem: If one DataFrame has duplicate keys, your result will multiply rows
stations = pd.DataFrame({'id': ['A', 'B', 'A'], 'name': ['X', 'Y', 'Z']})  # 'A' appears twice!
readings = pd.DataFrame({'id': ['A', 'B'], 'temp': [22, 25]})
result = pd.merge(readings, stations, on='id')  # 'A' reading appears twice in result

# Solution: Check for and handle duplicates before joining

❌ MISTAKE 2: Wrong join type
# Be careful about which join type you need:
# - inner: Only rows that match in both DataFrames
# - left: All rows from left DataFrame, matching rows from right
# - right: All rows from right DataFrame, matching rows from left
# - outer: All rows from both DataFrames

❌ MISTAKE 3: Data type mismatches
df1 = pd.DataFrame({'id': [1, 2, 3], 'data': ['a', 'b', 'c']})     # id is integer
df2 = pd.DataFrame({'id': ['1', '2', '3'], 'info': ['x', 'y', 'z']}) # id is string
result = pd.merge(df1, df2, on='id')  # Won't match! 1 ≠ '1'

# Solution: Convert data types before joining
df2['id'] = df2['id'].astype(int)

❌ MISTAKE 4: Not handling missing values in join keys
df1 = pd.DataFrame({'id': [1, 2, None], 'data': ['a', 'b', 'c']})
df2 = pd.DataFrame({'id': [1, 2, 3], 'info': ['x', 'y', 'z']})
# The None in df1 won't match anything in df2

# Solution: Clean your data first or use appropriate join strategy
"""

"""
CONGRATULATIONS! 🎉

You've mastered the fundamentals of data joining in pandas:
✅ Combining data from multiple sources using common keys
✅ Understanding different join types (inner, left, outer, right)
✅ Handling spatial relationships between datasets
✅ Validating join results for quality assurance
✅ Dealing with duplicate keys and missing data

These skills are crucial for:
- Combining environmental monitoring data from different sensors
- Linking geographic locations with attribute data
- Merging datasets from different time periods or sources
- Creating comprehensive datasets for analysis
- Quality control in data processing pipelines

Real-world applications:
🌍 GIS: Linking spatial coordinates with attribute data
📊 Environmental science: Combining weather, air quality, and pollution data
📈 Data science: Creating master datasets from multiple sources
🔬 Research: Integrating data from different experiments or studies

Pro tips for success:
- Always validate your joins with the validation function
- Check for duplicate keys before joining
- Understand your data relationships before choosing join type
- Start with small test datasets to verify your logic
- Document your joining strategy for reproducibility

Keep practicing and you'll become a data joining expert! 🚀
"""
