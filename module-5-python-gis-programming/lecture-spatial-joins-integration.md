# Lecture: Spatial Joins and Integration

## Module: Open Source GIS Programming with Python
**Duration:** 50 minutes
**Format:** Interactive lecture with multimedia content

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **Apply** pandas join concepts to spatial relationships using GeoPandas spatial joins
- **Select** appropriate spatial predicates for different analysis scenarios
- **Design** multi-step spatial analysis workflows combining joins with other operations
- **Optimize** spatial join performance for large datasets

---

## Lecture Outline

### I. Introduction and Context (10 minutes)
- From attribute joins to spatial joins: extending pandas concepts
- Real-world scenarios requiring spatial data integration
- Performance considerations in spatial analysis workflows

### II. Core Concepts (25 minutes)
- **Spatial Joins vs. Attribute Joins**
  - Pandas merge() vs. GeoPandas sjoin()
  - Join types and spatial predicates
  - Handling one-to-many spatial relationships

- **Spatial Predicates in Practice**
  - Intersects, within, contains, touches
  - Choosing the right predicate for analysis goals
  - Dealing with edge cases and precision issues

- **Complex Analysis Workflows**
  - Chaining spatial operations
  - Combining spatial joins with groupby operations
  - Multi-dataset integration strategies

### III. Practical Applications (10 minutes)
- Urban planning case study: schools, census tracts, and service areas
- Environmental analysis: pollution monitoring and demographic impacts
- Performance optimization techniques

### IV. Summary and Next Steps (5 minutes)
- Spatial join patterns and best practices
- Connection to upcoming assignments
- Preparation for raster-vector integration

---

## Key Concepts

### From Attribute Joins to Spatial Joins

**Pandas Attribute Joins (Review):**
```python
# Traditional table join based on shared attributes
import pandas as pd

# Join customer data with order data on customer_id
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Carol'],
    'city': ['Phoenix', 'Tucson', 'Flagstaff']
})

orders = pd.DataFrame({
    'customer_id': [1, 1, 2, 3],
    'product': ['Laptop', 'Mouse', 'Tablet', 'Phone'],
    'amount': [1200, 25, 800, 600]
})

# Merge on shared attribute
result = customers.merge(orders, on='customer_id', how='left')
```

**GeoPandas Spatial Joins:**
```python
# Spatial join based on geometric relationships
import geopandas as gpd

# Join schools to census tracts based on location
schools = gpd.read_file('schools.shp')
census_tracts = gpd.read_file('census_tracts.shp')

# Spatial join: which census tract contains each school?
schools_with_demographics = gpd.sjoin(
    schools, census_tracts, 
    how='left', predicate='within'
)
```

**Key Differences:**
- **Attribute join**: Match on shared ID values
- **Spatial join**: Match on geometric relationships
- **Attribute join**: Exact matches only
- **Spatial join**: Fuzzy spatial relationships (tolerance, precision)
- **Attribute join**: Usually one-to-one or many-to-one
- **Spatial join**: Can be one-to-many (point intersects multiple polygons)

### Spatial Join Types and Predicates

**Join Types (same as pandas):**
- **Left join**: Keep all records from left dataset, match from right
- **Inner join**: Keep only records that have spatial matches
- **Right join**: Keep all records from right dataset, match from left

**Spatial Predicates:**
```python
# Different ways geometries can relate spatially
gpd.sjoin(points, polygons, predicate='within')      # Point inside polygon
gpd.sjoin(polygons1, polygons2, predicate='intersects')  # Any overlap
gpd.sjoin(polygons1, polygons2, predicate='contains')    # Polygon A contains polygon B
gpd.sjoin(lines, polygons, predicate='touches')      # Share boundary but no interior overlap
```

**Choosing the Right Predicate:**
- **within**: Finding which administrative unit contains each business
- **intersects**: Finding all parcels that overlap with flood zones
- **contains**: Finding all counties that completely contain protected areas
- **touches**: Finding adjacent properties or neighboring jurisdictions

### Handling One-to-Many Relationships

**The Challenge**: Spatial joins often create multiple matches per feature.

```python
# Example: Points near polygon boundaries might intersect multiple polygons
hospitals = gpd.read_file('hospitals.shp')
zip_codes = gpd.read_file('zip_codes.shp')

# This might create duplicate hospital records if hospital is near zip code boundary
hospitals_with_zips = gpd.sjoin(hospitals, zip_codes, predicate='intersects')

print(f"Original hospitals: {len(hospitals)}")
print(f"After spatial join: {len(hospitals_with_zips)}")
# Output might show more records after join due to multiple matches
```

**Solutions:**
```python
# Strategy 1: Use more restrictive predicate
hospitals_with_zips = gpd.sjoin(hospitals, zip_codes, predicate='within')

# Strategy 2: Keep only first match using drop_duplicates
hospitals_unique = hospitals_with_zips.drop_duplicates(subset=['hospital_id'])

# Strategy 3: Choose best match based on criteria
def find_best_zip_match(group):
    # Return the zip code with largest overlap area
    return group.loc[group['overlap_area'].idxmax()]

best_matches = hospitals_with_zips.groupby('hospital_id').apply(find_best_zip_match)
```

### Complex Multi-Step Analysis Workflows

**Real-World Example: School District Resource Allocation**

```python
# Step 1: Spatial join schools to census tracts
schools_demographics = gpd.sjoin(schools, census_tracts, predicate='within')

# Step 2: Calculate summary statistics by school district
district_stats = schools_demographics.groupby('district_id').agg({
    'total_population': 'sum',
    'median_income': 'mean',
    'percent_poverty': 'mean',
    'enrollment': 'sum'
}).reset_index()

# Step 3: Spatial join to find schools within 1 mile of highways
highway_buffer = highways.buffer(1609)  # 1 mile buffer in meters
schools_near_highways = gpd.sjoin(schools, highway_buffer, predicate='within')

# Step 4: Combine results for comprehensive analysis
final_analysis = district_stats.merge(
    schools_near_highways.groupby('district_id').size().reset_index(name='schools_near_highways'),
    on='district_id', how='left'
).fillna(0)
```

### Performance Optimization Strategies

**Spatial Indexing:**
```python
# GeoPandas automatically creates spatial index for sjoin operations
# But you can optimize further for repeated operations
schools_sindex = schools.sindex
census_tracts_sindex = census_tracts.sindex

# For large datasets, consider using explicit spatial indexing
from shapely.strtree import STRtree
```

**Data Preprocessing:**
```python
# 1. Ensure same CRS before spatial join
schools = schools.to_crs('EPSG:32612')  # UTM Zone 12N
census_tracts = census_tracts.to_crs('EPSG:32612')

# 2. Filter data to area of interest first
aoi_bounds = study_area.total_bounds
schools_filtered = schools.cx[aoi_bounds[0]:aoi_bounds[2], 
                            aoi_bounds[1]:aoi_bounds[3]]

# 3. Use appropriate predicate - 'intersects' is faster than 'within'
# but less precise
```

**Memory Management:**
```python
# For very large datasets, process in chunks
def chunked_spatial_join(left_gdf, right_gdf, chunk_size=1000):
    results = []
    for i in range(0, len(left_gdf), chunk_size):
        chunk = left_gdf.iloc[i:i+chunk_size]
        chunk_result = gpd.sjoin(chunk, right_gdf, predicate='within')
        results.append(chunk_result)
    return pd.concat(results, ignore_index=True)
```

### Integration with Other GeoPandas Operations

**Spatial Joins + Buffers:**
```python
# Find all businesses within 500m of bus stops
bus_stops_buffer = bus_stops.buffer(500)
businesses_near_transit = gpd.sjoin(businesses, bus_stops_buffer, predicate='within')
```

**Spatial Joins + Overlay Operations:**
```python
# Find the portion of each census tract within flood zones
flood_zone_intersect = gpd.overlay(census_tracts, flood_zones, how='intersection')

# Then calculate affected population
flood_zone_intersect['affected_population'] = (
    flood_zone_intersect['population'] * 
    flood_zone_intersect.geometry.area / flood_zone_intersect['total_tract_area']
)
```

**Spatial Joins + Aggregation:**
```python
# Calculate total retail space per neighborhood
stores_with_neighborhoods = gpd.sjoin(retail_stores, neighborhoods, predicate='within')

neighborhood_retail = stores_with_neighborhoods.groupby('neighborhood_id').agg({
    'store_sqft': 'sum',
    'employees': 'sum',
    'annual_revenue': 'sum'
})
```

---

## Interactive Elements

### Discussion Questions

1. **Data Relationships**: You have a dataset of crime incidents (points) and police patrol zones (polygons). A crime occurs exactly on the boundary between two zones. Which spatial predicate would you use and how would you handle the ambiguity?

2. **Performance Planning**: You need to analyze the relationship between 50,000 building footprints and 10,000 parcels. What strategies would you use to optimize this spatial join?

3. **Analysis Design**: A city wants to identify underserved areas for public health services. You have clinics (points), census blocks (polygons), and population data. Design a multi-step analysis workflow.

### Hands-on Activity

**Urban Analysis Demonstration:**
Using Arizona urban data, we'll demonstrate:
1. Joining demographic data from census tracts to school locations
2. Finding parks within walking distance of residential areas
3. Calculating service coverage statistics by neighborhood
4. Handling edge cases and performance optimization
5. Creating summary reports combining multiple spatial relationships

---

## Resources

### Required Materials
- GeoPandas spatial joins documentation: https://geopandas.org/docs/user_guide/mergingdata.html
- Sample Arizona datasets: schools, census tracts, city boundaries
- Review of pandas merge operations: https://pandas.pydata.org/docs/user_guide/merging.html

### Supplementary Resources
- **Performance Guide**: GeoPandas performance tips: https://geopandas.org/docs/user_guide/indexing.html
- **Spatial Predicates Reference**: Shapely predicates documentation: https://shapely.readthedocs.io/en/stable/manual.html#predicates
- **Case Studies**: Urban analysis workflows with spatial joins
- **Best Practices**: Handling precision and edge cases in spatial joins

---

## Preparation for Next Session

### Required Reading
- GeoPandas documentation on merging and joining spatial data
- Review pandas groupby and aggregation methods
- Study spatial predicate definitions and use cases

### Recommended Preparation
- Practice pandas merge operations with sample non-spatial data
- Explore Arizona census and administrative boundary datasets
- Test basic spatial join operations in Jupyter notebook

### Technical Setup
- Verify GeoPandas and pandas packages are current
- Download sample datasets for hands-on practice
- Test spatial join operations with small datasets first

---

## Notes for Instructors

### Technical Requirements
- [ ] Codespaces with GeoPandas, pandas, matplotlib installed
- [ ] Sample datasets: Arizona schools, census tracts, city boundaries, business locations
- [ ] Datasets with known spatial relationships for clear examples
- [ ] Backup simple geometries for demonstrations

### Common Issues
- **Performance Problems**: Students may attempt spatial joins on large datasets without optimization
- **Duplicate Records**: Many-to-one spatial relationships create confusion - emphasize this early
- **CRS Mismatches**: Spatial joins require same coordinate system - check this first
- **Predicate Confusion**: Students mix up 'within' vs 'contains' - use clear visual examples
- **Edge Cases**: Points exactly on boundaries may behave unexpectedly

### Timing Adjustments
- **If Running Behind**: Focus on basic spatial join concepts and one practical example
- **If Ahead**: Introduce overlay operations and more complex multi-dataset workflows
- **Interactive Extensions**: Let students design analysis scenarios using local data

### Assessment Integration
- Connect examples to upcoming GeoPandas join assignment
- Emphasize problem-solving approach: "How would you answer this question spatially?"
- Use examples that mirror real planning and analysis challenges

### Progression Notes
- **From Previous**: Build on pandas joins and basic GeoPandas operations
- **To Next**: Prepare foundation for raster-vector integration and complex analysis
- **Skills Building**: Emphasize systematic approach to multi-step spatial analysis
- **Practical Applications**: Always connect to real-world GIS workflows students will encounter