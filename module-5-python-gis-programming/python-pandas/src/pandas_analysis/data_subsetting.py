"""
Data Subsetting Module - Student Implementation
===============================================

Welcome! This module teaches you how to filter and select data in pandas.

Think of filtering data like asking questions:
- "Show me only the rows where air quality is good"
- "Find all the data from stations with temperature between 15-30 degrees"
- "Give me data that meets multiple conditions at once"

Don't worry if this seems complex - we'll break it down into simple steps!

What you'll learn:
- How to filter rows based on conditions (boolean indexing)
- How to combine multiple conditions (AND, OR logic)
- How to handle missing data when filtering
- How to make your filters run fast on large datasets

IMPORTANT: Read all the comments carefully. They guide you step-by-step!
"""

import pandas as pd
import numpy as np
import time
from typing import Dict, List, Tuple, Union, Any, Optional


def boolean_filter_environmental_data(df: pd.DataFrame,
                                    air_quality_threshold: float = 100.0,
                                    temperature_range: Tuple[float, float] = (15.0, 30.0)) -> pd.DataFrame:
    """
    FILTER ENVIRONMENTAL DATA (Like asking questions about your data)

    Imagine you have a spreadsheet of environmental monitoring data from different
    weather stations. You want to find only the "good quality" readings:
    - Air quality must be good (low numbers are better)
    - Temperature must be comfortable (not too hot, not too cold)
    - No missing/broken sensor readings

    This is like asking: "Show me only the rows where air quality ≤ 100 AND
    temperature is between 15-30 degrees AND we have no missing data"

    Your Task: Write the filtering logic to answer this question.

    Args:
        df: A DataFrame with environmental data (like a spreadsheet)
        air_quality_threshold: Maximum OK air quality (default 100.0)
        temperature_range: (min_temp, max_temp) comfortable range (default 15-30)

    Returns:
        A filtered DataFrame with only the "good" rows
    """

    # STEP 1: Handle empty DataFrame
    # If someone gives us empty data, just return it as-is
    if df.empty:
        return df.copy()

    # STEP 2: Check that required columns exist
    # We need these columns to do our filtering
    required_columns = ['air_quality_index', 'temperature_celsius', 'humidity_percent']

    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # STEP 3: Create individual filter conditions
    # Think of each condition as a True/False question for each row

    # CONDITION 1: Air quality must be good (≤ threshold)
    # HINT: Use df['column_name'] <= value to create a True/False series
    # FILL IN: air_quality_ok = ???

    air_quality_ok = df['air_quality_index'] <= air_quality_threshold

    # CONDITION 2: Temperature must be in comfortable range
    # We need BOTH: temperature >= minimum AND temperature <= maximum
    # HINT: Use df['column_name'] >= min_temp for minimum check
    # HINT: Use df['column_name'] <= max_temp for maximum check
    # HINT: Use & to combine conditions (AND logic)
    # FILL IN: temperature_ok = ???

    min_temp, max_temp = temperature_range
    temperature_ok = (df['temperature_celsius'] >= min_temp) & (df['temperature_celsius'] <= max_temp)

    # CONDITION 3: No missing data in critical columns
    # We don't want rows where important sensor readings are missing
    # HINT: Use df['column_name'].notna() to check if values are not missing
    # HINT: Use & to combine multiple "not missing" checks
    # FILL IN: no_missing_data = ???

    no_missing_data = (
        df['air_quality_index'].notna() &
        df['temperature_celsius'].notna() &
        df['humidity_percent'].notna()
    )

    # STEP 4: Combine all conditions
    # All conditions must be True for a row to be included
    # HINT: Use & to combine all three condition variables
    # FILL IN: all_conditions = ???

    all_conditions = air_quality_ok & temperature_ok & no_missing_data

    # STEP 5: Apply the filter to get our result
    # This gives us only the rows where all_conditions is True
    # HINT: Use df[condition] to filter a DataFrame
    # FILL IN: filtered_df = ???

    filtered_df = df[all_conditions]

    # STEP 6: Return a copy to avoid modifying the original data
    return filtered_df.copy()

    # That's it! Your function now:
    # ✅ Filters for good air quality
    # ✅ Filters for comfortable temperature
    # ✅ Removes rows with missing sensor data
    # ✅ Handles edge cases like empty data


def multi_condition_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    ANALYZE DATA BY CREATING MULTIPLE CATEGORIES (Like sorting into different boxes)

    Imagine you're sorting environmental readings into different quality categories:
    - "Excellent" - Perfect air and temperature
    - "Good" - Decent air quality, any temperature
    - "Poor" - Everything else

    This is like having three different boxes and putting each row of data
    into the appropriate box based on its values.

    Your Task: Sort the data into these three categories and return all three boxes.

    Args:
        df: DataFrame with environmental data

    Returns:
        A dictionary with three keys:
        - 'excellent': DataFrame with the best quality data
        - 'good': DataFrame with decent quality data
        - 'poor': DataFrame with everything else
    """

    # STEP 1: Handle empty DataFrame
    if df.empty:
        empty_df = pd.DataFrame(columns=df.columns if hasattr(df, 'columns') else [])
        return {
            'excellent': empty_df,
            'good': empty_df,
            'poor': empty_df
        }

    # STEP 2: Check that required columns exist
    required_columns = ['air_quality_index', 'temperature_celsius']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # STEP 3: Define the criteria for each category

    # EXCELLENT CONDITIONS:
    # - Air quality ≤ 50 (really good air)
    # - Temperature between 20-25°C (perfect comfort)
    # - No missing data in key columns
    # HINT: Create conditions similar to the previous function
    # FILL IN the conditions below:

    excellent_air = df['air_quality_index'] <= 50
    excellent_temp = (df['temperature_celsius'] >= 20) & (df['temperature_celsius'] <= 25)
    excellent_no_missing = df['air_quality_index'].notna() & df['temperature_celsius'].notna()

    # Combine all excellent conditions
    # FILL IN: excellent_condition = ???
    excellent_condition = excellent_air & excellent_temp & excellent_no_missing

    # GOOD CONDITIONS:
    # - Air quality ≤ 100 (acceptable air)
    # - Any temperature (we're not picky about temperature for "good")
    # - No missing data in key columns
    # - BUT NOT already classified as excellent
    # HINT: Use ~ before a condition to mean "NOT that condition"

    good_air = df['air_quality_index'] <= 100
    good_no_missing = df['air_quality_index'].notna() & df['temperature_celsius'].notna()
    not_excellent = ~excellent_condition  # NOT excellent

    # FILL IN: good_condition = ???
    good_condition = good_air & good_no_missing & not_excellent

    # POOR CONDITIONS:
    # - Everything else that's not excellent or good
    # HINT: Use ~ before a condition to mean "NOT that condition"
    # HINT: Use | to mean "OR"
    # FILL IN: poor_condition = ???

    poor_condition = ~(excellent_condition | good_condition)

    # STEP 4: Create the three separate DataFrames
    # Apply each condition to create filtered versions

    # FILL IN the missing parts:
    excellent_df = df[excellent_condition].copy()
    good_df = df[good_condition].copy()
    poor_df = df[poor_condition].copy()

    # STEP 5: Package everything into a dictionary
    result = {
        'excellent': excellent_df,
        'good': good_df,
        'poor': poor_df
    }

    return result

    # Your function now creates three categories:
    # ✅ "Excellent" - Perfect conditions
    # ✅ "Good" - Acceptable conditions
    # ✅ "Poor" - Everything else
    # ✅ No overlap between categories
    # ✅ Every row goes into exactly one category


# ==============================================================================
# HELPER SECTION - Bonus functions for extra practice!
# ==============================================================================

def _validate_dataframe_structure(df: pd.DataFrame, required_columns: List[str]) -> None:
    """
    BONUS HELPER: Check if DataFrame has the columns we need
    (You can implement this for extra practice, or skip it!)
    """
    if df.empty:
        return

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame missing required columns: {missing_columns}")


def _check_data_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    BONUS HELPER: Report what type of data is in each column
    (You can implement this for extra practice, or skip it!)
    """
    return {col: str(df[col].dtype) for col in df.columns}


def _count_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """
    BONUS HELPER: Count how many missing values are in each column
    (You can implement this for extra practice, or skip it!)
    """
    return df.isnull().sum().to_dict()


# ==============================================================================
# EXAMPLES - Try these in a Python console to understand how filtering works!
# ==============================================================================

"""
EXAMPLE 1: Simple filtering

# Create some sample data
data = {
    'air_quality_index': [30, 150, 75, 200, 45],
    'temperature_celsius': [22, 35, 18, 10, 25],
    'humidity_percent': [60, 80, 45, 30, 55]
}
df = pd.DataFrame(data)

# Apply our filter
filtered = boolean_filter_environmental_data(df, air_quality_threshold=100)
print(f"Original rows: {len(df)}")
print(f"Filtered rows: {len(filtered)}")

EXAMPLE 2: Understanding boolean conditions

# This creates a True/False series
air_good = df['air_quality_index'] <= 100
print(air_good)
# Output: 0    True, 1    False, 2    True, 3    False, 4    True

# Use it to filter
good_air_data = df[air_good]
print(good_air_data)
# Shows only rows where air_good is True

EXAMPLE 3: Combining conditions

# Multiple conditions with AND (&)
both_conditions = (df['air_quality_index'] <= 100) & (df['temperature_celsius'] >= 15)

# Multiple conditions with OR (|)
either_condition = (df['air_quality_index'] <= 50) | (df['temperature_celsius'] >= 25)
"""

# ==============================================================================
# COMMON MISTAKES - Watch out for these!
# ==============================================================================

"""
❌ MISTAKE 1: Using 'and' instead of '&'
# Wrong:
condition = (df['col1'] > 5) and (df['col2'] < 10)  # This won't work!

# Right:
condition = (df['col1'] > 5) & (df['col2'] < 10)   # Use & for pandas

❌ MISTAKE 2: Forgetting parentheses
# Wrong:
condition = df['col1'] > 5 & df['col2'] < 10  # Operator precedence issues!

# Right:
condition = (df['col1'] > 5) & (df['col2'] < 10)  # Always use parentheses

❌ MISTAKE 3: Not handling missing values
# Problem:
df[df['column'] > 5]  # Includes NaN rows, which might not be wanted

# Better:
df[(df['column'] > 5) & df['column'].notna()]  # Exclude missing values

❌ MISTAKE 4: Using assignment (=) instead of comparison (==)
# Wrong:
df[df['status'] = 'active']  # This tries to assign, not compare!

# Right:
df[df['status'] == 'active']  # Use == to compare values
"""

"""
CONGRATULATIONS! 🎉

You've learned the fundamentals of data filtering in pandas:
✅ Creating boolean conditions (True/False questions)
✅ Combining multiple conditions with & (AND) and | (OR)
✅ Handling missing data appropriately
✅ Organizing data into multiple categories
✅ Writing efficient filtering code

These skills are essential for:
- Environmental data analysis
- GIS data processing
- Quality control and data cleaning
- Exploratory data analysis
- Real-world data science projects

Tips for success:
- Start with simple conditions and build up complexity
- Always test your conditions on small sample data first
- Use parentheses liberally when combining conditions
- Check for missing data before filtering
- Remember: & means AND, | means OR, ~ means NOT

Keep practicing and you'll become a pandas filtering expert! 🚀
"""
