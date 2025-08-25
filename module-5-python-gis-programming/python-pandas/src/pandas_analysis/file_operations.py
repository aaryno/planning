"""
File Operations Module - Student Implementation
==============================================

Welcome! This module teaches you how to read and write data files with pandas.

Think of this like learning to open different types of documents:
- Reading CSV files (like opening Excel spreadsheets)
- Writing data back to files (like saving your work)
- Handling different file formats and encodings
- Making sure your data loaded correctly

Don't worry if file operations seem tricky - we'll guide you step by step!

What you'll learn:
- How to read CSV files into pandas DataFrames
- How to write DataFrames to different file formats
- How to handle common file problems (encoding, missing files, etc.)
- How to validate that your data loaded correctly
- How to make file operations fast and reliable

IMPORTANT: Read all the comments carefully. They contain step-by-step instructions!
"""

import pandas as pd
import numpy as np
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any, Optional


def load_environmental_data(file_path: str,
                          encoding: str = 'utf-8',
                          delimiter: str = ',') -> pd.DataFrame:
    """
    LOAD ENVIRONMENTAL DATA FROM CSV FILES (Like opening a digital spreadsheet)

    Imagine you have environmental sensor data saved in a CSV file (like Excel, but simpler).
    This function opens that file and converts it into a pandas DataFrame so you can work with it.

    Common scenarios:
    - Weather station data exported from sensors
    - Air quality measurements from monitoring stations
    - Water quality data from environmental agencies
    - Any tabular data stored in CSV format

    Your Task: Write code to safely load a CSV file and handle common problems.

    Args:
        file_path: Path to the CSV file (like "data/weather_stations.csv")
        encoding: How the file is encoded (usually 'utf-8')
        delimiter: What separates the columns (usually ',')

    Returns:
        pandas DataFrame with the loaded data
    """

    # STEP 1: Check if the file actually exists
    # Before trying to open a file, make sure it's really there!
    # HINT: Use os.path.exists() or Path(file_path).exists()
    # FILL IN: if not ???:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # STEP 2: Try to load the CSV file
    # We use a try/except block to handle errors gracefully
    # This is like having a backup plan if something goes wrong

    try:
        # HINT: Use pd.read_csv() with the provided parameters
        # Basic format: pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
        # FILL IN: df = ???

        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

        # STEP 3: Basic validation - check if we got any data
        if df.empty:
            raise ValueError(f"File {file_path} was loaded but contains no data")

        # STEP 4: Clean up common issues in environmental data

        # Remove any completely empty rows
        # HINT: Use df.dropna(how='all') to remove rows where ALL values are missing
        # FILL IN: df = ???

        df = df.dropna(how='all')

        # Remove any completely empty columns
        # HINT: Use df.dropna(how='all', axis=1) to remove columns where ALL values are missing
        # FILL IN: df = ???

        df = df.dropna(how='all', axis=1)

        # Strip whitespace from string columns (common issue with CSV files)
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                # HINT: Use df[col].str.strip() to remove extra spaces
                # FILL IN: df[col] = ???
                df[col] = df[col].str.strip()

        # STEP 5: Return the cleaned DataFrame
        return df

    except UnicodeDecodeError:
        # Handle encoding problems (very common with CSV files!)
        raise ValueError(f"Could not read file {file_path} with encoding '{encoding}'. "
                        "Try encoding='latin-1' or encoding='cp1252'")

    except pd.errors.EmptyDataError:
        # Handle completely empty files
        raise ValueError(f"File {file_path} is empty or contains no readable data")

    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Error reading file {file_path}: {str(e)}")

    # Your function now:
    # ✅ Checks that files exist before trying to load them
    # ✅ Handles common encoding problems
    # ✅ Cleans up empty rows and columns
    # ✅ Removes extra whitespace from text
    # ✅ Provides helpful error messages


def save_processed_data(df: pd.DataFrame,
                       output_path: str,
                       file_format: str = 'csv',
                       include_index: bool = False) -> Dict[str, Any]:
    """
    SAVE YOUR PROCESSED DATA TO FILES (Like saving your work)

    After you've cleaned and analyzed your data, you want to save it for later use.
    This function saves your DataFrame to different file formats with proper error handling.

    Think of it like "Save As" in Microsoft Word, but for data:
    - Save as CSV (most common, works everywhere)
    - Save as Excel (good for sharing with non-programmers)
    - Save as JSON (good for web applications)

    Your Task: Write code to save DataFrames in different formats safely.

    Args:
        df: The DataFrame to save
        output_path: Where to save it (like "results/cleaned_data.csv")
        file_format: What format to save as ('csv', 'excel', 'json')
        include_index: Whether to save row numbers (usually False)

    Returns:
        Dictionary with save operation details and statistics
    """

    # STEP 1: Create the output directory if it doesn't exist
    # If you're saving to "results/data.csv", make sure the "results" folder exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        # HINT: Use os.makedirs() to create directories
        # FILL IN: ???
        os.makedirs(output_dir, exist_ok=True)

    # STEP 2: Check that we have data to save
    if df.empty:
        raise ValueError("Cannot save empty DataFrame")

    # STEP 3: Record start time (to measure how long saving takes)
    start_time = time.time()

    # STEP 4: Save based on the requested format
    try:
        if file_format.lower() == 'csv':
            # Save as CSV file
            # HINT: Use df.to_csv(output_path, index=include_index)
            # FILL IN: ???
            df.to_csv(output_path, index=include_index, encoding='utf-8')

        elif file_format.lower() == 'excel':
            # Save as Excel file (.xlsx)
            # Make sure the path ends with .xlsx
            if not output_path.endswith('.xlsx'):
                output_path += '.xlsx'
            # HINT: Use df.to_excel(output_path, index=include_index)
            # FILL IN: ???
            df.to_excel(output_path, index=include_index, engine='openpyxl')

        elif file_format.lower() == 'json':
            # Save as JSON file
            # Make sure the path ends with .json
            if not output_path.endswith('.json'):
                output_path += '.json'
            # HINT: Use df.to_json(output_path, orient='records', indent=2)
            # 'orient=records' makes each row a separate JSON object
            # 'indent=2' makes it readable
            # FILL IN: ???
            df.to_json(output_path, orient='records', indent=2)

        else:
            raise ValueError(f"Unsupported file format: {file_format}. Use 'csv', 'excel', or 'json'")

    except Exception as e:
        raise RuntimeError(f"Error saving file {output_path}: {str(e)}")

    # STEP 5: Calculate how long the save operation took
    save_time = time.time() - start_time

    # STEP 6: Get information about the saved file
    file_size = os.path.getsize(output_path)  # Size in bytes

    # STEP 7: Create a report about what we saved
    save_report = {
        'output_path': output_path,
        'file_format': file_format,
        'rows_saved': len(df),
        'columns_saved': len(df.columns),
        'file_size_bytes': file_size,
        'file_size_mb': round(file_size / (1024 * 1024), 2),
        'save_time_seconds': round(save_time, 3),
        'include_index': include_index
    }

    return save_report

    # Your function now:
    # ✅ Creates output directories automatically
    # ✅ Saves to multiple file formats
    # ✅ Handles errors gracefully
    # ✅ Reports detailed statistics about the save operation
    # ✅ Times the save operation for performance monitoring


def validate_data_integrity(original_file: str,
                           processed_df: pd.DataFrame,
                           tolerance: float = 0.1) -> Dict[str, Any]:
    """
    CHECK THAT YOUR DATA PROCESSING DIDN'T BREAK ANYTHING (Quality control)

    After loading and processing data, it's important to check that everything still
    makes sense. This function compares your processed data against the original file
    to catch any problems.

    Think of it like proofreading an important document:
    - Did you accidentally delete important information?
    - Are the numbers still reasonable?
    - Did you introduce any errors during processing?

    Your Task: Compare processed data against the original and report any issues.

    Args:
        original_file: Path to the original CSV file
        processed_df: The DataFrame after your processing
        tolerance: How much difference is acceptable (0.1 = 10%)

    Returns:
        Dictionary with validation results and any warnings
    """

    validation_report = {
        'is_valid': True,
        'warnings': [],
        'original_rows': 0,
        'processed_rows': len(processed_df),
        'original_columns': 0,
        'processed_columns': len(processed_df.columns),
        'data_type_changes': {},
        'missing_data_changes': {},
        'numeric_range_changes': {}
    }

    # STEP 1: Load the original file for comparison
    try:
        # HINT: Use the load_environmental_data function you already wrote!
        # FILL IN: original_df = ???
        original_df = load_environmental_data(original_file)

    except Exception as e:
        validation_report['is_valid'] = False
        validation_report['warnings'].append(f"Could not load original file for comparison: {str(e)}")
        return validation_report

    # STEP 2: Compare basic dimensions
    validation_report['original_rows'] = len(original_df)
    validation_report['original_columns'] = len(original_df.columns)

    # Check for major row loss (might indicate a problem)
    row_loss_percentage = (len(original_df) - len(processed_df)) / len(original_df) * 100
    if row_loss_percentage > tolerance * 100:
        validation_report['warnings'].append(
            f"Lost {row_loss_percentage:.1f}% of rows during processing (>{tolerance*100:.1f}% threshold)"
        )

    # STEP 3: Check for data type changes
    # Compare data types between original and processed data
    common_columns = set(original_df.columns) & set(processed_df.columns)

    for col in common_columns:
        original_type = str(original_df[col].dtype)
        processed_type = str(processed_df[col].dtype)

        if original_type != processed_type:
            validation_report['data_type_changes'][col] = {
                'original': original_type,
                'processed': processed_type
            }

    # STEP 4: Check for missing data changes
    # Compare how much missing data we have before and after
    for col in common_columns:
        original_missing = original_df[col].isna().sum()
        processed_missing = processed_df[col].isna().sum()

        if original_missing != processed_missing:
            validation_report['missing_data_changes'][col] = {
                'original_missing': int(original_missing),
                'processed_missing': int(processed_missing),
                'change': int(processed_missing - original_missing)
            }

    # STEP 5: Check numeric ranges (for numeric columns)
    # Make sure we didn't accidentally change the data values dramatically
    for col in common_columns:
        if pd.api.types.is_numeric_dtype(original_df[col]) and pd.api.types.is_numeric_dtype(processed_df[col]):

            # Calculate basic statistics
            orig_min = original_df[col].min()
            orig_max = original_df[col].max()
            orig_mean = original_df[col].mean()

            proc_min = processed_df[col].min()
            proc_max = processed_df[col].max()
            proc_mean = processed_df[col].mean()

            # Check if the ranges changed dramatically
            if pd.notna(orig_min) and pd.notna(proc_min):
                min_change = abs(orig_min - proc_min) / abs(orig_min) if orig_min != 0 else 0
                max_change = abs(orig_max - proc_max) / abs(orig_max) if orig_max != 0 else 0
                mean_change = abs(orig_mean - proc_mean) / abs(orig_mean) if orig_mean != 0 else 0

                if any(change > tolerance for change in [min_change, max_change, mean_change]):
                    validation_report['numeric_range_changes'][col] = {
                        'original_range': [float(orig_min), float(orig_max)],
                        'processed_range': [float(proc_min), float(proc_max)],
                        'original_mean': float(orig_mean),
                        'processed_mean': float(proc_mean)
                    }

    # STEP 6: Generate overall assessment
    if validation_report['data_type_changes']:
        validation_report['warnings'].append(
            f"Data types changed for {len(validation_report['data_type_changes'])} columns"
        )

    if validation_report['numeric_range_changes']:
        validation_report['warnings'].append(
            f"Numeric ranges changed significantly for {len(validation_report['numeric_range_changes'])} columns"
        )

    # STEP 7: Final validation decision
    if not validation_report['warnings']:
        validation_report['warnings'].append("Data validation passed! No significant issues detected.")
    else:
        validation_report['is_valid'] = len(validation_report['warnings']) <= 2  # Allow minor warnings

    return validation_report

    # Your function now:
    # ✅ Compares processed data against the original
    # ✅ Checks for unexpected data loss
    # ✅ Monitors data type changes
    # ✅ Tracks missing data changes
    # ✅ Validates that numeric ranges make sense
    # ✅ Provides detailed warnings and recommendations


def batch_process_files(input_directory: str,
                       output_directory: str,
                       processing_function: callable,
                       file_pattern: str = '*.csv') -> Dict[str, Any]:
    """
    PROCESS MULTIPLE FILES AT ONCE (Like batch cooking)

    Sometimes you have many data files that all need the same processing.
    Instead of processing them one by one, this function handles them all automatically.

    Think of it like batch cooking:
    - You have 10 different CSV files with environmental data
    - You want to clean and process all of them the same way
    - This function does it automatically and gives you a summary

    Your Task: Process multiple files and create a summary report.

    Args:
        input_directory: Folder containing input files
        output_directory: Folder to save processed files
        processing_function: Function to apply to each DataFrame
        file_pattern: Pattern to match files (like '*.csv' for all CSV files)

    Returns:
        Dictionary with processing results and statistics
    """

    # STEP 1: Check that input directory exists
    if not os.path.exists(input_directory):
        raise FileNotFoundError(f"Input directory not found: {input_directory}")

    # STEP 2: Create output directory if needed
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    # STEP 3: Find all files matching our pattern
    # HINT: Use Path(input_directory).glob(file_pattern) to find matching files
    # FILL IN: input_files = list(???)
    input_files = list(Path(input_directory).glob(file_pattern))

    # STEP 4: Initialize tracking variables
    processing_report = {
        'input_directory': input_directory,
        'output_directory': output_directory,
        'file_pattern': file_pattern,
        'total_files_found': len(input_files),
        'files_processed_successfully': 0,
        'files_failed': 0,
        'processing_errors': [],
        'file_details': [],
        'total_processing_time': 0
    }

    if len(input_files) == 0:
        processing_report['processing_errors'].append("No files found matching the pattern")
        return processing_report

    # STEP 5: Process each file
    start_time = time.time()

    for input_file in input_files:
        file_start_time = time.time()

        try:
            # STEP 5A: Load the file
            # HINT: Use your load_environmental_data function
            # FILL IN: df = ???
            df = load_environmental_data(str(input_file))

            # STEP 5B: Apply the processing function
            # The processing_function is passed in by the user
            processed_df = processing_function(df)

            # STEP 5C: Generate output filename
            output_filename = f"processed_{input_file.name}"
            output_path = os.path.join(output_directory, output_filename)

            # STEP 5D: Save the processed data
            # HINT: Use your save_processed_data function
            # FILL IN: save_result = ???
            save_result = save_processed_data(processed_df, output_path, 'csv')

            # STEP 5E: Record success
            file_processing_time = time.time() - file_start_time

            file_details = {
                'input_file': str(input_file),
                'output_file': output_path,
                'original_rows': len(df),
                'processed_rows': save_result['rows_saved'],
                'processing_time': round(file_processing_time, 3),
                'status': 'success'
            }

            processing_report['file_details'].append(file_details)
            processing_report['files_processed_successfully'] += 1

        except Exception as e:
            # STEP 5F: Record failure
            file_processing_time = time.time() - file_start_time

            error_details = {
                'input_file': str(input_file),
                'error': str(e),
                'processing_time': round(file_processing_time, 3),
                'status': 'failed'
            }

            processing_report['file_details'].append(error_details)
            processing_report['files_failed'] += 1
            processing_report['processing_errors'].append(f"{input_file.name}: {str(e)}")

    # STEP 6: Calculate final statistics
    processing_report['total_processing_time'] = round(time.time() - start_time, 3)

    return processing_report

    # Your function now:
    # ✅ Processes multiple files automatically
    # ✅ Creates output directories as needed
    # ✅ Handles errors gracefully (continues with other files)
    # ✅ Provides detailed statistics and timing information
    # ✅ Records both successes and failures for review


# ==============================================================================
# HELPER SECTION - Bonus functions for extra practice!
# ==============================================================================

def _detect_file_encoding(file_path: str) -> str:
    """
    BONUS HELPER: Try to guess the encoding of a text file
    (You can implement this for extra practice, or skip it!)
    """
    # Common encodings to try
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1000)  # Try to read first 1000 characters
            return encoding
        except UnicodeDecodeError:
            continue

    return 'utf-8'  # Default fallback


def _get_file_info(file_path: str) -> Dict[str, Any]:
    """
    BONUS HELPER: Get detailed information about a file
    (You can implement this for extra practice, or skip it!)
    """
    if not os.path.exists(file_path):
        return {'exists': False}

    stat = os.stat(file_path)

    return {
        'exists': True,
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'created_time': time.ctime(stat.st_ctime),
        'modified_time': time.ctime(stat.st_mtime),
        'is_readable': os.access(file_path, os.R_OK),
        'is_writable': os.access(file_path, os.W_OK)
    }


def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    BONUS HELPER: Clean up messy column names
    (You can implement this for extra practice, or skip it!)
    """
    df = df.copy()

    # Clean column names
    new_columns = []
    for col in df.columns:
        # Convert to lowercase
        clean_col = str(col).lower()
        # Replace spaces and special characters with underscores
        clean_col = ''.join(c if c.isalnum() else '_' for c in clean_col)
        # Remove multiple underscores
        clean_col = '_'.join(filter(None, clean_col.split('_')))
        new_columns.append(clean_col)

    df.columns = new_columns
    return df


# ==============================================================================
# EXAMPLES - Try these to understand file operations!
# ==============================================================================

"""
EXAMPLE 1: Basic file loading

# Load a CSV file
df = load_environmental_data('data/weather_stations.csv')
print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
print(df.head())  # Show first 5 rows

EXAMPLE 2: Saving in different formats

# Save as CSV
save_result = save_processed_data(df, 'output/results.csv', 'csv')
print(f"Saved {save_result['rows_saved']} rows to {save_result['output_path']}")

# Save as Excel
save_result = save_processed_data(df, 'output/results.xlsx', 'excel')

# Save as JSON
save_result = save_processed_data(df, 'output/results.json', 'json')

EXAMPLE 3: Data validation

# Check if processing changed your data unexpectedly
validation = validate_data_integrity('data/original.csv', processed_df)
if validation['is_valid']:
    print("✅ Data validation passed!")
else:
    print("⚠️  Data validation warnings:")
    for warning in validation['warnings']:
        print(f"  - {warning}")

EXAMPLE 4: Batch processing

# Process all CSV files in a directory
def my_cleaning_function(df):
    # Remove empty rows
    df = df.dropna(how='all')
    # Convert text to lowercase
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.lower()
    return df

results = batch_process_files(
    input_directory='raw_data/',
    output_directory='cleaned_data/',
    processing_function=my_cleaning_function,
    file_pattern='*.csv'
)

print(f"Processed {results['files_processed_successfully']} files successfully")
print(f"Failed to process {results['files_failed']} files")
"""

# ==============================================================================
# COMMON MISTAKES - Watch out for these!
# ==============================================================================

"""
❌ MISTAKE 1: Not checking if files exist
# Wrong:
df = pd.read_csv('nonexistent_file.csv')  # This will crash!

# Right:
if os.path.exists('file.csv'):
    df = pd.read_csv('file.csv')
else:
    print("File not found!")

❌ MISTAKE 2: Ignoring encoding issues
# Problem: File has special characters that don't load correctly
# Solution: Try different encodings or detect automatically

❌ MISTAKE 3: Not handling empty files
# Wrong:
df = pd.read_csv('empty_file.csv')
result = df.mean()  # Crashes on empty data!

# Right:
df = pd.read_csv('empty_file.csv')
if not df.empty:
    result = df.mean()

❌ MISTAKE 4: Overwriting important files
# Problem: Accidentally saving over your original data
# Solution: Always save processed data to different filenames/directories

❌ MISTAKE 5: Not creating output directories
# Wrong:
df.to_csv('results/subfolder/data.csv')  # Crashes if directories don't exist!

# Right:
os.makedirs('results/subfolder', exist_ok=True)
df.to_csv('results/subfolder/data.csv')

❌ MISTAKE 6: Not handling large files efficiently
# Problem: Loading huge files can crash your computer
# Solution: Consider chunking for very large files:
# chunk_list = []
# for chunk in pd.read_csv('huge_file.csv', chunksize=1000):
#     processed_chunk = process_data(chunk)
#     chunk_list.append(processed_chunk)
# result = pd.concat(chunk_list, ignore_index=True)
"""

# ==============================================================================
# FILE FORMAT REFERENCE
# ==============================================================================

"""
📁 COMMON FILE FORMATS FOR ENVIRONMENTAL DATA:

CSV (Comma-Separated Values):
✅ Pros: Universal compatibility, small size, easy to edit
❌ Cons: No data types, no multiple sheets
📝 Use for: Most environmental sensor data, simple tabular data

Excel (.xlsx):
✅ Pros: Preserves formatting, multiple sheets, familiar to non-programmers
❌ Cons: Larger file size, can have compatibility issues
📝 Use for: Sharing with stakeholders, complex datasets with metadata

JSON (JavaScript Object Notation):
✅ Pros: Structured data, preserves hierarchies, web-friendly
❌ Cons: Less efficient for tabular data, harder to read
📝 Use for: API data, nested/hierarchical environmental data

Parquet:
✅ Pros: Very fast, compressed, preserves data types
❌ Cons: Requires special software to view
📝 Use for: Large datasets, data warehousing, performance-critical applications

📊 ENCODING REFERENCE:
- UTF-8: Modern standard, handles all international characters
- Latin-1 (ISO-8859-1): Older European standard
- CP1252: Windows standard, similar to Latin-1
- ASCII: Basic English only, very limited

💡 PRO TIP: When in doubt, try UTF-8 first, then Latin-1 if that fails.
"""

"""
CONGRATULATIONS! 🎉

You've mastered the fundamentals of file operations in pandas:
✅ Loading data from various file formats safely
✅ Handling common file problems (encoding, missing files, etc.)
✅ Saving data in multiple formats
✅ Validating data integrity after processing
✅ Batch processing multiple files efficiently
✅ Understanding different file formats and their trade-offs

These skills are essential for:
- Loading environmental sensor data from various sources
- Cleaning and preprocessing raw data files
- Saving analysis results for sharing and archival
- Building robust data processing pipelines
- Working with legacy data in different formats

Real-world applications:
🌍 Environmental monitoring: Loading data from weather stations, air quality sensors
📊 GIS workflows: Processing spatial data from various government agencies
🔬 Scientific research: Handling data from different instruments and databases
📈 Data analysis: Creating reproducible workflows for data processing

Pro tips for success:
- Always validate your data after loading
- Use consistent naming conventions for your files
- Keep backups of original data (never overwrite source files)
- Document your file processing steps for reproducibility
- Test with small files first before processing large datasets
- Handle errors gracefully - files will have problems!

Keep practicing and you'll become a file operations expert! 🚀
"""
