"""
GeoPandas Analysis Package - GIST 604B Assignment
==================================================

A comprehensive spatial analysis toolkit for learning GeoPandas fundamentals
through hands-on programming with real-world geospatial datasets.

This package provides functions for:
- Loading and exploring spatial data from various formats
- Performing geometric operations and spatial calculations
- Conducting spatial joins and relationship analysis
- Creating static and interactive visualizations

Author: Student Name
Course: GIST 604B - Open Source GIS Programming
Module: Python GIS Programming
"""

__version__ = "0.1.0"
__author__ = "GIST 604B Student"
__email__ = "student@email.arizona.edu"

# Package metadata
__title__ = "geopandas-analysis"
__description__ = "GeoPandas fundamentals through automated assessment"
__url__ = "https://github.com/your-org/geopandas-analysis"
__license__ = "MIT"

# Core imports for the package
try:
    # Import key functions from each module to make them easily accessible
    from .spatial_data_loading import (
        load_spatial_dataset,
        explore_spatial_properties,
        validate_spatial_data,
        standardize_crs,
    )

    from .geometric_operations import (
        calculate_spatial_metrics,
        create_buffers_and_zones,
        geometric_transformations,
        proximity_analysis,
    )

    from .spatial_joins_analysis import (
        spatial_intersection_analysis,
        point_in_polygon_analysis,
        spatial_aggregation,
        multi_criteria_spatial_filter,
    )

    from .visualization_mapping import (
        create_choropleth_map,
        multi_layer_visualization,
        interactive_web_map,
        export_publication_maps,
    )

    # List of functions available when using 'from geopandas_analysis import *'
    __all__ = [
        # Spatial data loading functions
        'load_spatial_dataset',
        'explore_spatial_properties',
        'validate_spatial_data',
        'standardize_crs',

        # Geometric operations functions
        'calculate_spatial_metrics',
        'create_buffers_and_zones',
        'geometric_transformations',
        'proximity_analysis',

        # Spatial joins and analysis functions
        'spatial_intersection_analysis',
        'point_in_polygon_analysis',
        'spatial_aggregation',
        'multi_criteria_spatial_filter',

        # Visualization and mapping functions
        'create_choropleth_map',
        'multi_layer_visualization',
        'interactive_web_map',
        'export_publication_maps',
    ]

except ImportError as e:
    # Handle cases where the modules haven't been implemented yet
    # This prevents import errors during development
    import warnings
    warnings.warn(
        f"Some functions could not be imported: {e}. "
        f"This is normal during development - implement the missing functions in the appropriate modules.",
        ImportWarning
    )
    __all__ = []

# Version information
def get_version():
    """Return the current version of the geopandas_analysis package."""
    return __version__

def get_info():
    """Return basic package information."""
    return {
        'name': __title__,
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'email': __email__,
        'url': __url__,
        'license': __license__,
    }

# Development utilities
def list_functions():
    """List all available functions in the package."""
    if __all__:
        print(f"Available functions in {__title__} v{__version__}:")
        print("\n📊 Spatial Data Loading:")
        for func in __all__[:4]:
            print(f"  - {func}")
        print("\n📐 Geometric Operations:")
        for func in __all__[4:8]:
            print(f"  - {func}")
        print("\n🔗 Spatial Joins & Analysis:")
        for func in __all__[8:12]:
            print(f"  - {func}")
        print("\n🎨 Visualization & Mapping:")
        for func in __all__[12:]:
            print(f"  - {func}")
    else:
        print("No functions available yet. Implement the modules first!")

def check_dependencies():
    """Check if all required spatial analysis dependencies are available."""
    dependencies = {
        'geopandas': 'Core spatial data analysis',
        'pandas': 'Data manipulation and analysis',
        'numpy': 'Numerical computing',
        'shapely': 'Geometric operations',
        'fiona': 'Spatial data I/O',
        'pyproj': 'Coordinate reference system transformations',
        'matplotlib': 'Static plotting and visualization',
        'contextily': 'Web map tile basemaps',
        'folium': 'Interactive web mapping',
        'geodatasets': 'Sample spatial datasets',
    }

    print(f"Checking spatial analysis dependencies for {__title__} v{__version__}:\n")

    all_available = True
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"✅ {package:12} - {description}")
        except ImportError:
            print(f"❌ {package:12} - {description} (NOT AVAILABLE)")
            all_available = False

    if all_available:
        print(f"\n🎉 All spatial analysis dependencies are available!")
        print(f"You're ready to start your GeoPandas assignment!")
    else:
        print(f"\n⚠️  Some dependencies are missing.")
        print(f"Run: uv sync --all-extras --dev")

    return all_available

# Package initialization message
def _show_welcome():
    """Show welcome message when package is imported."""
    if __name__ != "__main__":  # Only show when imported, not when run directly
        print(f"🗺️  {__title__} v{__version__} loaded successfully!")
        print(f"📚 Use help(geopandas_analysis) or geopandas_analysis.list_functions() for available functions")

# Show welcome message on import (optional - can be commented out if annoying)
# _show_welcome()
