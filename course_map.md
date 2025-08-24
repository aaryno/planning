# Course Map: GIST 604B - Open Source Geographic Information Systems

## Course Learning Outcomes (Syllabus):

**Understand the Open Source software development philosophy** and have basic knowledge of the Software Development Life Cycle.
This objective will be evaluated in assignments, discussions, and practical implementation exercises.

**Be comfortable checking out projects from a Git repo**, creating branches, reviewing changes, and issuing merge requests.
These skills will be evaluated in GitHub assignments and collaborative project work.

**Know and have experience using the primary OGC Standard protocols** for serving and consuming vector and raster data: WMS and WFS.
These skills will be evaluated in web services assignments and integration exercises.

**Be comfortable using QGIS** for loading, symbolizing, and processing data from files, spatial databases, and OGC services.
These skills will be evaluated in QGIS tutorial assignments and practical exercises.

**Be able to perform table joins and spatial joins in QGIS** to combine spatial and tabular data.
These skills will be evaluated in advanced QGIS assignments and data integration projects.

**Be able to write a simple query or function using PyQGIS.**
These skills will be evaluated in Python programming assignments and automation exercises.

**Be comfortable performing basic administration of GeoServer**, including connecting data stores, creating/deleting layers, setting rendering styles on layers, creating layer groups, and using the WMS/WFS examples to generate example OGC queries.
These skills will be evaluated in GeoServer configuration assignments and web services projects.

**Be able to visualize data stored in PostGIS, GeoServer, and shapefiles.**
These skills will be evaluated in database integration assignments and visualization projects.

**Have foundational knowledge and experience using PostGIS.**
These skills will be evaluated in spatial database assignments and query exercises.

**Be able to write basic PostGIS queries** with the assistance of postgis.net and other documentation.
These skills will be evaluated in SQL and spatial query assignments.

**Be familiar with Docker and containerization concepts.**
These skills will be evaluated in containerization assignments and deployment exercises.

**Understand core client-server architecture concepts** and understand which GIS components belong to which class.
These skills will be evaluated in architecture discussions and system design exercises.

**Be able to create a webpage containing interactive GIS maps** that allow you to add/edit/remove data, switch data sources, and perform a variety of web mapping tasks.
These skills will be evaluated in web development assignments and interactive mapping projects.

**Understand how web map tiling works.**
These skills will be evaluated in web mapping assignments and tile service implementation.

---

## Course Map

| Module Title | Outcomes (At the end of this module/unit/week, students will be able to…) | Learning Materials (Lectures, readings, videos, etc.) | Activities/Assignments/Assessments |
|--------------|--------------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------|

### Module 0: Introduction and Open Source
**Identify** the core principles and philosophy of open source software development
**Differentiate** between proprietary and open source software licensing models
**Navigate** GitHub interface and understand repository structure
**Recognize** the importance of community-driven software development
**Examine** real-world examples of open source GIS projects

**Lectures:**
- Class Introduction
- Open Source Software Philosophy
- History and Evolution of Open Source GIS

**Readings:**
- Open Source Initiative Definition
- Case studies of successful open source projects

**[Assignment] GitHub Hello** - Introduction to GitHub platform and basic repository operations
**[Assignment] Open Source Discovery** - Research and analyze open source GIS projects
**[Discussion] Open Source vs. Proprietary Software** - Compare advantages and limitations

---

### Module 1: Source Code Management (Git)
**Create** and manage Git repositories using command line and desktop tools
**Implement** branching strategies for collaborative development
**Execute** merge and pull request workflows
**Resolve** basic merge conflicts in version control
**Apply** best practices for commit messages and repository organization

**Lectures:**
- Git Fundamentals and Version Control Concepts
- GitHub Branch Management
- GitHub Desktop Workflow

**Readings:**
- Git documentation and best practices
- Collaborative development workflows

**[Assignment] GitHub Branch** - Practice creating and managing branches in Git repositories
**[Assignment] GitHub Desktop** - Use GUI tools for Git operations and collaboration
**[Discussion] Version Control Best Practices** - Share experiences with collaborative coding

---

### Module 2: Open Source Desktop GIS - QGIS
**Navigate** the QGIS interface and access core functionality
**Load** and visualize spatial data from multiple file formats
**Apply** symbology and styling techniques for effective cartographic representation
**Execute** spatial analysis tools and geoprocessing operations
**Create** and edit spatial data layers
**Integrate** data from different coordinate reference systems
**Generate** high-quality map layouts and exports

**Lectures:**
- QGIS Interface and Core Functionality
- Spatial Data Formats and Loading
- Symbology and Cartographic Design
- Spatial Analysis Tools

**Readings:**
- QGIS User Guide chapters
- Cartographic design principles

**[Assignment] QGIS Tutorials (Intro)** - Basic QGIS operations and interface navigation
**[Assignment] QGIS Tutorials (Intermediate)** - Spatial analysis and data processing
**[Assignment] QGIS Tutorials (Advanced)** - Complex workflows and automation
**[Assignment] QGIS Secret Mutant Hero Team** - Collaborative mapping project
**[Discussion] QGIS vs. Commercial GIS Software** - Compare features and capabilities

---

### Module 3: Containerization - Docker
**Understand** containerization concepts and benefits for GIS applications
**Create** and manage Docker containers for GIS workflows
**Configure** development environments using GitHub Codespaces
**Deploy** containerized applications for consistent execution across platforms
**Troubleshoot** common containerization issues

**Lectures:**
- Introduction to Containerization
- Docker Fundamentals for GIS
- GitHub Codespaces Development Environment

**Readings:**
- Docker documentation and best practices
- Containerization in enterprise GIS

**[Assignment] Codespace Intro** - Set up and use cloud-based development environments
**[Assignment] Docker** - Create and manage containers for GIS applications
**[Discussion] Containerization Benefits** - Discuss advantages for GIS deployment

---

### Module 4: Open Source GIS Programming with Python
**Write** Python scripts for spatial data processing using Pandas
**Manipulate** geospatial data programmatically with GeoPandas
**Perform** spatial joins and attribute operations through code
**Process** raster data using Rasterio library
**Automate** repetitive GIS workflows through scripting
**Integrate** Python with QGIS through PyQGIS

**Lectures:**
- Python for Data Science with Pandas
- Geospatial Python Programming with GeoPandas
- Spatial Joins and Data Integration
- Raster Processing with Rasterio

**Readings:**
- Python geospatial libraries documentation
- Spatial data processing tutorials

**[Assignment] Python Pandas** - Data manipulation and analysis with tabular data
**[Assignment] Python GeoPandas Intro** - Introduction to geospatial data processing
**[Assignment] Python GeoPandas Join** - Spatial and attribute joins using code
**[Assignment] Python Rasterio** - Raster data processing and analysis
**[Discussion] Python vs. GUI Tools** - Compare programmatic and graphical approaches

---

### Module 5: Open Source Spatial RDBMS - PostGIS
**Understand** relational database concepts for spatial data
**Write** SQL queries for spatial and non-spatial data retrieval
**Execute** PostGIS spatial functions and operations
**Load** and manage large spatial datasets in PostgreSQL/PostGIS
**Optimize** spatial queries for performance
**Connect** external applications to PostGIS databases

**Lectures:**
- SQL Fundamentals for GIS
- PostGIS Introduction and Spatial Functions
- Loading OpenStreetMap Data into PostGIS

**Readings:**
- PostGIS documentation and tutorials
- Spatial database design principles

**[Assignment] SQL Intro** - Basic SQL queries and database operations
**[Assignment] PostGIS Intro** - Spatial functions and geometric operations
**[Assignment] PostGIS OSM Load** - Loading and querying large spatial datasets
**[Discussion] Database vs. File-based Storage** - Compare data management approaches

---

### Module 6: OGC Web Services
**Configure** GeoServer for serving spatial data via web services
**Implement** WMS and WFS protocols for data sharing
**Create** and manage data stores and layers in GeoServer
**Apply** styling and symbology to web-served layers
**Generate** OGC-compliant web service requests
**Integrate** web services with desktop and web GIS applications

**Lectures:**
- GeoServer Introduction and Configuration
- OGC Standards: WMS, WFS, and WCS
- Styling and Layer Management
- Web Service Integration

**Readings:**
- OGC standards documentation
- GeoServer user manual

**[Assignment] GeoServer Intro** - Basic server setup and configuration
**[Assignment] GeoServer - OSM Load** - Serving OpenStreetMap data via web services
**[Assignment] GeoServer - OSM Styles** - Advanced styling and cartographic representation
**[Discussion] Web Services Architecture** - Discuss client-server GIS architecture

---

### Module 7: Open Source GIS Web Development
**Create** interactive web maps using Leaflet JavaScript library
**Implement** user interaction features for web-based GIS
**Develop** web applications that consume GIS web services
**Integrate** multiple data sources in web mapping applications
**Deploy** web-based GIS solutions for end-user access
**Design** responsive and user-friendly mapping interfaces

**Lectures:**
- Web Mapping Fundamentals with Leaflet
- JavaScript for Interactive GIS
- Python Web Application Development
- Web GIS User Experience Design

**Readings:**
- Leaflet documentation and tutorials
- Web development best practices for GIS

**[Assignment] WebGIS - Leaflet** - Create interactive web maps with client-side functionality
**[Assignment] WebGIS - Python Web App** - Develop server-side web applications for GIS
**[Discussion] Web vs. Desktop GIS** - Compare delivery methods for GIS functionality

---

### Module 8: Open Source Tools - GDAL/OGR
**Execute** command-line tools for spatial data conversion and processing
**Automate** data format transformations using GDAL utilities
**Process** large datasets efficiently through command-line operations
**Integrate** GDAL tools into larger GIS workflows
**Troubleshoot** data format and projection issues using OGR tools

**Lectures:**
- GDAL/OGR Introduction and Command-Line Operations
- Data Format Conversion and Transformation
- Automation and Batch Processing

**Readings:**
- GDAL/OGR documentation
- Command-line GIS processing tutorials

**[Assignment] GDAL** - Data conversion and processing using command-line tools
**[Discussion] GUI vs. Command-Line Tools** - Compare different approaches to GIS processing

---

## Assessment Alignment

### Knowledge Level (Remember/Understand)
- **Identify** open source principles and licensing models
- **Recognize** GIS software categories and components
- **Understand** containerization and web services concepts

### Comprehension Level (Understand/Apply)
- **Navigate** software interfaces and development environments
- **Execute** basic operations in QGIS, Python, and database systems
- **Configure** servers and web services

### Application Level (Apply/Analyze)
- **Implement** spatial analysis workflows across multiple platforms
- **Create** integrated solutions using multiple open source tools
- **Troubleshoot** technical issues in complex GIS environments

### Analysis Level (Analyze/Evaluate)
- **Compare** different approaches to GIS problem-solving
- **Evaluate** tool selection for specific use cases
- **Design** efficient workflows for spatial data processing

### Synthesis Level (Create/Evaluate)
- **Develop** custom web applications for GIS functionality
- **Integrate** multiple open source technologies into cohesive solutions
- **Automate** complex spatial data processing workflows