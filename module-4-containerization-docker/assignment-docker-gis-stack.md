# Assignment: Docker GIS Stack

## Module: Containerization - Docker
**Points:** 10
**Due:** One week after assignment
**Type:** Hands-on Implementation and Integration

---

## Assignment Overview

This assignment teaches you to create and manage a complete containerized GIS stack using Docker. You'll deploy PostgreSQL/PostGIS, QGIS Server, and a web frontend as interconnected services, demonstrating how containerization enables consistent, scalable GIS deployments across different environments.

---

## Learning Objectives

By completing this assignment, you will be able to:
- **Create** multi-container Docker applications using docker-compose
- **Deploy** a complete GIS stack with database, server, and web components
- **Configure** service networking and data persistence in containerized environments
- **Manage** container orchestration, scaling, and resource allocation
- **Troubleshoot** common containerization issues in GIS deployments
- **Implement** best practices for container security and data management

---

## Prerequisites

Before starting this assignment:
- [ ] Complete Codespace Intro assignment from this module
- [ ] Have Docker Desktop installed and running
- [ ] Basic understanding of QGIS and PostGIS from previous modules
- [ ] Access to terminal/command line interface
- [ ] Sample spatial data for testing (shapefiles or GeoJSON)

---

## Assignment Tasks

### Part 1: Database Container Setup (25 points)

1. **PostgreSQL/PostGIS Container (15 points)**
   - Create docker-compose.yml with PostgreSQL/PostGIS service
   - Configure persistent data volumes for database storage
   - Set up environment variables for database credentials
   - Enable PostGIS extensions and configure spatial reference systems
   - Test connection and verify PostGIS functionality

2. **Data Loading and Configuration (10 points)**
   - Load sample spatial data into PostGIS using container tools
   - Create spatial indexes for optimal query performance
   - Set up database users with appropriate permissions
   - Configure connection pooling and performance settings
   - Document database schema and data structure

### Part 2: QGIS Server Container (30 points)

1. **QGIS Server Deployment (20 points)**
   - Add QGIS Server service to docker-compose configuration
   - Configure FastCGI or Apache integration for web serving
   - Mount QGIS project files and data directories
   - Set up environment variables for server configuration
   - Test WMS and WFS service endpoints

2. **Service Integration and Configuration (10 points)**
   - Connect QGIS Server to PostGIS database container
   - Configure QGIS projects to use containerized database
   - Set up layer styling and symbology for web services
   - Implement service metadata and capabilities documents
   - Test service integration and data access

### Part 3: Web Frontend and Orchestration (25 points)

1. **Web Application Container (15 points)**
   - Deploy lightweight web server (nginx or Apache)
   - Create simple web map consuming QGIS Server services
   - Configure reverse proxy for service access
   - Implement basic authentication and security measures
   - Test complete web mapping functionality

2. **Container Orchestration (10 points)**
   - Configure service dependencies and startup order
   - Implement health checks and restart policies
   - Set up container networking and port management
   - Configure resource limits and scaling options
   - Document deployment and maintenance procedures

### Part 4: Performance and Production Readiness (20 points)

1. **Performance Optimization (10 points)**
   - Monitor container resource usage and performance
   - Implement caching strategies for improved response times
   - Optimize database queries and spatial indexes
   - Configure connection pooling and concurrent request handling
   - Benchmark service performance under load

2. **Production Deployment Considerations (10 points)**
   - Implement proper logging and monitoring
   - Set up backup and recovery procedures
   - Configure SSL/TLS certificates for secure connections
   - Document scaling and maintenance procedures
   - Create deployment guide for different environments

---

## Deliverables

### Docker Configuration
Your submission must include:

1. **docker-compose.yml**
   - Complete multi-service configuration
   - Proper service dependencies and networking
   - Environment variable configuration
   - Volume mounts and data persistence
   - Resource limits and scaling options

2. **Configuration Files**
   - QGIS project files (.qgs/.qgz) configured for containers
   - Web server configuration (nginx.conf or Apache config)
   - Database initialization scripts
   - Environment files for different deployment scenarios

3. **Sample Data and Documentation**
   - Sample spatial datasets for testing
   - Database schema documentation
   - Service endpoint documentation
   - Troubleshooting guide

### Technical Report
Submit a comprehensive report (4-6 pages) containing:

1. **Architecture Overview**
   - System diagram showing container relationships
   - Network configuration and port mappings
   - Data flow between services
   - Security considerations and implementations

2. **Implementation Details**
   - Step-by-step deployment instructions
   - Configuration decisions and rationale
   - Performance optimization strategies
   - Testing procedures and results

3. **Production Readiness Analysis**
   - Scalability considerations and recommendations
   - Monitoring and maintenance procedures
   - Backup and disaster recovery planning
   - Security audit and recommendations

4. **Lessons Learned**
   - Challenges encountered and solutions
   - Comparison with non-containerized deployment
   - Benefits and limitations of containerized approach
   - Future improvements and enhancements

---

## Evaluation Criteria

### Technical Implementation (50%)
- **Docker Configuration**: Correct docker-compose setup with all services
- **Service Integration**: Proper networking and data flow between containers
- **Data Persistence**: Correct volume configuration and data management
- **Performance Optimization**: Effective resource usage and caching strategies
- **Security Implementation**: Proper authentication and secure configurations

### System Architecture and Design (30%)
- **Container Orchestration**: Appropriate service dependencies and startup order
- **Scalability Design**: Resource limits and scaling considerations
- **Network Architecture**: Efficient service communication and port management
- **Production Readiness**: Logging, monitoring, and maintenance procedures
- **Documentation Quality**: Clear deployment and troubleshooting guides

### Problem Solving and Analysis (20%)
- **Troubleshooting Skills**: Effective problem identification and resolution
- **Performance Analysis**: Meaningful benchmarking and optimization
- **Critical Thinking**: Thoughtful analysis of containerization trade-offs
- **Innovation**: Creative solutions and improvements beyond basic requirements

---

## Resources

### Docker Documentation
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Networking Guide](https://docs.docker.com/network/)
- [Docker Volume Management](https://docs.docker.com/storage/volumes/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### GIS Container Images
- [PostGIS Official Image](https://hub.docker.com/r/postgis/postgis)
- [QGIS Server Images](https://hub.docker.com/u/qgis)
- [OpenMapTiles](https://openmaptiles.org/docs/generate/docker/)

### Sample Data and Projects
- [Natural Earth Data](https://www.naturalearthdata.com/)
- [QGIS Sample Projects](https://github.com/qgis/QGIS-Sample-Data)
- [PostGIS Tutorial Data](https://postgis.net/docs/postgis_installation.html#sample_data)

### Performance and Monitoring
- [Docker Stats and Monitoring](https://docs.docker.com/config/containers/runmetrics/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [QGIS Server Performance](https://docs.qgis.org/latest/en/docs/server_manual/getting_started.html#performance-tuning)

---

## Submission Instructions

1. **Docker Configuration Files**
   - Create zip file: `LastName_FirstName_DockerGIS.zip`
   - Include docker-compose.yml and all configuration files
   - Include sample data and QGIS project files
   - Include README.md with deployment instructions

2. **Technical Report**
   - File name: `LastName_FirstName_DockerGIS_Report.pdf`
   - Include all required sections and diagrams
   - Embed screenshots of working services
   - Document performance benchmarks and analysis

3. **Submission Method**: Upload both files to D2L assignment dropbox
4. **Due Date**: [Insert specific due date]
5. **Testing**: Ensure your configuration works on a clean Docker environment

---

## Integration with Course

This assignment builds on:
- **Module 3**: QGIS project creation and configuration
- **Module 6**: PostGIS database management and spatial data
- **Previous assignment**: GitHub Codespaces and container basics

This assignment prepares you for:
- **Module 7**: Web service deployment and OGC standards
- **Module 8**: Web application development and integration
- **Professional Practice**: Production GIS system deployment

---

## Getting Help

### Support Resources
- **Office Hours**: Schedule appointment for Docker troubleshooting
- **Email**: aaryn@email.arizona.edu for technical questions
- **GitHub Discussions**: Post configuration issues and solutions
- **Docker Community**: [Docker Community Forums](https://forums.docker.com/)

### Common Issues and Solutions
- **Port Conflicts**: Use `docker ps` to check occupied ports
- **Volume Permissions**: Ensure proper file ownership and permissions
- **Service Dependencies**: Check container logs with `docker-compose logs`
- **Network Issues**: Use `docker network ls` and inspect network configuration
- **Performance Problems**: Monitor with `docker stats` and optimize resource allocation

### Best Practices Reminders
- Always use version tags for production images
- Implement proper secret management for credentials
- Test deployment on clean environment before submission
- Document all custom configuration decisions
- Implement graceful shutdown procedures for all services

This assignment represents real-world GIS infrastructure deployment practices. The skills you develop here are directly applicable to enterprise GIS environments and cloud deployments!
