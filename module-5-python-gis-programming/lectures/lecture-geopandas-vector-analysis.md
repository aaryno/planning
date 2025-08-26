# Lecture: GeoPandas Vector Analysis

## Module: Open Source GIS Programming with Python
**Duration:** 50 minutes
**Format:** Interactive lecture with multimedia content

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **Apply** pandas DataFrame concepts to spatial data using GeoPandas GeoDataFrames
- **Perform** essential spatial operations including buffering, intersection, and containment
- **Execute** spatial joins to combine datasets based on geographic relationships
- **Implement** coordinate reference system transformations for accurate spatial analysis

---

## Lecture Outline

### I. Introduction and Context (10 minutes)
- Bridging pandas DataFrames to spatial GeoDataFrames
- Review of GeoPandas intro concepts
- Real-world spatial analysis scenarios in GIS workflows

### II. Core Concepts (25 minutes)
- **From DataFrames to GeoDataFrames**
  - Spatial extensions of pandas concepts
  - Geometry column and spatial indexing
  - Reading and writing spatial formats

- **Essential Spatial Operations**
  - Point-in-polygon analysis
  - Buffering and proximity analysis
  - Geometric calculations (area, distance, centroids)

- **Coordinate Reference Systems**
  - Understanding CRS importance
  - Reprojecting data for accurate analysis
  - Working with different coordinate systems

### III. Practical Applications (10 minutes)
- Spatial join demonstration with census and points of interest
- Multi-step analysis workflow
- Performance considerations for large datasets

### IV. Summary and Next Steps (5 minutes)
- Key spatial operations recap
- Connection to upcoming assignments
- Preparation for advanced analysis topics

---

## Key Concepts

### GeoDataFrame as Enhanced DataFrame

GeoPandas extends pandas DataFrames by adding a special geometry column that stores spatial information. Think of it as your familiar attribute table with superpowers:

```python
# Regular pandas DataFrame
import pandas as pd
df = pd.DataFrame({'name': ['Store A', 'Store B'], 'revenue': [50000, 75000]})

# GeoPandas GeoDataFrame - same data structure plus geometry
import geopandas as gpd
gdf = gpd.GeoDataFrame({
    'name': ['Store A', 'Store B'], 
    'revenue': [50000, 75000],
    'geometry': [Point(-110.9, 32.2), Point(-110.8, 32.3)]
})
```

**Key advantages over regular DataFrames:**
- All pandas operations still work (filtering, groupby, joins)
- Additional spatial methods (.buffer(), .intersects(), .within())
- Automatic spatial visualization with .plot()
- Spatial indexing for faster operations

### Essential Spatial Operations

**Geometric Predicates** - Boolean tests between geometries:
- `.intersects()` - Do geometries touch or overlap?
- `.within()` - Is geometry A completely inside geometry B?
- `.contains()` - Does geometry A completely contain geometry B?
- `.touches()` - Do geometries share a boundary but not interior?

**Geometric Operations** - Create new geometries:
- `.buffer(distance)` - Create area around geometry
- `.intersection()` - Find overlapping area
- `.union()` - Combine geometries
- `.difference()` - Subtract one geometry from another

**Measurements** - Calculate spatial properties:
- `.area` - Calculate polygon area
- `.length` - Calculate line length
- `.distance()` - Calculate distance between geometries
- `.centroid` - Find geometric center

### Coordinate Reference Systems (CRS)

**Why CRS Matters:**
- Earth is 3D sphere, maps are 2D flat surfaces
- Different projections preserve different properties (area, distance, shape)
- Mixing CRS leads to inaccurate measurements and analysis

**Common CRS for Different Purposes:**
- **Geographic (WGS84, EPSG:4326):** Good for storage, poor for measurements
- **Projected (UTM zones):** Accurate measurements in local areas
- **Web Mercator (EPSG:3857):** Web mapping standard

**Essential CRS Operations:**
```python
# Check current CRS
print(gdf.crs)

# Reproject to UTM for accurate area calculations
gdf_utm = gdf.to_crs('EPSG:32612')  # UTM Zone 12N for Arizona

# Always reproject to same CRS before spatial operations
gdf1_utm = gdf1.to_crs('EPSG:32612')
gdf2_utm = gdf2.to_crs('EPSG:32612')
result = gdf1_utm.intersects(gdf2_utm)
```

### Spatial Joins

Spatial joins combine datasets based on geometric relationships rather than shared attributes:

**Types of Spatial Joins:**
- **Intersects:** Join based on any spatial overlap
- **Within:** Join points to containing polygons
- **Contains:** Join polygons to contained points

**Practical Example - Finding Census Tract for Each School:**
```python
# Points (schools) joined to polygons (census tracts)
schools_with_tracts = gpd.sjoin(schools, census_tracts, how='left', predicate='within')
```

This is like a table join, but instead of matching on shared IDs, we match based on "which polygon contains each point."

---

## Interactive Elements

### Discussion Questions
1. **Data Quality:** You have GPS points from a mobile app (WGS84) and need to calculate distances in feet. What CRS considerations do you need to address?

2. **Analysis Design:** A city wants to find all parks within 1000 feet of schools. What sequence of spatial operations would you use?

3. **Performance:** When working with 100,000 points and 5,000 polygons for spatial join, what strategies might improve processing speed?

### Hands-on Activity

**Quick Spatial Analysis Demo:**
Using sample Arizona data, we'll demonstrate:
1. Loading county and city boundaries
2. Reprojecting for accurate measurements
3. Finding which cities fall within each county (spatial join)
4. Calculating total urban area per county
5. Creating a buffer analysis around major highways

---

## Resources

### Required Materials
- GeoPandas documentation: https://geopandas.org/docs/user_guide.html
- Coordinate Reference Systems primer: https://docs.qgis.org/latest/en/docs/gentle_gis_introduction/coordinate_reference_systems.html
- Sample Arizona spatial datasets (provided in Codespaces)

### Supplementary Resources
- **Book:** "Python for Geospatial Data Analysis" by Bonny P. McClain
- **Tutorial:** Real Python GeoPandas Tutorial: https://realpython.com/python-geopandas/
- **Reference:** Shapely geometry operations: https://shapely.readthedocs.io/en/stable/manual.html
- **CRS Explorer:** https://epsg.org/ for finding appropriate coordinate systems

---

## Preparation for Next Session

### Required Reading
- GeoPandas User Guide sections on "Managing Projections" and "Geometric Manipulations"
- Review pandas groupby and aggregation concepts (we'll use these with spatial groups)

### Recommended Preparation
- Ensure Codespaces environment has GeoPandas installed
- Download and explore sample datasets from AZ Open Data portal
- Practice basic pandas operations (filtering, groupby) as refresher

### Technical Setup
- Verify matplotlib and contextily packages for mapping
- Test basic GeoPandas operations in Jupyter notebook
- Confirm understanding of pandas DataFrame operations

---

## Notes for Instructors

### Technical Requirements
- [ ] Codespaces with GeoPandas, matplotlib, contextily installed
- [ ] Sample datasets: AZ counties, cities, schools, census tracts
- [ ] Backup simple geometries for demonstrations
- [ ] Internet access for basemap tiles (contextily)

### Common Issues
- **CRS Confusion:** Students often forget to reproject before measurements. Emphasize "same CRS for spatial operations" rule
- **Large Dataset Performance:** Introduce spatial indexing concepts if students work with large files
- **Geometry vs. Geography:** Students may confuse geometric operations (flat plane) with true geographic calculations
- **Memory Issues:** Large datasets in Codespaces may require chunking or sampling strategies

### Timing Adjustments
- **If Running Behind:** Focus on buffer and spatial join examples, defer advanced geometric operations
- **If Ahead:** Introduce overlay operations (intersection, union, difference) with practical examples
- **Interactive Extensions:** Let students suggest analysis scenarios using local Arizona data

### Assessment Integration
- Connect examples directly to upcoming assignment requirements
- Use problems that mirror real GIS analysis workflows students will encounter
- Emphasize documentation and reproducible analysis practices