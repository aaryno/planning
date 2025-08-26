# Python Pandas for GIS Data Analysis

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 20 | Due: One week from assignment date**

---

## 🎯 Assignment Overview

Learn the **essential pandas skills** you need for GIS data analysis! This assignment teaches you how to work with tabular data (like CSV files) using Python's most popular data analysis library.

**What you'll learn:**
- Load CSV files with GIS data into Python
- Explore and understand your datasets  
- Filter data based on conditions (like "show me only high-quality readings")
- Calculate basic statistics and summaries
- Join datasets together (like combining station locations with measurements)
- Export your results for use in QGIS or other GIS software
- **Unit testing with pytest** - professional testing practices used in industry

**Time commitment:** About 3-4 hours total (includes learning unit testing)

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-python-pandas-[your-username]`

### Step 2: Choose Your Development Environment

**🪟 Windows Users: Use GitHub Codespaces (STRONGLY Recommended)**
- ✅ **No setup required** - everything works immediately
- ✅ **No Windows compatibility issues** - Unix environment provided
- ✅ **No conda/pip problems** - pre-configured pandas environment
- ✅ **Focus on learning** - not troubleshooting installation issues
- ✅ **Same environment as instructor** - guaranteed compatibility

```bash
# For Windows users (and everyone else):
# 1. Go to your assignment repository on GitHub
# 2. Click "Code" → "Create codespace on main"  
# 3. Wait 2-3 minutes for automatic setup
# 4. Start coding immediately!
```

**🐧🍎 Mac/Linux Users: Choose Your Preference**

**Option A: GitHub Codespaces (Recommended for All)**
```bash
# Click "Code" → "Create codespace on main"
# Pandas environment will be pre-configured and ready!
```

**Option B: Local Development (Mac/Linux Only - Windows at your own risk)**
```bash
# Clone your repository
git clone https://github.com/your-org/your-assignment-repo.git
cd your-assignment-repo

# Create conda environment
conda create -n gis-pandas python=3.11 pandas jupyter
conda activate gis-pandas

# OR use pip if you prefer
pip install pandas jupyter
```

### Step 3: Verify Your Environment

**In Codespaces or Local Setup:**
```bash
# Test that pandas and pytest are working
python -c "import pandas as pd; print(f'Pandas {pd.__version__} ready!')"
pip install pytest
python -c "import pytest; print(f'pytest {pytest.__version__} ready!')"

# You should see both libraries working!
```

---

## 📁 Understanding Your Assignment Files

```
python-pandas/
├── README.md                     # This file - your instructions
├── src/
│   └── pandas_basics.py          # 👈 YOUR CODE GOES HERE (5 functions to complete)
├── tests/
│   └── test_pandas_basics.py     # 🧪 Unit tests - learn professional testing!
├── data/
│   ├── weather_stations.csv      # Station location data
│   ├── temperature_readings.csv  # Daily temperature measurements
│   └── data_dictionary.md        # Explains what each column means
├── pytest.ini                   # Test configuration
├── requirements.txt              # Python dependencies
└── .github/workflows/            # 🤖 Automated grading (CI/CD)
```

---

## 📝 Your Assignment Tasks

You need to implement **5 functions** in the file `src/pandas_basics.py`. Each function builds on the previous one, so complete them in order.

### 🔧 Part 1: Load and Explore Data (4 points)
**Function:** `load_and_explore_gis_data(file_path)`

**What to do:**
1. Use `pd.read_csv()` to load a CSV file
2. Print basic information about the dataset (shape, columns, data types)
3. Display the first 5 rows using `.head()`
4. Show summary statistics using `.describe()`
5. Handle any obvious data issues

**Example output:**
```
Dataset loaded successfully!
Shape: (150, 5) - 150 rows and 5 columns
Columns: station_id, station_name, latitude, longitude, elevation_m

First 5 rows:
  station_id    station_name  latitude  longitude  elevation_m
0    STN_001    Central Park    40.768    -73.982          35
...
```

### 📊 Part 2: Filter Environmental Data (4 points)
**Function:** `filter_environmental_data(df, min_temp=15, max_temp=30, quality="good")`

**What to do:**
1. Filter the DataFrame to show only rows where:
   - Temperature is between min_temp and max_temp
   - Data quality equals the specified quality level
2. Print how many rows were kept vs. removed
3. Return the filtered DataFrame

**Example output:**
```
Filtering data...
Original dataset: 500 rows
After filtering: 247 rows kept, 253 rows removed
Filters applied:
- Temperature between 15°C and 30°C
- Data quality = 'good'
```

### 📈 Part 3: Calculate Basic Statistics (4 points)
**Function:** `calculate_station_statistics(df)`

**What to do:**
1. Group the data by station_id using `.groupby()`
2. Calculate mean temperature and humidity for each station
3. Count how many readings each station has
4. Create a summary DataFrame with these statistics
5. Show the station with highest and lowest average temperature

**Example output:**
```
Station Statistics Summary:
station_id  avg_temperature  avg_humidity  reading_count
STN_001            22.5           65.2            45
STN_002            21.8           67.1            52
...

Hottest station: STN_005 (avg: 24.3°C)
Coolest station: STN_012 (avg: 18.7°C)
```

### 🔗 Part 4: Join Station Data (4 points)
**Function:** `join_station_data(stations_df, readings_df)`

**What to do:**
1. Use `pd.merge()` to join the stations and readings DataFrames
2. Join on the common column `station_id`
3. Print information about the join results
4. Return the combined DataFrame

**Example output:**
```
Joining station locations with temperature readings...
Stations dataset: 15 stations
Readings dataset: 500 readings  
After joining: 500 rows (all readings matched to stations)
New columns added: station_name, latitude, longitude, elevation_m
```

### 💾 Part 5: Save Processed Data (2 points)
**Function:** `save_processed_data(df, output_file)`

**What to do:**
1. Save the DataFrame to a CSV file using `.to_csv()`
2. Include proper headers and formatting
3. Print confirmation that the file was saved
4. Show the file size and location

### Code Quality (2 points)
Clean, readable code with good comments and proper error handling.

---

## 🧪 Learning Professional Unit Testing with pytest

**Important Learning Objective**: This assignment teaches you **unit testing** - a critical professional skill where you write tests to verify your code works correctly.

### Step 1: Install Testing Dependencies

```bash
# In your Codespace or local environment
pip install pytest pandas

# OR if using conda
conda install pytest pandas
```

### Step 2: Understanding Unit Tests

Look at `tests/test_pandas_basics.py` to see how professional unit tests work:

```python
# Example unit test structure
import pytest
import pandas as pd
from src.pandas_basics import load_and_explore_gis_data

def test_load_and_explore_gis_data():
    """Test that function loads CSV and returns correct DataFrame"""
    # Arrange: Set up test data
    test_file = 'data/weather_stations.csv'
    
    # Act: Run the function
    result = load_and_explore_gis_data(test_file)
    
    # Assert: Check the results
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert 'station_id' in result.columns
```

### Step 3: Run Unit Tests as You Develop

**This is how professional developers work!** Test each function as you implement it:

```bash
# Run all tests
pytest tests/

# Run tests for a specific function
pytest tests/test_pandas_basics.py::test_load_and_explore_gis_data -v

# Run tests with detailed output
pytest tests/ -v --tb=short
```

You'll see output like:
```
======================== test session starts =========================
tests/test_pandas_basics.py::test_load_and_explore_gis_data PASSED
tests/test_pandas_basics.py::test_filter_environmental_data FAILED
tests/test_pandas_basics.py::test_calculate_station_statistics PASSED
tests/test_pandas_basics.py::test_join_station_data FAILED  
tests/test_pandas_basics.py::test_save_processed_data PASSED

======================= 3 passed, 2 failed ========================
```

### Step 4: Debug Failing Tests

When tests fail, pytest gives you detailed information:

```bash
# Get detailed failure information
pytest tests/ -v -s

# Use pytest's debugging features
pytest tests/test_pandas_basics.py::test_filter_data --pdb
```

### Step 5: Submit Your Work

When all tests pass locally:

```bash
# Verify all tests pass
pytest tests/

# Commit and push your work
git add .
git commit -m "Complete pandas assignment - all tests passing"  
git push origin main
```

**🤖 Automated Grading:** When you push to GitHub, the CI/CD pipeline automatically runs the same pytest tests and calculates your grade. **No manual grading script needed** - the unit tests ARE the grading system!

---

## 📊 Sample Data Provided

### `weather_stations.csv`
Information about 15 environmental monitoring stations in New York City:
- `station_id` - Unique identifier (STN_001, STN_002, etc.)
- `station_name` - Human-readable name
- `latitude`, `longitude` - Location coordinates  
- `elevation_m` - Height above sea level
- `station_type` - Type of monitoring equipment

### `temperature_readings.csv`
95 daily temperature measurements from the stations:
- `station_id` - Links to station information
- `date` - When measurement was taken (Jan 15-21, 2023)
- `temperature_c` - Air temperature in Celsius
- `humidity_percent` - Relative humidity
- `data_quality` - Quality flag ("good", "fair", "poor")

**💡 Tip:** Read `data/data_dictionary.md` for detailed information about the datasets!

---

## 📚 Learning Resources

### Pandas Basics
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html) - Quick tutorial
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) - Reference guide

### Key Functions You'll Use
```python
# Load data
df = pd.read_csv('filename.csv')

# Explore data
df.head()        # Show first 5 rows
df.info()        # Show column info
df.describe()    # Summary statistics

# Filter rows
filtered = df[df['column'] > value]
filtered = df[(df['temp'] > 15) & (df['quality'] == 'good')]

# Group and calculate
stats = df.groupby('station_id')['temperature'].mean()

# Join dataframes  
combined = pd.merge(df1, df2, on='common_column')

# Save results
df.to_csv('output.csv', index=False)
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

**"FileNotFoundError: No such file or directory"**
- Make sure you're in the assignment directory
- Check that data files are in the `data/` folder
- Use `pwd` to see your current location

**"KeyError: 'column_name'"**  
- Check column names using `df.columns`
- Column names are case-sensitive
- Look for extra spaces in column names

**"Tests are failing but my code looks right"**
- Read the error messages carefully
- Print intermediate results to debug: `print(df.head())`
- Make sure your function returns the right data type
- Check that your filtering conditions are correct

**"Grade script shows 0 points"**
- Run `python test_my_functions.py` first
- Fix any failing tests before running `grade.py`
- Make sure all 5 functions are implemented
- Check that function names are spelled correctly

---

## 📤 Submission Requirements

### What to Submit
1. **Completed code**: All 5 functions working in `src/pandas_basics.py`
2. **Passing tests**: `grade.py` shows 20/20 points
3. **Git commit**: Push your final code to your repository

### Grading Breakdown (20 points total)
- **Function 1** (4 pts): Load and explore data correctly
- **Function 2** (4 pts): Filter data with proper conditions  
- **Function 3** (4 pts): Calculate statistics by group
- **Function 4** (4 pts): Join datasets successfully
- **Function 5** (2 pts): Save data correctly
- **Code Quality** (2 pts): Clean, readable code with comments

### Success Checklist
- [ ] All functions implemented in `src/pandas_basics.py`
- [ ] `pytest tests/` shows all tests passing locally
- [ ] GitHub Actions shows green checkmark (automated tests pass)
- [ ] Code is clean and well-commented
- [ ] You understand how unit testing works
- [ ] Final commit pushed to GitHub

---

## 🎓 Why This Matters for GIS

**Real-world applications:**

🌡️ **Environmental Monitoring:** Process sensor data, filter for quality, calculate station averages

🏙️ **Urban Planning:** Combine census data with boundaries, analyze demographics by region

🌊 **Hydrology:** Join stream gauge data with station locations, identify flow patterns

🌱 **Agriculture:** Process crop yield data, correlate with weather and soil conditions

📊 **Data Preparation:** Clean and prepare tabular data before importing into QGIS

**Next steps:** These pandas skills will be essential for upcoming **GeoPandas** assignments where you'll work with spatial data directly!

---

## 🆘 Getting Help

1. **Read pytest error messages** - they show exactly which assertions failed
2. **Run individual tests** - `pytest tests/test_pandas_basics.py::test_function_name -v`
3. **Use print statements** - debug your code by printing intermediate results  
4. **Check the test file** - understand what the tests expect your functions to do
5. **Run tests frequently** - catch errors early with `pytest tests/`
6. **Use pytest debugging** - `pytest tests/ --pdb` drops you into Python debugger
7. **Ask on the course forum** - post specific test failure messages for help
8. **Attend office hours** - get help understanding unit testing concepts

---

**Remember:** Take your time to understand each function before moving to the next one. The step-by-step approach will make you successful! 🚀

**Good luck!**