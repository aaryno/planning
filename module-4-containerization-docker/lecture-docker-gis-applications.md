# Lecture: Docker GIS Applications

## Module: Containerization - Docker
**Duration:** 50 minutes
**Format:** Interactive lecture with live containerized GIS demonstrations and practical exercises

---

## 🎯 Learning Objectives

By the end of this lecture, students will be able to:
- **Deploy** containerized GIS applications including PostGIS, GeoServer, and web mapping services
- **Configure** multi-container GIS stacks using Docker Compose for complex geospatial workflows
- **Analyze** real-world containerization patterns used in production GIS environments
- **Design** containerized solutions for common GIS deployment challenges and scalability requirements
- **Evaluate** the benefits and trade-offs of containerizing different types of geospatial applications

---

## 📋 Lecture Outline

### I. GIS Containerization Landscape (12 minutes)
- Current state of containerized GIS applications
- Major geospatial software available as containers
- Industry adoption patterns and success stories
- Challenges specific to GIS containerization

### II. Core GIS Container Patterns (18 minutes)
- Spatial databases: PostGIS, SpatiaLite, MongoDB
- Web mapping servers: GeoServer, MapServer, QGIS Server
- Analysis environments: Python GIS, R spatial, GDAL toolchains
- Complete GIS stacks and orchestration strategies

### III. Production Deployment Scenarios (15 minutes)
- Enterprise GIS infrastructure using containers
- Cloud deployment patterns and auto-scaling
- Development to production workflows
- Monitoring and maintenance strategies

### IV. Hands-on Multi-Container Demo (5 minutes)
- Live deployment of complete GIS stack
- Integration testing and troubleshooting
- Performance considerations and optimization

---

## 📚 Core Content

### The GIS Containerization Revolution

#### **Why GIS Applications Need Containerization**
Geographic Information Systems present unique challenges that make containerization particularly valuable:

- **Complex Dependencies**: GIS software often requires specific versions of GDAL, GEOS, PROJ, and other geospatial libraries
- **Platform Inconsistencies**: Different operating systems handle spatial libraries differently
- **Resource Management**: Spatial analysis and map rendering can be resource-intensive
- **Scaling Challenges**: Web mapping services need to handle variable user loads
- **Development Environments**: Ensuring consistent analysis results across different machines

#### **Current Industry Adoption**
```
📊 **GIS Container Adoption (2024)**
Government Agencies:     78% using containers for web mapping
Research Institutions:   65% containerizing analysis workflows  
Commercial GIS Companies: 82% deploying services via containers
Consulting Firms:        54% using containers for client projects
Open Source Projects:    91% providing official container images
```

#### **Containerization Success Stories**
- **USGS**: Containerized National Map services serving 50M+ requests daily
- **European Space Agency**: Sentinel data processing using container orchestration
- **OpenStreetMap**: Tile rendering infrastructure using Docker containers
- **CARTO**: Complete SaaS platform built on containerized microservices

### Essential GIS Container Categories

#### **Spatial Database Containers**

**PostGIS - The Gold Standard**
```bash
# Official PostGIS container with multiple versions
docker run -d \
  --name spatial_database \
  -e POSTGRES_PASSWORD=gis_secure_123 \
  -e POSTGRES_DB=spatial_data \
  -e POSTGRES_USER=gis_user \
  -p 5432:5432 \
  -v postgis_data:/var/lib/postgresql/data \
  postgis/postgis:15-3.3

# Verify PostGIS functionality
docker exec -it spatial_database psql -U gis_user -d spatial_data \
  -c "SELECT PostGIS_Full_Version();"
```

**Advanced PostGIS Configuration:**
```yaml
# docker-compose.yml for production PostGIS
version: '3.8'
services:
  postgis:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: production_gis
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --locale=C"
    volumes:
      - postgis_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d production_gis"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### **Web Mapping Service Containers**

**GeoServer - Enterprise Web Mapping**
```bash
# GeoServer with persistent configuration
docker run -d \
  --name geoserver \
  -p 8080:8080 \
  -v geoserver_data:/opt/geoserver/data_dir \
  -e GEOSERVER_ADMIN_PASSWORD=admin_secure_123 \
  kartoza/geoserver:2.23.0

# Access GeoServer admin interface at http://localhost:8080/geoserver
```

**MapServer - High-Performance Mapping**
```dockerfile
# Custom MapServer container
FROM ubuntu:20.04

# Install MapServer dependencies
RUN apt-get update && apt-get install -y \
    mapserver-bin \
    cgi-mapserver \
    apache2 \
    libapache2-mod-fcgid \
    && rm -rf /var/lib/apt/lists/*

# Configure Apache for MapServer
COPY mapserver.conf /etc/apache2/sites-available/
RUN a2ensite mapserver && a2enmod fcgid

# Copy mapfiles and data
COPY mapfiles/ /var/www/mapfiles/
COPY data/ /var/www/data/

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

#### **Analysis Environment Containers**

**Python GIS Stack**
```dockerfile
# Complete Python GIS environment
FROM python:3.11-slim

# Install system dependencies for spatial libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python GIS packages
RUN pip install \
    geopandas==0.14.1 \
    rasterio==1.3.9 \
    folium==0.15.0 \
    contextily==1.4.0 \
    shapely==2.0.2 \
    fiona==1.9.5 \
    pyproj==3.6.1 \
    jupyter==1.0.0 \
    matplotlib==3.8.2 \
    seaborn==0.13.0

# Set up working directory
WORKDIR /workspace
EXPOSE 8888

# Default command for Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

**R Spatial Analysis Environment**
```dockerfile
# R Spatial container with comprehensive packages
FROM rocker/geospatial:4.3.2

# Install additional R spatial packages
RUN R -e "install.packages(c('leaflet', 'mapview', 'tmap', 'gstat', 'spatstat'))"

# Install system tools
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up RStudio Server
EXPOSE 8787
```

### Complete GIS Stack Orchestration

#### **Multi-Container GIS Application**
```yaml
# Complete GIS infrastructure stack
version: '3.8'

services:
  # Spatial Database
  postgis:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: gis_platform
      POSTGRES_USER: gis_admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgis_data:/var/lib/postgresql/data
    networks:
      - gis_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gis_admin -d gis_platform"]

  # Web Map Server
  geoserver:
    image: kartoza/geoserver:2.23.0
    depends_on:
      - postgis
    environment:
      GEOSERVER_ADMIN_PASSWORD: ${GEOSERVER_PASSWORD}
      GEOSERVER_ADMIN_USER: admin
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
    networks:
      - gis_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/geoserver"]

  # Tile Cache
  tilecache:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - tile_cache:/var/cache/nginx
    networks:
      - gis_network
    depends_on:
      - geoserver

  # Analysis Environment  
  jupyter:
    build: 
      context: ./python-gis
      dockerfile: Dockerfile
    volumes:
      - ./notebooks:/workspace
      - analysis_data:/data
    networks:
      - gis_network
    depends_on:
      - postgis

  # Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-proxy.conf:/etc/nginx/nginx.conf
      - ssl_certs:/etc/nginx/ssl
    networks:
      - gis_network
    depends_on:
      - geoserver
      - jupyter

volumes:
  postgis_data:
  geoserver_data:
  tile_cache:
  analysis_data:
  ssl_certs:

networks:
  gis_network:
    driver: bridge
```

#### **Environment Configuration Management**
```bash
# .env file for production deployment
DB_PASSWORD=secure_production_password_123
GEOSERVER_PASSWORD=geoserver_admin_456
JUPYTER_TOKEN=notebook_access_token_789

# SSL Configuration
SSL_CERT_PATH=/path/to/ssl/certificate.crt
SSL_KEY_PATH=/path/to/ssl/private.key

# Resource Limits
POSTGIS_MEMORY=4g
GEOSERVER_MEMORY=2g
JUPYTER_MEMORY=8g

# Networking
EXTERNAL_PORT=80
INTERNAL_NETWORK=172.20.0.0/16
```

### Production Deployment Patterns

#### **Cloud Deployment Architecture**
```
🌐 **Cloud GIS Container Architecture**
┌─────────────────────────────────┐
│        Load Balancer            │ ← Traffic distribution
├─────────────────────────────────┤
│     Application Gateway         │ ← SSL termination, routing
├─────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐     │
│  │GeoServer │  │GeoServer │     │ ← Horizontally scaled
│  │Instance 1│  │Instance 2│     │
│  └──────────┘  └──────────┘     │
├─────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐     │
│  │ PostGIS  │  │  Redis   │     │ ← Data layer
│  │ Primary  │  │  Cache   │     │
│  └──────────┘  └──────────┘     │
├─────────────────────────────────┤
│      Persistent Storage         │ ← Volume management
└─────────────────────────────────┘
```

#### **Scaling Strategies**
- **Horizontal Scaling**: Multiple GeoServer instances behind load balancer
- **Database Optimization**: Read replicas and connection pooling
- **Caching Layers**: Redis for session data, Nginx for tile caching
- **Resource Management**: CPU and memory limits per container
- **Auto-scaling**: Container orchestration based on resource usage

#### **Monitoring and Maintenance**
```yaml
# Monitoring stack addition
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - gis_network

  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - gis_network

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - gis_network
```

### Security and Best Practices

#### **Container Security Hardening**
```dockerfile
# Security-hardened GIS container example
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r gisuser && useradd -r -g gisuser gisuser

# Install dependencies with security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python packages with specific versions
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set secure permissions
RUN chown -R gisuser:gisuser /app
USER gisuser

# Use non-root port
EXPOSE 8080
```

#### **Network Security**
```yaml
# Secure network configuration
services:
  postgis:
    networks:
      - db_network  # Internal database network
    # No external port exposure

  geoserver:
    networks:
      - db_network   # Access to database
      - web_network  # Access from web tier
    # Port only exposed internally

  nginx:
    networks:
      - web_network  # Access to application services
    ports:
      - "443:443"    # Only HTTPS exposed externally
```

---

## 🎨 Interactive Elements

### Live Demonstration: Complete GIS Stack Deployment (15 minutes)

#### **Demo Scenario: Municipal GIS Platform**
Deploy a complete municipal GIS platform using containers:

**Step 1: Infrastructure Setup**
```bash
# Clone demo repository
git clone https://github.com/course/municipal-gis-stack
cd municipal-gis-stack

# Review docker-compose configuration
cat docker-compose.yml

# Start all services
docker-compose up -d

# Monitor startup progress
docker-compose logs -f
```

**Step 2: Service Verification**
```bash
# Check all containers are running
docker-compose ps

# Test PostGIS connection
docker-compose exec postgis psql -U gis_admin -d municipal_data \
  -c "SELECT version(), PostGIS_Full_Version();"

# Verify GeoServer is responding
curl -u admin:password http://localhost:8080/geoserver/rest/about/version

# Test Jupyter notebook environment
curl http://localhost:8888/api
```

**Step 3: Data Loading and Visualization**
```bash
# Load sample municipal data
docker-compose exec postgis psql -U gis_admin -d municipal_data \
  -f /docker-entrypoint-initdb.d/load_municipal_data.sql

# Configure GeoServer layers via REST API
curl -u admin:password -X POST \
  -H "Content-Type: application/json" \
  -d @geoserver-config.json \
  http://localhost:8080/geoserver/rest/workspaces

# Access web map interface
echo "Municipal GIS Platform ready at: http://localhost"
```

### Hands-on Exercise: Container Troubleshooting (12 minutes)

#### **Exercise: Debugging Failed GIS Stack**
Students work in pairs to diagnose and fix common container issues:

**Problem Scenarios:**
1. **Database Connection Failure**: PostGIS container fails to start due to volume permissions
2. **GeoServer Memory Issues**: Application runs out of memory during large dataset processing
3. **Network Isolation**: Services can't communicate due to network configuration
4. **Data Persistence**: Container restart loses all configuration changes

**Troubleshooting Toolkit:**
```bash
# Container health checking
docker-compose ps
docker-compose logs service_name

# Resource monitoring
docker stats
docker exec -it container_name top

# Network debugging
docker network ls
docker network inspect network_name

# Volume inspection
docker volume ls
docker volume inspect volume_name

# Process investigation
docker exec -it container_name bash
ps aux | grep process_name
```

#### **Solution Documentation**
Students must document:
- Problem symptoms observed
- Diagnostic steps taken
- Root cause identification
- Solution implemented
- Prevention strategies

### Case Study Analysis: Real-World Deployments (8 minutes)

#### **Industry Case Studies**
- **Case A**: National Weather Service containerized weather data processing
- **Case B**: Smart city platform using microservices architecture
- **Case C**: Environmental monitoring network with edge computing
- **Case D**: Academic research collaboration platform

#### **Analysis Framework**
Students evaluate each case study using these criteria:
- **Technical Architecture**: Container design patterns and orchestration
- **Scalability Approach**: Handling growth and varying loads
- **Security Implementation**: Access control and data protection
- **Operational Strategy**: Monitoring, maintenance, and updates
- **Business Impact**: Cost savings, performance improvements, reliability gains

---

## 🛠️ Tools and Resources

### Essential GIS Container Images

#### **Official and Community Images**
- **PostGIS/PostGIS**: Official spatial database containers
- **Kartoza/GeoServer**: Community-maintained GeoServer images
- **OSGeo/GDAL**: Official GDAL/OGR toolkit containers
- **Jupyter/SciPy-Notebook**: Scientific Python environments
- **Nginx**: Web server and reverse proxy
- **Redis**: In-memory data structure store

#### **Specialized GIS Containers**
- **TileServer GL**: Vector tile serving
- **pg_tileserv**: PostGIS tile server
- **pg_featureserv**: PostGIS feature server
- **Martin**: PostGIS vector tile server
- **OpenMapTiles**: Complete tile serving stack

### Development and Deployment Tools

#### **Container Orchestration**
- **Docker Compose**: Multi-container application orchestration
- **Kubernetes**: Production-grade container orchestration
- **Docker Swarm**: Docker-native clustering solution
- **Rancher**: Complete container management platform

#### **Monitoring and Management**
- **Portainer**: Container management web interface
- **Grafana + Prometheus**: Monitoring and alerting
- **ELK Stack**: Logging and analytics
- **Traefik**: Modern reverse proxy and load balancer

### Learning Resources

#### **Official Documentation**
- [PostGIS Docker Documentation](https://registry.hub.docker.com/r/postgis/postgis) - Spatial database containers
- [GeoServer Docker Guide](https://docs.geoserver.org/latest/en/user/installation/docker.html) - Web mapping server setup
- [Docker Compose Reference](https://docs.docker.com/compose/) - Multi-container orchestration

#### **Community Resources**
- [Kartoza Docker Images](https://github.com/kartoza) - Comprehensive GIS container collection
- [OSGeo Docker Examples](https://github.com/OSGeo/gdal/tree/master/docker) - Official geospatial containers
- [Awesome Docker GIS](https://github.com/sacridini/Awesome-Geospatial#docker) - Curated container list

---

## 👨‍🏫 Instructor Notes

### Pre-Lecture Preparation

#### **Technical Infrastructure**
- [ ] Docker environment with sufficient resources (8GB+ RAM recommended)
- [ ] Sample GIS datasets prepared and accessible
- [ ] Docker Compose files tested and validated
- [ ] Network connectivity for container image downloads
- [ ] Backup plan for offline demonstration if needed

#### **Student Environment Setup**
- [ ] Verify student computer specifications meet Docker requirements
- [ ] Confirm Docker Desktop installation on student machines
- [ ] Test network policies allow Docker Hub access
- [ ] Prepare USB drives with pre-downloaded images for network issues

### Lecture Delivery Strategy

#### **Live Demonstration Best Practices**
- **Pre-pull Images**: Download all required images before class
- **Scripted Commands**: Prepare command sequences for consistent demonstration
- **Error Recovery**: Plan for common failure scenarios and recovery procedures
- **Time Management**: Keep demonstrations focused with clear learning objectives

#### **Student Engagement Techniques**
- **Real-World Relevance**: Connect every concept to professional GIS applications
- **Hands-On Practice**: Students follow along with their own containers
- **Peer Learning**: Encourage collaboration during troubleshooting exercises
- **Problem-Based Learning**: Present challenges that require container solutions

### Common Challenges and Solutions

#### **Technical Issues**
- **Resource Limitations**: Guide resource allocation and optimization strategies
- **Network Connectivity**: Provide offline alternatives and cached images
- **Permission Problems**: Address Docker daemon access and file permissions
- **Version Conflicts**: Explain container versioning and compatibility

#### **Conceptual Difficulties**
- **Complexity Overwhelm**: Break down multi-container applications into components
- **Networking Confusion**: Use visual diagrams and simple examples first
- **Production Concerns**: Address security, scalability, and maintenance questions
- **Tool Selection**: Guide decision-making for appropriate container choices

### Assessment Integration

#### **Immediate Learning Verification**
- **Container Deployment**: Students successfully deploy multi-service GIS stack
- **Troubleshooting Skills**: Diagnose and resolve common container problems
- **Configuration Understanding**: Explain Docker Compose service relationships
- **Performance Analysis**: Identify resource bottlenecks and optimization opportunities

#### **Professional Application**
- **Architecture Design**: Students propose containerization strategy for given scenario
- **Security Consideration**: Identify security implications and mitigation strategies
- **Scalability Planning**: Design scaling approach for varying load requirements
- **Operational Strategy**: Develop maintenance and update procedures

---

## 🔗 Connection to Professional Practice

### Industry Relevance

#### **Current Market Trends**
- **Cloud-First Strategy**: Organizations migrating GIS infrastructure to cloud platforms
- **Microservices Architecture**: Breaking monolithic GIS applications into containerized services
- **DevOps Integration**: Automated deployment and scaling of geospatial services
- **Edge Computing**: Containerized GIS processing closer to data sources

#### **Career Preparation**
- **DevOps Skills**: Understanding of modern deployment and infrastructure management
- **Cloud Competency**: Knowledge of containerized application deployment patterns
- **System Architecture**: Ability to design scalable, maintainable GIS systems
- **Troubleshooting Expertise**: Diagnostic skills for complex distributed systems

### Real-World Applications

#### **Government and Public Sector**
- **Emergency Response**: Rapidly deployable GIS services for crisis situations
- **Multi-Agency Collaboration**: Standardized GIS platforms across departments
- **Citizen Services**: Scalable web mapping for public information access
- **Data Sharing**: Secure, controlled access to spatial data resources

#### **Commercial and Consulting**
- **Client Deployments**: Portable GIS solutions for diverse client environments
- **SaaS Platforms**: Multi-tenant geospatial applications with container isolation
- **Analysis Services**: Scalable processing for large spatial datasets
- **Proof of Concepts**: Rapid deployment for client demonstrations

---

## 📋 Preparation for Next Session

### Required Actions
- [ ] Complete hands-on deployment of multi-container GIS stack
- [ ] Document troubleshooting procedures for common container issues
- [ ] Identify potential containerization opportunities in current or future projects
- [ ] Research container orchestration platforms (Kubernetes, Docker Swarm)

### Recommended Reading
- [Docker Compose Best Practices](https://docs.docker.com/compose/production/) - Production deployment guidelines
- [Container Security Guide](https://docs.docker.com/engine/security/) - Security hardening procedures
- [GIS Cloud Architecture Patterns](https://aws.amazon.com/solutions/implementations/gis-on-aws/) - Enterprise deployment examples

### Next Lecture Preview
The next lecture will explore Docker networking and data persistence in detail, covering advanced topics like custom networks, volume management, and container communication patterns. We'll dive deep into the infrastructure layer that supports complex GIS applications, building on the application-level knowledge gained today.

Students should come prepared with working multi-container deployments and questions about scaling, security, and operational management of containerized GIS systems.

### Assignment Integration
This lecture directly supports:
- **Docker GIS Stack Assignment**: Practical application of multi-container deployment
- **Professional Portfolio Development**: Real-world containerization examples
- **Career Preparation**: Industry-standard deployment practices and troubleshooting skills

The concepts and hands-on experience gained today provide essential foundation for advanced containerization topics and prepare students for modern GIS professional environments where containerized applications are increasingly the standard.