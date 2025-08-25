# Assignment: QGIS Fundamentals for GIS Professionals

## Module: Open Source Desktop GIS - QGIS
**Points:** 25
**Due:** One week after assignment
**Type:** Hands-on Practice with Professional Translation

---

## Assignment Overview

This assignment introduces GIS Masters students to QGIS by leveraging existing GIS knowledge from ESRI products. You'll complete structured tutorials from qgistutorials.com while documenting the translation between ArcGIS workflows and QGIS equivalents. This assignment emphasizes understanding open source alternatives to familiar commercial tools and building confidence with QGIS interface and core functionality.

---

## Learning Objectives

By completing this assignment, you will be able to:
- **Navigate** the QGIS interface efficiently and locate tools equivalent to ArcGIS functions
- **Load** spatial data from multiple formats using QGIS data management tools
- **Apply** symbology and basic styling techniques for cartographic representation
- **Execute** fundamental spatial operations including table joins and attribute queries
- **Compare** QGIS workflows with ArcGIS equivalents and identify advantages/limitations

---

## Prerequisites

Before starting this assignment:
- [ ] Install QGIS 3.34+ (LTR version) on your workstation - [Download](https://qgis.org/en/site/forusers/download.html)
- [ ] Complete Module 0 GitHub setup for assignment submission
- [ ] Familiarity with basic GIS concepts (assumed from ArcGIS experience)
- [ ] Optional: Watch "QGIS for ArcGIS Users" introduction video

---

## Assignment Tasks

### Part 1: Interface Exploration and Basic Mapping (5 points)

Complete the tutorial: [Making a Map in QGIS](http://www.qgistutorials.com/en/docs/3/making_a_map.html)

**ArcGIS Translation Exercise:**
While completing the tutorial, document in a markdown file (`interface_comparison.md`) the QGIS equivalent for these ArcGIS tools:
- Add Data button → QGIS equivalent
- Table of Contents → QGIS equivalent  
- Symbology pane → QGIS equivalent
- Layout View → QGIS equivalent
- Export Map → QGIS equivalent

**Deliverables:**
- `screencap_japan_map.png` - Final styled map from tutorial step 35
- `interface_comparison.md` - ArcGIS to QGIS tool translation table

### Part 2: Attribute Analysis and Selection (5 points)

Complete the tutorial: [Working with Attributes](http://www.qgistutorials.com/en/docs/3/working_with_attributes.html)

**Professional Analysis:**
After completing the tutorial, perform these additional tasks:
1. Create a selection of capitals with population > 1 million
2. Export selected features to a new shapefile named `major_capitals.shp`
3. Calculate a new field showing population density (if area data available)

**Deliverables:**
- `screencap_populated_capitals.png` - Final map from tutorial step 16
- `major_capitals.shp` (with .prj, .dbf, .shx files) - Exported selection
- `attribute_workflow.md` - Compare QGIS Select by Attribute vs ArcGIS equivalent

### Part 3: Symbology and Data Visualization (5 points)

Complete the tutorial: [Basic Vector Styling](http://www.qgistutorials.com/en/docs/3/basic_vector_styling.html)

**Professional Enhancement:**
After the basic tutorial:
1. Create a categorized symbology showing different power plant types
2. Add labels showing power plant names for facilities > 1000MW
3. Create a custom color ramp for the graduated symbols

**Deliverables:**
- `screencap_powerplants_basic.png` - Tutorial completion (step 28)
- `screencap_powerplants_enhanced.png` - Your enhanced symbology
- `symbology_notes.md` - Document 3 symbology features QGIS has that ArcGIS lacks (or vice versa)

### Part 4: CSV Data Integration and Web Services (5 points)

Complete the tutorial: [Importing Spreadsheets/CSV](http://www.qgistutorials.com/en/docs/3/importing_spreadsheets_csv.html)

**Data Source:** Use current earthquake data from USGS: 
[https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv)

**Professional Extension:**
1. Filter earthquakes by magnitude (show only > 4.0)
2. Add a basemap using QuickMapServices plugin
3. Style points by magnitude using graduated symbols
4. Create a simple layout with legend and scale bar

**Deliverables:**
- `screencap_earthquakes_map.png` - Enhanced earthquake visualization
- `data_integration_notes.md` - Compare CSV integration: QGIS vs ArcGIS Pro

### Part 5: Spatial Joins and Table Analysis (5 points)

Complete the tutorial: [Performing Table Joins](http://www.qgistutorials.com/en/docs/3/performing_table_joins.html)

**Advanced Professional Task:**
After completing the basic join:
1. Export the joined layer to a GeoPackage format (.gpkg)
2. Create a choropleth map showing population density by county
3. Add proper classification breaks using Natural Breaks (Jenks)
4. Include data source citation and methodology notes

**Deliverables:**
- `screencap_county_population.png` - Final map with joined data
- `county_population.gpkg` - Joined data in open source format
- `join_comparison.md` - Document advantages of GeoPackage vs Shapefile format

---

## Deliverables

### Primary Submission
GitHub repository branch named `qgis-intro-assignment` containing:
- All required screenshots (PNG format)
- All data files created during exercises
- All markdown documentation files
- `reflection_paper.md` (500-750 words) discussing your transition from ArcGIS to QGIS

### Documentation Requirements
Each markdown file should include:
- Clear headings and organization
- Screenshots where appropriate
- Specific tool names and menu locations
- Professional observations about workflow differences

---

## Evaluation Criteria

### Technical Implementation (60%)
- Successful completion of all qgistutorials.com exercises
- Correct creation of required data outputs and maps
- Proper use of QGIS tools and interface elements
- Quality of cartographic design and symbology

### Professional Analysis (25%)
- Thoughtful comparison between QGIS and ArcGIS workflows
- Identification of advantages and limitations of each platform
- Documentation of tool equivalencies and differences
- Understanding of open source GIS ecosystem concepts

### Documentation and Communication (15%)
- Clear, professional writing in markdown files
- Organized repository structure and file naming
- Comprehensive reflection paper demonstrating learning
- Proper citation of data sources and methodology

---

## ESRI to QGIS Translation Guide

### Common Tool Equivalents
| ArcGIS Tool | QGIS Equivalent | Location |
|-------------|----------------|----------|
| Add Data | Layer → Add Layer | Menu bar or toolbar |
| Table of Contents | Layers Panel | Left panel |
| Attribute Table | Open Attribute Table | Right-click layer |
| Select by Attributes | Select Features by Value | Toolbar |
| Export Data | Export → Save Features As | Right-click layer |
| Symbology | Properties → Symbology | Double-click layer |
| Layout View | Project → New Print Layout | Menu bar |

### Key Differences to Note
- QGIS uses "Projects" instead of "Map Documents"
- Processing Toolbox contains analysis tools (similar to ArcToolbox)
- Plugin system extends functionality (like ArcGIS Extensions)
- Free and open source vs commercial licensing
- Different file format preferences (.gpkg vs .gdb)

---

## Resources

### Essential Documentation
- [QGIS User Guide](https://docs.qgis.org/latest/en/docs/user_manual/) - Official documentation
- [QGIS Training Manual](https://docs.qgis.org/latest/en/docs/training_manual/) - Comprehensive tutorials
- [QGIS Tutorials by Ujaval Gandhi](http://www.qgistutorials.com/) - Assignment source tutorials

### Video Resources
- [QGIS for ArcGIS Users](https://www.youtube.com/watch?v=9OTY7NXlU5I) - Interface comparison
- [QGIS Basics Playlist](https://www.youtube.com/playlist?list=PLO6KswO64zVu9PToJiHQyAhOxPJwLNtl3) - Fundamental operations

### Sample Data Sources
- [Natural Earth](https://www.naturalearthdata.com/) - Free global datasets
- [USGS Earthquake Data](https://earthquake.usgs.gov/earthquakes/feed/v1.0/) - Real-time geospatial data
- [OpenStreetMap](https://www.openstreetmap.org/) - Community-driven mapping data

---

## Professional Development Notes

### Industry Context
- QGIS is used by government agencies, NGOs, and consulting firms worldwide
- Open source GIS reduces software costs and increases customization possibilities
- Many organizations use hybrid workflows combining QGIS and ArcGIS
- QGIS skills are increasingly requested in GIS job postings

### Career Advantages
- Demonstrates adaptability and openness to new tools
- Understanding of open source development and community
- Cost-effective solution knowledge for budget-conscious organizations
- Foundation for advanced open source GIS programming and development

---

## Submission Instructions

1. **Repository Setup**: Create branch named `qgis-intro-assignment` in your course GitHub repository
2. **File Organization**: Create folder structure: `/maps`, `/data`, `/documentation`
3. **File Naming**: Use descriptive names with no spaces (use underscores or hyphens)
4. **Commit Messages**: Use clear, professional commit messages describing changes
5. **Pull Request**: Submit PR to merge assignment branch with main branch
6. **Due Date**: One week from assignment date (check course calendar)

---

## Getting Help

- **Office Hours**: Check course schedule for instructor availability
- **Email**: aaryn@email.arizona.edu for technical issues
- **GitHub Discussions**: Course discussion forum for peer collaboration
- **QGIS Community**: [GIS Stack Exchange](https://gis.stackexchange.com/) for advanced troubleshooting
- **Documentation Issues**: If tutorial links are broken, check course announcements for alternatives

---

## Bonus Opportunities (Optional)

### Plugin Exploration (+2 points)
Install and demonstrate one QGIS plugin that enhances functionality:
- QuickMapServices for basemaps
- QTiles for tile generation  
- Processing R Provider for statistical analysis
- Document plugin functionality in `bonus_plugin.md`

### Format Comparison (+2 points)
Create a technical comparison between Shapefile, GeoPackage, and GeoJSON formats:
- File size differences for same dataset
- Feature support comparison
- Performance considerations
- Industry usage patterns
- Submit as `format_analysis.md`

### Workflow Automation (+3 points)
Create a simple Processing Model that automates a multi-step workflow:
- Buffer creation → Intersect → Calculate statistics
- Document the model creation process
- Export model as .model3 file
- Explain potential time savings for repetitive tasks