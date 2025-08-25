# GIST 604B Course Planning - Fall 2025 Refresh

## Overview

This directory contains comprehensive course planning materials for GIST 604B: Open Source Geographic Information Systems at the University of Arizona. The course has been redesigned for Fall 2025 with an updated technology stack focused on modern open source GIS tools and workflows.

## Course Structure

The course is organized into **10 modules** (0-9) with a total of **58 lectures** and **26 assignments** covering the complete open source GIS ecosystem:

```
Module 0: Introduction and Open Source (6 lectures, 1 assignment)
Module 1: GitHub and Repository Management (5 lectures, 1 assignment)  
Module 2: Source Code Management (Git) (5 lectures, 2 assignments)
Module 3: Open Source Desktop GIS - QGIS (6 lectures, 4 assignments)
Module 4: Containerization - Docker (5 lectures, 2 assignments)
Module 5: Open Source GIS Programming with Python (6 lectures, 4 assignments)
Module 6: Open Source Spatial RDBMS - PostGIS (5 lectures, 3 assignments)
Module 7: OGC Web Services and Tiling (6 lectures, 4 assignments)
Module 8: Open Source GIS Web Development (6 lectures, 3 assignments)
Module 9: Open Source Tools - GDAL/OGR (6 lectures, 2 assignments)
```

## Technology Stack

The course covers an integrated open source GIS technology stack:

- **Foundation**: Git/GitHub for version control and collaboration
- **Desktop GIS**: QGIS for spatial analysis and visualization
- **Database**: PostgreSQL/PostGIS for spatial data management
- **Programming**: Python (GeoPandas, Rasterio, PyQGIS) for automation
- **Containerization**: Docker for consistent deployment
- **Web Services**: QGIS Server and lightweight PostGIS services
- **Web Development**: Leaflet and modern web mapping frameworks
- **Data Processing**: GDAL/OGR for format conversion and processing

## Key Changes from Previous Version

### Simplified Web Services
- **Replaced GeoServer** with QGIS Server for easier learning curve
- **Added lightweight alternatives**: pg_tileserv and pg_featureserv
- **Enhanced tiling focus**: New OGC Tiling Services assignment
- **Modern standards**: OGC API and vector tiles emphasis

### Enhanced Integration
- **Containerization throughout**: Docker used across multiple modules
- **Progressive skill building**: Each module builds on previous knowledge
- **Real-world workflows**: Professional development practices
- **Version control emphasis**: Git integration in all projects

### Modern Technologies
- **Python-centric approach**: Extensive GeoPandas and automation focus
- **Web development**: Full-stack applications with Leaflet
- **Cloud deployment**: GitHub Codespaces and container orchestration
- **Performance optimization**: Tiling, caching, and scalability

## Directory Structure

```
planning/
├── README.md (this file)
├── course_map.md (comprehensive course learning objectives)
├── create_module_files.py (utility script for file generation)
├── module-0-introduction-open-source/
│   ├── lecture-*.md (6 lecture files)
│   └── assignment-open-source-discovery.md
├── module-1-github-repository-management/
│   ├── lecture-*.md (5 lecture files)
│   └── assignment-github-hello.md
├── module-2-source-code-management-git/
│   ├── lecture-*.md (5 lecture files)
│   ├── assignment-github-branch.md
│   └── assignment-github-desktop.md
├── module-3-qgis-desktop-gis/
│   ├── lecture-*.md (6 lecture files)
│   ├── assignment-qgis-tutorials-intro.md
│   ├── assignment-qgis-tutorials-intermediate.md
│   ├── assignment-qgis-tutorials-advanced.md
│   └── assignment-qgis-team-mapping-project.md
├── module-4-containerization-docker/
│   ├── lecture-*.md (5 lecture files)
│   ├── assignment-codespace-intro.md
│   └── assignment-docker-gis-stack.md
├── module-5-python-gis-programming/
│   ├── lecture-*.md (6 lecture files)
│   ├── assignment-python-pandas.md
│   ├── assignment-python-geopandas-intro.md
│   ├── assignment-python-geopandas-join.md
│   └── assignment-python-rasterio.md
├── module-6-postgis-spatial-database/
│   ├── lecture-*.md (5 lecture files)
│   ├── assignment-sql-intro.md
│   ├── assignment-postgis-intro.md
│   └── assignment-postgis-osm-load.md
├── module-7-ogc-web-services/
│   ├── lecture-*.md (6 lecture files)
│   ├── assignment-qgis-server-setup.md
│   ├── assignment-postgis-lightweight-services.md
│   ├── assignment-ogc-tiling-services.md
│   └── assignment-web-service-integration.md
├── module-8-web-gis-development/
│   ├── lecture-*.md (6 lecture files)
│   ├── assignment-interactive-leaflet-maps.md
│   ├── assignment-python-web-gis-app.md
│   └── assignment-multi-service-web-app.md
└── module-9-gdal-ogr-tools/
    ├── lecture-*.md (6 lecture files)
    ├── assignment-gdal-data-processing.md
    └── assignment-automated-processing-pipeline.md
```

## File Naming Conventions

- **Lectures**: `lecture-[topic-description].md`
- **Assignments**: `assignment-[assignment-name].md`
- **Consistent formatting**: Lowercase with hyphens for readability
- **Descriptive names**: Clear indication of content and purpose

## Content Standards

### Lecture Files Include:
- Learning objectives with action verbs (Bloom's taxonomy)
- 50-minute structured outline with timing
- Interactive elements and hands-on activities
- Key concepts and technical details
- Resources for further learning
- Preparation instructions for next session
- Notes for instructors including common issues

### Assignment Files Include:
- Clear learning objectives and prerequisites
- Detailed task breakdown with point allocations
- Comprehensive deliverable specifications
- Evaluation criteria and rubrics
- Resources and documentation links
- Submission instructions and due dates
- Integration with other course modules
- Troubleshooting and support information

## Quality Assurance

### Technical Accuracy
- All content reviewed for current best practices
- Technology versions and compatibility verified
- Links and resources validated for accessibility
- Code examples tested for functionality

### Pedagogical Design
- Progressive difficulty and skill building
- Multiple learning styles accommodated
- Real-world applications emphasized
- Assessment aligned with learning objectives

### Professional Standards
- Industry-relevant skills and practices
- Current open source GIS ecosystem coverage
- Professional workflow integration
- Career preparation focus

## Implementation Timeline

### Phase 1: Foundation Modules (Weeks 1-4)
- Module 0: Open source principles and philosophy
- Module 1: GitHub and collaboration workflows
- Module 2: Git version control mastery
- Module 3: QGIS desktop GIS proficiency

### Phase 2: Technical Infrastructure (Weeks 5-6)
- Module 4: Docker containerization and deployment
- Module 5: Python GIS programming automation

### Phase 3: Database and Services (Weeks 7-8)
- Module 6: PostGIS spatial database management
- Module 7: OGC web services and tiling

### Phase 4: Integration and Advanced Topics (Weeks 9-10)
- Module 8: Web GIS development and applications
- Module 9: GDAL/OGR data processing pipelines

## Assessment Philosophy

### Grading Approach
- **Completion-focused**: Emphasis on effort and problem-solving
- **Progressive mastery**: Building skills incrementally
- **Real-world application**: Practical, professional skills
- **Collaborative learning**: Peer support encouraged

### Assignment Types
- **Hands-on practice**: Technical skill development
- **Research projects**: Understanding ecosystem and community
- **Integration projects**: Combining multiple technologies
- **Team collaborations**: Professional workflow simulation

## Technology Requirements

### Student Prerequisites
- Computer with admin rights for software installation
- Reliable internet connection for cloud services
- GitHub account for version control and collaboration
- Willingness to work with command-line interfaces

### Software Stack
- Git and GitHub Desktop
- QGIS LTR (Long Term Release)
- Docker Desktop
- Python with scientific computing packages
- Code editor (VS Code recommended)
- PostgreSQL/PostGIS access via containers

## Support Resources

### Documentation
- Comprehensive course map with learning outcomes
- Detailed assignment instructions and rubrics
- Troubleshooting guides for common issues
- Resource links for additional learning

### Community
- GitHub Discussions for peer collaboration
- Office hours for individual support
- Study groups for collaborative problem-solving
- Professional networking opportunities

## Future Development

### Continuous Improvement
- Annual technology stack updates
- Student feedback integration
- Industry trend incorporation
- Guest expert contributions

### Expansion Opportunities
- Advanced modules for specialized topics
- Summer intensive workshops
- Industry partnership projects
- Open source contribution programs

---

## Quick Start for Instructors

1. **Review course_map.md** for comprehensive learning objectives
2. **Examine sample lectures** for presentation format and standards
3. **Study assignment examples** for assessment criteria and expectations
4. **Test technology stack** to ensure all tools work in your environment
5. **Customize content** for your specific teaching style and emphasis

## Quick Start for Students

1. **Read course syllabus** for policies and expectations
2. **Set up GitHub account** and join course organization
3. **Install required software** following provided guides
4. **Review Module 0 materials** to understand open source principles
5. **Prepare for hands-on learning** with curiosity and persistence

---

**Contact Information:**
- Course Instructor: Dr. Aaryn Olsson (aaryn@email.arizona.edu)
- Course GitHub: https://github.com/ua-gist604b-s25
- University of Arizona GIST Program: https://geography.arizona.edu

This planning repository represents a complete redesign of GIST 604B with modern open source GIS technologies, pedagogical best practices, and real-world professional skill development. The course prepares students for careers in the rapidly evolving geospatial technology landscape.