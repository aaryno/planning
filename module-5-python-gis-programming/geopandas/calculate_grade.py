#!/usr/bin/env python3
"""
GIST 604B - Python GeoPandas Introduction
Professional Grading Engine

This script provides comprehensive automated grading for the GeoPandas introduction
assignment, following Module 5 unified grading standards.

Functions tested:
- load_spatial_dataset() (4 points)
- explore_spatial_properties() (4 points)
- validate_spatial_data() (4 points)
- standardize_crs() (3 points)

Usage:
    python calculate_grade.py                    # Run grading
    python calculate_grade.py --verbose          # Detailed output
    python calculate_grade.py --json-only       # JSON output only

Author: GIST 604B Course Team
"""

import subprocess
import json
import xml.etree.ElementTree as ET
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import traceback


class GeoPandasGrader:
    """Professional grading engine for GeoPandas introduction assignment."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.assignment_name = "Python GeoPandas Introduction - Spatial Data Fundamentals"
        self.total_points = 15

        # Function point allocation
        self.function_points = {
            'load_spatial_dataset': 4,
            'explore_spatial_properties': 4,
            'validate_spatial_data': 4,
            'standardize_crs': 3
        }

        # Grade report structure
        self.grade_report = {
            'assignment': self.assignment_name,
            'total_points': 0,
            'possible_points': self.total_points,
            'percentage': 0.0,
            'letter_grade': 'F',
            'category_breakdown': {},
            'feedback': [],
            'timestamp': datetime.now().isoformat(),
            'grading_version': '1.0.0'
        }

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp."""
        if self.verbose or level in ["ERROR", "CRITICAL"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = {"INFO": "ℹ️", "ERROR": "❌", "SUCCESS": "✅", "WARNING": "⚠️"}.get(level, "📋")
            print(f"[{timestamp}] {prefix} {message}")

    def check_environment(self) -> bool:
        """Verify the assignment environment and structure."""
        self.log("Checking assignment environment...")

        required_files = [
            'src/spatial_basics.py',
            'tests/test_spatial_basics.py',
            'pyproject.toml'
        ]

        required_dirs = ['src', 'tests', 'data']

        missing_items = []

        # Check directories
        for dir_name in required_dirs:
            if not Path(dir_name).exists():
                missing_items.append(f"Directory: {dir_name}/")

        # Check files
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_items.append(f"File: {file_path}")

        if missing_items:
            self.log("Missing required files/directories:", "ERROR")
            for item in missing_items:
                self.log(f"  - {item}", "ERROR")
            return False

        self.log("Assignment structure verified", "SUCCESS")
        return True

    def test_imports(self) -> Dict[str, bool]:
        """Test if required functions can be imported."""
        self.log("Testing function imports...")

        import_results = {}

        try:
            # Test individual function imports
            for func_name in self.function_points.keys():
                try:
                    exec(f"from src.spatial_basics import {func_name}")
                    import_results[func_name] = True
                    self.log(f"  ✅ {func_name} import successful")
                except ImportError as e:
                    import_results[func_name] = False
                    self.log(f"  ❌ {func_name} import failed: {e}", "ERROR")
                except Exception as e:
                    import_results[func_name] = False
                    self.log(f"  ❌ {func_name} import error: {e}", "ERROR")

            # Test if functions are implemented (not just pass statements)
            try:
                import inspect
                from src.spatial_basics import (
                    load_spatial_dataset, explore_spatial_properties,
                    validate_spatial_data, standardize_crs
                )

                functions = [load_spatial_dataset, explore_spatial_properties,
                           validate_spatial_data, standardize_crs]

                implemented_count = 0
                for func in functions:
                    try:
                        source = inspect.getsource(func)
                        # Simple heuristic: if function has more than just pass or is longer
                        if 'pass' not in source or len(source.strip().split('\n')) > 10:
                            implemented_count += 1
                            self.log(f"  📝 {func.__name__} appears implemented")
                        else:
                            self.log(f"  ⚠️  {func.__name__} may be placeholder only", "WARNING")
                    except Exception as e:
                        self.log(f"  ⚠️  Could not analyze {func.__name__}: {e}", "WARNING")

                self.log(f"Implementation progress: {implemented_count}/{len(functions)} functions", "INFO")

            except Exception as e:
                self.log(f"Could not analyze implementation status: {e}", "WARNING")

        except Exception as e:
            self.log(f"Critical import error: {e}", "ERROR")
            for func_name in self.function_points.keys():
                import_results[func_name] = False

        return import_results

    def run_tests(self) -> Tuple[int, str]:
        """Run pytest and return exit code and output."""
        self.log("Running comprehensive test suite...")

        # Pytest command with comprehensive options
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--junit-xml=test-results.xml",
            "--disable-warnings"  # Reduce noise in output
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            self.log(f"Tests completed with exit code: {result.returncode}")

            if self.verbose:
                self.log("Test output:")
                print(result.stdout)
                if result.stderr:
                    self.log("Test errors:", "WARNING")
                    print(result.stderr)

            return result.returncode, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            self.log("Tests timed out after 5 minutes", "ERROR")
            return -1, "Tests timed out"
        except Exception as e:
            self.log(f"Error running tests: {e}", "ERROR")
            return -1, str(e)

    def parse_test_results(self) -> Dict[str, Dict[str, Any]]:
        """Parse pytest XML results and categorize by function."""
        self.log("Parsing test results...")

        category_breakdown = {}

        # Initialize categories
        for func_name, max_points in self.function_points.items():
            category_breakdown[func_name] = {
                'earned': 0,
                'possible': max_points,
                'percentage': 0,
                'tests_passed': 0,
                'tests_total': 0,
                'test_details': []
            }

        if not Path('test-results.xml').exists():
            self.log("No test results file found", "WARNING")
            return category_breakdown

        try:
            tree = ET.parse('test-results.xml')
            root = tree.getroot()

            # Parse test cases
            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name', '')
                class_name = testcase.get('classname', '')

                # Determine which function this test belongs to
                assigned_function = None
                for func_name in self.function_points.keys():
                    if func_name in test_name or func_name in class_name:
                        assigned_function = func_name
                        break

                if assigned_function:
                    category = category_breakdown[assigned_function]
                    category['tests_total'] += 1

                    # Check if test passed
                    failure = testcase.find('failure')
                    error = testcase.find('error')

                    if failure is None and error is None:
                        category['tests_passed'] += 1
                        category['test_details'].append({
                            'name': test_name,
                            'status': 'PASS',
                            'message': None
                        })
                    else:
                        failure_msg = failure.get('message', '') if failure is not None else ''
                        error_msg = error.get('message', '') if error is not None else ''
                        message = failure_msg or error_msg

                        category['test_details'].append({
                            'name': test_name,
                            'status': 'FAIL',
                            'message': message[:200] + '...' if len(message) > 200 else message
                        })

            # Calculate points for each function
            for func_name, category in category_breakdown.items():
                if category['tests_total'] > 0:
                    percentage = category['tests_passed'] / category['tests_total']
                    category['percentage'] = round(percentage * 100, 1)
                    category['earned'] = round(category['possible'] * percentage)
                else:
                    category['percentage'] = 0
                    category['earned'] = 0

                self.log(f"  {func_name}: {category['tests_passed']}/{category['tests_total']} tests passed ({category['percentage']}%) = {category['earned']}/{category['possible']} points")

        except Exception as e:
            self.log(f"Error parsing test results: {e}", "ERROR")
            self.log(f"Traceback: {traceback.format_exc()}", "ERROR")

        return category_breakdown

    def calculate_letter_grade(self, percentage: float) -> str:
        """Calculate letter grade based on percentage."""
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

    def generate_feedback(self, category_breakdown: Dict[str, Dict[str, Any]],
                         import_results: Dict[str, bool]) -> List[str]:
        """Generate detailed feedback for students."""
        feedback = []

        for func_name, breakdown in category_breakdown.items():
            if not import_results.get(func_name, False):
                feedback.append(f"❌ {func_name}: Function cannot be imported. Check for syntax errors or missing implementation.")
            elif breakdown['earned'] == breakdown['possible']:
                feedback.append(f"✅ {func_name}: Excellent work! All tests passed ({breakdown['tests_passed']}/{breakdown['tests_total']}).")
            elif breakdown['earned'] > 0:
                feedback.append(f"⚠️  {func_name}: Partial credit earned. {breakdown['tests_passed']}/{breakdown['tests_total']} tests passed. Review failing tests for improvement opportunities.")
            else:
                if breakdown['tests_total'] > 0:
                    feedback.append(f"❌ {func_name}: No points earned. 0/{breakdown['tests_total']} tests passed. Function may not be implemented or has major issues.")
                else:
                    feedback.append(f"❌ {func_name}: No tests found for this function. Ensure function is properly implemented and named.")

        return feedback

    def create_grade_summary(self, grade_report: Dict[str, Any]) -> str:
        """Create student-friendly grade summary."""
        summary = f"""# 📊 Assignment Grade Report

**Assignment**: {grade_report['assignment']}
**Total Score**: {grade_report['total_points']}/{grade_report['possible_points']} points ({grade_report['percentage']:.1f}%)
**Letter Grade**: {grade_report['letter_grade']}
**Graded**: {datetime.fromisoformat(grade_report['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}

## 📈 Function Scores:
"""

        for func_name, breakdown in grade_report['category_breakdown'].items():
            summary += f"\n- **{func_name}**: {breakdown['earned']}/{breakdown['possible']} points ({breakdown['percentage']}%)"
            if breakdown['tests_total'] > 0:
                summary += f" - {breakdown['tests_passed']}/{breakdown['tests_total']} tests passed"

        summary += "\n\n## 💡 Feedback:\n"
        for item in grade_report['feedback']:
            summary += f"- {item}\n"

        # Add improvement suggestions for low scores
        if grade_report['percentage'] < 80:
            summary += "\n## 🔧 Improvement Suggestions:\n"
            summary += "- Review the interactive notebooks for implementation guidance\n"
            summary += "- Test your functions individually before running the full test suite\n"
            summary += "- Focus on functions with 0 points first - these likely have syntax or import errors\n"
            summary += "- Check that function names match exactly (case-sensitive)\n"
            summary += "- Ensure all required parameters and return types are correct\n"

        # Add encouragement for good scores
        elif grade_report['percentage'] >= 90:
            summary += "\n## 🎉 Excellent Work!\n"
            summary += "- Your implementation demonstrates strong understanding of spatial data concepts\n"
            summary += "- Continue building on this foundation in the next assignment\n"
            summary += "- Consider exploring additional GeoPandas functionality\n"

        summary += "\n---\n*Automated grading system - Contact your instructor with questions about this feedback*"

        return summary

    def set_environment_variables(self, grade_report: Dict[str, Any]):
        """Set environment variables for GitHub Actions integration."""
        os.environ['ASSIGNMENT_SCORE'] = str(grade_report['total_points'])
        os.environ['ASSIGNMENT_TOTAL'] = str(grade_report['possible_points'])
        os.environ['ASSIGNMENT_PERCENTAGE'] = f"{grade_report['percentage']:.1f}"
        os.environ['ASSIGNMENT_GRADE'] = grade_report['letter_grade']
        os.environ['ASSIGNMENT_TIMESTAMP'] = grade_report['timestamp']

    def grade_assignment(self) -> Dict[str, Any]:
        """Main grading workflow."""
        self.log("🎯 Starting GeoPandas assignment grading...")

        # Step 1: Check environment
        if not self.check_environment():
            self.grade_report['feedback'].append("❌ Assignment structure is incomplete. Missing required files or directories.")
            return self.grade_report

        # Step 2: Test imports
        import_results = self.test_imports()
        failed_imports = [func for func, success in import_results.items() if not success]

        if failed_imports:
            self.grade_report['feedback'].append(f"⚠️  Import issues with: {', '.join(failed_imports)}")

        # Step 3: Run tests
        test_exit_code, test_output = self.run_tests()

        # Step 4: Parse results
        category_breakdown = self.parse_test_results()

        # Step 5: Calculate final grade
        total_earned = sum(cat['earned'] for cat in category_breakdown.values())
        percentage = (total_earned / self.total_points) * 100
        letter_grade = self.calculate_letter_grade(percentage)

        # Step 6: Generate feedback
        feedback = self.generate_feedback(category_breakdown, import_results)

        # Step 7: Compile final report
        self.grade_report.update({
            'total_points': total_earned,
            'percentage': round(percentage, 1),
            'letter_grade': letter_grade,
            'category_breakdown': category_breakdown,
            'feedback': feedback,
            'test_exit_code': test_exit_code
        })

        self.log(f"Grading complete: {total_earned}/{self.total_points} points ({percentage:.1f}%) - {letter_grade}", "SUCCESS")

        return self.grade_report


def main():
    """Main entry point for the grading script."""
    parser = argparse.ArgumentParser(description="Grade GeoPandas Introduction Assignment")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json-only", "-j", action="store_true", help="Output JSON only")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory for reports")

    args = parser.parse_args()

    # Initialize grader
    grader = GeoPandasGrader(verbose=args.verbose)

    try:
        # Run grading
        grade_report = grader.grade_assignment()

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)

        # Save JSON report
        json_path = output_dir / 'grade-report.json'
        with open(json_path, 'w') as f:
            json.dump(grade_report, f, indent=2)
        grader.log(f"Grade report saved: {json_path}")

        # Save student summary
        if not args.json_only:
            summary = grader.create_grade_summary(grade_report)
            summary_path = output_dir / 'grade-summary.md'
            with open(summary_path, 'w') as f:
                f.write(summary)
            grader.log(f"Grade summary saved: {summary_path}")

            # Display summary
            print("\n" + "="*50)
            print(summary)
            print("="*50)

        # Set environment variables for CI
        grader.set_environment_variables(grade_report)

        # Exit code based on completion
        if grade_report['total_points'] == 0 and grade_report.get('test_exit_code', 0) != 0:
            sys.exit(1)  # Tests failed to run
        else:
            sys.exit(0)  # Grading completed successfully

    except Exception as e:
        grader.log(f"Critical error in grading: {e}", "ERROR")
        grader.log(f"Traceback: {traceback.format_exc()}", "ERROR")
        sys.exit(2)


if __name__ == "__main__":
    main()
