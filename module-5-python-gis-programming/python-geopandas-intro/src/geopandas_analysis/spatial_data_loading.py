"""
Spatial Data Loading Module - Student Implementation
=====================================================

Welcome to the world of spatial data! This module teaches you how to work with
geospatial datasets using GeoPandas - think of it as pandas for geographic data.

Don't worry if you're new to GIS - we'll guide you through each spatial concept!

IMPORTANT: Read all the comments carefully. They explain spatial concepts step-by-step.

What you'll learn:
- Loading spatial data from different file formats (Shapefiles, GeoJSON, etc.)
- Understanding coordinate reference systems (CRS) - like different map projections
- Checking data quality and fixing common spatial data problems
- Transforming data between different coordinate systems

Remember: Always visualize your spatial data! Use .plot() to see what your data looks like.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Union, Any, Optional
import warnings
from shapely.geometry import Point, LineString, Polygon
from shapely.validation import explain_validity
from pyproj import CRS


def load_spatial_dataset(file_path: Union[str, Path],
                        file_format: Optional[str] = None,
                        encoding: str = 'utf-8') -> gpd.GeoDataFrame:
    """
    LOAD SPATIAL DATA FROM FILES (Like opening a map in your GIS software)

    Spatial data comes in many formats - Shapefiles (.shp), GeoJSON (.geojson),
    GeoPackage (.gpkg), and more. This function loads them into a GeoDataFrame,
    which is like a pandas DataFrame but with a special 'geometry' column for shapes.

    Think of it like this:
    - Regular DataFrame: spreadsheet with rows and columns of data
    - GeoDataFrame: spreadsheet PLUS a column of shapes (points, lines, polygons)

    Example of what we're creating:
        name          population    geometry
        Phoenix       1600000      POLYGON((lon1 lat1, lon2 lat2, ...))
        Tucson        550000       POLYGON((lon3 lat3, lon4 lat4, ...))

    Your Task: Load spatial data and handle common file format issues.

    Args:
        file_path: Path to the spatial data file (like "data/cities.shp")
        file_format: Optional format hint ("shapefile", "geojson", "gpkg")
        encoding: Text encoding for attribute data (usually 'utf-8')

    Returns:
        A GeoDataFrame with spatial data loaded and ready for analysis
    """

    # STEP 1: Convert path to Path object and check if file exists
    # This makes file handling more reliable across different operating systems
    file_path = Path(file_path)

    # Check if the file actually exists - don't try to load missing files!
    # HINT: Use file_path.exists() to check if file is there
    # HINT: If file doesn't exist, raise FileNotFoundError with a helpful message

    if not file_path.exists():
        raise FileNotFoundError(f"Spatial data file not found: {file_path}")

    # STEP 2: Determine file format if not provided
    # Different spatial formats need different handling
    if file_format is None:
        # Get the file extension (like .shp, .geojson, .gpkg)
        # HINT: Use file_path.suffix to get the extension
        suffix = file_path.suffix.lower()

        # Map file extensions to format names
        format_mapping = {
            '.shp': 'shapefile',
            '.geojson': 'geojson',
            '.json': 'geojson',
            '.gpkg': 'gpkg',
            '.gdb': 'gdb',
            '.kml': 'kml',
            '.csv': 'csv'  # CSV with coordinate columns
        }

        # FILL IN: Get the format from the mapping, or default to 'unknown'
        # HINT: Use format_mapping.get(suffix, 'unknown')
        file_format = format_mapping.get(suffix, 'unknown')

    # STEP 3: Handle special cases before loading

    # Handle CSV files with coordinate columns (not true spatial format)
    if file_format == 'csv':
        try:
            # For CSV, we need to create geometry from coordinate columns
            # HINT: Use pd.read_csv() first, then convert to GeoDataFrame
            df = pd.read_csv(file_path, encoding=encoding)

            # Look for common coordinate column names
            # Common names: lon/lat, longitude/latitude, x/y, lng/lat
            coord_columns = []
            for lon_name in ['longitude', 'lon', 'lng', 'x']:
                for lat_name in ['latitude', 'lat', 'y']:
                    if lon_name in df.columns and lat_name in df.columns:
                        coord_columns = [lon_name, lat_name]
                        break
                if coord_columns:
                    break

            if not coord_columns:
                raise ValueError("CSV file must have coordinate columns (lon/lat, x/y, etc.)")

            # Create Point geometries from coordinates
            # HINT: Use gpd.points_from_xy(df[x_col], df[y_col]) to create points
            geometry = gpd.points_from_xy(df[coord_columns[0]], df[coord_columns[1]])

            # Create GeoDataFrame
            # HINT: Use gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
            # Note: We assume WGS84 (EPSG:4326) for CSV coordinates
            gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

        except Exception as e:
            raise ValueError(f"Could not load CSV as spatial data: {str(e)}")

    else:
        # STEP 4: Load other spatial formats using GeoPandas
        try:
            # This is the main loading step for most spatial formats
            # HINT: Use gpd.read_file(file_path, encoding=encoding)
            # The encoding parameter helps with international characters

            gdf = gpd.read_file(file_path, encoding=encoding)

        except Exception as e:
            # If loading fails, try common fixes

            # Try different encodings for text issues
            if 'encoding' in str(e).lower() or 'codec' in str(e).lower():
                for alt_encoding in ['latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        gdf = gpd.read_file(file_path, encoding=alt_encoding)
                        warnings.warn(f"Used {alt_encoding} encoding instead of {encoding}")
                        break
                    except:
                        continue
                else:
                    raise ValueError(f"Could not load file with any encoding: {str(e)}")
            else:
                raise ValueError(f"Could not load spatial data: {str(e)}")

    # STEP 5: Basic validation of loaded data

    # Check if we actually got a GeoDataFrame
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Loaded data is not a GeoDataFrame")

    # Check if there's a geometry column
    if gdf.geometry is None:
        raise ValueError("No geometry column found in spatial data")

    # Check if we got any data
    if len(gdf) == 0:
        warnings.warn("Loaded spatial dataset is empty")

    # STEP 6: Add some helpful metadata
    # Store information about where this data came from
    gdf.attrs['source_file'] = str(file_path)
    gdf.attrs['file_format'] = file_format
    gdf.attrs['loading_encoding'] = encoding

    return gdf


def explore_spatial_properties(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """
    EXPLORE SPATIAL DATA PROPERTIES (Like getting a "summary report" of your map)

    When you get a new spatial dataset, you need to understand what you're working with:
    - What coordinate system is it using? (Are coordinates in degrees or meters?)
    - What types of shapes does it contain? (Points, lines, or polygons?)
    - Where in the world is this data located?
    - How much area does it cover?

    Think of this like examining a paper map before using it - you check the scale,
    projection, and what area it covers.

    Your Task: Extract key spatial information that helps understand the dataset.

    Args:
        gdf: A GeoDataFrame to analyze

    Returns:
        A dictionary with comprehensive spatial information
    """

    # Initialize results dictionary
    properties = {}

    # STEP 1: Basic data information
    # HINT: Use len(gdf) to get number of features (rows)
    # HINT: Use len(gdf.columns) to get number of attribute columns

    properties['feature_count'] = len(gdf)
    properties['attribute_count'] = len(gdf.columns) - 1  # Subtract 1 for geometry column
    properties['column_names'] = list(gdf.columns)

    # STEP 2: Coordinate Reference System (CRS) information
    # The CRS tells us how to interpret coordinates - very important for spatial analysis!

    if gdf.crs is not None:
        # HINT: Use gdf.crs to get CRS information
        # HINT: Use gdf.crs.to_epsg() to get EPSG code (if available)
        properties['crs'] = str(gdf.crs)
        try:
            properties['epsg_code'] = gdf.crs.to_epsg()
        except:
            properties['epsg_code'] = None

        # Determine if CRS is geographic (degrees) or projected (meters/feet)
        # Geographic CRS use lat/lon in degrees
        # Projected CRS use x/y in linear units like meters
        properties['crs_type'] = 'geographic' if gdf.crs.is_geographic else 'projected'
        properties['crs_units'] = str(getattr(gdf.crs, 'axis_info', [{}])[0].get('unit_name', 'unknown'))
    else:
        properties['crs'] = None
        properties['epsg_code'] = None
        properties['crs_type'] = 'unknown'
        properties['crs_units'] = 'unknown'
        warnings.warn("Dataset has no coordinate reference system (CRS) defined!")

    # STEP 3: Geometry types and validity
    # Find out what types of shapes we're working with

    if len(gdf) > 0:
        # Get the types of geometries (Point, LineString, Polygon, etc.)
        # HINT: Use gdf.geometry.geom_type to get geometry types
        geom_types = gdf.geometry.geom_type.value_counts()
        properties['geometry_types'] = geom_types.to_dict()

        # Find the most common geometry type
        properties['primary_geometry_type'] = geom_types.index[0] if len(geom_types) > 0 else 'None'

        # Check for invalid geometries (shapes that don't make geometric sense)
        # HINT: Use gdf.geometry.is_valid to check validity
        valid_geometries = gdf.geometry.is_valid
        properties['valid_geometries'] = valid_geometries.sum()
        properties['invalid_geometries'] = len(gdf) - valid_geometries.sum()
        properties['percent_valid'] = round((valid_geometries.sum() / len(gdf)) * 100, 2)

        # Check for empty/null geometries
        # HINT: Use gdf.geometry.is_empty and gdf.geometry.isna()
        properties['empty_geometries'] = gdf.geometry.is_empty.sum()
        properties['null_geometries'] = gdf.geometry.isna().sum()

    else:
        # Handle empty datasets
        properties['geometry_types'] = {}
        properties['primary_geometry_type'] = 'None'
        properties['valid_geometries'] = 0
        properties['invalid_geometries'] = 0
        properties['percent_valid'] = 0.0
        properties['empty_geometries'] = 0
        properties['null_geometries'] = 0

    # STEP 4: Spatial extent (bounding box)
    # This tells us the geographic area covered by the data

    if len(gdf) > 0 and not gdf.geometry.empty.all():
        # Get the total bounds (extent) of all geometries
        # HINT: Use gdf.total_bounds to get [minx, miny, maxx, maxy]
        total_bounds = gdf.total_bounds

        properties['spatial_extent'] = {
            'min_x': float(total_bounds[0]),
            'min_y': float(total_bounds[1]),
            'max_x': float(total_bounds[2]),
            'max_y': float(total_bounds[3])
        }

        # Calculate the width and height of the extent
        properties['extent_width'] = float(total_bounds[2] - total_bounds[0])
        properties['extent_height'] = float(total_bounds[3] - total_bounds[1])

        # Estimate the "center" of the data
        properties['centroid'] = {
            'x': float((total_bounds[0] + total_bounds[2]) / 2),
            'y': float((total_bounds[1] + total_bounds[3]) / 2)
        }

    else:
        properties['spatial_extent'] = None
        properties['extent_width'] = 0.0
        properties['extent_height'] = 0.0
        properties['centroid'] = {'x': 0.0, 'y': 0.0}

    # STEP 5: Attribute data analysis
    # Look at the non-spatial columns to understand the data better

    properties['attribute_summary'] = {}

    # Analyze each non-geometry column
    for column in gdf.columns:
        if column != gdf.geometry.name:  # Skip the geometry column
            col_data = gdf[column]

            # Basic statistics for this column
            col_info = {
                'data_type': str(col_data.dtype),
                'null_count': col_data.isna().sum(),
                'unique_count': col_data.nunique(),
                'null_percentage': round((col_data.isna().sum() / len(gdf)) * 100, 2)
            }

            # Add specific statistics based on data type
            if pd.api.types.is_numeric_dtype(col_data):
                # For numeric columns, add min/max/mean
                col_info.update({
                    'min_value': float(col_data.min()) if not col_data.empty else None,
                    'max_value': float(col_data.max()) if not col_data.empty else None,
                    'mean_value': float(col_data.mean()) if not col_data.empty else None
                })
            elif pd.api.types.is_string_dtype(col_data) or col_data.dtype == 'object':
                # For text columns, add most common values
                if not col_data.empty:
                    value_counts = col_data.value_counts().head(3)
                    col_info['most_common'] = value_counts.to_dict()

            properties['attribute_summary'][column] = col_info

    # STEP 6: Add metadata if available
    # Check if there's additional information stored with the dataset
    properties['metadata'] = getattr(gdf, 'attrs', {})

    return properties


def validate_spatial_data(gdf: gpd.GeoDataFrame, fix_issues: bool = True) -> Tuple[gpd.GeoDataFrame, Dict[str, Any]]:
    """
    VALIDATE AND FIX SPATIAL DATA ISSUES (Like spell-checking for maps)

    Spatial data can have problems that cause analysis to fail:
    - Invalid geometries: shapes that don't make mathematical sense
    - Missing coordinate systems: we don't know where on Earth the data is
    - Duplicate features: the same place appears multiple times
    - Empty geometries: features with no actual shape

    Think of this like checking a paper map for errors - torn sections, missing legends,
    or unclear symbols that need to be fixed before you can use the map.

    Your Task: Find spatial data problems and optionally fix them.

    Args:
        gdf: GeoDataFrame to validate
        fix_issues: If True, attempt to fix problems automatically

    Returns:
        - Fixed GeoDataFrame (if fix_issues=True) or original (if False)
        - Report dictionary describing issues found and fixes applied
    """

    # Initialize validation report
    validation_report = {
        'original_feature_count': len(gdf),
        'issues_found': [],
        'fixes_applied': [],
        'final_feature_count': None,
        'validation_successful': True
    }

    # Work with a copy so we don't modify the original unless fixing
    working_gdf = gdf.copy() if fix_issues else gdf

    # STEP 1: Check for missing coordinate reference system
    if working_gdf.crs is None:
        issue = "Missing coordinate reference system (CRS)"
        validation_report['issues_found'].append(issue)

        if fix_issues:
            # Try to guess CRS based on coordinate values
            # If coordinates are roughly -180 to 180 and -90 to 90, likely WGS84
            if len(working_gdf) > 0:
                bounds = working_gdf.total_bounds
                if (-180 <= bounds[0] <= 180 and -180 <= bounds[2] <= 180 and
                    -90 <= bounds[1] <= 90 and -90 <= bounds[3] <= 90):
                    # HINT: Set CRS to WGS84 using working_gdf.set_crs('EPSG:4326', inplace=True)
                    working_gdf.set_crs('EPSG:4326', inplace=True)
                    validation_report['fixes_applied'].append("Set CRS to WGS84 (EPSG:4326) based on coordinate range")
                else:
                    validation_report['fixes_applied'].append("Could not automatically determine CRS - manual intervention needed")

    # STEP 2: Check for invalid geometries
    if len(working_gdf) > 0:
        # HINT: Use working_gdf.geometry.is_valid to find invalid geometries
        invalid_mask = ~working_gdf.geometry.is_valid
        invalid_count = invalid_mask.sum()

        if invalid_count > 0:
            issue = f"Found {invalid_count} invalid geometries"
            validation_report['issues_found'].append(issue)

            if fix_issues:
                # Try to fix invalid geometries using buffer(0) trick
                # This often fixes self-intersecting polygons and other issues
                try:
                    # HINT: Use working_gdf.loc[invalid_mask, 'geometry'] = working_gdf.loc[invalid_mask, 'geometry'].buffer(0)
                    working_gdf.loc[invalid_mask, 'geometry'] = working_gdf.loc[invalid_mask, 'geometry'].buffer(0)

                    # Check how many we fixed
                    still_invalid = ~working_gdf.geometry.is_valid
                    fixed_count = invalid_count - still_invalid.sum()

                    if fixed_count > 0:
                        validation_report['fixes_applied'].append(f"Fixed {fixed_count} invalid geometries using buffer(0)")

                    if still_invalid.sum() > 0:
                        validation_report['fixes_applied'].append(f"{still_invalid.sum()} geometries could not be automatically fixed")

                except Exception as e:
                    validation_report['fixes_applied'].append(f"Could not fix invalid geometries: {str(e)}")

    # STEP 3: Check for empty/null geometries
    if len(working_gdf) > 0:
        # Check for null geometries (missing geometry data)
        # HINT: Use working_gdf.geometry.isna() to find null geometries
        null_mask = working_gdf.geometry.isna()
        null_count = null_mask.sum()

        # Check for empty geometries (geometries with no actual shape)
        # HINT: Use working_gdf.geometry.is_empty to find empty geometries
        empty_mask = working_gdf.geometry.is_empty
        empty_count = empty_mask.sum()

        if null_count > 0:
            issue = f"Found {null_count} features with null/missing geometries"
            validation_report['issues_found'].append(issue)

        if empty_count > 0:
            issue = f"Found {empty_count} features with empty geometries"
            validation_report['issues_found'].append(issue)

        if fix_issues and (null_count > 0 or empty_count > 0):
            # Remove features with null or empty geometries
            # HINT: Use ~(null_mask | empty_mask) to keep only valid geometries
            removal_mask = null_mask | empty_mask
            working_gdf = working_gdf[~removal_mask].copy()

            removed_count = removal_mask.sum()
            if removed_count > 0:
                validation_report['fixes_applied'].append(f"Removed {removed_count} features with null or empty geometries")

    # STEP 4: Check for duplicate geometries
    if len(working_gdf) > 1:
        # Find features with identical geometries
        # This is computationally expensive, so we use a simple approach
        try:
            # Convert geometries to well-known text (WKT) for comparison
            # HINT: Use working_gdf.geometry.to_wkt() to convert to text
            geometry_wkt = working_gdf.geometry.to_wkt()
            duplicate_geoms = geometry_wkt.duplicated()
            duplicate_count = duplicate_geoms.sum()

            if duplicate_count > 0:
                issue = f"Found {duplicate_count} features with duplicate geometries"
                validation_report['issues_found'].append(issue)

                if fix_issues:
                    # Remove duplicate geometries, keeping the first occurrence
                    # HINT: Use working_gdf[~duplicate_geoms] to remove duplicates
                    working_gdf = working_gdf[~duplicate_geoms].copy()
                    validation_report['fixes_applied'].append(f"Removed {duplicate_count} duplicate geometries")

        except Exception as e:
            validation_report['issues_found'].append(f"Could not check for duplicate geometries: {str(e)}")

    # STEP 5: Check coordinate ranges for reasonableness
    if len(working_gdf) > 0:
        bounds = working_gdf.total_bounds

        # Check for extremely large coordinates that might indicate CRS issues
        max_coord = max(abs(bounds[0]), abs(bounds[1]), abs(bounds[2]), abs(bounds[3]))

        if working_gdf.crs and working_gdf.crs.is_geographic:
            # For geographic CRS, coordinates should be within reasonable lat/lon ranges
            if bounds[0] < -180 or bounds[2] > 180 or bounds[1] < -90 or bounds[3] > 90:
                issue = "Coordinates outside valid geographic range (-180 to 180, -90 to 90)"
                validation_report['issues_found'].append(issue)

        elif max_coord > 1e8:  # 100 million - unreasonably large for most projected coordinates
            issue = f"Extremely large coordinate values (max: {max_coord:,.0f}) - possible CRS issue"
            validation_report['issues_found'].append(issue)

    # STEP 6: Final validation summary
    validation_report['final_feature_count'] = len(working_gdf)
    features_removed = validation_report['original_feature_count'] - validation_report['final_feature_count']

    if features_removed > 0:
        validation_report['fixes_applied'].append(f"Total features removed during validation: {features_removed}")

    # Determine if validation was successful
    critical_issues = [issue for issue in validation_report['issues_found']
                      if any(critical in issue.lower() for critical in ['invalid', 'null', 'missing crs'])]

    if critical_issues and not fix_issues:
        validation_report['validation_successful'] = False
    elif critical_issues and fix_issues and not validation_report['fixes_applied']:
        validation_report['validation_successful'] = False

    return working_gdf, validation_report


def standardize_crs(gdf: gpd.GeoDataFrame,
                   target_crs: Optional[Union[str, int]] = None,
                   auto_select: bool = True) -> Tuple[gpd.GeoDataFrame, Dict[str, Any]]:
    """
    STANDARDIZE COORDINATE REFERENCE SYSTEM (Like converting between different map projections)

    Different spatial datasets often use different coordinate systems:
    - Some use latitude/longitude in degrees (like GPS coordinates)
    - Others use projected coordinates in meters or feet (like state plane coordinates)
    - For analysis, we often need all datasets in the same coordinate system

    Think of this like converting between different measurement systems - you can't
    add meters and feet directly, so you need to convert everything to the same units.

    Common coordinate systems:
    - EPSG:4326 (WGS84): Worldwide latitude/longitude in degrees
    - EPSG:3857 (Web Mercator): Web mapping standard, meters
    - EPSG:2223 (Arizona Central): Arizona State Plane in feet

    Your Task: Transform spatial data to a standard coordinate system.

    Args:
        gdf: GeoDataFrame to transform
        target_crs: Desired coordinate system (EPSG code or CRS string)
        auto_select: If True, automatically choose appropriate CRS based on data location

    Returns:
        - Transformed GeoDataFrame
        - Transformation report with details about the operation
    """

    # Initialize transformation report
    transform_report = {
        'original_crs': str(gdf.crs) if gdf.crs else None,
        'original_epsg': None,
        'target_crs': None,
        'target_epsg': None,
        'transformation_applied': False,
        'auto_selection_used': False,
        'warnings': [],
        'coordinate_shift_stats': {}
    }

    # STEP 1: Handle missing CRS in source data
    if gdf.crs is None:
        transform_report['warnings'].append("Source data has no CRS defined - assuming WGS84")
        # HINT: Use gdf.set_crs('EPSG:4326', inplace=True) to set WGS84
        gdf = gdf.copy()
        gdf.set_crs('EPSG:4326', inplace=True)

    # Get original CRS information
    try:
        if gdf.crs is not None:
            transform_report['original_epsg'] = gdf.crs.to_epsg()
        else:
            transform_report['original_epsg'] = None
    except:
        transform_report['original_epsg'] = None

    # STEP 2: Auto-select target CRS if requested
    if auto_select and target_crs is None:
        transform_report['auto_selection_used'] = True

        # Get the center coordinates of the data
        if len(gdf) > 0:
            bounds = gdf.total_bounds
            center_lon = (bounds[0] + bounds[2]) / 2
            center_lat = (bounds[1] + bounds[3]) / 2

            # Auto-select based on geographic location and current CRS
            if gdf.crs.is_geographic:
                # For geographic data, choose projected CRS based on location

                # US-specific projections
                if -125 <= center_lon <= -66 and 20 <= center_lat <= 50:
                    # Continental US - use appropriate State Plane or UTM
                    if -114 <= center_lon <= -109 and 31 <= center_lat <= 37:
                        # Arizona area - use Arizona Central State Plane
                        target_crs = 'EPSG:2223'  # Arizona Central (US Feet)
                    elif -180 <= center_lon <= -120:
                        # Western US - use appropriate UTM zone
                        utm_zone = int((center_lon + 180) / 6) + 1
                        target_crs = f'EPSG:{32600 + utm_zone}'  # UTM North
                    else:
                        # Default to Web Mercator for web mapping
                        target_crs = 'EPSG:3857'
                else:
                    # Outside US - use Web Mercator as safe default
                    target_crs = 'EPSG:3857'
            else:
                # Already projected - may want to standardize to Web Mercator
                if gdf.crs.to_epsg() not in [3857, 4326]:
                    target_crs = 'EPSG:3857'
                else:
                    # Already in a standard CRS
                    target_crs = str(gdf.crs)

        else:
            # Empty dataset - use Web Mercator as default
            target_crs = 'EPSG:3857'

    # STEP 3: Set default target if still None
    if target_crs is None:
        target_crs = 'EPSG:4326'  # Default to WGS84

    # STEP 4: Check if transformation is needed
    try:
        target_crs_obj = CRS.from_user_input(target_crs)
        transform_report['target_crs'] = str(target_crs_obj)
        transform_report['target_epsg'] = target_crs_obj.to_epsg()

        # Check if transformation is actually needed
        if gdf.crs == target_crs_obj:
            transform_report['transformation_applied'] = False
            transform_report['warnings'].append("Source and target CRS are the same - no transformation needed")
            return gdf, transform_report

    except Exception as e:
        raise ValueError(f"Invalid target CRS '{target_crs}': {str(e)}")

    # STEP 5: Perform the transformation
    try:
        # Store original bounds for comparison
        if len(gdf) > 0:
            original_bounds = gdf.total_bounds
        else:
            original_bounds = None

        # HINT: Use gdf.to_crs(target_crs) to transform coordinates
        transformed_gdf = gdf.to_crs(target_crs)

        # STEP 6: Calculate transformation statistics
        if len(transformed_gdf) > 0 and original_bounds is not None:
            new_bounds = transformed_gdf.total_bounds

            # Calculate the shift in coordinate values
            transform_report['coordinate_shift_stats'] = {
                'original_bounds': {
                    'minx': float(original_bounds[0]),
                    'miny': float(original_bounds[1]),
                    'maxx': float(original_bounds[2]),
                    'maxy': float(original_bounds[3])
                },
                'transformed_bounds': {
                    'minx': float(new_bounds[0]),
                    'miny': float(new_bounds[1]),
                    'maxx': float(new_bounds[2]),
                    'maxy': float(new_bounds[3])
                },
                'coordinate_magnitude_change': {
                    'x_factor': abs(new_bounds[0] / original_bounds[0]) if original_bounds[0] != 0 else float('inf'),
                    'y_factor': abs(new_bounds[1] / original_bounds[1]) if original_bounds[1] != 0 else float('inf')
                }
            }

        transform_report['transformation_applied'] = True

        return transformed_gdf, transform_report

    except Exception as e:
        raise ValueError(f"Coordinate transformation failed: {str(e)}")


# ==============================================================================
# HELPER FUNCTIONS AND CONSTANTS
# ==============================================================================

def _detect_csv_coordinate_columns(df: pd.DataFrame) -> Optional[List[str]]:
    """
    HELPER: Detect coordinate columns in CSV files
    (You don't need to implement this - it's already done!)
    """
    # Common coordinate column name patterns
    longitude_patterns = ['longitude', 'lon', 'lng', 'long', 'x', 'easting']
    latitude_patterns = ['latitude', 'lat', 'y', 'northing']

    # Find matching columns
    lon_col = None
    lat_col = None

    for col in df.columns:
        col_lower = col.lower().strip()
        if not lon_col and any(pattern in col_lower for pattern in longitude_patterns):
            lon_col = col
        if not lat_col and any(pattern in col_lower for pattern in latitude_patterns):
            lat_col = col

    return [lon_col, lat_col] if (lon_col and lat_col) else None


def _validate_coordinate_ranges(gdf: gpd.GeoDataFrame) -> List[str]:
    """
    HELPER: Validate that coordinates are within reasonable ranges
    (You don't need to implement this - it's already done!)
    """
    warnings_list = []

    if len(gdf) == 0:
        return warnings_list

    bounds = gdf.total_bounds

    # Check based on CRS type
    if gdf.crs and gdf.crs.is_geographic:
        # Geographic coordinates should be within world bounds
        if bounds[0] < -180 or bounds[2] > 180:
            warnings_list.append(f"Longitude values outside valid range: {bounds[0]:.2f} to {bounds[2]:.2f}")

        if bounds[1] < -90 or bounds[3] > 90:
            warnings_list.append(f"Latitude values outside valid range: {bounds[1]:.2f} to {bounds[3]:.2f}")

    else:
        # Projected coordinates - check for unreasonably large values
        max_coord = max(abs(bounds[0]), abs(bounds[1]), abs(bounds[2]), abs(bounds[3]))
        if max_coord > 50_000_000:  # 50 million units is very large for most projections
            warnings_list.append(f"Very large coordinate values detected (max: {max_coord:,.0f}) - check CRS")

    return warnings_list


# ==============================================================================
# CONSTANTS AND REFERENCE DATA
# ==============================================================================

# Common spatial file formats and their characteristics
SPATIAL_FORMATS = {
    'shapefile': {
        'extensions': ['.shp'],
        'description': 'ESRI Shapefile - most common GIS format',
        'multi_file': True,  # Requires .shp, .shx, .dbf files
        'supports_crs': True
    },
    'geojson': {
        'extensions': ['.geojson', '.json'],
        'description': 'GeoJSON - web-friendly spatial format',
        'multi_file': False,
        'supports_crs': True
    },
    'gpkg': {
        'extensions': ['.gpkg'],
        'description': 'GeoPackage - modern spatial database format',
        'multi_file': False,
        'supports_crs': True
    },
    'kml': {
        'extensions': ['.kml'],
        'description': 'KML - Google Earth format',
        'multi_file': False,
        'supports_crs': False  # Always WGS84
    }
}

# Common coordinate reference systems for different regions
REGIONAL_CRS = {
    'arizona': {
        'epsg_codes': [2223, 2224, 2225],  # Arizona Central, East, West
        'description': 'Arizona State Plane Coordinate Systems',
        'units': 'feet'
    },
    'web_mapping': {
        'epsg_codes': [3857],
        'description': 'Web Mercator - standard for web maps',
        'units': 'meters'
    },
    'global': {
        'epsg_codes': [4326],
        'description': 'WGS84 Geographic - GPS coordinates',
        'units': 'degrees'
    }
}

"""
CONGRATULATIONS! 🗺️

You've completed the spatial data loading module! You now know how to:
✅ Load spatial data from different file formats (Shapefiles, GeoJSON, CSV, etc.)
✅ Explore spatial properties like CRS, geometry types, and data extent
✅ Validate spatial data and fix common issues automatically
✅ Transform data between different coordinate reference systems

These are fundamental skills for any GIS programmer!

Next Steps:
1. Test your functions in the Jupyter notebook: notebooks/01_data_exploration.ipynb
2. Try loading different types of spatial data
3. Experiment with coordinate transformations
4. Move on to geometric operations in the next module

Remember:
- Always visualize your spatial data with .plot()
- Check the CRS before doing spatial analysis
- When in doubt, transform to a projected CRS for measurements
- Geographic CRS (lat/lon) are good for display, projected CRS for analysis

Keep exploring! 🚀
"""
