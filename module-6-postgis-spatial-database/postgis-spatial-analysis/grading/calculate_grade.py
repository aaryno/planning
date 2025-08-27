#!/usr/bin/env python3
"""
PostGIS Spatial Analysis Assignment - Professional Grading Engine
================================================================

Automated grading system for progressive spatial analysis queries.
Each query is worth 2 points for a total of 20 points.

Foundation Assignment Pattern (10 functions × 2 points = 20 total):
- Queries 1-4: Guided examples and templates (higher completion expectations)
- Queries 5-7: Moderate challenges (partial credit for attempts)
- Queries 8-10: Advanced challenges (bonus credit for completion)

Usage:
    python grading/calculate_grade.py
    python grading/calculate_grade.py --verbose
    python grading/calculate_grade.py --json-output grade-report.json
"""

import os
import sys
import json
import traceback
import argparse
import subprocess
import psycopg2
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional


class PostGISSpatialAnalysisGrader:
    """Professional grading engine for PostGIS spatial analysis assignment."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.assignment_dir = Path(__file__).parent.parent
        self.total_points = 0
        self.max_points = 20
        self.results = {}
        self.detailed_feedback = []
        self.connection = None
        self.cursor = None

        # Progressive difficulty structure
        self.query_points = {
            "01_spatial_inspection": 2,
            "02_simple_buffers": 2,
            "03_spatial_measurements": 2,
            "04_coordinate_transformations": 2,
            "05_spatial_relationships": 2,
            "06_spatial_joins": 2,
            "07_complex_buffer_analysis": 2,
            "08_multi_layer_intersections": 2,
            "09_network_analysis": 2,
            "10_decision_analysis_challenge": 2
        }

        # Difficulty levels for adaptive grading
        self.difficulty_levels = {
            "guided": ["01_spatial_inspection", "02_simple_buffers", "03_spatial_measurements", "04_coordinate_transformations"],
            "moderate": ["05_spatial_relationships", "06_spatial_joins", "07_complex_buffer_analysis"],
            "advanced": ["08_multi_layer_intersections", "09_network_analysis", "10_decision_analysis_challenge"]
        }

    def log(self, message: str, level: str = "INFO"):
        """Log messages with optional verbosity control."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "ERROR" or self.verbose:
            print(f"[{timestamp}] {level}: {message}")

    def setup_database_connection(self) -> bool:
        """Establish database connection for testing."""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'spatial_analysis'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASS', 'postgres'),
                port=os.getenv('DB_PORT', 5432)
            )
            self.cursor = self.connection.cursor()

            # Test PostGIS availability
            self.cursor.execute("SELECT PostGIS_Version();")
            postgis_version = self.cursor.fetchone()[0]
            self.log(f"Connected to database with PostGIS {postgis_version}")
            return True

        except Exception as e:
            self.log(f"Database connection failed: {e}", "ERROR")
            return False

    def cleanup_database_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_sql_file(self, filename: str) -> Tuple[bool, List[Tuple], str]:
        """Execute SQL file and return success status, results, and error message."""
        sql_file = self.assignment_dir / "sql" / filename

        if not sql_file.exists():
            return False, [], f"SQL file not found: {filename}"

        try:
            with open(sql_file, 'r') as f:
                sql_content = f.read()

            # Remove comments for execution
            sql_lines = []
            in_comment_block = False

            for line in sql_content.split('\n'):
                line = line.strip()

                # Handle multi-line comments
                if '/*' in line and '*/' in line:
                    continue
                elif '/*' in line:
                    in_comment_block = True
                    continue
                elif '*/' in line:
                    in_comment_block = False
                    continue
                elif in_comment_block:
                    continue

                # Skip single-line comments and empty lines
                if line.startswith('--') or not line:
                    continue

                sql_lines.append(line)

            sql_query = ' '.join(sql_lines)

            # Check for incomplete work - but handle progressive difficulty
            query_num = int(filename[:2])

            if '____' in sql_query:
                if query_num <= 4:  # Guided templates should be completed
                    return False, [], "Query contains unfinished template blanks"
                else:  # Advanced queries may have some blanks as design choices
                    if sql_query.count('____') > 10:
                        return False, [], "Query appears significantly incomplete"

            # Check if query is too short (likely not implemented)
            if len(sql_query.strip()) < 30:
                if query_num <= 7:
                    return False, [], "Query not implemented"
                else:
                    return False, [], "Advanced challenge not attempted"

            # Execute the query
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()

            return True, results, "Success"

        except psycopg2.Error as e:
            return False, [], f"SQL execution error: {str(e)}"
        except Exception as e:
            return False, [], f"File processing error: {str(e)}"

    def grade_guided_query(self, query_name: str, results: List[Tuple]) -> Tuple[int, str]:
        """Grade guided queries (01-04) with high expectations for completion."""
        try:
            if not results:
                return 0, "No results returned - template may not be completed"

            # Basic execution gets 1 point
            points = 1
            feedback = ["Query executed successfully"]

            # Check result quality for second point
            if query_name == "01_spatial_inspection":
                # Should inspect multiple datasets
                if len(results) >= 3:
                    points = 2
                    feedback.append("Successfully inspected multiple spatial datasets")
                else:
                    feedback.append("Incomplete dataset inspection")

            elif query_name == "02_simple_buffers":
                # Should have buffer calculations
                has_buffer_calcs = any(isinstance(row[i], (int, float)) and 2 <= float(row[i]) <= 5
                                     for row in results for i in range(min(6, len(row)))
                                     if row[i] is not None)
                if has_buffer_calcs:
                    points = 2
                    feedback.append("Accurate buffer area calculations")
                else:
                    feedback.append("Buffer calculations may be incorrect")

            elif query_name == "03_spatial_measurements":
                # Should have distance or area measurements
                has_measurements = any(isinstance(row[i], (int, float)) and float(row[i]) > 0
                                     for row in results for i in range(min(5, len(row)))
                                     if row[i] is not None)
                if has_measurements:
                    points = 2
                    feedback.append("Successful spatial measurements")
                else:
                    feedback.append("Spatial measurements may be missing")

            elif query_name == "04_coordinate_transformations":
                # Should demonstrate coordinate system differences
                coordinate_ranges = []
                for row in results:
                    for i in range(2, min(6, len(row))):
                        if isinstance(row[i], (int, float)):
                            coordinate_ranges.append(abs(float(row[i])))

                # Should have both small (degrees) and large (projected) coordinates
                if coordinate_ranges and max(coordinate_ranges) > 1000 * min(coordinate_ranges):
                    points = 2
                    feedback.append("Successful coordinate system transformations")
                else:
                    feedback.append("Coordinate transformation may be incomplete")

            return points, "; ".join(feedback)

        except Exception as e:
            return 1, f"Execution successful but validation error: {str(e)}"

    def grade_moderate_query(self, query_name: str, results: List[Tuple]) -> Tuple[int, str]:
        """Grade moderate difficulty queries (05-07) with partial credit."""
        try:
            if not results:
                return 0, "No results returned - query may not be implemented"

            # Basic execution gets 1 point
            points = 1
            feedback = ["Query executed successfully"]

            # Additional point for meaningful results
            if len(results) >= 2 and len(results[0]) >= 3:
                points = 2
                feedback.append("Meaningful spatial analysis results")

                # Bonus indicators for quality
                if query_name == "05_spatial_relationships":
                    # Look for evidence of spatial relationship functions
                    relationship_evidence = any('protected' in str(cell).lower() or 'watershed' in str(cell).lower()
                                              for row in results for cell in row if cell is not None)
                    if relationship_evidence:
                        feedback.append("Evidence of spatial relationship analysis")

                elif query_name == "06_spatial_joins":
                    # Look for multi-table attributes
                    if len(results[0]) >= 5:
                        feedback.append("Multi-table spatial join successful")

                elif query_name == "07_complex_buffer_analysis":
                    # Look for complex buffer analysis
                    if any(isinstance(cell, (int, float)) and float(cell) > 1
                          for row in results for cell in row if cell is not None):
                        feedback.append("Complex buffer calculations present")

            return points, "; ".join(feedback)

        except Exception as e:
            return 1, f"Execution successful but validation error: {str(e)}"

    def grade_advanced_query(self, query_name: str, results: List[Tuple]) -> Tuple[int, str]:
        """Grade advanced challenge queries (08-10) with bonus credit approach."""
        try:
            if not results:
                return 0, "Advanced challenge not attempted or incomplete"

            # Any meaningful result from advanced challenges deserves credit
            points = 2  # Full credit for attempting advanced challenges
            feedback = ["Advanced spatial analysis challenge completed"]

            # Quality indicators
            if len(results) >= 3:
                feedback.append("Comprehensive analysis results")

            if len(results[0]) >= 5:
                feedback.append("Multi-factor analysis evident")

            # Specific advanced query recognition
            if query_name == "08_multi_layer_intersections":
                feedback.append("Multi-layer intersection analysis accomplished")
            elif query_name == "09_network_analysis":
                feedback.append("Network analysis challenge completed")
            elif query_name == "10_decision_analysis_challenge":
                feedback.append("Ultimate MCDA challenge - exceptional work!")

            return points, "; ".join(feedback)

        except Exception as e:
            return 1, f"Advanced challenge attempted but validation error: {str(e)}"

    def grade_query(self, query_name: str) -> Dict[str, Any]:
        """Grade individual query based on difficulty level."""
        filename = f"{query_name}.sql"
        max_points = self.query_points[query_name]

        self.log(f"Grading {filename}...")

        # Execute the query
        success, results, error_msg = self.execute_sql_file(filename)

        if not success:
            # Handle different failure types based on difficulty
            query_num = int(query_name[:2])

            if "not found" in error_msg:
                status = "FILE_MISSING"
                points = 0
            elif "not implemented" in error_msg or "not attempted" in error_msg:
                if query_num <= 7:
                    status = "NOT_IMPLEMENTED"
                    points = 0
                else:
                    status = "ADVANCED_NOT_ATTEMPTED"
                    points = 0
            elif "incomplete" in error_msg:
                if query_num <= 4:
                    status = "TEMPLATE_INCOMPLETE"
                    points = 0
                else:
                    status = "PARTIAL_ATTEMPT"
                    points = 1  # Partial credit for attempt
            else:
                status = "EXECUTION_ERROR"
                points = 0

            return {
                "query": query_name,
                "filename": filename,
                "points_earned": points,
                "points_possible": max_points,
                "status": status,
                "error": error_msg,
                "feedback": f"Query failed: {error_msg}",
                "execution_time": 0.0
            }

        # Grade based on difficulty level
        start_time = datetime.now()

        if query_name in self.difficulty_levels["guided"]:
            points, feedback = self.grade_guided_query(query_name, results)
        elif query_name in self.difficulty_levels["moderate"]:
            points, feedback = self.grade_moderate_query(query_name, results)
        else:  # advanced
            points, feedback = self.grade_advanced_query(query_name, results)

        execution_time = (datetime.now() - start_time).total_seconds()

        status = "PASSED" if points == max_points else "PARTIAL" if points > 0 else "FAILED"

        return {
            "query": query_name,
            "filename": filename,
            "points_earned": points,
            "points_possible": max_points,
            "status": status,
            "feedback": feedback,
            "result_count": len(results),
            "execution_time": execution_time
        }

    def generate_final_grade(self) -> Dict[str, Any]:
        """Generate final grade report."""
        percentage = (self.total_points / self.max_points) * 100

        # Letter grade calculation
        if percentage >= 95:
            letter_grade = "A+"
        elif percentage >= 90:
            letter_grade = "A"
        elif percentage >= 85:
            letter_grade = "B+"
        elif percentage >= 80:
            letter_grade = "B"
        elif percentage >= 75:
            letter_grade = "C+"
        elif percentage >= 70:
            letter_grade = "C"
        elif percentage >= 65:
            letter_grade = "D+"
        elif percentage >= 60:
            letter_grade = "D"
        else:
            letter_grade = "F"

        # Analyze completion by difficulty level
        guided_points = sum(self.results.get(q, {}).get("points_earned", 0) for q in self.difficulty_levels["guided"])
        moderate_points = sum(self.results.get(q, {}).get("points_earned", 0) for q in self.difficulty_levels["moderate"])
        advanced_points = sum(self.results.get(q, {}).get("points_earned", 0) for q in self.difficulty_levels["advanced"])

        return {
            "assignment": "PostGIS Spatial Analysis - Foundation Level",
            "total_points": self.total_points,
            "possible_points": self.max_points,
            "percentage": round(percentage, 1),
            "letter_grade": letter_grade,
            "timestamp": datetime.now().isoformat(),
            "difficulty_breakdown": {
                "guided_queries": {
                    "points_earned": guided_points,
                    "points_possible": 8,
                    "queries": self.difficulty_levels["guided"]
                },
                "moderate_queries": {
                    "points_earned": moderate_points,
                    "points_possible": 6,
                    "queries": self.difficulty_levels["moderate"]
                },
                "advanced_queries": {
                    "points_earned": advanced_points,
                    "points_possible": 6,
                    "queries": self.difficulty_levels["advanced"]
                }
            },
            "query_results": self.results,
            "performance_analysis": {
                "foundation_mastery": guided_points >= 6,
                "spatial_thinking_development": moderate_points >= 4,
                "advanced_challenge_success": advanced_points >= 2,
                "ready_for_professional_work": percentage >= 80,
                "postgis_proficiency_level": (
                    "Advanced" if percentage >= 85 else
                    "Intermediate" if percentage >= 70 else
                    "Developing"
                )
            },
            "learning_outcomes": {
                "spatial_data_inspection": guided_points >= 2,
                "coordinate_transformations": any("04_coordinate" in q and self.results.get(q, {}).get("points_earned", 0) >= 1 for q in self.results),
                "spatial_relationships": any("05_spatial" in q and self.results.get(q, {}).get("points_earned", 0) >= 1 for q in self.results),
                "multi_table_analysis": any("06_spatial" in q and self.results.get(q, {}).get("points_earned", 0) >= 1 for q in self.results),
                "advanced_analysis": advanced_points >= 2
            }
        }

    def run_grading(self) -> Dict[str, Any]:
        """Execute the complete grading process."""
        self.log("Starting PostGIS Spatial Analysis Assignment Grading")
        self.log("Progressive Difficulty: Guided → Moderate → Advanced")
        self.log("=" * 60)

        # Setup database connection
        if not self.setup_database_connection():
            return {
                "error": "Database connection failed",
                "total_points": 0,
                "possible_points": self.max_points,
                "percentage": 0.0,
                "letter_grade": "F"
            }

        try:
            # Grade each query
            for query_name in self.query_points.keys():
                result = self.grade_query(query_name)
                self.results[query_name] = result
                self.total_points += result["points_earned"]

                # Determine difficulty level for logging
                if query_name in self.difficulty_levels["guided"]:
                    level = "GUIDED"
                elif query_name in self.difficulty_levels["moderate"]:
                    level = "MODERATE"
                else:
                    level = "ADVANCED"

                self.log(f"[{level}] {result['filename']}: {result['points_earned']}/{result['points_possible']} points - {result['status']}")
                if result.get('feedback') and self.verbose:
                    self.log(f"  Feedback: {result['feedback']}")

            # Generate final grade
            final_grade = self.generate_final_grade()

            self.log("=" * 60)
            self.log(f"FINAL GRADE: {final_grade['total_points']}/{final_grade['possible_points']} ({final_grade['percentage']}%) - {final_grade['letter_grade']}")

            # Log difficulty breakdown
            guided = final_grade['difficulty_breakdown']['guided_queries']
            moderate = final_grade['difficulty_breakdown']['moderate_queries']
            advanced = final_grade['difficulty_breakdown']['advanced_queries']

            self.log(f"Guided Queries (1-4): {guided['points_earned']}/{guided['points_possible']}")
            self.log(f"Moderate Queries (5-7): {moderate['points_earned']}/{moderate['points_possible']}")
            self.log(f"Advanced Queries (8-10): {advanced['points_earned']}/{advanced['points_possible']}")

            # Set environment variables for GitHub Actions
            if os.getenv('GITHUB_ACTIONS'):
                os.system(f"echo 'TOTAL_POINTS={final_grade['total_points']}' >> $GITHUB_ENV")
                os.system(f"echo 'POSSIBLE_POINTS={final_grade['possible_points']}' >> $GITHUB_ENV")
                os.system(f"echo 'PERCENTAGE={final_grade['percentage']}' >> $GITHUB_ENV")
                os.system(f"echo 'LETTER_GRADE={final_grade['letter_grade']}' >> $GITHUB_ENV")

            return final_grade

        finally:
            self.cleanup_database_connection()


def main():
    """Main grading function."""
    parser = argparse.ArgumentParser(description='Grade PostGIS Spatial Analysis Assignment')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--json-output', '-j', help='Output JSON report to file')

    args = parser.parse_args()

    # Create grader and run
    grader = PostGISSpatialAnalysisGrader(verbose=args.verbose)
    results = grader.run_grading()

    # Output JSON if requested
    if args.json_output:
        with open(args.json_output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to {args.json_output}")

    # Display summary
    print("\n" + "=" * 60)
    print("POSTGIS SPATIAL ANALYSIS - GRADING SUMMARY")
    print("=" * 60)
    print(f"Assignment: Foundation Level (Progressive Difficulty)")
    print(f"Final Grade: {results.get('total_points', 0)}/{results.get('possible_points', 20)} ({results.get('percentage', 0)}%) - {results.get('letter_grade', 'F')}")

    if 'difficulty_breakdown' in results:
        print(f"\nDifficulty Level Performance:")
        guided = results['difficulty_breakdown']['guided_queries']
        moderate = results['difficulty_breakdown']['moderate_queries']
        advanced = results['difficulty_breakdown']['advanced_queries']
        print(f"  Guided Templates (1-4): {guided['points_earned']}/{guided['points_possible']} points")
        print(f"  Moderate Challenges (5-7): {moderate['points_earned']}/{moderate['points_possible']} points")
        print(f"  Advanced Challenges (8-10): {advanced['points_earned']}/{advanced['points_possible']} points")

    if 'performance_analysis' in results:
        perf = results['performance_analysis']
        print(f"\nLearning Outcomes:")
        print(f"  PostGIS Proficiency: {perf['postgis_proficiency_level']}")
        print(f"  Foundation Mastery: {'✓' if perf['foundation_mastery'] else '○'}")
        print(f"  Spatial Thinking: {'✓' if perf['spatial_thinking_development'] else '○'}")
        print(f"  Advanced Challenges: {'✓' if perf['advanced_challenge_success'] else '○'}")
        print(f"  Professional Ready: {'✓' if perf['ready_for_professional_work'] else '○'}")

    # Exit with error code if assignment failed
    if results.get('percentage', 0) < 60:
        print(f"\n❌ Assignment score below passing threshold (60%)")
        sys.exit(1)
    else:
        print(f"\n✅ Assignment completed successfully!")
        print(f"Grade: {results.get('letter_grade', 'F')} ({results.get('percentage', 0)}%)")


if __name__ == "__main__":
    main()
