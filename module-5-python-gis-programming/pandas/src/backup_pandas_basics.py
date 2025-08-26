"""
Pandas Basics for GIS Data Analysis - Student Implementation
===========================================================

Welcome! This module teaches you essential pandas skills for working with GIS data.

Pandas is Python's most popular library for working with tabular data (like CSV files).
Think of it as Excel, but with the power of Python programming!

Don't worry if you're new to pandas - we'll guide you through each step with
detailed comments and examples.

What you'll learn:
- How to load CSV files into pandas DataFrames
- How to explore and understand your data
- How to filter data based on conditions
- How to calculate statistics and group data
- How to join datasets together
- How to save your results

IMPORTANT: Read all the comments carefully. They explain what each line does!
"""

import pandas as pd
import numpy as np
import os


def load_and_explore_gis_data(file_path):
    """
    LOAD AND EXPLORE GIS DATA (Like opening a spreadsheet and getting familiar with it)

    This function loads a CSV file and shows you important information about the data,
    like how many rows and columns it has, what the columns are called, and what the
    first few rows look like.

    Think of this as your first step whenever you get a new dataset - you need to
    understand what you're working with before you can analyze it!

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

    print("=" * 50)
    print("LOADING AND EXPLORING GIS DATA")
    print("=" * 50)

    # STEP 1: Check if the file exists
    # Before trying to load a file, we should make sure it actually exists
    # This prevents confusing error messages later

    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        print("Please check:")
        print("- Is the file path correct?")
        print("- Are you in the right directory?")
        print("- Does the file exist?")
        return None

    print(f"📁 Loading data from: {file_path}")

    # STEP 2: Load the CSV file into a pandas DataFrame
    # pd.read_csv() is the most common way to load data into pandas
    # A DataFrame is like a spreadsheet - it has rows and columns

    try:
        df = pd.read_csv(file_path)
        print("✅ File loaded successfully!")
    except Exception as e:
        print(f"❌ ERROR loading file: {e}")
        print("Common solutions:")
        print("- Check if the file is a valid CSV")
        print("- Make sure the file isn't open in Excel")
        print("- Try opening the file in a text editor to check its format")
        return None

    # STEP 3: Show basic information about the dataset
    # This helps you understand what you're working with

    print(f"\n📊 DATASET OVERVIEW:")
    print(f"Shape: {df.shape} - {df.shape[0]} rows and {df.shape[1]} columns")

    # STEP 4: Show the column names
    # Column names tell you what kind of information each column contains
    print(f"\n📋 COLUMNS:")
    for i, column in enumerate(df.columns, 1):
        print(f"{i:2d}. {column}")

    # STEP 5: Show data types
    # This tells you what kind of data is in each column (numbers, text, dates, etc.)
    print(f"\n🔍 DATA TYPES:")
    for column, dtype in df.dtypes.items():
        print(f"{column:20s}: {dtype}")

    # STEP 6: Show the first 5 rows
    # This gives you a preview of what the actual data looks like
    print(f"\n👀 FIRST 5 ROWS:")
    print(df.head())

    # STEP 7: Show basic statistics for numeric columns
    # This gives you an idea of the range and distribution of your numeric data
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    if len(numeric_columns) > 0:
        print(f"\n📈 SUMMARY STATISTICS (numeric columns only):")
        print(df.describe())
    else:
        print(f"\n📈 No numeric columns found for summary statistics")

    # STEP 8: Check for missing values
    # Missing values (NaN, null, empty) are common in real-world data
    missing_data = df.isnull().sum()
    total_missing = missing_data.sum()

    if total_missing > 0:
        print(f"\n⚠️  MISSING VALUES FOUND:")
        for column, missing_count in missing_data.items():
            if missing_count > 0:
                percentage = (missing_count / len(df)) * 100
                print(f"{column:20s}: {missing_count} missing ({percentage:.1f}%)")
    else:
        print(f"\n✅ NO MISSING VALUES - Great!")

    print("=" * 50)
    print("Data exploration complete!")
    print("=" * 50)

    return df


def filter_environmental_data(df, min_temp=15, max_temp=30, quality="good"):
    """
    FILTER ENVIRONMENTAL DATA (Like using filters in Excel to show only certain rows)

    This function takes a DataFrame with environmental readings and filters it to show
    only the data that meets your criteria. For example, you might only want to see
    readings with good data quality and reasonable temperatures.

    This is very useful for cleaning data before analysis!

    Args:
        df (pandas.DataFrame): The DataFrame with environmental data
        min_temp (float): Minimum acceptable temperature (default: 15°C)
        max_temp (float): Maximum acceptable temperature (default: 30°C)
        quality (str): Required data quality level (default: "good")

    Returns:
        pandas.DataFrame: Filtered DataFrame with only rows meeting the criteria

    Example:
        >>> filtered_df = filter_environmental_data(df, min_temp=20, max_temp=25)
        Filtering environmental data...
        Original dataset: 500 rows
        After filtering: 247 rows kept, 253 rows removed
        ...
    """

    print("=" * 50)
    print("FILTERING ENVIRONMENTAL DATA")
    print("=" * 50)

    # STEP 1: Check if the DataFrame is empty
    if df is None or df.empty:
        print("❌ ERROR: DataFrame is empty or None")
        return pd.DataFrame()

    # Show the filtering criteria
    print(f"🔍 FILTERING CRITERIA:")
    print(f"   Temperature: between {min_temp}°C and {max_temp}°C")
    print(f"   Data quality: '{quality}'")

    # STEP 2: Check that required columns exist
    # We need these columns to do our filtering
    required_columns = ['temperature_c', 'data_quality']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"❌ ERROR: Missing required columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
        return pd.DataFrame()

    print(f"✅ All required columns found")

    # STEP 3: Show original dataset size
    original_size = len(df)
    print(f"\n📊 Original dataset: {original_size} rows")

    # STEP 4: Create filter conditions
    # In pandas, we create "boolean masks" - these are True/False for each row

    # CONDITION 1: Temperature must be within the specified range
    # This creates a True/False value for each row
    temp_condition = (df['temperature_c'] >= min_temp) & (df['temperature_c'] <= max_temp)

    # Let's see how many rows meet the temperature condition
    temp_passed = temp_condition.sum()  # sum() counts True values
    print(f"   Temperature filter: {temp_passed} rows pass")

    # CONDITION 2: Data quality must match what we want
    quality_condition = df['data_quality'] == quality
    quality_passed = quality_condition.sum()
    print(f"   Quality filter: {quality_passed} rows pass")

    # CONDITION 3: No missing values in important columns
    # We don't want rows where temperature or quality data is missing
    not_missing = df['temperature_c'].notna() & df['data_quality'].notna()
    not_missing_passed = not_missing.sum()
    print(f"   No missing data: {not_missing_passed} rows pass")

    # STEP 5: Combine all conditions
    # ALL conditions must be True for a row to be kept
    # The & symbol means "AND" in pandas
    all_conditions = temp_condition & quality_condition & not_missing

    # STEP 6: Apply the filter to create the filtered DataFrame
    # df[condition] keeps only rows where condition is True
    filtered_df = df[all_conditions].copy()  # .copy() prevents modifying the original

    # STEP 7: Show results
    filtered_size = len(filtered_df)
    removed_size = original_size - filtered_size

    print(f"\n📊 FILTERING RESULTS:")
    print(f"   Rows kept: {filtered_size}")
    print(f"   Rows removed: {removed_size}")

    if original_size > 0:
        percentage_kept = (filtered_size / original_size) * 100
        print(f"   Percentage kept: {percentage_kept:.1f}%")

    # STEP 8: Show some examples of what was kept
    if not filtered_df.empty:
        print(f"\n👀 SAMPLE OF FILTERED DATA:")
        print(filtered_df[['temperature_c', 'data_quality']].head())
    else:
        print(f"\n⚠️  WARNING: No rows remain after filtering!")
        print(f"Try relaxing your criteria:")
        print(f"   - Use wider temperature range")
        print(f"   - Check available quality values: {df['data_quality'].unique()}")

    print("=" * 50)
    print("Filtering complete!")
    print("=" * 50)

    return filtered_df


def calculate_station_statistics(df):
    """
    CALCULATE STATISTICS BY STATION (Like making a summary table in Excel)

    This function groups environmental readings by weather station and calculates
    useful statistics like average temperature, humidity, and number of readings.

    This is very common in GIS work - you often want to summarize data by location,
    region, or other geographic groupings.

    Args:
        df (pandas.DataFrame): DataFrame with columns 'station_id', 'temperature_c',
                              and 'humidity_percent'

    Returns:
        pandas.DataFrame: Summary statistics for each station

    Example:
        >>> stats_df = calculate_station_statistics(readings_df)
        Calculating station statistics...
        Found 5 unique stations
        Station with highest avg temperature: STN_003 (24.5°C)
        ...
    """

    print("=" * 50)
    print("CALCULATING STATION STATISTICS")
    print("=" * 50)

    # STEP 1: Check if DataFrame is valid
    if df is None or df.empty:
        print("❌ ERROR: DataFrame is empty or None")
        return pd.DataFrame()

    # STEP 2: Check for required columns
    required_columns = ['station_id', 'temperature_c', 'humidity_percent']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"❌ ERROR: Missing required columns: {missing_columns}")
        print(f"Available columns: {list(df.columns)}")
        return pd.DataFrame()

    print(f"✅ All required columns found")

    # STEP 3: Show basic information about the data
    total_rows = len(df)
    unique_stations = df['station_id'].nunique()
    print(f"\n📊 DATA OVERVIEW:")
    print(f"   Total readings: {total_rows}")
    print(f"   Unique stations: {unique_stations}")

    # Show the station IDs
    station_list = sorted(df['station_id'].unique())
    print(f"   Station IDs: {station_list}")

    # STEP 4: Group the data by station_id
    # .groupby() is like creating separate tables for each station
    print(f"\n🔄 Grouping data by station...")

    try:
        grouped = df.groupby('station_id')
    except Exception as e:
        print(f"❌ ERROR during grouping: {e}")
        return pd.DataFrame()

    # STEP 5: Calculate statistics for each group
    # We'll create a new DataFrame with one row per station

    print(f"📈 Calculating statistics...")

    # Calculate various statistics
    stats_dict = {
        'station_id': [],
        'reading_count': [],
        'avg_temperature': [],
        'min_temperature': [],
        'max_temperature': [],
        'avg_humidity': [],
        'min_humidity': [],
        'max_humidity': []
    }

    # Loop through each station group and calculate stats
    for station_id, station_data in grouped:
        # Only include stations with valid temperature and humidity data
        valid_temp = station_data['temperature_c'].notna()
        valid_humidity = station_data['humidity_percent'].notna()
        valid_both = valid_temp & valid_humidity
        clean_data = station_data[valid_both]

        if len(clean_data) > 0:
            stats_dict['station_id'].append(station_id)
            stats_dict['reading_count'].append(len(clean_data))
            stats_dict['avg_temperature'].append(clean_data['temperature_c'].mean())
            stats_dict['min_temperature'].append(clean_data['temperature_c'].min())
            stats_dict['max_temperature'].append(clean_data['temperature_c'].max())
            stats_dict['avg_humidity'].append(clean_data['humidity_percent'].mean())
            stats_dict['min_humidity'].append(clean_data['humidity_percent'].min())
            stats_dict['max_humidity'].append(clean_data['humidity_percent'].max())

        print(f"   {station_id}: {len(clean_data)} valid readings")

    # STEP 6: Create the summary DataFrame
    if len(stats_dict['station_id']) == 0:
        print("❌ ERROR: No valid data found for any station")
        return pd.DataFrame()

    stats_df = pd.DataFrame(stats_dict)

    # Round numeric values to make them more readable
    numeric_columns = ['avg_temperature', 'min_temperature', 'max_temperature',
                      'avg_humidity', 'min_humidity', 'max_humidity']
    for col in numeric_columns:
        stats_df[col] = stats_df[col].round(1)

    # STEP 7: Show the results
    print(f"\n📊 STATION STATISTICS SUMMARY:")
    print(stats_df.to_string(index=False))

    # STEP 8: Highlight interesting findings
    if len(stats_df) > 0:
        hottest_station = stats_df.loc[stats_df['avg_temperature'].idxmax()]
        coolest_station = stats_df.loc[stats_df['avg_temperature'].idxmin()]
        most_readings = stats_df.loc[stats_df['reading_count'].idxmax()]

        print(f"\n🌡️  INTERESTING FINDINGS:")
        print(f"   Hottest station: {hottest_station['station_id']} "
              f"(avg: {hottest_station['avg_temperature']}°C)")
        print(f"   Coolest station: {coolest_station['station_id']} "
              f"(avg: {coolest_station['avg_temperature']}°C)")
        print(f"   Most readings: {most_readings['station_id']} "
              f"({most_readings['reading_count']} readings)")

    print("=" * 50)
    print("Station statistics calculation complete!")
    print("=" * 50)

    return stats_df


def join_station_data(stations_df, readings_df):
    """
    JOIN STATION DATA (Like using VLOOKUP in Excel to combine tables)

    This function combines two DataFrames:
    1. stations_df: Information about weather stations (locations, names, etc.)
    2. readings_df: Temperature and humidity measurements from those stations

    The result is a single DataFrame that shows both the measurements AND
    information about where each measurement was taken.

    This is very common in GIS - you often have separate tables that you need
    to combine based on a common field (like station ID).

    Args:
        stations_df (pandas.DataFrame): DataFrame with station information
        readings_df (pandas.DataFrame): DataFrame with measurement data

    Returns:
        pandas.DataFrame: Combined DataFrame with both station info and readings

    Example:
        >>> combined_df = join_station_data(stations_df, readings_df)
        Joining station data...
        Stations: 5 stations
        Readings: 500 measurements
        Result: 500 rows with location information added
        ...
    """

    print("=" * 50)
    print("JOINING STATION DATA")
    print("=" * 50)

    # STEP 1: Check if both DataFrames are valid
    if stations_df is None or stations_df.empty:
        print("❌ ERROR: Stations DataFrame is empty or None")
        return pd.DataFrame()

    if readings_df is None or readings_df.empty:
        print("❌ ERROR: Readings DataFrame is empty or None")
        return pd.DataFrame()

    print(f"✅ Both DataFrames are valid")

    # STEP 2: Check for the common column we'll join on
    join_column = 'station_id'

    if join_column not in stations_df.columns:
        print(f"❌ ERROR: '{join_column}' not found in stations DataFrame")
        print(f"Available columns: {list(stations_df.columns)}")
        return pd.DataFrame()

    if join_column not in readings_df.columns:
        print(f"❌ ERROR: '{join_column}' not found in readings DataFrame")
        print(f"Available columns: {list(readings_df.columns)}")
        return pd.DataFrame()

    print(f"✅ Join column '{join_column}' found in both DataFrames")

    # STEP 3: Show information about what we're joining
    stations_count = len(stations_df)
    readings_count = len(readings_df)
    unique_stations_in_readings = readings_df[join_column].nunique()
    unique_stations_available = stations_df[join_column].nunique()

    print(f"\n📊 DATA TO JOIN:")
    print(f"   Stations DataFrame: {stations_count} stations")
    print(f"   Readings DataFrame: {readings_count} measurements")
    print(f"   Unique stations in readings: {unique_stations_in_readings}")
    print(f"   Unique stations available: {unique_stations_available}")

    # STEP 4: Check which stations in readings have matching station info
    readings_stations = set(readings_df[join_column].unique())
    available_stations = set(stations_df[join_column].unique())

    matching_stations = readings_stations.intersection(available_stations)
    missing_stations = readings_stations - available_stations

    print(f"\n🔍 MATCHING ANALYSIS:")
    print(f"   Stations with matches: {len(matching_stations)}")
    if missing_stations:
        print(f"   Stations missing info: {len(missing_stations)} {sorted(missing_stations)}")
    else:
        print(f"   All reading stations have station info - Perfect!")

    # STEP 5: Perform the join
    # pd.merge() combines DataFrames based on common columns
    # 'left' join keeps all readings, even if some don't have station info
    print(f"\n🔄 Performing join...")

    try:
        # Use 'left' join to keep all readings
        # This means we keep every row from readings_df, and add station info where available
        joined_df = pd.merge(
            readings_df,        # Left table (we keep all rows from this)
            stations_df,        # Right table (we add info from this)
            on=join_column,     # Column to join on
            how='left'          # Type of join
        )
        print(f"✅ Join completed successfully!")

    except Exception as e:
        print(f"❌ ERROR during join: {e}")
        return pd.DataFrame()

    # STEP 6: Analyze the join results
    result_count = len(joined_df)

    print(f"\n📊 JOIN RESULTS:")
    print(f"   Original readings: {readings_count}")
    print(f"   Joined result: {result_count} rows")

    # Check if any readings didn't get station info
    # These would have NaN values in columns from the stations DataFrame
    station_columns = [col for col in stations_df.columns if col != join_column]
    if station_columns:
        # Check for missing values in the first station info column
        first_station_col = station_columns[0]
        missing_info = joined_df[first_station_col].isna().sum()

        if missing_info > 0:
            print(f"   ⚠️  {missing_info} readings have no station info")
        else:
            print(f"   ✅ All readings have complete station info!")

    # STEP 7: Show what new columns were added
    original_columns = set(readings_df.columns)
    new_columns = [col for col in joined_df.columns if col not in original_columns]

    if new_columns:
        print(f"\n📋 NEW COLUMNS ADDED:")
        for col in new_columns:
            print(f"   - {col}")

    # STEP 8: Show a preview of the joined data
    print(f"\n👀 PREVIEW OF JOINED DATA:")
    # Show first few rows with both original and new columns
    preview_columns = list(readings_df.columns)[:3] + new_columns[:3]
    available_preview_columns = [col for col in preview_columns if col in joined_df.columns]

    if available_preview_columns:
        print(joined_df[available_preview_columns].head())
    else:
        print(joined_df.head())

    print("=" * 50)
    print("Join complete!")
    print("=" * 50)

    return joined_df


def save_processed_data(df, output_file):
    """
    SAVE PROCESSED DATA (Like saving your Excel spreadsheet)

    This function saves your processed DataFrame to a CSV file that can be:
    - Opened in Excel or other spreadsheet programs
    - Imported into QGIS for mapping
    - Shared with colleagues
    - Used for further analysis

    Args:
        df (pandas.DataFrame): The DataFrame to save
        output_file (str): Path and filename for the output CSV (like 'output/results.csv')

    Returns:
        bool: True if successful, False if there was an error

    Example:
        >>> success = save_processed_data(processed_df, 'output/environmental_analysis.csv')
        Saving processed data...
        File saved successfully: output/environmental_analysis.csv
        File size: 125.3 KB
        ...
    """

    print("=" * 50)
    print("SAVING PROCESSED DATA")
    print("=" * 50)

    # STEP 1: Check if DataFrame is valid
    if df is None or df.empty:
        print("❌ ERROR: DataFrame is empty or None - nothing to save")
        return False

    print(f"📊 Data to save: {len(df)} rows, {len(df.columns)} columns")

    # STEP 2: Check the output file path
    print(f"💾 Output file: {output_file}")

    # Create the directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"📁 Creating directory: {output_dir}")
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"❌ ERROR creating directory: {e}")
            return False

    # STEP 3: Save the DataFrame to CSV
    print(f"💾 Saving data...")

    try:
        # Save with good default settings:
        # - index=False: Don't save row numbers as a column
        # - float_format='%.2f': Round decimals to 2 places for readability
        df.to_csv(
            output_file,
            index=False,           # Don't include row numbers
            float_format='%.2f'    # Format decimal numbers nicely
        )
        print(f"✅ File saved successfully!")

    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
        print("Common solutions:")
        print("- Make sure the file isn't open in Excel")
        print("- Check that you have write permission to the directory")
        print("- Try a different filename or location")
        return False

    # STEP 4: Verify the file was created and show file info
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)

        # Convert file size to human-readable format
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"

        print(f"\n📁 FILE INFORMATION:")
        print(f"   Location: {os.path.abspath(output_file)}")
        print(f"   Size: {size_str}")
        print(f"   Rows saved: {len(df)}")
        print(f"   Columns saved: {len(df.columns)}")

        # STEP 5: Show column names that were saved
        print(f"\n📋 COLUMNS SAVED:")
        for i, column in enumerate(df.columns, 1):
            print(f"   {i:2d}. {column}")

        # STEP 6: Give helpful next steps
        print(f"\n🎯 WHAT YOU CAN DO WITH THIS FILE:")
        print(f"   📊 Open in Excel or Google Sheets for viewing")
        print(f"   🗺️  Import into QGIS for mapping (if it has coordinates)")
        print(f"   📤 Share with colleagues")
        print(f"   📈 Use for further analysis")
        print(f"   🔄 Read back into Python: pd.read_csv('{output_file}')")

        print("=" * 50)
        print("Data successfully saved!")
        print("=" * 50)

        return True

    else:
        print(f"❌ ERROR: File was not created")
        return False


# ==============================================================================
# HELPER FUNCTIONS - These support the main functions above
# ==============================================================================

def _check_required_columns(df, required_columns, function_name="function"):
    """
    Helper function to check if a DataFrame has all required columns.
    This reduces repetitive code in the main functions.
    """
    if df is None or df.empty:
        return False, ["DataFrame is empty or None"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, missing_columns

    return True, []


def _format_number(number, decimal_places=1):
    """
    Helper function to format numbers for display.
    Makes output more readable.
    """
    try:
        return f"{float(number):.{decimal_places}f}"
    except (ValueError, TypeError):
        return str(number)


# ==============================================================================
# EXAMPLE USAGE - Uncomment these lines to test your functions
# ==============================================================================

# """
# Example of how to use all the functions together:

if __name__ == "__main__":

    # Step 1: Load station locations
    stations = load_and_explore_gis_data('data/weather_stations.csv')

    # # Step 2: Load temperature readings
    # readings = load_and_explore_gis_data('data/temperature_readings.csv')

    # # Step 3: Filter for good quality data
    # filtered_readings = filter_environmental_data(readings, min_temp=15, max_temp=30, quality="good")

    # # Step 4: Calculate statistics by station
    # station_stats = calculate_station_statistics(filtered_readings)

    # # Step 5: Join station info with readings
    # combined_data = join_station_data(stations, filtered_readings)

    # # Step 6: Save the results
    # save_processed_data(combined_data, 'output/processed_environmental_data.csv')
    # save_processed_data(station_stats, 'output/station_statistics.csv')
# """

"""
CONGRATULATIONS! 🎉

You've learned the essential pandas skills for GIS data analysis:

✅ Loading CSV files and exploring data structure
✅ Filtering data based on multiple conditions
✅ Calculating summary statistics by groups
✅ Joining related datasets together
✅ Saving results for further use

These skills form the foundation for:
🌍 Environmental data analysis
🏙️  Urban planning and demographics
🌊 Hydrological and climate studies
🌱 Agricultural and ecological research
🗺️  Preparing data for GIS mapping

Next steps:
- Practice with your own datasets
- Learn GeoPandas for spatial data
- Explore data visualization with matplotlib
- Try more advanced pandas operations

Keep up the great work! 🚀
"""
