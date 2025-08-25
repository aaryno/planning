"""
Test Package for Pandas Analysis Assignment
===========================================

This package contains comprehensive automated tests for the pandas analysis assignment.
All test modules use pytest framework with additional plugins for coverage and benchmarking.

Test Modules:
-------------
- test_data_structures: Tests for Series and DataFrame operations
- test_data_subsetting: Tests for boolean indexing and filtering
- test_data_joins: Tests for join and merge operations
- test_file_operations: Tests for robust I/O operations

Test Configuration:
------------------
- Coverage threshold: 80%
- Performance benchmarks included
- Automated grading integration
- CI/CD pipeline compatibility

Usage:
------
Run all tests:
    pytest tests/

Run specific module:
    pytest tests/test_data_structures.py

Run with coverage:
    pytest tests/ --cov=src --cov-report=html

Run benchmarks only:
    pytest tests/ --benchmark-only
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
from typing import Dict, Any, List

# Test configuration constants
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
TEMP_OUTPUT_DIR = Path(tempfile.gettempdir()) / "pandas_assignment_tests"

# Performance thresholds for benchmarks
PERFORMANCE_THRESHOLDS = {
    "series_creation_max_time": 1.0,
    "dataframe_optimization_max_time": 2.0,
    "boolean_filtering_max_time": 1.0,
    "join_operations_max_time": 3.0,
    "file_io_max_time": 10.0
}

# Test data sizes for performance testing
TEST_DATA_SIZES = {
    "small": 1000,
    "medium": 10000,
    "large": 100000
}


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (may take several seconds)"
    )
    config.addinivalue_line(
        "markers", "benchmark: marks tests as performance benchmarks"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


@pytest.fixture(scope="session")
def test_output_dir():
    """Create temporary directory for test outputs."""
    TEMP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yield TEMP_OUTPUT_DIR
    # Cleanup after all tests
    if TEMP_OUTPUT_DIR.exists():
        shutil.rmtree(TEMP_OUTPUT_DIR)


@pytest.fixture
def sample_gis_dataframe():
    """Create a sample GIS-style DataFrame for testing."""
    np.random.seed(42)
    size = 1000

    data = {
        'station_id': range(1, size + 1),
        'station_name': [f'Station_{i%10}' for i in range(size)],
        'latitude': np.random.uniform(45.0, 46.0, size),
        'longitude': np.random.uniform(-123.5, -122.0, size),
        'elevation_m': np.random.randint(0, 500, size),
        'air_quality_index': np.random.normal(75, 25, size),
        'temperature_celsius': np.random.normal(20, 8, size),
        'humidity_percent': np.random.normal(50, 15, size),
        'active': np.random.choice([True, False], size, p=[0.8, 0.2]),
        'region': np.random.choice(['Urban', 'Suburban', 'Rural'], size),
        'install_date': pd.date_range('2020-01-01', periods=size, freq='D')[:size]
    }

    # Add some missing values to make it realistic
    data['air_quality_index'][np.random.choice(size, 50, replace=False)] = np.nan
    data['temperature_celsius'][np.random.choice(size, 30, replace=False)] = np.nan

    return pd.DataFrame(data)


@pytest.fixture
def sample_environmental_data():
    """Create environmental monitoring data for testing joins and filtering."""
    np.random.seed(123)

    # Base stations
    stations = pd.DataFrame({
        'station_id': range(1, 21),
        'station_name': [f'Monitor_{i:02d}' for i in range(1, 21)],
        'latitude': np.random.uniform(45.0, 45.6, 20),
        'longitude': np.random.uniform(-123.0, -122.0, 20),
        'region_id': np.random.choice(range(1, 6), 20),
        'elevation_m': np.random.randint(5, 200, 20)
    })

    # Measurements (multiple per station)
    measurements = []
    for station_id in range(1, 21):
        for hour in range(24):
            measurements.append({
                'station_id': station_id,
                'timestamp': pd.Timestamp('2023-01-01') + pd.Timedelta(hours=hour),
                'air_quality_index': max(10, np.random.normal(70, 30)),
                'temperature_celsius': np.random.normal(18, 6),
                'humidity_percent': np.random.normal(55, 20),
                'wind_speed_kmh': np.random.exponential(10),
                'precipitation_mm': max(0, np.random.normal(0.5, 2))
            })

    measurements_df = pd.DataFrame(measurements)

    # Regional information
    regions = pd.DataFrame({
        'region_id': range(1, 6),
        'region_name': ['Downtown', 'Suburban_North', 'Industrial_East', 'Rural_West', 'Coastal'],
        'population': [50000, 25000, 15000, 5000, 8000],
        'area_km2': [25, 45, 30, 120, 35]
    })

    return {
        'stations': stations,
        'measurements': measurements_df,
        'regions': regions
    }


@pytest.fixture
def large_dataframe_for_benchmarks():
    """Create large DataFrame for performance testing."""
    np.random.seed(456)
    size = TEST_DATA_SIZES["large"]

    return pd.DataFrame({
        'id': range(size),
        'category': np.random.choice(['A', 'B', 'C', 'D'], size),
        'value1': np.random.random(size) * 1000,
        'value2': np.random.randint(0, 1000, size),
        'flag': np.random.choice([True, False], size),
        'date': pd.date_range('2020-01-01', periods=size, freq='1H')
    })


@pytest.fixture
def csv_test_files(test_output_dir):
    """Create various CSV test files with different characteristics."""
    files = {}

    # Standard CSV
    df_standard = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'value': [10.5, 20.3, 30.1, 40.7]
    })
    standard_path = test_output_dir / "standard.csv"
    df_standard.to_csv(standard_path, index=False)
    files['standard'] = str(standard_path)

    # CSV with encoding issues (Latin-1)
    df_encoded = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['José', 'François', 'Müller'],
        'location': ['São Paulo', 'Paris', 'München']
    })
    encoded_path = test_output_dir / "encoded.csv"
    df_encoded.to_csv(encoded_path, index=False, encoding='latin-1')
    files['encoded'] = str(encoded_path)

    # CSV with missing values
    df_missing = pd.DataFrame({
        'station': ['A', 'B', 'C', 'D'],
        'temperature': [20.5, np.nan, 25.1, 22.3],
        'humidity': [60, 55, np.nan, 65],
        'status': ['Active', 'Inactive', 'Active', np.nan]
    })
    missing_path = test_output_dir / "missing_values.csv"
    df_missing.to_csv(missing_path, index=False)
    files['missing'] = str(missing_path)

    return files


def assert_dataframe_equal_flexible(df1: pd.DataFrame, df2: pd.DataFrame,
                                   check_dtype: bool = True,
                                   check_index: bool = True,
                                   rtol: float = 1e-5):
    """
    Flexible DataFrame equality assertion for testing.

    Args:
        df1, df2: DataFrames to compare
        check_dtype: Whether to check data types
        check_index: Whether to check index equality
        rtol: Relative tolerance for float comparisons
    """
    try:
        pd.testing.assert_frame_equal(
            df1, df2,
            check_dtype=check_dtype,
            check_index=check_index,
            rtol=rtol
        )
    except AssertionError as e:
        pytest.fail(f"DataFrames are not equal: {str(e)}")


def assert_performance_acceptable(execution_time: float,
                                operation_name: str,
                                max_time: float = None):
    """
    Assert that operation performance meets requirements.

    Args:
        execution_time: Actual execution time in seconds
        operation_name: Name of the operation for error messages
        max_time: Maximum acceptable time (uses default if None)
    """
    if max_time is None:
        max_time = PERFORMANCE_THRESHOLDS.get(
            f"{operation_name}_max_time",
            5.0  # Default 5 second limit
        )

    assert execution_time <= max_time, (
        f"{operation_name} took {execution_time:.3f}s, "
        f"but should complete within {max_time}s"
    )


# Export useful testing utilities
__all__ = [
    'PERFORMANCE_THRESHOLDS',
    'TEST_DATA_SIZES',
    'assert_dataframe_equal_flexible',
    'assert_performance_acceptable',
    'sample_gis_dataframe',
    'sample_environmental_data',
    'large_dataframe_for_benchmarks',
    'csv_test_files'
]
