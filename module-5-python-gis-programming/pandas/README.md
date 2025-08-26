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

**🎓 Learning Approach:**
This assignment uses **interactive Jupyter notebooks** to teach you each function step-by-step, then you implement the actual code in Python files for grading. This mirrors real-world data science workflows where you prototype in notebooks before writing production code!

**Time commitment:** About 3-4 hours total (includes notebook learning and testing)

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

# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (this creates a virtual environment automatically)
uv sync --group test --group dev

# Activate the virtual environment (optional - uv run handles this automatically)
source .venv/bin/activate
```

### Step 3: Verify Your Environment

**In Codespaces or Local Setup:**
```bash
# Test that pandas and pytest are working with uv
uv run python -c "import pandas as pd; print(f'Pandas {pd.__version__} ready!')"
uv run python -c "import pytest; print(f'pytest {pytest.__version__} ready!')"

# You should see both libraries working!
# Note: uv automatically manages the virtual environment
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
├── pytest.ini                    # Test configuration  
├── pyproject.toml                # Modern Python project configuration (replaces requirements.txt)
├── uv.lock                       # Locked dependency versions for reproducible builds
├── requirements.txt              # Legacy dependency file (kept for compatibility)
└── .github/workflows/            # 🤖 Automated grading (CI/CD)
```

---

## 📝 Your Assignment Tasks

You need to implement **5 functions** in the file `src/pandas_basics.py`. Each function has a corresponding Jupyter notebook in the `notebooks/` directory that teaches you how to build it step by step.

**📚 Learning Process:**
1. **Learn**: Open the notebook for each function to understand how it works
2. **Implement**: Write your code in `src/pandas_basics.py` (replace the TODO comments)
3. **Test**: Run pytest to verify your implementation works correctly

**🎯 Your Task:** The notebooks show you HOW to build each function, but you must implement the actual code in `src/pandas_basics.py` to pass the unit tests. The notebooks are for learning - the assignment requires working code in the .py file!

### 🔧 Part 1: Load and Explore Data (4 points)
**Function:** `load_and_explore_gis_data(file_path)`  
📚 **Learning Notebook:** `notebooks/01_function_load_and_explore_gis_data.ipynb`

**What to implement in `src/pandas_basics.py`:**
1. Use `pd.read_csv()` to load a CSV file
2. Print basic information about the dataset (shape, columns, data types)
3. Display the first 5 rows using `.head()`
4. Show summary statistics using `.describe()`
5. Handle file not found errors and other issues
6. Return the loaded DataFrame

**Test your function:**
```bash
uv run pytest tests/test_pandas_basics.py::test_load_and_explore_gis_data -v
```

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
📚 **Learning Notebook:** `notebooks/02_function_filter_environmental_data.ipynb`

**What to implement in `src/pandas_basics.py`:**
1. Filter the DataFrame using boolean indexing to show only rows where:
   - Temperature is between min_temp and max_temp
   - Data quality equals the specified quality level
2. Handle input validation and missing columns
3. Print filtering statistics (rows kept vs. removed)
4. Return the filtered DataFrame

**Test your function:**
```bash
uv run pytest tests/test_pandas_basics.py::test_filter_environmental_data -v
```

**Example output:**
```
Filtering data...
Original dataset: 500 rows
After filtering: 247 rows kept, 253 rows removed
Filters applied:
- Temperature between 15°C and 30°C
- Data quality = 'good'
```

### 📈 Part 3: Calculate Station Statistics (4 points)
**Function:** `calculate_station_statistics(df)`  
📚 **Learning Notebook:** `notebooks/03_function_calculate_station_statistics.ipynb`

**What to implement in `src/pandas_basics.py`:**
1. Group the data by station_id using `.groupby()`
2. Calculate mean temperature and humidity for each station (rounded to 1 decimal)
3. Count how many readings each station has using `.size()`
4. Create a summary DataFrame with columns: station_id, avg_temperature, avg_humidity, reading_count
5. Find and report the hottest and coolest stations
6. Return the statistics DataFrame

**Test your function:**
```bash
uv run pytest tests/test_pandas_basics.py::test_calculate_station_statistics -v
```

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
📚 **Learning Notebook:** `notebooks/04_function_join_station_data.ipynb`

**What to implement in `src/pandas_basics.py`:**
1. Use `pd.merge()` with a LEFT JOIN to preserve all readings
2. Join on the common column `station_id`
3. Analyze the relationship between datasets (which stations match)
4. Report join results (rows preserved, new columns added)
5. Handle cases where some readings might not have station info
6. Return the combined DataFrame

**Test your function:**
```bash
uv run pytest tests/test_pandas_basics.py::test_join_station_data -v
```

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
📚 **Learning Notebook:** `notebooks/05_function_save_processed_data.ipynb`

**What to implement in `src/pandas_basics.py`:**
1. Create output directory if it doesn't exist
2. Save the DataFrame to CSV using `.to_csv()` with good formatting
3. Validate the saved file by reading it back
4. Report file size, location, and rows saved
5. Handle errors (permissions, disk space, invalid paths)
6. Return True for success, False for failure

**Test your function:**
```bash
uv run pytest tests/test_pandas_basics.py::test_save_processed_data -v
```

### Code Quality (2 points)
Clean, readable code following the patterns shown in the notebooks.

---

## 🧪 Professional Development Workflow

**Important Learning Objective**: This assignment teaches you professional development practices including unit testing and the notebook-to-code workflow used in industry.

### Step 1: Learning with Notebooks

```bash
# Navigate to the notebooks directory
cd notebooks/

# Open Jupyter in your browser (if using local setup)
uv run jupyter notebook

# In Codespaces, notebooks open directly in VS Code
```

**Work through notebooks in order:**
1. `01_function_load_and_explore_gis_data.ipynb`
2. `02_function_filter_environmental_data.ipynb`  
3. `03_function_calculate_station_statistics.ipynb`
4. `04_function_join_station_data.ipynb`
5. `05_function_save_processed_data.ipynb`

### Step 2: Implement Functions

After learning from each notebook:
1. Open `src/pandas_basics.py`
2. Find the corresponding function
3. Replace TODO comments with your implementation
4. Test immediately (see Step 3)

### Step 3: Test-Driven Development

**Professional developers test as they code!** Test each function individually:

```bash
# Test a specific function
uv run pytest tests/test_pandas_basics.py::test_load_and_explore_gis_data -v

# Test all functions
uv run pytest tests/ -v

# Get detailed output when tests fail
uv run pytest tests/ -v -s
```

### Step 4: Debug and Iterate

When tests fail, the error messages tell you exactly what's wrong:

```bash
# Example of what you might see:
FAILED tests/test_pandas_basics.py::test_filter_environmental_data 
AssertionError: Expected DataFrame with 45 rows, got 0 rows
```

This tells you your filtering isn't working correctly - go back to the notebook to review!

### Step 5: Final Validation

When all functions work:

```bash
# Verify everything passes
uv run pytest tests/ -v

# You should see all PASSED
# Then commit and push your code
git add .
git commit -m "Complete pandas assignment - all functions implemented"
git push origin main
```

**🤖 Automated Grading:** GitHub Actions runs the same tests automatically and calculates your grade!

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