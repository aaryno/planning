"""
Pandas Analysis Package - GIST 604B Assignment
===============================================

This package contains modules for automated assessment of pandas data analysis skills.
Students must implement the functions in each module to pass the automated tests.

Modules:
--------
- data_structures: Series and DataFrame creation and optimization
- data_subsetting: Boolean indexing and filtering operations
- data_joins: Data joining and merging operations
- file_operations: Robust I/O operations with error handling

Usage:
------
from pandas_analysis.data_structures import create_gis_series, analyze_series_properties
from pandas_analysis.data_subsetting import boolean_filter_environmental_data
from pandas_analysis.data_joins import smart_join_gis_data
from pandas_analysis.file_operations import robust_csv_reader
"""

__version__ = "0.1.0"
__author__ = "GIST 604B Students"

# Import main functions from each module
# Note: These imports will fail until students implement the functions

try:
    from .data_structures import (
        create_gis_series,
        analyze_series_properties,
        create_gis_dataframe,
        optimize_dataframe_memory,
    )
except ImportError:
    # Functions not yet implemented
    pass

try:
    from .data_subsetting import (
        boolean_filter_environmental_data,
        multi_condition_analysis,
        optimize_boolean_operations,
    )
except ImportError:
    # Functions not yet implemented
    pass

try:
    from .data_joins import (
        validate_join_keys,
        smart_join_gis_data,
        complex_multi_dataset_join,
    )
except ImportError:
    # Functions not yet implemented
    pass

try:
    from .file_operations import (
        robust_csv_reader,
        export_with_metadata,
    )
except ImportError:
    # Functions not yet implemented
    pass

# Package metadata
__all__ = [
    # Data Structures
    "create_gis_series",
    "analyze_series_properties",
    "create_gis_dataframe",
    "optimize_dataframe_memory",

    # Data Subsetting
    "boolean_filter_environmental_data",
    "multi_condition_analysis",
    "optimize_boolean_operations",

    # Data Joins
    "validate_join_keys",
    "smart_join_gis_data",
    "complex_multi_dataset_join",

    # File Operations
    "robust_csv_reader",
    "export_with_metadata",
]
