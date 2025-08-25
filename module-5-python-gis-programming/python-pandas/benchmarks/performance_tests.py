"""
Performance Benchmarks for Pandas Analysis Assignment
====================================================

This module contains performance benchmarks for all student-implemented functions.
Benchmarks use pytest-benchmark plugin to measure execution time and memory usage.

Usage:
    pytest benchmarks/performance_tests.py --benchmark-only
    pytest benchmarks/performance_tests.py --benchmark-json=results.json

Performance Requirements:
    - Series creation: 10,000 elements in <1.0s
    - Memory optimization: >20% reduction for large datasets
    - Boolean filtering: 100,000 rows in <1.0s
    - Join operations: 50,000 rows in <3.0s
    - File I/O: 50MB files in <10s
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
import time
from typing import Dict, Any, List

# Import student implementations
try:
    from src.pandas_analysis.data_structures import (
        create_gis_series,
        analyze_series_properties,
        create_gis_dataframe,
        optimize_dataframe_memory
    )
    from src.pandas_analysis.data_subsetting import (
        boolean_filter_environmental_data,
        multi_condition_analysis,
        optimize_boolean_operations
    )
    from src.pandas_analysis.data_joins import (
        validate_join_keys,
        smart_join_gis_data,
        complex_multi_dataset_join
    )
    from src.pandas_analysis.file_operations import (
        robust_csv_reader,
        export_with_metadata
    )
except ImportError:
    pytest.skip("Student implementation not found", allow_module_level=True)


# Test data generators
def generate_large_series_data(size: int = 100000):
    """Generate large dataset for Series performance testing."""
    np.random.seed(42)
    return {
        'data': np.random.uniform(-1000, 1000, size).tolist(),
        'index': [f'location_{i:06d}' for i in range(size)],
        'name': 'large_measurement_series'
    }


def generate_memory_inefficient_dataframe(size: int = 50000):
    """Generate DataFrame with suboptimal memory usage for optimization testing."""
    np.random.seed(123)

    # Create data with memory-inefficient types
    data = {
        'station_id': np.random.randint(1, 1000, size).astype('int64'),  # Could be int16
        'region': np.random.choice(['Urban', 'Suburban', 'Rural', 'Industrial'], size),  # Should be categorical
        'elevation_m': np.random.randint(0, 500, size).astype('int64'),  # Could be int16
        'temperature': np.random.uniform(-10, 40, size).astype('float64'),  # Could be float32
        'humidity': np.random.uniform(0, 100, size).astype('float64'),  # Could be float32
        'active': np.random.choice([0, 1], size).astype('int64'),  # Should be boolean
        'status': np.random.choice(['Active', 'Inactive', 'Maintenance', 'Offline'], size),  # Should be categorical
        'install_date': pd.date_range('2010-01-01', periods=size, freq='D')[:size]
    }

    return pd.DataFrame(data)


def generate_environmental_data(size: int = 100000):
    """Generate large environmental dataset for filtering benchmarks."""
    np.random.seed(456)

    return pd.DataFrame({
        'station_id': range(size),
        'air_quality_index': np.random.normal(75, 30, size),
        'temperature_celsius': np.random.normal(22, 8, size),
        'humidity_percent': np.random.normal(50, 20, size),
        'wind_speed_kmh': np.random.exponential(10, size),
        'precipitation_mm': np.maximum(0, np.random.normal(2, 5, size)),
        'timestamp': pd.date_range('2023-01-01', periods=size, freq='1H')
    })


def generate_join_datasets(left_size: int = 50000, right_size: int = 30000):
    """Generate datasets for join performance testing."""
    np.random.seed(789)

    # Create overlapping key ranges for realistic join scenarios
    max_key = max(left_size, right_size) // 2

    left_df = pd.DataFrame({
        'region_id': np.random.randint(1, max_key, left_size),
        'infrastructure_score': np.random.uniform(0, 100, left_size),
        'road_density': np.random.uniform(0.1, 5.0, left_size),
        'bridge_count': np.random.randint(0, 50, left_size)
    })

    right_df = pd.DataFrame({
        'region_id': np.random.randint(1, max_key, right_size),
        'population': np.random.randint(1000, 100000, right_size),
        'median_income': np.random.uniform(30000, 120000, right_size),
        'education_index': np.random.uniform(0, 10, right_size)
    })

    return left_df, right_df


class TestDataStructuresBenchmarks:
    """Performance benchmarks for data structures module."""

    @pytest.mark.benchmark(group="series-creation")
    def test_create_gis_series_performance(self, benchmark):
        """Benchmark Series creation with large dataset."""
        series_data = generate_large_series_data(10000)

        result = benchmark(
            create_gis_series,
            series_data['data'],
            series_data['index'],
            series_data['name']
        )

        assert isinstance(result, pd.Series), "Should return pandas Series"
        assert len(result) == 10000, "Should create series with correct size"
        assert result.name == series_data['name'], "Should set series name"

    @pytest.mark.benchmark(group="series-analysis")
    def test_analyze_series_properties_performance(self, benchmark):
        """Benchmark series analysis with large dataset."""
        # Create large series with mixed data types and missing values
        np.random.seed(42)
        size = 100000
        data = np.random.random(size)
        # Add some NaN values
        data[np.random.choice(size, size//10, replace=False)] = np.nan

        series = pd.Series(data, name='benchmark_series')

        result = benchmark(analyze_series_properties, series)

        assert isinstance(result, dict), "Should return dictionary"
        assert result['size'] == size, "Should report correct size"
        assert result['has_nulls'] is True, "Should detect null values"

    @pytest.mark.benchmark(group="dataframe-creation")
    def test_create_gis_dataframe_performance(self, benchmark):
        """Benchmark DataFrame creation with type optimization."""
        np.random.seed(42)
        size = 50000

        data_dict = {
            'station_id': list(range(size)),
            'station_name': [f'Station_{i%1000}' for i in range(size)],  # Repeated values for categorization
            'latitude': np.random.uniform(45.0, 46.0, size).tolist(),
            'longitude': np.random.uniform(-123.0, -122.0, size).tolist(),
            'elevation': np.random.randint(0, 1000, size).tolist(),
            'active': [bool(x) for x in np.random.choice([0, 1], size)],
            'install_date': [f'2020-{(i%12)+1:02d}-{(i%28)+1:02d}' for i in range(size)],
            'region': np.random.choice(['North', 'South', 'East', 'West'], size).tolist()
        }

        result = benchmark(create_gis_dataframe, data_dict)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame"
        assert len(result) == size, "Should create DataFrame with correct size"

    @pytest.mark.benchmark(group="memory-optimization", min_rounds=3)
    def test_optimize_dataframe_memory_performance(self, benchmark):
        """Benchmark memory optimization on large DataFrame."""
        df = generate_memory_inefficient_dataframe(30000)
        original_memory = df.memory_usage(deep=True).sum()

        optimized_df, memory_info = benchmark(optimize_dataframe_memory, df)

        assert isinstance(optimized_df, pd.DataFrame), "Should return optimized DataFrame"
        assert isinstance(memory_info, dict), "Should return memory info"
        assert len(optimized_df) == len(df), "Should preserve row count"

        # Verify memory reduction
        optimized_memory = optimized_df.memory_usage(deep=True).sum()
        reduction_percent = ((original_memory - optimized_memory) / original_memory) * 100
        assert reduction_percent >= 20, f"Should achieve at least 20% memory reduction, got {reduction_percent:.1f}%"


class TestDataSubsettingBenchmarks:
    """Performance benchmarks for data subsetting module."""

    @pytest.mark.benchmark(group="boolean-filtering")
    def test_boolean_filter_environmental_data_performance(self, benchmark):
        """Benchmark boolean filtering on large environmental dataset."""
        df = generate_environmental_data(100000)

        result = benchmark(
            boolean_filter_environmental_data,
            df,
            100.0,  # AQI threshold
            (15.0, 30.0)  # Temperature range
        )

        assert isinstance(result, pd.DataFrame), "Should return DataFrame"
        assert len(result) < len(df), "Should filter some rows"
        # Verify filtering worked correctly
        assert result['air_quality_index'].max() <= 100.0, "Should respect AQI threshold"

    @pytest.mark.benchmark(group="multi-condition")
    def test_multi_condition_analysis_performance(self, benchmark):
        """Benchmark multi-condition analysis on large dataset."""
        df = generate_environmental_data(50000)

        result = benchmark(multi_condition_analysis, df)

        assert isinstance(result, dict), "Should return dictionary"
        assert len(result) == 4, "Should return 4 categories"

        # Verify all rows are categorized
        total_categorized = sum(len(cat_df) for cat_df in result.values())
        # Allow for some rows to be dropped due to missing values
        assert total_categorized >= len(df) * 0.8, "Should categorize most rows"

    @pytest.mark.benchmark(group="optimize-boolean")
    def test_optimize_boolean_operations_performance(self, benchmark):
        """Benchmark optimized boolean operations."""
        df = generate_environmental_data(75000)

        conditions = [
            "air_quality_index <= 100",
            "temperature_celsius >= 15",
            "humidity_percent <= 80",
            "wind_speed_kmh < 20"
        ]

        result_df, exec_time = benchmark(optimize_boolean_operations, df, conditions)

        assert isinstance(result_df, pd.DataFrame), "Should return DataFrame"
        assert isinstance(exec_time, (int, float)), "Should return execution time"
        assert exec_time > 0, "Execution time should be positive"


class TestDataJoinsBenchmarks:
    """Performance benchmarks for data joins module."""

    @pytest.mark.benchmark(group="join-validation")
    def test_validate_join_keys_performance(self, benchmark):
        """Benchmark join key validation on large DataFrames."""
        left_df, right_df = generate_join_datasets(100000, 75000)

        result = benchmark(validate_join_keys, left_df, right_df, 'region_id')

        assert isinstance(result, dict), "Should return validation dictionary"
        assert 'common_keys_count' in result, "Should report common keys"
        assert result['estimated_result_rows'] > 0, "Should estimate result size"

    @pytest.mark.benchmark(group="smart-join")
    def test_smart_join_gis_data_performance(self, benchmark):
        """Benchmark smart GIS data joining."""
        left_df, right_df = generate_join_datasets(50000, 30000)

        result_df, stats = benchmark(
            smart_join_gis_data,
            left_df,
            right_df,
            'region_id',
            'left'
        )

        assert isinstance(result_df, pd.DataFrame), "Should return DataFrame"
        assert isinstance(stats, dict), "Should return statistics"
        assert len(result_df) == len(left_df), "Left join should preserve left size"

    @pytest.mark.benchmark(group="multi-dataset-join")
    def test_complex_multi_dataset_join_performance(self, benchmark):
        """Benchmark complex multi-dataset joins."""
        np.random.seed(42)
        size = 10000

        datasets = {
            'base': pd.DataFrame({
                'id': range(size),
                'base_value': np.random.random(size)
            }),
            'demographics': pd.DataFrame({
                'id': np.random.choice(size, size//2),
                'population': np.random.randint(1000, 50000, size//2)
            }),
            'infrastructure': pd.DataFrame({
                'id': np.random.choice(size, size//3),
                'road_quality': np.random.uniform(0, 10, size//3)
            }),
            'environmental': pd.DataFrame({
                'id': np.random.choice(size, size//4),
                'air_quality': np.random.uniform(0, 200, size//4)
            })
        }

        join_sequence = [
            ('base', 'demographics', 'id'),
            ('base', 'infrastructure', 'id'),
            ('base', 'environmental', 'id')
        ]

        result = benchmark(complex_multi_dataset_join, datasets, join_sequence)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame"
        assert len(result) == size, "Should preserve base dataset size"


class TestFileOperationsBenchmarks:
    """Performance benchmarks for file operations module."""

    @pytest.fixture(scope="class")
    def large_csv_file(self):
        """Create a large CSV file for I/O benchmarks."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Generate ~50MB CSV file
            np.random.seed(42)
            rows = 500000

            # Write header
            f.write('station_id,name,latitude,longitude,elevation,temperature,humidity,active,region\n')

            # Write data rows
            regions = ['Urban', 'Suburban', 'Rural', 'Industrial', 'Coastal']
            for i in range(rows):
                f.write(f'{i},'
                       f'Station_{i%1000},'
                       f'{45 + np.random.random():.6f},'
                       f'{-123 + np.random.random():.6f},'
                       f'{np.random.randint(0, 500)},'
                       f'{np.random.normal(20, 10):.2f},'
                       f'{np.random.uniform(0, 100):.1f},'
                       f'{np.random.choice(["True", "False"])},'
                       f'{np.random.choice(regions)}\n')

            filepath = f.name

        yield filepath

        # Cleanup
        os.unlink(filepath)

    @pytest.mark.benchmark(group="csv-reading")
    def test_robust_csv_reader_performance(self, benchmark, large_csv_file):
        """Benchmark robust CSV reading on large file."""

        df, quality_report = benchmark(robust_csv_reader, large_csv_file)

        assert isinstance(df, pd.DataFrame), "Should return DataFrame"
        assert isinstance(quality_report, dict), "Should return quality report"
        assert len(df) > 400000, "Should read most rows successfully"
        assert 'file_size_mb' in quality_report, "Should report file size"

    @pytest.mark.benchmark(group="export-metadata")
    def test_export_with_metadata_performance(self, benchmark):
        """Benchmark DataFrame export with metadata."""
        # Create large DataFrame
        np.random.seed(42)
        size = 100000
        df = pd.DataFrame({
            'id': range(size),
            'value1': np.random.random(size),
            'value2': np.random.randint(0, 1000, size),
            'category': np.random.choice(['A', 'B', 'C', 'D'], size),
            'timestamp': pd.date_range('2023-01-01', periods=size, freq='1H')
        })

        metadata = {
            'title': 'Performance Test Dataset',
            'description': 'Large dataset for export benchmarking',
            'processing_date': '2023-01-01',
            'source': 'Synthetic data for testing',
            'rows': len(df),
            'columns': len(df.columns)
        }

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            success = benchmark(export_with_metadata, df, temp_path, metadata)
            assert success is True, "Export should succeed"

            # Verify file was created
            assert os.path.exists(temp_path), "Export file should exist"

            # Check file size is reasonable
            file_size = os.path.getsize(temp_path)
            assert file_size > 1000000, "File should be reasonably large (>1MB)"

        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            # Also cleanup potential metadata file
            metadata_path = temp_path.replace('.csv', '_metadata.json')
            if os.path.exists(metadata_path):
                os.unlink(metadata_path)


class TestIntegratedWorkflowBenchmarks:
    """Benchmarks for realistic integrated workflows."""

    @pytest.mark.benchmark(group="end-to-end")
    def test_complete_gis_workflow_performance(self, benchmark):
        """Benchmark complete GIS data processing workflow."""

        def complete_workflow():
            # Step 1: Create and optimize environmental data
            np.random.seed(42)
            size = 20000

            raw_data = {
                'station_id': list(range(size)),
                'station_name': [f'Monitor_{i%500}' for i in range(size)],
                'air_quality_index': np.random.normal(75, 30, size).tolist(),
                'temperature_celsius': np.random.normal(22, 8, size).tolist(),
                'humidity_percent': np.random.normal(50, 15, size).tolist(),
                'active': [bool(x) for x in np.random.choice([0, 1], size)],
                'region_id': np.random.randint(1, 100, size).tolist()
            }

            # Create DataFrame with optimization
            df = create_gis_dataframe(raw_data)
            optimized_df, _ = optimize_dataframe_memory(df)

            # Step 2: Filter data
            filtered_df = boolean_filter_environmental_data(
                optimized_df, 100.0, (15.0, 30.0)
            )

            # Step 3: Create demographic data and join
            demo_df = pd.DataFrame({
                'region_id': range(1, 101),
                'population': np.random.randint(1000, 100000, 100),
                'area_km2': np.random.uniform(10, 500, 100)
            })

            joined_df, stats = smart_join_gis_data(
                filtered_df, demo_df, 'region_id', 'left'
            )

            return joined_df, stats

        result_df, stats = benchmark(complete_workflow)

        assert isinstance(result_df, pd.DataFrame), "Workflow should return DataFrame"
        assert len(result_df) > 0, "Should have some results after workflow"
        assert 'population' in result_df.columns, "Should include joined demographic data"

    @pytest.mark.benchmark(group="memory-efficiency", timer=time.perf_counter)
    def test_memory_efficient_large_dataset_processing(self, benchmark):
        """Test memory efficiency with very large datasets."""

        def memory_efficient_processing():
            # Process data in chunks to test memory efficiency
            np.random.seed(123)
            total_size = 200000
            chunk_size = 50000

            results = []
            for i in range(0, total_size, chunk_size):
                chunk_data = {
                    'id': list(range(i, min(i + chunk_size, total_size))),
                    'category': np.random.choice(['A', 'B', 'C'],
                                               min(chunk_size, total_size - i)).tolist(),
                    'value': np.random.random(min(chunk_size, total_size - i)).tolist()
                }

                chunk_df = create_gis_dataframe(chunk_data)
                optimized_chunk, _ = optimize_dataframe_memory(chunk_df)
                results.append(optimized_chunk)

            # Combine results
            final_df = pd.concat(results, ignore_index=True)
            return final_df

        result = benchmark(memory_efficient_processing)

        assert isinstance(result, pd.DataFrame), "Should return combined DataFrame"
        assert len(result) == 200000, "Should process all rows"


# Configuration for benchmark thresholds
PERFORMANCE_THRESHOLDS = {
    'series_creation_max_time': 1.0,
    'memory_optimization_max_time': 2.0,
    'boolean_filtering_max_time': 1.0,
    'smart_join_max_time': 3.0,
    'csv_reading_max_time': 10.0,
    'export_metadata_max_time': 15.0,
    'end_to_end_workflow_max_time': 20.0
}


def pytest_benchmark_update_json(config, benchmarks, output_json):
    """Custom benchmark result processing."""
    # Add performance threshold checking
    for benchmark in benchmarks:
        name = benchmark['name']
        mean_time = benchmark['stats']['mean']

        # Check against thresholds
        for threshold_key, threshold_value in PERFORMANCE_THRESHOLDS.items():
            if threshold_key.replace('_max_time', '').replace('_', '-') in name:
                benchmark['threshold_met'] = mean_time <= threshold_value
                benchmark['threshold_value'] = threshold_value
                break
