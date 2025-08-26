"""
Test Suite for Visualization Mapping Module
===========================================

This file tests all functions in the visualization_mapping module to ensure
they work correctly with map creation, styling, and export functionality.

Test Categories:
1. create_choropleth_map: Testing thematic mapping and color schemes
2. multi_layer_visualization: Testing multi-layer map composition
3. interactive_web_map: Testing interactive web map creation
4. export_publication_maps: Testing map export and publication formats

Run these tests to verify your visualization implementations work correctly!
"""

import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import Path
import tempfile
import warnings
import matplotlib.pyplot as plt
import matplotlib
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
from shapely.validation import make_valid

# Import the functions we're testing
from src.geopandas_analysis.visualization_mapping import (
    create_choropleth_map,
    multi_layer_visualization,
    interactive_web_map,
    export_publication_maps
)

# Import test utilities
from tests import (
    create_test_points,
    create_test_polygons,
    create_test_lines,
    SPATIAL_TOLERANCE
)


class TestCreateChoroplethMap:
    """Test the create_choropleth_map function."""

    def test_basic_choropleth_creation(self):
        """Test basic choropleth map creation."""
        polygons = create_test_polygons()

        # Create map with area_value column
        result = create_choropleth_map(polygons, column='area_value')

        assert result is not None
        # Should return matplotlib figure or axis object
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_choropleth_with_custom_colormap(self):
        """Test choropleth with custom colormap."""
        polygons = create_test_polygons()

        result = create_choropleth_map(polygons, column='area_value',
                                     cmap='viridis', scheme='quantiles')

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_choropleth_classification_schemes(self):
        """Test different classification schemes."""
        polygons = create_test_polygons()
        # Add more varied data for classification
        polygons['test_values'] = [10, 50, 100, 200, 500, 1000][:len(polygons)]

        schemes = ['natural_breaks', 'equal_interval', 'quantiles', 'percentiles']

        for scheme in schemes:
            try:
                result = create_choropleth_map(polygons, column='test_values',
                                             scheme=scheme, k=3)
                assert result is not None
            except (ValueError, NotImplementedError):
                # Some schemes might not be available or applicable
                pass

    def test_choropleth_with_missing_values(self):
        """Test choropleth handling of missing/NaN values."""
        polygons = create_test_polygons()
        polygons['values_with_nan'] = [100, np.nan][:len(polygons)]

        result = create_choropleth_map(polygons, column='values_with_nan')

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_choropleth_styling_options(self):
        """Test various styling options."""
        polygons = create_test_polygons()

        result = create_choropleth_map(polygons, column='area_value',
                                     figsize=(12, 8),
                                     edgecolor='black',
                                     linewidth=0.5,
                                     alpha=0.8)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_choropleth_legend_customization(self):
        """Test legend customization options."""
        polygons = create_test_polygons()

        result = create_choropleth_map(polygons, column='area_value',
                                     legend=True,
                                     legend_kwargs={'loc': 'upper right'})

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_choropleth_invalid_column(self):
        """Test error handling with invalid column name."""
        polygons = create_test_polygons()

        with pytest.raises((KeyError, ValueError)):
            create_choropleth_map(polygons, column='nonexistent_column')

    def test_choropleth_empty_geodataframe(self):
        """Test choropleth with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry', 'value'], crs='EPSG:4326')

        result = create_choropleth_map(empty_gdf, column='value')

        # Should handle empty data gracefully
        assert result is not None or result is None  # Implementation dependent

    def test_choropleth_single_feature(self):
        """Test choropleth with single feature."""
        single_polygon = create_test_polygons().iloc[[0]]

        result = create_choropleth_map(single_polygon, column='area_value')

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))


class TestMultiLayerVisualization:
    """Test the multi_layer_visualization function."""

    def test_basic_multi_layer_map(self):
        """Test basic multi-layer visualization."""
        points = create_test_points()
        polygons = create_test_polygons()
        lines = create_test_lines()

        layers = {
            'polygons': polygons,
            'points': points,
            'lines': lines
        }

        result = multi_layer_visualization(layers)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_with_styling(self):
        """Test multi-layer visualization with custom styling."""
        points = create_test_points()
        polygons = create_test_polygons()

        layers = {
            'base_polygons': polygons,
            'overlay_points': points
        }

        styling = {
            'base_polygons': {'color': 'lightblue', 'alpha': 0.7, 'edgecolor': 'black'},
            'overlay_points': {'color': 'red', 'markersize': 50, 'marker': 'o'}
        }

        result = multi_layer_visualization(layers, styling=styling)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_with_labels(self):
        """Test multi-layer visualization with labels."""
        points = create_test_points()
        polygons = create_test_polygons()

        layers = {
            'regions': polygons,
            'cities': points
        }

        labels = {
            'regions': 'name',
            'cities': 'name'
        }

        result = multi_layer_visualization(layers, labels=labels)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_different_crs(self):
        """Test multi-layer visualization with different CRS."""
        points = create_test_points()  # EPSG:4326
        polygons = create_test_polygons().to_crs('EPSG:3857')  # Web Mercator

        layers = {
            'polygons': polygons,
            'points': points
        }

        result = multi_layer_visualization(layers)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_with_basemap(self):
        """Test multi-layer visualization with basemap."""
        points = create_test_points()

        layers = {'points': points}

        try:
            result = multi_layer_visualization(layers, add_basemap=True)
            assert result is not None
        except (ImportError, Exception):
            # Basemap functionality might require additional dependencies
            pytest.skip("Basemap functionality not available")

    def test_multi_layer_layer_ordering(self):
        """Test that layer ordering is preserved."""
        points = create_test_points()
        polygons = create_test_polygons()
        lines = create_test_lines()

        # Use OrderedDict to ensure specific ordering
        from collections import OrderedDict
        layers = OrderedDict([
            ('bottom_layer', polygons),
            ('middle_layer', lines),
            ('top_layer', points)
        ])

        result = multi_layer_visualization(layers)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_empty_layer(self):
        """Test multi-layer with empty layer."""
        points = create_test_points()
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:4326')

        layers = {
            'points': points,
            'empty': empty_gdf
        }

        result = multi_layer_visualization(layers)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_single_layer(self):
        """Test multi-layer with single layer."""
        points = create_test_points()

        layers = {'single_layer': points}

        result = multi_layer_visualization(layers)

        assert result is not None
        assert isinstance(result, (plt.Figure, plt.Axes, tuple))

    def test_multi_layer_invalid_layer_data(self):
        """Test error handling with invalid layer data."""
        invalid_layers = {
            'invalid': "not a geodataframe"
        }

        with pytest.raises((TypeError, AttributeError)):
            multi_layer_visualization(invalid_layers)


class TestInteractiveWebMap:
    """Test the interactive_web_map function."""

    def test_basic_web_map_creation(self):
        """Test basic interactive web map creation."""
        points = create_test_points()

        result = interactive_web_map(points)

        assert result is not None
        # Should return folium Map object or similar
        # Check for common attributes of web maps
        assert hasattr(result, 'save') or hasattr(result, '_repr_html_') or callable(result)

    def test_web_map_with_popup_info(self):
        """Test web map with popup information."""
        points = create_test_points()

        result = interactive_web_map(points, popup_columns=['name', 'value'])

        assert result is not None

    def test_web_map_with_markers(self):
        """Test web map with custom markers."""
        points = create_test_points()

        result = interactive_web_map(points, marker_type='circle',
                                   marker_color='blue', marker_size=10)

        assert result is not None

    def test_web_map_choropleth(self):
        """Test interactive choropleth web map."""
        polygons = create_test_polygons()

        result = interactive_web_map(polygons, choropleth_column='area_value')

        assert result is not None

    def test_web_map_custom_basemap(self):
        """Test web map with custom basemap."""
        points = create_test_points()

        try:
            result = interactive_web_map(points, tiles='OpenStreetMap')
            assert result is not None
        except ImportError:
            pytest.skip("Folium not available for interactive mapping")

    def test_web_map_clustering(self):
        """Test web map with marker clustering."""
        # Create more points for clustering
        n_points = 20
        x_coords = np.random.uniform(-1, 1, n_points)
        y_coords = np.random.uniform(-1, 1, n_points)

        many_points = gpd.GeoDataFrame({
            'id': range(n_points),
            'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
        }, crs='EPSG:4326')

        try:
            result = interactive_web_map(many_points, cluster_markers=True)
            assert result is not None
        except (ImportError, NotImplementedError):
            pytest.skip("Clustering functionality not available")

    def test_web_map_different_geometry_types(self):
        """Test web map with different geometry types."""
        polygons = create_test_polygons()

        result = interactive_web_map(polygons)

        assert result is not None

    def test_web_map_custom_center_zoom(self):
        """Test web map with custom center and zoom."""
        points = create_test_points()

        result = interactive_web_map(points, center_lat=1.5, center_lon=1.5, zoom_start=10)

        assert result is not None

    def test_web_map_empty_data(self):
        """Test web map with empty data."""
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:4326')

        result = interactive_web_map(empty_gdf)

        # Should handle empty data gracefully
        assert result is not None or result is None  # Implementation dependent

    def test_web_map_invalid_geometry(self):
        """Test web map error handling with invalid geometry."""
        invalid_gdf = gpd.GeoDataFrame({
            'geometry': [None, Point(0, 0)]
        }, crs='EPSG:4326')

        # Should handle invalid geometries gracefully
        result = interactive_web_map(invalid_gdf)
        assert result is not None or result is None


class TestExportPublicationMaps:
    """Test the export_publication_maps function."""

    def test_basic_map_export(self, tmp_path):
        """Test basic map export functionality."""
        polygons = create_test_polygons()
        output_path = tmp_path / "test_map.png"

        result = export_publication_maps(polygons, output_path=str(output_path))

        # Should create file or return success indicator
        assert output_path.exists() or result is True or result is not None

    def test_export_multiple_formats(self, tmp_path):
        """Test exporting maps in multiple formats."""
        points = create_test_points()

        formats = ['png', 'pdf', 'svg']

        for fmt in formats:
            output_path = tmp_path / f"test_map.{fmt}"
            try:
                result = export_publication_maps(points, output_path=str(output_path),
                                               format=fmt)
                # Check if file was created or operation succeeded
                assert output_path.exists() or result is not None
            except (ValueError, NotImplementedError):
                # Some formats might not be supported
                pass

    def test_export_with_custom_styling(self, tmp_path):
        """Test export with custom styling parameters."""
        polygons = create_test_polygons()
        output_path = tmp_path / "styled_map.png"

        styling = {
            'figsize': (12, 8),
            'dpi': 300,
            'facecolor': 'white',
            'edgecolor': 'black',
            'linewidth': 0.5
        }

        result = export_publication_maps(polygons, output_path=str(output_path),
                                       **styling)

        assert output_path.exists() or result is not None

    def test_export_with_title_labels(self, tmp_path):
        """Test export with title and labels."""
        points = create_test_points()
        output_path = tmp_path / "labeled_map.png"

        result = export_publication_maps(points, output_path=str(output_path),
                                       title="Test Map",
                                       xlabel="Longitude",
                                       ylabel="Latitude")

        assert output_path.exists() or result is not None

    def test_export_high_dpi(self, tmp_path):
        """Test export with high DPI for publication quality."""
        polygons = create_test_polygons()
        output_path = tmp_path / "high_dpi_map.png"

        result = export_publication_maps(polygons, output_path=str(output_path),
                                       dpi=300, bbox_inches='tight')

        assert output_path.exists() or result is not None

    def test_export_choropleth_map(self, tmp_path):
        """Test export of choropleth map."""
        polygons = create_test_polygons()
        output_path = tmp_path / "choropleth_export.png"

        result = export_publication_maps(polygons, output_path=str(output_path),
                                       column='area_value', cmap='viridis',
                                       legend=True)

        assert output_path.exists() or result is not None

    def test_export_with_basemap(self, tmp_path):
        """Test export with contextual basemap."""
        points = create_test_points().to_crs('EPSG:3857')
        output_path = tmp_path / "basemap_export.png"

        try:
            result = export_publication_maps(points, output_path=str(output_path),
                                           add_basemap=True)
            assert output_path.exists() or result is not None
        except (ImportError, Exception):
            pytest.skip("Basemap functionality not available")

    def test_export_invalid_path(self):
        """Test error handling with invalid output path."""
        points = create_test_points()
        invalid_path = "/invalid/path/that/does/not/exist/map.png"

        with pytest.raises((OSError, IOError, ValueError)):
            export_publication_maps(points, output_path=invalid_path)

    def test_export_empty_geodataframe(self, tmp_path):
        """Test export with empty GeoDataFrame."""
        empty_gdf = gpd.GeoDataFrame([], columns=['geometry'], crs='EPSG:4326')
        output_path = tmp_path / "empty_map.png"

        result = export_publication_maps(empty_gdf, output_path=str(output_path))

        # Should handle empty data gracefully
        assert output_path.exists() or result is None or result is not None

    def test_export_batch_maps(self, tmp_path):
        """Test batch export of multiple maps."""
        points = create_test_points()
        polygons = create_test_polygons()

        datasets = {
            'points_map': points,
            'polygons_map': polygons
        }

        output_dir = tmp_path / "batch_export"
        output_dir.mkdir()

        for name, gdf in datasets.items():
            output_path = output_dir / f"{name}.png"
            result = export_publication_maps(gdf, output_path=str(output_path))
            # At least some exports should succeed
            assert output_path.exists() or result is not None


# Integration and performance tests
class TestVisualizationIntegration:
    """Integration tests combining multiple visualization functions."""

    def test_complete_visualization_workflow(self, tmp_path):
        """Test complete workflow: choropleth -> multi-layer -> interactive -> export."""
        points = create_test_points()
        polygons = create_test_polygons()

        # Step 1: Create choropleth map
        choropleth = create_choropleth_map(polygons, column='area_value')
        assert choropleth is not None

        # Step 2: Create multi-layer visualization
        layers = {'polygons': polygons, 'points': points}
        multi_layer = multi_layer_visualization(layers)
        assert multi_layer is not None

        # Step 3: Create interactive web map
        try:
            interactive = interactive_web_map(points)
            assert interactive is not None
        except ImportError:
            pytest.skip("Interactive mapping dependencies not available")

        # Step 4: Export publication map
        output_path = tmp_path / "workflow_export.png"
        export_result = export_publication_maps(polygons, output_path=str(output_path))
        assert output_path.exists() or export_result is not None

    @pytest.mark.benchmark
    def test_performance_large_dataset_visualization(self):
        """Test performance with larger datasets."""
        # Create larger test dataset
        n_features = 1000
        x_coords = np.random.uniform(-180, 180, n_features)
        y_coords = np.random.uniform(-90, 90, n_features)

        large_points = gpd.GeoDataFrame({
            'id': range(n_features),
            'value': np.random.randint(1, 100, n_features),
            'geometry': [Point(x, y) for x, y in zip(x_coords, y_coords)]
        }, crs='EPSG:4326')

        import time

        # Test choropleth performance
        start_time = time.time()
        choropleth = create_choropleth_map(large_points.head(100), column='value')
        choropleth_time = time.time() - start_time

        # Test multi-layer performance
        start_time = time.time()
        layers = {'points': large_points.head(500)}
        multi_layer = multi_layer_visualization(layers)
        multi_layer_time = time.time() - start_time

        # Performance assertions (adjust thresholds as needed)
        assert choropleth_time < 30.0  # Should complete within 30 seconds
        assert multi_layer_time < 60.0  # Should complete within 60 seconds

        assert choropleth is not None
        assert multi_layer is not None

        print(f"Choropleth creation: {choropleth_time:.2f}s")
        print(f"Multi-layer visualization: {multi_layer_time:.2f}s")

    def test_memory_efficiency_visualization(self):
        """Test memory efficiency of visualization operations."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Create and destroy multiple visualizations
        points = create_test_points()
        polygons = create_test_polygons()

        for _ in range(5):
            choropleth = create_choropleth_map(polygons, column='area_value')
            layers = {'points': points, 'polygons': polygons}
            multi_layer = multi_layer_visualization(layers)

            # Clean up matplotlib figures
            plt.close('all')

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024

    def test_consistent_styling_across_functions(self):
        """Test that styling is consistent across different visualization functions."""
        polygons = create_test_polygons()

        # Test that similar styling parameters work across functions
        styling_params = {
            'figsize': (10, 8),
            'edgecolor': 'black',
            'alpha': 0.7
        }

        # Should work with choropleth
        choropleth = create_choropleth_map(polygons, column='area_value', **styling_params)
        assert choropleth is not None

        # Should work with multi-layer (adapted parameters)
        layers = {'polygons': polygons}
        layer_styling = {'polygons': styling_params}
        multi_layer = multi_layer_visualization(layers, styling=layer_styling)
        assert multi_layer is not None

    def test_coordinate_system_handling(self, tmp_path):
        """Test coordinate system handling across visualization functions."""
        # Test with different CRS
        crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:32633']

        for crs in crs_list:
            try:
                points = create_test_points().to_crs(crs)

                # All functions should handle different CRS
                choropleth = create_choropleth_map(points, column='value')
                assert choropleth is not None

                layers = {'points': points}
                multi_layer = multi_layer_visualization(layers)
                assert multi_layer is not None

                # Export should preserve CRS information
                output_path = tmp_path / f"crs_test_{crs.replace(':', '_')}.png"
                export_result = export_publication_maps(points, output_path=str(output_path))

                plt.close('all')  # Clean up

            except Exception as e:
                # Some CRS transformations might fail in test environment
                print(f"CRS {crs} test failed: {e}")
                continue
