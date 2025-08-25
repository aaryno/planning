"""
Test module for data subsetting implementation
Comprehensive automated testing for pandas boolean indexing and filtering operations
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
    from src.pandas_analysis.data_subsetting import (
        boolean_filter_environmental_data,
        multi_condition_analysis,
        optimize_boolean_operations
    )
except ImportError:
    pytest.skip("Student implementation not found", allow_module_level=True)


class TestBooleanFilterEnvironmentalData:
    """Test cases for boolean_filter_environmental_data function"""

    def test_basic_filtering(self):
        """Test basic filtering functionality with standard conditions"""
        df = pd.DataFrame({
            'air_quality_index': [50, 120, 80, 95, 45],
            'temperature_celsius': [20, 35, 18, 25, 22],
            'humidity_percent': [60, 45, 70, 55, 65],
            'station_id': [1, 2, 3, 4, 5]
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 30.0))

        assert isinstance(result, pd.DataFrame), "Function must return a pandas DataFrame"
        # Should include rows 0, 2, 4 (AQI <= 100 and temp in range)
        expected_stations = [1, 3, 5]
        assert list(result['station_id']) == expected_stations, f"Expected stations {expected_stations}"
        assert len(result) == 3, "Should return 3 rows meeting criteria"

    def test_default_parameters(self):
        """Test function with default parameter values"""
        df = pd.DataFrame({
            'air_quality_index': [99, 101, 50],
            'temperature_celsius': [20, 22, 25],
            'humidity_percent': [50, 55, 60]
        })

        result = boolean_filter_environmental_data(df)  # Use defaults

        assert len(result) == 2, "Should return 2 rows with default thresholds"
        assert result['air_quality_index'].max() <= 100.0, "All AQI values should be <= default threshold"

    def test_temperature_range_filtering(self):
        """Test temperature range filtering specifically"""
        df = pd.DataFrame({
            'air_quality_index': [50, 50, 50, 50, 50],
            'temperature_celsius': [10, 15, 20, 25, 35],
            'humidity_percent': [50, 50, 50, 50, 50]
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 25.0))

        assert len(result) == 3, "Should return 3 rows with temperature in range [15, 25]"
        assert result['temperature_celsius'].min() >= 15.0, "All temperatures should be >= 15"
        assert result['temperature_celsius'].max() <= 25.0, "All temperatures should be <= 25"

    def test_nan_value_handling(self):
        """Test handling of NaN values in filter columns"""
        df = pd.DataFrame({
            'air_quality_index': [50, np.nan, 80, 95, np.nan],
            'temperature_celsius': [20, 22, np.nan, 25, 18],
            'humidity_percent': [60, 55, 70, np.nan, 65],
            'station_id': [1, 2, 3, 4, 5]
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 30.0))

        # Should only include rows without NaN in critical columns
        assert result['air_quality_index'].isna().sum() == 0, "Result should not contain NaN AQI values"
        assert result['temperature_celsius'].isna().sum() == 0, "Result should not contain NaN temperature values"
        # Row 1 (station 1) should be the only one meeting all criteria without NaN
        expected_stations = [1, 5] if len(result) == 2 else [1]
        assert 1 in result['station_id'].values, "Station 1 should be included"

    def test_empty_result(self):
        """Test case where no rows meet the criteria"""
        df = pd.DataFrame({
            'air_quality_index': [150, 200, 180],
            'temperature_celsius': [40, 45, 50],
            'humidity_percent': [20, 25, 30]
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 30.0))

        assert isinstance(result, pd.DataFrame), "Should return DataFrame even if empty"
        assert len(result) == 0, "Should return empty DataFrame when no rows meet criteria"
        assert list(result.columns) == list(df.columns), "Should preserve column structure"

    def test_all_rows_qualify(self):
        """Test case where all rows meet the criteria"""
        df = pd.DataFrame({
            'air_quality_index': [50, 60, 70, 80],
            'temperature_celsius': [20, 22, 25, 18],
            'humidity_percent': [50, 55, 60, 65]
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 30.0))

        assert len(result) == len(df), "All rows should meet criteria"
        pd.testing.assert_frame_equal(result.reset_index(drop=True), df.reset_index(drop=True))

    def test_column_preservation(self):
        """Test that all original columns are preserved"""
        df = pd.DataFrame({
            'air_quality_index': [50, 80, 95],
            'temperature_celsius': [20, 22, 25],
            'humidity_percent': [50, 55, 60],
            'station_name': ['A', 'B', 'C'],
            'latitude': [45.1, 45.2, 45.3],
            'longitude': [-122.1, -122.2, -122.3],
            'extra_column': ['X', 'Y', 'Z']
        })

        result = boolean_filter_environmental_data(df, 100.0, (15.0, 30.0))

        assert set(result.columns) == set(df.columns), "All original columns should be preserved"
        assert len(result) > 0, "Should have some results"

    @pytest.mark.benchmark(group="filtering")
    def test_performance_large_dataset(self, benchmark):
        """Test performance on large dataset"""
        np.random.seed(42)
        size = 100000

        df = pd.DataFrame({
            'air_quality_index': np.random.normal(80, 30, size),
            'temperature_celsius': np.random.normal(22, 8, size),
            'humidity_percent': np.random.normal(50, 15, size),
            'station_id': range(size)
        })

        result = benchmark(boolean_filter_environmental_data, df, 100.0, (15.0, 30.0))

        assert len(result) > 0, "Should return some filtered results"
        assert len(result) < len(df), "Should filter out some rows"


class TestMultiConditionAnalysis:
    """Test cases for multi_condition_analysis function"""

    def test_basic_categorization(self):
        """Test basic categorization functionality"""
        df = pd.DataFrame({
            'air_quality_index': [25, 75, 125, 175],  # excellent, good, poor, critical
            'temperature_celsius': [20, 22, 15, 35],  # good for all categories
            'humidity_percent': [50, 65, 25, 85]      # good for all categories
        })

        result = multi_condition_analysis(df)

        assert isinstance(result, dict), "Function must return a dictionary"
        expected_keys = {'excellent', 'good', 'poor', 'critical'}
        assert set(result.keys()) == expected_keys, f"Must return exactly these keys: {expected_keys}"

        # Check that each category has the expected row
        assert len(result['excellent']) == 1, "Should have 1 excellent quality reading"
        assert len(result['good']) == 1, "Should have 1 good quality reading"
        assert len(result['poor']) == 1, "Should have 1 poor quality reading"
        assert len(result['critical']) == 1, "Should have 1 critical quality reading"

    def test_excellent_category_criteria(self):
        """Test excellent category criteria specifically"""
        df = pd.DataFrame({
            'air_quality_index': [30, 50, 51],  # 30,50 eligible, 51 not
            'temperature_celsius': [20, 22, 20],  # all in [18,24] range
            'humidity_percent': [45, 55, 45]      # all in [40,60] range
        })

        result = multi_condition_analysis(df)

        excellent_df = result['excellent']
        assert len(excellent_df) == 2, "Should have 2 excellent readings"
        assert excellent_df['air_quality_index'].max() <= 50, "Excellent AQI should be <= 50"
        assert excellent_df['temperature_celsius'].min() >= 18, "Excellent temp should be >= 18"
        assert excellent_df['temperature_celsius'].max() <= 24, "Excellent temp should be <= 24"

    def test_mutual_exclusivity(self):
        """Test that categories are mutually exclusive"""
        np.random.seed(123)
        df = pd.DataFrame({
            'air_quality_index': np.random.uniform(10, 200, 100),
            'temperature_celsius': np.random.uniform(10, 40, 100),
            'humidity_percent': np.random.uniform(20, 90, 100)
        })

        result = multi_condition_analysis(df)

        # Collect all row indices across categories
        all_indices = set()
        for category, cat_df in result.items():
            current_indices = set(cat_df.index)
            # Check no overlap with previous categories
            assert current_indices.isdisjoint(all_indices), f"Category {category} overlaps with previous categories"
            all_indices.update(current_indices)

    def test_complete_coverage(self):
        """Test that all rows are assigned to exactly one category"""
        df = pd.DataFrame({
            'air_quality_index': [25, 75, 125, 175, 90],
            'temperature_celsius': [20, 22, 15, 35, 28],
            'humidity_percent': [50, 65, 25, 85, 45]
        })

        result = multi_condition_analysis(df)

        total_categorized = sum(len(cat_df) for cat_df in result.values())
        assert total_categorized == len(df), "All rows should be categorized exactly once"

    def test_edge_case_boundary_values(self):
        """Test boundary values for category definitions"""
        df = pd.DataFrame({
            'air_quality_index': [50, 50.1, 100, 100.1, 150, 150.1],  # Boundary values
            'temperature_celsius': [20, 20, 20, 20, 20, 20],
            'humidity_percent': [50, 50, 50, 50, 50, 50]
        })

        result = multi_condition_analysis(df)

        # Row with AQI=50 should be excellent (<=50)
        # Row with AQI=50.1 should be good (<=100 but not excellent)
        assert any(50 in cat_df['air_quality_index'].values for cat_df in [result['excellent']]), "AQI=50 should be in excellent"
        assert any(100 in cat_df['air_quality_index'].values for cat_df in [result['good']]), "AQI=100 should be in good"
