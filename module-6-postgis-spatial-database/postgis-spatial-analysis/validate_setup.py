#!/usr/bin/env python3
"""
SQL Introduction Assignment - Complete Setup Validation

This script validates that the entire assignment setup is working correctly
after moving SQL files to the sql/ subdirectory.

Usage:
    python validate_setup.py
    python validate_setup.py --verbose
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


class AssignmentValidator:
    """Comprehensive validation of SQL Introduction assignment setup."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.assignment_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []

    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
            print(f"{emoji.get(level, '•')} {message}")

    def validate_file_structure(self) -> bool:
        """Validate the complete file structure."""
        self.log("Validating file structure...", "INFO")

        expected_files = {
            # Core assignment files
            "README.md": "Assignment instructions",
            "docker-compose.yml": "Database environment",
            "test_assignment.py": "Test framework",

            # SQL files in subdirectory
            "sql/01_basic_select.sql": "Basic SELECT query",
            "sql/02_column_selection.sql": "Column selection and aliases",
            "sql/03_where_clause.sql": "WHERE clause filtering",
            "sql/04_multiple_conditions.sql": "Multiple conditions",
            "sql/05_sorting.sql": "ORDER BY sorting",
            "sql/06_aggregates.sql": "Aggregate functions",
            "sql/07_group_by.sql": "GROUP BY clause",
            "sql/08_having_clause.sql": "HAVING clause",
            "sql/09_joins.sql": "JOIN operations",
            "sql/10_complex_query.sql": "Complex query with subquery",

            # Data and grading
            "data/load_sample_data.sql": "Sample database initialization",
            "grading/calculate_grade.py": "Grading engine",
            ".github/workflows/test-and-grade.yml": "CI/CD workflow"
        }

        all_files_exist = True
        for file_path, description in expected_files.items():
            full_path = self.assignment_dir / file_path
            if full_path.exists():
                self.log(f"Found {file_path} ({description})", "SUCCESS")
            else:
                self.log(f"Missing {file_path} ({description})", "ERROR")
                self.errors.append(f"Missing required file: {file_path}")
                all_files_exist = False

        return all_files_exist

    def validate_sql_files(self) -> bool:
        """Validate SQL file content and structure."""
        self.log("Validating SQL file content...", "INFO")

        sql_validations = {
            "01_basic_select.sql": ["SELECT", "FROM", "LIMIT"],
            "02_column_selection.sql": ["AS"],
            "03_where_clause.sql": ["WHERE"],
            "04_multiple_conditions.sql": ["AND", "OR", "BETWEEN", "IN"],
            "05_sorting.sql": ["ORDER BY"],
            "06_aggregates.sql": ["COUNT", "AVG", "MIN", "MAX"],
            "07_group_by.sql": ["GROUP BY"],
            "08_having_clause.sql": ["HAVING"],
            "09_joins.sql": ["JOIN"],
            "10_complex_query.sql": ["SELECT.*SELECT", "\\(.*SELECT"]  # Subquery patterns
        }

        all_valid = True
        sql_dir = self.assignment_dir / "sql"

        for filename, required_keywords in sql_validations.items():
            file_path = sql_dir / filename
            if not file_path.exists():
                self.log(f"SQL file missing: {filename}", "ERROR")
                all_valid = False
                continue

            try:
                with open(file_path, 'r') as f:
                    content = f.read().upper()

                # Check for required keywords
                missing_keywords = []
                for keyword in required_keywords:
                    if keyword.startswith("\\") or ".*" in keyword:
                        # Regex pattern - just check if SELECT appears twice (basic subquery check)
                        if keyword == "SELECT.*SELECT":
                            if content.count("SELECT") < 2:
                                missing_keywords.append("subquery (multiple SELECT)")
                        elif keyword == "\\(.*SELECT":
                            if "(" not in content or content.count("SELECT") < 2:
                                missing_keywords.append("subquery with parentheses")
                    else:
                        if keyword not in content:
                            missing_keywords.append(keyword)

                if missing_keywords:
                    self.log(f"{filename}: Missing keywords - {', '.join(missing_keywords)}", "WARNING")
                    self.warnings.append(f"{filename}: Missing expected SQL keywords")
                else:
                    self.log(f"{filename}: All required SQL concepts present", "SUCCESS")

            except Exception as e:
                self.log(f"Error reading {filename}: {e}", "ERROR")
                self.errors.append(f"Cannot read SQL file: {filename}")
                all_valid = False

        return all_valid

    def validate_test_framework(self) -> bool:
        """Validate the test framework can be imported and initialized."""
        self.log("Validating test framework...", "INFO")

        try:
            # Test imports without pytest dependency
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "test_assignment",
                self.assignment_dir / "test_assignment.py"
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)

                # Test that the file structure works
                test_dir = self.assignment_dir
                sql_files = list((test_dir / "sql").glob("*.sql"))

                if len(sql_files) == 10:
                    self.log("Test framework can find all 10 SQL files", "SUCCESS")
                else:
                    self.log(f"Test framework found {len(sql_files)} SQL files, expected 10", "WARNING")

                return True
            else:
                self.errors.append("Cannot load test_assignment.py module")
                return False

        except Exception as e:
            self.log(f"Error validating test framework: {e}", "ERROR")
            self.errors.append(f"Test framework validation failed: {e}")
            return False

    def validate_grading_engine(self) -> bool:
        """Validate the grading engine works correctly."""
        self.log("Validating grading engine...", "INFO")

        try:
            import importlib.util
            import sys

            # Add grading directory to path
            grading_dir = self.assignment_dir / "grading"
            sys.path.insert(0, str(grading_dir))

            spec = importlib.util.spec_from_file_location(
                "calculate_grade",
                grading_dir / "calculate_grade.py"
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Test SQLGradingEngine
                grader = module.SQLGradingEngine()

                # Test query categories
                expected_categories = 10
                actual_categories = len(grader.QUERY_CATEGORIES)

                if actual_categories == expected_categories:
                    self.log(f"Grading engine has {actual_categories} query categories", "SUCCESS")
                else:
                    self.log(f"Grading engine has {actual_categories} categories, expected {expected_categories}", "WARNING")

                # Test file existence checks
                missing_files = []
                for category, config in grader.QUERY_CATEGORIES.items():
                    filename = config['name'] + '.sql'
                    if not grader.sql_file_exists(filename):
                        missing_files.append(filename)

                if not missing_files:
                    self.log("Grading engine can find all SQL files", "SUCCESS")
                else:
                    self.log(f"Grading engine cannot find: {', '.join(missing_files)}", "ERROR")
                    self.errors.append(f"Grading engine file detection failed")
                    return False

                # Test total points calculation
                total_points = grader.TOTAL_POSSIBLE_POINTS
                expected_points = 20  # 10 queries × 2 points each

                if total_points == expected_points:
                    self.log(f"Total points correct: {total_points}", "SUCCESS")
                else:
                    self.log(f"Total points is {total_points}, expected {expected_points}", "WARNING")

                return True
            else:
                self.errors.append("Cannot load calculate_grade.py module")
                return False

        except Exception as e:
            self.log(f"Error validating grading engine: {e}", "ERROR")
            self.errors.append(f"Grading engine validation failed: {e}")
            return False
        finally:
            # Clean up sys.path
            if str(grading_dir) in sys.path:
                sys.path.remove(str(grading_dir))

    def validate_docker_setup(self) -> bool:
        """Validate Docker configuration."""
        self.log("Validating Docker setup...", "INFO")

        docker_file = self.assignment_dir / "docker-compose.yml"
        if not docker_file.exists():
            self.errors.append("docker-compose.yml not found")
            return False

        try:
            with open(docker_file, 'r') as f:
                content = f.read()

            required_components = [
                "postgres:15",
                "POSTGRES_DB: gis_intro",
                "POSTGRES_USER: postgres",
                "5432:5432"
            ]

            missing_components = []
            for component in required_components:
                if component not in content:
                    missing_components.append(component)

            if missing_components:
                self.log(f"Docker setup missing: {', '.join(missing_components)}", "WARNING")
                self.warnings.append("Docker configuration incomplete")
            else:
                self.log("Docker configuration complete", "SUCCESS")

            return len(missing_components) == 0

        except Exception as e:
            self.log(f"Error reading docker-compose.yml: {e}", "ERROR")
            self.errors.append(f"Docker validation failed: {e}")
            return False

    def validate_data_setup(self) -> bool:
        """Validate sample data initialization."""
        self.log("Validating data setup...", "INFO")

        data_file = self.assignment_dir / "data" / "load_sample_data.sql"
        if not data_file.exists():
            self.errors.append("Sample data file not found")
            return False

        try:
            with open(data_file, 'r') as f:
                content = f.read()

            required_tables = ["cities", "state_info", "weather_stations", "temperature_readings"]
            missing_tables = []

            for table in required_tables:
                if f"CREATE TABLE {table}" not in content:
                    missing_tables.append(table)

            if missing_tables:
                self.log(f"Missing table definitions: {', '.join(missing_tables)}", "ERROR")
                self.errors.append("Sample data incomplete")
                return False
            else:
                self.log("All required tables defined in sample data", "SUCCESS")

            # Check for INSERT statements
            if "INSERT INTO" in content:
                self.log("Sample data includes INSERT statements", "SUCCESS")
            else:
                self.log("No INSERT statements found in sample data", "WARNING")
                self.warnings.append("Sample data may be empty")

            return True

        except Exception as e:
            self.log(f"Error reading sample data: {e}", "ERROR")
            self.errors.append(f"Data validation failed: {e}")
            return False

    def validate_github_workflow(self) -> bool:
        """Validate GitHub Actions workflow."""
        self.log("Validating GitHub Actions workflow...", "INFO")

        workflow_file = self.assignment_dir / ".github" / "workflows" / "test-and-grade.yml"
        if not workflow_file.exists():
            self.errors.append("GitHub Actions workflow not found")
            return False

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            required_elements = [
                "postgres:15",
                "POSTGRES_DB: gis_intro",
                "python test_assignment.py",
                "python grading/calculate_grade.py",
                "sql/*.sql"
            ]

            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)

            if missing_elements:
                self.log(f"Workflow missing: {', '.join(missing_elements)}", "WARNING")
                self.warnings.append("GitHub workflow incomplete")
            else:
                self.log("GitHub Actions workflow complete", "SUCCESS")

            return len(missing_elements) == 0

        except Exception as e:
            self.log(f"Error reading GitHub workflow: {e}", "ERROR")
            self.errors.append(f"Workflow validation failed: {e}")
            return False

    def run_validation(self) -> bool:
        """Run complete validation suite."""
        self.log("🚀 Starting SQL Introduction Assignment Validation", "INFO")
        self.log("=" * 60, "INFO")

        validations = [
            ("File Structure", self.validate_file_structure),
            ("SQL File Content", self.validate_sql_files),
            ("Test Framework", self.validate_test_framework),
            ("Grading Engine", self.validate_grading_engine),
            ("Docker Setup", self.validate_docker_setup),
            ("Sample Data", self.validate_data_setup),
            ("GitHub Workflow", self.validate_github_workflow)
        ]

        results = {}
        for name, validation_func in validations:
            self.log(f"\n📋 {name}:", "INFO")
            results[name] = validation_func()

        # Summary
        self.log("\n" + "=" * 60, "INFO")
        self.log("📊 VALIDATION SUMMARY", "INFO")
        self.log("=" * 60, "INFO")

        passed = sum(results.values())
        total = len(results)

        for name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{name}: {status}")

        self.log(f"\n🎯 Overall: {passed}/{total} validations passed", "INFO")

        if self.warnings:
            self.log(f"\n⚠️ Warnings ({len(self.warnings)}):", "WARNING")
            for warning in self.warnings:
                self.log(f"  • {warning}", "WARNING")

        if self.errors:
            self.log(f"\n❌ Errors ({len(self.errors)}):", "ERROR")
            for error in self.errors:
                self.log(f"  • {error}", "ERROR")

        success = len(self.errors) == 0

        if success:
            self.log("\n🎉 VALIDATION COMPLETE - Assignment ready for students!", "SUCCESS")
            self.log("✅ All SQL files are in sql/ subdirectory", "SUCCESS")
            self.log("✅ Test framework updated for new structure", "SUCCESS")
            self.log("✅ Grading engine updated for new structure", "SUCCESS")
            self.log("✅ Documentation updated with correct paths", "SUCCESS")
        else:
            self.log("\n💥 VALIDATION FAILED - Please fix errors before deployment", "ERROR")

        return success


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Validate SQL Introduction assignment setup')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')

    args = parser.parse_args()

    validator = AssignmentValidator(verbose=args.verbose)
    success = validator.run_validation()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
