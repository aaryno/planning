#!/usr/bin/env python3
"""
CI/CD Grading Script for Python Rasterio Assignment
==================================================

This script is designed to run in CI/CD pipelines (GitHub Actions) to automatically
grade student assignments based on pytest results.

IMPORTANT: Students should NOT run this script locally!
Students should use: pytest tests/ -v

This script:
1. Parses pytest XML output
2. Calculates grades based on test results
3. Generates structured output for automated systems
4. Provides detailed feedback for continuous integration

Usage (CI/CD only):
    python calculate_grade.py --results test-results.xml --output grade.json

Environment Variables:
    GITHUB_ENV: GitHub Actions environment file path
    CI: Set to 'true' in CI environments
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class RasterioAssignmentGrader:
    """Automated grader for Python Rasterio assignment."""

    # Grading rubric configuration
    TOTAL_POINTS = 20
    GRADE_THRESHOLDS = {
        'A': 90,
        'B': 80,
        'C': 70,
        'D': 60,
        'F': 0
    }

    # Test categories and their point values (simplified rasterio assignment)
    TEST_CATEGORIES = {
        'test_load_and_explore': {'name': 'Load and Explore Raster', 'points': 5},
        'test_calculate_statistics': {'name': 'Calculate Raster Statistics', 'points': 5},
        'test_extract_subset': {'name': 'Extract Raster Subset', 'points': 5},
        'test_visualize_raster': {'name': 'Visualize Raster Data', 'points': 3},
        'test_code_quality': {'name': 'Code Quality & Integration', 'points': 2}
    }

    def __init__(self, results_file: str = 'test-results.xml'):
        """
        Initialize grader with test results file.

        Args:
            results_file: Path to pytest XML results file
        """
        self.results_file = results_file
        self.is_ci = os.getenv('CI', '').lower() == 'true'

    def parse_test_results(self) -> Dict:
        """
        Parse pytest XML results into structured data.

        Returns:
            Dict containing test results and metadata
        """
        if not Path(self.results_file).exists():
            return {
                'tests': [],
                'summary': {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'error': 0
                },
                'execution_time': 0.0,
                'error': f'Test results file {self.results_file} not found'
            }

        try:
            tree = ET.parse(self.results_file)
            root = tree.getroot()

            tests = []
            summary = {
                'total': int(root.get('tests', 0)),
                'passed': 0,
                'failed': int(root.get('failures', 0)),
                'skipped': int(root.get('skipped', 0)),
                'error': int(root.get('errors', 0))
            }

            # Parse individual test cases
            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name', '')
                class_name = testcase.get('classname', '')
                time_taken = float(testcase.get('time', 0))

                # Determine test status
                if testcase.find('failure') is not None:
                    status = 'failed'
                    error_info = testcase.find('failure').text or ''
                elif testcase.find('error') is not None:
                    status = 'error'
                    error_info = testcase.find('error').text or ''
                elif testcase.find('skipped') is not None:
                    status = 'skipped'
                    error_info = testcase.find('skipped').text or ''
                else:
                    status = 'passed'
                    error_info = ''

                tests.append({
                    'name': test_name,
                    'class': class_name,
                    'status': status,
                    'time': time_taken,
                    'error_info': error_info
                })

                if status == 'passed':
                    summary['passed'] += 1

            summary['execution_time'] = float(root.get('time', 0))

            return {
                'tests': tests,
                'summary': summary,
                'execution_time': summary['execution_time'],
                'error': None
            }

        except Exception as e:
            return {
                'tests': [],
                'summary': {
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'error': 0
                },
                'execution_time': 0.0,
                'error': f'Failed to parse test results: {str(e)}'
            }

    def categorize_tests(self, tests: List[Dict]) -> Dict:
        """
        Categorize tests by function being tested.

        Args:
            tests: List of test dictionaries

        Returns:
            Dict mapping categories to test results
        """
        categorized = {category: [] for category in self.TEST_CATEGORIES.keys()}

        for test in tests:
            test_name = test['name'].lower()
            class_name = test['class'].lower()
            full_name = f"{class_name}.{test_name}"

            # Categorize based on test name patterns
            if 'load' in test_name and 'explore' in test_name:
                categorized['test_load_and_explore'].append(test)
            elif 'statistic' in test_name or 'stats' in test_name:
                categorized['test_calculate_statistics'].append(test)
            elif 'subset' in test_name or 'extract' in test_name or 'clip' in test_name:
                categorized['test_extract_subset'].append(test)
            elif 'visualize' in test_name or 'plot' in test_name or 'map' in test_name:
                categorized['test_visualize_raster'].append(test)
            elif 'integration' in test_name or 'quality' in test_name or 'import' in test_name:
                categorized['test_code_quality'].append(test)
            else:
                # Default categorization for uncategorized tests
                if 'raster' in test_name:
                    categorized['test_code_quality'].append(test)

        return categorized

    def calculate_grade(self, test_results: Dict) -> Dict:
        """
        Calculate grade based on test results.

        Args:
            test_results: Parsed test results

        Returns:
            Dict containing grade information
        """
        if test_results.get('error'):
            return {
                'total_points': 0,
                'possible_points': self.TOTAL_POINTS,
                'percentage': 0,
                'letter_grade': 'F',
                'category_breakdown': {},
                'tests_passed': 0,
                'tests_total': 0,
                'feedback': [f"❌ Error: {test_results['error']}"],
                'error': test_results['error']
            }

        categorized_tests = self.categorize_tests(test_results['tests'])
        category_breakdown = {}
        total_earned = 0
        feedback = []

        # Calculate points for each category
        for category, category_info in self.TEST_CATEGORIES.items():
            category_tests = categorized_tests[category]
            max_points = category_info['points']

            if not category_tests:
                # No tests found for this category
                earned = 0
                percentage = 0
                feedback.append(f"⚠️  {category_info['name']}: No tests found (0/{max_points} points)")
            else:
                passed_tests = len([t for t in category_tests if t['status'] == 'passed'])
                total_tests = len(category_tests)
                percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
                earned = (passed_tests / total_tests) * max_points if total_tests > 0 else 0

                if percentage == 100:
                    feedback.append(f"✅ {category_info['name']}: All tests passed ({earned:.1f}/{max_points} points)")
                elif percentage >= 80:
                    feedback.append(f"👍 {category_info['name']}: Mostly working ({earned:.1f}/{max_points} points)")
                elif percentage >= 50:
                    feedback.append(f"⚠️  {category_info['name']}: Partially working ({earned:.1f}/{max_points} points)")
                else:
                    feedback.append(f"❌ {category_info['name']}: Needs significant work ({earned:.1f}/{max_points} points)")

            category_breakdown[category] = {
                'earned': earned,
                'possible': max_points,
                'percentage': percentage,
                'tests_passed': len([t for t in category_tests if t['status'] == 'passed']),
                'tests_total': len(category_tests)
            }

            total_earned += earned

        # Calculate overall grade
        overall_percentage = (total_earned / self.TOTAL_POINTS) * 100
        letter_grade = 'F'
        for grade, threshold in self.GRADE_THRESHOLDS.items():
            if overall_percentage >= threshold:
                letter_grade = grade
                break

        return {
            'total_points': total_earned,
            'possible_points': self.TOTAL_POINTS,
            'percentage': overall_percentage,
            'letter_grade': letter_grade,
            'category_breakdown': category_breakdown,
            'tests_passed': test_results['summary']['passed'],
            'tests_total': test_results['summary']['total'],
            'feedback': feedback,
            'error': None
        }

    def generate_feedback(self, grade_info: Dict) -> List[str]:
        """
        Generate detailed feedback for students.

        Args:
            grade_info: Grade calculation results

        Returns:
            List of feedback messages
        """
        feedback = []

        # Overall performance
        percentage = grade_info['percentage']
        letter_grade = grade_info['letter_grade']

        feedback.append("=" * 60)
        feedback.append("🎓 PYTHON RASTERIO ASSIGNMENT - AUTOMATED FEEDBACK")
        feedback.append("=" * 60)
        feedback.append(f"📊 Final Grade: {letter_grade} ({percentage:.1f}%)")
        feedback.append(f"🎯 Points Earned: {grade_info['total_points']:.1f}/{grade_info['possible_points']}")
        feedback.append(f"🧪 Tests Passed: {grade_info['tests_passed']}/{grade_info['tests_total']}")
        feedback.append("")

        # Category-specific feedback
        feedback.append("📋 Function-by-Function Results:")
        feedback.extend(grade_info['feedback'])
        feedback.append("")

        # Recommendations based on performance
        if letter_grade in ['A', 'B']:
            feedback.append("🎉 Excellent work! Your raster processing skills are solid.")
            feedback.append("💡 Consider exploring advanced rasterio features for bonus learning.")
        elif letter_grade == 'C':
            feedback.append("👍 Good progress! A few areas need attention:")
            feedback.append("- Review failing test cases carefully")
            feedback.append("- Test your functions with different raster datasets")
            feedback.append("- Ask for help during office hours if needed")
        else:
            feedback.append("🔧 Significant improvements needed:")
            feedback.append("- Start with the function that has the most failing tests")
            feedback.append("- Make sure you understand rasterio basics")
            feedback.append("- Review the assignment instructions and sample code")
            feedback.append("- Don't hesitate to ask for help!")

        feedback.append("")
        feedback.append("🛠️ Professional Skills Developed:")
        feedback.append("- ✅ Raster data processing with rasterio")
        feedback.append("- ✅ Geospatial data analysis techniques")
        feedback.append("- ✅ Unit testing and test-driven development")
        feedback.append("- ✅ Continuous integration workflows")
        feedback.append("- ✅ Professional Python development practices")

        feedback.append("=" * 60)

        return feedback

    def output_for_github_actions(self, grade_info: Dict) -> None:
        """
        Output environment variables for GitHub Actions.

        Args:
            grade_info: Grade calculation results
        """
        if not self.is_ci:
            return

        github_env = os.getenv('GITHUB_ENV')
        if not github_env:
            return

        try:
            with open(github_env, 'a') as f:
                f.write(f"LETTER_GRADE={grade_info['letter_grade']}\n")
                f.write(f"GRADE_PERCENTAGE={grade_info['percentage']:.1f}\n")
                f.write(f"POINTS={grade_info['total_points']:.1f}\n")
                f.write(f"TESTS_PASSED={grade_info['tests_passed']}\n")
                f.write(f"TESTS_TOTAL={grade_info['tests_total']}\n")

                # Set failure flag if not all tests passed
                if grade_info['tests_passed'] < grade_info['tests_total']:
                    f.write("TESTS_FAILED=true\n")

            print("✅ Environment variables set for GitHub Actions")
        except Exception as e:
            print(f"⚠️  Failed to set GitHub Actions environment variables: {e}")

    def save_grade_report(self, grade_info: Dict, output_file: str) -> None:
        """
        Save detailed grade report to JSON file.

        Args:
            grade_info: Grade calculation results
            output_file: Output file path
        """
        try:
            report_data = {
                **grade_info,
                'timestamp': datetime.now().isoformat(),
                'assignment': 'python-rasterio',
                'grader_version': '2.0',
                'total_functions': 4,
                'function_names': [
                    'load_and_explore_raster',
                    'calculate_raster_statistics',
                    'extract_raster_subset',
                    'visualize_raster_data'
                ]
            }

            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2)

            print(f"✅ Grade report saved to {output_file}")
        except Exception as e:
            print(f"⚠️  Failed to save grade report: {e}")

    def run(self, output_file: Optional[str] = None) -> Dict:
        """
        Run the complete grading process.

        Args:
            output_file: Optional output file for grade report

        Returns:
            Grade calculation results
        """
        print("🎓 Starting Python Rasterio Assignment Grading...")
        print(f"📁 Reading test results from: {self.results_file}")

        # Parse test results
        test_results = self.parse_test_results()
        if test_results.get('error'):
            print(f"❌ Error parsing test results: {test_results['error']}")

        # Calculate grade
        grade_info = self.calculate_grade(test_results)

        # Generate and display feedback
        feedback_lines = self.generate_feedback(grade_info)
        for line in feedback_lines:
            print(line)

        # Output for CI/CD
        self.output_for_github_actions(grade_info)

        # Save detailed report if requested
        if output_file:
            self.save_grade_report(grade_info, output_file)

        return grade_info


def main():
    """Main entry point for the grading script."""
    parser = argparse.ArgumentParser(
        description='Automated grading for Python Rasterio assignment'
    )
    parser.add_argument(
        '--results',
        default='test-results.xml',
        help='Path to pytest XML results file (default: test-results.xml)'
    )
    parser.add_argument(
        '--output',
        help='Path to save detailed grade report JSON file'
    )
    parser.add_argument(
        '--ci-only',
        action='store_true',
        help='Run only in CI environments'
    )

    args = parser.parse_args()

    # Check if running in CI when ci-only flag is set
    if args.ci_only and not os.getenv('CI'):
        print("❌ This script should only be run in CI/CD environments!")
        print("💡 Students should use: pytest tests/ -v")
        sys.exit(1)

    try:
        grader = RasterioAssignmentGrader(args.results)
        grade_info = grader.run(args.output)

        # Exit with appropriate code
        if grade_info['letter_grade'] in ['A', 'B', 'C']:
            sys.exit(0)  # Passing grade
        else:
            sys.exit(1)  # Failing grade

    except KeyboardInterrupt:
        print("\n⚠️  Grading interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error during grading: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
