#!/usr/bin/env python3
"""
Automated Grade Calculation Script for GeoPandas Spatial Analysis Assignment
============================================================================

Calculates final grade based on spatial analysis assessment components:
- Spatial Correctness (15 points): Geometric operations, CRS handling, spatial joins
- Performance (5 points): Efficiency with large spatial datasets, spatial indexing
- Code Quality (5 points): Formatting, linting, type hints, spatial best practices
- Visualization Quality (5 points): Map generation, proper symbology, interactive features

Total: 30 points
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Tuple
import subprocess
import re
import tempfile
from datetime import datetime

class SpatialGradeCalculator:
    """Automated grade calculator for GeoPandas spatial analysis assignment."""

    def __init__(self):
        self.total_points = 30
        self.component_weights = {
            'spatial_correctness': 15,    # Spatial operations and analysis correctness
            'performance': 5,             # Spatial performance and optimization
            'code_quality': 5,            # Code formatting, linting, type hints
            'visualization_quality': 5     # Map generation and visualization quality
        }
        self.grade_report = {
            'total_score': 0,
            'component_scores': {},
            'feedback': [],
            'detailed_results': {},
            'spatial_metrics': {},
            'timestamp': datetime.now().isoformat()
        }

    def calculate_spatial_correctness_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on spatial analysis correctness."""
        try:
            # Parse pytest results focusing on spatial functionality
            if Path('test-results.xml').exists():
                tree = ET.parse('test-results.xml')
                root = tree.getroot()

                total_tests = int(root.get('tests', 0))
                failures = int(root.get('failures', 0))
                errors = int(root.get('errors', 0))
                passed = total_tests - failures - errors

                if total_tests == 0:
                    return 0, {'error': 'No spatial tests found'}

                # Analyze spatial-specific test results
                spatial_test_breakdown = self._analyze_spatial_tests(root)

                # Calculate weighted score based on spatial test categories
                spatial_weights = {
                    'spatial_data_loading': 0.25,      # 25% - loading and exploring data
                    'geometric_operations': 0.35,      # 35% - measurements, buffers, transforms
                    'spatial_joins_analysis': 0.25,    # 25% - spatial relationships
                    'visualization_mapping': 0.15      # 15% - map creation
                }

                weighted_score = 0
                for category, weight in spatial_weights.items():
                    category_pass_rate = spatial_test_breakdown.get(category, {}).get('pass_rate', 0)
                    weighted_score += weight * category_pass_rate

                final_score = int(self.component_weights['spatial_correctness'] * weighted_score)

                details = {
                    'total_tests': total_tests,
                    'passed': passed,
                    'failed': failures,
                    'errors': errors,
                    'overall_pass_rate': f"{passed/total_tests:.2%}" if total_tests > 0 else "0%",
                    'spatial_breakdown': spatial_test_breakdown,
                    'weighted_score': f"{weighted_score:.2%}"
                }

                return final_score, details

            else:
                # Fallback: run specific spatial tests
                return self._run_spatial_correctness_tests()

        except Exception as e:
            return 0, {'error': f'Failed to calculate spatial correctness: {str(e)}'}

    def _analyze_spatial_tests(self, test_root) -> Dict[str, Dict[str, Any]]:
        """Analyze spatial test results by category."""
        categories = {
            'spatial_data_loading': [],
            'geometric_operations': [],
            'spatial_joins_analysis': [],
            'visualization_mapping': []
        }

        # Parse test cases and categorize
        for testcase in test_root.findall('.//testcase'):
            classname = testcase.get('classname', '')
            name = testcase.get('name', '')

            # Categorize tests based on class and function names
            if 'spatial_data_loading' in classname.lower() or 'load' in name.lower():
                category = 'spatial_data_loading'
            elif 'geometric_operations' in classname.lower() or any(op in name.lower() for op in ['buffer', 'centroid', 'area', 'distance']):
                category = 'geometric_operations'
            elif 'spatial_joins' in classname.lower() or 'join' in name.lower():
                category = 'spatial_joins_analysis'
            elif 'visualization' in classname.lower() or 'map' in name.lower():
                category = 'visualization_mapping'
            else:
                category = 'geometric_operations'  # Default category

            # Check if test passed
            failed = testcase.find('failure') is not None or testcase.find('error') is not None
            categories[category].append({
                'name': name,
                'passed': not failed,
                'time': float(testcase.get('time', 0))
            })

        # Calculate statistics for each category
        result = {}
        for category, tests in categories.items():
            if tests:
                passed_count = sum(1 for t in tests if t['passed'])
                total_count = len(tests)
                pass_rate = passed_count / total_count
                avg_time = sum(t['time'] for t in tests) / total_count

                result[category] = {
                    'total': total_count,
                    'passed': passed_count,
                    'failed': total_count - passed_count,
                    'pass_rate': pass_rate,
                    'average_time': avg_time
                }
            else:
                result[category] = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'pass_rate': 0,
                    'average_time': 0
                }

        return result

    def _run_spatial_correctness_tests(self) -> Tuple[int, Dict[str, Any]]:
        """Run specific spatial correctness validation tests."""
        try:
            # Test basic spatial functionality
            test_script = '''
import sys
sys.path.insert(0, "src")

try:
    from geopandas_analysis.spatial_data_loading import load_spatial_dataset, explore_spatial_properties
    from geopandas_analysis.geometric_operations import calculate_spatial_metrics, create_buffers_and_zones
    from geopandas_analysis.spatial_joins_analysis import spatial_intersection_analysis
    from geopandas_analysis.visualization_mapping import create_choropleth_map

    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import tempfile
    import json

    results = {"tests": 0, "passed": 0, "details": []}

    # Test 1: Basic spatial data creation and loading
    results["tests"] += 1
    try:
        test_gdf = gpd.GeoDataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30],
            'geometry': [Point(0, 0), Point(1, 1), Point(2, 2)]
        }, crs='EPSG:4326')

        props = explore_spatial_properties(test_gdf)
        assert props['feature_count'] == 3
        assert props['primary_geometry_type'] == 'Point'
        results["passed"] += 1
        results["details"].append("✅ Spatial data exploration works")
    except Exception as e:
        results["details"].append(f"❌ Spatial data exploration failed: {str(e)}")

    # Test 2: Geometric operations
    results["tests"] += 1
    try:
        metrics_gdf = calculate_spatial_metrics(test_gdf)
        assert 'area_units2' in metrics_gdf.columns
        assert 'length_units' in metrics_gdf.columns
        results["passed"] += 1
        results["details"].append("✅ Spatial metrics calculation works")
    except Exception as e:
        results["details"].append(f"❌ Spatial metrics failed: {str(e)}")

    # Test 3: Buffer operations
    results["tests"] += 1
    try:
        buffer_results = create_buffers_and_zones(test_gdf, [100])
        assert 'buffers' in buffer_results
        results["passed"] += 1
        results["details"].append("✅ Spatial buffering works")
    except Exception as e:
        results["details"].append(f"❌ Spatial buffering failed: {str(e)}")

    # Test 4: CRS handling
    results["tests"] += 1
    try:
        transformed = test_gdf.to_crs('EPSG:3857')
        assert transformed.crs.to_epsg() == 3857
        results["passed"] += 1
        results["details"].append("✅ CRS transformations work")
    except Exception as e:
        results["details"].append(f"❌ CRS transformation failed: {str(e)}")

    print(json.dumps(results))

except ImportError as e:
    print(json.dumps({"tests": 0, "passed": 0, "error": f"Import failed: {str(e)}"}))
except Exception as e:
    print(json.dumps({"tests": 0, "passed": 0, "error": f"Test execution failed: {str(e)}"}))
'''

            # Run the test script
            result = subprocess.run(
                ['python', '-c', test_script],
                capture_output=True, text=True, timeout=120
            )

            if result.returncode == 0 and result.stdout.strip():
                test_results = json.loads(result.stdout.strip())

                if 'error' in test_results:
                    return 0, {'error': test_results['error']}

                total_tests = test_results.get('tests', 0)
                passed_tests = test_results.get('passed', 0)

                if total_tests > 0:
                    pass_rate = passed_tests / total_tests
                    score = int(self.component_weights['spatial_correctness'] * pass_rate)

                    details = {
                        'total_tests': total_tests,
                        'passed': passed_tests,
                        'failed': total_tests - passed_tests,
                        'pass_rate': f"{pass_rate:.2%}",
                        'test_details': test_results.get('details', [])
                    }

                    return score, details
                else:
                    return 0, {'error': 'No spatial tests executed'}
            else:
                return 0, {'error': f'Spatial test execution failed: {result.stderr}'}

        except Exception as e:
            return 0, {'error': f'Spatial correctness test failed: {str(e)}'}

    def calculate_performance_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on spatial performance benchmarks."""
        try:
            if Path('benchmark.json').exists():
                with open('benchmark.json', 'r') as f:
                    benchmark_data = json.load(f)

                benchmarks = benchmark_data.get('benchmarks', [])
                if not benchmarks:
                    return 0, {'error': 'No performance benchmarks found'}

                # Focus on spatial-specific benchmarks
                spatial_benchmarks = [b for b in benchmarks
                                    if any(keyword in b.get('name', '').lower()
                                          for keyword in ['spatial', 'buffer', 'join', 'transform', 'geometric'])]

                if not spatial_benchmarks:
                    # If no spatial-specific benchmarks, use all benchmarks
                    spatial_benchmarks = benchmarks

                # Performance scoring criteria for spatial operations
                performance_thresholds = {
                    'excellent': 1.0,    # Full points
                    'good': 0.8,         # 80% of points
                    'acceptable': 0.6,   # 60% of points
                    'poor': 0.3          # 30% of points
                }

                total_score = 0
                benchmark_scores = []

                for benchmark in spatial_benchmarks:
                    mean_time = benchmark.get('stats', {}).get('mean', float('inf'))
                    name = benchmark.get('name', 'unknown')

                    # Scoring based on operation type and expected performance
                    if 'buffer' in name.lower():
                        # Buffer operations - should be fast with spatial indexing
                        if mean_time < 0.01:
                            score = performance_thresholds['excellent']
                        elif mean_time < 0.05:
                            score = performance_thresholds['good']
                        elif mean_time < 0.1:
                            score = performance_thresholds['acceptable']
                        else:
                            score = performance_thresholds['poor']
                    elif 'join' in name.lower():
                        # Spatial joins - more expensive but should use spatial indexing
                        if mean_time < 0.1:
                            score = performance_thresholds['excellent']
                        elif mean_time < 0.5:
                            score = performance_thresholds['good']
                        elif mean_time < 1.0:
                            score = performance_thresholds['acceptable']
                        else:
                            score = performance_thresholds['poor']
                    else:
                        # General spatial operations
                        if mean_time < 0.05:
                            score = performance_thresholds['excellent']
                        elif mean_time < 0.2:
                            score = performance_thresholds['good']
                        elif mean_time < 0.5:
                            score = performance_thresholds['acceptable']
                        else:
                            score = performance_thresholds['poor']

                    benchmark_scores.append({
                        'name': name,
                        'mean_time': mean_time,
                        'score': score
                    })
                    total_score += score

                # Calculate average performance score
                if spatial_benchmarks:
                    avg_score = total_score / len(spatial_benchmarks)
                    final_score = int(self.component_weights['performance'] * avg_score)
                else:
                    final_score = 0
                    avg_score = 0

                details = {
                    'total_benchmarks': len(benchmarks),
                    'spatial_benchmarks': len(spatial_benchmarks),
                    'average_performance_score': f"{avg_score:.2%}",
                    'benchmark_details': benchmark_scores[:10],  # Limit to 10 for report
                    'overall_mean_time': sum(b['mean_time'] for b in benchmark_scores) / len(benchmark_scores) if benchmark_scores else 0
                }

                return final_score, details

            else:
                # Run basic performance test if benchmark.json not found
                return self._run_basic_performance_test()

        except Exception as e:
            return 0, {'error': f'Failed to calculate spatial performance: {str(e)}'}

    def _run_basic_performance_test(self) -> Tuple[int, Dict[str, Any]]:
        """Run basic spatial performance validation."""
        try:
            perf_test_script = '''
import sys
sys.path.insert(0, "src")
import time
import json
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

try:
    from geopandas_analysis.geometric_operations import calculate_spatial_metrics

    # Create moderately sized test dataset
    n_points = 500
    test_gdf = gpd.GeoDataFrame({
        'id': range(n_points),
        'value': np.random.randint(1, 100, n_points),
        'geometry': [Point(np.random.uniform(-180, 180), np.random.uniform(-90, 90))
                    for _ in range(n_points)]
    }, crs='EPSG:4326')

    # Test spatial metrics calculation performance
    start_time = time.time()
    result = calculate_spatial_metrics(test_gdf)
    end_time = time.time()

    execution_time = end_time - start_time
    features_per_second = n_points / execution_time if execution_time > 0 else 0

    # Performance scoring
    if features_per_second > 1000:
        score = 1.0  # Excellent
    elif features_per_second > 500:
        score = 0.8  # Good
    elif features_per_second > 100:
        score = 0.6  # Acceptable
    else:
        score = 0.3  # Poor

    results = {
        'execution_time': execution_time,
        'features_processed': n_points,
        'features_per_second': features_per_second,
        'performance_score': score,
        'test_successful': True
    }

    print(json.dumps(results))

except Exception as e:
    print(json.dumps({'test_successful': False, 'error': str(e)}))
'''

            result = subprocess.run(
                ['python', '-c', perf_test_script],
                capture_output=True, text=True, timeout=60
            )

            if result.returncode == 0 and result.stdout.strip():
                perf_results = json.loads(result.stdout.strip())

                if perf_results.get('test_successful', False):
                    score = int(self.component_weights['performance'] * perf_results['performance_score'])
                    details = {
                        'execution_time': perf_results['execution_time'],
                        'features_processed': perf_results['features_processed'],
                        'features_per_second': perf_results['features_per_second'],
                        'performance_rating': 'excellent' if perf_results['performance_score'] >= 0.9
                                            else 'good' if perf_results['performance_score'] >= 0.7
                                            else 'acceptable' if perf_results['performance_score'] >= 0.5
                                            else 'poor'
                    }
                    return score, details
                else:
                    return 0, {'error': perf_results.get('error', 'Performance test failed')}
            else:
                return 0, {'error': 'Performance test execution failed'}

        except Exception as e:
            return 0, {'error': f'Performance test failed: {str(e)}'}

    def calculate_code_quality_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on code quality metrics."""
        quality_checks = {
            'black_formatting': {'weight': 0.3, 'passed': False},
            'ruff_linting': {'weight': 0.3, 'passed': False},
            'mypy_type_checking': {'weight': 0.2, 'passed': False},
            'bandit_security': {'weight': 0.2, 'passed': False}
        }

        details = {'checks': {}}

        try:
            # Check Black formatting
            black_result = subprocess.run(
                ['black', '--check', '--diff', 'src/', 'tests/'],
                capture_output=True, text=True
            )
            quality_checks['black_formatting']['passed'] = (black_result.returncode == 0)
            details['checks']['black_formatting'] = {
                'passed': quality_checks['black_formatting']['passed'],
                'output': black_result.stdout[:500] if black_result.stdout else None
            }

            # Check Ruff linting
            ruff_result = subprocess.run(
                ['ruff', 'check', 'src/', 'tests/', '--output-format=json'],
                capture_output=True, text=True
            )
            quality_checks['ruff_linting']['passed'] = (ruff_result.returncode == 0)

            # Parse ruff output for spatial-specific issues
            ruff_issues = []
            if ruff_result.stdout:
                try:
                    ruff_data = json.loads(ruff_result.stdout)
                    spatial_issues = [issue for issue in ruff_data
                                    if any(keyword in issue.get('filename', '').lower()
                                          for keyword in ['spatial', 'geometric', 'visualization'])]
                    ruff_issues = spatial_issues[:5]  # Limit for report
                except:
                    pass

            details['checks']['ruff_linting'] = {
                'passed': quality_checks['ruff_linting']['passed'],
                'spatial_issues': ruff_issues
            }

            # Check MyPy type checking
            mypy_result = subprocess.run(
                ['mypy', 'src/', '--no-error-summary', '--json-report=/tmp/mypy_report'],
                capture_output=True, text=True
            )
            quality_checks['mypy_type_checking']['passed'] = (mypy_result.returncode == 0)
            details['checks']['mypy_type_checking'] = {
                'passed': quality_checks['mypy_type_checking']['passed'],
                'error_summary': mypy_result.stdout[:300] if mypy_result.stdout else None
            }

            # Check Bandit security scanning
            bandit_result = subprocess.run(
                ['bandit', '-r', 'src/', '-f', 'json'],
                capture_output=True, text=True
            )
            quality_checks['bandit_security']['passed'] = (bandit_result.returncode == 0)
            details['checks']['bandit_security'] = {
                'passed': quality_checks['bandit_security']['passed']
            }

        except Exception as e:
            details['error'] = f'Code quality check failed: {str(e)}'

        # Calculate weighted score
        total_weight = 0
        weighted_score = 0

        for check, config in quality_checks.items():
            weight = config['weight']
            passed = config['passed']
            total_weight += weight
            if passed:
                weighted_score += weight

        if total_weight > 0:
            final_score = int(self.component_weights['code_quality'] * (weighted_score / total_weight))
        else:
            final_score = 0

        details['quality_score_breakdown'] = {
            check: {'weight': f"{config['weight']:.1%}", 'passed': config['passed']}
            for check, config in quality_checks.items()
        }
        details['weighted_score'] = f"{weighted_score/total_weight:.2%}" if total_weight > 0 else "0%"

        return final_score, details

    def calculate_visualization_quality_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on spatial visualization quality."""
        try:
            viz_test_script = '''
import sys
sys.path.insert(0, "src")
import json
import tempfile
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

try:
    from geopandas_analysis.visualization_mapping import create_choropleth_map, multi_layer_visualization, export_publication_maps
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import numpy as np

    results = {'tests': 0, 'passed': 0, 'details': []}

    # Create test spatial data
    test_points = gpd.GeoDataFrame({
        'name': ['A', 'B', 'C', 'D'],
        'value': [10, 20, 30, 40],
        'geometry': [Point(-110, 33), Point(-111, 34), Point(-112, 35), Point(-109, 32)]
    }, crs='EPSG:4326')

    test_polygons = gpd.GeoDataFrame({
        'name': ['Region 1', 'Region 2'],
        'pop_density': [100, 200],
        'geometry': [
            Polygon([(-111, 33), (-110, 33), (-110, 34), (-111, 34)]),
            Polygon([(-112, 34), (-111, 34), (-111, 35), (-112, 35)])
        ]
    }, crs='EPSG:4326')

    # Test 1: Choropleth map creation
    results['tests'] += 1
    try:
        fig, ax = create_choropleth_map(test_polygons, 'pop_density')
        assert fig is not None
        assert ax is not None
        plt.close(fig)
        results['passed'] += 1
        results['details'].append("✅ Choropleth map creation works")
    except Exception as e:
        results['details'].append(f"❌ Choropleth map failed: {str(e)}")

    # Test 2: Multi-layer visualization
    results['tests'] += 1
    try:
        layers = {'points': test_points, 'polygons': test_polygons}
        fig, ax = multi_layer_visualization(layers, title="Test Multi-layer Map")
        assert fig is not None
        assert ax is not None
        plt.close(fig)
        results['passed'] += 1
        results['details'].append("✅ Multi-layer visualization works")
    except Exception as e:
        results['details'].append(f"❌ Multi-layer visualization failed: {str(e)}")

    # Test 3: Map export functionality
    results['tests'] += 1
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            configs = [{'type': 'simple', 'title': 'Test Export', 'color': 'blue'}]
            exported = export_publication_maps(test_points, tmpdir, map_configs=configs, file_formats=['png'])
            assert len(exported) > 0
            # Check if file was actually created
            created_files = [f for f in exported.values() if os.path.exists(f)]
            assert len(created_files) > 0
        results['passed'] += 1
        results['details'].append("✅ Map export functionality works")
    except Exception as e:
        results['details'].append(f"❌ Map export failed: {str(e)}")

    # Test 4: Interactive map functionality (if available)
    results['tests'] += 1
    try:
        try:
            from geopandas_analysis.visualization_mapping import interactive_web_map
            web_map = interactive_web_map(test_points, popup_columns=['name', 'value'])
            assert web_map is not None
            results['passed'] += 1
            results['details'].append("✅ Interactive web map creation works")
        except ImportError:
            results['details'].append("⚠️  Interactive mapping not available (folium not installed)")
    except Exception as e:
        results['details'].append(f"❌ Interactive web map failed: {str(e)}")

    print(json.dumps(results))

except ImportError as e:
    print(json.dumps({'tests': 0, 'passed': 0, 'error': f'Visualization imports failed: {str(e)}'}))
except Exception as e:
    print(json.dumps({'tests': 0, 'passed': 0, 'error': f'Visualization test failed: {str(e)}'}))
'''

            # Run visualization tests
            result = subprocess.run(
                ['python', '-c', viz_test_script],
                capture_output=True, text=True, timeout=120
            )

            if result.returncode == 0 and result.stdout.strip():
                viz_results = json.loads(result.stdout.strip())

                if 'error' in viz_results:
                    return 0, {'error': viz_results['error']}

                total_tests = viz_results.get('tests', 0)
                passed_tests = viz_results.get('passed', 0)

                if total_tests > 0:
                    pass_rate = passed_tests / total_tests
                    score = int(self.component_weights['visualization_quality'] * pass_rate)

                    details = {
                        'total_tests': total_tests,
                        'passed': passed_tests,
                        'failed': total_tests - passed_tests,
                        'pass_rate': f"{pass_rate:.2%}",
                        'visualization_details': viz_results.get('details', [])
                    }

                    return score, details
                else:
                    return 0, {'error': 'No visualization tests executed'}
            else:
                return 0, {'error': f'Visualization test execution failed: {result.stderr}'}

        except Exception as e:
            return 0, {'error': f'Visualization quality assessment failed: {str(e)}'}

    def generate_spatial_feedback(self) -> List[str]:
        """Generate spatial analysis-specific feedback."""
        feedback = []

        # Component-specific feedback
        scores = self.grade_report['component_scores']

        # Spatial correctness feedback
        spatial_score = scores.get('spatial_correctness', 0)
        if spatial_score >= 13:  # 85%+ of 15 points
            feedback.append("🗺️ Excellent spatial analysis skills! Your geometric operations and CRS handling are solid.")
        elif spatial_score >= 10:  # 65%+
            feedback.append("📊 Good spatial analysis foundation. Review spatial join operations and CRS transformations.")
        elif spatial_score >= 7:   # 45%+
            feedback.append("🔧 Spatial analysis needs improvement. Focus on coordinate reference systems and geometric operations.")
        else:
            feedback.append("❌ Spatial analysis requires significant work. Review GeoPandas fundamentals and coordinate systems.")

        # Performance feedback
        perf_score = scores.get('performance', 0)
        if perf_score >= 4:  # 80%+ of 5 points
            feedback.append("⚡ Great spatial performance optimization! Using spatial indexing effectively.")
        elif perf_score >= 3:  # 60%+
            feedback.append("⚡ Good performance. Consider using spatial indexes (.sindex) for large datasets.")
        else:
            feedback.append("🐌 Spatial operations are slow. Use spatial indexing and efficient algorithms.")

        # Code quality feedback
        quality_score = scores.get('code_quality', 0)
        if quality_score >= 4:  # 80%+ of 5 points
            feedback.append("✨ Clean, well-formatted spatial analysis code!")
        elif quality_score >= 3:  # 60%+
            feedback.append("📝 Code quality is good. Minor formatting and type hint improvements needed.")
        else:
            feedback.append("🔧 Focus on code formatting (Black) and linting (Ruff) for cleaner code.")

        # Visualization feedback
        viz_score = scores.get('visualization_quality', 0)
        if viz_score >= 4:  # 80%+ of 5 points
            feedback.append("🎨 Excellent spatial visualizations! Maps are well-designed with proper symbology.")
        elif viz_score >= 3:  # 60%+
            feedback.append("🗺️ Good mapping skills. Consider improving legends, colors, and interactive features.")
        else:
            feedback.append("📊 Map visualization needs work. Focus on proper legends, color schemes, and layout.")

        # Overall spatial analysis feedback
        total_score = sum(scores.values())
        percentage = (total_score / self.total_points) * 100

        if percentage >= 90:
            feedback.append("🏆 Outstanding spatial analyst! Professional-level GeoPandas skills demonstrated.")
        elif percentage >= 80:
            feedback.append("🌟 Strong spatial analysis capabilities! Great work with GeoPandas.")
        elif percentage >= 70:
            feedback.append("📈 Good spatial analysis foundation. Continue practicing with real datasets.")
        elif percentage >= 60:
            feedback.append("⚠️ Basic spatial skills present but need significant improvement.")
        else:
            feedback.append("📚 Spatial analysis fundamentals need work. Review GeoPandas documentation and examples.")

        return feedback

    def calculate_final_grade(self) -> Dict[str, Any]:
        """Calculate the final grade by running all spatial analysis assessment components."""
        print("🗺️ Starting spatial analysis grade calculation...")

        # Calculate component scores
        print("Assessing spatial correctness...")
        spatial_score, spatial_details = self.calculate_spatial_correctness_score()

        print("Evaluating spatial performance...")
        performance_score, performance_details = self.calculate_performance_score()

        print("Checking code quality...")
        quality_score, quality_details = self.calculate_code_quality_score()

        print("Testing visualization capabilities...")
        viz_score, viz_details = self.calculate_visualization_quality_score()

        # Store component scores
        self.grade_report['component_scores'] = {
            'spatial_correctness': spatial_score,
            'performance': performance_score,
            'code_quality': quality_score,
            'visualization_quality': viz_score
        }

        # Store detailed results
        self.grade_report['detailed_results'] = {
            'spatial_correctness': spatial_details,
            'performance': performance_details,
            'code_quality': quality_details,
            'visualization_quality': viz_details
        }

        # Calculate total score
        self.grade_report['total_score'] = sum(self.grade_report['component_scores'].values())

        # Add spatial-specific metrics
        self.grade_report['spatial_metrics'] = {
            'coordinate_system_handling': spatial_score >= 10,
            'geometric_operations_working': spatial_score >= 8,
            'spatial_joins_functional': spatial_score >= 6,
            'visualization_capable': viz_score >= 3,
            'performance_optimized': performance_score >= 3
        }

        # Generate feedback
        self.grade_report['feedback'] = self.generate_spatial_feedback()

        return self.grade_report


def main():
    """Main entry point for spatial analysis grade calculation."""
    try:
        calculator = SpatialGradeCalculator()
        grade_report = calculator.calculate_final_grade()

        # Save grade report
        with open('grade_report.json', 'w') as f:
            json.dump(grade_report, f, indent=2)

        # Print summary
        print(f"\n{'='*60}")
        print("🗺️ SPATIAL ANALYSIS GRADING RESULTS")
        print(f"{'='*60}")
        print(f"Total Score: {grade_report['total_score']}/{calculator.total_points}")
        print(f"Percentage: {(grade_report['total_score']/calculator.total_points)*100:.1f}%")

        print(f"\n📊 Spatial Component Breakdown:")
        component_names = {
            'spatial_correctness': 'Spatial Operations & Analysis',
            'performance': 'Spatial Performance',
            'code_quality': 'Code Quality',
            'visualization_quality': 'Visualization & Mapping'
        }

        for component, score in grade_report['component_scores'].items():
            max_score = calculator.component_weights[component]
            percentage = (score / max_score * 100) if max_score > 0 else 0
            status = "✅" if percentage >= 60 else "❌"
            print(f"  {status} {component_names.get(component, component)}: {score}/{max_score} ({percentage:.1f}%)")

        print(f"\n🗺️ Spatial Capabilities Assessment:")
        metrics = grade_report['spatial_metrics']
        for capability, status in metrics.items():
            status_icon = "✅" if status else "❌"
            readable_name = capability.replace('_', ' ').title()
            print(f"  {status_icon} {readable_name}")

        print(f"\n💡 Spatial Analysis Feedback:")
        for feedback_item in grade_report['feedback']:
            print(f"  {feedback_item}")

        # Spatial-specific success criteria
        passing_grade = calculator.total_points * 0.6  # 18 points
        spatial_fundamentals_met = (
            grade_report['component_scores']['spatial_correctness'] >= 9 and  # 60% of spatial ops
            grade_report['component_scores']['visualization_quality'] >= 2     # 40% of visualization
        )

        print(f"\n🎯 Assessment Summary:")
        if grade_report['total_score'] >= passing_grade:
            if spatial_fundamentals_met:
                print(f"  🎉 EXCELLENT: Spatial analysis fundamentals mastered!")
                print(f"  🗺️ Ready for advanced GeoPandas and spatial analysis work")
            else:
                print(f"  ✅ PASSED: Meets minimum requirements")
                print(f"  📈 Continue practicing spatial analysis techniques")
        else:
            print(f"  ❌ NEEDS WORK: Below passing threshold ({passing_grade} points)")
            print(f"  📚 Focus on spatial fundamentals and coordinate systems")

        print(f"\n⏰ Completed: {grade_report['timestamp']}")
        print(f"{'='*60}")

        # Set exit code based on grade
        if grade_report['total_score'] >= passing_grade:
            print("🏁 Spatial analysis assessment: PASSED")
            sys.exit(0)  # Pass
        else:
            print("🔄 Spatial analysis assessment: NEEDS IMPROVEMENT")
            sys.exit(1)  # Fail

    except Exception as e:
        print(f"❌ Grade calculation failed: {str(e)}")

        # Create minimal error report
        error_report = {
            'total_score': 0,
            'component_scores': {
                'spatial_correctness': 0,
                'performance': 0,
                'code_quality': 0,
                'visualization_quality': 0
            },
            'feedback': [f"Grade calculation failed: {str(e)}"],
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

        with open('grade_report.json', 'w') as f:
            json.dump(error_report, f, indent=2)

        sys.exit(1)


if __name__ == "__main__":
    main()
