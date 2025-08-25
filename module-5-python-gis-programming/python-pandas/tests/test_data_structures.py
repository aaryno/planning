"""
Test module for data structures implementation
Comprehensive automated testing for pandas Series and DataFrame operations
"""

import pytest
import pandas as pd
import numpy as np
import sys
from typing import Dict, List, Any, Tuple
from unittest.mock import patch
import warnings

# Import the student's implementation
try:
    from src.pandas_analysis.data_structures import (
        create_gis_series,
        analyze_series_properties,
        create_gis_dataframe,
        optimize_dataframe_memory
    )
except ImportError:
    pytest.skip("Student implementation not found", allow_module_level=True)


class TestCreateGISSeries:
    """Test cases for create_gis_series function"""

    def test_basic_series_creation(self):
        """Test basic Series creation with integer data"""
        data = [100, 200, 300, 400]
        index = ['Station_A', 'Station_B', 'Station_C', 'Station_D']
        name = 'elevation_meters'

        result = create_gis_series(data, index, name)

        assert isinstance(result, pd.Series), "Function must return a pandas Series"
        assert result.name == name, f"Series name should be '{name}'"
        assert list(result.index) == index, "Index values don't match expected"
        assert list(result.values) == data, "Series values don't match input data"
        assert len(result) == len(data), "Series length incorrect"

    def test_mixed_numeric_types(self):
        """Test Series creation with mixed int and float data"""
        data = [10, 15.5, 20, 25.7, 30]
        index = ['P1', 'P2', 'P3', 'P4', 'P5']
        name = 'temperature_celsius'

        result = create_gis_series(data, index, name)

        assert isinstance(result, pd.Series), "Function must return a pandas Series"
        assert result.dtype == np.float64, "Mixed int/float data should result in float64 dtype"
        assert result.name == name, "Series name not set correctly"
        np.testing.assert_array_almost_equal(result.values, data, decimal=10)

    def test_empty_data(self):
        """Test Series creation with empty data"""
        data = []
        index = []
        name = 'empty_series'

        result = create_gis_series(data, index, name)

        assert isinstance(result, pd.Series), "Function must return a pandas Series"
        assert len(result) == 0, "Empty series should have length 0"
        assert result.name == name, "Series name should be set even for empty series"

    def test_large_dataset(self):
        """Test Series creation with large dataset"""
        size = 10000
        data = list(range(size))
        index = [f'location_{i}' for i in range(size)]
        name = 'large_dataset'

        result = create_gis_series(data, index, name)

        assert isinstance(result, pd.Series), "Function must return a pandas Series"
        assert len(result) == size, f"Series should have {size} elements"
        assert result.name == name, "Series name not preserved in large dataset"

    def test_negative_values(self):
        """Test Series creation with negative values"""
        data = [-10.5, -5.0, 0.0, 5.5, 10.0]
        index = ['Below1', 'Below2', 'Zero', 'Above1', 'Above2']
        name = 'elevation_change'

        result = create_gis_series(data, index, name)

        assert isinstance(result, pd.Series), "Function must return a pandas Series"
        np.testing.assert_array_almost_equal(result.values, data)
        assert all(result.index == index), "Index not preserved correctly"


class TestAnalyzeSeriesProperties:
    """Test cases for analyze_series_properties function"""

    def test_complete_property_analysis(self):
        """Test comprehensive Series property analysis"""
        data = [1.0, 2.5, np.nan, 4.0, 5.5]
        series = pd.Series(data, index=['a', 'b', 'c', 'd', 'e'], name='test_series')

        result = analyze_series_properties(series)

        required_keys = {'dtype', 'size', 'index_type', 'has_nulls', 'memory_usage'}
        assert isinstance(result, dict), "Function must return a dictionary"
        assert set(result.keys()) == required_keys, f"Missing keys: {required_keys - set(result.keys())}"

        # Check specific properties
        assert result['size'] == 5, "Size should be 5"
        assert result['has_nulls'] is True, "Should detect null values"
        assert isinstance(result['memory_usage'], int), "Memory usage must be an integer (bytes)"
        assert result['memory_usage'] > 0, "Memory usage should be positive"

    def test_no_null_values(self):
        """Test Series with no null values"""
        data = [10, 20, 30, 40, 50]
        series = pd.Series(data, name='no_nulls')

        result = analyze_series_properties(series)

        assert result['has_nulls'] is False, "Should not detect null values when none exist"
        assert result['size'] == 5, "Size should be 5"

    def test_different_dtypes(self):
        """Test Series with different data types"""
        # Integer series
        int_series = pd.Series([1, 2, 3, 4, 5], dtype='int64')
        int_result = analyze_series_properties(int_series)
        assert 'int' in str(int_result['dtype']), "Should detect integer dtype"

        # String series
        str_series = pd.Series(['a', 'b', 'c', 'd'], dtype='object')
        str_result = analyze_series_properties(str_series)
        assert str_result['dtype'] == 'object', "Should detect object dtype for strings"

        # Boolean series
        bool_series = pd.Series([True, False, True], dtype='bool')
        bool_result = analyze_series_properties(bool_series)
        assert bool_result['dtype'] == 'bool', "Should detect boolean dtype"

    def test_empty_series(self):
        """Test analysis of empty Series"""
        empty_series = pd.Series([], dtype='float64')

        result = analyze_series_properties(empty_series)

        assert result['size'] == 0, "Empty series should have size 0"
        assert result['has_nulls'] is False, "Empty series should not have nulls"
        assert isinstance(result['memory_usage'], int), "Memory usage should still be an integer"


class TestCreateGISDataFrame:
    """Test cases for create_gis_dataframe function"""

    def test_basic_dataframe_creation(self):
        """Test basic DataFrame creation with type optimization"""
        data_dict = {
            'station_id': [1, 2, 3, 4, 5],
            'station_name': ['Site_A', 'Site_B', 'Site_A', 'Site_C', 'Site_B'],
            'elevation': [100.5, 150.0, 200.7, 175.2, 190.0],
            'active': [True, True, False, True, False],
            'install_date': ['2020-01-15', '2020-03-20', '2019-12-10', '2021-05-30', '2020-11-15']
        }

        result = create_gis_dataframe(data_dict)

        assert isinstance(result, pd.DataFrame), "Function must return a pandas DataFrame"
        assert len(result) == 5, "DataFrame should have 5 rows"
        assert len(result.columns) == 5, "DataFrame should have 5 columns"

        # Check that categorical optimization was applied
        assert result['station_name'].dtype.name == 'category', "Repeated strings should be converted to category"

        # Check date conversion
        assert pd.api.types.is_datetime64_any_dtype(result['install_date']), "Date strings should be converted to datetime"

        # Check boolean preservation
        assert result['active'].dtype == 'bool', "Boolean data should remain boolean"

    def test_categorical_optimization(self):
        """Test categorical data type optimization"""
        data_dict = {
            'region': ['North', 'South', 'North', 'East', 'South', 'North', 'East'] * 10,
            'status': ['Active', 'Inactive', 'Active', 'Maintenance'] * 17 + ['Active', 'Active', 'Active'],
            'values': list(range(70))
        }

        result = create_gis_dataframe(data_dict)

        assert result['region'].dtype.name == 'category', "Region should be categorical"
        assert result['status'].dtype.name == 'category', "Status should be categorical"
        assert pd.api.types.is_numeric_dtype(result['values']), "Numeric values should remain numeric"

    def test_mixed_date_formats(self):
        """Test handling of different date formats"""
        data_dict = {
            'id': [1, 2, 3, 4],
            'date1': ['2020-01-15', '2020-03-20', '2019-12-10', '2021-05-30'],
            'date2': ['01/15/2020', '03/20/2020', '12/10/2019', '05/30/2021'],
            'timestamp': ['2020-01-15 10:30:00', '2020-03-20 14:45:30', '2019-12-10 09:15:45', '2021-05-30 16:20:10']
        }

        result = create_gis_dataframe(data_dict)

        # At least one date column should be converted
        date_columns = [col for col in result.columns if pd.api.types.is_datetime64_any_dtype(result[col])]
        assert len(date_columns) >= 1, "At least one date column should be converted to datetime"

    def test_numeric_data_preservation(self):
        """Test that numeric data types are preserved appropriately"""
        data_dict = {
            'integers': [1, 2, 3, 4, 5],
            'floats': [1.1, 2.2, 3.3, 4.4, 5.5],
            'mixed_numeric': [1, 2.5, 3, 4.7, 5]
        }

        result = create_gis_dataframe(data_dict)

        assert pd.api.types.is_integer_dtype(result['integers']), "Integer column should remain integer"
        assert pd.api.types.is_float_dtype(result['floats']), "Float column should remain float"
        assert pd.api.types.is_float_dtype(result['mixed_numeric']), "Mixed numeric should be float"


class TestOptimizeDataFrameMemory:
    """Test cases for optimize_dataframe_memory function"""

    def test_memory_optimization_basic(self):
        """Test basic memory optimization functionality"""
        # Create a DataFrame with suboptimal data types
        np.random.seed(42)
        data = {
            'large_int': np.random.randint(0, 100, 1000).astype('int64'),  # Can be int8
            'category_text': ['Category_A', 'Category_B', 'Category_C'] * 334,  # Can be categorical
            'small_float': np.random.random(1000).astype('float64') * 10,  # Can be float32
            'boolean_int': np.random.choice([0, 1], 1000).astype('int64')  # Can be boolean
        }
        df = pd.DataFrame(data)
        original_memory = df.memory_usage(deep=True).sum()

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # Check return types
        assert isinstance(optimized_df, pd.DataFrame), "First return value must be DataFrame"
        assert isinstance(memory_info, dict), "Second return value must be dictionary"

        # Check memory reduction
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        memory_reduction = (original_memory - optimized_memory) / original_memory

        assert memory_reduction >= 0.2, f"Memory reduction should be at least 20%, got {memory_reduction:.2%}"

        # Check data integrity
        assert len(optimized_df) == len(df), "Row count should be preserved"
        assert len(optimized_df.columns) == len(df.columns), "Column count should be preserved"

        # Check that values are approximately equal (allowing for float precision differences)
        pd.testing.assert_frame_equal(df.select_dtypes(include=[np.number]),
                                    optimized_df.select_dtypes(include=[np.number]),
                                    check_dtype=False, check_exact=False, atol=1e-10)

    def test_categorical_conversion(self):
        """Test conversion of string columns to categorical"""
        data = {
            'high_cardinality': [f'Value_{i%50}' for i in range(1000)],  # Many repeated values
            'low_cardinality': ['A', 'B', 'C'] * 334,  # Few unique values
            'unique_strings': [f'Unique_{i}' for i in range(1000)]  # All unique
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # High and low cardinality should be categorical
        assert optimized_df['high_cardinality'].dtype.name == 'category', "High cardinality repeated strings should be categorical"
        assert optimized_df['low_cardinality'].dtype.name == 'category', "Low cardinality strings should be categorical"

        # Unique strings might or might not be categorical depending on implementation
        # but should still result in memory savings overall

    def test_integer_downcasting(self):
        """Test integer downcasting optimization"""
        data = {
            'small_ints': np.random.randint(0, 127, 1000).astype('int64'),  # Can be int8
            'medium_ints': np.random.randint(0, 32767, 1000).astype('int64'),  # Can be int16
            'large_ints': np.random.randint(0, 2147483647, 1000).astype('int64')  # Stay int64
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # Check that downcasting occurred where appropriate
        small_optimized_size = optimized_df['small_ints'].memory_usage(deep=True)
        small_original_size = df['small_ints'].memory_usage(deep=True)

        assert small_optimized_size < small_original_size, "Small integers should use less memory after optimization"

    def test_float_downcasting(self):
        """Test float precision optimization"""
        data = {
            'precise_floats': np.random.random(1000).astype('float64'),
            'simple_floats': [1.0, 2.0, 3.5, 4.2] * 250
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # At least some memory reduction should occur
        original_memory = df.memory_usage(deep=True).sum()
        optimized_memory = optimized_df.memory_usage(deep=True).sum()

        assert optimized_memory <= original_memory, "Optimized DataFrame should not use more memory"

    def test_memory_info_completeness(self):
        """Test that memory reduction info is complete"""
        data = {
            'col1': np.random.randint(0, 100, 100).astype('int64'),
            'col2': ['A', 'B', 'C'] * 34,
            'col3': np.random.random(100).astype('float64')
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # Check that memory_info contains expected information
        assert isinstance(memory_info, dict), "Memory info must be a dictionary"

        # Should contain overall reduction information
        expected_keys = {'original_memory_mb', 'optimized_memory_mb', 'total_reduction_percent'}
        assert all(key in memory_info for key in expected_keys), f"Missing keys in memory_info: {expected_keys - set(memory_info.keys())}"

        # Check that values are reasonable
        assert memory_info['original_memory_mb'] > 0, "Original memory should be positive"
        assert memory_info['optimized_memory_mb'] > 0, "Optimized memory should be positive"
        assert memory_info['total_reduction_percent'] >= 0, "Reduction percentage should be non-negative"

    def test_data_integrity_preservation(self):
        """Test that data values are preserved during optimization"""
        np.random.seed(123)
        data = {
            'integers': np.random.randint(0, 100, 50),
            'floats': np.random.random(50) * 100,
            'categories': np.random.choice(['A', 'B', 'C', 'D'], 50),
            'booleans': np.random.choice([True, False], 50)
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # Check that data values are preserved (allowing for small floating point differences)
        np.testing.assert_array_equal(df['integers'].values, optimized_df['integers'].values)
        np.testing.assert_array_almost_equal(df['floats'].values, optimized_df['floats'].values, decimal=5)

        # Categories and booleans should be exactly equal
        pd.testing.assert_series_equal(df['categories'].astype(str), optimized_df['categories'].astype(str), check_names=False)
        np.testing.assert_array_equal(df['booleans'].values, optimized_df['booleans'].values)


class TestPerformanceBenchmarks:
    """Performance benchmarks for data structure operations"""

    @pytest.mark.benchmark(group="series_creation")
    def test_series_creation_performance(self, benchmark):
        """Benchmark Series creation performance"""
        data = list(range(10000))
        index = [f'station_{i}' for i in range(10000)]
        name = 'benchmark_series'

        result = benchmark(create_gis_series, data, index, name)

        assert len(result) == 10000, "Benchmark series should have 10000 elements"
        assert result.name == name, "Benchmark series name should be preserved"

    @pytest.mark.benchmark(group="dataframe_optimization")
    def test_memory_optimization_performance(self, benchmark):
        """Benchmark memory optimization performance"""
        np.random.seed(42)
        data = {
            'large_ints': np.random.randint(0, 100, 5000).astype('int64'),
            'categories': np.random.choice(['Cat_A', 'Cat_B', 'Cat_C', 'Cat_D'], 5000),
            'floats': np.random.random(5000).astype('float64') * 1000,
            'booleans': np.random.choice([0, 1], 5000).astype('int64')
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = benchmark(optimize_dataframe_memory, df)

        assert len(optimized_df) == 5000, "Optimized DataFrame should preserve row count"
        assert memory_info['total_reduction_percent'] > 0, "Should achieve some memory reduction"


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_create_series_mismatched_lengths(self):
        """Test Series creation with mismatched data and index lengths"""
        data = [1, 2, 3]
        index = ['a', 'b']  # Different length
        name = 'mismatched'

        with pytest.raises((ValueError, IndexError)):
            create_gis_series(data, index, name)

    def test_analyze_properties_none_input(self):
        """Test analyze_series_properties with None input"""
        with pytest.raises((AttributeError, TypeError)):
            analyze_series_properties(None)

    def test_create_dataframe_empty_dict(self):
        """Test DataFrame creation with empty dictionary"""
        result = create_gis_dataframe({})

        assert isinstance(result, pd.DataFrame), "Should return DataFrame even for empty input"
        assert len(result) == 0, "Empty input should create empty DataFrame"
        assert len(result.columns) == 0, "Empty input should have no columns"

    def test_optimize_memory_already_optimal(self):
        """Test memory optimization on already optimal DataFrame"""
        data = {
            'small_ints': np.array([1, 2, 3, 4, 5], dtype='int8'),
            'categories': pd.Categorical(['A', 'B', 'A', 'B', 'A']),
            'small_floats': np.array([1.1, 2.2, 3.3], dtype='float32')
        }
        df = pd.DataFrame(data)

        optimized_df, memory_info = optimize_dataframe_memory(df)

        # Should still work, even if no optimization is possible
        assert isinstance(optimized_df, pd.DataFrame), "Should return DataFrame"
        assert isinstance(memory_info, dict), "Should return memory info"
        assert len(optimized_df) == len(df), "Should preserve data"


# Test fixtures for common data
@pytest.fixture
def sample_environmental_data():
    """Sample environmental monitoring data for testing"""
    np.random.seed(42)
    return {
        'station_id': range(100),
        'station_name': [f'Station_{i%10}' for i in range(100)],
        'air_quality_index': np.random.normal(75, 25, 100),
        'temperature': np.random.normal(20, 5, 100),
        'humidity': np.random.normal(50, 15, 100),
        'timestamp': pd.date_range('2023-01-01', periods=100, freq='1H'),
        'active': np.random.choice([True, False], 100, p=[0.8, 0.2])
    }

@pytest.fixture
def large_test_dataframe():
    """Large DataFrame for performance testing"""
    np.random.seed(123)
    size = 10000
    return pd.DataFrame({
        'id': range(size),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], size),
        'value1': np.random.random(size) * 1000,
        'value2': np.random.randint(0, 1000, size),
        'flag': np.random.choice([True, False], size),
        'date': pd.date_range('2020-01-01', periods=size, freq='1H')
    })
