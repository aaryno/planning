"""
GIST 604B - Python GeoPandas Analysis
Advanced Spatial Operations

This module contains functions for advanced spatial analysis operations:
- Geometric operations (buffers, measurements, transformations)
- Spatial joins and analysis workflows
- Professional mapping and visualization

Student: [Your Name]
Date: [Current Date]
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from pathlib import Path
from shapely.geometry import Point, Polygon, LineString, MultiPoint
from shapely.ops import unary_union
import warnings
from typing import Dict, List, Tuple, Union, Optional, Any

# ============================================================================
# MODULE 1: GEOMETRIC OPERATIONS
# ============================================================================

def calculate_geometric_properties(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """
    Calculate geometric properties of spatial features including area, perimeter,
    length, centroids, and bounding boxes.

    This function analyzes the geometric characteristics of spatial features,
    providing measurements and derived geometries useful for spatial analysis.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial dataset to analyze

    Returns:
        Dict[str, Any]: Dictionary containing geometric properties with keys:
            - 'areas': Series of area measurements (for polygons)
            - 'perimeters': Series of perimeter/length measurements
            - 'centroids': GeoSeries of centroid points
            - 'bounds': DataFrame of bounding boxes (minx, miny, maxx, maxy)
            - 'total_area': Total area of all features
            - 'geometry_types': Count of different geometry types
            - 'summary_stats': Basic statistics about measurements

    Example:
        >>> props = calculate_geometric_properties(watershed_gdf)
        >>> print(f"Total watershed area: {props['total_area']:,.2f} sq meters")
        >>> print(f"Average polygon area: {props['areas'].mean():,.2f} sq meters")

    TODO: Implement this function step by step:

    1. Initialize results dictionary
    2. Check the CRS and warn if using geographic coordinates:
       - Geographic CRS (like EPSG:4326) will give wrong area calculations
       - Suggest reprojecting to appropriate projected CRS for measurements
    3. Calculate areas for polygon geometries:
       - Use gdf.area for area calculations
       - Handle different geometry types (only polygons have meaningful areas)
       - Store areas in square meters/feet depending on CRS
    4. Calculate perimeters/lengths:
       - Use gdf.length for perimeter (polygons) or length (lines)
       - Handle points (which have zero length/perimeter)
    5. Generate centroids:
       - Use gdf.centroid to get geometric centers
       - Handle cases where centroid might fall outside polygon
    6. Calculate bounding boxes:
       - Use gdf.bounds to get rectangular extents
       - Include both individual and overall bounds
    7. Create summary statistics:
       - Min, max, mean, median for areas and perimeters
       - Count different geometry types present
    8. Calculate total measurements:
       - Sum of all areas (for polygons)
       - Total length of all linear features
    9. Return comprehensive results dictionary

    Geometry type handling:
    - Points: length=0, area=0, but still have centroids and bounds
    - Lines: length>0, area=0, centroids along the line
    - Polygons: both length (perimeter) and area, centroids inside/on polygon
    """
    # TODO: Implement calculate_geometric_properties function
    # Your implementation goes here
    pass


def create_spatial_buffers(gdf: gpd.GeoDataFrame,
                         distance: Union[float, List[float]],
                         unit: str = 'meters') -> gpd.GeoDataFrame:
    """
    Create buffer zones around spatial features with specified distances.

    This function generates buffer polygons around point, line, or polygon features,
    useful for proximity analysis, zone creation, and spatial influence modeling.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial dataset to buffer
        distance (Union[float, List[float]]): Buffer distance(s):
            - Single value: Same buffer distance for all features
            - List: Different buffer distance for each feature (must match feature count)
        unit (str): Distance unit ('meters', 'feet', 'kilometers', 'miles')
                   Default is 'meters'

    Returns:
        gpd.GeoDataFrame: Dataset with buffer geometries, preserving original attributes

    Raises:
        ValueError: If distance list length doesn't match feature count
        ValueError: If unit is not supported
        RuntimeError: If CRS is not suitable for buffering operations

    Example:
        >>> # Create 500m buffers around all cities
        >>> city_buffers = create_spatial_buffers(cities_gdf, 500, 'meters')
        >>>
        >>> # Create variable buffers based on population
        >>> distances = cities_gdf['population'] / 1000  # Larger cities get bigger buffers
        >>> pop_buffers = create_spatial_buffers(cities_gdf, distances.tolist(), 'meters')

    TODO: Implement this function step by step:

    1. Input validation:
       - Check that distance is positive number(s)
       - If distance is list, ensure length matches number of features
       - Validate that unit is supported
    2. Handle coordinate system requirements:
       - Check if CRS is projected (required for accurate buffering)
       - If geographic CRS, either reproject or warn about inaccuracy
       - Remember original CRS to transform back if needed
    3. Convert distance units if necessary:
       - Support meters, feet, kilometers, miles
       - Convert all distances to the CRS units (usually meters)
    4. Perform buffering operation:
       - Use gdf.buffer(distance) for single distance
       - Use gdf.geometry.buffer(distance_series) for variable distances
       - Handle negative distances (inward buffers for polygons)
    5. Handle buffer results:
       - Ensure resulting geometries are valid
       - Handle cases where buffer creates empty geometries
       - Preserve original attribute data
    6. Transform back to original CRS if projection was changed
    7. Return GeoDataFrame with buffer geometries

    Buffer considerations:
    - Points: Create circular buffers
    - Lines: Create corridor buffers (rounded ends)
    - Polygons: Expand or contract the boundary
    - Negative distances: Create inward buffers (erosion)
    """
    # TODO: Implement create_spatial_buffers function
    # Your implementation goes here
    pass


def perform_geometric_transformations(gdf: gpd.GeoDataFrame,
                                    operations: List[str]) -> Dict[str, gpd.GeoDataFrame]:
    """
    Apply geometric transformations to simplify or modify spatial features.

    This function performs various geometric operations to transform features
    for analysis, visualization, or data processing needs.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial dataset to transform
        operations (List[str]): List of operations to perform:
            - 'simplify': Simplify geometry to reduce coordinate complexity
            - 'convex_hull': Create convex hull around geometries
            - 'envelope': Create bounding box rectangles
            - 'centroid': Extract geometric centers as points

    Returns:
        Dict[str, gpd.GeoDataFrame]: Dictionary with operation names as keys
                                    and transformed GeoDataFrames as values

    Example:
        >>> transformations = perform_geometric_transformations(
        ...     complex_polygons_gdf,
        ...     ['simplify', 'convex_hull', 'centroid']
        ... )
        >>> simplified = transformations['simplify']
        >>> hulls = transformations['convex_hull']
        >>> centers = transformations['centroid']

    TODO: Implement this function step by step:

    1. Initialize results dictionary
    2. Validate input operations list:
       - Check that all operations are supported
       - Ensure operations list is not empty
    3. For each requested operation, create transformed version:

       a) 'simplify' operation:
          - Use gdf.simplify() to reduce coordinate complexity
          - Choose appropriate tolerance based on data extent
          - Preserve topology while reducing detail

       b) 'convex_hull' operation:
          - Use gdf.convex_hull to create minimal bounding polygons
          - Useful for generalizing complex shapes
          - Good for envelope/extent analysis

       c) 'envelope' operation:
          - Use gdf.envelope to create bounding boxes
          - Creates rectangular extents around features
          - Useful for spatial indexing and quick visualization

       d) 'centroid' operation:
          - Use gdf.centroid to extract geometric centers
          - Convert all geometries to representative points
          - Useful for point-based analysis of polygon/line data

    4. Preserve original attributes in all transformations
    5. Ensure CRS is maintained in all output datasets
    6. Handle edge cases (empty geometries, invalid results)
    7. Return dictionary of transformed datasets

    Transformation uses:
    - Simplify: Reduce file size, improve performance, web display
    - Convex hull: Generalize shapes, create simplified boundaries
    - Envelope: Quick spatial indexing, overview mapping
    - Centroid: Convert to points for analysis, label placement
    """
    # TODO: Implement perform_geometric_transformations function
    # Your implementation goes here
    pass


# ============================================================================
# MODULE 2: SPATIAL JOINS & ANALYSIS
# ============================================================================

def execute_spatial_intersection(gdf1: gpd.GeoDataFrame,
                               gdf2: gpd.GeoDataFrame,
                               operation: str = 'intersects') -> gpd.GeoDataFrame:
    """
    Find spatial relationships between two datasets using intersection operations.

    This function performs spatial joins to find features that intersect, are contained
    within, or have other spatial relationships with features in another dataset.

    Args:
        gdf1 (gpd.GeoDataFrame): Primary dataset (left side of join)
        gdf2 (gpd.GeoDataFrame): Secondary dataset (right side of join)
        operation (str): Spatial relationship to test:
            - 'intersects': Features that overlap or touch
            - 'within': Features from gdf1 completely inside gdf2 features
            - 'contains': Features from gdf1 that completely contain gdf2 features
            - 'crosses': Features that cross boundaries

    Returns:
        gpd.GeoDataFrame: Joined dataset with attributes from both inputs

    Example:
        >>> # Find cities within watersheds
        >>> cities_in_watersheds = execute_spatial_intersection(
        ...     cities_gdf, watersheds_gdf, operation='within'
        ... )
        >>> print(f"Found {len(cities_in_watersheds)} cities within watersheds")

    TODO: Implement this function step by step:

    1. Input validation:
       - Ensure both inputs are GeoDataFrames
       - Check that operation type is supported
       - Verify both datasets have valid geometry columns
    2. CRS compatibility:
       - Check if both datasets use the same CRS
       - If different, reproject gdf2 to match gdf1's CRS
       - Warn about any CRS transformations
    3. Perform spatial join based on operation:
       - Use gpd.sjoin() or gpd.overlay() depending on needs
       - 'intersects': Standard spatial join with intersects predicate
       - 'within': Find gdf1 features completely inside gdf2 features
       - 'contains': Find gdf1 features that contain gdf2 features
       - 'crosses': Find features that cross boundaries
    4. Handle join results:
       - Remove duplicate columns with same names
       - Rename columns to avoid conflicts (add suffixes)
       - Preserve geometry from appropriate dataset
    5. Clean up results:
       - Remove any invalid geometries
       - Handle cases with no spatial relationships found
       - Ensure consistent data types in result
    6. Return the spatially joined dataset

    Spatial relationship definitions:
    - Intersects: Any spatial overlap or touching
    - Within: Geometry A is completely inside geometry B
    - Contains: Geometry A completely contains geometry B
    - Crosses: Linear features cross polygon boundaries
    """
    # TODO: Implement execute_spatial_intersection function
    # Your implementation goes here
    pass


def aggregate_spatial_data(gdf: gpd.GeoDataFrame,
                         group_by: Union[str, gpd.GeoDataFrame],
                         agg_functions: Dict[str, str]) -> gpd.GeoDataFrame:
    """
    Aggregate spatial data by grouping features and summarizing attributes.

    This function groups spatial features and calculates summary statistics,
    useful for creating spatial summaries and regional analysis.

    Args:
        gdf (gpd.GeoDataFrame): Input dataset to aggregate
        group_by (Union[str, gpd.GeoDataFrame]): Grouping method:
            - str: Column name to group by (e.g., 'region', 'category')
            - gpd.GeoDataFrame: Spatial dataset to group by (spatial aggregation)
        agg_functions (Dict[str, str]): Aggregation functions for each column:
            - {'population': 'sum', 'income': 'mean', 'area': 'sum'}
            - Supported: 'sum', 'mean', 'count', 'min', 'max', 'std'

    Returns:
        gpd.GeoDataFrame: Aggregated dataset with summary statistics

    Example:
        >>> # Aggregate cities by state
        >>> state_summary = aggregate_spatial_data(
        ...     cities_gdf,
        ...     'state_name',
        ...     {'population': 'sum', 'elevation': 'mean'}
        ... )
        >>>
        >>> # Aggregate points by watershed polygons
        >>> watershed_summary = aggregate_spatial_data(
        ...     monitoring_points_gdf,
        ...     watersheds_gdf,
        ...     {'measurement': 'mean', 'count': 'count'}
        ... )

    TODO: Implement this function step by step:

    1. Input validation:
       - Check that agg_functions contains valid column names
       - Verify that aggregation functions are supported
       - Ensure group_by is either string or GeoDataFrame
    2. Handle different grouping methods:

       a) If group_by is string (attribute-based aggregation):
          - Check that column exists in gdf
          - Use pandas groupby on the specified column
          - Apply aggregation functions to numeric columns
          - Handle geometry aggregation (union of grouped features)

       b) If group_by is GeoDataFrame (spatial aggregation):
          - First perform spatial join to assign features to groups
          - Then aggregate based on spatial group membership
          - Preserve geometry from the grouping dataset

    3. Apply aggregation functions:
       - For each column in agg_functions, apply the specified function
       - Handle different data types appropriately
       - Calculate geometry aggregations (union, centroid, etc.)
    4. Handle geometry aggregation:
       - For polygon groups: union all geometries in group
       - For point groups: can create multipoint or convex hull
       - For mixed types: choose appropriate method
    5. Create result GeoDataFrame:
       - Include aggregated attributes
       - Include aggregated geometries
       - Preserve CRS from original dataset
    6. Clean and return results:
       - Remove any invalid aggregations
       - Ensure all geometries are valid
       - Sort results logically

    Aggregation strategies:
    - Attribute-based: Group by shared attribute values
    - Spatial-based: Group by spatial containment or intersection
    - Geometry handling: Union for areas, centroid/multipoint for points
    """
    # TODO: Implement aggregate_spatial_data function
    # Your implementation goes here
    pass


def filter_by_spatial_criteria(gdf: gpd.GeoDataFrame,
                             spatial_filters: Dict[str, Any],
                             attribute_filters: Optional[Dict[str, Any]] = None) -> gpd.GeoDataFrame:
    """
    Apply complex spatial and attribute filters to select features meeting multiple criteria.

    This function implements multi-criteria selection workflows common in GIS analysis,
    allowing selection based on spatial relationships, geometric properties, and attributes.

    Args:
        gdf (gpd.GeoDataFrame): Input dataset to filter
        spatial_filters (Dict[str, Any]): Spatial filter criteria:
            - 'min_area': Minimum area (for polygons)
            - 'max_area': Maximum area (for polygons)
            - 'within_bounds': [minx, miny, maxx, maxy] bounding box
            - 'intersects_geometry': Geometry to intersect with
            - 'buffer_distance': Distance for proximity filtering
        attribute_filters (Optional[Dict[str, Any]]): Attribute filter criteria:
            - {'population': {'min': 1000, 'max': 50000}}
            - {'category': {'values': ['urban', 'suburban']}}
            - {'date': {'after': '2020-01-01'}}

    Returns:
        gpd.GeoDataFrame: Filtered dataset meeting all criteria

    Example:
        >>> # Find medium-sized cities in specific region
        >>> filtered_cities = filter_by_spatial_criteria(
        ...     cities_gdf,
        ...     spatial_filters={
        ...         'within_bounds': [-120, 35, -115, 40],
        ...         'min_area': 1000
        ...     },
        ...     attribute_filters={
        ...         'population': {'min': 10000, 'max': 100000},
        ...         'state': {'values': ['CA', 'NV']}
        ...     }
        ... )

    TODO: Implement this function step by step:

    1. Input validation:
       - Check that spatial_filters contains valid criteria
       - Validate attribute_filters if provided
       - Ensure filter values are appropriate types
    2. Start with full dataset and apply filters progressively:
       - Create a copy to avoid modifying original data
       - Apply each filter and track how many features remain
    3. Apply spatial filters:

       a) Area-based filters (for polygons):
          - 'min_area': gdf[gdf.area >= min_area]
          - 'max_area': gdf[gdf.area <= max_area]
          - Handle units (ensure consistent units)

       b) Bounding box filter:
          - 'within_bounds': Use gdf.cx[minx:maxx, miny:maxy]
          - Or use bounds checking with gdf.bounds

       c) Geometry intersection filter:
          - 'intersects_geometry': Use gdf[gdf.intersects(geometry)]
          - Handle different geometry types appropriately

       d) Proximity/buffer filter:
          - 'buffer_distance': Create buffer around reference and intersect
          - Need reference geometry for this filter

    4. Apply attribute filters if provided:
       - For numeric ranges: df[df[col] >= min] & df[df[col] <= max]
       - For value lists: df[df[col].isin(values)]
       - For date ranges: Convert dates and apply range filters
       - Handle missing values appropriately
    5. Combine all filter results:
       - Apply filters progressively (AND logic)
       - Track filtering progress for debugging
       - Log how many features remain after each filter
    6. Validate and return results:
       - Ensure result is still a valid GeoDataFrame
       - Check that some features remain (warn if empty result)
       - Preserve original CRS and data types

    Filter types supported:
    - Spatial: area, bounds, intersection, proximity
    - Attribute: numeric ranges, categorical values, date ranges
    - Combination: All filters applied with AND logic
    """
    # TODO: Implement filter_by_spatial_criteria function
    # Your implementation goes here
    pass


# ============================================================================
# MODULE 3: MAPPING & VISUALIZATION
# ============================================================================

def create_static_choropleth_map(gdf: gpd.GeoDataFrame,
                               column: str,
                               title: str = "Choropleth Map",
                               color_scheme: str = 'viridis',
                               classification: str = 'quantiles') -> plt.Figure:
    """
    Create a professional static choropleth map with proper cartographic styling.

    This function generates publication-quality thematic maps with appropriate
    color schemes, classification methods, and cartographic elements.

    Args:
        gdf (gpd.GeoDataFrame): Input dataset with polygons to map
        column (str): Column name to visualize (must be numeric)
        title (str): Map title
        color_scheme (str): Color scheme ('viridis', 'plasma', 'Blues', 'Reds', 'RdYlBu')
        classification (str): Data classification method:
            - 'quantiles': Equal count in each class
            - 'equal_interval': Equal range in each class
            - 'natural_breaks': Jenks natural breaks
            - 'std_mean': Standard deviation from mean

    Returns:
        plt.Figure: Matplotlib figure object with the choropleth map

    Example:
        >>> # Create population density map
        >>> fig = create_static_choropleth_map(
        ...     counties_gdf,
        ...     'pop_density',
        ...     title='Population Density by County',
        ...     color_scheme='Reds',
        ...     classification='natural_breaks'
        ... )
        >>> plt.show()

    TODO: Implement this function step by step:

    1. Input validation:
       - Check that column exists and is numeric
       - Validate color scheme and classification method
       - Ensure gdf contains polygon geometries
    2. Data preparation:
       - Handle missing values in the mapped column
       - Calculate data ranges and statistics
       - Prepare data for classification
    3. Apply data classification:
       - 'quantiles': Use pd.qcut() for equal-count classes
       - 'equal_interval': Use pd.cut() for equal-range classes
       - 'natural_breaks': Implement Jenks breaks or use mapclassify
       - 'std_mean': Classes based on standard deviations from mean
    4. Set up the map:
       - Create figure with appropriate size
       - Set up coordinate system for mapping
       - Ensure CRS is appropriate for display (geographic preferred)
    5. Create the choropleth:
       - Use gdf.plot() with appropriate parameters
       - Apply color scheme and classification
       - Set edge colors and line widths
       - Handle missing data with separate color
    6. Add cartographic elements:
       - Title with proper formatting
       - Color bar legend with class labels
       - North arrow (if appropriate)
       - Scale bar (if appropriate)
       - Data source attribution
    7. Style the map:
       - Remove axis ticks and labels
       - Set appropriate margins
       - Use professional typography
       - Ensure good contrast and readability
    8. Return the completed figure

    Cartographic best practices:
    - Choose colors appropriate for data type (sequential, diverging, categorical)
    - Use proper classification methods for data distribution
    - Include clear, informative legends
    - Maintain good contrast and accessibility
    """
    # TODO: Implement create_static_choropleth_map function
    # Your implementation goes here
    pass


def generate_interactive_map(gdf: gpd.GeoDataFrame,
                           popup_columns: Optional[List[str]] = None,
                           base_map: str = 'OpenStreetMap',
                           marker_color: str = 'blue') -> folium.Map:
    """
    Create an interactive web map using Folium with multiple layers and controls.

    This function generates interactive maps suitable for web display with
    clickable features, popups, and layer controls.

    Args:
        gdf (gpd.GeoDataFrame): Input spatial dataset to map
        popup_columns (Optional[List[str]]): Columns to include in popups
                                          If None, includes all columns
        base_map (str): Base map style:
            - 'OpenStreetMap': Standard OSM tiles
            - 'Stamen Terrain': Terrain visualization
            - 'CartoDB positron': Light, clean base map
            - 'CartoDB dark_matter': Dark theme base map
        marker_color (str): Color for point markers ('red', 'blue', 'green', etc.)

    Returns:
        folium.Map: Interactive Folium map object

    Example:
        >>> # Create interactive city map with population info
        >>> interactive_map = generate_interactive_map(
        ...     cities_gdf,
        ...     popup_columns=['name', 'population', 'country'],
        ...     base_map='CartoDB positron',
        ...     marker_color='red'
        ... )
        >>> interactive_map.save('cities_map.html')

    TODO: Implement this function step by step:

    1. Input validation and preparation:
       - Ensure gdf has valid geometries
       - Check that popup_columns exist if specified
       - Validate base_map and marker_color options
    2. Coordinate system handling:
       - Convert to WGS84 (EPSG:4326) if not already
       - Web mapping requires geographic coordinates
       - Store original CRS if transformation needed
    3. Calculate map center and zoom:
       - Find the centroid of all features
       - Calculate appropriate zoom level based on data extent
       - Handle edge cases (single point, global data)
    4. Initialize the Folium map:
       - Create map centered on data
       - Set initial zoom level
       - Configure base map tile layer
    5. Prepare popup content:
       - If popup_columns specified, use only those columns
       - If None, use all non-geometry columns
       - Format popup content as HTML
       - Handle missing values and data types
    6. Add features to map based on geometry type:

       a) Point geometries:
          - Use folium.Marker() for individual points
          - Apply marker_color
          - Add popups with formatted content

       b) Polygon geometries:
          - Use folium.GeoJson() for polygons
          - Set style (fill, stroke, opacity)
          - Add popups with attribute information

       c) Line geometries:
          - Use folium.PolyLine() for lines
          - Set line style (color, weight, opacity)
          - Add popups with attribute information

    7. Add map controls and features:
       - Layer control if multiple layers
       - Zoom control
       - Fullscreen control (optional)
       - Scale display
    8. Optimize for performance:
       - For large datasets, consider clustering (MarkerCluster)
       - Use appropriate zoom levels
       - Limit popup content size
    9. Return the interactive map object

    Interactive features:
    - Clickable features with popup information
    - Pan and zoom controls
    - Layer switching capabilities
    - Responsive design for different screen sizes
    """
    # TODO: Implement generate_interactive_map function
    # Your implementation goes here
    pass


# ============================================================================
# HELPER FUNCTIONS (Optional - add as needed)
# ============================================================================

def _validate_crs_for_measurements(gdf: gpd.GeoDataFrame) -> bool:
    """
    Helper function to check if CRS is appropriate for distance/area measurements.

    Args:
        gdf (gpd.GeoDataFrame): Dataset to check

    Returns:
        bool: True if CRS is projected (good for measurements), False if geographic
    """
    # TODO: Optional helper function - implement if needed
    pass


def _format_popup_content(row: pd.Series, columns: List[str]) -> str:
    """
    Helper function to format popup content for interactive maps.

    Args:
        row (pd.Series): Feature attributes
        columns (List[str]): Columns to include in popup

    Returns:
        str: Formatted HTML content for popup
    """
    # TODO: Optional helper function - implement if needed
    pass


def _calculate_appropriate_tolerance(gdf: gpd.GeoDataFrame) -> float:
    """
    Helper function to calculate appropriate simplification tolerance.

    Args:
        gdf (gpd.GeoDataFrame): Dataset to analyze

    Returns:
        float: Suggested tolerance value for geometry simplification
    """
    # TODO: Optional helper function - implement if needed
    pass
