#!/usr/bin/env python3
"""
Script to create all lecture and assignment files for GIST 604B course planning.
This script generates the complete directory structure and markdown files for all modules.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Module definitions with their lectures and assignments
MODULES = {
    "module-0-introduction-open-source": {
        "title": "Introduction and Open Source",
        "lectures": [
            "lecture-class-introduction-course-overview.md",
            "lecture-open-source-philosophy-history.md",
            "lecture-licensing-legal-considerations.md",
            "lecture-business-models-sustainability.md",
            "lecture-community-development-governance.md",
            "lecture-gis-ecosystem-overview.md"
        ],
        "assignments": [
            "assignment-open-source-discovery.md"
        ]
    },
    "module-1-github-repository-management": {
        "title": "GitHub and Repository Management",
        "lectures": [
            "lecture-github-platform-overview.md",
            "lecture-repository-structure-organization.md",
            "lecture-github-features-collaboration.md",
            "lecture-contributing-open-source.md",
            "lecture-professional-development-workflows.md"
        ],
        "assignments": [
            "assignment-github-hello.md"
        ]
    },
    "module-2-source-code-management-git": {
        "title": "Source Code Management (Git)",
        "lectures": [
            "lecture-git-fundamentals-version-control.md",
            "lecture-branch-management-strategies.md",
            "lecture-github-desktop-workflow.md",
            "lecture-collaborative-development-pull-requests.md",
            "lecture-advanced-git-operations.md"
        ],
        "assignments": [
            "assignment-github-branch.md",
            "assignment-github-desktop.md"
        ]
    },
    "module-3-qgis-desktop-gis": {
        "title": "Open Source Desktop GIS - QGIS",
        "lectures": [
            "lecture-qgis-interface-functionality.md",
            "lecture-spatial-data-loading.md",
            "lecture-symbology-cartographic-design.md",
            "lecture-spatial-analysis-workflows.md",
            "lecture-data-creation-editing.md",
            "lecture-map-layout-export.md"
        ],
        "assignments": [
            "assignment-qgis-tutorials-intro.md",
            "assignment-qgis-tutorials-intermediate.md",
            "assignment-qgis-tutorials-advanced.md",
            "assignment-qgis-team-mapping-project.md"
        ]
    },
    "module-4-containerization-docker": {
        "title": "Containerization - Docker",
        "lectures": [
            "lecture-containerization-docker-fundamentals.md",
            "lecture-docker-gis-applications.md",
            "lecture-github-codespaces-setup.md",
            "lecture-container-orchestration-deployment.md",
            "lecture-docker-networking-persistence.md"
        ],
        "assignments": [
            "assignment-codespace-intro.md",
            "assignment-docker-gis-stack.md"
        ]
    },
    "module-5-python-gis-programming": {
        "title": "Open Source GIS Programming with Python",
        "lectures": [
            "lecture-python-pandas-data-science.md",
            "lecture-geopandas-vector-analysis.md",
            "lecture-spatial-joins-integration.md",
            "lecture-rasterio-processing.md",
            "lecture-pyqgis-automation.md",
            "lecture-python-gis-ecosystem.md"
        ],
        "assignments": [
            "assignment-python-pandas.md",
            "assignment-python-geopandas-intro.md",
            "assignment-python-geopandas-join.md",
            "assignment-python-rasterio.md"
        ]
    },
    "module-6-postgis-spatial-database": {
        "title": "Open Source Spatial RDBMS - PostGIS",
        "lectures": [
            "lecture-sql-fundamentals-gis.md",
            "lecture-postgis-spatial-functions.md",
            "lecture-osm-data-loading.md",
            "lecture-spatial-query-optimization.md",
            "lecture-postgis-integration.md"
        ],
        "assignments": [
            "assignment-sql-intro.md",
            "assignment-postgis-intro.md",
            "assignment-postgis-osm-load.md"
        ]
    },
    "module-7-ogc-web-services": {
        "title": "OGC Web Services and Tiling",
        "lectures": [
            "lecture-qgis-server-web-services.md",
            "lecture-ogc-standards-implementation.md",
            "lecture-postgis-lightweight-services.md",
            "lecture-vector-raster-tiles.md",
            "lecture-web-service-integration.md",
            "lecture-tiling-strategies-performance.md"
        ],
        "assignments": [
            "assignment-qgis-server-setup.md",
            "assignment-postgis-lightweight-services.md",
            "assignment-ogc-tiling-services.md",
            "assignment-web-service-integration.md"
        ]
    },
    "module-8-web-gis-development": {
        "title": "Open Source GIS Web Development",
        "lectures": [
            "lecture-leaflet-web-mapping.md",
            "lecture-javascript-interactive-gis.md",
            "lecture-web-gis-architecture.md",
            "lecture-python-web-development.md",
            "lecture-progressive-web-apps.md",
            "lecture-ux-design-accessibility.md"
        ],
        "assignments": [
            "assignment-interactive-leaflet-maps.md",
            "assignment-python-web-gis-app.md",
            "assignment-multi-service-web-app.md"
        ]
    },
    "module-9-gdal-ogr-tools": {
        "title": "Open Source Tools - GDAL/OGR",
        "lectures": [
            "lecture-gdal-ogr-command-line.md",
            "lecture-data-format-conversion.md",
            "lecture-automation-batch-processing.md",
            "lecture-gdal-integration-workflows.md",
            "lecture-performance-optimization.md",
            "lecture-quality-control-validation.md"
        ],
        "assignments": [
            "assignment-gdal-data-processing.md",
            "assignment-automated-processing-pipeline.md"
        ]
    }
}

def create_file_with_header(filepath, module_name, file_type, title):
    """Create a markdown file with appropriate header based on type."""

    # Skip if file already exists and has content
    if filepath.exists() and filepath.stat().st_size > 100:
        print(f"Skipped (exists): {filepath}")
        return

    # Extract module info
    module_info = MODULES[module_name]
    module_title = module_info["title"]

    # Determine if this is a lecture or assignment
    if file_type == "lecture":
        template = f"""# Lecture: {title}

## Module: {module_title}
**Duration:** 50 minutes
**Format:** Interactive lecture with multimedia content

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **[Verb]** [learning objective 1]
- **[Verb]** [learning objective 2]
- **[Verb]** [learning objective 3]
- **[Verb]** [learning objective 4]

---

## Lecture Outline

### I. Introduction and Context (10 minutes)
- [Topic overview]
- [Connection to previous modules]
- [Real-world applications]

### II. Core Concepts (25 minutes)
- **[Concept 1]**
  - [Key points]
  - [Examples]

- **[Concept 2]**
  - [Key points]
  - [Examples]

### III. Practical Applications (10 minutes)
- [Demonstration or case study]
- [Tools and techniques]
- [Best practices]

### IV. Summary and Next Steps (5 minutes)
- [Key takeaways]
- [Connection to assignments]
- [Preparation for next lecture]

---

## Key Concepts

### [Concept Name]
[Detailed explanation]

### [Another Concept]
[Detailed explanation]

---

## Interactive Elements

### Discussion Questions
1. [Question 1]
2. [Question 2]
3. [Question 3]

### Hands-on Activity
[Brief activity or demonstration]

---

## Resources

### Required Materials
- [List of required readings, software, etc.]

### Supplementary Resources
- [Additional readings]
- [Online resources]
- [Documentation links]

---

## Preparation for Next Session

### Required Reading
- [Reading assignments]

### Recommended Preparation
- [Software installation]
- [Account setup]
- [Practice exercises]

---

## Notes for Instructors

### Technical Requirements
- [ ] [Equipment needed]
- [ ] [Software setup]
- [ ] [Sample data]

### Common Issues
- [Troubleshooting tips]
- [Alternative approaches]
"""

    elif file_type == "assignment":
        template = f"""# Assignment: {title}

## Module: {module_title}
**Points:** 10
**Due:** One week after assignment
**Type:** [Hands-on Practice / Research / Project]

---

## Assignment Overview

[Brief description of the assignment purpose and what students will accomplish]

---

## Learning Objectives

By completing this assignment, you will be able to:
- **[Verb]** [specific skill or knowledge]
- **[Verb]** [specific skill or knowledge]
- **[Verb]** [specific skill or knowledge]
- **[Verb]** [specific skill or knowledge]

---

## Prerequisites

Before starting this assignment:
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]
- [ ] [Prerequisite 3]

---

## Assignment Tasks

### Part 1: [Task Name] ([Points] points)
[Detailed instructions for first part]

### Part 2: [Task Name] ([Points] points)
[Detailed instructions for second part]

### Part 3: [Task Name] ([Points] points)
[Detailed instructions for third part]

---

## Deliverables

### Primary Submission
[What students need to submit]

### Documentation Requirements
[Any additional documentation needed]

---

## Evaluation Criteria

### Technical Implementation ([Percentage]%)
- [Criteria 1]
- [Criteria 2]

### Quality and Professionalism ([Percentage]%)
- [Criteria 1]
- [Criteria 2]

### Learning Demonstration ([Percentage]%)
- [Criteria 1]
- [Criteria 2]

---

## Resources

### Documentation
- [Links to relevant documentation]

### Tutorials
- [Links to helpful tutorials]

### Sample Data
- [Data sources if needed]

---

## Submission Instructions

1. **File Format**: [Required format]
2. **File Name**: [Naming convention]
3. **Submission Method**: [How to submit]
4. **Due Date**: [Date]

---

## Getting Help

- **Office Hours**: [Information]
- **Email**: aaryn@email.arizona.edu
- **GitHub Discussions**: [Course discussion forum]
"""

    # Write the file
    os.makedirs(filepath.parent, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"Created: {filepath}")

def create_all_files():
    """Create all module directories and files."""

    for module_name, module_info in MODULES.items():
        module_dir = BASE_DIR / module_name

        # Create lectures
        for lecture_file in module_info["lectures"]:
            # Extract title from filename
            title = lecture_file.replace("lecture-", "").replace(".md", "").replace("-", " ").title()
            filepath = module_dir / lecture_file
            create_file_with_header(filepath, module_name, "lecture", title)

        # Create assignments
        for assignment_file in module_info["assignments"]:
            # Extract title from filename
            title = assignment_file.replace("assignment-", "").replace(".md", "").replace("-", " ").title()
            filepath = module_dir / assignment_file
            create_file_with_header(filepath, module_name, "assignment", title)

def main():
    """Main function to create all course files."""
    print("Creating GIST 604B course planning files...")
    print("=" * 50)

    create_all_files()

    print("=" * 50)
    print("File creation complete!")

    # Print summary
    total_files = sum(len(info["lectures"]) + len(info["assignments"]) for info in MODULES.values())
    print(f"Created {total_files} files across {len(MODULES)} modules")

    # Print module summary
    for module_name, module_info in MODULES.items():
        lectures = len(module_info["lectures"])
        assignments = len(module_info["assignments"])
        print(f"  {module_name}: {lectures} lectures, {assignments} assignments")

if __name__ == "__main__":
    main()
