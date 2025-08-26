"""
Pandas Basics for GIS Data Analysis - Student Implementation
===========================================================

Welcome! This module teaches you essential pandas skills for working with GIS data.

Pandas is Python's most popular library for working with tabular data (like CSV files).
Think of it as Excel, but with the power of Python programming!

Don't worry if you're new to pandas - we've provided Jupyter notebooks in the `notebooks/`
directory to guide you through building each function step by step.

What you'll learn:
- How to load CSV files into pandas DataFrames
- How to explore and understand your data
- How to filter data based on conditions
- How to calculate statistics and group data
- How to join datasets together
- How to save your results

ASSIGNMENT INSTRUCTIONS:
========================
1. Complete each function below by replacing the TODO comments with your code
2. Use the Jupyter notebooks in `notebooks/` to learn how to build each function
3. Test your functions as you go: `uv run pytest tests/test_pandas_basics.py::test_function_name -v`
4. Make sure all tests pass before submitting: `uv run pytest tests/ -v`

IMPORTANT: The notebooks show you HOW to build each function, but you must implement
the actual code here in this file to pass the unit tests!
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def load_and_explore_gis_data(file_path):
    """
    LOAD AND EXPLORE GIS DATA (Like opening a spreadsheet and getting familiar with it)

    This function loads a CSV file and shows you important information about the data,
    like how many rows and columns it has, what the columns are called, and what the
    first few rows look like.

    Think of this as your first step whenever you get a new dataset - you need to
    understand what you're working with before you can analyze it!

    📚 Learning Resource: See `notebooks/01_function_load_and_explore_gis_data.ipynb`
    🧪 Test Command: `uv run pytest tests/test_pandas_basics.py::test_load_and_explore_gis_data -v`

    Args:
        file_path (str): Path to the CSV file (like 'data/weather_stations.csv')

    Returns:
        pandas.DataFrame: The loaded data as a DataFrame (like a spreadsheet in Python)

    Example:
        >>> df = load_and_explore_gis_data('data/weather_stations.csv')
        Dataset loaded successfully!
        Shape: (15, 5) - 15 rows and 5 columns
        ...
    """

    # TODO: Print a header to show what function is running
    # TODO: Use something like print("=" * 50) and print("LOADING AND EXPLORING GIS DATA")

    # TODO: Check if the file exists using os.path.exists()
    # TODO: If file doesn't exist, print an error message and return None
    # TODO: Include helpful suggestions like checking the path and directory

    # TODO: Print the file path being loaded

    # TODO: Use a try/except block to load the CSV file
    # TODO: Use pd.read_csv(file_path) to load the data into a DataFrame
    # TODO: If loading succeeds, print a success message
    # TODO: If loading fails, print the error and return None

    # TODO: Print basic dataset information:
    # TODO: - Shape (rows and columns) using df.shape
    # TODO: - Column names using df.columns
    # TODO: - Data types for each column using df.dtypes or df.info()

    # TODO: Show the first 5 rows using df.head()
    # TODO: Print a header like "FIRST 5 ROWS:" before showing the data

    # TODO: Show summary statistics using df.describe()
    # TODO: Print a header like "SUMMARY STATISTICS:" before showing stats

    # TODO: Check for data quality issues:
    # TODO: - Count missing values using df.isnull().sum()
    # TODO: - Count duplicate rows using df.duplicated().sum()
    # TODO: - Report the results with appropriate messages

    # TODO: Print a completion message

    # TODO: Return the loaded DataFrame

    pass  # Remove this line when you implement the function


def filter_environmental_data(df, min_temp=15, max_temp=30, quality="good"):
    """
    FILTER ENVIRONMENTAL DATA (Like applying filters in Excel to show only certain data)

    This function filters temperature readings to show only data that meets your criteria:
    - Temperature within a specified range (default: 15-30°C)
    - Only data with a specific quality level (default: "good")

    This is essential for data cleaning - removing outliers and poor quality measurements!

    📚 Learning Resource: See `notebooks/02_function_filter_environmental_data.ipynb`
    🧪 Test Command: `uv run pytest tests/test_pandas_basics.py::test_filter_environmental_data -v`

    Args:
        df (pandas.DataFrame): The environmental data to filter (must have 'temperature_c' and 'data_quality' columns)
        min_temp (float): Minimum temperature threshold in Celsius (default: 15)
        max_temp (float): Maximum temperature threshold in Celsius (default: 30)
        quality (str): Required data quality level (default: "good")

    Returns:
        pandas.DataFrame: Filtered data meeting all specified conditions

    Example:
        >>> filtered = filter_environmental_data(df, min_temp=10, max_temp=35, quality="good")
        Filtering data...
        Original dataset: 500 rows
        After filtering: 247 rows kept, 253 rows removed
        ...
    """

    # TODO: Print a header to show what function is running
    # TODO: Use print("=" * 50) and print("FILTERING ENVIRONMENTAL DATA")

    # TODO: Input validation - check if df is None or empty
    # TODO: If invalid input, print error and return empty DataFrame: pd.DataFrame()

    # TODO: Check for required columns: 'temperature_c' and 'data_quality'
    # TODO: If missing columns, print error with available columns and return empty DataFrame

    # TODO: Store the original number of rows for reporting
    # TODO: Use len(df) to get row count

    # TODO: Print the filtering criteria being applied
    # TODO: Show min_temp, max_temp, and quality parameters

    # TODO: Check if the specified quality level exists in the data
    # TODO: Use df['data_quality'].unique() to see available quality levels
    # TODO: If quality not found, print warning and available options

    # TODO: Create temperature filter using boolean indexing
    # TODO: Use: (df['temperature_c'] >= min_temp) & (df['temperature_c'] <= max_temp)
    # TODO: Remember to use parentheses around each condition when combining with &

    # TODO: Create quality filter using boolean indexing
    # TODO: Use: df['data_quality'] == quality

    # TODO: Combine filters using & (AND operation)
    # TODO: Apply combined filter to get filtered DataFrame
    # TODO: Use: filtered_df = df[combined_filter].copy()

    # TODO: Calculate and report filtering results
    # TODO: - Original count (stored earlier)
    # TODO: - Filtered count using len(filtered_df)
    # TODO: - Removed count (original - filtered)
    # TODO: - Percentage removed

    # TODO: Show summary statistics of filtered data
    # TODO: - Temperature range in filtered data
    # TODO: - Quality distribution in filtered data

    # TODO: Print completion message

    # TODO: Return the filtered DataFrame

    pass  # Remove this line when you implement the function


def calculate_station_statistics(df):
    """
    CALCULATE STATION STATISTICS (Like creating a summary report for each weather station)

    This function groups temperature readings by station and calculates summary statistics
    for each station. This is essential for understanding patterns across different
    monitoring locations!

    📚 Learning Resource: See `notebooks/03_function_calculate_station_statistics.ipynb`
    🧪 Test Command: `uv run pytest tests/test_pandas_basics.py::test_calculate_station_statistics -v`

    Args:
        df (pandas.DataFrame): Environmental data with 'station_id', 'temperature_c', and 'humidity_percent' columns

    Returns:
        pandas.DataFrame: Statistics summary with columns:
            - station_id: Station identifier
            - avg_temperature: Mean temperature in Celsius (rounded to 1 decimal)
            - avg_humidity: Mean humidity percentage (rounded to 1 decimal)
            - reading_count: Number of readings for this station

    Example:
        >>> stats = calculate_station_statistics(df)
        Station Statistics Summary:
        station_id  avg_temperature  avg_humidity  reading_count
        STN_001            22.5           65.2            45
        STN_002            21.8           67.1            52
        ...
    """

    # TODO: Print a header to show what function is running
    # TODO: Use print("=" * 50) and print("CALCULATING STATION STATISTICS")

    # TODO: Input validation - check if df is None or empty
    # TODO: If invalid, print error and return empty DataFrame: pd.DataFrame()

    # TODO: Check for required columns: 'station_id', 'temperature_c', 'humidity_percent'
    # TODO: If missing columns, print error with available columns and return empty DataFrame

    # TODO: Print input data summary (number of readings being processed)

    # TODO: Get unique stations and print how many stations found
    # TODO: Use df['station_id'].unique()

    # TODO: Group data by station_id using df.groupby('station_id')

    # TODO: Calculate average temperature for each station
    # TODO: Use grouped_data['temperature_c'].mean()
    # TODO: Round to 1 decimal place using .round(1)

    # TODO: Calculate average humidity for each station
    # TODO: Use grouped_data['humidity_percent'].mean()
    # TODO: Round to 1 decimal place using .round(1)

    # TODO: Count readings per station
    # TODO: Use grouped_data.size() to count all rows per group

    # TODO: Create summary DataFrame with the statistics
    # TODO: Create a DataFrame with columns: station_id, avg_temperature, avg_humidity, reading_count
    # TODO: Make sure to reset the index so station_id becomes a regular column

    # TODO: Print summary of results:
    # TODO: - Temperature range across all stations
    # TODO: - Humidity range across all stations
    # TODO: - Total readings processed
    # TODO: - Average readings per station

    # TODO: Find and report temperature extremes:
    # TODO: - Hottest station (highest average temperature)
    # TODO: - Coolest station (lowest average temperature)
    # TODO: Use .idxmax() and .idxmin() or sort the DataFrame

    # TODO: Print the complete statistics table
    # TODO: Use print(stats_df.to_string(index=False)) for nice formatting

    # TODO: Print completion message

    # TODO: Return the statistics DataFrame

    pass  # Remove this line when you implement the function


def join_station_data(stations_df, readings_df):
    """
    JOIN STATION DATA WITH READINGS (Like connecting two Excel sheets with a common column)

    This function combines weather station location information with temperature readings.
    After joining, each temperature reading will have the station's name, coordinates,
    and elevation - enabling geographic analysis!

    📚 Learning Resource: See `notebooks/04_function_join_station_data.ipynb`
    🧪 Test Command: `uv run pytest tests/test_pandas_basics.py::test_join_station_data -v`

    Args:
        stations_df (pandas.DataFrame): Weather station information with columns:
            - station_id: Unique station identifier
            - station_name: Human-readable station name
            - latitude, longitude: Station coordinates
            - elevation_m: Station elevation in meters

        readings_df (pandas.DataFrame): Environmental measurements with columns:
            - station_id: Links to stations_df station_id
            - date: Measurement date
            - temperature_c: Temperature measurement in Celsius
            - humidity_percent: Humidity measurement percentage
            - data_quality: Quality assessment flag

    Returns:
        pandas.DataFrame: Combined dataset with both station information and environmental readings

    Example:
        >>> combined = join_station_data(stations_df, readings_df)
        Joining station locations with temperature readings...
        Stations dataset: 15 stations
        Readings dataset: 500 readings
        After joining: 500 rows (all readings matched to stations)
        ...
    """

    # TODO: Print a header to show what function is running
    # TODO: Use print("=" * 50) and print("JOINING STATION DATA WITH READINGS")

    # TODO: Input validation - check if both DataFrames are valid
    # TODO: Check for None or empty DataFrames, return empty DataFrame if invalid

    # TODO: Check for required columns in both DataFrames
    # TODO: Both need 'station_id' column for joining
    # TODO: If missing, print error and return empty DataFrame

    # TODO: Print input data summary
    # TODO: Show number of stations and number of readings

    # TODO: Analyze the relationship between datasets
    # TODO: Get unique station_ids from both DataFrames using .unique()
    # TODO: Find stations that are in both datasets (intersection)
    # TODO: Find stations only in stations_df (difference)
    # TODO: Find stations only in readings_df (difference)
    # TODO: Report these relationships to help understand the data

    # TODO: Perform the join using pd.merge()
    # TODO: Use LEFT JOIN to preserve all readings: how='left'
    # TODO: Join on 'station_id' column: on='station_id'
    # TODO: Syntax: pd.merge(readings_df, stations_df, on='station_id', how='left')

    # TODO: Validate the join results
    # TODO: Check that no readings were lost (row count should match readings_df)
    # TODO: Check which new columns were added from stations_df
    # TODO: Check how many readings have complete location information

    # TODO: Report join results
    # TODO: - Original readings count
    # TODO: - Final joined data count
    # TODO: - Confirmation that all readings preserved
    # TODO: - New columns added
    # TODO: - Coverage of location data

    # TODO: If some readings lack location data, report which stations are missing

    # TODO: Print completion message

    # TODO: Return the joined DataFrame

    pass  # Remove this line when you implement the function


def save_processed_data(df, output_file):
    """
    SAVE PROCESSED DATA (Like saving your Excel work so you can use it later)

    This function saves your processed DataFrame to a CSV file that you can open in
    QGIS, Excel, or other programs. It includes validation to make sure the file
    was saved correctly!

    📚 Learning Resource: See `notebooks/05_function_save_processed_data.ipynb`
    🧪 Test Command: `uv run pytest tests/test_pandas_basics.py::test_save_processed_data -v`

    Args:
        df (pandas.DataFrame): The processed data to save
        output_file (str): Path where to save the CSV file (e.g., 'output/processed_data.csv')

    Returns:
        bool: True if saving was successful, False otherwise

    Example:
        >>> success = save_processed_data(processed_df, 'output/final_results.csv')
        Saving processed data...
        File saved: output/final_results.csv
        File size: 15.2 KB
        Data rows saved: 247
        Ready for use in QGIS!
    """

    # TODO: Print a header to show what function is running
    # TODO: Use print("=" * 50) and print("SAVING PROCESSED DATA")

    # TODO: Input validation
    # TODO: Check if df is None, return False if invalid
    # TODO: Check if df is empty (warn but continue - empty files can be valid)
    # TODO: Check if output_file is valid string, return False if invalid

    # TODO: Convert output_file to Path object for easier manipulation
    # TODO: Use: output_path = Path(output_file)

    # TODO: Print information about the data being saved
    # TODO: - DataFrame shape
    # TODO: - Number of columns
    # TODO: - Memory usage (optional)

    # TODO: Print information about output location
    # TODO: - Full file path
    # TODO: - Directory where file will be saved
    # TODO: - Filename

    # TODO: Create output directory if it doesn't exist
    # TODO: Use output_path.parent.mkdir(parents=True, exist_ok=True)
    # TODO: Wrap in try/except to handle permission errors
    # TODO: Return False if directory creation fails

    # TODO: Save the data using df.to_csv()
    # TODO: Use these parameters for good formatting:
    # TODO: - index=False (don't save row numbers)
    # TODO: - float_format='%.3f' (round floats to 3 decimals)
    # TODO: - na_rep='' (empty string for missing values)
    # TODO: Wrap in try/except to handle save errors (permissions, disk space, etc.)
    # TODO: Return False if saving fails

    # TODO: Validate the saved file
    # TODO: Check that file exists using output_path.exists()
    # TODO: Get file size using output_path.stat().st_size
    # TODO: Try reading the file back to verify it's valid
    # TODO: Compare original and reloaded shapes to ensure data integrity

    # TODO: Print success summary
    # TODO: - File location (full path)
    # TODO: - File size in bytes and KB
    # TODO: - Number of data rows saved
    # TODO: - Number of columns saved
    # TODO: - Confirmation message about being ready for QGIS/Excel

    # TODO: Return True for success

    pass  # Remove this line when you implement the function


# Helper functions (you don't need to modify these)
def _check_required_columns(df, required_columns, data_name="DataFrame"):
    """
    Helper function to check if DataFrame has required columns.

    Args:
        df: DataFrame to check
        required_columns: List of required column names
        data_name: Name for error messages

    Returns:
        List of missing column names (empty if all present)
    """
    if df is None or df.empty:
        return required_columns

    missing_columns = [col for col in required_columns if col not in df.columns]
    return missing_columns


def _format_number(value, decimals=1):
    """
    Helper function to safely format numbers with specified decimal places.

    Args:
        value: Number to format
        decimals: Number of decimal places

    Returns:
        Formatted number or original value if not numeric
    """
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return value
