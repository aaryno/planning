#!/usr/bin/env python3
"""
SQL Introduction Assignment - Automated Grading Script

Calculates grades for 10 SQL queries (2 points each = 20 total points)
Generates detailed grade reports and sets environment variables for CI/CD.

Usage:
    python calculate_grade.py
    python calculate_grade.py --output grade-report.json
    python calculate_grade.py --verbose
"""

import json
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class SQLGradingEngine:
    """Professional grading engine for SQL Introduction assignment."""

    # Define the 10 SQL query categories (2 points each)
    QUERY_CATEGORIES = {
        'basic_select': {
            'name': '01_basic_select',
            'points': 2,
            'description': 'Basic SELECT statement with LIMIT',
            'concepts': ['SELECT', 'FROM', 'LIMIT'],
            'test_method': 'test_01_basic_select'
        },
        'column_selection': {
            'name': '02_column_selection',
            'points': 2,
            'description': 'Column selection and aliases',
            'concepts': ['Column selection', 'AS aliases'],
            'test_method': 'test_02_column_selection'
        },
        'where_clause': {
            'name': '03_where_clause',
            'points': 2,
            'description': 'WHERE clause with comparison operators',
            'concepts': ['WHERE', 'comparison operators'],
            'test_method': 'test_03_where_clause'
        },
        'multiple_conditions': {
            'name': '04_multiple_conditions',
            'points': 2,
            'description': 'Multiple conditions and logical operators',
            'concepts': ['AND', 'OR', 'BETWEEN', 'IN'],
            'test_method': 'test_04_multiple_conditions'
        },
        'sorting': {
            'name': '05_sorting',
            'points': 2,
            'description': 'Sorting with ORDER BY clause',
            'concepts': ['ORDER BY', 'ASC', 'DESC'],
            'test_method': 'test_05_sorting'
        },
        'aggregates': {
            'name': '06_aggregates',
            'points': 2,
            'description': 'Aggregate functions',
            'concepts': ['COUNT', 'AVG', 'MIN', 'MAX'],
            'test_method': 'test_06_aggregates'
        },
        'group_by': {
            'name': '07_group_by',
            'points': 2,
            'description': 'GROUP BY clause with aggregation',
            'concepts': ['GROUP BY', 'aggregation'],
            'test_method': 'test_07_group_by'
        },
        'having_clause': {
            'name': '08_having_clause',
            'points': 2,
            'description': 'HAVING clause for filtering groups',
            'concepts': ['HAVING', 'group filtering'],
            'test_method': 'test_08_having_clause'
        },
        'joins': {
            'name': '09_joins',
            'points': 2,
            'description': 'Basic JOIN operations',
            'concepts': ['INNER JOIN', 'table relationships'],
            'test_method': 'test_09_joins'
        },
        'complex_query': {
            'name': '10_complex_query',
            'points': 2,
            'description': 'Complex query with subquery',
            'concepts': ['subqueries', 'complex WHERE'],
            'test_method': 'test_10_complex_query'
        }
    }

    TOTAL_POSSIBLE_POINTS = 20

    def __init__(self, assignment_dir: Path = None, verbose: bool = False):
        self.assignment_dir = assignment_dir or Path(__file__).parent.parent
        self.verbose = verbose
        self.test_results = {}
        self.grade_report = {}

    def run_tests(self) -> Dict[str, Any]:
        """Run the automated test suite and capture results."""
        if self.verbose:
            print("🧪 Running SQL assignment test suite...")

        try:
            # Run pytest with JSON output
            cmd = [
                'python', '-m', 'pytest',
                str(self.assignment_dir / 'test_assignment.py'),
                '-v', '--tb=short', '--json-report', '--json-report-file=test-results.json'
            ]

            # Try without json-report if plugin not available
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.assignment_dir)
            except subprocess.SubprocessError:
                # Fallback without JSON report
                cmd = [
                    'python', '-m', 'pytest',
                    str(self.assignment_dir / 'test_assignment.py'),
                    '-v', '--tb=short'
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.assignment_dir)

            # Parse test output to determine which tests passed/failed
            self.parse_test_output(result.stdout, result.stderr, result.returncode)

            if self.verbose:
                print(f"✅ Tests completed with return code: {result.returncode}")
                print(f"📊 Passed: {self.count_passed_tests()}/{len(self.QUERY_CATEGORIES)}")

            return self.test_results

        except Exception as e:
            if self.verbose:
                print(f"❌ Error running tests: {e}")
            # Create default failed results
            for category in self.QUERY_CATEGORIES:
                self.test_results[category] = {
                    'passed': False,
                    'error': str(e),
                    'score': 0
                }
            return self.test_results

    def parse_test_output(self, stdout: str, stderr: str, return_code: int):
        """Parse pytest output to determine test results."""
        # Initialize all tests as failed
        for category in self.QUERY_CATEGORIES:
            self.test_results[category] = {
                'passed': False,
                'error': None,
                'score': 0
            }

        # Parse stdout for test results
        lines = stdout.split('\n')
        for line in lines:
            line = line.strip()

            # Look for test results
            for category, config in self.QUERY_CATEGORIES.items():
                test_method = config['test_method']
                if test_method in line:
                    if 'PASSED' in line or '✓' in line:
                        self.test_results[category] = {
                            'passed': True,
                            'error': None,
                            'score': config['points']
                        }
                        if self.verbose:
                            print(f"✅ {config['name']}: PASSED ({config['points']} points)")
                    elif 'FAILED' in line or '✗' in line:
                        self.test_results[category] = {
                            'passed': False,
                            'error': 'Test failed - check query logic and syntax',
                            'score': 0
                        }
                        if self.verbose:
                            print(f"❌ {config['name']}: FAILED (0 points)")

        # If we couldn't parse specific tests, make educated guesses based on overall success
        if return_code == 0 and not any(result['passed'] for result in self.test_results.values()):
            # All tests likely passed but we couldn't parse individual results
            for category in self.QUERY_CATEGORIES:
                if self.sql_file_exists(self.QUERY_CATEGORIES[category]['name'] + '.sql'):
                    self.test_results[category] = {
                        'passed': True,
                        'error': None,
                        'score': self.QUERY_CATEGORIES[category]['points']
                    }

    def sql_file_exists(self, filename: str) -> bool:
        """Check if SQL file exists."""
        return (self.assignment_dir / 'sql' / filename).exists()

    def count_passed_tests(self) -> int:
        """Count number of tests that passed."""
        return sum(1 for result in self.test_results.values() if result['passed'])

    def calculate_grade(self) -> Dict[str, Any]:
        """Calculate overall grade and generate detailed report."""
        # Calculate totals
        total_earned = sum(result['score'] for result in self.test_results.values())
        percentage = (total_earned / self.TOTAL_POSSIBLE_POINTS) * 100
        letter_grade = self.calculate_letter_grade(percentage)

        # Build category breakdown
        category_breakdown = {}
        for category, config in self.QUERY_CATEGORIES.items():
            result = self.test_results[category]
            category_breakdown[category] = {
                'query_file': 'sql/' + config['name'] + '.sql',
                'earned': result['score'],
                'possible': config['points'],
                'percentage': (result['score'] / config['points']) * 100 if config['points'] > 0 else 0,
                'status': 'passed' if result['passed'] else 'failed',
                'concepts': config['concepts'],
                'error': result['error']
            }

        # Generate feedback
        feedback = self.generate_feedback(total_earned, percentage)

        # Create comprehensive grade report
        self.grade_report = {
            'assignment': 'SQL Introduction - Database Fundamentals',
            'assignment_type': 'Foundation Level (SQL Basics)',
            'total_points': total_earned,
            'possible_points': self.TOTAL_POSSIBLE_POINTS,
            'percentage': round(percentage, 1),
            'letter_grade': letter_grade,
            'tests_passed': self.count_passed_tests(),
            'tests_total': len(self.QUERY_CATEGORIES),
            'category_breakdown': category_breakdown,
            'feedback': feedback,
            'performance_metrics': {
                'queries_completed': self.count_completed_queries(),
                'syntax_accuracy': self.calculate_syntax_accuracy(),
                'concept_mastery': self.calculate_concept_mastery()
            },
            'professional_context': {
                'skills_assessed': [
                    'Basic SQL syntax and structure',
                    'Data filtering and sorting',
                    'Aggregate functions and grouping',
                    'Table relationships and joins',
                    'Complex query construction'
                ],
                'industry_relevance': 'Essential foundation for all database roles including GIS database administration, data analysis, and application development',
                'next_steps': 'Ready for PostGIS spatial functions and advanced database operations'
            },
            'timestamp': datetime.now().isoformat(),
            'grading_version': '1.0'
        }

        return self.grade_report

    def calculate_letter_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade."""
        if percentage >= 97: return 'A+'
        elif percentage >= 93: return 'A'
        elif percentage >= 90: return 'A-'
        elif percentage >= 87: return 'B+'
        elif percentage >= 83: return 'B'
        elif percentage >= 80: return 'B-'
        elif percentage >= 77: return 'C+'
        elif percentage >= 73: return 'C'
        elif percentage >= 70: return 'C-'
        elif percentage >= 67: return 'D+'
        elif percentage >= 63: return 'D'
        elif percentage >= 60: return 'D-'
        else: return 'F'

    def count_completed_queries(self) -> int:
        """Count how many SQL files exist."""
        count = 0
        for config in self.QUERY_CATEGORIES.values():
            if self.sql_file_exists(config['name'] + '.sql'):
                count += 1
        return count

    def calculate_syntax_accuracy(self) -> str:
        """Calculate syntax accuracy based on test results."""
        passed_tests = self.count_passed_tests()
        total_tests = len(self.QUERY_CATEGORIES)
        accuracy = (passed_tests / total_tests) * 100

        if accuracy >= 90: return 'excellent'
        elif accuracy >= 80: return 'good'
        elif accuracy >= 70: return 'satisfactory'
        elif accuracy >= 60: return 'needs_improvement'
        else: return 'poor'

    def calculate_concept_mastery(self) -> List[str]:
        """Identify which SQL concepts were mastered."""
        mastered_concepts = []
        concept_groups = {
            'Basic Queries': ['basic_select', 'column_selection'],
            'Filtering': ['where_clause', 'multiple_conditions'],
            'Sorting': ['sorting'],
            'Aggregation': ['aggregates', 'group_by', 'having_clause'],
            'Joins': ['joins'],
            'Advanced': ['complex_query']
        }

        for group_name, categories in concept_groups.items():
            group_passed = all(self.test_results[cat]['passed'] for cat in categories if cat in self.test_results)
            if group_passed:
                mastered_concepts.append(group_name)

        return mastered_concepts

    def generate_feedback(self, total_earned: int, percentage: float) -> List[str]:
        """Generate personalized feedback based on performance."""
        feedback = []

        # Overall performance feedback
        if percentage >= 90:
            feedback.append("🌟 Excellent work! You've mastered SQL fundamentals.")
            feedback.append("💪 You're ready for PostGIS spatial queries.")
        elif percentage >= 80:
            feedback.append("✅ Good job! You understand core SQL concepts well.")
            feedback.append("🔍 Review any failed queries to strengthen your foundation.")
        elif percentage >= 70:
            feedback.append("📚 Satisfactory progress, but more practice needed.")
            feedback.append("💡 Focus on understanding SQL execution order and syntax.")
        else:
            feedback.append("⚠️ SQL fundamentals need significant improvement.")
            feedback.append("📖 Review PostgreSQL documentation and practice basic queries.")

        # Specific concept feedback
        failed_categories = [cat for cat, result in self.test_results.items() if not result['passed']]

        if 'basic_select' in failed_categories or 'column_selection' in failed_categories:
            feedback.append("🎯 Practice basic SELECT syntax and column selection.")

        if 'where_clause' in failed_categories or 'multiple_conditions' in failed_categories:
            feedback.append("🔍 Work on WHERE clause filtering and logical operators.")

        if 'aggregates' in failed_categories or 'group_by' in failed_categories:
            feedback.append("📊 Review aggregate functions and GROUP BY concepts.")

        if 'joins' in failed_categories:
            feedback.append("🔗 Practice table joins - this is crucial for PostGIS work.")

        if 'complex_query' in failed_categories:
            feedback.append("🧩 Work on combining multiple SQL concepts in complex queries.")

        # Encouragement
        completed_queries = self.count_completed_queries()
        if completed_queries == len(self.QUERY_CATEGORIES):
            feedback.append("👏 Great effort completing all 10 SQL queries!")
        elif completed_queries >= 7:
            feedback.append(f"👍 Good progress with {completed_queries}/10 queries completed.")

        return feedback

    def save_grade_report(self, output_file: str = 'grade-report.json'):
        """Save grade report to JSON file."""
        output_path = self.assignment_dir / output_file
        with open(output_path, 'w') as f:
            json.dump(self.grade_report, f, indent=2)

        if self.verbose:
            print(f"📝 Grade report saved to: {output_path}")

    def set_environment_variables(self):
        """Set environment variables for GitHub Actions CI/CD."""
        grade_data = self.grade_report

        # Set standard environment variables
        env_vars = {
            'ASSIGNMENT_SCORE': str(grade_data['total_points']),
            'POSSIBLE_POINTS': str(grade_data['possible_points']),
            'GRADE_PERCENTAGE': str(grade_data['percentage']),
            'LETTER_GRADE': grade_data['letter_grade'],
            'TESTS_PASSED': str(grade_data['tests_passed']),
            'TESTS_TOTAL': str(grade_data['tests_total']),
            'SQL_QUERIES_COMPLETED': str(grade_data['performance_metrics']['queries_completed']),
            'SYNTAX_ACCURACY': grade_data['performance_metrics']['syntax_accuracy']
        }

        # Set environment variables for CI/CD
        if os.getenv('GITHUB_ENV'):
            with open(os.getenv('GITHUB_ENV'), 'a') as env_file:
                for key, value in env_vars.items():
                    env_file.write(f"{key}={value}\n")

        # Set for current process
        for key, value in env_vars.items():
            os.environ[key] = value

        if self.verbose:
            print("🌐 Environment variables set for CI/CD:")
            for key, value in env_vars.items():
                print(f"  {key}={value}")

    def print_summary(self):
        """Print grade summary to console."""
        report = self.grade_report

        print("\n" + "="*60)
        print("📋 SQL INTRODUCTION ASSIGNMENT - GRADE SUMMARY")
        print("="*60)
        print(f"📊 Score: {report['total_points']}/{report['possible_points']} points ({report['percentage']}%)")
        print(f"🎯 Grade: {report['letter_grade']}")
        print(f"✅ Tests Passed: {report['tests_passed']}/{report['tests_total']}")
        print(f"📝 Queries Completed: {report['performance_metrics']['queries_completed']}/10")
        print(f"🎭 Syntax Accuracy: {report['performance_metrics']['syntax_accuracy']}")

        print("\n📈 QUERY BREAKDOWN:")
        for category, breakdown in report['category_breakdown'].items():
            status_emoji = "✅" if breakdown['status'] == 'passed' else "❌"
            print(f"  {status_emoji} {breakdown['query_file']}: {breakdown['earned']}/{breakdown['possible']} pts")

        print(f"\n🎓 CONCEPTS MASTERED: {', '.join(report['performance_metrics']['concept_mastery'])}")

        print("\n💬 FEEDBACK:")
        for feedback_item in report['feedback']:
            print(f"  • {feedback_item}")

        print("\n🚀 NEXT STEPS:")
        print(f"  • {report['professional_context']['next_steps']}")
        print("="*60)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Calculate grades for SQL Introduction assignment')
    parser.add_argument('--output', '-o', default='grade-report.json',
                       help='Output file for grade report (default: grade-report.json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress summary output (CI/CD mode)')

    args = parser.parse_args()

    # Initialize grading engine
    grading_engine = SQLGradingEngine(verbose=args.verbose)

    try:
        # Run tests and calculate grade
        if args.verbose:
            print("🚀 Starting SQL assignment grading process...")

        grading_engine.run_tests()
        grade_report = grading_engine.calculate_grade()

        # Save results
        grading_engine.save_grade_report(args.output)
        grading_engine.set_environment_variables()

        # Display results
        if not args.quiet:
            grading_engine.print_summary()

        # Exit with appropriate code
        percentage = grade_report['percentage']
        if percentage >= 70:  # Passing grade
            sys.exit(0)
        else:
            if args.verbose:
                print("⚠️  Assignment did not meet minimum passing requirements (70%)")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error in grading process: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
