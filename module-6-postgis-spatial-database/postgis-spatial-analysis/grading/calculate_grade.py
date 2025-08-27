#!/usr/bin/env python3
"""
PostGIS Spatial Analysis Assignment - Professional Grading Engine
================================================================

Automated grading system for advanced spatial analysis queries.
Each query is worth 5 points for a total of 20 points.

Assignment Categories (4 functions × 5 points = 20 total):
- Multi-Layer Intersection Analysis (5 points)
- Advanced Buffer Analysis (5 points)
- Network Routing Analysis (5 points)
- Multi-Criteria Decision Analysis (5 points)

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

        # Grading criteria for each query
        self.query_points = {
            "01_multi_layer_intersection": 5,
            "02_advanced_buffer_analysis": 5,
            "03_network_routing_analysis": 5,
            "04_multi_criteria_decision_analysis": 5
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

            # Remove comments and check for TODO items
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

            # Check for incomplete work
            if '____' in sql_query or 'TODO' in sql_query.upper():
                return False, [], "Query contains unfinished TODO items or placeholder blanks"

            # Execute the query
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()

            return True, results, "Success"

        except psycopg2.Error as e:
            return False, [], f"SQL execution error: {str(e)}"
        except Exception as e:
            return False, [], f"File processing error: {str(e)}"

    def validate_intersection_analysis(self, results: List[Tuple]) -> Tuple[int, str]:
        """Validate multi-layer intersection analysis results."""
        try:
            if not results:
                return 0, "No results returned - query may be incomplete"

            # Check minimum number of results
            if len(results) < 3:
                return 1, f"Only {len(results)} intersections found, expected at least 3"

            # Validate result structure (should have 7+ columns)
            if len(results[0]) < 7:
                return 1, f"Insufficient columns ({len(results[0])}), expected at least 7"

            points = 2  # Base points for execution
            feedback = []

            # Check for spatial analysis components
            for row in results[:3]:  # Check first 3 rows
                protected_area = row[0]
                watershed_name = row[3] if len(row) > 3 else None
                overlap_acres = row[5] if len(row) > 5 else None
                percent_protected = row[6] if len(row) > 6 else None

                if protected_area is None:
                    feedback.append("Protected area names missing")
                    break

                if watershed_name is None:
                    feedback.append("Watershed names missing")
                    break

                if not isinstance(overlap_acres, (int, float)) or overlap_acres <= 0:
                    feedback.append("Invalid overlap area calculations")
                    break

                if not isinstance(percent_protected, (int, float)) or not (0 <= percent_protected <= 100):
                    feedback.append("Invalid percentage calculations")
                    break
            else:
                points += 1  # +1 for correct data structure
                feedback.append("Correct intersection analysis structure")

            # Check if results are ordered by area (largest first)
            try:
                overlap_areas = [float(row[5]) for row in results if len(row) > 5]
                if overlap_areas == sorted(overlap_areas, reverse=True):
                    points += 1  # +1 for correct ordering
                    feedback.append("Results properly ordered by overlap area")
                else:
                    feedback.append("Results not ordered correctly")
            except:
                feedback.append("Could not validate ordering")

            # Check for significant overlaps only (filtering)
            significant_overlaps = [r for r in results if len(r) > 5 and float(r[5]) > 1000]
            if len(significant_overlaps) == len(results):
                points += 1  # +1 for proper filtering
                feedback.append("Correctly filtered to significant overlaps")

            return min(points, 5), "; ".join(feedback)

        except Exception as e:
            return 1, f"Validation error: {str(e)}"

    def validate_buffer_analysis(self, results: List[Tuple]) -> Tuple[int, str]:
        """Validate advanced buffer analysis results."""
        try:
            if not results:
                return 0, "No results returned - query may be incomplete"

            if len(results) < 2:
                return 1, f"Only {len(results)} facilities found, expected at least 2"

            # Validate result structure (should have 8+ columns)
            if len(results[0]) < 8:
                return 1, f"Insufficient columns ({len(results[0])}), expected at least 8"

            points = 2  # Base points for execution
            feedback = []

            # Validate buffer analysis components
            for row in results[:3]:
                facility_name = row[0]
                routes_1mile = row[2] if len(row) > 2 else None
                routes_5mile = row[3] if len(row) > 3 else None
                closest_distance = row[4] if len(row) > 4 else None
                accessibility_rating = row[7] if len(row) > 7 else None

                if facility_name is None:
                    feedback.append("Facility names missing")
                    break

                if not isinstance(routes_1mile, int) or routes_1mile < 0:
                    feedback.append("Invalid 1-mile route counts")
                    break

                if not isinstance(routes_5mile, int) or routes_5mile < routes_1mile:
                    feedback.append("Invalid 5-mile route counts (should be >= 1-mile counts)")
                    break

                if not isinstance(closest_distance, (int, float)) or closest_distance <= 0:
                    feedback.append("Invalid distance calculations")
                    break

                if accessibility_rating not in ['Excellent Access', 'Good Access', 'Limited Access', 'Remote Location']:
                    feedback.append("Invalid accessibility ratings")
                    break
            else:
                points += 1  # +1 for correct data structure
                feedback.append("Correct buffer analysis structure")

            # Check for limited access filtering
            limited_access_count = sum(1 for row in results if len(row) > 4 and float(row[4]) > 2.0)
            if limited_access_count >= len(results) // 2:
                points += 1  # +1 for proper filtering
                feedback.append("Correctly filtered for limited access facilities")

            # Check ordering by accessibility (most remote first)
            try:
                distances = [float(row[4]) for row in results if len(row) > 4]
                if distances == sorted(distances, reverse=True):
                    points += 1  # +1 for correct ordering
                    feedback.append("Results properly ordered by remoteness")
                else:
                    feedback.append("Ordering could be improved")
            except:
                feedback.append("Could not validate ordering")

            return min(points, 5), "; ".join(feedback)

        except Exception as e:
            return 1, f"Validation error: {str(e)}"

    def validate_routing_analysis(self, results: List[Tuple]) -> Tuple[int, str]:
        """Validate network routing analysis results."""
        try:
            if not results:
                return 0, "No results returned - query may be incomplete"

            if len(results) < 3:
                return 1, f"Only {len(results)} route pairs found, expected at least 3"

            # Validate result structure (should have 10+ columns)
            if len(results[0]) < 10:
                return 1, f"Insufficient columns ({len(results[0])}), expected at least 10"

            points = 2  # Base points for execution
            feedback = []

            # Validate routing analysis components
            routing_ratios = []
            for row in results[:3]:
                origin_name = row[0]
                destination_name = row[2] if len(row) > 2 else None
                straight_line_miles = row[4] if len(row) > 4 else None
                network_miles = row[5] if len(row) > 5 else None
                efficiency_ratio = row[6] if len(row) > 6 else None
                route_difficulty = row[9] if len(row) > 9 else None

                if origin_name == destination_name:
                    feedback.append("Origin and destination should be different")
                    break

                if not isinstance(straight_line_miles, (int, float)) or straight_line_miles <= 0:
                    feedback.append("Invalid straight-line distance calculations")
                    break

                if not isinstance(network_miles, (int, float)) or network_miles < straight_line_miles:
                    feedback.append("Invalid network distance calculations")
                    break

                if not isinstance(efficiency_ratio, (int, float)) or efficiency_ratio < 1.0:
                    feedback.append("Invalid efficiency ratio calculations")
                    break

                if route_difficulty not in ['Easy', 'Moderate', 'Difficult', 'Very Difficult']:
                    feedback.append("Invalid route difficulty classifications")
                    break

                routing_ratios.append(float(efficiency_ratio))
            else:
                points += 1  # +1 for correct data structure
                feedback.append("Correct routing analysis structure")

            # Check for inefficient routes (focus of analysis)
            inefficient_routes = [r for r in routing_ratios if r > 2.0]
            if inefficient_routes:
                points += 1  # +1 for identifying inefficient routes
                feedback.append(f"Successfully identified {len(inefficient_routes)} inefficient routes")

            # Check ordering logic
            try:
                # Should be ordered by improvement priority and efficiency
                priority_order = []
                for row in results:
                    if len(row) > 10:
                        priority = row[10]
                        if priority == 'High Priority':
                            priority_order.append(1)
                        elif priority == 'Medium Priority':
                            priority_order.append(2)
                        else:
                            priority_order.append(3)

                if priority_order == sorted(priority_order):
                    points += 1  # +1 for correct prioritization
                    feedback.append("Results properly prioritized")
            except:
                feedback.append("Could not validate prioritization")

            return min(points, 5), "; ".join(feedback)

        except Exception as e:
            return 1, f"Validation error: {str(e)}"

    def validate_decision_analysis(self, results: List[Tuple]) -> Tuple[int, str]:
        """Validate multi-criteria decision analysis results."""
        try:
            if not results:
                return 0, "No results returned - query may be incomplete"

            if len(results) < 3:
                return 1, f"Only {len(results)} candidates found, expected at least 3"

            # Validate result structure (should have 12+ columns)
            if len(results[0]) < 12:
                return 1, f"Insufficient columns ({len(results[0])}), expected at least 12"

            points = 2  # Base points for execution
            feedback = []

            # Validate multi-criteria analysis components
            composite_scores = []
            for row in results[:5]:  # Check first 5 candidates
                longitude = row[1] if len(row) > 1 else None
                latitude = row[2] if len(row) > 2 else None
                transport_score = row[3] if len(row) > 3 else None
                coverage_score = row[4] if len(row) > 4 else None
                monitoring_score = row[5] if len(row) > 5 else None
                protected_score = row[6] if len(row) > 6 else None
                terrain_score = row[7] if len(row) > 7 else None
                composite_score = row[8] if len(row) > 8 else None
                suitability = row[9] if len(row) > 9 else None

                # Validate coordinates
                if not isinstance(longitude, (int, float)) or not (-110 <= longitude <= -104):
                    feedback.append("Invalid longitude coordinates")
                    break

                if not isinstance(latitude, (int, float)) or not (36 <= latitude <= 42):
                    feedback.append("Invalid latitude coordinates")
                    break

                # Validate individual scores (0-100 scale)
                scores = [transport_score, coverage_score, monitoring_score, protected_score, terrain_score]
                for i, score in enumerate(scores):
                    if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                        feedback.append(f"Invalid criterion score {i+1}")
                        break
                else:
                    # Validate composite score
                    if not isinstance(composite_score, (int, float)) or not (0 <= composite_score <= 100):
                        feedback.append("Invalid composite score calculation")
                        break

                    # Validate weighted calculation (approximately)
                    expected_composite = (transport_score * 0.25 + coverage_score * 0.30 +
                                        monitoring_score * 0.20 + protected_score * 0.15 + terrain_score * 0.10)
                    if abs(composite_score - expected_composite) > 2.0:
                        feedback.append("Composite score calculation error")
                        break

                    if suitability not in ['Excellent', 'Good', 'Fair', 'Poor']:
                        feedback.append("Invalid suitability rating")
                        break

                    composite_scores.append(float(composite_score))
            else:
                points += 1  # +1 for correct data structure
                feedback.append("Correct multi-criteria analysis structure")

            # Check ordering by composite score (best first)
            if composite_scores == sorted(composite_scores, reverse=True):
                points += 1  # +1 for correct ordering
                feedback.append("Results properly ordered by composite score")

            # Check for viable candidates (quality filtering)
            viable_sites = [s for s in composite_scores if s >= 60]
            if len(viable_sites) >= 2:
                points += 1  # +1 for identifying viable candidates
                feedback.append(f"Successfully identified {len(viable_sites)} viable candidate sites")

            return min(points, 5), "; ".join(feedback)

        except Exception as e:
            return 1, f"Validation error: {str(e)}"

    def grade_query(self, query_name: str) -> Dict[str, Any]:
        """Grade individual query and return results."""
        filename = f"{query_name}.sql"
        max_points = self.query_points[query_name]

        self.log(f"Grading {filename}...")

        # Execute the query
        success, results, error_msg = self.execute_sql_file(filename)

        if not success:
            return {
                "query": query_name,
                "filename": filename,
                "points_earned": 0,
                "points_possible": max_points,
                "status": "FAILED",
                "error": error_msg,
                "feedback": f"Query failed to execute: {error_msg}",
                "execution_time": 0.0
            }

        # Validate query-specific requirements
        start_time = datetime.now()

        if query_name == "01_multi_layer_intersection":
            points, feedback = self.validate_intersection_analysis(results)
        elif query_name == "02_advanced_buffer_analysis":
            points, feedback = self.validate_buffer_analysis(results)
        elif query_name == "03_network_routing_analysis":
            points, feedback = self.validate_routing_analysis(results)
        elif query_name == "04_multi_criteria_decision_analysis":
            points, feedback = self.validate_decision_analysis(results)
        else:
            points, feedback = 0, "Unknown query type"

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

        return {
            "assignment": "PostGIS Spatial Analysis",
            "total_points": self.total_points,
            "possible_points": self.max_points,
            "percentage": round(percentage, 1),
            "letter_grade": letter_grade,
            "timestamp": datetime.now().isoformat(),
            "category_breakdown": {
                "multi_layer_intersection": {
                    "earned": self.results.get("01_multi_layer_intersection", {}).get("points_earned", 0),
                    "possible": 5,
                    "status": self.results.get("01_multi_layer_intersection", {}).get("status", "NOT_ATTEMPTED")
                },
                "advanced_buffer_analysis": {
                    "earned": self.results.get("02_advanced_buffer_analysis", {}).get("points_earned", 0),
                    "possible": 5,
                    "status": self.results.get("02_advanced_buffer_analysis", {}).get("status", "NOT_ATTEMPTED")
                },
                "network_routing_analysis": {
                    "earned": self.results.get("03_network_routing_analysis", {}).get("points_earned", 0),
                    "possible": 5,
                    "status": self.results.get("03_network_routing_analysis", {}).get("status", "NOT_ATTEMPTED")
                },
                "multi_criteria_decision_analysis": {
                    "earned": self.results.get("04_multi_criteria_decision_analysis", {}).get("points_earned", 0),
                    "possible": 5,
                    "status": self.results.get("04_multi_criteria_decision_analysis", {}).get("status", "NOT_ATTEMPTED")
                }
            },
            "detailed_results": self.results,
            "performance_notes": {
                "spatial_analysis_proficiency": "Advanced" if percentage >= 85 else "Intermediate" if percentage >= 70 else "Developing",
                "postgis_mastery": percentage >= 80,
                "ready_for_advanced_gis": percentage >= 75
            }
        }

    def run_grading(self) -> Dict[str, Any]:
        """Execute the complete grading process."""
        self.log("Starting PostGIS Spatial Analysis Assignment Grading")
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

                self.log(f"{result['filename']}: {result['points_earned']}/{result['points_possible']} points - {result['status']}")
                if result.get('feedback'):
                    self.log(f"  Feedback: {result['feedback']}")

            # Generate final grade
            final_grade = self.generate_final_grade()

            self.log("=" * 60)
            self.log(f"FINAL GRADE: {final_grade['total_points']}/{final_grade['possible_points']} ({final_grade['percentage']}%) - {final_grade['letter_grade']}")

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

    # Exit with error code if assignment failed
    if results.get('percentage', 0) < 60:
        sys.exit(1)


if __name__ == "__main__":
    main()
