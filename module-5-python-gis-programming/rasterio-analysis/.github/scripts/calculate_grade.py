#!/usr/bin/env python3
"""
Professional Grading Engine for Rasterio Analysis Assignment
===========================================================

This script provides automated grading and feedback for the GIST 604B
Rasterio Analysis assignment, featuring advanced raster processing and analysis.

The assignment tests 5 core analytical functions:
1. calculate_topographic_metrics - Terrain analysis (5 points)
2. analyze_vegetation_indices - Remote sensing analysis (5 points)
3. sample_raster_at_locations - Spatial sampling (5 points)
4. process_cloud_optimized_geotiff - Efficient data processing (5 points)
5. query_stac_and_analyze - Modern data discovery (5 points)

Total possible points: 25

Usage:
    python calculate_grade.py --results test-results.xml --output grade-report.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import xml.etree.ElementTree as ET


class RasterioAnalysisGrader:
    """
    Professional grading engine for the Rasterio Analysis assignment.

    This grader evaluates student implementations of 5 advanced raster analysis
    functions and provides comprehensive feedback with professional standards.
    """

    # Grade boundaries for letter grades
    GRADE_BOUNDARIES = {
        'A': 90,  # 22.5+ points
        'B': 80,  # 20+ points
        'C': 70,  # 17.5+ points
        'D': 60,  # 15+ points
        'F': 0    # Below 15 points
    }

    # Function categories and their point values
    FUNCTION_CATEGORIES = {
        'topographic_metrics': {
            'name': 'calculate_topographic_metrics',
            'points': 5,
            'description': 'Topographic analysis and terrain modeling',
            'skills': ['Slope calculation', 'Aspect analysis', 'Hillshade generation', 'Terrain classification']
        },
        'vegetation_indices': {
            'name': 'analyze_vegetation_indices',
            'points': 5,
            'description': 'Vegetation analysis and remote sensing',
            'skills': ['NDVI calculation', 'EVI computation', 'Vegetation classification', 'Health assessment']
        },
        'spatial_sampling': {
            'name': 'sample_raster_at_locations',
            'points': 5,
            'description': 'Spatial sampling and interpolation',
            'skills': ['Point sampling', 'Buffer analysis', 'Interpolation methods', 'Coordinate transformation']
        },
        'cog_processing': {
            'name': 'process_cloud_optimized_geotiff',
            'points': 5,
            'description': 'Cloud-optimized geospatial processing',
            'skills': ['COG structure analysis', 'Efficient windowed reading', 'Overview optimization', 'Performance metrics']
        },
        'stac_analysis': {
            'name': 'query_stac_and_analyze',
            'points': 5,
            'description': 'STAC catalog integration and temporal analysis',
            'skills': ['STAC catalog querying', 'Temporal data analysis', 'Time series processing', 'Change detection']
        }
    }

    def __init__(self, results_file: str, output_file: str):
        """
        Initialize the grader with test results and output configuration.

        Args:
            results_file: Path to pytest XML results file
            output_file: Path to save JSON grade report
        """
        self.results_file = Path(results_file)
        self.output_file = Path(output_file)
        self.test_results = {}
        self.category_scores = {}
        self.total_points = 0
        self.total_possible = 25
        self.percentage = 0.0
        self.letter_grade = 'F'
        self.feedback = []

    def parse_test_results(self) -> Dict[str, Any]:
        """
        Parse pytest XML results and extract test information.

        Returns:
            Dictionary containing parsed test results
        """
        try:
            if not self.results_file.exists():
                print(f"❌ Test results file not found: {self.results_file}")
                return self._create_empty_results()

            tree = ET.parse(self.results_file)
            root = tree.getroot()

            # Extract test summary
            test_summary = {
                'tests_total': int(root.get('tests', 0)),
                'tests_passed': 0,
                'tests_failed': 0,
                'tests_skipped': int(root.get('skipped', 0)),
                'tests_errors': int(root.get('errors', 0)),
                'execution_time': float(root.get('time', 0.0)),
                'test_details': []
            }

            # Parse individual test cases
            for testcase in root.findall('.//testcase'):
                test_name = testcase.get('name', 'unknown_test')
                class_name = testcase.get('classname', 'unknown_class')
                execution_time = float(testcase.get('time', 0.0))

                # Determine test status
                status = 'passed'
                error_message = None
                error_type = None

                # Check for failures
                failure = testcase.find('failure')
                if failure is not None:
                    status = 'failed'
                    error_message = failure.text
                    error_type = failure.get('message', 'Test failed')
                    test_summary['tests_failed'] += 1
                # Check for errors
                elif testcase.find('error') is not None:
                    error = testcase.find('error')
                    status = 'error'
                    error_message = error.text
                    error_type = error.get('message', 'Test error')
                    test_summary['tests_errors'] += 1
                # Check for skipped tests
                elif testcase.find('skipped') is not None:
                    status = 'skipped'
                    skip_info = testcase.find('skipped')
                    error_message = skip_info.get('message', 'Test skipped')
                else:
                    test_summary['tests_passed'] += 1

                test_detail = {
                    'name': test_name,
                    'class': class_name,
                    'status': status,
                    'time': execution_time,
                    'error_message': error_message,
                    'error_type': error_type
                }
                test_summary['test_details'].append(test_detail)

            self.test_results = test_summary
            return test_summary

        except ET.ParseError as e:
            print(f"❌ Error parsing XML results: {e}")
            return self._create_empty_results()
        except Exception as e:
            print(f"❌ Unexpected error parsing results: {e}")
            return self._create_empty_results()

    def _create_empty_results(self) -> Dict[str, Any]:
        """Create empty results structure when parsing fails."""
        return {
            'tests_total': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'tests_skipped': 0,
            'tests_errors': 0,
            'execution_time': 0.0,
            'test_details': []
        }

    def categorize_tests(self) -> Dict[str, Dict[str, Any]]:
        """
        Categorize test results by function and calculate category scores.

        Returns:
            Dictionary with category-wise test results and scores
        """
        # Initialize category scores
        for category_key, category_info in self.FUNCTION_CATEGORIES.items():
            self.category_scores[category_key] = {
                'name': category_info['name'],
                'description': category_info['description'],
                'skills': category_info['skills'],
                'possible_points': category_info['points'],
                'earned_points': 0,
                'tests_passed': 0,
                'tests_total': 0,
                'tests_failed': 0,
                'percentage': 0.0,
                'status': 'incomplete',
                'feedback': []
            }

        # Process each test and assign to categories
        for test in self.test_results.get('test_details', []):
            test_name = test['name'].lower()
            category_assigned = False

            # Map tests to categories based on test naming patterns
            for category_key, category_info in self.FUNCTION_CATEGORIES.items():
                function_name = category_info['name']

                # Check if test belongs to this function category
                if (function_name.replace('_', '') in test_name.replace('_', '') or
                    category_key in test_name or
                    any(skill.lower().replace(' ', '') in test_name.replace('_', '')
                        for skill in category_info['skills'])):

                    self.category_scores[category_key]['tests_total'] += 1

                    if test['status'] == 'passed':
                        self.category_scores[category_key]['tests_passed'] += 1
                    elif test['status'] in ['failed', 'error']:
                        self.category_scores[category_key]['tests_failed'] += 1

                        # Add specific error feedback
                        error_msg = test.get('error_message', 'Unknown error')
                        if error_msg and len(error_msg) < 200:  # Keep feedback concise
                            self.category_scores[category_key]['feedback'].append(
                                f"❌ {test['name']}: {error_msg[:100]}..."
                            )

                    category_assigned = True
                    break

            # Handle uncategorized tests
            if not category_assigned and test['status'] == 'passed':
                print(f"⚠️  Uncategorized passing test: {test['name']}")

        # Calculate scores and percentages for each category
        for category_key in self.category_scores:
            category = self.category_scores[category_key]

            if category['tests_total'] > 0:
                # Calculate percentage of tests passed
                test_percentage = (category['tests_passed'] / category['tests_total']) * 100

                # Award points based on test passage rate
                if test_percentage >= 90:
                    category['earned_points'] = category['possible_points']
                    category['status'] = 'excellent'
                elif test_percentage >= 80:
                    category['earned_points'] = int(category['possible_points'] * 0.9)
                    category['status'] = 'good'
                elif test_percentage >= 70:
                    category['earned_points'] = int(category['possible_points'] * 0.8)
                    category['status'] = 'acceptable'
                elif test_percentage >= 50:
                    category['earned_points'] = int(category['possible_points'] * 0.6)
                    category['status'] = 'needs_improvement'
                else:
                    category['earned_points'] = int(category['possible_points'] * 0.3)
                    category['status'] = 'incomplete'

                category['percentage'] = test_percentage
            else:
                # No tests found for this category
                category['status'] = 'not_implemented'
                category['feedback'].append(f"❌ No tests found for {category['name']} function")

        return self.category_scores

    def calculate_grade(self) -> Dict[str, Any]:
        """
        Calculate final grade based on category scores.

        Returns:
            Dictionary containing final grade information
        """
        # Sum up points from all categories
        self.total_points = sum(cat['earned_points'] for cat in self.category_scores.values())
        self.percentage = (self.total_points / self.total_possible) * 100

        # Determine letter grade
        self.letter_grade = 'F'  # Default
        for letter, threshold in self.GRADE_BOUNDARIES.items():
            if self.percentage >= threshold:
                self.letter_grade = letter
                break

        return {
            'total_points': self.total_points,
            'total_possible': self.total_possible,
            'percentage': self.percentage,
            'letter_grade': self.letter_grade,
            'tests_passed': self.test_results.get('tests_passed', 0),
            'tests_total': self.test_results.get('tests_total', 0),
            'category_breakdown': self.category_scores
        }

    def generate_feedback(self) -> List[str]:
        """
        Generate comprehensive feedback based on performance.

        Returns:
            List of feedback messages
        """
        feedback = []

        # Overall performance feedback
        if self.percentage >= 90:
            feedback.append("🎉 Outstanding work! You've mastered advanced raster analysis techniques.")
            feedback.append("Your implementations demonstrate professional-level geospatial programming skills.")
        elif self.percentage >= 80:
            feedback.append("👍 Excellent work! Your raster analysis skills are developing well.")
            feedback.append("Minor refinements needed in some analytical functions.")
        elif self.percentage >= 70:
            feedback.append("👌 Good progress on raster analysis fundamentals.")
            feedback.append("Focus on improving accuracy and completeness of analytical calculations.")
        elif self.percentage >= 60:
            feedback.append("📚 Basic understanding demonstrated, but significant improvements needed.")
            feedback.append("Review assignment requirements and analytical methodology.")
        else:
            feedback.append("🔧 Major improvements required across all analytical functions.")
            feedback.append("Consider reviewing course materials and seeking additional help.")

        # Category-specific feedback
        feedback.append("\n📊 Function-by-Function Analysis:")

        for category_key, category in self.category_scores.items():
            status_emoji = {
                'excellent': '🌟', 'good': '✅', 'acceptable': '👍',
                'needs_improvement': '⚠️', 'incomplete': '❌', 'not_implemented': '🚫'
            }

            emoji = status_emoji.get(category['status'], '❓')
            feedback.append(
                f"{emoji} {category['name']}: {category['earned_points']}/{category['possible_points']} points "
                f"({category['percentage']:.1f}% tests passed)"
            )

            if category['status'] == 'excellent':
                feedback.append(f"   Perfect implementation of {category['description']}")
            elif category['status'] == 'not_implemented':
                feedback.append(f"   Missing: {category['description']}")
                feedback.append(f"   Required skills: {', '.join(category['skills'])}")
            elif category['feedback']:
                feedback.append(f"   Issues found in {category['description']}")
                for fb in category['feedback'][:2]:  # Limit to 2 most relevant issues
                    feedback.append(f"   {fb}")

        # Professional development context
        feedback.append(f"\n🎯 Professional Skills Assessment:")
        skills_mastered = sum(1 for cat in self.category_scores.values()
                            if cat['status'] in ['excellent', 'good'])
        total_skills = len(self.category_scores)

        feedback.append(f"Skills mastered: {skills_mastered}/{total_skills}")
        feedback.append("These advanced raster analysis capabilities are essential for:")
        feedback.append("• Environmental monitoring and assessment")
        feedback.append("• Natural hazard analysis and modeling")
        feedback.append("• Agricultural and forestry applications")
        feedback.append("• Urban planning and development")
        feedback.append("• Climate change research")

        self.feedback = feedback
        return feedback

    def output_for_github_actions(self) -> None:
        """
        Set environment variables for GitHub Actions workflow.
        """
        env_vars = {
            'LETTER_GRADE': self.letter_grade,
            'GRADE_PERCENTAGE': f"{self.percentage:.1f}",
            'POINTS': str(self.total_points),
            'TESTS_PASSED': str(self.test_results.get('tests_passed', 0)),
            'TESTS_TOTAL': str(self.test_results.get('tests_total', 0)),
            'ASSIGNMENT_STATUS': 'COMPLETE' if self.percentage >= 70 else 'NEEDS_WORK'
        }

        # Write to GITHUB_ENV if available
        github_env = os.environ.get('GITHUB_ENV')
        if github_env:
            try:
                with open(github_env, 'a') as f:
                    for key, value in env_vars.items():
                        f.write(f"{key}={value}\n")
                print("✅ Environment variables set for GitHub Actions")
            except Exception as e:
                print(f"⚠️  Could not write to GITHUB_ENV: {e}")

        # Also print for immediate visibility
        print("\n" + "="*50)
        print("📊 GRADING SUMMARY")
        print("="*50)
        for key, value in env_vars.items():
            print(f"{key}={value}")
        print("="*50)

    def save_grade_report(self) -> None:
        """
        Save comprehensive grade report as JSON file.
        """
        report = {
            'assignment': 'Rasterio Analysis - Advanced Raster Processing',
            'timestamp': datetime.now().isoformat(),
            'student_info': {
                'total_points': self.total_points,
                'possible_points': self.total_possible,
                'percentage': round(self.percentage, 2),
                'letter_grade': self.letter_grade
            },
            'test_execution': {
                'tests_total': self.test_results.get('tests_total', 0),
                'tests_passed': self.test_results.get('tests_passed', 0),
                'tests_failed': self.test_results.get('tests_failed', 0),
                'tests_skipped': self.test_results.get('tests_skipped', 0),
                'tests_errors': self.test_results.get('tests_errors', 0),
                'execution_time': self.test_results.get('execution_time', 0.0)
            },
            'function_analysis': self.category_scores,
            'feedback': self.feedback,
            'professional_context': {
                'skills_assessed': list(self.FUNCTION_CATEGORIES.keys()),
                'industry_relevance': 'Advanced raster analysis for environmental and geospatial applications',
                'next_steps': [
                    'Apply techniques to real-world datasets',
                    'Explore additional vegetation indices',
                    'Integrate with cloud-based processing workflows',
                    'Develop automated monitoring systems'
                ]
            }
        }

        try:
            with open(self.output_file, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Grade report saved to {self.output_file}")
        except Exception as e:
            print(f"❌ Error saving grade report: {e}")

    def run(self) -> Dict[str, Any]:
        """
        Execute the complete grading workflow.

        Returns:
            Final grade results dictionary
        """
        print("🎓 Starting Rasterio Analysis Assignment Grading...")
        print(f"📄 Results file: {self.results_file}")
        print(f"💾 Output file: {self.output_file}")

        # Parse test results
        print("\n📊 Parsing test results...")
        self.parse_test_results()
        print(f"Tests found: {self.test_results.get('tests_total', 0)}")
        print(f"Tests passed: {self.test_results.get('tests_passed', 0)}")

        # Categorize and score tests
        print("\n🔍 Analyzing function implementations...")
        self.categorize_tests()

        # Calculate final grade
        print("\n📈 Calculating final grade...")
        grade_info = self.calculate_grade()

        # Generate feedback
        print("\n💬 Generating feedback...")
        self.generate_feedback()

        # Output for GitHub Actions
        print("\n🔧 Setting up GitHub Actions environment...")
        self.output_for_github_actions()

        # Save comprehensive report
        print("\n💾 Saving grade report...")
        self.save_grade_report()

        print(f"\n🎯 Final Grade: {self.letter_grade} ({self.percentage:.1f}%)")
        print(f"📊 Points: {self.total_points}/{self.total_possible}")

        return grade_info


def main():
    """
    Main entry point for the grading script.
    """
    parser = argparse.ArgumentParser(
        description='Professional grading engine for Rasterio Analysis assignment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python calculate_grade.py --results test-results.xml --output grade-report.json
  python calculate_grade.py -r tests.xml -o grades.json

This grader evaluates 5 advanced raster analysis functions:
1. calculate_topographic_metrics - Terrain analysis (5 points)
2. analyze_vegetation_indices - Remote sensing (5 points)
3. sample_raster_at_locations - Spatial sampling (5 points)
4. process_cloud_optimized_geotiff - COG processing (5 points)
5. query_stac_and_analyze - STAC integration (5 points)
        """
    )

    parser.add_argument(
        '--results', '-r',
        type=str,
        required=True,
        help='Path to pytest XML results file'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Path to save JSON grade report'
    )

    args = parser.parse_args()

    try:
        # Initialize and run grader
        grader = RasterioAnalysisGrader(args.results, args.output)
        final_results = grader.run()

        # Exit with appropriate code
        if final_results['percentage'] >= 70:
            print("\n✅ Assignment completed successfully!")
            sys.exit(0)
        else:
            print("\n⚠️  Assignment needs improvement.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Grading failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
