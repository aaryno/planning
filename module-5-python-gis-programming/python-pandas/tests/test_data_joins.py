"""
Test module for data joins implementation
Comprehensive automated testing for pandas join and merge operations
"""

import pytest
import pandas as pd
import numpy as np
import time
import sys
from typing import Dict, List, Any, Tuple
from unittest.mock import patch
import warnings

# Import the student's implementation
try:
    from src.pandas_analysis.data_joins import (
        validate_join_keys,
        smart_join_gis_data,
        complex_multi_dataset_join
    )
except ImportError:
    pytest.skip("Student implementation not found", allow_module_level=True)


class TestValidateJoinKeys:
    """Test cases for validate_join_keys function"""

    def test_basic_key_validation(self):
        """Test basic join key validation functionality"""
        left_df = pd.DataFrame({
            'station_id': [1, 2, 3, 4],
            'temperature': [20, 25, 30, 22]
        })
        right_df = pd.DataFrame({
            'station_id': [1, 2, 5],
            'location': ['A', 'B', 'C']
        })

        result = validate_join_keys(left_df, right_df, 'station_id')

        assert isinstance(result, dict), "Function must return a dictionary"

        # Check required keys exist
        required_keys = {
            'key_exists_left', 'key_exists_right', 'left_unique_count',
            'right_unique_count', 'left_duplicate_count', 'right_duplicate_count',
            'common_keys_count', 'left_only_count', 'right_only_count',
            'data_type_compatible', 'estimated_result_rows', 'join_recommendation'
        }
        assert set(result.keys()) == required_keys, f"Missing keys: {required_keys - set(result.keys())}"

        # Check specific values
        assert result['key_exists_left'] is True, "Join key should exist in left DataFrame"
        assert result['key_exists_right'] is True, "Join key should exist in right DataFrame"
        assert result['common_keys_count'] == 2, "Should find 2 common keys (1, 2)"
        assert result['left_only_count'] == 2, "Should find 2 left-only keys (3, 4)"
        assert result['right_only_count'] == 1, "Should find 1 right-only key (5)"

    def test_missing_join_key(self):
        """Test validation when join key is missing in one DataFrame"""
        left_df = pd.DataFrame({'station_id': [1, 2, 3], 'temp': [20, 25, 30]})
        right_df = pd.DataFrame({'location_id': [1, 2], 'location': ['A', 'B']})

        result = validate_join_keys(left_df, right_df, 'station_id')

        assert result['key_exists_left'] is True, "Key should exist in left DataFrame"
        assert result['key_exists_right'] is False, "Key should not exist in right DataFrame"

    def test_duplicate_key_detection(self):
        """Test detection of duplicate keys"""
        left_df = pd.DataFrame({
            'station_id': [1, 2, 2, 3, 3, 3],  # 1 duplicate of 2, 2 duplicates of 3
            'reading': [10, 20, 21, 30, 31, 32]
        })
        right_df = pd.DataFrame({
            'station_id': [1, 1, 2],  # 1 duplicate of 1
            'location': ['A', 'A2', 'B']
        })

        result = validate_join_keys(left_df, right_df, 'station_id')

        assert result['left_duplicate_count'] == 3, "Should detect 3 duplicate rows in left (1 of id=2, 2 of id=3)"
        assert result['right_duplicate_count'] == 1, "Should detect 1 duplicate row in right (1 of id=1)"
        assert result['left_unique_count'] == 3, "Should have 3 unique keys in left (1, 2, 3)"
        assert result['right_unique_count'] == 2, "Should have 2 unique keys in right (1, 2)"

    def test_data_type_compatibility(self):
        """Test data type compatibility checking"""
        left_df = pd.DataFrame({'id': [1, 2, 3]})  # int64
        right_df = pd.DataFrame({'id': ['1', '2', '4']})  # object (string)

        result = validate_join_keys(left_df, right_df, 'id')

        # Implementation may vary, but should detect incompatibility
        assert 'data_type_compatible' in result, "Should check data type compatibility"
        assert isinstance(result['data_type_compatible'], bool), "Compatibility should be boolean"

    def test_empty_dataframes(self):
        """Test validation with empty DataFrames"""
        left_df = pd.DataFrame({'id': []})
        right_df = pd.DataFrame({'id': [1, 2, 3]})

        result = validate_join_keys(left_df, right_df, 'id')

        assert result['left_unique_count'] == 0, "Empty DataFrame should have 0 unique keys"
        assert result['common_keys_count'] == 0, "Should have 0 common keys with empty left"
        assert result['estimated_result_rows'] == 0, "Estimated result should be 0 with empty left"

    def test_join_recommendation(self):
        """Test that function provides join recommendations"""
        left_df = pd.DataFrame({'id': [1, 2, 3, 4], 'data': ['a', 'b', 'c', 'd']})
        right_df = pd.DataFrame({'id': [1, 2], 'info': ['x', 'y']})

        result = validate_join_keys(left_df, right_df, 'id')

        assert isinstance(result['join_recommendation'], str), "Should provide string recommendation"
        assert len(result['join_recommendation']) > 0, "Recommendation should not be empty"

    @pytest.mark.benchmark(group="validation")
    def test_validation_performance(self, benchmark):
        """Test validation performance on large DataFrames"""
        np.random.seed(42)
        size = 100000

        left_df = pd.DataFrame({
            'id': np.random.randint(0, size//2, size),
            'value': np.random.random(size)
        })
        right_df = pd.DataFrame({
            'id': np.random.randint(0, size//3, size//2),
            'info': np.random.choice(['A', 'B', 'C'], size//2)
        })

        result = benchmark(validate_join_keys, left_df, right_df, 'id')

        assert isinstance(result, dict), "Should return validation results"
        assert result['estimated_result_rows'] > 0, "Should estimate some result rows"


class TestSmartJoinGISData:
    """Test cases for smart_join_gis_data function"""

    def test_basic_left_join(self):
        """Test basic left join functionality"""
        infrastructure_df = pd.DataFrame({
            'region_id': [1, 2, 3, 4],
            'roads_km': [10, 15, 8, 12],
            'bridges': [2, 3, 1, 2]
        })
        demographic_df = pd.DataFrame({
            'region_id': [1, 2, 5],
            'population': [1000, 1500, 800],
            'median_age': [35, 42, 28]
        })

        result_df, stats = smart_join_gis_data(
            infrastructure_df, demographic_df, 'region_id', 'left'
        )

        assert isinstance(result_df, pd.DataFrame), "First return value must be DataFrame"
        assert isinstance(stats, dict), "Second return value must be dictionary"

        # Check DataFrame properties
        assert len(result_df) == 4, "Left join should preserve all left rows"
        assert 'population' in result_df.columns, "Should include right DataFrame columns"

        # Check statistics
        required_stat_keys = {
            'input_left_rows', 'input_right_rows', 'output_rows',
            'matched_keys', 'unmatched_left_keys', 'unmatched_right_keys',
            'duplicate_keys_handled', 'null_keys_dropped'
        }
        assert set(stats.keys()) == required_stat_keys, f"Missing stat keys: {required_stat_keys - set(stats.keys())}"

        assert stats['input_left_rows'] == 4, "Should record correct input left rows"
        assert stats['input_right_rows'] == 3, "Should record correct input right rows"
        assert stats['output_rows'] == 4, "Should record correct output rows"
        assert stats['matched_keys'] == 2, "Should have 2 matched keys (1, 2)"
        assert stats['unmatched_left_keys'] == 2, "Should have 2 unmatched left keys (3, 4)"

    def test_inner_join(self):
        """Test inner join functionality"""
        left_df = pd.DataFrame({
            'station_id': [1, 2, 3, 4],
            'temperature': [20, 25, 30, 22]
        })
        right_df = pd.DataFrame({
            'station_id': [2, 3, 5],
            'location': ['B', 'C', 'E']
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'station_id', 'inner')

        assert len(result_df) == 2, "Inner join should only include matched rows"
        assert stats['output_rows'] == 2, "Stats should reflect inner join result size"
        assert set(result_df['station_id']) == {2, 3}, "Should only include common keys"

    def test_outer_join(self):
        """Test outer join functionality"""
        left_df = pd.DataFrame({
            'id': [1, 2, 3],
            'left_data': ['a', 'b', 'c']
        })
        right_df = pd.DataFrame({
            'id': [2, 3, 4],
            'right_data': ['x', 'y', 'z']
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'id', 'outer')

        assert len(result_df) == 4, "Outer join should include all unique keys"
        assert stats['output_rows'] == 4, "Stats should reflect outer join result size"

    def test_duplicate_key_handling(self):
        """Test handling of duplicate keys in join"""
        left_df = pd.DataFrame({
            'region_id': [1, 1, 2, 3],  # Duplicate region_id=1
            'measurement': [10, 11, 20, 30]
        })
        right_df = pd.DataFrame({
            'region_id': [1, 2, 2],  # Duplicate region_id=2
            'info': ['A', 'B', 'C']
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'region_id', 'left')

        assert isinstance(result_df, pd.DataFrame), "Should handle duplicates gracefully"
        assert stats['duplicate_keys_handled'] >= 0, "Should report duplicate handling"
        assert len(result_df) >= len(left_df), "Result should have at least as many rows as left"

    def test_null_key_handling(self):
        """Test handling of null values in join keys"""
        left_df = pd.DataFrame({
            'id': [1, 2, np.nan, 4],
            'value': [10, 20, 30, 40]
        })
        right_df = pd.DataFrame({
            'id': [1, np.nan, 3],
            'info': ['A', 'B', 'C']
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'id', 'left')

        assert isinstance(result_df, pd.DataFrame), "Should handle null keys"
        # Depending on implementation, null keys might be dropped or handled specially
        assert stats['null_keys_dropped'] >= 0, "Should report null key handling"

    def test_overlapping_column_names(self):
        """Test handling of overlapping column names"""
        left_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Left1', 'Left2', 'Left3'],
            'value': [10, 20, 30]
        })
        right_df = pd.DataFrame({
            'id': [1, 2, 4],
            'name': ['Right1', 'Right2', 'Right4'],
            'value': [100, 200, 400]
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'id', 'left')

        # Should handle overlapping columns with suffixes or other strategy
        assert len(result_df.columns) > 3, "Should have more columns than just id plus unique names"
        # The exact column names depend on implementation (suffixes, etc.)

    def test_data_type_preservation(self):
        """Test that data types are preserved during join"""
        left_df = pd.DataFrame({
            'id': [1, 2, 3],
            'float_col': [1.5, 2.5, 3.5],
            'int_col': pd.array([10, 20, 30], dtype='int32'),
            'bool_col': [True, False, True]
        })
        right_df = pd.DataFrame({
            'id': [1, 2, 4],
            'str_col': ['a', 'b', 'c']
        })

        result_df, stats = smart_join_gis_data(left_df, right_df, 'id', 'left')

        # Check that data types are reasonably preserved
        assert pd.api.types.is_float_dtype(result_df['float_col']), "Float column should remain float"
        assert pd.api.types.is_bool_dtype(result_df['bool_col']), "Bool column should remain bool"
        assert pd.api.types.is_object_dtype(result_df['str_col']), "String column should be object type"

    @pytest.mark.benchmark(group="joins")
    def test_join_performance(self, benchmark):
        """Test join performance on moderately large datasets"""
        np.random.seed(42)
        left_size = 50000
        right_size = 30000

        left_df = pd.DataFrame({
            'id': np.random.randint(0, left_size//2, left_size),
            'left_value': np.random.random(left_size)
        })
        right_df = pd.DataFrame({
            'id': np.random.randint(0, right_size//2, right_size),
            'right_value': np.random.choice(['A', 'B', 'C'], right_size)
        })

        result_df, stats = benchmark(smart_join_gis_data, left_df, right_df, 'id', 'left')

        assert len(result_df) == left_size, "Left join should preserve left DataFrame size"
        assert stats['output_rows'] == left_size, "Stats should match result"


class TestComplexMultiDatasetJoin:
    """Test cases for complex_multi_dataset_join function"""

    def test_basic_sequential_join(self):
        """Test basic sequential joining of multiple datasets"""
        datasets = {
            'infrastructure': pd.DataFrame({
                'region_id': [1, 2, 3],
                'roads_km': [10, 15, 8]
            }),
            'demographics': pd.DataFrame({
                'region_id': [1, 2, 4],
                'population': [1000, 1500, 800]
            }),
            'environment': pd.DataFrame({
                'region_id': [1, 2, 3],
                'air_quality': [50, 75, 60]
            })
        }

        join_sequence = [
            ('infrastructure', 'demographics', 'region_id'),
            ('infrastructure', 'environment', 'region_id')
        ]

        result = complex_multi_dataset_join(datasets, join_sequence)

        assert isinstance(result, pd.DataFrame), "Function must return a DataFrame"
        assert len(result) == 3, "Should preserve base dataset size for left joins"
        assert 'roads_km' in result.columns, "Should include infrastructure columns"
        assert 'population' in result.columns, "Should include demographic columns"
        assert 'air_quality' in result.columns, "Should include environment columns"

    def test_three_dataset_join(self):
        """Test joining three datasets in sequence"""
        datasets = {
            'base': pd.DataFrame({
                'id': [1, 2, 3, 4],
                'base_value': ['A', 'B', 'C', 'D']
            }),
            'second': pd.DataFrame({
                'id': [1, 2, 3],
                'second_value': [10, 20, 30]
            }),
            'third': pd.DataFrame({
                'id': [1, 2, 5],
                'third_value': [100, 200, 500]
            })
        }

        join_sequence = [
            ('base', 'second', 'id'),
            ('base', 'third', 'id')
        ]

        result = complex_multi_dataset_join(datasets, join_sequence)

        expected_columns = {'id', 'base_value', 'second_value', 'third_value'}
        assert set(result.columns) >= expected_columns, "Should include all dataset columns"
        assert len(result) == 4, "Should preserve base dataset size"

    def test_invalid_dataset_name(self):
        """Test error handling for invalid dataset names"""
        datasets = {
            'dataset1': pd.DataFrame({'id': [1, 2], 'value': [10, 20]})
        }

        join_sequence = [
            ('dataset1', 'nonexistent_dataset', 'id')
        ]

        with pytest.raises((KeyError, ValueError)):
            complex_multi_dataset_join(datasets, join_sequence)

    def test_missing_join_key(self):
        """Test error handling for missing join keys"""
        datasets = {
            'left': pd.DataFrame({'id': [1, 2], 'value': [10, 20]}),
            'right': pd.DataFrame({'other_id': [1, 2], 'info': ['A', 'B']})
        }

        join_sequence = [
            ('left', 'right', 'id')  # 'id' doesn't exist in 'right'
        ]

        with pytest.raises((KeyError, ValueError)):
            complex_multi_dataset_join(datasets, join_sequence)

    def test_empty_join_sequence(self):
        """Test behavior with empty join sequence"""
        datasets = {
            'data': pd.DataFrame({'id': [1, 2], 'value': [10, 20]})
        }

        join_sequence = []

        # Depending on implementation, this might return the first dataset or raise an error
        try:
            result = complex_multi_dataset_join(datasets, join_sequence)
            assert isinstance(result, pd.DataFrame), "Should handle empty sequence gracefully"
        except (ValueError, IndexError):
            pass  # Acceptable to raise error for empty sequence

    def test_single_dataset_no_joins(self):
        """Test with single dataset and no actual joins needed"""
        datasets = {
            'only_data': pd.DataFrame({
                'id': [1, 2, 3],
                'value': [10, 20, 30]
            })
        }

        join_sequence = []

        # Should either return the single dataset or handle gracefully
        try:
            result = complex_multi_dataset_join(datasets, join_sequence)
            if result is not None:
                assert len(result) >= 0, "Result should be valid DataFrame"
        except (ValueError, IndexError):
            pass  # Acceptable behavior

    def test_complex_join_chain(self):
        """Test complex chain of joins with multiple datasets"""
        # Simulate a realistic GIS scenario
        datasets = {
            'stations': pd.DataFrame({
                'station_id': [1, 2, 3, 4],
                'name': ['A', 'B', 'C', 'D'],
                'region_id': [10, 10, 20, 20]
            }),
            'regions': pd.DataFrame({
                'region_id': [10, 20, 30],
                'region_name': ['North', 'South', 'East'],
                'area_km2': [100, 150, 75]
            }),
            'measurements': pd.DataFrame({
                'station_id': [1, 2, 3],
                'temperature': [20, 25, 30],
                'humidity': [60, 55, 70]
            }),
            'demographics': pd.DataFrame({
                'region_id': [10, 20],
                'population': [50000, 75000],
                'density': [500, 500]
            })
        }

        join_sequence = [
            ('stations', 'regions', 'region_id'),
            ('stations', 'measurements', 'station_id'),
            ('stations', 'demographics', 'region_id')
        ]

        result = complex_multi_dataset_join(datasets, join_sequence)

        assert isinstance(result, pd.DataFrame), "Should return valid DataFrame"
        assert len(result) == 4, "Should preserve stations (base) count"

        # Check that columns from all datasets are present
        expected_columns = {'station_id', 'name', 'region_id', 'region_name',
                          'temperature', 'population'}
        assert expected_columns.issubset(set(result.columns)), \
            "Should include columns from all joined datasets"

    @pytest.mark.benchmark(group="multi-join")
    def test_multi_join_performance(self, benchmark):
        """Test performance of multi-dataset joins"""
        np.random.seed(42)
        base_size = 10000

        datasets = {
            'base': pd.DataFrame({
                'id': range(base_size),
                'base_value': np.random.random(base_size)
            }),
            'second': pd.DataFrame({
                'id': np.random.choice(base_size, base_size//2),
                'second_value': np.random.choice(['A', 'B', 'C'], base_size//2)
            }),
            'third': pd.DataFrame({
                'id': np.random.choice(base_size, base_size//3),
                'third_value': np.random.random(base_size//3)
            })
        }

        join_sequence = [
            ('base', 'second', 'id'),
            ('base', 'third', 'id')
        ]

        result = benchmark(complex_multi_dataset_join, datasets, join_sequence)

        assert len(result) == base_size, "Should preserve base dataset size"
        assert len(result.columns) >= 4, "Should have columns from multiple datasets"


class TestIntegrationScenarios:
    """Integration tests combining multiple functions"""

    def test_validate_then_join_workflow(self):
        """Test workflow of validation followed by smart join"""
        left_df = pd.DataFrame({
            'station_id': [1, 2, 3, 4],
            'temperature': [20, 25, 30, 22]
        })
        right_df = pd.DataFrame({
            'station_id': [1, 2, 5],
            'location': ['A', 'B', 'C']
        })

        # First validate
        validation = validate_join_keys(left_df, right_df, 'station_id')

        assert validation['key_exists_left'], "Validation should pass for left"
        assert validation['key_exists_right'], "Validation should pass for right"

        # Then perform join
        result_df, stats = smart_join_gis_data(left_df, right_df, 'station_id', 'left')

        # Results should be consistent
        assert len(result_df) == validation['input_left_rows'] if 'input_left_rows' in validation else len(left_df)

    def test_realistic_gis_scenario(self):
        """Test realistic GIS data processing scenario"""
        # Environmental monitoring stations
        stations = pd.DataFrame({
            'station_id': [1, 2, 3, 4, 5],
            'name': ['Downtown', 'Park', 'Industrial', 'Suburban', 'Coastal'],
            'lat': [45.52, 45.53, 45.51, 45.54, 45.50],
            'lon': [-122.67, -122.68, -122.66, -122.69, -122.65],
            'region_id': [1, 1, 2, 1, 3]
        })

        # Air quality measurements
        measurements = pd.DataFrame({
            'station_id': [1, 2, 3, 4, 6],  # Station 6 doesn't exist, station 5 has no measurement
            'aqi': [85, 45, 120, 67, 95],
            'pm25': [35, 20, 55, 30, 40]
        })

        # Regional information
        regions = pd.DataFrame({
            'region_id': [1, 2, 3, 4],  # Region 4 has no stations
            'region_name': ['Metro', 'Industrial', 'Coastal', 'Rural'],
            'population': [500000, 100000, 50000, 25000]
        })

        # Test multi-dataset join
        datasets = {
            'stations': stations,
            'measurements': measurements,
            'regions': regions
        }

        join_sequence = [
            ('stations', 'measurements', 'station_id'),
            ('stations', 'regions', 'region_id')
        ]

        result = complex_multi_dataset_join(datasets, join_sequence)

        assert isinstance(result, pd.DataFrame), "Should return valid result"
        assert len(result) == len(stations), "Should preserve all stations"
        assert 'aqi' in result.columns, "Should include measurement data"
        assert 'region_name' in result.columns, "Should include regional data"
