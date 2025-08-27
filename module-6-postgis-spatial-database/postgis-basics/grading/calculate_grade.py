#!/usr/bin/env python3
"""
PostGIS Basics Assignment - Automated Grading Script

Calculates grades for 8 PostGIS spatial queries (2.5 points each = 20 total points)
Generates detailed grade reports and sets environment variables for CI/CD.

Usage:
    python calculate_grade.py
    python calculate_grade.py --output grade-report.json
    python calculate_grade.py --verbose

Author: GIST 604B Module 6 - PostGIS Fundamentals
"""

import json
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class PostGISGradingEngine:
    """Professional grading engine for PostGIS Basics assignment."""

    # Define the 8 PostGIS query categories (2.5 points each)
    QUERY_CATEGORIES = {
        'spatial_inspection': {
            'name': '01_spatial_inspection',
            'points': 2.5,
            'description': 'Spatial data inspection with PostGIS functions',
            'concepts': ['ST_GeometryType', 'ST_SRID', 'ST_AsText', 'spatial metadata'],
            'test_method': 'test_01_spatial_inspection'
        },
        'geometry_creation': {
            'name': '02_geometry_creation',
            'points': 2.5,
            'description': 'Creating geometries with PostGIS functions',
            'concepts': ['ST_MakePoint', 'ST_GeomFromText', 'ST_SetSRID', 'WKT format'],
            'test_method': 'test_02_geometry_creation'
        },
        'spatial_measurements': {
            'name': '03_spatial_measurements',
            'points': 2.5,
            'description': 'Calculating spatial measurements',
            'concepts': ['ST_Distance_Sphere', 'ST_Area', 'ST_Length', 'coordinate projection'],
            'test_method': 'test_03_spatial_measurements'
        },
        'coordinate_transformation': {
            'name': '04_coordinate_transformation',
            'points': 2.5,
            'description': 'Transforming between coordinate reference systems',
            'concepts': ['ST_Transform', 'EPSG codes', 'ST_X', 'ST_Y', 'CRS conversion'],
            'test_method': 'test_04_coordinate_transformation'
        },
        'spatial_relationships': {
            'name': '05_spatial_relationships',
            'points': 2.5,
            'description': 'Querying spatial relationships between geometries',
            'concepts': ['ST_Within', 'ST_Intersects', 'ST_DWithin', 'spatial joins'],
            'test_method': 'test_05_spatial_relationships'
        },
        'buffer_operations': {
            'name': '06_buffer_operations',
            'points': 2.5,
            'description': 'Creating and analyzing buffer zones',
            'concepts': ['ST_Buffer', 'spatial analysis', 'CTEs', 'proximity analysis'],
            'test_method': 'test_06_buffer_operations'
        },
        'spatial_joins': {
            'name': '07_spatial_joins',
            'points': 2.5,
            'description': 'Advanced spatial joins between multiple datasets',
            'concepts': ['spatial JOIN', 'ST_Intersection', 'aggregation', 'DISTINCT ON'],
            'test_method': 'test_07_spatial_joins'
        },
        'complex_analysis': {
            'name': '08_complex_analysis',
            'points': 2.5,
            'description': 'Multi-step complex spatial analysis',
            'concepts': ['WITH clauses', 'ST_Union', 'window functions', 'comprehensive analysis'],
            'test_method': 'test_08_complex_analysis'
        }
    }

    # Assignment metadata
    TOTAL_POINTS = 20.0
    ASSIGNMENT_NAME = "PostGIS Basics - Spatial Database Fundamentals"
    MODULE_NAME = "Module 6"

    def __init__(self):
        """Initialize the PostGIS grading engine."""
        self.assignment_dir = Path(__file__).parent.parent
        self.test_results = {}
        self.grade_data = {}

    def run_tests(self) -> Dict[str, Any]:
        """
        Run pytest tests and capture results.

        Returns:
            Dictionary containing test results and metadata
        """
        print("🧪 Running PostGIS assignment tests...")

        try:
            # Run tests with JSON output for parsing
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                str(self.assignment_dir / 'test_assignment.py'),
                '-v', '--tb=short', '--json-report',
                '--json-report-file=test-results.json'
            ], capture_output=True, text=True, cwd=self.assignment_dir)

            # Parse test output
            self.test_results = self.parse_test_output(result.stdout, result.stderr)

            # Try to load detailed JSON results if available
            json_results_file = self.assignment_dir / 'test-results.json'
            if json_results_file.exists():
                try:
                    with open(json_results_file, 'r') as f:
                        json_data = json.load(f)
                        self.test_results['detailed_results'] = json_data
                except Exception as e:
                    print(f"⚠️  Could not parse JSON test results: {e}")

            return self.test_results

        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'error': str(e)
            }

    def parse_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse pytest output to extract test results.

        Args:
            stdout: Standard output from pytest
            stderr: Standard error from pytest

        Returns:
            Parsed test results dictionary
        """
        results = {
            'stdout': stdout,
            'stderr': stderr,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'test_details': {}
        }

        # Parse test outcomes from stdout
        lines = stdout.split('\n')

        for line in lines:
            line = line.strip()

            # Count test outcomes
            if 'PASSED' in line:
                results['passed_tests'] += 1
                results['total_tests'] += 1
            elif 'FAILED' in line:
                results['failed_tests'] += 1
                results['total_tests'] += 1
            elif 'SKIPPED' in line:
                results['skipped_tests'] += 1
                results['total_tests'] += 1

            # Extract individual test details
            if '::test_' in line and ('PASSED' in line or 'FAILED' in line or 'SKIPPED' in line):
                test_name = line.split('::')[-1].split(' ')[0]
                status = 'PASSED' if 'PASSED' in line else 'FAILED' if 'FAILED' in line else 'SKIPPED'
                results['test_details'][test_name] = status

        return results

    def sql_file_exists(self, filename: str) -> bool:
        """Check if SQL file exists."""
        return (self.assignment_dir / 'sql' / filename).exists()

    def is_template_completed(self, filename: str) -> bool:
        """
        Check if SQL template has been completed (no blanks remaining).

        Args:
            filename: Name of SQL file to check

        Returns:
            True if template is completed, False otherwise
        """
        sql_file = self.assignment_dir / 'sql' / filename
        if not sql_file.exists():
            return False

        try:
            with open(sql_file, 'r') as f:
                content = f.read()

            # Check for common template placeholders
            placeholders = ['_____', '____', 'TODO:', 'HINT:']
            return not any(placeholder in content for placeholder in placeholders)

        except Exception:
            return False

    def count_passed_tests(self) -> int:
        """Count number of passed tests."""
        return self.test_results.get('passed_tests', 0)

    def count_completed_templates(self) -> int:
        """
        Count number of completed SQL templates.

        Returns:
            Number of completed templates
        """
        completed = 0
        for category_data in self.QUERY_CATEGORIES.values():
            filename = f"{category_data['name']}.sql"
            if self.is_template_completed(filename):
                completed += 1
        return completed

    def calculate_grade(self) -> Dict[str, Any]:
        """
        Calculate comprehensive grade based on test results and template completion.

        Returns:
            Complete grade breakdown and analysis
        """
        print("📊 Calculating PostGIS assignment grade...")

        # Run tests to get current results
        self.run_tests()

        # Initialize grade structure
        grade_data = {
            'assignment': self.ASSIGNMENT_NAME,
            'module': self.MODULE_NAME,
            'total_points': 0,
            'possible_points': self.TOTAL_POINTS,
            'percentage': 0,
            'letter_grade': 'F',
            'category_breakdown': {},
            'completion_status': {},
            'test_summary': {},
            'feedback': []
        }

        # Analyze each query category
        for category_key, category_info in self.QUERY_CATEGORIES.items():
            filename = f"{category_info['name']}.sql"
            test_method = category_info['test_method']
            points = category_info['points']

            # Check template completion
            template_completed = self.is_template_completed(filename)
            file_exists = self.sql_file_exists(filename)

            # Check test results
            test_passed = self.test_results.get('test_details', {}).get(test_method, 'UNKNOWN') == 'PASSED'

            # Calculate points for this category
            category_points = 0
            if file_exists and template_completed and test_passed:
                category_points = points
            elif file_exists and template_completed:
                category_points = points * 0.5  # Partial credit for completion without passing tests

            # Store category breakdown
            grade_data['category_breakdown'][category_key] = {
                'earned': category_points,
                'possible': points,
                'percentage': (category_points / points) * 100 if points > 0 else 0,
                'status': 'Complete' if test_passed else 'Partial' if template_completed else 'Incomplete',
                'file_exists': file_exists,
                'template_completed': template_completed,
                'test_passed': test_passed,
                'description': category_info['description'],
                'concepts': category_info['concepts']
            }

            grade_data['total_points'] += category_points

        # Calculate final grade metrics
        grade_data['percentage'] = (grade_data['total_points'] / grade_data['possible_points']) * 100
        grade_data['letter_grade'] = self.calculate_letter_grade(grade_data['percentage'])

        # Add test summary
        grade_data['test_summary'] = {
            'total_tests': self.test_results.get('total_tests', 0),
            'passed_tests': self.test_results.get('passed_tests', 0),
            'failed_tests': self.test_results.get('failed_tests', 0),
            'skipped_tests': self.test_results.get('skipped_tests', 0),
            'test_success_rate': (self.test_results.get('passed_tests', 0) / max(self.test_results.get('total_tests', 1), 1)) * 100
        }

        # Add completion status
        grade_data['completion_status'] = {
            'completed_queries': self.count_completed_templates(),
            'total_queries': len(self.QUERY_CATEGORIES),
            'completion_rate': (self.count_completed_templates() / len(self.QUERY_CATEGORIES)) * 100
        }

        # Generate feedback
        grade_data['feedback'] = self.generate_feedback(grade_data)

        self.grade_data = grade_data
        return grade_data

    def calculate_letter_grade(self, percentage: float) -> str:
        """
        Convert percentage to letter grade.

        Args:
            percentage: Grade percentage (0-100)

        Returns:
            Letter grade (A, B, C, D, F)
        """
        if percentage >= 93:
            return 'A'
        elif percentage >= 90:
            return 'A-'
        elif percentage >= 87:
            return 'B+'
        elif percentage >= 83:
            return 'B'
        elif percentage >= 80:
            return 'B-'
        elif percentage >= 77:
            return 'C+'
        elif percentage >= 73:
            return 'C'
        elif percentage >= 70:
            return 'C-'
        elif percentage >= 67:
            return 'D+'
        elif percentage >= 63:
            return 'D'
        elif percentage >= 60:
            return 'D-'
        else:
            return 'F'

    def generate_feedback(self, grade_data: Dict[str, Any]) -> List[str]:
        """
        Generate detailed feedback based on grade analysis.

        Args:
            grade_data: Complete grade breakdown

        Returns:
            List of feedback messages
        """
        feedback = []

        # Overall performance feedback
        percentage = grade_data['percentage']
        if percentage >= 90:
            feedback.append("🎉 Excellent work! You've mastered PostGIS spatial database fundamentals.")
        elif percentage >= 80:
            feedback.append("👍 Good job! You have a solid understanding of PostGIS concepts.")
        elif percentage >= 70:
            feedback.append("📚 Decent progress. Review the concepts and improve your spatial queries.")
        else:
            feedback.append("⚠️  Need improvement. Focus on completing templates and understanding PostGIS functions.")

        # Template completion feedback
        completion_rate = grade_data['completion_status']['completion_rate']
        if completion_rate < 100:
            incomplete_count = 8 - grade_data['completion_status']['completed_queries']
            feedback.append(f"📝 Complete {incomplete_count} remaining SQL templates to improve your grade.")

        # Test-specific feedback
        test_success_rate = grade_data['test_summary']['test_success_rate']
        if test_success_rate < 75:
            feedback.append("🔧 Review your spatial SQL syntax - many queries have testing issues.")

        # Category-specific feedback
        failed_categories = []
        for category_key, category_data in grade_data['category_breakdown'].items():
            if category_data['status'] == 'Incomplete':
                failed_categories.append(self.QUERY_CATEGORIES[category_key]['description'])

        if failed_categories:
            feedback.append(f"🎯 Focus on these areas: {', '.join(failed_categories[:3])}")

        # PostGIS-specific feedback
        if percentage < 80:
            feedback.append("📖 Review PostGIS documentation for ST_ functions and spatial concepts.")
            feedback.append("🗄️ Practice with the provided spatial datasets to build confidence.")

        return feedback

    def save_grade_report(self, output_file: str = "grade-report.json") -> None:
        """
        Save detailed grade report to JSON file.

        Args:
            output_file: Output filename for grade report
        """
        if not self.grade_data:
            self.calculate_grade()

        report_data = {
            **self.grade_data,
            'generated_at': datetime.now().isoformat(),
            'assignment_metadata': {
                'total_queries': len(self.QUERY_CATEGORIES),
                'points_per_query': 2.5,
                'assignment_type': 'PostGIS Spatial Database Fundamentals',
                'difficulty_level': 'Foundation (⭐⭐)',
                'estimated_time': '2-3 hours'
            },
            'raw_test_output': {
                'stdout': self.test_results.get('stdout', ''),
                'stderr': self.test_results.get('stderr', '')
            }
        }

        output_path = self.assignment_dir / output_file
        try:
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"📄 Grade report saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving grade report: {e}")

    def set_environment_variables(self) -> None:
        """Set environment variables for CI/CD pipeline integration."""
        if not self.grade_data:
            self.calculate_grade()

        # Set GitHub Actions environment variables
        env_vars = {
            'POSTGIS_ASSIGNMENT_SCORE': str(self.grade_data['total_points']),
            'POSTGIS_ASSIGNMENT_PERCENTAGE': str(round(self.grade_data['percentage'], 2)),
            'POSTGIS_ASSIGNMENT_LETTER_GRADE': self.grade_data['letter_grade'],
            'POSTGIS_ASSIGNMENT_STATUS': 'PASSED' if self.grade_data['percentage'] >= 70 else 'FAILED',
            'POSTGIS_COMPLETED_QUERIES': str(self.grade_data['completion_status']['completed_queries']),
            'POSTGIS_TOTAL_QUERIES': str(len(self.QUERY_CATEGORIES)),
            'POSTGIS_TEST_SUCCESS_RATE': str(round(self.grade_data['test_summary']['test_success_rate'], 2))
        }

        # Write to GitHub Actions environment file if in CI
        github_env_file = os.getenv('GITHUB_ENV')
        if github_env_file:
            try:
                with open(github_env_file, 'a') as f:
                    for key, value in env_vars.items():
                        f.write(f"{key}={value}\n")
                print("✅ Environment variables set for CI/CD")
            except Exception as e:
                print(f"⚠️  Could not write to GITHUB_ENV: {e}")

        # Set local environment variables
        for key, value in env_vars.items():
            os.environ[key] = value

    def print_summary(self) -> None:
        """Print a comprehensive grade summary to console."""
        if not self.grade_data:
            self.calculate_grade()

        print("\n" + "="*70)
        print(f"📊 {self.ASSIGNMENT_NAME} - GRADE REPORT")
        print("="*70)

        print(f"\n🎯 OVERALL GRADE")
        print(f"   Score: {self.grade_data['total_points']:.1f} / {self.grade_data['possible_points']:.1f} points")
        print(f"   Percentage: {self.grade_data['percentage']:.1f}%")
        print(f"   Letter Grade: {self.grade_data['letter_grade']}")

        print(f"\n📈 PROGRESS SUMMARY")
        print(f"   Completed Queries: {self.grade_data['completion_status']['completed_queries']} / 8")
        print(f"   Passed Tests: {self.grade_data['test_summary']['passed_tests']} / {self.grade_data['test_summary']['total_tests']}")
        print(f"   Completion Rate: {self.grade_data['completion_status']['completion_rate']:.1f}%")

        print(f"\n🗄️ POSTGIS QUERY BREAKDOWN")
        for category_key, category_data in self.grade_data['category_breakdown'].items():
            status_icon = "✅" if category_data['status'] == 'Complete' else "⚠️" if category_data['status'] == 'Partial' else "❌"
            print(f"   {status_icon} {category_data['description']}: {category_data['earned']:.1f}/{category_data['possible']:.1f} pts")

        print(f"\n💬 FEEDBACK")
        for feedback_item in self.grade_data['feedback']:
            print(f"   • {feedback_item}")

        print("\n" + "="*70)


def main():
    """Main function for command-line execution."""
    parser = argparse.ArgumentParser(description='PostGIS Basics Assignment Grading Engine')
    parser.add_argument('--output', '-o', default='grade-report.json',
                       help='Output file for grade report (default: grade-report.json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--no-summary', action='store_true',
                       help='Skip printing grade summary')

    args = parser.parse_args()

    # Initialize grading engine
    grader = PostGISGradingEngine()

    try:
        # Calculate grade
        grade_data = grader.calculate_grade()

        # Save report
        grader.save_grade_report(args.output)

        # Set environment variables for CI/CD
        grader.set_environment_variables()

        # Print summary unless suppressed
        if not args.no_summary:
            grader.print_summary()

        # Exit with appropriate code
        if grade_data['percentage'] >= 70:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure

    except Exception as e:
        print(f"❌ Fatal error in grading engine: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)  # Error


if __name__ == '__main__':
    main()
