#!/usr/bin/env python3
"""
Automated Grade Calculation Script for Python Pandas Assignment
Calculates final grade based on multiple assessment components.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Tuple
import subprocess
import re

class GradeCalculator:
    """Automated grade calculator for Python pandas assignment."""

    def __init__(self):
        self.total_points = 30
        self.component_weights = {
            'correctness': 15,      # Unit tests passing
            'performance': 5,       # Performance benchmarks
            'code_quality': 5,      # Linting, formatting, type hints
            'coverage': 5           # Test coverage
        }
        self.grade_report = {
            'total_score': 0,
            'component_scores': {},
            'feedback': [],
            'detailed_results': {},
            'timestamp': None
        }

    def calculate_correctness_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on passing unit tests."""
        try:
            # Parse pytest results from XML
            if Path('test-results.xml').exists():
                tree = ET.parse('test-results.xml')
                root = tree.getroot()

                total_tests = int(root.get('tests', 0))
                failures = int(root.get('failures', 0))
                errors = int(root.get('errors', 0))
                passed = total_tests - failures - errors

                if total_tests == 0:
                    return 0, {'error': 'No tests found'}

                pass_rate = passed / total_tests
                score = int(self.component_weights['correctness'] * pass_rate)

                details = {
                    'total_tests': total_tests,
                    'passed': passed,
                    'failed': failures,
                    'errors': errors,
                    'pass_rate': f"{pass_rate:.2%}",
                    'test_breakdown': self._parse_test_breakdown(root)
                }

                return score, details

            else:
                # Fallback: run pytest and capture output
                result = subprocess.run(
                    ['pytest', 'tests/', '--tb=short', '-v'],
                    capture_output=True, text=True, timeout=300
                )

                # Parse pytest output
                output_lines = result.stdout.split('\n')
                passed = len([line for line in output_lines if '::' in line and 'PASSED' in line])
                failed = len([line for line in output_lines if '::' in line and 'FAILED' in line])
                total = passed + failed

                if total == 0:
                    return 0, {'error': 'No tests executed'}

                pass_rate = passed / total if total > 0 else 0
                score = int(self.component_weights['correctness'] * pass_rate)

                details = {
                    'total_tests': total,
                    'passed': passed,
                    'failed': failed,
                    'pass_rate': f"{pass_rate:.2%}",
                    'pytest_output': result.stdout[-1000:] if result.stdout else ""
                }

                return score, details

        except Exception as e:
            return 0, {'error': f'Failed to calculate correctness: {str(e)}'}

    def calculate_performance_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on performance benchmarks."""
        try:
            if Path('benchmark.json').exists():
                with open('benchmark.json', 'r') as f:
                    benchmark_data = json.load(f)

                benchmarks = benchmark_data.get('benchmarks', [])
                if not benchmarks:
                    return 0, {'error': 'No benchmark results found'}

                # Define performance thresholds (in seconds)
                thresholds = {
                    'test_boolean_filter_performance': 1.0,
                    'test_multi_condition_performance': 2.0,
                    'test_series_creation_performance': 0.5,
                    'test_join_performance': 1.5
                }

                passed_benchmarks = 0
                total_benchmarks = 0
                benchmark_details = {}

                for bench in benchmarks:
                    name = bench.get('name', '')
                    mean_time = bench.get('stats', {}).get('mean', float('inf'))

                    if name in thresholds:
                        total_benchmarks += 1
                        threshold = thresholds[name]
                        passed = mean_time <= threshold

                        if passed:
                            passed_benchmarks += 1

                        benchmark_details[name] = {
                            'mean_time': f"{mean_time:.4f}s",
                            'threshold': f"{threshold:.2f}s",
                            'passed': passed,
                            'performance_ratio': min(threshold / mean_time, 2.0) if mean_time > 0 else 0
                        }

                if total_benchmarks == 0:
                    return 0, {'error': 'No recognized benchmarks found'}

                performance_rate = passed_benchmarks / total_benchmarks
                score = int(self.component_weights['performance'] * performance_rate)

                details = {
                    'total_benchmarks': total_benchmarks,
                    'passed_benchmarks': passed_benchmarks,
                    'performance_rate': f"{performance_rate:.2%}",
                    'benchmark_details': benchmark_details
                }

                return score, details

            else:
                # Try to run benchmarks
                result = subprocess.run(
                    ['pytest', 'benchmarks/', '--benchmark-only', '--benchmark-json=benchmark.json'],
                    capture_output=True, text=True, timeout=300
                )

                if result.returncode == 0 and Path('benchmark.json').exists():
                    return self.calculate_performance_score()  # Recursive call
                else:
                    return 0, {'error': 'Benchmark execution failed', 'stderr': result.stderr}

        except Exception as e:
            return 0, {'error': f'Failed to calculate performance: {str(e)}'}

    def calculate_code_quality_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on code quality metrics."""
        quality_checks = {}
        total_score = 0
        max_score = self.component_weights['code_quality']

        # Check code formatting with black
        try:
            result = subprocess.run(
                ['black', '--check', 'src/', 'tests/'],
                capture_output=True, text=True
            )
            black_passed = result.returncode == 0
            quality_checks['formatting'] = {
                'passed': black_passed,
                'weight': 0.3,
                'message': 'Code formatting' if black_passed else 'Code formatting issues found'
            }
            if black_passed:
                total_score += max_score * 0.3
        except Exception as e:
            quality_checks['formatting'] = {
                'passed': False,
                'weight': 0.3,
                'message': f'Black check failed: {str(e)}'
            }

        # Check linting with ruff
        try:
            result = subprocess.run(
                ['ruff', 'check', 'src/', 'tests/'],
                capture_output=True, text=True
            )
            ruff_passed = result.returncode == 0
            quality_checks['linting'] = {
                'passed': ruff_passed,
                'weight': 0.4,
                'message': 'No linting errors' if ruff_passed else f'Linting issues: {result.stdout[:200]}'
            }
            if ruff_passed:
                total_score += max_score * 0.4
        except Exception as e:
            quality_checks['linting'] = {
                'passed': False,
                'weight': 0.4,
                'message': f'Ruff check failed: {str(e)}'
            }

        # Check type hints with mypy
        try:
            result = subprocess.run(
                ['mypy', 'src/'],
                capture_output=True, text=True
            )
            mypy_passed = result.returncode == 0
            quality_checks['type_checking'] = {
                'passed': mypy_passed,
                'weight': 0.3,
                'message': 'Type checking passed' if mypy_passed else f'Type issues: {result.stdout[:200]}'
            }
            if mypy_passed:
                total_score += max_score * 0.3
        except Exception as e:
            quality_checks['type_checking'] = {
                'passed': False,
                'weight': 0.3,
                'message': f'MyPy check failed: {str(e)}'
            }

        return int(total_score), {
            'quality_checks': quality_checks,
            'total_possible': max_score
        }

    def calculate_coverage_score(self) -> Tuple[int, Dict[str, Any]]:
        """Calculate score based on test coverage."""
        try:
            if Path('coverage.xml').exists():
                tree = ET.parse('coverage.xml')
                root = tree.getroot()

                # Parse coverage percentage
                coverage_elem = root.find('.//coverage')
                if coverage_elem is not None:
                    line_rate = float(coverage_elem.get('line-rate', 0))
                    branch_rate = float(coverage_elem.get('branch-rate', 0))

                    # Average line and branch coverage
                    avg_coverage = (line_rate + branch_rate) / 2
                    coverage_percent = avg_coverage * 100

                    # Calculate score based on coverage thresholds
                    if coverage_percent >= 95:
                        score = self.component_weights['coverage']
                    elif coverage_percent >= 80:
                        score = int(self.component_weights['coverage'] * 0.8)
                    elif coverage_percent >= 60:
                        score = int(self.component_weights['coverage'] * 0.6)
                    elif coverage_percent >= 40:
                        score = int(self.component_weights['coverage'] * 0.4)
                    else:
                        score = 0

                    details = {
                        'line_coverage': f"{line_rate:.2%}",
                        'branch_coverage': f"{branch_rate:.2%}",
                        'average_coverage': f"{avg_coverage:.2%}",
                        'coverage_threshold_met': coverage_percent >= 80
                    }

                    return score, details

            # Fallback: run coverage
            result = subprocess.run(
                ['coverage', 'run', '-m', 'pytest', 'tests/'],
                capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0:
                coverage_result = subprocess.run(
                    ['coverage', 'report', '--format=json'],
                    capture_output=True, text=True
                )

                if coverage_result.returncode == 0:
                    coverage_data = json.loads(coverage_result.stdout)
                    coverage_percent = coverage_data.get('totals', {}).get('percent_covered', 0)

                    if coverage_percent >= 95:
                        score = self.component_weights['coverage']
                    elif coverage_percent >= 80:
                        score = int(self.component_weights['coverage'] * 0.8)
                    elif coverage_percent >= 60:
                        score = int(self.component_weights['coverage'] * 0.6)
                    else:
                        score = 0

                    details = {
                        'coverage_percent': f"{coverage_percent:.1f}%",
                        'lines_covered': coverage_data.get('totals', {}).get('covered_lines', 0),
                        'lines_total': coverage_data.get('totals', {}).get('num_statements', 0)
                    }

                    return score, details

            return 0, {'error': 'Could not calculate coverage'}

        except Exception as e:
            return 0, {'error': f'Failed to calculate coverage: {str(e)}'}

    def _parse_test_breakdown(self, xml_root) -> Dict[str, Dict[str, int]]:
        """Parse detailed test breakdown from XML results."""
        breakdown = {
            'data_structures': {'passed': 0, 'failed': 0},
            'data_subsetting': {'passed': 0, 'failed': 0},
            'data_joins': {'passed': 0, 'failed': 0},
            'file_operations': {'passed': 0, 'failed': 0}
        }

        for testcase in xml_root.findall('.//testcase'):
            classname = testcase.get('classname', '')
            test_failed = testcase.find('failure') is not None or testcase.find('error') is not None

            if 'data_structures' in classname:
                module = 'data_structures'
            elif 'data_subsetting' in classname:
                module = 'data_subsetting'
            elif 'data_joins' in classname:
                module = 'data_joins'
            elif 'file_operations' in classname:
                module = 'file_operations'
            else:
                continue

            if test_failed:
                breakdown[module]['failed'] += 1
            else:
                breakdown[module]['passed'] += 1

        return breakdown

    def generate_feedback(self) -> List[str]:
        """Generate detailed feedback based on scores."""
        feedback = []

        # Overall performance feedback
        total_score = self.grade_report['total_score']
        percentage = (total_score / self.total_points) * 100

        if percentage >= 90:
            feedback.append("🎉 Excellent work! Your code meets professional standards.")
        elif percentage >= 80:
            feedback.append("👍 Good job! Your implementation is solid with room for minor improvements.")
        elif percentage >= 70:
            feedback.append("👌 Decent work, but several areas need improvement.")
        elif percentage >= 60:
            feedback.append("⚠️ Your code works but needs significant improvements.")
        else:
            feedback.append("❌ Major issues found. Please review the requirements carefully.")

        # Component-specific feedback
        scores = self.grade_report['component_scores']

        if scores.get('correctness', 0) < self.component_weights['correctness'] * 0.8:
            feedback.append("🔧 Focus on making your functions pass the unit tests.")

        if scores.get('performance', 0) < self.component_weights['performance'] * 0.6:
            feedback.append("⚡ Consider optimizing your algorithms for better performance.")

        if scores.get('code_quality', 0) < self.component_weights['code_quality'] * 0.7:
            feedback.append("✨ Improve code formatting, fix linting issues, and add type hints.")

        if scores.get('coverage', 0) < self.component_weights['coverage'] * 0.6:
            feedback.append("🎯 Write more comprehensive tests to increase coverage.")

        return feedback

    def calculate_final_grade(self) -> Dict[str, Any]:
        """Calculate the final grade by running all assessment components."""
        print("Starting automated grade calculation...")

        # Calculate component scores
        correctness_score, correctness_details = self.calculate_correctness_score()
        performance_score, performance_details = self.calculate_performance_score()
        quality_score, quality_details = self.calculate_code_quality_score()
        coverage_score, coverage_details = self.calculate_coverage_score()

        # Store component scores
        self.grade_report['component_scores'] = {
            'correctness': correctness_score,
            'performance': performance_score,
            'code_quality': quality_score,
            'coverage': coverage_score
        }

        # Store detailed results
        self.grade_report['detailed_results'] = {
            'correctness': correctness_details,
            'performance': performance_details,
            'code_quality': quality_details,
            'coverage': coverage_details
        }

        # Calculate total score
        self.grade_report['total_score'] = sum(self.grade_report['component_scores'].values())

        # Generate feedback
        self.grade_report['feedback'] = self.generate_feedback()

        # Add timestamp
        from datetime import datetime
        self.grade_report['timestamp'] = datetime.now().isoformat()

        return self.grade_report

def main():
    """Main entry point for grade calculation."""
    calculator = GradeCalculator()
    grade_report = calculator.calculate_final_grade()

    # Save grade report
    with open('grade_report.json', 'w') as f:
        json.dump(grade_report, f, indent=2)

    # Print summary
    print(f"\n{'='*50}")
    print("AUTOMATED GRADING RESULTS")
    print(f"{'='*50}")
    print(f"Total Score: {grade_report['total_score']}/{calculator.total_points}")
    print(f"Percentage: {(grade_report['total_score']/calculator.total_points)*100:.1f}%")
    print(f"\nComponent Breakdown:")
    for component, score in grade_report['component_scores'].items():
        max_score = calculator.component_weights[component]
        print(f"  {component.title()}: {score}/{max_score}")

    print(f"\nFeedback:")
    for feedback_item in grade_report['feedback']:
        print(f"  {feedback_item}")

    # Set exit code based on grade
    if grade_report['total_score'] >= calculator.total_points * 0.6:
        sys.exit(0)  # Pass
    else:
        sys.exit(1)  # Fail

if __name__ == "__main__":
    main()
