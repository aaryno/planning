# Python Rasterio - Working with Raster Data

## 🎯 Assignment Overview

Welcome to your introduction to working with raster data in Python! This assignment will teach you the basics of reading, analyzing, and processing raster datasets using the `rasterio` library - a powerful tool that GIS professionals use to work with satellite imagery, elevation data, and other gridded datasets.

**Don't worry if you're new to programming!** This assignment is designed as a guided walkthrough. Each function has detailed comments showing you exactly what to write.

## 📚 What You'll Learn

By completing this assignment, you'll be able to:
- Open and read raster files (like GeoTIFFs)
- Extract basic information about raster datasets
- Calculate simple vegetation indices (NDVI)
- Sample raster values at specific locations
- Work with remote raster data (Cloud-Optimized GeoTIFFs)

## 🏗️ Assignment Structure

This assignment has **3 main parts** with **8 simple functions** total:

### Part 1: Raster Basics (3 functions)
- Read raster files and get basic information
- Extract raster statistics
- Understand coordinate systems and projections

### Part 2: Band Math and Indices (2 functions)  
- Calculate NDVI (vegetation health indicator)
- Work with multi-band satellite imagery

### Part 3: Practical Applications (3 functions)
- Sample raster values at point locations
- Read remote raster data
- Create simple raster summaries

## 🚀 Getting Started

### Step 1: Open Your Development Environment

**Recommended: Use GitHub Codespaces**
1. Click the green "Code" button in your GitHub repository
2. Select "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the environment to load (2-3 minutes)

### Step 2: Understand the File Structure

```
python-rasterio/
├── src/
│   └── rasterio_analysis/
│       ├── raster_basics.py      ← Functions 1-3 (YOU EDIT THIS)
│       ├── band_math.py          ← Functions 4-5 (YOU EDIT THIS)  
│       └── applications.py       ← Functions 6-8 (YOU EDIT THIS)
├── tests/                        ← Tests (DON'T EDIT)
├── data/                         ← Sample data files
└── README.md                     ← This file
```

### Step 3: Look at the Sample Data

Your assignment includes sample raster files:
- `data/sample_elevation.tif` - Elevation data for practicing
- `data/sample_landsat.tif` - Multi-band satellite imagery
- `data/sample_points.geojson` - Point locations for sampling

## 📝 Your Tasks

### Part 1: Raster Basics (6 points)

Open `src/rasterio_analysis/raster_basics.py` and complete these functions:

#### Function 1: `read_raster_info()`
```python
def read_raster_info(raster_path):
    """
    Read basic information about a raster file.
    
    This function should:
    1. Open the raster file using rasterio.open()
    2. Extract width, height, number of bands
    3. Get the coordinate reference system (CRS)
    4. Return all this information in a dictionary
    
    HINT: Use 'with rasterio.open(raster_path) as src:'
    """
    # YOUR CODE GOES HERE
    # Fill in the missing parts following the comments
```

#### Function 2: `get_raster_stats()`
```python
def get_raster_stats(raster_path, band_number=1):
    """
    Calculate basic statistics for a raster band.
    
    This function should:
    1. Open the raster file
    2. Read the specified band as an array
    3. Calculate min, max, mean, and standard deviation
    4. Handle nodata values properly
    
    HINT: Use src.read(band_number) to read a band
    HINT: Use numpy functions like np.nanmin(), np.nanmax()
    """
    # YOUR CODE GOES HERE
```

#### Function 3: `get_raster_extent()`
```python
def get_raster_extent(raster_path):
    """
    Get the geographic extent (bounding box) of a raster.
    
    This function should:
    1. Open the raster file
    2. Get the bounds (left, bottom, right, top)
    3. Return as a dictionary with clear labels
    
    HINT: Use src.bounds to get the bounding box
    """
    # YOUR CODE GOES HERE
```

### Part 2: Band Math and Indices (4 points)

Open `src/rasterio_analysis/band_math.py` and complete these functions:

#### Function 4: `calculate_ndvi()`
```python
def calculate_ndvi(raster_path, red_band=3, nir_band=4):
    """
    Calculate NDVI (Normalized Difference Vegetation Index).
    
    NDVI = (NIR - Red) / (NIR + Red)
    
    This function should:
    1. Open the multi-band raster file
    2. Read the red band and near-infrared band
    3. Calculate NDVI using the formula above
    4. Handle division by zero (use np.where)
    5. Return the NDVI array and basic stats
    
    HINT: Be careful with nodata values!
    HINT: NDVI values should be between -1 and 1
    """
    # YOUR CODE GOES HERE
```

#### Function 5: `analyze_vegetation()`
```python
def analyze_vegetation(ndvi_array):
    """
    Classify vegetation health based on NDVI values.
    
    Classification:
    - NDVI < 0.2: Non-vegetation (water, buildings, bare soil)
    - NDVI 0.2-0.4: Sparse vegetation 
    - NDVI 0.4-0.7: Moderate vegetation
    - NDVI > 0.7: Dense vegetation
    
    This function should:
    1. Count pixels in each category
    2. Calculate percentages
    3. Return a summary dictionary
    
    HINT: Use np.sum() with boolean conditions
    """
    # YOUR CODE GOES HERE
```

### Part 3: Practical Applications (5 points)

Open `src/rasterio_analysis/applications.py` and complete these functions:

#### Function 6: `sample_raster_at_points()`
```python
def sample_raster_at_points(raster_path, points_list):
    """
    Extract raster values at specific coordinate locations.
    
    This function should:
    1. Open the raster file
    2. For each point (x, y) in points_list
    3. Convert coordinates to pixel indices
    4. Read the pixel value
    5. Return list of values
    
    HINT: Use rasterio.transform.rowcol() to convert coordinates
    HINT: Check if coordinates are within raster bounds
    """
    # YOUR CODE GOES HERE
```

#### Function 7: `read_remote_raster()`
```python
def read_remote_raster(url, bbox=None):
    """
    Read a raster from a remote URL (like a COG).
    
    This function should:
    1. Open the remote raster using the URL
    2. Optionally clip to a bounding box
    3. Read the data efficiently
    4. Return the data array and metadata
    
    HINT: COG URLs work just like local files with rasterio.open()
    HINT: Use windowed reading if bbox is provided
    """
    # YOUR CODE GOES HERE
```

#### Function 8: `create_raster_summary()`
```python
def create_raster_summary(raster_path):
    """
    Create a comprehensive summary of a raster dataset.
    
    This function should:
    1. Combine information from previous functions
    2. Include file info, statistics, and extent
    3. Add any special properties (like nodata values)
    4. Return a formatted summary dictionary
    
    HINT: You can call your other functions from this one!
    """
    # YOUR CODE GOES HERE
```

## 🧪 Testing Your Work

After completing each function, test it:

```bash
# Test individual parts
python -m pytest tests/test_raster_basics.py -v
python -m pytest tests/test_band_math.py -v  
python -m pytest tests/test_applications.py -v

# Test everything
python -m pytest tests/ -v
```

## 💡 Helpful Tips

### Getting Stuck?
1. **Read the error messages carefully** - they often tell you exactly what's wrong
2. **Check your variable names** - make sure they match the function requirements
3. **Print intermediate values** - use `print()` to see what your variables contain
4. **Use the sample data** - test with the provided files first

### Common Beginner Mistakes:
- Forgetting to import numpy as `np`
- Not handling nodata values (they show up as `nan`)
- Mixing up coordinate order (x,y vs y,x)
- Not closing raster files properly (use `with` statements)

### Debugging Example:
```python
def read_raster_info(raster_path):
    with rasterio.open(raster_path) as src:
        # Add print statements to debug
        print(f"Width: {src.width}")
        print(f"Height: {src.height}")
        print(f"Bands: {src.count}")
        
        # Your code here
        info = {
            'width': src.width,
            'height': src.height,
            # ... etc
        }
        return info
```

## 🎯 Grading

**Total: 15 points**

- **Part 1: Raster Basics (6 points)**
  - Function 1: `read_raster_info()` (2 points)
  - Function 2: `get_raster_stats()` (2 points) 
  - Function 3: `get_raster_extent()` (2 points)

- **Part 2: Band Math (4 points)**
  - Function 4: `calculate_ndvi()` (2 points)
  - Function 5: `analyze_vegetation()` (2 points)

- **Part 3: Applications (5 points)**
  - Function 6: `sample_raster_at_points()` (2 points)
  - Function 7: `read_remote_raster()` (2 points)
  - Function 8: `create_raster_summary()` (1 point)

### What We're Looking For:
- ✅ **Functions work correctly** (pass the tests)
- ✅ **Code handles errors gracefully** (doesn't crash on bad input)
- ✅ **Results make sense** (reasonable values and formats)
- ✅ **Following instructions** (using the required approach)

## 🆘 Getting Help

### If You're Stuck:
1. **Re-read the function comments** - they contain step-by-step instructions
2. **Look at the test files** - they show examples of how functions should work
3. **Check the sample data** - make sure you understand what you're working with
4. **Ask for help** - post in the discussion forum or attend office hours

### Common Questions:

**Q: "My function returns None instead of a value"**
A: Make sure you have a `return` statement at the end of your function.

**Q: "I get a 'module not found' error"**  
A: Check that you're in the right directory and rasterio is installed.

**Q: "My NDVI values look wrong"**
A: Make sure you're using the right bands and handling nodata properly.

**Q: "Tests are failing but my function seems right"**
A: Check that your return format matches exactly what the tests expect.

## 🏆 Success Tips

1. **Start simple** - Get basic functionality working first
2. **Test frequently** - Run tests after each function
3. **Read carefully** - The comments tell you exactly what to do
4. **Don't overthink it** - These functions are simpler than they might seem
5. **Use the resources** - Sample data and tests are there to help you

## 📚 Additional Resources

- [Rasterio Documentation](https://rasterio.readthedocs.io/) - Official docs
- [Rasterio Quickstart](https://rasterio.readthedocs.io/en/latest/quickstart.html) - Getting started guide
- [Working with Raster Data in Python](https://carpentries-incubator.github.io/geospatial-python/04-raster-structure/index.html) - Tutorial

Remember: This is a learning exercise! The goal is to understand how to work with raster data, not to write perfect production code. Take your time, ask questions, and don't be afraid to experiment.

Good luck! 🌟