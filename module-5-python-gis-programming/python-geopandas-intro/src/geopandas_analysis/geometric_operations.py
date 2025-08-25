"""
Geometric Operations Module - Student Implementation
====================================================

Welcome to spatial geometry! This module teaches you how to measure, transform,
and analyze the geometric properties of spatial features.

Think of this as your "spatial calculator" - you'll learn to:
- Measure areas, distances, and perimeters (like using a ruler on a map)
- Create buffer zones around features (like drawing circles around points)
- Transform shapes (find centers, simplify complex shapes)
- Analyze spatial relationships (which features are closest to each other?)

IMPORTANT: Most geometric operations require projected coordinates (meters/feet),
not geographic coordinates (degrees). Always check your CRS!

What you'll learn:
- Calculating accurate spatial measurements (area, length, distance)
- Creating buffer zones for proximity analysis
- Transforming geometries for different purposes
- Finding spatial relationships between features
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Any, Optional
import warnings
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from shapely.ops import unary_union
from scipy.spatial import cKDTree
import math


def calculate_spatial_metrics(gdf: gpd.GeoDataFrame,
                            unit_conversion: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    CALCULATE SPATIAL MEASUREMENTS (Like using a ruler and calculator on your map)

    This function adds columns with spatial measurements to your data:
    - Area: How much space does each polygon cover? (in square units)
    - Length/Perimeter: How long are lines or polygon borders? (in linear units)
    - Distance from centroid: How far is each feature from the center of all data?

    CRITICAL: This only works properly with projected coordinate systems (meters/feet).
    If your data is in degrees (lat/lon), the measurements will be wrong!

    Think of it like this:
    - You can't measure a room accurately using latitude and longitude
    - You need to use feet or meters - that's what projected coordinates give you

    Your Task: Calculate spatial measurements and handle coordinate system issues.

    Args:
        gdf: GeoDataFrame with spatial features to measure
        unit_conversion: Optional conversion factor ('km2' for area, 'km' for length)

    Returns:
        GeoDataFrame with added columns for spatial measurements
    """

    # STEP 1: Input validation and setup
    if len(gdf) == 0:
        # Return empty dataframe with measurement columns
        result_gdf = gdf.copy()
        result_gdf['area_units2'] = pd.Series([], dtype=float)
        result_gdf['length_units'] = pd.Series([], dtype=float)
        result_gdf['centroid_distance'] = pd.Series([], dtype=float)
        return result_gdf

    # STEP 2: Check coordinate system and warn if necessary
    crs_warning = None
    if gdf.crs is None:
        crs_warning = "No CRS defined - measurements may be inaccurate"
        warnings.warn(crs_warning)
    elif gdf.crs.is_geographic:
        crs_warning = "Data is in geographic coordinates (degrees) - measurements will be inaccurate. Transform to projected CRS first."
        warnings.warn(crs_warning)

    # Make a copy to avoid modifying the original
    result_gdf = gdf.copy()

    # STEP 3: Calculate area for polygon features
    # Initialize area column with zeros
    result_gdf['area_units2'] = 0.0

    # Find polygon and multipolygon features
    # HINT: Use gdf.geometry.type to get geometry types
    # HINT: Check for 'Polygon' and 'MultiPolygon' types
    polygon_mask = gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])

    if polygon_mask.any():
        # Calculate area for polygon features
        # HINT: Use gdf.geometry.area to calculate areas
        result_gdf.loc[polygon_mask, 'area_units2'] = gdf.loc[polygon_mask].geometry.area

        # Apply unit conversion if requested
        if unit_conversion == 'km2':
            # Convert from square meters to square kilometers (divide by 1,000,000)
            # HINT: 1 km² = 1,000,000 m²
            result_gdf.loc[polygon_mask, 'area_units2'] = result_gdf.loc[polygon_mask, 'area_units2'] / 1_000_000
        elif unit_conversion == 'acres':
            # Convert from square meters to acres (divide by 4,047)
            # HINT: 1 acre = 4,047 m²
            result_gdf.loc[polygon_mask, 'area_units2'] = result_gdf.loc[polygon_mask, 'area_units2'] / 4047

    # STEP 4: Calculate length/perimeter for all geometry types
    result_gdf['length_units'] = 0.0

    # For points, length is 0 (already set)
    # For lines, calculate length
    # HINT: Use gdf.geometry.type to identify 'LineString' and 'MultiLineString'
    line_mask = gdf.geometry.type.isin(['LineString', 'MultiLineString'])
    if line_mask.any():
        # HINT: Use gdf.geometry.length to calculate line lengths
        result_gdf.loc[line_mask, 'length_units'] = gdf.loc[line_mask].geometry.length

    # For polygons, calculate perimeter (boundary length)
    if polygon_mask.any():
        # HINT: Use gdf.geometry.boundary.length to calculate perimeter
        result_gdf.loc[polygon_mask, 'length_units'] = gdf.loc[polygon_mask].geometry.boundary.length

    # Apply unit conversion to length measurements
    if unit_conversion == 'km':
        # Convert from meters to kilometers (divide by 1,000)
        result_gdf['length_units'] = result_gdf['length_units'] / 1000
    elif unit_conversion == 'miles':
        # Convert from meters to miles (divide by 1,609.34)
        result_gdf['length_units'] = result_gdf['length_units'] / 1609.34

    # STEP 5: Calculate distance from overall centroid
    try:
        # Find the centroid of all features combined
        # HINT: Use gdf.geometry.unary_union to combine all geometries
        # HINT: Then use .centroid to find the center point
        all_geom_union = gdf.geometry.unary_union
        overall_centroid = all_geom_union.centroid

        # Calculate distance from each feature's centroid to the overall centroid
        # HINT: Use gdf.geometry.centroid to get each feature's center
        # HINT: Use .distance() method to calculate distances
        feature_centroids = gdf.geometry.centroid
        distances = feature_centroids.distance(overall_centroid)

        result_gdf['centroid_distance'] = distances

        # Apply unit conversion to distances
        if unit_conversion == 'km':
            result_gdf['centroid_distance'] = result_gdf['centroid_distance'] / 1000
        elif unit_conversion == 'miles':
            result_gdf['centroid_distance'] = result_gdf['centroid_distance'] / 1609.34

    except Exception as e:
        # If centroid calculation fails, set distances to NaN
        result_gdf['centroid_distance'] = np.nan
        warnings.warn(f"Could not calculate centroid distances: {str(e)}")

    # STEP 6: Add metadata about the calculations
    result_gdf.attrs['measurement_crs'] = str(gdf.crs) if gdf.crs else 'None'
    result_gdf.attrs['unit_conversion'] = unit_conversion
    result_gdf.attrs['crs_warning'] = crs_warning

    return result_gdf


def create_buffers_and_zones(gdf: gpd.GeoDataFrame,
                           buffer_distances: Union[float, List[float]],
                           buffer_style: str = 'round') -> Dict[str, gpd.GeoDataFrame]:
    """
    CREATE BUFFER ZONES (Like drawing circles or zones around map features)

    Buffer zones are areas within a certain distance of features. Common uses:
    - Find all areas within 1 mile of schools
    - Create 500-meter safety zones around hazardous sites
    - Analyze what's within walking distance of bus stops

    Think of it like drawing circles with a compass around points on a map,
    or creating "zones of influence" around important features.

    Your Task: Create buffer zones at different distances with various styles.

    Args:
        gdf: GeoDataFrame with features to buffer
        buffer_distances: Distance(s) for buffer zones (in CRS units)
        buffer_style: 'round' (circular) or 'square' (rectangular) buffers

    Returns:
        Dictionary with different buffer zone GeoDataFrames
    """

    if len(gdf) == 0:
        return {'original': gdf, 'buffers': gpd.GeoDataFrame()}

    # STEP 1: Validate inputs and setup
    # Convert single distance to list for consistent processing
    if isinstance(buffer_distances, (int, float)):
        distances = [float(buffer_distances)]
    else:
        distances = [float(d) for d in buffer_distances]

    # Check for valid distances
    if any(d <= 0 for d in distances):
        raise ValueError("All buffer distances must be positive")

    # Check CRS - buffers need projected coordinates for accurate distances
    if gdf.crs is None:
        warnings.warn("No CRS defined - buffer distances may be inaccurate")
    elif gdf.crs.is_geographic:
        warnings.warn("Geographic CRS detected - buffer distances in degrees may not represent real-world distances")

    results = {'original': gdf.copy()}

    # STEP 2: Create buffers for each distance
    buffer_gdfs = []

    for distance in distances:
        # Make a copy for this distance
        buffer_gdf = gdf.copy()

        # STEP 3: Create the buffer geometries
        if buffer_style.lower() == 'round':
            # Create circular/round buffers
            # HINT: Use gdf.geometry.buffer(distance) to create round buffers
            buffer_geometries = gdf.geometry.buffer(distance)

        elif buffer_style.lower() == 'square':
            # Create square/rectangular buffers
            # HINT: Use gdf.geometry.buffer(distance, cap_style=3) for square buffers
            # cap_style=3 means square endcaps
            buffer_geometries = gdf.geometry.buffer(distance, cap_style=3)

        else:
            raise ValueError("buffer_style must be 'round' or 'square'")

        # Replace geometries with buffer geometries
        buffer_gdf.geometry = buffer_geometries

        # Add metadata about the buffer
        buffer_gdf['buffer_distance'] = distance
        buffer_gdf['buffer_style'] = buffer_style
        buffer_gdf['original_id'] = range(len(buffer_gdf))

        buffer_gdfs.append(buffer_gdf)

    # STEP 4: Combine all buffers into one GeoDataFrame
    if buffer_gdfs:
        combined_buffers = pd.concat(buffer_gdfs, ignore_index=True)
        results['buffers'] = gpd.GeoDataFrame(combined_buffers, crs=gdf.crs)

    # STEP 5: Create dissolved (merged) buffers for each distance
    # This combines overlapping buffers into single features
    dissolved_buffers = []

    for distance in distances:
        # Get buffers for this distance
        distance_buffers = results['buffers'][results['buffers']['buffer_distance'] == distance]

        if len(distance_buffers) > 0:
            try:
                # HINT: Use unary_union to combine overlapping geometries
                dissolved_geom = unary_union(distance_buffers.geometry.values)

                # Create new GeoDataFrame with dissolved geometry
                dissolved_gdf = gpd.GeoDataFrame(
                    {'buffer_distance': [distance],
                     'buffer_style': [buffer_style],
                     'feature_count': [len(distance_buffers)]},
                    geometry=[dissolved_geom],
                    crs=gdf.crs
                )
                dissolved_buffers.append(dissolved_gdf)

            except Exception as e:
                warnings.warn(f"Could not dissolve buffers for distance {distance}: {str(e)}")

    if dissolved_buffers:
        results['dissolved_buffers'] = pd.concat(dissolved_buffers, ignore_index=True)

    # STEP 6: Create buffer rings (donuts) - areas between different buffer distances
    if len(distances) > 1:
        # Sort distances to ensure proper ring creation
        sorted_distances = sorted(distances)
        rings = []

        for i in range(len(sorted_distances)):
            inner_distance = sorted_distances[i-1] if i > 0 else 0
            outer_distance = sorted_distances[i]

            # Create outer buffer
            outer_buffer = gdf.geometry.buffer(outer_distance)

            if inner_distance > 0:
                # Create inner buffer and subtract from outer
                inner_buffer = gdf.geometry.buffer(inner_distance)
                # HINT: Use .difference() to subtract inner from outer buffer
                ring_geom = outer_buffer.difference(inner_buffer)
            else:
                # First ring - just the buffer itself
                ring_geom = outer_buffer

            # Create ring GeoDataFrame
            ring_gdf = gdf.copy()
            ring_gdf.geometry = ring_geom
            ring_gdf['inner_distance'] = inner_distance
            ring_gdf['outer_distance'] = outer_distance
            ring_gdf['ring_width'] = outer_distance - inner_distance

            rings.append(ring_gdf)

        if rings:
            results['buffer_rings'] = pd.concat(rings, ignore_index=True)

    return results


def geometric_transformations(gdf: gpd.GeoDataFrame,
                            operations: List[str] = None) -> gpd.GeoDataFrame:
    """
    TRANSFORM GEOMETRIES (Like using different tools to modify shapes on a map)

    Sometimes you need to modify geometries for analysis or visualization:
    - Find centroids: Get the center point of complex shapes
    - Create convex hulls: Draw the smallest shape that contains all points
    - Simplify geometries: Remove unnecessary detail to make maps load faster
    - Create envelopes: Draw bounding boxes around features

    Think of this like having different tools in a graphics program - each
    transformation serves a different purpose for spatial analysis.

    Your Task: Apply various geometric transformations based on the operations list.

    Args:
        gdf: GeoDataFrame with geometries to transform
        operations: List of transformations to apply ['centroid', 'convex_hull', 'simplify', 'envelope']

    Returns:
        GeoDataFrame with additional columns containing transformed geometries
    """

    if len(gdf) == 0:
        return gdf.copy()

    # Set default operations if none provided
    if operations is None:
        operations = ['centroid', 'convex_hull', 'envelope']

    # Make a copy to avoid modifying original
    result_gdf = gdf.copy()

    # STEP 1: Create centroid points (center of each feature)
    if 'centroid' in operations:
        try:
            # HINT: Use gdf.geometry.centroid to get center points
            result_gdf['geometry_centroid'] = gdf.geometry.centroid

            # For points, centroid is the same as the original geometry
            # For lines, centroid is the center point along the line
            # For polygons, centroid is the center point inside the shape

        except Exception as e:
            warnings.warn(f"Could not calculate centroids: {str(e)}")
            result_gdf['geometry_centroid'] = None

    # STEP 2: Create convex hulls (smallest shape containing all vertices)
    if 'convex_hull' in operations:
        try:
            # HINT: Use gdf.geometry.convex_hull to create convex hulls
            result_gdf['geometry_convex_hull'] = gdf.geometry.convex_hull

            # Convex hull is like stretching a rubber band around the outside
            # of a shape - it creates the smallest convex polygon containing
            # all the points of the original shape

        except Exception as e:
            warnings.warn(f"Could not calculate convex hulls: {str(e)}")
            result_gdf['geometry_convex_hull'] = None

    # STEP 3: Create simplified geometries (remove unnecessary detail)
    if 'simplify' in operations:
        try:
            # Determine appropriate simplification tolerance based on data extent
            if gdf.crs and gdf.crs.is_geographic:
                # For geographic data, use degrees
                tolerance = 0.001  # About 100 meters at equator
            else:
                # For projected data, use distance in CRS units
                # Calculate tolerance as 0.1% of the data extent
                bounds = gdf.total_bounds
                extent = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
                tolerance = extent * 0.001  # 0.1% of extent

            # HINT: Use gdf.geometry.simplify(tolerance) to simplify shapes
            result_gdf['geometry_simplified'] = gdf.geometry.simplify(tolerance)

            # Simplification removes vertices that don't significantly change
            # the shape - useful for making complex polygons display faster

        except Exception as e:
            warnings.warn(f"Could not simplify geometries: {str(e)}")
            result_gdf['geometry_simplified'] = None

    # STEP 4: Create envelopes/bounding boxes (rectangular bounds)
    if 'envelope' in operations:
        try:
            # HINT: Use gdf.geometry.envelope to create bounding rectangles
            result_gdf['geometry_envelope'] = gdf.geometry.envelope

            # Envelope creates the smallest rectangle that completely
            # contains the original geometry - useful for quick spatial indexing

        except Exception as e:
            warnings.warn(f"Could not calculate envelopes: {str(e)}")
            result_gdf['geometry_envelope'] = None

    # STEP 5: Create oriented bounding boxes (rotated rectangles)
    if 'oriented_bbox' in operations:
        try:
            # This creates the smallest possible rectangle containing each geometry,
            # even if it's rotated relative to the coordinate axes
            oriented_boxes = []

            for geom in gdf.geometry:
                if geom is not None and not geom.is_empty:
                    try:
                        # Get the minimum rotated rectangle
                        # HINT: Use geom.minimum_rotated_rectangle for oriented bounding box
                        oriented_box = geom.minimum_rotated_rectangle
                        oriented_boxes.append(oriented_box)
                    except:
                        # Fallback to regular envelope if oriented box fails
                        oriented_boxes.append(geom.envelope)
                else:
                    oriented_boxes.append(None)

            result_gdf['geometry_oriented_bbox'] = oriented_boxes

        except Exception as e:
            warnings.warn(f"Could not calculate oriented bounding boxes: {str(e)}")
            result_gdf['geometry_oriented_bbox'] = None

    # STEP 6: Calculate transformation statistics
    stats = {}

    # Compare areas before and after simplification (for polygons)
    if 'simplify' in operations and 'geometry_simplified' in result_gdf.columns:
        polygon_mask = gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])
        if polygon_mask.any():
            original_areas = gdf.loc[polygon_mask].geometry.area
            simplified_areas = result_gdf.loc[polygon_mask, 'geometry_simplified'].area

            # Calculate area preservation percentage
            area_preservation = (simplified_areas / original_areas * 100).mean()
            stats['simplification_area_preservation_percent'] = round(area_preservation, 2)

    # Calculate how much space convex hulls add (for non-convex shapes)
    if 'convex_hull' in operations and 'geometry_convex_hull' in result_gdf.columns:
        polygon_mask = gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])
        if polygon_mask.any():
            original_areas = gdf.loc[polygon_mask].geometry.area
            hull_areas = result_gdf.loc[polygon_mask, 'geometry_convex_hull'].area

            # Calculate average area increase due to convex hull
            area_increase = ((hull_areas - original_areas) / original_areas * 100).mean()
            stats['convex_hull_area_increase_percent'] = round(area_increase, 2)

    # Store statistics in GeoDataFrame attributes
    result_gdf.attrs['transformation_stats'] = stats
    result_gdf.attrs['operations_applied'] = operations

    return result_gdf


def proximity_analysis(gdf: gpd.GeoDataFrame,
                      analysis_type: str = 'nearest_neighbor',
                      target_gdf: Optional[gpd.GeoDataFrame] = None,
                      max_distance: Optional[float] = None) -> Union[gpd.GeoDataFrame, Dict[str, Any]]:
    """
    ANALYZE SPATIAL PROXIMITY (Find what's close to what on your map)

    Proximity analysis helps answer questions like:
    - What's the closest hospital to each school?
    - How far is each house from the nearest park?
    - Which features are within 1000 meters of each other?
    - What's the average distance between similar features?

    Think of this like using a GPS to find "nearby" locations, but doing it
    systematically for lots of features at once.

    Your Task: Perform different types of proximity analysis.

    Args:
        gdf: Source GeoDataFrame (what we're measuring from)
        analysis_type: Type of analysis ('nearest_neighbor', 'distance_matrix', 'within_distance')
        target_gdf: Target GeoDataFrame (what we're measuring to). If None, use gdf itself
        max_distance: Maximum distance to consider (for filtering results)

    Returns:
        Results vary by analysis_type - either GeoDataFrame with distance info or dictionary with results
    """

    if len(gdf) == 0:
        return gdf.copy() if analysis_type != 'distance_matrix' else {'distances': np.array([]), 'ids': []}

    # STEP 1: Setup and validation
    # If no target provided, analyze within the same dataset
    if target_gdf is None:
        target_gdf = gdf.copy()
        self_analysis = True
    else:
        self_analysis = False

    # Check CRS compatibility
    if gdf.crs != target_gdf.crs:
        if target_gdf.crs is not None and gdf.crs is not None:
            # Transform target to match source CRS
            target_gdf = target_gdf.to_crs(gdf.crs)
            warnings.warn("Target GeoDataFrame CRS transformed to match source")

    # Warn about geographic coordinates
    if gdf.crs and gdf.crs.is_geographic:
        warnings.warn("Geographic coordinates detected - distances will be in degrees, not real-world units")

    # STEP 2: Nearest Neighbor Analysis
    if analysis_type == 'nearest_neighbor':
        result_gdf = gdf.copy()

        # Initialize result columns
        result_gdf['nearest_distance'] = np.nan
        result_gdf['nearest_target_id'] = -1

        try:
            # Get centroids for distance calculations
            # HINT: Use .geometry.centroid to get center points
            source_centroids = gdf.geometry.centroid
            target_centroids = target_gdf.geometry.centroid

            # Convert centroids to coordinate arrays for efficient processing
            source_coords = np.array([[geom.x, geom.y] for geom in source_centroids])
            target_coords = np.array([[geom.x, geom.y] for geom in target_centroids])

            # Use scipy's cKDTree for efficient nearest neighbor search
            # This is much faster than calculating all pairwise distances
            tree = cKDTree(target_coords)

            for i, source_coord in enumerate(source_coords):
                if self_analysis:
                    # For self-analysis, find the 2nd nearest (1st is itself)
                    # HINT: Use tree.query(point, k=2) to get 2 nearest neighbors
                    distances, indices = tree.query(source_coord, k=2)
                    nearest_dist = distances[1]  # Second closest (first is itself)
                    nearest_idx = indices[1]
                else:
                    # For different datasets, find the 1st nearest
                    # HINT: Use tree.query(point, k=1) to get nearest neighbor
                    distances, indices = tree.query(source_coord, k=1)
                    nearest_dist = distances if np.isscalar(distances) else distances[0]
                    nearest_idx = indices if np.isscalar(indices) else indices[0]

                # Store results
                result_gdf.iloc[i, result_gdf.columns.get_loc('nearest_distance')] = nearest_dist
                result_gdf.iloc[i, result_gdf.columns.get_loc('nearest_target_id')] = nearest_idx

                # Filter by max_distance if specified
                if max_distance is not None and nearest_dist > max_distance:
                    result_gdf.iloc[i, result_gdf.columns.get_loc('nearest_distance')] = np.nan
                    result_gdf.iloc[i, result_gdf.columns.get_loc('nearest_target_id')] = -1

        except Exception as e:
            warnings.warn(f"Nearest neighbor analysis failed: {str(e)}")

        return result_gdf

    # STEP 3: Distance Matrix Analysis
    elif analysis_type == 'distance_matrix':
        try:
            # Create a matrix of all pairwise distances
            source_centroids = gdf.geometry.centroid
            target_centroids = target_gdf.geometry.centroid

            # Initialize distance matrix
            n_source = len(gdf)
            n_target = len(target_gdf)
            distance_matrix = np.full((n_source, n_target), np.nan)

            # Calculate all pairwise distances
            for i, source_geom in enumerate(source_centroids):
                for j, target_geom in enumerate(target_centroids):
                    try:
                        # HINT: Use source_geom.distance(target_geom) to calculate distance
                        dist = source_geom.distance(target_geom)
                        distance_matrix[i, j] = dist
                    except:
                        distance_matrix[i, j] = np.nan

            # Filter by max_distance if specified
            if max_distance is not None:
                distance_matrix[distance_matrix > max_distance] = np.nan

            # Return results dictionary
            return {
                'distance_matrix': distance_matrix,
                'source_ids': list(range(len(gdf))),
                'target_ids': list(range(len(target_gdf))),
                'matrix_shape': distance_matrix.shape,
                'valid_distances': np.sum(~np.isnan(distance_matrix)),
                'mean_distance': np.nanmean(distance_matrix),
                'min_distance': np.nanmin(distance_matrix),
                'max_distance': np.nanmax(distance_matrix)
            }

        except Exception as e:
            warnings.warn(f"Distance matrix analysis failed: {str(e)}")
            return {'error': str(e)}

    # STEP 4: Within Distance Analysis
    elif analysis_type == 'within_distance':
        if max_distance is None:
            raise ValueError("max_distance must be specified for within_distance analysis")

        result_gdf = gdf.copy()
        result_gdf['neighbors_within_distance'] = 0
        result_gdf['neighbor_ids'] = None

        try:
            # Get centroids
            source_centroids = gdf.geometry.centroid
            target_centroids = target_gdf.geometry.centroid

            # For each source feature, count targets within max_distance
            for i, source_geom in enumerate(source_centroids):
                neighbors = []
                neighbor_count = 0

                for j, target_geom in enumerate(target_centroids):
                    if self_analysis and i == j:
                        continue  # Skip self in self-analysis

                    try:
                        dist = source_geom.distance(target_geom)
                        if dist <= max_distance:
                            neighbors.append(j)
                            neighbor_count += 1
                    except:
                        continue

                # Store results
                result_gdf.iloc[i, result_gdf.columns.get_loc('neighbors_within_distance')] = neighbor_count
                result_gdf.iloc[i, result_gdf.columns.get_loc('neighbor_ids')] = neighbors

        except Exception as e:
            warnings.warn(f"Within distance analysis failed: {str(e)}")

        return result_gdf

    else:
        raise ValueError(f"Unknown analysis_type: {analysis_type}. Must be 'nearest_neighbor', 'distance_matrix', or 'within_distance'")


# ==============================================================================
# HELPER FUNCTIONS AND UTILITIES
# ==============================================================================

def _calculate_polygon_compactness(geometry) -> float:
    """
    HELPER: Calculate how "round" or compact a polygon is
    (You don't need to implement this - it's already done!)
    """
    try:
        if geometry.geom_type not in ['Polygon', 'MultiPolygon']:
            return np.nan

        area = geometry.area
        perimeter = geometry.boundary.length

        if perimeter == 0:
            return 0

        # Polsby-Popper compactness: 4π × area / perimeter²
        # Perfect circle = 1.0, long thin shapes approach 0
        compactness = (4 * math.pi * area) / (perimeter ** 2)
        return min(compactness, 1.0)  # Cap at 1.0 for numerical stability

    except:
        return np.nan


def _estimate_appropriate_buffer_distance(gdf: gpd.GeoDataFrame) -> float:
    """
    HELPER: Estimate a reasonable buffer distance based on feature spacing
    (You don't need to implement this - it's already done!)
    """
    try:
        if len(gdf) < 2:
            return 1000  # Default 1000 units

        # Calculate average distance between feature centroids
        centroids = gdf.geometry.centroid
        coords = np.array([[geom.x, geom.y] for geom in centroids])

        # Use k-nearest neighbors to estimate typical spacing
        tree = cKDTree(coords)
        distances, _ = tree.query(coords, k=min(5, len(coords)))

        # Use mean of distances to 2nd through 5th nearest neighbors
        # (excluding distance to self which is 0)
        if distances.shape[1] > 1:
            mean_distance = np.mean(distances[:, 1:])
            return mean_distance * 0.1  # 10% of typical spacing
        else:
            return 1000

    except:
        return 1000


# ==============================================================================
# CONSTANTS AND REFERENCE DATA
# ==============================================================================

# Common buffer distances for different analysis types (in meters)
COMMON_BUFFER_DISTANCES = {
    'walkable': [400, 800],  # 5-10 minute walk
    'neighborhood': [1600, 3200],  # 0.5-1 mile radius
    'city_services': [8000, 16000],  # 5-10 mile radius
    'regional': [32000, 80000],  # 20-50 mile radius
}

# Unit conversion factors
UNIT_CONVERSIONS = {
    'meters_to_kilometers': 1000,
    'meters_to_miles': 1609.34,
    'meters_to_feet': 0.3048,
    'square_meters_to_square_kilometers': 1_000_000,
    'square_meters_to_acres': 4047,
    'square_meters_to_square_feet': 0.092903,
}

# Geometry simplification tolerances by scale
SIMPLIFICATION_TOLERANCES = {
    'high_detail': 0.0001,    # Very detailed - minimal simplification
    'medium_detail': 0.001,   # Moderate simplification
    'low_detail': 0.01,       # Heavy simplification for web display
    'overview': 0.1,          # Very generalized for small-scale maps
}

"""
CONGRATULATIONS! 📐

You've completed the geometric operations module! You now know how to:
✅ Calculate accurate spatial measurements (area, length, distance)
✅ Create buffer zones for proximity analysis
✅ Transform geometries (centroids, hulls, simplification)
✅ Perform proximity analysis (nearest neighbors, distance matrices)

These geometric skills are essential for spatial analysis!

Next Steps:
1. Test your functions in: notebooks/02_spatial_operations.ipynb
2. Try different buffer distances and see how they affect analysis
3. Experiment with geometry transformations
4. Move on to spatial joins and relationship analysis

Key Reminders:
- Always use projected coordinates (meters/feet) for accurate measurements
- Geographic coordinates (lat/lon) give measurements in degrees - not useful!
- Buffer analysis helps answer "what's within X distance" questions
- Proximity analysis finds spatial relationships between features
- Transform geometries to simplify complex shapes for better performance

Pro Tips:
- Visualize your results! Use .plot() to see buffers and transformed geometries
- Check your CRS before doing measurements - it makes all the difference
- Use appropriate buffer distances for your analysis scale
- Simplify geometries for web mapping to improve performance

Keep building your spatial analysis skills! 🚀
"""
