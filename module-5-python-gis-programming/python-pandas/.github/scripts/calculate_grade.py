#!/usr/bin/env python3
"""
CI/CD Grading Script for Python Pandas Assignment
=================================================

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
    python grade.py --results test-results.xml --output grade.json

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


class PandasAssignmentGrader:
    """Automated grader for Python Pandas assignment."""

    # Grading rubric configuration
    TOTAL_POINTS = 20
    GRADE_THRESHOLDS = {
        'A': 90,
        'B': 80,
        'C': 70,
        'D': 60,
        'F': 0
    }

    # Test categories and their point values
    TEST_CATEGORIES = {
        'test_load_and_explore': {'name': 'Load and Explore Data', 'points': 4},
        'test_filter_environmental': {'name': 'Filter Environmental Data', 'points': 4},
        'test_calculate_station': {'name': 'Calculate Station Statistics', 'points': 4},
        'test_join_station': {'name': 'Join Station Data', 'points': 4},
        'test_save_processed': {'name': 'Save Processed Data', 'points': 2},
        'test_integration': {'name': 'Integration Tests', 'points': 2}
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
        Parse pytest XML results and extract test information.

        Returns:
            Dictionary containing test results and statistics
        """
        try:
            if not os.path.exists(self.results_file):
                return {
                    'error': f'Test results file not found: {self.results_file}',
                    'total_tests': 0,
                    'passed': 0,
                    'failed': 0,
                    'errors': 0,
                    'skipped': 0,
                    'test_details': []
                }

            tree = ET.parse(self.results_file)
            root = tree.getroot()

            # Extract overall statistics
            total_tests = int(root.get('tests', 0))
            failures = int(root.get('failures', 0))
            errors = int(root.get('errors', 0))
            skipped = int(root.get('skipped', 0))
            passed = total_tests - failures - errors - skipped

            # Extract individual test details
            test_details = []
            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name', 'Unknown')
                test_class = testcase.get('classname', '')
                test_time = float(testcase.get('time', 0))

                # Determine test status
                if testcase.find('failure') is not None:
                    status = 'failed'
                    message = testcase.find('failure').get('message', 'Test failed')
                elif testcase.find('error') is not None:
                    status = 'error'
                    message = testcase.find('error').get('message', 'Test error')
                elif testcase.find('skipped') is not None:
                    status = 'skipped'
                    message = testcase.find('skipped').get('message', 'Test skipped')
                else:
                    status = 'passed'
                    message = 'Test passed'

                test_details.append({
                    'name': test_name,
                    'class': test_class,
                    'status': status,
                    'message': message,
                    'time': test_time
                })

            return {
                'total_tests': total_tests,
                'passed': passed,
                'failed': failures,
                'errors': errors,
                'skipped': skipped,
                'test_details': test_details
            }

        except Exception as e:
            return {
                'error': f'Failed to parse test results: {str(e)}',
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'skipped': 0,
                'test_details': []
            }

    def categorize_tests(self, test_details: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorize tests by function being tested.

        Args:
            test_details: List of test detail dictionaries

        Returns:
            Dictionary mapping categories to test lists
        """
        categorized = {category: [] for category in self.TEST_CATEGORIES.keys()}
        categorized['other'] = []

        for test in test_details:
            test_name = test['name'].lower()
            categorized_flag = False

            for category in self.TEST_CATEGORIES.keys():
                if category in test_name:
                    categorized[category].append(test)
                    categorized_flag = True
                    break

            if not categorized_flag:
                categorized['other'].append(test)

        return categorized

    def calculate_grade(self, results: Dict) -> Dict:
        """
        Calculate final grade based on test results.

        Args:
            results: Test results dictionary

        Returns:
            Dictionary containing grade information
        """
        if 'error' in results:
            return {
                'total_points': 0,
                'percentage': 0.0,
                'letter_grade': 'F',
                'status': 'error',
                'message': results['error']
            }

        # Calculate basic percentage
        total_tests = results['total_tests']
        passed_tests = results['passed']

        if total_tests == 0:
            percentage = 0.0
        else:
            percentage = (passed_tests / total_tests) * 100

        # Categorize tests for detailed scoring
        categorized = self.categorize_tests(results['test_details'])

        # Calculate points by category
        category_points = {}
        total_earned_points = 0

        for category, info in self.TEST_CATEGORIES.items():
            category_tests = categorized.get(category, [])
            if not category_tests:
                category_points[category] = {'earned': 0, 'possible': info['points'], 'percentage': 0}
                continue

            passed_in_category = sum(1 for test in category_tests if test['status'] == 'passed')
            total_in_category = len(category_tests)

            if total_in_category > 0:
                category_percentage = (passed_in_category / total_in_category)
                earned_points = int(info['points'] * category_percentage)
            else:
                category_percentage = 0
                earned_points = 0

            category_points[category] = {
                'earned': earned_points,
                'possible': info['points'],
                'percentage': category_percentage * 100,
                'passed': passed_in_category,
                'total': total_in_category
            }

            total_earned_points += earned_points

        # Determine letter grade
        final_percentage = (total_earned_points / self.TOTAL_POINTS) * 100
        letter_grade = 'F'

        for grade, threshold in sorted(self.GRADE_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if final_percentage >= threshold:
                letter_grade = grade
                break

        return {
            'total_points': total_earned_points,
            'possible_points': self.TOTAL_POINTS,
            'percentage': final_percentage,
            'letter_grade': letter_grade,
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'category_breakdown': category_points,
            'test_summary': {
                'total': total_tests,
                'passed': passed_tests,
                'failed': results['failed'],
                'errors': results['errors'],
                'skipped': results['skipped']
            },
            'status': 'complete'
        }

    def generate_feedback(self, grade_info: Dict, results: Dict) -> List[str]:
        """
        Generate detailed feedback for students.

        Args:
            grade_info: Grade calculation results
            results: Test results

        Returns:
            List of feedback messages
        """
        feedback = []

        if grade_info['status'] == 'error':
            feedback.append("❌ ERROR: Unable to process test results")
            feedback.append(f"   {grade_info.get('message', 'Unknown error')}")
            feedback.append("   Make sure all functions are implemented and have no syntax errors")
            return feedback

        # Overall performance
        percentage = grade_info['percentage']
        letter = grade_info['letter_grade']
        points = grade_info['total_points']

        if percentage >= 90:
            feedback.append(f"🎉 EXCELLENT WORK! Grade: {letter} ({percentage:.1f}%) - {points}/20 points")
            feedback.append("   All or nearly all functions are working correctly")
        elif percentage >= 80:
            feedback.append(f"👍 GOOD WORK! Grade: {letter} ({percentage:.1f}%) - {points}/20 points")
            feedback.append("   Most functions are working well with minor issues")
        elif percentage >= 70:
            feedback.append(f"⚠️  SATISFACTORY Grade: {letter} ({percentage:.1f}%) - {points}/20 points")
            feedback.append("   Basic functionality present but needs improvement")
        elif percentage >= 60:
            feedback.append(f"🔧 NEEDS WORK Grade: {letter} ({percentage:.1f}%) - {points}/20 points")
            feedback.append("   Several functions need attention")
        else:
            feedback.append(f"❌ SIGNIFICANT ISSUES Grade: {letter} ({percentage:.1f}%) - {points}/20 points")
            feedback.append("   Most functions are not working correctly")

        # Category-specific feedback
        feedback.append("\n📊 DETAILED BREAKDOWN:")

        for category, info in self.TEST_CATEGORIES.items():
            if category in grade_info['category_breakdown']:
                cat_data = grade_info['category_breakdown'][category]
                cat_name = info['name']
                earned = cat_data['earned']
                possible = cat_data['possible']

                if earned == possible:
                    feedback.append(f"   ✅ {cat_name}: {earned}/{possible} points - Perfect!")
                elif earned >= possible * 0.7:
                    feedback.append(f"   ⚠️  {cat_name}: {earned}/{possible} points - Minor issues")
                else:
                    feedback.append(f"   ❌ {cat_name}: {earned}/{possible} points - Needs work")

        # Specific guidance based on failures
        if results['failed'] > 0 or results['errors'] > 0:
            feedback.append("\n🔧 IMPROVEMENT SUGGESTIONS:")

            failed_tests = [t for t in results['test_details'] if t['status'] in ['failed', 'error']]

            for test in failed_tests[:5]:  # Show first 5 failed tests
                feedback.append(f"   • {test['name']}: {test['message'][:100]}...")

            if len(failed_tests) > 5:
                feedback.append(f"   • ... and {len(failed_tests) - 5} more failed tests")

            feedback.append("\n💡 DEBUGGING TIPS:")
            feedback.append("   • Run 'pytest tests/ -v' locally for detailed output")
            feedback.append("   • Check that functions return correct data types (DataFrames, etc.)")
            feedback.append("   • Verify column names match exactly (case-sensitive)")
            feedback.append("   • Test with the provided sample data files")
            feedback.append("   • Add print statements to debug intermediate results")

        return feedback

    def output_for_github_actions(self, grade_info: Dict, feedback: List[str]):
        """
        Output results in GitHub Actions format.

        Args:
            grade_info: Grade information
            feedback: Feedback messages
        """
        if not self.is_ci:
            return

        github_env = os.getenv('GITHUB_ENV')
        if not github_env:
            return

        try:
            with open(github_env, 'a') as f:
                # Match workflow expected variable names
                f.write(f"LETTER_GRADE={grade_info['letter_grade']}\n")
                f.write(f"GRADE_PERCENTAGE={grade_info['percentage']:.1f}\n")
                f.write(f"POINTS={grade_info['total_points']}\n")
                f.write(f"TESTS_PASSED={grade_info['tests_passed']}\n")
                f.write(f"TESTS_TOTAL={grade_info['tests_total']}\n")

                # Success status for CI
                success = grade_info['percentage'] >= 70  # C or better
                f.write(f"ASSIGNMENT_PASSED={'true' if success else 'false'}\n")

            print("✅ GitHub Actions environment updated")

        except Exception as e:
            print(f"⚠️  Could not update GitHub Actions environment: {e}")

    def save_grade_report(self, grade_info: Dict, feedback: List[str], output_file: str = 'grade-report.json'):
        """
        Save detailed grade report as JSON.

        Args:
            grade_info: Grade information
            feedback: Feedback messages
            output_file: Output file path
        """
        report = {
            'assignment': 'GIST 604B - Python Pandas for GIS Data Analysis',
            'timestamp': datetime.now().isoformat(),
            'grading_system': 'pytest-based automated testing',
            'grade': grade_info,
            'feedback': feedback,
            'rubric': {
                'total_points': self.TOTAL_POINTS,
                'categories': self.TEST_CATEGORIES,
                'grade_scale': self.GRADE_THRESHOLDS
            }
        }

        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Grade report saved to {output_file}")
        except Exception as e:
            print(f"⚠️  Could not save grade report: {e}")

    def run(self, output_file: Optional[str] = None) -> bool:
        """
        Run the complete grading process.

        Args:
            output_file: Optional output file for grade report

        Returns:
            True if grading completed successfully
        """
        print("🎓 GIST 604B - Python Pandas Assignment Grader")
        print("=" * 60)
        print("📊 Analyzing test results...")

        # Parse test results
        results = self.parse_test_results()

        # Calculate grade
        grade_info = self.calculate_grade(results)

        # Generate feedback
        feedback = self.generate_feedback(grade_info, results)

        # Display results
        print("\n".join(feedback))

        # Output for CI systems
        if self.is_ci:
            self.output_for_github_actions(grade_info, feedback)

        # Save detailed report
        if output_file:
            self.save_grade_report(grade_info, feedback, output_file)

        # Return success status
        return grade_info['status'] != 'error' and grade_info['percentage'] >= 60


def main():
    """Main entry point for CI/CD grading."""
    parser = argparse.ArgumentParser(
        description='Automated grader for Python Pandas assignment (CI/CD only)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPORTANT: This script is for CI/CD use only!

Students should use:
    pytest tests/ -v

For local testing and development.
        """
    )

    parser.add_argument(
        '--results',
        default='test-results.xml',
        help='Path to pytest XML results file (default: test-results.xml)'
    )

    parser.add_argument(
        '--output',
        help='Output file for detailed grade report (JSON format)'
    )

    parser.add_argument(
        '--ci-only',
        action='store_true',
        help='Only run in CI environments (default: auto-detect)'
    )

    args = parser.parse_args()

    # Check if running in non-CI environment
    is_ci = os.getenv('CI', '').lower() == 'true'

    if args.ci_only and not is_ci:
        print("❌ This script is configured to run only in CI environments")
        print("💡 Students should use: pytest tests/ -v")
        sys.exit(1)

    if not is_ci:
        print("⚠️  WARNING: This script is designed for CI/CD environments")
        print("💡 For local development, use: pytest tests/ -v")
        print("⏸️  Continuing anyway...\n")

    # Run grader
    grader = PandasAssignmentGrader(args.results)
    success = grader.run(args.output)

    # Exit with appropriate code for CI
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
