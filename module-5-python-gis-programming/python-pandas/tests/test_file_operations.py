"""
Test File Operations Module - Comprehensive Test Suite
=====================================================

This file tests all the file I/O operations for pandas data analysis.

Test Categories:
- CSV loading with various formats and encodings
- Data saving with metadata preservation
- Data integrity validation and error detection
- Batch file processing operations
- Error handling and edge cases
- Performance benchmarks

Important: These tests verify that your file operations are robust,
handle errors gracefully, and work with real-world messy data.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
import csv
from io import StringIO

# Import the functions we're testing
from src.pandas_analysis.file_operations import (
    load_environmental_data,
    save_processed_data,
    validate_data_integrity,
    batch_process_files,
    _detect_file_encoding,
    _get_file_info,
    _clean_column_names
)


class TestLoadEnvironmentalData:
    """Test the load_environmental_data function"""

    def test_load_basic_csv(self, tmp_path):
        """Test loading a basic CSV file"""
        # Create test CSV file
        test_data = """station_id,temperature,humidity,date
        STATION_001,25.5,68.2,2023-01-15
        STATION_002,22.1,71.8,2023-01-15
        STATION_003,28.9,65.4,2023-01-15"""

        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text(test_data)

        # Test loading
        result = load_environmental_data(str(csv_file))

        # Verify results
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['station_id', 'temperature', 'humidity', 'date']
        assert result['temperature'].dtype in ['float64', 'float32']

    def test_load_csv_with_missing_values(self, tmp_path):
        """Test loading CSV with missing values"""
        test_data = """station_id,temperature,humidity
        STATION_001,25.5,
        STATION_002,,71.8
        STATION_003,28.9,65.4"""

        csv_file = tmp_path / "missing_data.csv"
        csv_file.write_text(test_data)

        result = load_environmental_data(str(csv_file))

        assert result.isna().sum().sum() == 2  # Two missing values
        assert len(result) == 3

    def test_load_csv_with_different_encoding(self, tmp_path):
        """Test loading CSV with different encoding"""
        # Create CSV with special characters
        test_data = "name,location\nStación Météo,Montréal\n"

        csv_file = tmp_path / "encoded_data.csv"
        csv_file.write_text(test_data, encoding='utf-8')

        result = load_environmental_data(str(csv_file))

        assert len(result) == 1
        assert 'Stación' in result['name'].iloc[0]

    def test_load_nonexistent_file(self):
        """Test error handling for non-existent file"""
        with pytest.raises((FileNotFoundError, IOError)):
            load_environmental_data("nonexistent_file.csv")

    def test_load_empty_file(self, tmp_path):
        """Test loading an empty CSV file"""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        result = load_environmental_data(str(csv_file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_load_malformed_csv(self, tmp_path):
        """Test handling of malformed CSV data"""
        test_data = """station_id,temperature,humidity
        STATION_001,25.5,68.2
        STATION_002,invalid_number,71.8
        STATION_003,28.9,"""

        csv_file = tmp_path / "malformed.csv"
        csv_file.write_text(test_data)

        # Should not raise error but handle gracefully
        result = load_environmental_data(str(csv_file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3


class TestSaveProcessedData:
    """Test the save_processed_data function"""

    def test_save_basic_dataframe(self, tmp_path):
        """Test saving a basic DataFrame to CSV"""
        # Create test DataFrame
        df = pd.DataFrame({
            'station': ['A', 'B', 'C'],
            'temp': [20.1, 22.5, 19.8],
            'humidity': [65, 70, 62]
        })

        output_file = tmp_path / "output.csv"
        metadata = {'processed_by': 'test_suite', 'date': '2023-01-15'}

        # Test saving
        save_processed_data(df, str(output_file), metadata)

        # Verify file was created
        assert output_file.exists()

        # Verify content can be read back
        loaded_df = pd.read_csv(output_file)
        assert len(loaded_df) == 3
        assert list(loaded_df.columns) == ['station', 'temp', 'humidity']

    def test_save_with_index(self, tmp_path):
        """Test saving DataFrame with custom index"""
        df = pd.DataFrame({
            'value': [1, 2, 3]
        }, index=['A', 'B', 'C'])

        output_file = tmp_path / "indexed_output.csv"

        save_processed_data(df, str(output_file), include_index=True)

        # Verify index was saved
        loaded_df = pd.read_csv(output_file, index_col=0)
        assert list(loaded_df.index) == ['A', 'B', 'C']

    def test_save_empty_dataframe(self, tmp_path):
        """Test saving an empty DataFrame"""
        df = pd.DataFrame()
        output_file = tmp_path / "empty_output.csv"

        save_processed_data(df, str(output_file))

        assert output_file.exists()

    def test_save_to_invalid_path(self):
        """Test error handling for invalid file path"""
        df = pd.DataFrame({'a': [1, 2, 3]})

        with pytest.raises((OSError, IOError, PermissionError)):
            save_processed_data(df, "/invalid/path/file.csv")

    def test_save_with_special_characters(self, tmp_path):
        """Test saving data with special characters"""
        df = pd.DataFrame({
            'location': ['Montréal', 'México', 'São Paulo'],
            'temp': [20.1, 22.5, 19.8]
        })

        output_file = tmp_path / "special_chars.csv"
        save_processed_data(df, str(output_file))

        # Verify special characters are preserved
        loaded_df = pd.read_csv(output_file)
        assert 'Montréal' in loaded_df['location'].values


class TestValidateDataIntegrity:
    """Test the validate_data_integrity function"""

    def test_validate_clean_data(self):
        """Test validation of clean, complete data"""
        df = pd.DataFrame({
            'station_id': ['A001', 'B002', 'C003'],
            'temperature': [20.1, 22.5, 19.8],
            'humidity': [65, 70, 62],
            'date': pd.date_range('2023-01-01', periods=3)
        })

        report = validate_data_integrity(df)

        assert isinstance(report, dict)
        assert 'missing_values' in report
        assert 'data_types' in report
        assert 'duplicate_rows' in report
        assert report['missing_values']['total_missing'] == 0

    def test_validate_data_with_missing_values(self):
        """Test validation of data with missing values"""
        df = pd.DataFrame({
            'station_id': ['A001', 'B002', None],
            'temperature': [20.1, None, 19.8],
            'humidity': [65, 70, 62]
        })

        report = validate_data_integrity(df)

        assert report['missing_values']['total_missing'] == 2
        assert 'station_id' in report['missing_values']['by_column']
        assert 'temperature' in report['missing_values']['by_column']

    def test_validate_data_with_duplicates(self):
        """Test validation of data with duplicate rows"""
        df = pd.DataFrame({
            'station_id': ['A001', 'B002', 'A001'],
            'temperature': [20.1, 22.5, 20.1],
            'humidity': [65, 70, 65]
        })

        report = validate_data_integrity(df)

        assert report['duplicate_rows']['count'] > 0

    def test_validate_data_types(self):
        """Test validation of data types"""
        df = pd.DataFrame({
            'station_id': ['A001', 'B002', 'C003'],
            'temperature': [20.1, 22.5, 19.8],
            'count': [1, 2, 3],
            'active': [True, False, True]
        })

        report = validate_data_integrity(df)

        data_types = report['data_types']
        assert len(data_types) == 4
        assert data_types['temperature'] in ['float64', 'float32']
        assert data_types['count'] in ['int64', 'int32', 'int16', 'int8']

    def test_validate_empty_dataframe(self):
        """Test validation of empty DataFrame"""
        df = pd.DataFrame()

        report = validate_data_integrity(df)

        assert report['missing_values']['total_missing'] == 0
        assert report['duplicate_rows']['count'] == 0

    def test_validate_single_column_data(self):
        """Test validation of single-column DataFrame"""
        df = pd.DataFrame({'values': [1, 2, 3, None, 5]})

        report = validate_data_integrity(df)

        assert report['missing_values']['total_missing'] == 1
        assert 'values' in report['missing_values']['by_column']


class TestBatchProcessFiles:
    """Test the batch_process_files function"""

    def test_batch_process_multiple_files(self, tmp_path):
        """Test processing multiple CSV files in batch"""
        # Create multiple test files
        for i in range(3):
            test_data = f"""station_id,temperature
            STATION_00{i+1},{20 + i}.5"""

            csv_file = tmp_path / f"data_{i+1}.csv"
            csv_file.write_text(test_data)

        file_pattern = str(tmp_path / "data_*.csv")

        results = batch_process_files(file_pattern)

        assert isinstance(results, dict)
        assert len(results) == 3
        for filename, df in results.items():
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1

    def test_batch_process_no_matching_files(self, tmp_path):
        """Test batch processing with no matching files"""
        file_pattern = str(tmp_path / "nonexistent_*.csv")

        results = batch_process_files(file_pattern)

        assert isinstance(results, dict)
        assert len(results) == 0

    def test_batch_process_mixed_file_quality(self, tmp_path):
        """Test batch processing with mix of good and bad files"""
        # Good file
        good_data = """station_id,temperature
        STATION_001,25.5"""
        good_file = tmp_path / "good_data.csv"
        good_file.write_text(good_data)

        # Bad file (empty)
        bad_file = tmp_path / "bad_data.csv"
        bad_file.write_text("")

        # Corrupted file
        corrupt_file = tmp_path / "corrupt_data.csv"
        corrupt_file.write_text("invalid,csv,content\n1,2")

        file_pattern = str(tmp_path / "*.csv")

        results = batch_process_files(file_pattern)

        # Should handle errors gracefully
        assert isinstance(results, dict)

    def test_batch_process_large_number_of_files(self, tmp_path):
        """Test batch processing performance with many files"""
        # Create 10 small files
        for i in range(10):
            test_data = f"""id,value
            {i},{i*10}"""
            csv_file = tmp_path / f"file_{i:02d}.csv"
            csv_file.write_text(test_data)

        file_pattern = str(tmp_path / "file_*.csv")

        results = batch_process_files(file_pattern)

        assert len(results) == 10
        for df in results.values():
            assert len(df) == 1


class TestHelperFunctions:
    """Test the private helper functions"""

    def test_detect_file_encoding(self, tmp_path):
        """Test encoding detection"""
        # Create file with UTF-8 encoding
        test_data = "name,city\nJosé,São Paulo"
        test_file = tmp_path / "utf8_file.csv"
        test_file.write_text(test_data, encoding='utf-8')

        encoding = _detect_file_encoding(str(test_file))

        assert isinstance(encoding, str)
        assert encoding.lower() in ['utf-8', 'utf-8-sig', 'ascii']

    def test_get_file_info(self, tmp_path):
        """Test file information extraction"""
        test_data = "a,b,c\n1,2,3\n4,5,6"
        test_file = tmp_path / "info_test.csv"
        test_file.write_text(test_data)

        info = _get_file_info(str(test_file))

        assert isinstance(info, dict)
        assert 'size_bytes' in info
        assert 'modified_date' in info
        assert info['size_bytes'] > 0

    def test_clean_column_names(self):
        """Test column name cleaning"""
        messy_columns = [' Station ID ', 'Temperature (°C)', 'Humidity%', 'Date-Time']

        clean_columns = _clean_column_names(messy_columns)

        assert isinstance(clean_columns, list)
        assert len(clean_columns) == len(messy_columns)
        # Should remove spaces and special characters
        for col in clean_columns:
            assert not col.startswith(' ')
            assert not col.endswith(' ')

    def test_clean_column_names_edge_cases(self):
        """Test column cleaning with edge cases"""
        edge_cases = ['', '   ', 'NORMAL', '123', 'special@#$chars']

        result = _clean_column_names(edge_cases)

        assert len(result) == len(edge_cases)
        assert all(isinstance(col, str) for col in result)

    def test_detect_encoding_nonexistent_file(self):
        """Test encoding detection for non-existent file"""
        result = _detect_file_encoding("nonexistent_file.csv")

        # Should return default encoding or handle gracefully
        assert result is None or isinstance(result, str)


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_complete_workflow(self, tmp_path):
        """Test a complete load-process-save workflow"""
        # Create input data
        input_data = """station_id,temperature,humidity,date
        STATION_001,25.5,68.2,2023-01-15
        STATION_002,22.1,71.8,2023-01-15"""

        input_file = tmp_path / "input.csv"
        input_file.write_text(input_data)

        # Load data
        df = load_environmental_data(str(input_file))
        assert len(df) == 2

        # Validate data
        report = validate_data_integrity(df)
        assert report['missing_values']['total_missing'] == 0

        # Save processed data
        output_file = tmp_path / "output.csv"
        save_processed_data(df, str(output_file))

        # Verify output
        assert output_file.exists()
        final_df = pd.read_csv(output_file)
        assert len(final_df) == 2

    def test_error_recovery_workflow(self, tmp_path):
        """Test workflow with various error conditions"""
        # Create problematic data
        problematic_data = """station_id,temperature,humidity
        STATION_001,25.5,68.2
        STATION_002,invalid,71.8
        STATION_003,,"""

        input_file = tmp_path / "problematic.csv"
        input_file.write_text(problematic_data)

        # Should load despite problems
        df = load_environmental_data(str(input_file))
        assert isinstance(df, pd.DataFrame)

        # Validation should identify issues
        report = validate_data_integrity(df)
        assert report['missing_values']['total_missing'] > 0

    def test_large_dataset_performance(self, tmp_path):
        """Test performance with larger datasets"""
        # Create larger dataset
        rows = []
        for i in range(1000):
            rows.append(f"STATION_{i:04d},{20 + (i % 20)},{60 + (i % 40)}")

        large_data = "station_id,temperature,humidity\n" + "\n".join(rows)
        large_file = tmp_path / "large_dataset.csv"
        large_file.write_text(large_data)

        # Test operations
        df = load_environmental_data(str(large_file))
        assert len(df) == 1000

        report = validate_data_integrity(df)
        assert isinstance(report, dict)

        output_file = tmp_path / "large_output.csv"
        save_processed_data(df, str(output_file))
        assert output_file.exists()


# Test fixtures for creating sample data
@pytest.fixture
def sample_environmental_data():
    """Fixture providing sample environmental data"""
    return pd.DataFrame({
        'station_id': ['STATION_001', 'STATION_002', 'STATION_003'],
        'temperature': [25.5, 22.1, 28.9],
        'humidity': [68.2, 71.8, 65.4],
        'pressure': [1013.2, 1015.8, 1011.9],
        'date': pd.date_range('2023-01-15', periods=3)
    })

@pytest.fixture
def messy_data():
    """Fixture providing messy data for testing validation"""
    return pd.DataFrame({
        'station_id': ['STATION_001', None, 'STATION_001'],
        'temperature': [25.5, 22.1, 25.5],
        'humidity': [68.2, None, 68.2],
        'notes': ['Good', 'Sensor error', 'Good']
    })

@pytest.fixture
def temp_csv_file(tmp_path, sample_environmental_data):
    """Fixture creating a temporary CSV file with sample data"""
    csv_file = tmp_path / "temp_data.csv"
    sample_environmental_data.to_csv(csv_file, index=False)
    return str(csv_file)


class TestPerformanceBenchmarks:
    """Performance benchmark tests"""

    def test_load_performance(self, tmp_path):
        """Benchmark loading performance"""
        # Create moderately large dataset
        rows = []
        for i in range(5000):
            rows.append(f"STATION_{i:04d},{20 + np.random.random():.2f},{60 + np.random.random()*40:.1f}")

        large_data = "station_id,temperature,humidity\n" + "\n".join(rows)
        large_file = tmp_path / "benchmark_data.csv"
        large_file.write_text(large_data)

        # Should load reasonably quickly (exact time depends on system)
        import time
        start_time = time.time()
        df = load_environmental_data(str(large_file))
        load_time = time.time() - start_time

        assert len(df) == 5000
        assert load_time < 5.0  # Should load 5000 rows in under 5 seconds

    def test_validation_performance(self, sample_environmental_data):
        """Benchmark validation performance"""
        # Create larger dataset for validation
        large_df = pd.concat([sample_environmental_data] * 1000, ignore_index=True)

        import time
        start_time = time.time()
        report = validate_data_integrity(large_df)
        validation_time = time.time() - start_time

        assert isinstance(report, dict)
        assert validation_time < 2.0  # Should validate 3000 rows in under 2 seconds

    def test_save_performance(self, tmp_path, sample_environmental_data):
        """Benchmark saving performance"""
        # Create larger dataset for saving
        large_df = pd.concat([sample_environmental_data] * 2000, ignore_index=True)
        output_file = tmp_path / "benchmark_output.csv"

        import time
        start_time = time.time()
        save_processed_data(large_df, str(output_file))
        save_time = time.time() - start_time

        assert output_file.exists()
        assert save_time < 3.0  # Should save 6000 rows in under 3 seconds


"""
CONGRATULATIONS! 🎉

If these tests pass, your file operations module can:
✅ Load CSV files with various formats and encodings
✅ Handle missing values and malformed data gracefully
✅ Save DataFrames with metadata preservation
✅ Validate data integrity comprehensively
✅ Process multiple files in batch operations
✅ Detect and handle various error conditions
✅ Perform operations efficiently on large datasets

These are professional-grade file handling skills that you'll use
throughout your career in data science and GIS programming!

Key takeaways:
- Always validate your data before processing
- Handle errors gracefully - don't let bad data crash your programs
- Test with realistic, messy data scenarios
- Consider performance with large datasets
- Use proper encoding for international data

Great job building robust file operations! 🚀
"""
