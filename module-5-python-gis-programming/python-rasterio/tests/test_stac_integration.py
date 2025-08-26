"""
Test suite for STAC integration functionality.

This module contains comprehensive tests for STAC (Spatio-Temporal Asset Catalog)
integration in the rasterio_analysis.stac_integration module, including catalog
search, satellite data access, and cloud-based processing workflows.

Author: Student Test Suite
Course: GIST 604B - Open Source GIS Programming
Assignment: Python Rasterio Advanced Processing
"""

import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
import tempfile
from pathlib import Path
import warnings
from unittest.mock import patch, MagicMock
import json
import requests
from shapely.geometry import box, Polygon

# Import the functions we're testing
try:
    from src.rasterio_analysis.stac_integration import (
        STACDataSource,
        search_satellite_imagery,
        download_stac_assets,
        process_stac_timeseries,
        calculate_indices_from_stac,
        create_composite_from_stac
    )
except ImportError as e:
    pytest.skip(f"Could not import STAC integration functions: {e}", allow_module_level=True)


class TestSTACIntegration:
    """Test suite for STAC integration functionality."""

    @pytest.fixture(scope="class")
    def sample_bbox(self):
        """Sample bounding box for testing (Phoenix, Arizona area)."""
        return (-112.5, 33.0, -111.5, 34.0)

    @pytest.fixture(scope="class")
    def sample_date_range(self):
        """Sample date range for testing."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    @pytest.fixture(scope="class")
    def mock_stac_catalog(self):
        """Mock STAC catalog for testing."""
        catalog_data = {
            "type": "Catalog",
            "id": "test-catalog",
            "title": "Test STAC Catalog",
            "description": "Mock catalog for testing",
            "links": [
                {
                    "rel": "search",
                    "href": "https://test-catalog.com/search",
                    "type": "application/json"
                }
            ]
        }
        return catalog_data

    @pytest.fixture(scope="class")
    def mock_stac_items(self):
        """Mock STAC items for testing."""
        items = []
        for i in range(3):
            item = {
                "type": "Feature",
                "id": f"test-item-{i}",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-112.0, 33.0],
                        [-111.0, 33.0],
                        [-111.0, 34.0],
                        [-112.0, 34.0],
                        [-112.0, 33.0]
                    ]]
                },
                "properties": {
                    "datetime": f"2023-0{i+1}-15T12:00:00Z",
                    "collection": "landsat-8",
                    "cloud_cover": 10 + i * 5
                },
                "assets": {
                    "red": {
                        "href": f"https://test.com/red_{i}.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "eo:bands": [{"name": "B4", "common_name": "red"}]
                    },
                    "nir": {
                        "href": f"https://test.com/nir_{i}.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "eo:bands": [{"name": "B5", "common_name": "nir"}]
                    },
                    "green": {
                        "href": f"https://test.com/green_{i}.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "eo:bands": [{"name": "B3", "common_name": "green"}]
                    },
                    "blue": {
                        "href": f"https://test.com/blue_{i}.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "eo:bands": [{"name": "B2", "common_name": "blue"}]
                    }
                }
            }
            items.append(item)
        return items

    def test_stac_data_source_initialization(self):
        """Test STACDataSource class initialization."""
        # Test with default parameters
        stac_source = STACDataSource()
        assert stac_source.catalog_url is None
        assert stac_source.max_items == 100

        # Test with custom parameters
        custom_source = STACDataSource(
            catalog_url="https://test-catalog.com",
            max_items=50,
            timeout=60
        )
        assert custom_source.catalog_url == "https://test-catalog.com"
        assert custom_source.max_items == 50
        assert custom_source.timeout == 60

    @patch('src.rasterio_analysis.stac_integration.pystac_client.Client.open')
    def test_stac_data_source_connect(self, mock_client_open, mock_stac_catalog):
        """Test STAC catalog connection."""
        mock_catalog = MagicMock()
        mock_catalog.to_dict.return_value = mock_stac_catalog
        mock_client_open.return_value = mock_catalog

        stac_source = STACDataSource("https://test-catalog.com")
        result = stac_source.connect_to_catalog()

        assert result['success'] == True
        assert result['catalog_info'] is not None
        assert 'connection_time' in result

    @patch('src.rasterio_analysis.stac_integration.requests.get')
    def test_search_satellite_imagery_mock(self, mock_get, sample_bbox, sample_date_range, mock_stac_items):
        """Test satellite imagery search with mocked STAC API."""
        # Mock the search response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": mock_stac_items
        }
        mock_get.return_value = mock_response

        result = search_satellite_imagery(
            bbox=sample_bbox,
            datetime_range=sample_date_range,
            collections=['landsat-8'],
            max_cloud_cover=20
        )

        # Check result structure
        required_keys = [
            'items_found', 'search_parameters', 'items', 'summary_statistics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check search results
        assert result['items_found'] > 0
        assert len(result['items']) > 0

        # Check search parameters
        params = result['search_parameters']
        assert params['bbox'] == sample_bbox
        assert params['collections'] == ['landsat-8']
        assert params['max_cloud_cover'] == 20

        # Check summary statistics
        stats = result['summary_statistics']
        assert 'date_range' in stats
        assert 'cloud_cover_stats' in stats
        assert 'collections_found' in stats

    def test_search_satellite_imagery_invalid_parameters(self):
        """Test search with invalid parameters."""
        # Invalid bounding box
        with pytest.raises(ValueError, match="Invalid bounding box"):
            search_satellite_imagery(
                bbox=(-180, -90, 180),  # Missing fourth coordinate
                datetime_range=('2023-01-01', '2023-01-31')
            )

        # Invalid date range
        with pytest.raises(ValueError, match="Invalid datetime range"):
            search_satellite_imagery(
                bbox=(-112, 33, -111, 34),
                datetime_range=('2023-01-31', '2023-01-01')  # End before start
            )

    @patch('src.rasterio_analysis.stac_integration.rasterio.open')
    @patch('src.rasterio_analysis.stac_integration.requests.get')
    def test_download_stac_assets_mock(self, mock_get, mock_rasterio_open, mock_stac_items, tmp_path):
        """Test STAC asset downloading with mocked operations."""
        # Mock HTTP response for asset download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content = MagicMock(return_value=[b'mock_data'] * 100)
        mock_get.return_value = mock_response

        # Mock rasterio validation
        mock_src = MagicMock()
        mock_src.width = 1000
        mock_src.height = 1000
        mock_src.count = 1
        mock_rasterio_open.return_value.__enter__ = MagicMock(return_value=mock_src)

        assets_to_download = [
            {
                'item_id': 'test-item-0',
                'asset_key': 'red',
                'url': 'https://test.com/red_0.tif'
            },
            {
                'item_id': 'test-item-0',
                'asset_key': 'nir',
                'url': 'https://test.com/nir_0.tif'
            }
        ]

        result = download_stac_assets(
            assets_to_download,
            download_directory=tmp_path,
            max_workers=2
        )

        # Check result structure
        required_keys = [
            'download_summary', 'successful_downloads', 'failed_downloads',
            'total_size_mb', 'download_time_seconds'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check download results
        assert result['download_summary']['total_requested'] == 2
        assert result['download_summary']['successful'] >= 0
        assert len(result['successful_downloads']) + len(result['failed_downloads']) == 2

    def test_download_stac_assets_invalid_directory(self):
        """Test asset download with invalid directory."""
        assets = [{'item_id': 'test', 'asset_key': 'red', 'url': 'https://test.com/test.tif'}]

        with pytest.raises(FileNotFoundError):
            download_stac_assets(assets, download_directory="/nonexistent/path")

    @patch('src.rasterio_analysis.stac_integration.xarray.open_dataset')
    def test_process_stac_timeseries_mock(self, mock_xr_open, mock_stac_items, tmp_path):
        """Test STAC timeseries processing with mocked data."""
        # Mock xarray dataset
        dates = pd.date_range('2023-01-01', periods=3, freq='M')
        mock_data = np.random.random((3, 100, 100))  # time, y, x

        mock_dataset = MagicMock()
        mock_dataset.dims = {'time': 3, 'y': 100, 'x': 100}
        mock_dataset['time'] = dates
        mock_dataset.values = mock_data
        mock_xr_open.return_value = mock_dataset

        # Create mock file paths
        asset_paths = []
        for i in range(3):
            asset_path = tmp_path / f"asset_{i}.tif"
            asset_path.touch()  # Create empty files
            asset_paths.append(str(asset_path))

        result = process_stac_timeseries(
            asset_paths,
            analysis_type='ndvi_timeseries',
            output_format='netcdf'
        )

        # Check result structure
        required_keys = [
            'timeseries_data', 'temporal_statistics', 'processing_info',
            'output_files', 'analysis_parameters'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check timeseries data info
        ts_data = result['timeseries_data']
        assert 'temporal_extent' in ts_data
        assert 'time_steps' in ts_data

        # Check temporal statistics
        temp_stats = result['temporal_statistics']
        assert 'mean_over_time' in temp_stats
        assert 'std_over_time' in temp_stats

    def test_process_stac_timeseries_empty_input(self):
        """Test timeseries processing with empty input."""
        with pytest.raises(ValueError, match="No asset paths provided"):
            process_stac_timeseries([], analysis_type='ndvi_timeseries')

    @patch('src.rasterio_analysis.stac_integration.rasterio.open')
    def test_calculate_indices_from_stac_mock(self, mock_rasterio_open, tmp_path):
        """Test vegetation index calculation from STAC assets."""
        # Mock rasterio data
        red_data = np.random.randint(1000, 2000, (500, 500), dtype=np.uint16)
        nir_data = np.random.randint(2000, 4000, (500, 500), dtype=np.uint16)

        def mock_open_side_effect(path):
            mock_src = MagicMock()
            mock_src.width = 500
            mock_src.height = 500
            mock_src.count = 1
            mock_src.crs = 'EPSG:4326'
            mock_src.transform = [0.001, 0, -112, 0, -0.001, 34, 0, 0, 1]

            if 'red' in str(path):
                mock_src.read.return_value = red_data.reshape(1, 500, 500)
            elif 'nir' in str(path):
                mock_src.read.return_value = nir_data.reshape(1, 500, 500)

            return MagicMock(__enter__=MagicMock(return_value=mock_src), __exit__=MagicMock())

        mock_rasterio_open.side_effect = mock_open_side_effect

        # Create mock asset files
        red_path = tmp_path / "red.tif"
        nir_path = tmp_path / "nir.tif"
        red_path.touch()
        nir_path.touch()

        asset_bands = {
            'red': str(red_path),
            'nir': str(nir_path)
        }

        result = calculate_indices_from_stac(
            asset_bands,
            indices=['NDVI', 'EVI'],
            output_directory=tmp_path
        )

        # Check result structure
        required_keys = [
            'calculated_indices', 'index_statistics', 'output_files', 'processing_info'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check calculated indices
        calc_indices = result['calculated_indices']
        assert 'NDVI' in calc_indices
        assert 'EVI' in calc_indices

        # Check statistics
        for index_name in ['NDVI', 'EVI']:
            stats = result['index_statistics'][index_name]
            assert 'mean' in stats
            assert 'std' in stats
            assert 'min' in stats
            assert 'max' in stats

    def test_calculate_indices_missing_bands(self):
        """Test index calculation with missing required bands."""
        asset_bands = {'red': 'red.tif'}  # Missing NIR for NDVI

        with pytest.raises(ValueError, match="Missing required bands"):
            calculate_indices_from_stac(
                asset_bands,
                indices=['NDVI'],
                output_directory='/tmp'
            )

    @patch('src.rasterio_analysis.stac_integration.rasterio.open')
    def test_create_composite_from_stac_mock(self, mock_rasterio_open, tmp_path):
        """Test composite creation from STAC assets."""
        # Mock multiple scenes with different data
        scenes = []
        for i in range(3):
            scene_data = {
                'red': np.random.randint(500 + i*100, 1500 + i*100, (200, 200), dtype=np.uint16),
                'green': np.random.randint(400 + i*100, 1400 + i*100, (200, 200), dtype=np.uint16),
                'blue': np.random.randint(300 + i*100, 1300 + i*100, (200, 200), dtype=np.uint16)
            }
            scenes.append(scene_data)

        def mock_open_side_effect(path):
            mock_src = MagicMock()
            mock_src.width = 200
            mock_src.height = 200
            mock_src.count = 1
            mock_src.crs = 'EPSG:4326'
            mock_src.transform = [0.001, 0, -112, 0, -0.001, 34, 0, 0, 1]

            # Determine which scene and band based on path
            scene_idx = int(str(path).split('_')[1])  # Extract scene number
            band = str(path).split('_')[2].split('.')[0]  # Extract band name

            mock_src.read.return_value = scenes[scene_idx][band].reshape(1, 200, 200)
            return MagicMock(__enter__=MagicMock(return_value=mock_src), __exit__=MagicMock())

        mock_rasterio_open.side_effect = mock_open_side_effect

        # Create mock scene assets
        scene_assets = []
        for i in range(3):
            scene = {}
            for band in ['red', 'green', 'blue']:
                path = tmp_path / f"scene_{i}_{band}.tif"
                path.touch()
                scene[band] = str(path)
            scene_assets.append(scene)

        output_path = tmp_path / "composite.tif"

        result = create_composite_from_stac(
            scene_assets,
            output_path,
            composite_method='median',
            bands=['red', 'green', 'blue']
        )

        # Check result structure
        required_keys = [
            'composite_info', 'input_scenes', 'processing_statistics',
            'output_file', 'quality_metrics'
        ]
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"

        # Check composite info
        comp_info = result['composite_info']
        assert comp_info['method'] == 'median'
        assert comp_info['bands_processed'] == ['red', 'green', 'blue']
        assert comp_info['scenes_used'] == 3

    def test_create_composite_invalid_method(self, tmp_path):
        """Test composite creation with invalid method."""
        scene_assets = [{'red': 'red.tif'}]
        output_path = tmp_path / "output.tif"

        with pytest.raises(ValueError, match="Unsupported composite method"):
            create_composite_from_stac(
                scene_assets,
                output_path,
                composite_method='invalid_method'
            )


class TestSTACDataSource:
    """Test the STACDataSource class functionality."""

    def test_stac_data_source_context_manager(self):
        """Test STACDataSource as context manager."""
        with STACDataSource("https://test-catalog.com") as stac_source:
            assert stac_source is not None
            assert stac_source.catalog_url == "https://test-catalog.com"

    @patch('src.rasterio_analysis.stac_integration.pystac_client.Client.open')
    def test_stac_data_source_search_functionality(self, mock_client_open, sample_bbox, mock_stac_items):
        """Test STAC data source search functionality."""
        # Mock the client and search
        mock_search = MagicMock()
        mock_search.items.return_value = mock_stac_items

        mock_catalog = MagicMock()
        mock_catalog.search.return_value = mock_search
        mock_client_open.return_value = mock_catalog

        stac_source = STACDataSource("https://test-catalog.com")

        results = stac_source.search_items(
            bbox=sample_bbox,
            datetime='2023-01-01/2023-03-31',
            collections=['landsat-8']
        )

        # Check results
        assert len(results) > 0
        assert all('id' in item for item in results)

    def test_stac_data_source_filter_by_cloud_cover(self, mock_stac_items):
        """Test filtering items by cloud cover."""
        stac_source = STACDataSource()

        # Filter items with cloud cover < 15%
        filtered_items = stac_source.filter_items_by_cloud_cover(
            mock_stac_items,
            max_cloud_cover=15
        )

        # Should filter out items with high cloud cover
        assert len(filtered_items) < len(mock_stac_items)

        for item in filtered_items:
            assert item['properties']['cloud_cover'] <= 15

    def test_stac_data_source_get_asset_urls(self, mock_stac_items):
        """Test extracting asset URLs from STAC items."""
        stac_source = STACDataSource()

        asset_urls = stac_source.get_asset_urls(
            mock_stac_items,
            asset_types=['red', 'nir']
        )

        # Check structure
        assert isinstance(asset_urls, dict)
        assert len(asset_urls) > 0

        # Check that URLs are extracted for requested asset types
        for item_id, assets in asset_urls.items():
            assert 'red' in assets
            assert 'nir' in assets
            assert assets['red'].startswith('https://')
            assert assets['nir'].startswith('https://')


class TestSTACEdgeCases:
    """Test edge cases and error conditions for STAC integration."""

    def test_stac_search_no_results(self):
        """Test STAC search with no results."""
        with patch('src.rasterio_analysis.stac_integration.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "type": "FeatureCollection",
                "features": []
            }
            mock_get.return_value = mock_response

            result = search_satellite_imagery(
                bbox=(-180, -90, 180, 90),  # Entire world
                datetime_range=('1900-01-01', '1900-01-02'),  # No data expected
                collections=['nonexistent-collection']
            )

            assert result['items_found'] == 0
            assert len(result['items']) == 0

    @patch('src.rasterio_analysis.stac_integration.requests.get')
    def test_stac_api_error_handling(self, mock_get):
        """Test handling of STAC API errors."""
        # Mock API error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            search_satellite_imagery(
                bbox=(-112, 33, -111, 34),
                datetime_range=('2023-01-01', '2023-01-31')
            )

    def test_stac_timeseries_single_timestep(self, tmp_path):
        """Test timeseries processing with only one timestep."""
        # Create single asset file
        asset_path = tmp_path / "single_asset.tif"
        asset_path.touch()

        with patch('src.rasterio_analysis.stac_integration.xarray.open_dataset') as mock_xr:
            mock_dataset = MagicMock()
            mock_dataset.dims = {'y': 100, 'x': 100}  # No time dimension
            mock_xr.return_value = mock_dataset

            result = process_stac_timeseries(
                [str(asset_path)],
                analysis_type='basic_stats'
            )

            # Should handle single timestep gracefully
            assert 'processing_info' in result
            assert 'warnings' in result['processing_info']

    def test_large_bbox_warning(self):
        """Test warning for very large bounding boxes."""
        with patch('src.rasterio_analysis.stac_integration.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"type": "FeatureCollection", "features": []}
            mock_get.return_value = mock_response

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                # Very large bounding box
                search_satellite_imagery(
                    bbox=(-180, -85, 180, 85),  # Nearly entire world
                    datetime_range=('2023-01-01', '2023-01-31'),
                    max_items=1000
                )

                # Should generate a warning about large area
                assert len(w) > 0
                assert any("large bounding box" in str(warning.message).lower() for warning in w)

    def test_concurrent_downloads_error_handling(self, tmp_path):
        """Test error handling in concurrent asset downloads."""
        assets = [
            {'item_id': 'test-1', 'asset_key': 'red', 'url': 'https://invalid-url-1.com/test.tif'},
            {'item_id': 'test-2', 'asset_key': 'red', 'url': 'https://invalid-url-2.com/test.tif'},
        ]

        with patch('src.rasterio_analysis.stac_integration.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

            result = download_stac_assets(
                assets,
                download_directory=tmp_path,
                max_workers=2
            )

            # Should handle connection errors gracefully
            assert result['download_summary']['successful'] == 0
            assert result['download_summary']['failed'] == 2
            assert len(result['failed_downloads']) == 2

            # Check error information is captured
            for failed_download in result['failed_downloads']:
                assert 'error_message' in failed_download
                assert 'Connection failed' in failed_download['error_message']
