# Course Map: GIST 604B - Open Source Geographic Information Systems

## Course Learning Outcomes (Syllabus):

**Understand the Open Source software development philosophy** and have basic knowledge of the Software Development Life Cycle.
This objective will be evaluated in assignments, discussions, and practical implementation exercises.

**Be comfortable checking out projects from a Git repo**, creating branches, reviewing changes, and issuing merge requests.
These skills will be evaluated in GitHub assignments and collaborative project work.

**Know and have experience using the primary OGC Standard protocols** for serving and consuming vector and raster data: WMS, WFS, and OGC Tiles.
These skills will be evaluated in web services assignments and integration exercises using QGIS Server and lightweight PostGIS services.

**Be comfortable using QGIS** for loading, symbolizing, and processing data from files, spatial databases, and OGC services.
These skills will be evaluated in QGIS tutorial assignments and practical exercises.

**Be able to perform table joins and spatial joins in QGIS** to combine spatial and tabular data.
These skills will be evaluated in advanced QGIS assignments and data integration projects.

**Be able to write simple queries and functions using PyQGIS** and Python geospatial libraries.
These skills will be evaluated in Python programming assignments and automation exercises.

**Be comfortable performing basic administration of web mapping services**, including deploying QGIS Server, configuring PostGIS-based services, and testing OGC endpoints.
These skills will be evaluated in web services configuration assignments and integration projects.

**Be able to visualize data stored in PostGIS, served via web services, and local files** using both desktop and web-based tools.
These skills will be evaluated in database integration assignments and multi-platform visualization projects.

**Have foundational knowledge and experience using PostGIS** for spatial data management and analysis.
These skills will be evaluated in spatial database assignments and query exercises.

**Be able to write basic PostGIS queries** with the assistance of postgis.net and other documentation.
These skills will be evaluated in SQL and spatial query assignments.

**Be familiar with Docker and containerization concepts** for consistent GIS application deployment.
These skills will be evaluated in containerization assignments and deployment exercises.

**Understand core client-server architecture concepts** and understand which GIS components belong to which tier.
These skills will be evaluated in architecture discussions and system design exercises.

**Be able to create interactive web maps** that consume OGC services, allow data interaction, and integrate multiple data sources.
These skills will be evaluated in web development assignments using Leaflet and modern web mapping frameworks.

**Understand how web map tiling works** including vector tiles, raster tiles, and OGC tile services.
These skills will be evaluated in tiling assignments and tile service implementation exercises.

---

## Course Map

| Module Title | Outcomes (At the end of this module/unit/week, students will be able to…) | Learning Materials (Lectures, readings, videos, etc.) | Activities/Assignments/Assessments |
|--------------|--------------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------|

### Module 0: Introduction and Open Source
**Identify** the core principles and philosophy of open source software development
**Differentiate** between proprietary and open source software licensing models
**Recognize** the importance of community-driven software development
**Examine** real-world examples of open source GIS projects and their impact
**Evaluate** licensing models and their implications for software development and distribution
**Analyze** the economic and social impacts of open source software in the geospatial industry

**Lectures:**
- Class Introduction and Course Overview
- Open Source Software Philosophy and History
- Licensing Models and Legal Considerations
- Open Source Business Models and Sustainability
- Community-Driven Development and Governance
- Open Source GIS Ecosystem Overview

**Readings:**
- Open Source Initiative Definition and principles
- Case studies of successful open source GIS projects (QGIS, PostGIS, GDAL)
- Comparison of open source vs. proprietary licenses
- "The Cathedral and the Bazaar" by Eric Raymond (selected chapters)

**[Assignment] Open Source Discovery** - Research and analyze open source GIS projects, their communities, and development models
**[Discussion] Open Source Impact** - Discuss advantages, limitations, and real-world impact of open source software in GIS

---

### Module 1: GitHub and Repository Management
**Navigate** GitHub interface and understand repository structure and organization
**Create** and manage GitHub repositories for project collaboration and documentation
**Implement** basic GitHub workflows including issues, project boards, and wikis
**Apply** GitHub features for documentation, collaboration, and project management
**Demonstrate** understanding of GitHub's role in modern open source development
**Contribute** to existing open source projects through GitHub workflows

**Lectures:**
- GitHub Platform Overview and Navigation
- Repository Structure and Organization Best Practices
- GitHub Features: Issues, Projects, Wikis, and Actions
- Contributing to Open Source via GitHub
- GitHub in Professional Development Workflows

**Readings:**
- GitHub documentation and collaboration best practices
- Open source contribution guidelines and etiquette
- GitHub workflow for collaborative development
- Professional portfolio development with GitHub

**[Assignment] GitHub Hello** - Create repositories, practice basic operations, and explore GitHub features
**[Discussion] GitHub's Role in Open Source** - Discuss GitHub's impact on collaborative coding and project discoverability

---

### Module 2: Source Code Management (Git)
**Create** and manage Git repositories using command line and desktop tools effectively
**Implement** branching strategies for collaborative development and feature management
**Execute** merge and pull request workflows with confidence and proper review processes
**Resolve** merge conflicts in version control systems using various strategies
**Apply** best practices for commit messages, repository organization, and code review
**Collaborate** effectively with team members using distributed version control workflows

**Lectures:**
- Git Fundamentals and Distributed Version Control Concepts
- Branch Management and Merging Strategies (Git Flow, GitHub Flow)
- GitHub Desktop Workflow and GUI Tools Integration
- Collaborative Development with Pull Requests and Code Review
- Advanced Git: Rebasing, Cherry-picking, and History Management

**Readings:**
- Git documentation and command reference guide
- Collaborative development workflows and team practices
- Version control best practices for GIS projects
- Git branching models comparison and selection

**[Assignment] GitHub Branch** - Practice creating, managing, and merging branches with realistic collaboration scenarios
**[Assignment] GitHub Desktop** - Master GUI tools for Git operations and team collaboration workflows
**[Discussion] Version Control in GIS Projects** - Share experiences and strategies for effective collaboration in geospatial projects

---

### Module 3: Open Source Desktop GIS - QGIS
**Navigate** the QGIS interface efficiently and access core functionality with confidence
**Load** and visualize spatial data from multiple file formats, databases, and web services
**Apply** symbology and styling techniques for effective cartographic representation and analysis
**Execute** spatial analysis tools and geoprocessing operations for real-world problem solving
**Create** and edit spatial data layers with precision and topological integrity
**Integrate** data from different coordinate reference systems and handle projection issues
**Generate** high-quality map layouts and exports for professional publication and presentation

**Lectures:**
- QGIS Interface and Core Functionality Deep Dive
- Spatial Data Formats and Advanced Loading Techniques
- Symbology and Advanced Cartographic Design Principles
- Spatial Analysis Tools and Geoprocessing Workflows
- Data Creation, Editing, and Quality Control
- Map Layout and Export Options for Multiple Media

**Readings:**
- QGIS User Guide selected chapters
- Cartographic design principles and best practices
- Spatial analysis methodology and workflow design
- QGIS plugin ecosystem and extensibility

**[Assignment] QGIS Tutorials (Intro)** - Master basic QGIS operations, interface navigation, and data loading
**[Assignment] QGIS Tutorials (Intermediate)** - Implement spatial analysis workflows and advanced styling techniques
**[Assignment] QGIS Tutorials (Advanced)** - Execute complex analysis and explore automation possibilities
**[Assignment] QGIS Team Mapping Project** - Collaborative mapping project with team coordination and shared data management
**[Discussion] QGIS in Professional Practice** - Compare QGIS capabilities with commercial alternatives and discuss real-world applications

---

### Module 4: Containerization - Docker
**Understand** containerization concepts and benefits for consistent GIS application deployment
**Create** and manage Docker containers for GIS workflows and service deployment
**Configure** development environments using GitHub Codespaces and local Docker setups
**Deploy** containerized applications for consistent execution across different platforms and environments
**Troubleshoot** common containerization issues in GIS contexts and Docker networking
**Implement** container orchestration concepts for complex multi-service GIS deployments

**Lectures:**
- Introduction to Containerization and Docker Fundamentals
- Docker for GIS Applications: Images, Containers, and Volumes
- GitHub Codespaces Development Environment Setup and Management
- Container Orchestration and Multi-service Deployments
- Docker Networking and Data Persistence for GIS Services

**Readings:**
- Docker documentation and containerization best practices
- Containerization in enterprise GIS and cloud deployments
- Cloud-based development environments and DevOps practices
- Container security and production deployment considerations

**[Assignment] Codespace Intro** - Set up and customize cloud-based development environments for GIS workflows
**[Assignment] Docker GIS Stack** - Create and manage containers for integrated GIS services (database, server, web interface)
**[Discussion] Containerization Benefits** - Discuss advantages for GIS deployment, development, and reproducible research

---

### Module 5: Open Source GIS Programming with Python
**Write** Python scripts for spatial data processing using Pandas for tabular data manipulation
**Manipulate** geospatial data programmatically with GeoPandas for vector operations and analysis
**Perform** spatial joins and attribute operations through code for automated data integration
**Process** raster data using Rasterio library for analysis, transformation, and extraction
**Automate** repetitive GIS workflows through scripting and batch processing techniques
**Integrate** Python with QGIS through PyQGIS for custom tools and automated map production

**Lectures:**
- Python for Data Science with Pandas: Advanced Data Manipulation
- Geospatial Python Programming with GeoPandas: Vector Analysis and Visualization
- Spatial Joins and Data Integration Techniques with Code Examples
- Raster Processing with Rasterio: Analysis and Transformation Workflows
- QGIS Automation with PyQGIS: Custom Tools and Batch Processing
- Python GIS Ecosystem: Libraries, Tools, and Integration Strategies

**Readings:**
- Python geospatial libraries documentation and tutorials
- Spatial data processing best practices and performance optimization
- Programming patterns and best practices for GIS automation
- PyQGIS cookbook and advanced scripting techniques

**[Assignment] Python Pandas** - Master data manipulation and analysis with complex tabular datasets
**[Assignment] Python GeoPandas Intro** - Implement geospatial data processing workflows with vector data
**[Assignment] Python GeoPandas Join** - Execute spatial and attribute joins using programmatic methods
**[Assignment] Python Rasterio** - Develop raster data processing and analysis automation workflows
**[Discussion] Automation vs. GUI Workflows** - Compare programmatic and graphical approaches for different GIS tasks

---

### Module 6: Open Source Spatial RDBMS - PostGIS
**Understand** relational database concepts for spatial data management and enterprise applications
**Write** SQL queries for spatial and non-spatial data retrieval with complex filtering and aggregation
**Execute** PostGIS spatial functions and geometric operations for advanced spatial analysis
**Load** and manage large spatial datasets in PostgreSQL/PostGIS using efficient import strategies
**Optimize** spatial queries for performance using indexes, query planning, and best practices
**Connect** external applications to PostGIS databases for integrated GIS workflows and data sharing

**Lectures:**
- SQL Fundamentals for GIS Applications and Spatial Data Management
- PostGIS Introduction: Spatial Functions and Geometric Operations
- Loading OpenStreetMap Data into PostGIS: Large Dataset Management
- Spatial Query Optimization: Indexes, Performance, and Best Practices
- PostGIS Integration: Connecting Desktop and Web Applications

**Readings:**
- PostGIS documentation and comprehensive function reference
- Spatial database design principles and normalization strategies
- SQL performance optimization techniques for large spatial datasets
- Enterprise spatial database architecture and administration

**[Assignment] SQL Intro** - Master SQL fundamentals with spatial data queries and database operations
**[Assignment] PostGIS Intro** - Implement spatial functions and geometric operations with real-world datasets
**[Assignment] PostGIS OSM Load** - Load, index, and efficiently query large spatial datasets (OpenStreetMap)
**[Discussion] Database vs. File Storage** - Compare data management approaches, scalability, and performance considerations

---

### Module 7: OGC Web Services and Tiling
**Configure** QGIS Server for serving spatial data via standardized OGC web services
**Implement** WMS and WFS protocols using familiar QGIS project files for seamless desktop-to-web workflows
**Deploy** lightweight PostGIS-based services (pg_tileserv, pg_featureserv) for microservice architectures
**Create** and serve vector and raster tiles using OGC Tiles API and modern tiling standards
**Generate** and test OGC-compliant web service requests using various client applications
**Integrate** web services with desktop GIS, web applications, and mobile platforms
**Compare** different web service architectures and select appropriate solutions for specific use cases

**Lectures:**
- QGIS Server: From Desktop Projects to Web Services
- OGC Standards: WMS, WFS, and OGC Tiles API Implementation
- Lightweight PostGIS Services: pg_tileserv and pg_featureserv
- Vector Tiles vs. Raster Tiles: Technology Comparison and Use Cases
- Web Service Integration and Client Application Development
- Tiling Strategies: Performance, Caching, and Scalability

**Readings:**
- QGIS Server documentation and deployment best practices
- OGC standards documentation (WMS, WFS, OGC Tiles)
- PostGIS web services comparison and architecture patterns
- Modern web mapping tile formats and optimization strategies

**[Assignment] QGIS Server Setup** - Deploy QGIS projects as web services using Docker containerization
**[Assignment] PostGIS Lightweight Services** - Configure and deploy pg_tileserv and pg_featureserv for data serving
**[Assignment] OGC Tiling Services** - Implement vector and raster tile serving with OGC Tiles API and performance optimization
**[Assignment] Web Service Integration** - Build client applications that consume multiple OGC services
**[Discussion] Service Architecture Trade-offs** - Compare simple vs. enterprise solutions for different deployment scenarios

---

### Module 8: Open Source GIS Web Development
**Create** interactive web maps using Leaflet JavaScript library with advanced customization
**Implement** user interaction features for web-based GIS applications including editing and analysis
**Develop** web applications that consume and integrate multiple OGC web services seamlessly
**Integrate** real-time data sources and dynamic content in comprehensive web mapping applications
**Deploy** production-ready web-based GIS solutions with proper error handling and user experience
**Design** responsive and accessible mapping interfaces that work across devices and platforms
**Build** full-stack GIS applications using modern web development frameworks and spatial APIs

**Lectures:**
- Modern Web Mapping with Leaflet: Advanced Features and Customization
- JavaScript for Interactive GIS: Event Handling and User Interface Design
- Web GIS Architecture: Client-Server Integration and API Design
- Python Web Application Development for GIS: Flask/FastAPI with Spatial Extensions
- Progressive Web Apps for GIS: Offline Functionality and Mobile Optimization
- Web GIS User Experience Design and Accessibility Standards

**Readings:**
- Leaflet documentation and advanced plugin ecosystem
- Modern web development best practices for mapping applications
- Web accessibility guidelines for interactive mapping interfaces
- Performance optimization for web-based geospatial applications

**[Assignment] Interactive Leaflet Maps** - Create sophisticated web maps with custom controls, popups, and user interactions
**[Assignment] Python Web GIS Application** - Develop full-stack web applications with spatial APIs and database integration
**[Assignment] Multi-Service Web App** - Build applications that integrate multiple OGC services and data sources
**[Discussion] Web vs. Desktop GIS** - Analyze delivery methods, user experience, and technical trade-offs for different applications

---

### Module 9: Open Source Tools - GDAL/OGR
**Execute** command-line tools for spatial data conversion and transformation with complex parameter configurations
**Automate** data format transformations using GDAL utilities for batch processing and pipeline integration
**Process** large datasets efficiently through optimized command-line operations and memory management
**Integrate** GDAL tools into larger, automated GIS workflows using scripting and scheduling
**Troubleshoot** data format and projection issues using OGR diagnostic tools and validation techniques
**Script** complex data processing pipelines using GDAL/OGR commands with error handling and logging
**Optimize** spatial data processing workflows for performance and reliability in production environments

**Lectures:**
- GDAL/OGR Introduction: Command-Line Spatial Data Processing
- Data Format Conversion and Transformation: Advanced Techniques and Options
- Automation and Batch Processing: Scripting Strategies for Large Datasets
- GDAL Integration: Embedding Tools in Larger Workflows and Applications
- Performance Optimization: Memory Management and Processing Efficiency
- Quality Control: Validation, Error Handling, and Troubleshooting

**Readings:**
- GDAL/OGR comprehensive documentation and command reference
- Command-line GIS processing tutorials and advanced techniques
- Automation scripting best practices for geospatial data processing
- Integration patterns for GDAL in enterprise GIS workflows

**[Assignment] GDAL Data Processing** - Master data conversion, transformation, and validation using command-line tools
**[Assignment] Automated Processing Pipeline** - Design and implement automated workflows for recurring spatial data processing tasks
**[Discussion] Command-Line vs. GUI Tools** - Compare approaches for different use cases, scalability, and reproducibility

---

## Assessment Alignment

### Knowledge Level (Remember/Understand)
- **Identify** open source principles, licensing models, and community structures in the GIS ecosystem
- **Recognize** GIS software categories, architectural components, and technology integration patterns
- **Understand** containerization, web services, distributed development, and modern GIS deployment concepts
- **Recall** OGC standards, spatial data formats, and interoperability protocols for web-based GIS

### Comprehension Level (Understand/Apply)
- **Navigate** software interfaces and development environments across desktop, web, and command-line tools
- **Execute** operations in QGIS, Python, database systems, and web platforms with proper workflow understanding
- **Configure** servers, services, and development tools for integrated GIS workflows and deployment scenarios
- **Apply** spatial analysis techniques across multiple platforms and technology stacks

### Application Level (Apply/Analyze)
- **Implement** spatial analysis workflows across multiple integrated platforms with data format conversions
- **Create** solutions using coordinated open source tools in production-ready workflows
- **Troubleshoot** technical issues in complex, multi-component GIS environments with systematic approaches
- **Deploy** containerized applications and web services for consistent cross-platform execution

### Analysis Level (Analyze/Evaluate)
- **Compare** different approaches to GIS problem-solving and evaluate tool selection for specific contexts
- **Evaluate** architecture patterns and workflow designs for scalability, performance, and maintainability
- **Design** efficient workflows for spatial data processing that balance automation and flexibility
- **Assess** trade-offs between simple and enterprise solutions for different organizational needs

### Synthesis Level (Create/Evaluate)
- **Develop** custom web applications that integrate multiple GIS technologies in cohesive user experiences
- **Integrate** diverse open source technologies into production-ready, enterprise-scale solutions
- **Automate** complex spatial data processing workflows with robust error handling and optimization
- **Architect** complete GIS systems that leverage the full open source technology stack effectively