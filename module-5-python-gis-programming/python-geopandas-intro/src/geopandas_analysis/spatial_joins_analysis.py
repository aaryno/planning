"""
Spatial Joins & Analysis Module - Student Implementation
========================================================

Welcome to spatial relationships! This module teaches you how to combine
datasets based on their geographic relationships, not just shared attributes.

Think of this like asking geographic questions:
- Which schools are inside which neighborhoods?
- What's the population of areas within 1 mile of hospitals?
- Which roads cross through each county?
- What features overlap with environmental hazards?

This is where GIS really shines - answering questions that regular
databases can't handle because they're based on location!

What you'll learn:
- Spatial joins: combining data based on location
- Point-in-polygon analysis: finding what contains what
- Spatial aggregation: summarizing data by geographic areas
- Complex spatial filtering: multiple criteria at once
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Any, Optional
import warnings


def spatial_intersection_analysis(gdf1: gpd.GeoDataFrame,
                                gdf2: gpd.GeoDataFrame,
                                intersection_type: str = 'intersects') -> gpd.GeoDataFrame:
    """
    FIND OVERLAPPING FEATURES (Like finding which shapes touch or overlap on a map)

    Spatial intersection finds features that have some kind of spatial relationship:
    - intersects: features that touch or overlap in any way
    - contains: features from gdf1 that completely contain features from gdf2
    - within: features from gdf1 that are completely inside features from gdf2
    - overlaps: features that partially overlap (not just touching)

    Your Task: Perform spatial joins based on different intersection types.

    Args:
        gdf1: Source GeoDataFrame (left side of join)
        gdf2: Target GeoDataFrame (right side of join)
        intersection_type: Type of spatial relationship to find

    Returns:
        GeoDataFrame with joined results
    """

    if len(gdf1) == 0 or len(gdf2) == 0:
        return gdf1.copy()

    # STEP 1: Validate inputs and coordinate systems
    if gdf1.crs != gdf2.crs:
        if gdf2.crs is not None and gdf1.crs is not None:
            gdf2 = gdf2.to_crs(gdf1.crs)
            warnings.warn("gdf2 CRS transformed to match gdf1")

    # STEP 2: Perform spatial join based on intersection type
    try:
        # HINT: Use gpd.sjoin(gdf1, gdf2, how='left', predicate=intersection_type)
        result = gpd.sjoin(gdf1, gdf2, how='left', predicate=intersection_type)

        # Add metadata about the join
        result.attrs['spatial_join_type'] = intersection_type
        result.attrs['left_features'] = len(gdf1)
        result.attrs['right_features'] = len(gdf2)
        result.attrs['joined_features'] = len(result)

        return result

    except Exception as e:
        warnings.warn(f"Spatial intersection analysis failed: {str(e)}")
        return gdf1.copy()


def point_in_polygon_analysis(points_gdf: gpd.GeoDataFrame,
                            polygons_gdf: gpd.GeoDataFrame,
                            aggregate_function: str = 'count') -> gpd.GeoDataFrame:
    """
    FIND POINTS INSIDE POLYGONS (Like counting how many cities are in each state)

    This is one of the most common GIS operations:
    - Count points in each polygon (how many schools per district?)
    - Sum values of points in each polygon (total population per county?)
    - Find average values (mean income per neighborhood?)

    Your Task: Find points inside polygons and summarize them.

    Args:
        points_gdf: GeoDataFrame with point features
        polygons_gdf: GeoDataFrame with polygon features
        aggregate_function: How to summarize points ('count', 'sum', 'mean')

    Returns:
        Polygon GeoDataFrame with aggregated point information
    """

    if len(points_gdf) == 0 or len(polygons_gdf) == 0:
        result = polygons_gdf.copy()
        result['point_count'] = 0
        return result

    # STEP 1: Ensure compatible coordinate systems
    if points_gdf.crs != polygons_gdf.crs:
        if points_gdf.crs is not None and polygons_gdf.crs is not None:
            points_gdf = points_gdf.to_crs(polygons_gdf.crs)

    # STEP 2: Perform spatial join to find points within polygons
    try:
        # HINT: Use gpd.sjoin(points_gdf, polygons_gdf, predicate='within')
        joined = gpd.sjoin(points_gdf, polygons_gdf, predicate='within')

        # STEP 3: Aggregate points by polygon
        result = polygons_gdf.copy()

        if aggregate_function == 'count':
            # Count points in each polygon
            # HINT: Use joined.groupby('index_right').size()
            point_counts = joined.groupby('index_right').size()
            result['point_count'] = 0
            result.loc[point_counts.index, 'point_count'] = point_counts.values

        return result

    except Exception as e:
        warnings.warn(f"Point in polygon analysis failed: {str(e)}")
        result = polygons_gdf.copy()
        result['point_count'] = 0
        return result


def spatial_aggregation(gdf: gpd.GeoDataFrame,
                       aggregation_zones: gpd.GeoDataFrame,
                       value_column: str,
                       agg_functions: List[str] = None) -> gpd.GeoDataFrame:
    """
    SUMMARIZE DATA BY SPATIAL AREAS (Like calculating statistics for geographic regions)

    This function takes numeric data from one dataset and summarizes it
    based on spatial zones from another dataset.

    Your Task: Aggregate attribute values based on spatial containment.

    Args:
        gdf: Source data with values to aggregate
        aggregation_zones: Zones to aggregate within
        value_column: Column name with values to aggregate
        agg_functions: List of aggregation functions ('sum', 'mean', 'count', 'max', 'min')

    Returns:
        Aggregation zones with summary statistics
    """

    if agg_functions is None:
        agg_functions = ['count', 'sum', 'mean']

    if len(gdf) == 0 or len(aggregation_zones) == 0:
        return aggregation_zones.copy()

    try:
        # STEP 1: Spatial join to assign features to zones
        joined = gpd.sjoin(gdf, aggregation_zones, predicate='within')

        # STEP 2: Group by zone and calculate aggregations
        result = aggregation_zones.copy()

        if value_column in joined.columns:
            grouped = joined.groupby('index_right')[value_column]

            for func in agg_functions:
                if func == 'count':
                    result[f'{value_column}_count'] = grouped.size()
                elif func == 'sum':
                    result[f'{value_column}_sum'] = grouped.sum()
                elif func == 'mean':
                    result[f'{value_column}_mean'] = grouped.mean()
                elif func == 'max':
                    result[f'{value_column}_max'] = grouped.max()
                elif func == 'min':
                    result[f'{value_column}_min'] = grouped.min()

        return result.fillna(0)

    except Exception as e:
        warnings.warn(f"Spatial aggregation failed: {str(e)}")
        return aggregation_zones.copy()


def multi_criteria_spatial_filter(gdf: gpd.GeoDataFrame,
                                 spatial_filter_gdf: Optional[gpd.GeoDataFrame] = None,
                                 attribute_filters: Optional[Dict[str, Any]] = None,
                                 spatial_operation: str = 'intersects',
                                 combine_logic: str = 'AND') -> gpd.GeoDataFrame:
    """
    COMPLEX FILTERING (Like finding features that meet multiple criteria)

    Sometimes you need features that meet both spatial AND attribute criteria:
    - Schools within flood zones AND with enrollment > 500
    - Parks that intersect rivers AND have area > 10 acres
    - Buildings within city limits AND built after 2000

    Your Task: Apply multiple filters and combine them logically.

    Args:
        gdf: GeoDataFrame to filter
        spatial_filter_gdf: Optional spatial filter dataset
        attribute_filters: Dictionary of attribute filter conditions
        spatial_operation: Type of spatial filter ('intersects', 'within', etc.)
        combine_logic: How to combine filters ('AND', 'OR')

    Returns:
        Filtered GeoDataFrame meeting specified criteria
    """

    if len(gdf) == 0:
        return gdf.copy()

    result_mask = pd.Series([True] * len(gdf), index=gdf.index)

    # STEP 1: Apply spatial filter if provided
    if spatial_filter_gdf is not None and len(spatial_filter_gdf) > 0:
        try:
            # Find features that meet spatial criteria
            spatial_join = gpd.sjoin(gdf, spatial_filter_gdf, predicate=spatial_operation)
            spatial_mask = gdf.index.isin(spatial_join.index)
        except:
            spatial_mask = pd.Series([False] * len(gdf), index=gdf.index)
    else:
        spatial_mask = pd.Series([True] * len(gdf), index=gdf.index)

    # STEP 2: Apply attribute filters if provided
    if attribute_filters:
        attribute_mask = pd.Series([True] * len(gdf), index=gdf.index)

        for column, condition in attribute_filters.items():
            if column in gdf.columns:
                try:
                    if isinstance(condition, dict):
                        # Handle complex conditions like {'>=': 100}
                        for operator, value in condition.items():
                            if operator == '>=':
                                mask = gdf[column] >= value
                            elif operator == '<=':
                                mask = gdf[column] <= value
                            elif operator == '>':
                                mask = gdf[column] > value
                            elif operator == '<':
                                mask = gdf[column] < value
                            elif operator == '==':
                                mask = gdf[column] == value
                            elif operator == '!=':
                                mask = gdf[column] != value
                            else:
                                continue

                            attribute_mask = attribute_mask & mask
                    else:
                        # Simple equality condition
                        mask = gdf[column] == condition
                        attribute_mask = attribute_mask & mask

                except Exception as e:
                    warnings.warn(f"Could not apply filter for column {column}: {str(e)}")
    else:
        attribute_mask = pd.Series([True] * len(gdf), index=gdf.index)

    # STEP 3: Combine filters based on logic
    if combine_logic.upper() == 'AND':
        # HINT: Use & operator to combine boolean masks
        final_mask = spatial_mask & attribute_mask
    elif combine_logic.upper() == 'OR':
        # HINT: Use | operator to combine boolean masks
        final_mask = spatial_mask | attribute_mask
    else:
        final_mask = spatial_mask & attribute_mask  # Default to AND

    # STEP 4: Apply the final filter
    result = gdf[final_mask].copy()

    # Add metadata about filtering
    result.attrs['original_count'] = len(gdf)
    result.attrs['filtered_count'] = len(result)
    result.attrs['spatial_filter_applied'] = spatial_filter_gdf is not None
    result.attrs['attribute_filters_applied'] = attribute_filters is not None
    result.attrs['combine_logic'] = combine_logic

    return result


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def _validate_spatial_join_inputs(gdf1: gpd.GeoDataFrame, gdf2: gpd.GeoDataFrame) -> bool:
    """Helper function to validate inputs for spatial joins."""
    if len(gdf1) == 0 or len(gdf2) == 0:
        return False

    if gdf1.geometry.empty.all() or gdf2.geometry.empty.all():
        return False

    return True


# Common spatial predicates for different analysis types
SPATIAL_PREDICATES = {
    'touching': 'intersects',
    'inside': 'within',
    'contains': 'contains',
    'overlapping': 'overlaps',
    'crossing': 'crosses',
    'near': 'dwithin'
}

"""
CONGRATULATIONS! 🔗

You've completed the spatial joins and analysis module! You now know how to:
✅ Find overlapping and intersecting features
✅ Perform point-in-polygon analysis
✅ Aggregate data based on spatial relationships
✅ Apply complex multi-criteria spatial filters

These are the core skills for spatial data analysis!

Next Steps:
1. Test your functions in: notebooks/03_analysis_workflow.ipynb
2. Try different spatial join types and see the results
3. Practice combining spatial and attribute filters
4. Move on to visualization and mapping

Remember:
- Spatial joins are like database joins, but based on location
- Always check that your datasets have compatible coordinate systems
- Point-in-polygon is one of the most useful GIS operations
- Complex filters help you find exactly the features you need

Keep exploring spatial relationships! 🚀
"""
