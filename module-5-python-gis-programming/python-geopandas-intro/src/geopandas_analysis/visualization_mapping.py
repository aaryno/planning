"""
Visualization & Mapping Module - Student Implementation
======================================================

Welcome to spatial visualization! This module teaches you how to create
beautiful, informative maps from your spatial data.

Maps are how we communicate spatial analysis results. Think of this module
as your "cartographic toolkit" - you'll learn to:
- Create choropleth maps (colored by data values)
- Combine multiple layers for rich visualizations
- Build interactive web maps for exploration
- Export publication-quality static maps

IMPORTANT: Good maps tell a story! Always consider:
- What question is your map answering?
- Who is your audience?
- What colors and symbols make sense?
- Does your map have proper legends and labels?

What you'll learn:
- Creating thematic maps with proper symbology
- Layering different spatial datasets effectively
- Building interactive maps for web browsers
- Exporting maps for reports and presentations
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import Dict, List, Tuple, Union, Any, Optional
import warnings
from pathlib import Path

# Import optional dependencies with fallbacks
try:
    import contextily as ctx
    HAS_CONTEXTILY = True
except ImportError:
    HAS_CONTEXTILY = False

try:
    import folium
    from folium import plugins
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False


def create_choropleth_map(gdf: gpd.GeoDataFrame,
                         value_column: str,
                         classification_method: str = 'quantiles',
                         color_scheme: str = 'Blues',
                         num_classes: int = 5,
                         title: str = None,
                         figsize: Tuple[int, int] = (12, 8)) -> Tuple[plt.Figure, plt.Axes]:
    """
    CREATE CHOROPLETH MAP (Color-coded thematic map showing data patterns)

    Choropleth maps use colors to show how a numeric value varies across areas.
    Common examples:
    - Population density by county (light to dark colors)
    - Income levels by neighborhood (different color intensities)
    - Election results by district (categorical colors)

    Think of this like a weather map - different colors show different
    temperature ranges, helping you quickly see spatial patterns.

    Your Task: Create a professional choropleth map with proper legend and styling.

    Args:
        gdf: GeoDataFrame with polygon features to map
        value_column: Column name with values to map with colors
        classification_method: How to group values ('quantiles', 'equal_interval', 'natural_breaks')
        color_scheme: Color palette name ('Blues', 'Reds', 'Greens', 'viridis', 'plasma')
        num_classes: Number of color classes to create
        title: Map title
        figsize: Figure size in inches (width, height)

    Returns:
        Tuple of (matplotlib Figure, Axes) for further customization
    """

    if len(gdf) == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, 'No data to display', ha='center', va='center')
        return fig, ax

    # STEP 1: Validate inputs and prepare data
    if value_column not in gdf.columns:
        raise ValueError(f"Column '{value_column}' not found in GeoDataFrame")

    # Check for numeric data
    if not pd.api.types.is_numeric_dtype(gdf[value_column]):
        warnings.warn(f"Column '{value_column}' is not numeric - attempting conversion")
        try:
            gdf = gdf.copy()
            gdf[value_column] = pd.to_numeric(gdf[value_column], errors='coerce')
        except:
            raise ValueError(f"Cannot convert column '{value_column}' to numeric")

    # Remove rows with missing values for mapping
    mapping_gdf = gdf.dropna(subset=[value_column]).copy()

    if len(mapping_gdf) == 0:
        raise ValueError(f"No valid numeric values found in column '{value_column}'")

    # STEP 2: Classify the data into groups
    values = mapping_gdf[value_column].values

    if classification_method == 'quantiles':
        # Equal number of features in each class
        # HINT: Use pd.qcut() to create quantile-based classes
        try:
            mapping_gdf['color_class'] = pd.qcut(values, q=num_classes, labels=False, duplicates='drop')
        except:
            # Fallback if quantiles fail (e.g., too many identical values)
            mapping_gdf['color_class'] = pd.cut(values, bins=num_classes, labels=False)

    elif classification_method == 'equal_interval':
        # Equal range intervals
        # HINT: Use pd.cut() to create equal-width intervals
        mapping_gdf['color_class'] = pd.cut(values, bins=num_classes, labels=False)

    elif classification_method == 'natural_breaks':
        # Natural breaks (Jenks) - simplified version
        # For a real implementation, you'd use a library like mapclassify
        # Here we'll approximate with quantiles
        try:
            mapping_gdf['color_class'] = pd.qcut(values, q=num_classes, labels=False, duplicates='drop')
        except:
            mapping_gdf['color_class'] = pd.cut(values, bins=num_classes, labels=False)
    else:
        raise ValueError("classification_method must be 'quantiles', 'equal_interval', or 'natural_breaks'")

    # STEP 3: Create the map
    fig, ax = plt.subplots(figsize=figsize)

    # Create colormap
    if color_scheme in ['viridis', 'plasma', 'inferno', 'magma']:
        cmap = plt.cm.get_cmap(color_scheme)
    else:
        # Try to get colormap, fallback to Blues if not found
        try:
            cmap = plt.cm.get_cmap(color_scheme)
        except:
            cmap = plt.cm.get_cmap('Blues')
            warnings.warn(f"Color scheme '{color_scheme}' not found, using 'Blues'")

    # STEP 4: Plot the choropleth
    # HINT: Use mapping_gdf.plot() with column='color_class', cmap=cmap, legend=True
    mapping_gdf.plot(
        column='color_class',
        cmap=cmap,
        legend=True,
        ax=ax,
        edgecolor='white',
        linewidth=0.5,
        legend_kwds={'shrink': 0.8}
    )

    # Plot features without data in gray
    missing_data = gdf[gdf[value_column].isna()]
    if len(missing_data) > 0:
        missing_data.plot(ax=ax, color='lightgray', edgecolor='white', linewidth=0.5)

    # STEP 5: Add title and labels
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title(f'{value_column} by {classification_method.replace("_", " ").title()}',
                    fontsize=14, fontweight='bold', pad=20)

    # Remove axis ticks and labels for cleaner look
    ax.set_xticks([])
    ax.set_yticks([])

    # Add value range information to legend
    legend_labels = []
    for i in range(int(mapping_gdf['color_class'].max()) + 1):
        class_data = mapping_gdf[mapping_gdf['color_class'] == i][value_column]
        if len(class_data) > 0:
            min_val = class_data.min()
            max_val = class_data.max()
            legend_labels.append(f'{min_val:.1f} - {max_val:.1f}')

    # STEP 6: Add basemap if available and appropriate
    if HAS_CONTEXTILY and gdf.crs is not None:
        try:
            # Transform to Web Mercator for basemap
            if gdf.crs.to_epsg() != 3857:
                basemap_gdf = mapping_gdf.to_crs(epsg=3857)
                ax_bounds = basemap_gdf.total_bounds

                # Add basemap
                ctx.add_basemap(ax, crs=basemap_gdf.crs, alpha=0.5,
                               source=ctx.providers.CartoDB.Positron)

        except Exception as e:
            # Basemap failed, continue without it
            pass

    plt.tight_layout()
    return fig, ax


def multi_layer_visualization(layers: Dict[str, gpd.GeoDataFrame],
                             layer_styles: Dict[str, Dict] = None,
                             title: str = "Multi-Layer Map",
                             figsize: Tuple[int, int] = (14, 10),
                             add_basemap: bool = True) -> Tuple[plt.Figure, plt.Axes]:
    """
    CREATE MULTI-LAYER VISUALIZATION (Combine different spatial datasets on one map)

    Multi-layer maps show relationships between different types of spatial features:
    - Cities (points) + Roads (lines) + Counties (polygons)
    - Schools (points) + School districts (polygons) + Rivers (lines)
    - Hospitals (points) + Population density (choropleth) + Highways (lines)

    Think of this like stacking transparent sheets of different map information
    to see how they relate to each other geographically.

    Your Task: Combine multiple spatial datasets into one comprehensive map.

    Args:
        layers: Dictionary with layer names and GeoDataFrames {'layer_name': gdf}
        layer_styles: Dictionary with styling for each layer
        title: Map title
        figsize: Figure size
        add_basemap: Whether to add a web tile basemap

    Returns:
        Tuple of (matplotlib Figure, Axes) for the multi-layer map
    """

    if not layers or len(layers) == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, 'No layers to display', ha='center', va='center')
        return fig, ax

    # STEP 1: Validate layers and ensure compatible CRS
    valid_layers = {}
    reference_crs = None

    for layer_name, gdf in layers.items():
        if gdf is None or len(gdf) == 0:
            warnings.warn(f"Layer '{layer_name}' is empty or None, skipping")
            continue

        # Set reference CRS from first valid layer
        if reference_crs is None:
            reference_crs = gdf.crs

        # Transform to reference CRS if needed
        if gdf.crs != reference_crs and gdf.crs is not None and reference_crs is not None:
            gdf = gdf.to_crs(reference_crs)

        valid_layers[layer_name] = gdf

    if not valid_layers:
        raise ValueError("No valid layers found")

    # STEP 2: Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # STEP 3: Set default styles if not provided
    if layer_styles is None:
        layer_styles = {}

    # Default colors for different layer types
    default_colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    color_idx = 0

    # STEP 4: Plot each layer
    for layer_name, gdf in valid_layers.items():
        # Get style for this layer or use defaults
        style = layer_styles.get(layer_name, {})

        # Determine geometry type for appropriate styling
        geom_types = gdf.geometry.type.value_counts()
        primary_geom_type = geom_types.index[0] if len(geom_types) > 0 else 'Unknown'

        # Set default style based on geometry type
        if primary_geom_type in ['Point', 'MultiPoint']:
            default_style = {
                'color': default_colors[color_idx % len(default_colors)],
                'markersize': 50,
                'alpha': 0.7,
                'edgecolors': 'white',
                'linewidths': 1
            }
        elif primary_geom_type in ['LineString', 'MultiLineString']:
            default_style = {
                'color': default_colors[color_idx % len(default_colors)],
                'linewidth': 2,
                'alpha': 0.8
            }
        else:  # Polygon types
            default_style = {
                'facecolor': default_colors[color_idx % len(default_colors)],
                'alpha': 0.6,
                'edgecolor': 'white',
                'linewidth': 0.5
            }

        # Merge with user-provided style
        final_style = {**default_style, **style}

        # STEP 5: Plot the layer
        try:
            # HINT: Use gdf.plot(ax=ax, **final_style) to plot each layer
            if primary_geom_type in ['Point', 'MultiPoint']:
                gdf.plot(ax=ax, **final_style, label=layer_name)
            else:
                gdf.plot(ax=ax, **final_style, label=layer_name)

        except Exception as e:
            warnings.warn(f"Failed to plot layer '{layer_name}': {str(e)}")

        color_idx += 1

    # STEP 6: Add basemap if requested and available
    if add_basemap and HAS_CONTEXTILY and reference_crs is not None:
        try:
            # Transform bounds to Web Mercator for basemap
            all_bounds = []
            for gdf in valid_layers.values():
                if gdf.crs.to_epsg() != 3857:
                    gdf_3857 = gdf.to_crs(epsg=3857)
                    all_bounds.extend(gdf_3857.total_bounds)
                else:
                    all_bounds.extend(gdf.total_bounds)

            if all_bounds:
                # Add basemap
                ctx.add_basemap(ax, crs='epsg:3857', alpha=0.4,
                              source=ctx.providers.CartoDB.Positron)

        except Exception as e:
            warnings.warn(f"Could not add basemap: {str(e)}")

    # STEP 7: Add title and legend
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

    # Add legend if multiple layers
    if len(valid_layers) > 1:
        ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))

    # Remove axis ticks for cleaner appearance
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    return fig, ax


def interactive_web_map(gdf: gpd.GeoDataFrame,
                       popup_columns: List[str] = None,
                       color_column: str = None,
                       basemap: str = 'OpenStreetMap',
                       zoom_start: int = 10) -> 'folium.Map':
    """
    CREATE INTERACTIVE WEB MAP (Build clickable, zoomable maps for web browsers)

    Interactive maps let users:
    - Zoom in and out to explore different scales
    - Click on features to see detailed information
    - Toggle layers on and off
    - Pan around to different areas

    Perfect for data exploration and sharing results with stakeholders
    who want to investigate the data themselves.

    Your Task: Create an interactive Folium map with clickable features.

    Args:
        gdf: GeoDataFrame with features to map
        popup_columns: Columns to show in feature popups
        color_column: Column to use for color-coding features
        basemap: Base map style ('OpenStreetMap', 'CartoDB positron', 'Stamen Terrain')
        zoom_start: Initial zoom level

    Returns:
        Folium Map object (can be saved as HTML)
    """

    if not HAS_FOLIUM:
        raise ImportError("folium is required for interactive web maps. Install with: pip install folium")

    if len(gdf) == 0:
        # Create empty map centered on world
        m = folium.Map(location=[0, 0], zoom_start=2)
        return m

    # STEP 1: Ensure data is in WGS84 for web mapping
    if gdf.crs is None:
        warnings.warn("No CRS defined - assuming WGS84")
        web_gdf = gdf.copy()
    elif gdf.crs.to_epsg() != 4326:
        # Transform to WGS84 for web mapping
        web_gdf = gdf.to_crs('EPSG:4326')
    else:
        web_gdf = gdf.copy()

    # STEP 2: Calculate map center and bounds
    bounds = web_gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2

    # STEP 3: Create base map
    # Set up basemap tiles
    if basemap.lower() == 'openstreetmap':
        tiles = 'OpenStreetMap'
    elif 'cartodb' in basemap.lower():
        tiles = 'CartoDB positron'
    elif 'stamen' in basemap.lower():
        tiles = 'Stamen Terrain'
    else:
        tiles = 'OpenStreetMap'

    # HINT: Create folium.Map with location=[center_lat, center_lon]
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=tiles
    )

    # STEP 4: Prepare popup content
    if popup_columns is None:
        # Use all non-geometry columns
        popup_columns = [col for col in web_gdf.columns if col != web_gdf.geometry.name]

    # STEP 5: Add features to map based on geometry type
    geom_types = web_gdf.geometry.type.value_counts()
    primary_geom_type = geom_types.index[0] if len(geom_types) > 0 else 'Unknown'

    for idx, row in web_gdf.iterrows():
        # Create popup content
        popup_html = "<div style='font-family: Arial; font-size: 12px;'>"
        for col in popup_columns:
            if col in row and pd.notna(row[col]):
                popup_html += f"<b>{col}:</b> {row[col]}<br>"
        popup_html += "</div>"

        popup = folium.Popup(popup_html, max_width=300)

        # Determine color
        if color_column and color_column in row:
            # Simple color mapping - in practice you'd want more sophisticated coloring
            try:
                value = float(row[color_column])
                # Normalize to 0-1 range for color mapping
                if color_column in web_gdf.columns:
                    col_min = web_gdf[color_column].min()
                    col_max = web_gdf[color_column].max()
                    if col_max > col_min:
                        normalized = (value - col_min) / (col_max - col_min)
                        # Convert to color (simple blue-red scale)
                        red = int(255 * normalized)
                        blue = int(255 * (1 - normalized))
                        color = f'#{red:02x}00{blue:02x}'
                    else:
                        color = 'blue'
                else:
                    color = 'blue'
            except:
                color = 'blue'
        else:
            color = 'blue'

        # Add feature based on geometry type
        try:
            if primary_geom_type in ['Point', 'MultiPoint']:
                # HINT: Use folium.CircleMarker for point features
                folium.CircleMarker(
                    location=[row.geometry.y, row.geometry.x],
                    radius=8,
                    popup=popup,
                    color='white',
                    weight=2,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)

            elif primary_geom_type in ['Polygon', 'MultiPolygon']:
                # HINT: Use folium.GeoJson for polygon features
                geojson_data = {
                    'type': 'Feature',
                    'geometry': row.geometry.__geo_interface__,
                    'properties': {col: str(row[col]) for col in popup_columns if col in row}
                }

                folium.GeoJson(
                    geojson_data,
                    style_function=lambda x, color=color: {
                        'fillColor': color,
                        'color': 'white',
                        'weight': 2,
                        'fillOpacity': 0.6
                    },
                    popup=popup
                ).add_to(m)

            elif primary_geom_type in ['LineString', 'MultiLineString']:
                # Convert linestring to coordinate list
                if hasattr(row.geometry, 'coords'):
                    coords = [[lat, lon] for lon, lat in row.geometry.coords]
                    folium.PolyLine(
                        locations=coords,
                        color=color,
                        weight=3,
                        opacity=0.8,
                        popup=popup
                    ).add_to(m)

        except Exception as e:
            warnings.warn(f"Could not add feature {idx} to map: {str(e)}")

    # STEP 6: Fit map to data bounds
    try:
        # HINT: Use m.fit_bounds() to zoom to show all features
        southwest = [bounds[1], bounds[0]]  # [lat_min, lon_min]
        northeast = [bounds[3], bounds[2]]  # [lat_max, lon_max]
        m.fit_bounds([southwest, northeast], padding=(20, 20))
    except:
        pass

    return m


def export_publication_maps(gdf: gpd.GeoDataFrame,
                          output_directory: Union[str, Path],
                          map_configs: List[Dict] = None,
                          file_formats: List[str] = None,
                          dpi: int = 300) -> Dict[str, str]:
    """
    EXPORT PUBLICATION-QUALITY MAPS (Create high-resolution maps for reports and papers)

    Publication maps need to be:
    - High resolution (300+ DPI for print)
    - Professional styling (clean fonts, proper colors)
    - Multiple formats (PNG for web, PDF for print, SVG for editing)
    - Consistent sizing and layout

    Your Task: Generate publication-ready maps in multiple formats.

    Args:
        gdf: GeoDataFrame to map
        output_directory: Directory to save maps
        map_configs: List of different map configurations to generate
        file_formats: List of formats to export ('png', 'pdf', 'svg', 'jpg')
        dpi: Resolution in dots per inch (300+ recommended for print)

    Returns:
        Dictionary with generated file paths
    """

    if len(gdf) == 0:
        return {'error': 'No data to map'}

    # STEP 1: Setup output directory
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    if file_formats is None:
        file_formats = ['png', 'pdf']

    if map_configs is None:
        # Default simple map configuration
        map_configs = [{
            'type': 'simple',
            'title': 'Spatial Data Map',
            'color': 'blue',
            'figsize': (12, 8)
        }]

    generated_files = {}

    # STEP 2: Generate each map configuration
    for i, config in enumerate(map_configs):
        map_type = config.get('type', 'simple')
        title = config.get('title', f'Map {i+1}')
        figsize = config.get('figsize', (12, 8))

        try:
            # Create the map based on configuration
            if map_type == 'simple':
                fig, ax = plt.subplots(figsize=figsize)

                # Simple styling
                gdf.plot(
                    ax=ax,
                    color=config.get('color', 'blue'),
                    alpha=config.get('alpha', 0.7),
                    edgecolor=config.get('edgecolor', 'white'),
                    linewidth=config.get('linewidth', 0.5)
                )

            elif map_type == 'choropleth' and 'value_column' in config:
                # Create choropleth map
                fig, ax = create_choropleth_map(
                    gdf=gdf,
                    value_column=config['value_column'],
                    title=title,
                    figsize=figsize,
                    color_scheme=config.get('color_scheme', 'Blues'),
                    num_classes=config.get('num_classes', 5)
                )

            else:
                # Default to simple map
                fig, ax = plt.subplots(figsize=figsize)
                gdf.plot(ax=ax, color='blue', alpha=0.7)

            # STEP 3: Apply publication styling
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xticks([])
            ax.set_yticks([])

            # Add scale bar and north arrow if possible
            # (Simplified implementation)

            # STEP 4: Export in each requested format
            base_filename = f"map_{i+1}_{title.replace(' ', '_').lower()}"

            for fmt in file_formats:
                try:
                    filename = f"{base_filename}.{fmt}"
                    filepath = output_dir / filename

                    # HINT: Use fig.savefig() with appropriate parameters
                    fig.savefig(
                        filepath,
                        format=fmt,
                        dpi=dpi,
                        bbox_inches='tight',
                        facecolor='white',
                        edgecolor='none',
                        transparent=False if fmt in ['jpg', 'jpeg'] else True
                    )

                    generated_files[f"{base_filename}_{fmt}"] = str(filepath)

                except Exception as e:
                    warnings.warn(f"Could not save {fmt} format: {str(e)}")

            plt.close(fig)  # Free memory

        except Exception as e:
            warnings.warn(f"Could not generate map configuration {i+1}: {str(e)}")

    return generated_files


# ==============================================================================
# HELPER FUNCTIONS AND UTILITIES
# ==============================================================================

def _get_optimal_figsize(gdf: gpd.GeoDataFrame, base_width: float = 10) -> Tuple[float, float]:
    """Calculate optimal figure size based on data extent."""
    try:
        bounds = gdf.total_bounds
        width_extent = bounds[2] - bounds[0]
        height_extent = bounds[3] - bounds[1]

        if width_extent > 0 and height_extent > 0:
            aspect_ratio = height_extent / width_extent
            height = base_width * aspect_ratio
            # Cap height to reasonable range
            height = min(max(height, 4), 16)
            return (base_width, height)
        else:
            return (base_width, 8)
    except:
        return (base_width, 8)


def _create_custom_colormap(colors: List[str], n_colors: int = 256):
    """Create custom colormap from list of colors."""
    try:
        from matplotlib.colors import LinearSegmentedColormap
        return LinearSegmentedColormap.from_list("custom", colors, N=n_colors)
    except:
        return plt.cm.Blues


# ==============================================================================
# CONSTANTS AND REFERENCE DATA
# ==============================================================================

# Professional color schemes for different map types
COLOR_SCHEMES = {
    'sequential': ['Blues', 'Greens', 'Oranges', 'Reds', 'Purples', 'YlOrRd', 'YlGnBu'],
    'diverging': ['RdYlBu', 'RdBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr'],
    'qualitative': ['Set1', 'Set2', 'Set3', 'Paired', 'Dark2', 'Accent'],
    'perceptual': ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
}

# Standard map sizes for different purposes
STANDARD_MAP_SIZES = {
    'presentation': (16, 9),    # 16:9 for slides
    'report': (8.5, 11),        # Letter size portrait
    'poster': (36, 24),         # Large poster
    'web': (12, 8),             # Web display
    'square': (10, 10),         # Square format
}

# Export quality settings
QUALITY_SETTINGS = {
    'draft': {'dpi': 150, 'formats': ['png']},
    'standard': {'dpi': 300, 'formats': ['png', 'pdf']},
    'publication': {'dpi': 600, 'formats': ['png', 'pdf', 'svg']},
}

"""
CONGRATULATIONS! 🎨

You've completed the visualization and mapping module! You now know how to:
✅ Create professional choropleth maps with proper symbology
✅ Combine multiple spatial datasets in layered visualizations
✅ Build interactive web maps for data exploration
✅ Export publication-quality maps for reports and presentations

These visualization skills help you communicate spatial analysis results effectively!

Next Steps:
1. Test your functions in: notebooks/04_visualization_gallery.ipynb
2. Experiment with different color schemes and styling options
3. Create interactive maps and save them as HTML files
4. Generate high-quality exports for your portfolio

Remember:
- Good maps tell a clear story - always consider your audience
- Color choice matters - use colorblind-friendly palettes when possible
- Interactive maps are great for exploration, static maps for communication
- High DPI (300+) is essential for print publications

Pro Tips:
- Test your maps on different devices and screen sizes
- Use consistent styling across multiple maps in a project
- Add appropriate legends, scale bars, and north arrows
- Keep basemaps subtle so they don't compete with your data

You're now equipped to create compelling spatial visualizations! 🚀
"""
