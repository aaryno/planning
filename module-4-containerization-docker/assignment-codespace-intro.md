# Assignment: GitHub Codespaces and Development Containers

## Module: Containerization - Docker
**Points:** 25
**Due:** One week after assignment
**Type:** Hands-on Development Environment Setup and Configuration

---

## Assignment Overview

This assignment introduces GIS Masters students to GitHub Codespaces and development containers (devcontainers), providing hands-on experience with cloud-based development environments. You'll learn to configure, customize, and troubleshoot devcontainers while transitioning from PyCharm-style IDEs to VS Code. The assignment emphasizes practical skills including Unix command-line basics, devcontainer configuration, and debugging broken environments. By deliberately breaking and fixing configurations, you'll gain confidence in troubleshooting development environment issues that commonly occur in professional software development.

---

## Learning Objectives

By completing this assignment, you will be able to:
- **Navigate** VS Code interface efficiently, leveraging PyCharm knowledge for smooth IDE transition
- **Configure** devcontainer.json files to create reproducible development environments
- **Execute** basic Unix commands for file management, process monitoring, and system navigation
- **Troubleshoot** broken devcontainer configurations using logs and safe mode recovery
- **Customize** development environments with extensions, settings, and automated file opening
- **Document** development environment setup procedures for team collaboration

---

## Prerequisites

Before starting this assignment:
- [ ] Active GitHub account with Codespaces access
- [ ] Completed Module 1 GitHub assignments (repository management skills)
- [ ] Familiarity with PyCharm or similar IDE (IntelliJ, Eclipse, Visual Studio)
- [ ] Basic programming experience (any language)
- [ ] No prior Docker or containerization knowledge required

---

## Assignment Tasks

### Part 1: Codespace Creation and VS Code Familiarization (5 points)

**Create Your First Codespace:**

1. **Repository Setup:**
   - Fork the course codespace template repository: `gist-604b-codespace-template`
   - Create a new codespace from your forked repository
   - Wait for the automatic setup to complete (this may take 2-3 minutes)

2. **VS Code Interface Exploration:**
   Document VS Code equivalents for these PyCharm features:
   
   | PyCharm Feature | VS Code Equivalent | Location/Shortcut |
   |-----------------|-------------------|-------------------|
   | Project Explorer | Explorer Panel | Ctrl+Shift+E |
   | Terminal | Integrated Terminal | Ctrl+` (backtick) |
   | Run Configuration | Run/Debug Panel | Ctrl+Shift+D |
   | Find in Files | Search Panel | Ctrl+Shift+F |
   | Version Control | Source Control | Ctrl+Shift+G |

3. **Extension Management:**
   - Install Python extension (if not already installed)
   - Install GitLens extension for enhanced Git integration
   - Install Remote Development extension pack
   - Document how VS Code extensions compare to PyCharm plugins

**Deliverables:**
- `vs_code_transition_guide.md` - PyCharm to VS Code comparison table
- `screencap_first_codespace.png` - Screenshot of your first running codespace

### Part 2: Unix Command Line Fundamentals (5 points)

**Essential Unix Commands for GIS Development:**

Using the Codespace terminal, complete these exercises and document each command:

1. **File System Navigation:**
   ```bash
   # Basic navigation
   pwd                    # Print working directory
   ls -la                 # List all files with details
   cd /workspaces         # Change to workspaces directory
   cd ~                   # Change to home directory
   ```

2. **File and Directory Operations:**
   ```bash
   # Create directory structure for GIS project
   mkdir -p gis_project/{data,scripts,outputs,docs}
   
   # Create sample files
   touch gis_project/data/sample.csv
   echo "# GIS Analysis Scripts" > gis_project/scripts/README.md
   
   # View file contents
   cat gis_project/scripts/README.md
   head -n 5 /etc/passwd    # View first 5 lines of system file
   ```

3. **Process and System Monitoring:**
   ```bash
   # System information
   uname -a               # System information
   df -h                  # Disk space usage
   free -h                # Memory usage
   ps aux                 # Running processes
   top                    # Real-time process monitor (press 'q' to quit)
   ```

4. **File Permissions and Ownership:**
   ```bash
   # Create executable script
   echo '#!/bin/bash\necho "Hello GIS World!"' > hello_gis.sh
   chmod +x hello_gis.sh  # Make executable
   ./hello_gis.sh         # Run the script
   ls -l hello_gis.sh     # Check permissions
   ```

**Deliverables:**
- `unix_commands_log.md` - Document each command used with explanation of output
- `gis_project/` - Directory structure created during exercises

### Part 3: Devcontainer Configuration and Customization (8 points)

**Understanding and Modifying devcontainer.json:**

1. **Examine Current Configuration:**
   - Open `.devcontainer/devcontainer.json` in your codespace
   - Study the existing configuration structure
   - Document what each major section does (image, features, customizations, etc.)

2. **Add Python GIS Environment:**
   Modify `devcontainer.json` to include these enhancements:
   
   ```json
   {
     "name": "GIS Development Environment",
     "image": "mcr.microsoft.com/devcontainers/python:3.11",
     "features": {
       "ghcr.io/devcontainers/features/git:1": {},
       "ghcr.io/devcontainers/features/github-cli:1": {},
       "ghcr.io/devcontainers/features/docker-in-docker:2": {}
     },
     "customizations": {
       "vscode": {
         "extensions": [
           "ms-python.python",
           "ms-python.pylint",
           "ms-toolsai.jupyter",
           "ms-vscode.vscode-json",
           "eamodio.gitlens",
           "ms-vscode-remote.remote-containers"
         ],
         "settings": {
           "python.defaultInterpreterPath": "/usr/local/bin/python",
           "python.linting.enabled": true,
           "python.linting.pylintEnabled": true,
           "editor.formatOnSave": true,
           "files.autoSave": "onWindowChange"
         }
       }
     },
     "postCreateCommand": "pip install geopandas folium rasterio matplotlib jupyter",
     "portsAttributes": {
       "8000": {
         "label": "Development Server"
       },
       "8888": {
         "label": "Jupyter Notebook"
       }
     }
   }
   ```

3. **Add Automatic File Opening:**
   Configure devcontainer to automatically open specific files when the codespace starts:
   
   ```json
   {
     // ... existing configuration ...
     "customizations": {
       "vscode": {
         // ... existing extensions and settings ...
         "openFiles": [
           "README.md",
           "gis_project/scripts/README.md",
           "setup_instructions.md"
         ]
       }
     }
   }
   ```

4. **Test Configuration:**
   - Commit your changes to trigger codespace rebuild
   - Create new codespace or rebuild existing one
   - Verify all Python GIS packages install correctly
   - Test that specified files open automatically

**Deliverables:**
- `devcontainer_working.json` - Your successful devcontainer configuration
- `screencap_working_environment.png` - Screenshot showing successful build with auto-opened files

### Part 4: Deliberate Breaking and Safe Mode Recovery (7 points)

**Learning Through Controlled Failure:**

1. **Introduce Configuration Error:**
   Create a deliberately broken devcontainer configuration:
   
   ```json
   {
     "name": "Broken GIS Environment",
     "image": "nonexistent/invalid-image:broken",
     "features": {
       "invalid-feature": "bad-config"
     },
     "customizations": {
       "vscode": {
         "extensions": [
           "invalid.extension.name",
           "another-fake-extension"
         ],
         "settings": {
           "python.invalidSetting": "bad-value",
           "editor.formatOnSave": "not-a-boolean"
         }
       }
     },
     "postCreateCommand": "pip install nonexistent-package-xyz invalid-dependency",
     // Deliberate JSON syntax error - missing closing bracket
     "portsAttributes": {
       "8000": {
         "label": "Development Server"
   }
   ```

2. **Document the Breaking Process:**
   - Commit this broken configuration
   - Attempt to rebuild your codespace
   - Document what error messages appear
   - Take screenshots of the failure process

3. **Safe Mode Recovery:**
   - When codespace fails to build, it should automatically enter safe mode
   - Access the codespace in safe mode (limited functionality)
   - Navigate to the devcontainer logs to understand the failure
   - Use commands to examine logs:
     ```bash
     # View recent system logs
     sudo journalctl --no-pager -n 50
     
     # Check Docker container logs (if available)
     sudo docker logs $(sudo docker ps -aq) || echo "No containers found"
     
     # View build process logs
     cat ~/.vscode-server/data/logs/*/output*
     ```

4. **Fix and Recovery:**
   - Identify the specific errors from logs
   - Fix the JSON syntax errors and invalid configurations
   - Replace broken elements with working alternatives
   - Document your problem-solving process

**Deliverables:**
- `devcontainer_broken.json` - Your deliberately broken configuration
- `screencap_safe_mode.png` - Screenshot showing safe mode interface
- `error_analysis.md` - Documentation of errors encountered and how you diagnosed them
- `troubleshooting_log.md` - Step-by-step record of your problem-solving process

---

## Advanced Professional Features

### Environment Documentation
Create comprehensive documentation for your development environment:

```markdown
# GIS Development Environment Setup

## Overview
This devcontainer provides a complete Python GIS development environment with...

## Included Packages
- GeoPandas: Spatial data manipulation
- Folium: Interactive maps
- Rasterio: Raster data processing
- Matplotlib: Data visualization
- Jupyter: Interactive notebooks

## Getting Started
1. Open repository in GitHub Codespaces
2. Wait for automatic environment setup (2-3 minutes)
3. Verify installation: `python -c "import geopandas; print('GIS environment ready!')"`

## Troubleshooting
Common issues and solutions...
```

### Performance Optimization
Document codespace performance considerations:
- Resource usage monitoring
- Package installation optimization
- Storage management
- Network considerations for large datasets

---

## Evaluation Criteria

### Technical Implementation (60%)
- Successful creation and configuration of working codespace
- Correct modification of devcontainer.json with appropriate GIS packages
- Demonstration of Unix command proficiency
- Successful recovery from broken configuration using safe mode

### Problem-Solving and Troubleshooting (25%)
- Quality of error analysis and diagnostic process
- Effective use of logs and debugging tools
- Clear documentation of problem-solving methodology
- Understanding of failure modes and recovery strategies

### Documentation and Communication (15%)
- Clear, comprehensive documentation of all procedures
- Professional presentation of technical information
- Effective use of screenshots and visual documentation
- Practical guidance for future users and team members

---

## Real-World Applications

### Professional Development Environments
- **Consulting Teams**: Standardized environments across team members
- **Research Groups**: Reproducible analysis environments
- **Government Agencies**: Controlled, compliant development setups
- **Educational Institutions**: Consistent student learning environments

### Industry Best Practices
- **DevOps Integration**: Infrastructure as code principles
- **Collaborative Development**: Shared development standards
- **Quality Assurance**: Reproducible testing environments
- **Documentation Standards**: Environment setup and maintenance

---

## Resources

### Official Documentation
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces) - Complete platform documentation
- [Development Containers Specification](https://containers.dev/) - Devcontainer standards and examples
- [VS Code in Codespaces](https://code.visualstudio.com/docs/remote/codespaces) - Editor-specific features
- [Devcontainer Features](https://github.com/devcontainers/features) - Pre-built environment components

### Unix/Linux Command References
- [Unix Command Cheat Sheet](https://www.guru99.com/linux-commands-cheat-sheet.html) - Essential commands
- [Linux File System Hierarchy](https://www.geeksforgeeks.org/linux-file-hierarchy-structure/) - Directory structure
- [File Permissions Guide](https://www.redhat.com/sysadmin/linux-file-permissions-explained) - Permission management

### VS Code Transition Resources
- [VS Code Tips for PyCharm Users](https://code.visualstudio.com/docs/python/editing) - Feature comparisons
- [Keyboard Shortcuts](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf) - Productivity shortcuts
- [Extension Marketplace](https://marketplace.visualstudio.com/vscode) - Available extensions

### Python GIS Stack Documentation
- [GeoPandas User Guide](https://geopandas.org/en/stable/getting_started.html) - Spatial data manipulation
- [Rasterio Documentation](https://rasterio.readthedocs.io/) - Raster processing
- [Folium Documentation](https://python-visualization.github.io/folium/) - Interactive mapping

---

## Submission Instructions

### Repository Organization
Submit via GitHub repository branch named `codespace-intro-assignment`:

```
/assignment-deliverables
├── documentation/
│   ├── vs_code_transition_guide.md
│   ├── unix_commands_log.md
│   ├── error_analysis.md
│   └── troubleshooting_log.md
├── configurations/
│   ├── devcontainer_working.json
│   ├── devcontainer_broken.json
│   └── environment_documentation.md
├── screenshots/
│   ├── screencap_first_codespace.png
│   ├── screencap_working_environment.png
│   └── screencap_safe_mode.png
└── project-files/
    └── gis_project/
        ├── data/
        ├── scripts/
        ├── outputs/
        └── docs/
```

### Quality Standards
- **Documentation**: Professional formatting with clear explanations
- **Screenshots**: High resolution, clearly showing relevant interfaces
- **Code**: Proper JSON formatting and syntax validation
- **Organization**: Logical file structure with descriptive naming

### Submission Checklist
- [ ] All required files present and properly named
- [ ] Working devcontainer configuration tested and validated
- [ ] Broken configuration deliberately created and documented
- [ ] Safe mode recovery process documented with screenshots
- [ ] Unix command exercises completed with explanations
- [ ] VS Code transition guide comprehensive and practical

---

## Getting Help

### Technical Support
- **Codespaces Issues**: GitHub Support for platform-specific problems
- **VS Code Help**: Built-in help system (Ctrl+Shift+P → "Help")
- **Unix Commands**: Manual pages (`man command_name`) within codespace
- **Python GIS Packages**: Package-specific documentation and Stack Overflow

### Troubleshooting Common Issues
- **Codespace Won't Start**: Check repository permissions and GitHub status
- **Build Failures**: Review devcontainer.json syntax and package availability
- **Performance Issues**: Monitor resource usage and optimize configuration
- **Extension Problems**: Check compatibility and installation logs

### Course Support
- **Office Hours**: Scheduled time for individual troubleshooting assistance
- **Discussion Forum**: Peer collaboration and problem-sharing
- **Email Support**: aaryn@email.arizona.edu for technical issues
- **Assignment Clarification**: GitHub Issues for assignment-specific questions

---

## Extension Opportunities (Optional)

### Advanced Configuration (+5 points)
Create sophisticated devcontainer with multiple services:
- PostgreSQL/PostGIS database integration
- Jupyter Lab server with custom extensions
- Automated data download and preprocessing
- Custom shell configuration and aliases

### Team Environment Template (+8 points)
Design devcontainer template for team collaboration:
- Standardized toolchain for GIS development team
- Automated code quality checks and formatting
- Pre-configured Git hooks and commit templates
- Documentation for onboarding new team members

### Performance Benchmarking (+6 points)
Compare development environment performance:
- Local development vs. Codespaces performance
- Different devcontainer base images and configurations
- Package installation time optimization
- Resource usage analysis and recommendations

### Integration with GIS Workflows (+10 points)
Demonstrate integration with professional GIS workflows:
- Automated spatial data processing pipeline
- Connection to external GIS services and APIs
- Integration with ArcGIS Online or QGIS Cloud
- Reproducible geospatial analysis environment for research

---

## Professional Development Notes

### Career Relevance
- **Cloud Development**: Industry trend toward cloud-based development environments
- **DevOps Skills**: Understanding of containerization and environment management
- **Team Collaboration**: Standardized development environments for team efficiency
- **Problem-Solving**: Diagnostic and troubleshooting skills valuable in any technical role

### Industry Applications
- **Remote Teams**: Consistent environments across distributed teams
- **Client Projects**: Reproducible analysis environments for consulting work
- **Research Collaboration**: Shared computational environments for academic projects
- **Training and Education**: Standardized learning environments for skill development

This assignment provides practical experience with modern development practices while building confidence in cloud-based development environments essential for contemporary GIS professional work.