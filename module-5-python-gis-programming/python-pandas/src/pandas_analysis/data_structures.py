"""
Data Structures Module - Student Implementation
====================================================

Welcome! This module teaches you how to work with pandas Series and DataFrames.

Don't worry if you're new to programming - we'll guide you through each step!

IMPORTANT: Read all the comments carefully. They contain step-by-step instructions.

What you'll learn:
- How to create pandas Series (like a single column of data)
- How to create pandas DataFrames (like a spreadsheet)
- How to analyze and optimize data for better performance
- How to work with different data types (numbers, text, dates)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Any


def create_gis_series(data: List[Union[int, float]],
                     index: List[str],
                     name: str) -> pd.Series:
    """
    CREATE A PANDAS SERIES (Think of it as a single column with labels)

    A pandas Series is like a single column in Excel with row labels.

    Example of what we want to create:
    Station_A    100.0
    Station_B    200.5
    Station_C    300.0
    Name: elevation_m, dtype: float64

    Your Task: Fill in the missing code below to create this Series.

    Args:
        data: A list of numbers like [100, 200.5, 300]
        index: A list of labels like ['Station_A', 'Station_B', 'Station_C']
        name: A name for this data like 'elevation_m'

    Returns:
        A pandas Series with the data, labels, and name
    """

    # STEP 1: Check if the data and index have the same length
    # If they don't match, we should raise an error
    # HINT: Use len(data) and len(index) to check lengths
    # HINT: Use "raise ValueError('message')" to create an error

    if len(data) != len(index):
        raise ValueError("Data and index must have the same length")

    # STEP 2: Handle the case where data is empty
    # If both data and index are empty, return an empty Series
    # HINT: Check if len(data) == 0

    if len(data) == 0:
        return pd.Series([], name=name, dtype=float)

    # STEP 3: Create the pandas Series
    # The pandas Series constructor looks like: pd.Series(data, index=index, name=name)
    # FILL IN THE MISSING PARTS BELOW:

    series = pd.Series(
        data,           # Put the data here
        index=index,    # Put the index here
        name=name       # Put the name here
    )

    # STEP 4: Return the series
    return series

    # That's it! The tests will check that your Series:
    # - Has the right data values
    # - Has the right index labels
    # - Has the right name
    # - Handles mixed integers and floats correctly


def analyze_series_properties(series: pd.Series) -> Dict[str, Any]:
    """
    ANALYZE A PANDAS SERIES (Extract information about the data)

    This function looks at a pandas Series and tells us important information,
    like what type of data it contains and how much memory it uses.

    Think of it like getting a "summary report" about your data.

    Your Task: Extract 5 specific pieces of information about the Series.

    Args:
        series: A pandas Series to analyze

    Returns:
        A dictionary with exactly these 5 keys:
        - 'dtype': What type of data (like int64, float64, object)
        - 'size': How many values are in the Series
        - 'index_type': What type the index labels are
        - 'has_nulls': True if there are missing values, False if not
        - 'memory_usage': How many bytes of memory it uses (as an integer)
    """

    # Create an empty dictionary to store our results
    result = {}

    # STEP 1: Get the data type
    # HINT: Use series.dtype to get the data type
    # FILL IN: result['dtype'] = ???

    result['dtype'] = series.dtype

    # STEP 2: Get the number of elements
    # HINT: Use series.size or len(series) to count elements
    # FILL IN: result['size'] = ???

    result['size'] = series.size

    # STEP 3: Get the index type
    # HINT: Use type(series.index) to get the index type
    # FILL IN: result['index_type'] = ???

    result['index_type'] = type(series.index)

    # STEP 4: Check if there are any missing (null) values
    # HINT: Use series.isna().any() - this returns True if ANY value is missing
    # FILL IN: result['has_nulls'] = ???

    result['has_nulls'] = series.isna().any()

    # STEP 5: Get memory usage in bytes
    # HINT: Use series.memory_usage(deep=True) to get exact memory usage
    # HINT: Make sure to convert to int() since tests expect an integer
    # FILL IN: result['memory_usage'] = ???

    result['memory_usage'] = int(series.memory_usage(deep=True))

    # Return the dictionary with all our findings
    return result


def create_gis_dataframe(data_dict: Dict[str, List[Any]]) -> pd.DataFrame:
    """
    CREATE A SMART DATAFRAME (Like a spreadsheet that understands your data)

    A DataFrame is like an Excel spreadsheet - it has multiple columns of data.
    But we want to make it "smart" by automatically detecting what type of data
    each column contains and converting it to the best format.

    Examples of smart conversions:
    - Text that looks like dates → Convert to actual date format
    - Repeated text values → Convert to "categories" to save memory
    - Keep numbers and True/False values as they are

    Your Task: Create a DataFrame and make these smart conversions.

    Args:
        data_dict: A dictionary like {'column_name': [values], 'other_column': [values]}

    Returns:
        A DataFrame with optimized data types
    """

    # STEP 1: Handle empty input
    # If the dictionary is empty, return an empty DataFrame
    if not data_dict or len(data_dict) == 0:
        return pd.DataFrame()

    # STEP 2: Create a basic DataFrame from the dictionary
    # HINT: Use pd.DataFrame(data_dict) to create a DataFrame
    # FILL IN: df = ???

    df = pd.DataFrame(data_dict)

    # STEP 3: Go through each column and make it smarter
    for column_name in df.columns:
        column_data = df[column_name]

        # STEP 3A: Try to convert date-like text to actual dates
        # We only do this for text columns (dtype 'object')
        if column_data.dtype == 'object':

            # Try to convert to dates - if it works, great! If not, keep as text
            try:
                # HINT: Use pd.to_datetime(column_data, errors='coerce')
                # The 'errors=coerce' means "if it fails, just put NaT (Not a Time)"
                converted_dates = pd.to_datetime(column_data, errors='coerce')

                # Only keep the conversion if most values successfully converted
                # (This prevents converting random text to dates)
                if converted_dates.notna().sum() > len(converted_dates) * 0.5:
                    df[column_name] = converted_dates
                    continue  # Move to next column since we're done with this one
            except:
                pass  # If anything goes wrong, just keep the original data

        # STEP 3B: Convert repeated text values to categories (saves memory)
        # Only do this for text columns that weren't converted to dates
        if column_data.dtype == 'object':

            # Check if this column has lots of repeated values
            # HINT: Use len(column_data.unique()) to count unique values
            # HINT: Use len(column_data) to count total values
            unique_ratio = len(column_data.unique()) / len(column_data)

            # If less than 50% of values are unique, convert to category
            if unique_ratio < 0.5:
                # HINT: Use column_data.astype('category') to convert
                # FILL IN: df[column_name] = ???
                df[column_name] = column_data.astype('category')

    # STEP 4: Return the smart DataFrame
    return df


def optimize_dataframe_memory(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    MAKE DATAFRAME USE LESS MEMORY (Like compressing a file to save space)

    DataFrames can use lots of computer memory. This function makes them smaller
    while keeping all the data exactly the same.

    Think of it like this:
    - Instead of using a huge truck to carry a small box, use a small car
    - Instead of storing the number 5 as a giant number, store it as a tiny number

    Your Task: Make the DataFrame use less memory and report how much you saved.

    Args:
        df: The DataFrame to make smaller

    Returns:
        - The compressed DataFrame (same data, less memory)
        - A report about how much memory you saved
    """

    # STEP 1: Handle empty DataFrame
    if df.empty:
        return df.copy(), {
            'original_memory_mb': 0.0,
            'optimized_memory_mb': 0.0,
            'total_reduction_percent': 0.0
        }

    # STEP 2: Measure original memory usage
    # HINT: Use df.memory_usage(deep=True).sum() to get total memory in bytes
    # HINT: Divide by (1024 * 1024) to convert bytes to megabytes (MB)
    original_memory_bytes = df.memory_usage(deep=True).sum()
    original_memory_mb = original_memory_bytes / (1024 * 1024)

    # STEP 3: Create a copy to optimize (don't change the original)
    optimized_df = df.copy()

    # STEP 4: Optimize each column
    for column_name in optimized_df.columns:
        column_data = optimized_df[column_name]

        # STEP 4A: Optimize integer columns (make them smaller)
        if column_data.dtype in ['int64', 'int32', 'int16']:
            # HINT: Use pd.to_numeric(column_data, downcast='integer')
            # This automatically picks the smallest integer type that fits
            # FILL IN: optimized_df[column_name] = ???
            optimized_df[column_name] = pd.to_numeric(column_data, downcast='integer')

        # STEP 4B: Optimize float columns (make them smaller if safe)
        elif column_data.dtype in ['float64']:
            # Try to use float32 instead of float64 (half the memory!)
            # But only if we don't lose important decimal places
            try:
                # HINT: Use pd.to_numeric(column_data, downcast='float')
                smaller_float = pd.to_numeric(column_data, downcast='float')
                optimized_df[column_name] = smaller_float
            except:
                pass  # If something goes wrong, keep the original

        # STEP 4C: Convert columns that are just 0s and 1s to True/False
        elif column_data.dtype in ['int64', 'int32', 'int16', 'int8']:
            unique_values = set(column_data.dropna().unique())
            # Check if column only contains 0 and 1 (or just 0, or just 1)
            if unique_values.issubset({0, 1}):
                # HINT: Convert to boolean using .astype('bool')
                # FILL IN: optimized_df[column_name] = ???
                optimized_df[column_name] = column_data.astype('bool')

        # STEP 4D: Convert repeated text to categories (already done in create_gis_dataframe)
        elif column_data.dtype == 'object':
            unique_ratio = len(column_data.unique()) / len(column_data)
            if unique_ratio < 0.5:
                optimized_df[column_name] = column_data.astype('category')

    # STEP 5: Measure new memory usage
    optimized_memory_bytes = optimized_df.memory_usage(deep=True).sum()
    optimized_memory_mb = optimized_memory_bytes / (1024 * 1024)

    # STEP 6: Calculate how much we saved
    if original_memory_mb > 0:
        # HINT: Percentage reduction = (original - new) / original * 100
        # FILL IN: reduction_percent = ???
        reduction_percent = (original_memory_mb - optimized_memory_mb) / original_memory_mb * 100
    else:
        reduction_percent = 0.0

    # STEP 7: Create the summary report
    memory_info = {
        'original_memory_mb': round(original_memory_mb, 4),
        'optimized_memory_mb': round(optimized_memory_mb, 4),
        'total_reduction_percent': round(reduction_percent, 2)
    }

    # STEP 8: Return both the optimized DataFrame and the report
    return optimized_df, memory_info


# ==============================================================================
# HELPER SECTION - You can ignore this section if you want!
# ==============================================================================
# These functions are optional helpers. The main functions above will work
# without these, but you can implement them if you want extra practice.

def _is_date_column(series: pd.Series) -> bool:
    """
    BONUS HELPER: Detect if a column contains dates
    (You don't need to implement this - it's just for extra practice!)
    """
    if series.dtype != 'object':
        return False

    try:
        # Try to convert a few sample values to dates
        sample_size = min(10, len(series))
        sample = series.dropna().head(sample_size)

        if len(sample) == 0:
            return False

        converted = pd.to_datetime(sample, errors='coerce')
        success_rate = converted.notna().sum() / len(converted)

        return success_rate > 0.5
    except:
        return False


def _should_be_categorical(series: pd.Series, threshold: float = 0.5) -> bool:
    """
    BONUS HELPER: Decide if a column should be converted to category type
    (You don't need to implement this - it's just for extra practice!)
    """
    if series.dtype != 'object':
        return False

    if len(series) == 0:
        return False

    unique_ratio = len(series.unique()) / len(series)
    return unique_ratio < threshold


# ==============================================================================
# CONSTANTS - Useful information you can use in your functions
# ==============================================================================

# Common date formats you might encounter
DATE_FORMATS = [
    '%Y-%m-%d',           # 2020-01-15
    '%m/%d/%Y',           # 01/15/2020
    '%d/%m/%Y',           # 15/01/2020
    '%Y-%m-%d %H:%M:%S'   # 2020-01-15 14:30:00
]

# Different types of numbers pandas can store
INTEGER_TYPES = ['int8', 'int16', 'int32', 'int64']
FLOAT_TYPES = ['float32', 'float64']

"""
CONGRATULATIONS! 🎉

If you've made it this far, you've learned how to:
✅ Create pandas Series with proper indexing
✅ Analyze data to understand its properties
✅ Create smart DataFrames that understand your data types
✅ Optimize memory usage to make your programs faster

These skills are super valuable for working with real-world data!

Remember:
- Read error messages carefully - they often tell you exactly what's wrong
- Test your functions with small examples first
- Don't be afraid to experiment - you can always undo changes
- Ask for help if you get stuck!

Good luck! 🚀
"""
