#!/usr/bin/env python3
"""
PostGIS Fundamentals Assignment - Automated Grading System
=========================================================

GIST 604B - Module 6: PostGIS Spatial Database
Professional grading system for PostGIS database operations assignment.

This script analyzes test results and provides comprehensive feedback on:
- Database connectivity and PostGIS verification
- Spatial data loading from multiple formats
- Spatial analysis using PostGIS functions
- Data export and validation capabilities

Usage:
    python calculate_grade.py --results test-results.xml --output grade-report.json
    python calculate_grade.py --help

Features:
- Comprehensive test result analysis
- Function-specific performance evaluation
- Database operation validation
- Professional feedback generation
- GitHub Actions integration
- Detailed error reporting and debugging assistance

Author: GIST 604B Course Materials
Version: 1.0.0
Date: December 2024
"""

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class PostGISAssignmentGrader:
    """
    Professional grading system for PostGIS fundamentals assignment.

    Evaluates student implementations of spatial database operations
    including connectivity, data loading, spatial analysis, and export.
    """

    def __init__(self, test_results_path: str, output_path: str = "grade-report.json"):
        """
        Initialize the grading system.

        Args:
            test_results_path: Path to pytest XML results file
            output_path: Path for grade report output
        """
        self.test_results_path = Path(test_results_path)
        self.output_path = Path(output_path)
        self.total_points = 20

        # Function-specific grading weights
        self.function_weights = {
            'connect_to_postgis': {
                'points': 5,
                'weight': 0.25,
                'description': 'Database connection and PostGIS verification'
            },
            'load_spatial_data': {
                'points': 5,
                'weight': 0.25,
                'description': 'Spatial data loading from CSV and GeoJSON'
            },
            'analyze_spatial_relationships': {
                'points': 5,
                'weight': 0.25,
                'description': 'Spatial analysis using PostGIS functions'
            },
            'export_analysis_results': {
                'points': 5,
                'weight': 0.25,
                'description': 'Multi-format data export and validation'
            }
        }

        # Grade scale
        self.grade_scale = {
            90: 'A', 80: 'B', 70: 'C', 60: 'D', 0: 'F'
        }

    def parse_test_results(self) -> Dict[str, Any]:
        """
        Parse pytest XML results and extract detailed test information.

        Returns:
            Dict containing parsed test results and statistics
        """
        if not self.test_results_path.exists():
            logger.error(f"Test results file not found: {self.test_results_path}")
            return self._create_empty_results()

        try:
            tree = ET.parse(self.test_results_path)
            root = tree.getroot()

            # Extract overall test statistics
            total_tests = int(root.get('tests', 0))
            failures = int(root.get('failures', 0))
            errors = int(root.get('errors', 0))
            skipped = int(root.get('skipped', 0))
            passed = total_tests - failures - errors - skipped

            # Parse individual test cases
            test_cases = []
            function_results = {}

            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name', 'unknown')
                classname = testcase.get('classname', 'unknown')
                test_time = float(testcase.get('time', 0))

                # Determine test status
                status = 'passed'
                error_message = None
                error_type = None

                failure = testcase.find('failure')
                error = testcase.find('error')
                skip = testcase.find('skipped')

                if failure is not None:
                    status = 'failed'
                    error_message = failure.text
                    error_type = failure.get('type', 'AssertionError')
                elif error is not None:
                    status = 'error'
                    error_message = error.text
                    error_type = error.get('type', 'Exception')
                elif skip is not None:
                    status = 'skipped'
                    error_message = skip.text

                test_case = {
                    'name': test_name,
                    'classname': classname,
                    'status': status,
                    'time': test_time,
                    'error_message': error_message,
                    'error_type': error_type
                }

                test_cases.append(test_case)

                # Categorize by function
                function_name = self._extract_function_name(test_name)
                if function_name not in function_results:
                    function_results[function_name] = {
                        'tests': [],
                        'passed': 0,
                        'failed': 0,
                        'errors': 0,
                        'total_time': 0
                    }

                function_results[function_name]['tests'].append(test_case)
                function_results[function_name]['total_time'] += test_time

                if status == 'passed':
                    function_results[function_name]['passed'] += 1
                elif status == 'failed':
                    function_results[function_name]['failed'] += 1
                elif status == 'error':
                    function_results[function_name]['errors'] += 1

            return {
                'total_tests': total_tests,
                'passed': passed,
                'failed': failures,
                'errors': errors,
                'skipped': skipped,
                'test_cases': test_cases,
                'function_results': function_results,
                'success_rate': (passed / total_tests * 100) if total_tests > 0 else 0
            }

        except ET.ParseError as e:
            logger.error(f"Error parsing XML results: {e}")
            return self._create_empty_results()
        except Exception as e:
            logger.error(f"Unexpected error parsing results: {e}")
            return self._create_empty_results()

    def _extract_function_name(self, test_name: str) -> str:
        """
        Extract the function name being tested from the test name.

        Args:
            test_name: Name of the test case

        Returns:
            Function name or 'unknown' if not identifiable
        """
        # Map test patterns to function names
        function_mappings = {
            'connect': 'connect_to_postgis',
            'connection': 'connect_to_postgis',
            'load': 'load_spatial_data',
            'data_loading': 'load_spatial_data',
            'spatial_data': 'load_spatial_data',
            'analyz': 'analyze_spatial_relationships',  # Handles analyze/analyse
            'spatial_relationships': 'analyze_spatial_relationships',
            'spatial_analysis': 'analyze_spatial_relationships',
            'export': 'export_analysis_results',
            'results': 'export_analysis_results'
        }

        test_lower = test_name.lower()

        for pattern, function_name in function_mappings.items():
            if pattern in test_lower:
                return function_name

        return 'unknown'

    def _create_empty_results(self) -> Dict[str, Any]:
        """Create empty results structure for error cases."""
        return {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'test_cases': [],
            'function_results': {},
            'success_rate': 0
        }

    def calculate_grade(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive grade based on test results and function performance.

        Args:
            test_results: Parsed test results from parse_test_results()

        Returns:
            Dict containing grade calculation and breakdown
        """
        if test_results['total_tests'] == 0:
            logger.warning("No tests found - assigning zero grade")
            return self._create_zero_grade()

        function_scores = {}
        total_weighted_score = 0
        total_possible_points = 0

        # Calculate score for each function
        for function_name, config in self.function_weights.items():
            function_result = test_results['function_results'].get(function_name, {
                'tests': [], 'passed': 0, 'failed': 0, 'errors': 0, 'total_time': 0
            })

            total_function_tests = len(function_result['tests'])
            passed_tests = function_result['passed']

            if total_function_tests == 0:
                # No tests found for this function
                function_score = 0
                success_rate = 0
                logger.warning(f"No tests found for {function_name}")
            else:
                success_rate = (passed_tests / total_function_tests) * 100
                function_score = (passed_tests / total_function_tests) * config['points']

            function_scores[function_name] = {
                'points_possible': config['points'],
                'points_earned': round(function_score, 2),
                'success_rate': round(success_rate, 1),
                'tests_passed': passed_tests,
                'tests_total': total_function_tests,
                'tests_failed': function_result['failed'],
                'tests_errors': function_result['errors'],
                'avg_execution_time': round(function_result['total_time'] / max(total_function_tests, 1), 3),
                'description': config['description']
            }

            total_weighted_score += function_score
            total_possible_points += config['points']

        # Calculate overall grade
        if total_possible_points == 0:
            percentage = 0
        else:
            percentage = (total_weighted_score / total_possible_points) * 100

        letter_grade = self._calculate_letter_grade(percentage)

        # Performance analysis
        performance_analysis = self._analyze_performance(test_results, function_scores)

        return {
            'total_points': self.total_points,
            'points_possible': total_possible_points,
            'points_earned': round(total_weighted_score, 2),
            'percentage': round(percentage, 1),
            'letter_grade': letter_grade,
            'function_scores': function_scores,
            'overall_stats': {
                'tests_total': test_results['total_tests'],
                'tests_passed': test_results['passed'],
                'tests_failed': test_results['failed'],
                'tests_errors': test_results['errors'],
                'tests_skipped': test_results['skipped'],
                'success_rate': round(test_results['success_rate'], 1)
            },
            'performance_analysis': performance_analysis,
            'timestamp': datetime.now().isoformat(),
            'grading_criteria': self.function_weights
        }

    def _calculate_letter_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade."""
        for threshold, grade in sorted(self.grade_scale.items(), reverse=True):
            if percentage >= threshold:
                return grade
        return 'F'

    def _create_zero_grade(self) -> Dict[str, Any]:
        """Create a zero grade structure for cases with no valid test results."""
        return {
            'total_points': self.total_points,
            'points_possible': self.total_points,
            'points_earned': 0,
            'percentage': 0,
            'letter_grade': 'F',
            'function_scores': {name: {
                'points_possible': config['points'],
                'points_earned': 0,
                'success_rate': 0,
                'tests_passed': 0,
                'tests_total': 0,
                'tests_failed': 0,
                'tests_errors': 0,
                'avg_execution_time': 0,
                'description': config['description']
            } for name, config in self.function_weights.items()},
            'overall_stats': {
                'tests_total': 0, 'tests_passed': 0, 'tests_failed': 0,
                'tests_errors': 0, 'tests_skipped': 0, 'success_rate': 0
            },
            'performance_analysis': {
                'strengths': [],
                'areas_for_improvement': ['No test results found - check implementation and test execution'],
                'recommendations': [
                    'Verify all functions are implemented in src/postgis_basics.py',
                    'Ensure Docker PostgreSQL database is running',
                    'Check database connection parameters',
                    'Run tests locally: pytest tests/ -v'
                ]
            },
            'timestamp': datetime.now().isoformat(),
            'grading_criteria': self.function_weights
        }

    def _analyze_performance(self, test_results: Dict[str, Any],
                           function_scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance and provide recommendations.

        Args:
            test_results: Parsed test results
            function_scores: Calculated function scores

        Returns:
            Dict containing performance analysis and recommendations
        """
        strengths = []
        areas_for_improvement = []
        recommendations = []

        # Analyze overall performance
        overall_success = test_results['success_rate']

        if overall_success >= 90:
            strengths.append("Excellent overall implementation with high test success rate")
        elif overall_success >= 70:
            strengths.append("Good foundation with solid test coverage")
        else:
            areas_for_improvement.append(f"Low overall success rate ({overall_success:.1f}%)")

        # Analyze function-specific performance
        for func_name, scores in function_scores.items():
            success_rate = scores['success_rate']

            if success_rate >= 90:
                strengths.append(f"Strong {func_name} implementation ({success_rate:.1f}% success)")
            elif success_rate >= 70:
                strengths.append(f"Good {func_name} foundation ({success_rate:.1f}% success)")
            elif success_rate > 0:
                areas_for_improvement.append(f"{func_name}: {success_rate:.1f}% success - needs improvement")
            else:
                areas_for_improvement.append(f"{func_name}: No successful tests - requires implementation")

        # Generate specific recommendations
        if function_scores['connect_to_postgis']['success_rate'] < 70:
            recommendations.extend([
                "Database Connection Issues:",
                "- Verify PostgreSQL with PostGIS is running (docker-compose up -d)",
                "- Check connection parameters (host, port, database name, credentials)",
                "- Ensure PostGIS extension is enabled (SELECT PostGIS_Version();)"
            ])

        if function_scores['load_spatial_data']['success_rate'] < 70:
            recommendations.extend([
                "Spatial Data Loading Issues:",
                "- Verify table creation SQL syntax (geometry column definitions)",
                "- Check CSV and GeoJSON file reading and parsing",
                "- Ensure proper SRID setting (EPSG:4326)",
                "- Verify spatial index creation syntax"
            ])

        if function_scores['analyze_spatial_relationships']['success_rate'] < 70:
            recommendations.extend([
                "Spatial Analysis Issues:",
                "- Review PostGIS function syntax (ST_Contains, ST_Distance, ST_Area)",
                "- Check coordinate system handling and transformations",
                "- Verify spatial query construction and execution",
                "- Ensure proper unit conversions (meters to kilometers)"
            ])

        if function_scores['export_analysis_results']['success_rate'] < 70:
            recommendations.extend([
                "Data Export Issues:",
                "- Verify output directory creation and file writing",
                "- Check CSV export with coordinate extraction (ST_X, ST_Y)",
                "- Ensure GeoJSON export using ST_AsGeoJSON",
                "- Validate export file formats and content"
            ])

        # Performance recommendations
        avg_execution_times = [scores['avg_execution_time'] for scores in function_scores.values()]
        if any(time > 5.0 for time in avg_execution_times):
            recommendations.append("Consider adding spatial indexes for better query performance")

        # General recommendations if no specific issues identified
        if not recommendations and overall_success < 90:
            recommendations.extend([
                "General Improvement Areas:",
                "- Review PostGIS documentation and examples",
                "- Test functions individually using interactive Python sessions",
                "- Check database logs for detailed error messages",
                "- Practice with spatial SQL queries in pgAdmin or psql"
            ])

        return {
            'strengths': strengths,
            'areas_for_improvement': areas_for_improvement,
            'recommendations': recommendations,
            'performance_summary': f"Overall test success rate: {overall_success:.1f}%"
        }

    def generate_feedback(self, grade_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive human-readable feedback.

        Args:
            grade_data: Complete grade calculation results

        Returns:
            Formatted feedback string
        """
        feedback = []

        # Header
        feedback.append("=" * 60)
        feedback.append("POSTGIS FUNDAMENTALS ASSIGNMENT - GRADING REPORT")
        feedback.append("=" * 60)

        # Overall grade
        feedback.append(f"\n🎓 FINAL GRADE: {grade_data['letter_grade']} ({grade_data['percentage']:.1f}%)")
        feedback.append(f"📊 POINTS EARNED: {grade_data['points_earned']}/{grade_data['total_points']}")

        # Test summary
        stats = grade_data['overall_stats']
        feedback.append(f"🧪 TESTS: {stats['tests_passed']}/{stats['tests_total']} passed")
        if stats['tests_failed'] > 0:
            feedback.append(f"❌ FAILED: {stats['tests_failed']}")
        if stats['tests_errors'] > 0:
            feedback.append(f"⚠️  ERRORS: {stats['tests_errors']}")

        # Function breakdown
        feedback.append(f"\n📋 FUNCTION PERFORMANCE BREAKDOWN:")
        feedback.append("-" * 60)

        for func_name, scores in grade_data['function_scores'].items():
            status_icon = "✅" if scores['success_rate'] >= 80 else "⚠️" if scores['success_rate'] >= 50 else "❌"
            feedback.append(f"{status_icon} {func_name}:")
            feedback.append(f"   Points: {scores['points_earned']:.1f}/{scores['points_possible']}")
            feedback.append(f"   Success Rate: {scores['success_rate']:.1f}%")
            feedback.append(f"   Tests: {scores['tests_passed']}/{scores['tests_total']} passed")
            feedback.append(f"   Description: {scores['description']}")

            if scores['tests_failed'] > 0 or scores['tests_errors'] > 0:
                feedback.append(f"   Issues: {scores['tests_failed']} failed, {scores['tests_errors']} errors")

            feedback.append("")

        # Performance analysis
        analysis = grade_data['performance_analysis']

        if analysis['strengths']:
            feedback.append("🌟 STRENGTHS:")
            for strength in analysis['strengths']:
                feedback.append(f"  ✓ {strength}")
            feedback.append("")

        if analysis['areas_for_improvement']:
            feedback.append("🔧 AREAS FOR IMPROVEMENT:")
            for area in analysis['areas_for_improvement']:
                feedback.append(f"  • {area}")
            feedback.append("")

        if analysis['recommendations']:
            feedback.append("💡 RECOMMENDATIONS:")
            for rec in analysis['recommendations']:
                if rec.endswith(":"):
                    feedback.append(f"\n{rec}")
                else:
                    feedback.append(f"  • {rec}")
            feedback.append("")

        # Professional context
        feedback.append("🚀 PROFESSIONAL CONTEXT:")
        feedback.append("  These PostGIS skills are essential for:")
        feedback.append("  • Enterprise GIS database management")
        feedback.append("  • Multi-user spatial data workflows")
        feedback.append("  • Web GIS application backends")
        feedback.append("  • Large-scale spatial analysis projects")
        feedback.append("  • Integration with business systems")

        # Footer
        feedback.append(f"\nReport generated: {grade_data['timestamp']}")
        feedback.append("=" * 60)

        return "\n".join(feedback)

    def output_for_github_actions(self, grade_data: Dict[str, Any]):
        """
        Output environment variables for GitHub Actions workflow.

        Args:
            grade_data: Complete grade calculation results
        """
        if 'GITHUB_ENV' in os.environ:
            env_file = os.environ['GITHUB_ENV']
            try:
                with open(env_file, 'a') as f:
                    f.write(f"LETTER_GRADE={grade_data['letter_grade']}\n")
                    f.write(f"GRADE_PERCENTAGE={grade_data['percentage']:.1f}\n")
                    f.write(f"POINTS={grade_data['points_earned']}\n")
                    f.write(f"TESTS_PASSED={grade_data['overall_stats']['tests_passed']}\n")
                    f.write(f"TESTS_TOTAL={grade_data['overall_stats']['tests_total']}\n")

                    if grade_data['overall_stats']['tests_total'] > grade_data['overall_stats']['tests_passed']:
                        f.write("TESTS_FAILED=true\n")
                    else:
                        f.write("TESTS_FAILED=false\n")

                logger.info("✅ GitHub Actions environment variables set successfully")
            except Exception as e:
                logger.error(f"❌ Failed to set GitHub Actions environment variables: {e}")
        else:
            logger.info("Not running in GitHub Actions - skipping environment variable output")

    def save_grade_report(self, grade_data: Dict[str, Any]):
        """
        Save comprehensive grade report to JSON file.

        Args:
            grade_data: Complete grade calculation results
        """
        try:
            # Ensure output directory exists
            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            # Add metadata
            report = {
                'assignment': 'PostGIS Fundamentals',
                'course': 'GIST 604B - Open Source GIS Programming',
                'module': 'Module 6 - PostGIS Spatial Database',
                'version': '1.0.0',
                **grade_data
            }

            with open(self.output_path, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Grade report saved to: {self.output_path}")

        except Exception as e:
            logger.error(f"❌ Failed to save grade report: {e}")
            raise

    def run(self) -> Dict[str, Any]:
        """
        Execute complete grading workflow.

        Returns:
            Complete grade data dictionary
        """
        logger.info("🚀 Starting PostGIS assignment grading...")
        logger.info(f"📋 Test results: {self.test_results_path}")
        logger.info(f"💾 Output file: {self.output_path}")

        # Parse test results
        logger.info("📊 Parsing test results...")
        test_results = self.parse_test_results()

        if test_results['total_tests'] == 0:
            logger.warning("⚠️  No tests found in results file")
        else:
            logger.info(f"✅ Found {test_results['total_tests']} tests")

        # Calculate grade
        logger.info("🔢 Calculating grade...")
        grade_data = self.calculate_grade(test_results)

        # Generate feedback
        logger.info("📝 Generating feedback...")
        feedback = self.generate_feedback(grade_data)
        print(feedback)

        # Save outputs
        logger.info("💾 Saving grade report...")
        self.save_grade_report(grade_data)

        # Output for GitHub Actions
        logger.info("🔧 Setting GitHub Actions outputs...")
        self.output_for_github_actions(grade_data)

        logger.info("✅ Grading completed successfully!")
        return grade_data


def main():
    """Command-line interface for the grading system."""
    parser = argparse.ArgumentParser(
        description="PostGIS Fundamentals Assignment - Automated Grading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python calculate_grade.py --results test-results.xml
  python calculate_grade.py --results test-results.xml --output my-grade.json
  python calculate_grade.py --help

This tool analyzes pytest XML results and generates comprehensive grades
for PostGIS database operations including connectivity, data loading,
spatial analysis, and export functionality.
        """
    )

    parser.add_argument(
        '--results', '-r',
        required=True,
        help='Path to pytest XML results file'
    )

    parser.add_argument(
        '--output', '-o',
        default='grade-report.json',
        help='Output path for grade report JSON (default: grade-report.json)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='PostGIS Assignment Grader v1.0.0'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        grader = PostGISAssignmentGrader(args.results, args.output)
        grade_data = grader.run()

        # Exit with appropriate code
        if grade_data['letter_grade'] in ['A', 'B']:
            sys.exit(0)
        elif grade_data['letter_grade'] == 'C':
            sys.exit(1)  # Warning level
        else:
            sys.exit(2)  # Needs significant work

    except FileNotFoundError as e:
        logger.error(f"❌ File not found: {e}")
        sys.exit(3)
    except Exception as e:
        logger.error(f"❌ Grading failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(4)


if __name__ == "__main__":
    main()
