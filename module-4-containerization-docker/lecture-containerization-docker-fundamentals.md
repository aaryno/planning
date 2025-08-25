# Lecture: Docker and Containerization Fundamentals

## Module: Containerization - Docker
**Duration:** 50 minutes
**Format:** Interactive lecture with live demonstrations and hands-on exercises

---

## 🎯 Learning Objectives

By the end of this lecture, students will be able to:
- **Explain** containerization concepts and how they differ from traditional virtualization
- **Identify** the key advantages of Docker for GIS application deployment and development
- **Execute** basic Docker commands for container lifecycle management
- **Analyze** Docker images and understand the layered architecture system
- **Design** simple Dockerfiles for containerizing GIS applications and workflows

---

## 📋 Lecture Outline

### I. Containerization Revolution in Software Development (12 minutes)
- Evolution from physical servers to containers
- Container vs. Virtual Machine architecture
- The "works on my machine" problem and its solution
- Container orchestration and microservices architecture

### II. Docker Architecture and Core Components (15 minutes)
- Docker Engine, Images, Containers, and Registries
- Image layering and Union File Systems
- Container lifecycle and resource isolation
- Docker Hub and container distribution

### III. Essential Docker Commands and Workflows (15 minutes)
- Image management: pull, build, push, list
- Container operations: run, stop, start, remove
- Data persistence and volume management
- Network configuration and port mapping

### IV. GIS Applications and Containerization Benefits (8 minutes)
- Reproducible geospatial analysis environments
- Simplified deployment of complex GIS stacks
- Scaling and load balancing for web mapping services
- Development environment standardization

---

## 📚 Core Content

### Understanding Containerization

#### **The Containerization Paradigm**
Containerization represents a fundamental shift in how we package, distribute, and run applications. Unlike traditional deployment methods, containers bundle an application with all its dependencies, libraries, and configuration files into a single, portable unit.

#### **Container vs. Virtual Machine Comparison**
```
🖥️ **Traditional Virtual Machines**
┌─────────────────────────────────┐
│          Application            │
├─────────────────────────────────┤
│            Guest OS             │
├─────────────────────────────────┤
│          Hypervisor             │
├─────────────────────────────────┤
│            Host OS              │
├─────────────────────────────────┤
│          Hardware               │
└─────────────────────────────────┘

📦 **Container Architecture**
┌─────────────────────────────────┐
│          Application            │
├─────────────────────────────────┤
│        Container Runtime        │
├─────────────────────────────────┤
│            Host OS              │
├─────────────────────────────────┤
│          Hardware               │
└─────────────────────────────────┘
```

#### **Key Advantages of Containerization**
- **Lightweight**: Containers share the host OS kernel, requiring fewer resources
- **Portable**: Run consistently across different environments (dev, test, production)
- **Scalable**: Easy to scale applications horizontally with container orchestration
- **Isolated**: Applications run in isolated environments preventing conflicts
- **Version Control**: Container images can be versioned and rolled back
- **Fast Startup**: Containers start in seconds compared to minutes for VMs

### Docker Architecture Deep Dive

#### **Core Docker Components**
- **Docker Engine**: The runtime that manages containers on the host system
- **Docker Images**: Read-only templates used to create containers
- **Docker Containers**: Running instances of Docker images
- **Docker Registry**: Service for storing and distributing Docker images
- **Dockerfile**: Text file containing instructions to build Docker images

#### **Image Layering System**
```
📊 **Docker Image Layers**
┌─────────────────────────────────┐
│      Application Layer          │ ← Your GIS application
├─────────────────────────────────┤
│      Dependencies Layer         │ ← GeoPandas, GDAL, etc.
├─────────────────────────────────┤
│      Python Runtime Layer       │ ← Python interpreter
├─────────────────────────────────┤
│      OS Libraries Layer         │ ← Ubuntu base libraries
├─────────────────────────────────┤
│      Base OS Layer             │ ← Ubuntu minimal
└─────────────────────────────────┘
```

#### **Container Lifecycle States**
- **Created**: Container exists but hasn't started
- **Running**: Container is executing
- **Paused**: Container processes are paused
- **Stopped**: Container has exited but still exists
- **Deleted**: Container and its file system are removed

### Essential Docker Commands

#### **Image Management Commands**
```bash
# Pull images from Docker Hub
docker pull ubuntu:20.04
docker pull postgis/postgis:13-3.2

# List local images
docker images
docker image ls

# Remove images
docker rmi ubuntu:20.04
docker image rm postgis/postgis:13-3.2

# Build image from Dockerfile
docker build -t my-gis-app:1.0 .

# Tag images for distribution
docker tag my-gis-app:1.0 myregistry/my-gis-app:latest
```

#### **Container Operations**
```bash
# Run containers
docker run hello-world                    # Simple test
docker run -it ubuntu:20.04 bash          # Interactive shell
docker run -d -p 8080:80 nginx            # Detached with port mapping

# Container lifecycle management
docker ps                                 # List running containers
docker ps -a                              # List all containers
docker stop container_name                # Stop container
docker start container_name               # Start stopped container
docker restart container_name             # Restart container
docker rm container_name                  # Remove container

# Execute commands in running containers
docker exec -it container_name bash       # Get interactive shell
docker exec container_name ls /app        # Execute single command
```

#### **Data Persistence and Volumes**
```bash
# Named volumes (Docker managed)
docker volume create gis_data
docker run -v gis_data:/data ubuntu:20.04

# Bind mounts (host directory)
docker run -v /host/path:/container/path ubuntu:20.04

# Temporary filesystems (RAM)
docker run --tmpfs /tmp ubuntu:20.04

# List and manage volumes
docker volume ls
docker volume inspect gis_data
docker volume rm gis_data
```

### GIS-Specific Docker Applications

#### **Geospatial Software Containerization Benefits**
- **Complex Dependencies**: GDAL, GEOS, PROJ libraries with specific versions
- **Environment Consistency**: Same analysis results across different machines
- **Deployment Simplification**: Ship entire GIS stack as single container
- **Development Isolation**: Test different software versions without conflicts

#### **Common GIS Container Use Cases**
```
🗺️ **GIS Container Applications**
├── Spatial Databases
│   ├── PostGIS containers for spatial data storage
│   ├── MongoDB with geospatial indexing
│   └── InfluxDB for time-series spatial data
├── Analysis Environments
│   ├── Python GIS stack (GeoPandas, Rasterio, GDAL)
│   ├── R spatial analysis (sf, sp, raster packages)
│   └── QGIS Server for headless processing
├── Web Mapping Services
│   ├── GeoServer for OGC web services
│   ├── MapServer for high-performance mapping
│   └── TileServer GL for vector tile serving
└── Processing Pipelines
    ├── GDAL/OGR for data transformation
    ├── FME Server for enterprise ETL
    └── Custom analysis workflows
```

#### **Real-World GIS Docker Examples**
- **Research Reproducibility**: Containerized analysis ensuring identical results
- **Web Mapping Deployment**: Containerized tile servers and map APIs
- **Government Systems**: Standardized GIS environments across agencies
- **Commercial Solutions**: SaaS GIS platforms using container orchestration

---

## 🎨 Interactive Elements

### Live Demonstration: Docker Basics (15 minutes)

#### **Demo 1: First Container Experience**
```bash
# Pull and run hello-world
docker run hello-world

# Interactive Ubuntu container
docker run -it ubuntu:20.04 bash
# Inside container:
apt update && apt install -y python3-pip
python3 --version
exit

# Show container persistence
docker ps -a
docker start container_name
docker exec -it container_name bash
```

#### **Demo 2: GIS Container Example**
```bash
# Run PostGIS container
docker run -d \
  --name gis_database \
  -e POSTGRES_PASSWORD=gis123 \
  -e POSTGRES_DB=spatial_data \
  -p 5432:5432 \
  postgis/postgis:13-3.2

# Verify PostGIS functionality
docker exec -it gis_database psql -U postgres -d spatial_data -c "SELECT PostGIS_Full_Version();"

# Python GIS environment
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  python:3.9 bash

# Inside container:
pip install geopandas matplotlib
python3 -c "import geopandas; print('GIS ready!')"
```

### Hands-on Activity: Container Exploration (10 minutes)

#### **Student Exercise: Container Lifecycle**
Students work in pairs to complete these tasks:

1. **Basic Operations:**
   - Pull an Ubuntu 20.04 image
   - Run interactive container and install Python
   - Exit and restart the same container
   - Verify Python is still installed

2. **Port Mapping Exercise:**
   - Run nginx container with port mapping
   - Access web server from browser
   - Modify default page using volume mount

3. **Data Persistence:**
   - Create named volume
   - Run container with volume attached
   - Create file in volume
   - Remove container and verify data persistence

#### **Exercise Checklist**
```
✅ **Container Mastery Checklist**
- [ ] Successfully pull and run first container
- [ ] Demonstrate interactive shell access
- [ ] Show container start/stop lifecycle
- [ ] Configure port mapping for web service
- [ ] Create and use named volume for data persistence
- [ ] List and inspect running containers
- [ ] Clean up containers and images
```

### Discussion Activity: GIS Use Cases (8 minutes)

#### **Small Group Discussions**
- **Group A**: How could Docker solve software installation challenges in GIS?
- **Group B**: What are the benefits for collaborative GIS research projects?
- **Group C**: How might government agencies use containers for GIS services?
- **Group D**: What challenges might arise when containerizing legacy GIS applications?

#### **Class Discussion Points**
1. **Reproducibility**: How containers ensure consistent analysis results
2. **Collaboration**: Sharing complete analysis environments with colleagues
3. **Deployment**: Simplifying complex GIS application deployment
4. **Development**: Isolating different project environments
5. **Scalability**: Handling varying computational loads

---

## 🛠️ Tools and Resources

### Essential Docker Tools

#### **Development Tools**
- **Docker Desktop**: GUI application for container management
- **Docker Compose**: Multi-container application orchestration
- **VS Code Docker Extension**: Container development integration
- **Portainer**: Web-based Docker management interface

#### **GIS-Specific Images**
- **OSGeo/GDAL**: Complete GDAL/OGR toolkit
- **PostGIS/PostGIS**: Spatial database with extensions
- **Jupyter/Scipy-Notebook**: Scientific Python environment
- **QGIS/QGIS**: Desktop GIS in container form

### Learning Resources

#### **Official Documentation**
- [Docker Documentation](https://docs.docker.com/) - Complete platform documentation
- [Docker Hub](https://hub.docker.com/) - Public container registry
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Optimization guidelines

#### **GIS Container Resources**
- [OSGeo Docker Images](https://github.com/OSGeo/gdal/tree/master/docker) - Official geospatial containers
- [Awesome Docker GIS](https://github.com/FrankBlue/awesome-docker-gis) - Curated GIS container list
- [Spatial-Docker](https://github.com/kartoza/docker-postgis) - PostGIS container examples

---

## 👨‍🏫 Instructor Notes

### Pre-Lecture Preparation

#### **Technical Setup**
- [ ] Docker Desktop installed and running on instructor machine
- [ ] Sample containers pre-pulled to avoid download delays
- [ ] Network connectivity verified for Docker Hub access
- [ ] Backup slides ready in case live demos fail

#### **Student Prerequisites Verification**
- [ ] Confirm student access to computers with Docker capability
- [ ] Verify administrative privileges for Docker installation
- [ ] Check network policies don't block Docker Hub access
- [ ] Prepare offline alternatives for network issues

### Lecture Delivery Strategy

#### **Timing Management**
- **Interactive Demos**: Keep each demo under 5 minutes with clear objectives
- **Student Exercises**: Circulate to provide individual assistance
- **Q&A Management**: Park complex questions for after-class discussion
- **Pace Adjustment**: Have optional advanced content ready for fast-moving groups

#### **Common Student Questions**
- **"How is this different from virtual machines?"** - Emphasize resource efficiency and startup speed
- **"Do I need to learn Linux to use Docker?"** - Basic commands helpful but not required initially
- **"What about Windows containers?"** - Focus on Linux containers for GIS applications
- **"How much does Docker cost?"** - Clarify Docker Desktop licensing for enterprise use

### Troubleshooting Common Issues

#### **Technical Problems**
- **Docker Installation Issues**: Provide alternative cloud-based Docker environments
- **Permission Problems**: Guide students through Docker group setup on Linux/Mac
- **Network Connectivity**: Have offline Docker images available on USB drives
- **Performance Issues**: Discuss resource allocation and system requirements

#### **Conceptual Challenges**
- **Abstract Concepts**: Use physical analogies (shipping containers, apartment buildings)
- **Command Line Intimidation**: Provide command cheat sheets and explain each step
- **Image vs Container Confusion**: Use consistent analogies (blueprint vs house)
- **Networking Complexity**: Start with simple port mapping, advance gradually

### Assessment Integration

#### **Immediate Assessment**
- **Command Execution**: Verify students can run basic Docker commands
- **Conceptual Understanding**: Quick quiz on containers vs VMs
- **Practical Application**: Students identify GIS use cases for containers
- **Troubleshooting**: Students diagnose and fix common container issues

#### **Connection to Assignments**
- **Codespace Assignment**: Understanding container foundation for devcontainers
- **GIS Stack Assignment**: Building complex multi-container applications
- **Professional Skills**: Container knowledge increasingly required in industry

---

## 🔗 Connection to Course Modules

### Foundation for Advanced Topics

#### **Module Integration**
- **Previous Knowledge**: GitHub Codespaces now makes sense as containerized environments
- **Current Module**: Foundation for Docker networking, orchestration, and GIS applications
- **Future Modules**: Python environments, database containers, web service deployment

#### **Professional Workflow Preparation**
- **Development Environments**: Standardized toolchains across teams
- **Deployment Strategies**: From development to production using containers
- **Collaboration**: Sharing complete analysis environments with reproducible results
- **Career Skills**: Container knowledge increasingly essential for GIS professionals

### Real-World Applications

#### **Industry Relevance**
- **Cloud Migration**: Understanding how organizations move to cloud platforms
- **DevOps Practices**: Integration with modern software development workflows
- **Microservices Architecture**: Breaking monolithic GIS applications into components
- **Scalability Solutions**: Handling varying computational and user loads

#### **Research Applications**
- **Reproducible Science**: Ensuring analysis results can be independently verified
- **Collaborative Research**: Sharing complete computational environments
- **Long-term Preservation**: Archiving analysis environments for future use
- **Cross-platform Compatibility**: Running same analysis on different operating systems

---

## 📋 Preparation for Next Session

### Required Actions
- [ ] Install Docker Desktop on personal computer (if not using lab computers)
- [ ] Create Docker Hub account for image sharing
- [ ] Complete basic Docker tutorial from official documentation
- [ ] Identify one GIS workflow that could benefit from containerization

### Recommended Reading
- [Docker Getting Started Guide](https://docs.docker.com/get-started/) - Official tutorial
- [Container vs VM Article](https://www.docker.com/resources/what-container) - Conceptual understanding
- [GIS Container Examples](https://github.com/kartoza) - Real-world implementations

### Next Lecture Preview
The next lecture will dive deep into Docker networking and data persistence, exploring how to build complex multi-container GIS applications. We'll cover Docker Compose for orchestrating services like PostGIS databases, GeoServer, and web applications, building on the fundamental concepts learned today.

Students should come prepared with Docker installed and basic command familiarity, ready to tackle more complex containerized GIS workflows and professional deployment scenarios.

### Assignment Integration
This lecture provides essential foundation knowledge for:
- **Codespace Assignment**: Understanding the container technology behind GitHub Codespaces
- **Docker GIS Stack Assignment**: Building multi-service geospatial applications
- **Professional Development**: Container skills increasingly required for GIS careers

The concepts learned today will be immediately applied in hands-on assignments, reinforcing theoretical knowledge through practical implementation of containerized GIS workflows.