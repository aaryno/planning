# Python Pandas Data Analysis - Automated Assessment

**GIST 604B - Open Source GIS Programming**  
**Module 5: Python GIS Programming**  
**Points: 30 | Due: Two weeks from assignment date**

---

## 🎯 Assignment Overview

This assignment introduces you to **pandas fundamentals** while teaching you professional software development practices through **automated assessment**. Your code will be continuously tested using **GitHub Actions CI/CD pipelines** - the same technology used by major tech companies for quality assurance.

### 🔑 Key Learning Innovation
- **Real-world Skills**: Experience with automated testing, code quality checks, and CI/CD workflows
- **Immediate Feedback**: Get instant results on code quality, correctness, and performance  
- **Professional Standards**: Learn industry best practices for data analysis code

### 📋 Prerequisites
- Basic Python programming knowledge
- Familiarity with git/GitHub
- Completion of "Codespaces Introduction" assignment

---

## 🚀 Getting Started

### Step 1: Accept the Assignment
1. Click the **GitHub Classroom assignment link** provided by your instructor
2. Accept the assignment to create your personal repository
3. Your repo will be named: `gist-604b-python-pandas-[your-username]`

### Step 2: Open Your Development Environment

**Option A: GitHub Codespaces (Recommended)**
```bash
# Click "Code" → "Create codespace on main"
# Everything will be pre-configured!
```

**Option B: Local Development**
```bash
# Clone your repository
git clone https://github.com/your-org/your-assignment-repo.git
cd your-assignment-repo

# Install uv package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project
uv sync --all-extras --dev
```

### Step 3: Verify Setup
```bash
# Check Python version
python --version  # Should be 3.13+

# Verify dependencies
uv pip list

# Run initial tests (these will fail until you implement functions)
uv run pytest tests/ -v
```

---

## 📁 Project Structure

```
your-assignment-repo/
├── 📜 README.md                     # This file
├── 📜 pyproject.toml                # Project configuration
├── 🔧 uv.lock                       # Dependency lock file
├── 📁 .github/
│   ├── 📁 workflows/
│   │   └── 📜 automated-grading.yml # CI/CD pipeline ⚙️
│   └── 📁 scripts/
│       └── 📜 calculate_grade.py    # Grading logic
├── 📁 src/pandas_analysis/          # 👈 YOUR CODE GOES HERE
│   ├── 📜 __init__.py
│   ├── 📜 data_structures.py        # 🔥 Part 1: Implement these functions
│   ├── 📜 data_subsetting.py        # 🔥 Part 2: Implement these functions  
│   ├── 📜 data_joins.py             # 🔥 Part 3: Implement these functions
│   └── 📜 file_operations.py        # 🔥 Part 4: Implement these functions
├── 📁 tests/                        # ✅ Test files (DON'T EDIT)
│   ├── 📜 test_data_structures.py   # Automated tests
│   ├── 📜 test_data_subsetting.py   # Automated tests
│   ├── 📜 test_data_joins.py        # Automated tests
│   ├── 📜 test_file_operations.py   # Automated tests
│   └── 📜 test_fixtures.py          # Test data
├── 📁 benchmarks/                   # ⚡ Performance tests (DON'T EDIT)
│   └── 📜 performance_tests.py      # Speed benchmarks
└── 📁 data/                         # 📊 Sample datasets (PROVIDED)
    ├── 📜 sample_gis_data.csv
    ├── 📜 environmental_stations.csv
    └── 📜 infrastructure_inventory.csv
```

---

## 📝 Assignment Tasks

You need to implement **4 modules** with specific functions that will be automatically tested:

### 🔧 Part 1: Data Structures (8 points)
**File:** `src/pandas_analysis/data_structures.py`

Implement these functions:
- `create_gis_series()` - Create pandas Series with proper indexing
- `analyze_series_properties()` - Extract Series metadata
- `create_gis_dataframe()` - Build DataFrame with type optimization  
- `optimize_dataframe_memory()` - Reduce memory usage by 20%+

### 📊 Part 2: Data Subsetting (10 points)  
**File:** `src/pandas_analysis/data_subsetting.py`

Implement these functions:
- `boolean_filter_environmental_data()` - Filter with boolean indexing
- `multi_condition_analysis()` - Categorize data by conditions
- `optimize_boolean_operations()` - Performance-optimized filtering

### 🔗 Part 3: Data Joins (7 points)
**File:** `src/pandas_analysis/data_joins.py`  

Implement these functions:
- `validate_join_keys()` - Pre-join validation
- `smart_join_gis_data()` - Intelligent joining with stats
- `complex_multi_dataset_join()` - Sequential multi-table joins

### 💾 Part 4: File Operations (5 points)
**File:** `src/pandas_analysis/file_operations.py`

Implement these functions:
- `robust_csv_reader()` - CSV reading with error handling  
- `export_with_metadata()` - Save data with embedded metadata

---

## 🤖 Automated Grading System

Every time you **push code** to GitHub, the automated grading system runs:

### 📊 Grade Breakdown (30 points total)

| Component | Points | What's Tested |
|-----------|--------|---------------|
| **Correctness** | 15 | Unit tests passing |
| **Performance** | 5 | Speed benchmarks |  
| **Code Quality** | 5 | Formatting, linting, type hints |
| **Test Coverage** | 5 | How much code is tested |

### 🔄 CI/CD Pipeline Steps

1. **Code Quality Checks**
   - Black formatting
   - Ruff linting  
   - MyPy type checking
   - Bandit security scan

2. **Correctness Testing**
   - Unit tests for all functions
   - Data integrity validation
   - Edge case handling

3. **Performance Benchmarks**
   - Speed tests on large datasets
   - Memory efficiency checks
   - Algorithm optimization validation

4. **Coverage Analysis**
   - Test coverage measurement
   - Code path analysis

5. **Final Grade Calculation**
   - Automated scoring
   - Detailed feedback generation

---

## 💻 Development Workflow

### 🔧 Local Development

```bash
# Make a new branch for your work
git checkout -b pandas-implementation

# Run tests while developing
uv run pytest tests/test_data_structures.py -v

# Check code quality
uv run black src/ tests/
uv run ruff check src/ tests/
uv run mypy src/

# Run performance benchmarks
uv run pytest benchmarks/ --benchmark-only

# Run all tests with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

### 📈 Viewing Results

**Local Results:**
```bash
# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**GitHub Results:**
- Go to your repo → "Actions" tab
- Click on latest workflow run
- View detailed results and feedback

### 🔄 Typical Development Cycle

1. **Implement** a function in one of the 4 modules
2. **Test locally**: `uv run pytest tests/test_[module].py -v`  
3. **Fix issues** until tests pass
4. **Check quality**: Run formatting and linting
5. **Commit & push**: `git add . && git commit -m "Implement function_name" && git push`
6. **Review feedback** in GitHub Actions results
7. **Iterate** until all tests pass

---

## 📊 Understanding Your Grade

### 🎯 Grade Thresholds

| Grade | Total Score | Percentage | Status |
|-------|-------------|------------|--------|
| **A** | 27-30 | 90-100% | ✅ Excellent |
| **B** | 24-26 | 80-89% | ✅ Good |  
| **C** | 21-23 | 70-79% | ✅ Satisfactory |
| **D** | 18-20 | 60-69% | ⚠️ Needs Improvement |
| **F** | < 18 | < 60% | ❌ Unsatisfactory |

### 📝 Reading Automated Feedback

After each push, you'll get detailed feedback:

**✅ Example Passing Result:**
```
🎉 Overall Score: 28/30 (93.3%)

Component Scores:
✅ Unit Tests: 14/15 (93%)
✅ Performance: 5/5 (100%) 
✅ Code Quality: 4/5 (80%)
✅ Test Coverage: 5/5 (100%)

💡 Feedback:
✅ Excellent work! Code meets professional standards
⚡ All performance benchmarks passed
✨ Consider adding more type hints for full score
```

**❌ Example Failing Result:**
```
❌ Overall Score: 16/30 (53.3%)

Component Scores:
❌ Unit Tests: 8/15 (53%)
❌ Performance: 2/5 (40%)
✅ Code Quality: 4/5 (80%) 
❌ Test Coverage: 2/5 (40%)

💡 Feedback:
🔧 Focus on making your functions pass the unit tests
⚡ Consider optimizing algorithms for better performance
🎯 Write more comprehensive tests to increase coverage
```

---

## 🛠️ Troubleshooting

### ❓ Common Issues

**🐛 Tests are failing**
```bash
# Run specific test with detailed output
uv run pytest tests/test_data_structures.py::TestCreateGISSeries::test_basic_series_creation -v -s

# Debug with print statements
# Add print() statements to your functions to debug
```

**🐌 Performance benchmarks failing**
```bash
# Run benchmarks locally to see timings
uv run pytest benchmarks/ --benchmark-only -v

# Profile your code
uv run python -m cProfile -s cumtime your_script.py
```

**💥 Import errors**
```bash
# Make sure you're in the right directory
pwd  # Should show your assignment directory

# Reinstall dependencies
uv sync --all-extras --dev
```

**🔧 Code quality issues**
```bash
# Auto-fix formatting
uv run black src/ tests/

# See detailed linting issues  
uv run ruff check src/ tests/ --show-source

# Fix type hints
uv run mypy src/ --show-error-codes
```

### 🆘 Getting Help

1. **Check the automated feedback** first - it usually tells you exactly what's wrong
2. **Read the test files** in `tests/` to understand what's expected
3. **Run tests locally** before pushing to GitHub
4. **Ask on the discussion forum** with specific error messages
5. **Attend office hours** for complex debugging

---

## 📤 Submission Instructions

### 🎯 Final Submission Process

1. **Ensure all tests pass locally:**
   ```bash
   uv run pytest tests/ -v
   ```

2. **Check your final grade:**
   ```bash
   python .github/scripts/calculate_grade.py
   ```

3. **Push your final code:**
   ```bash
   git add .
   git commit -m "Final submission - all tests passing"
   git push origin main
   ```

4. **Verify automated grading:**
   - Go to GitHub Actions
   - Ensure latest run shows "✅ PASS"
   - Final score should be ≥18 points (60%)

5. **Submit on Canvas:**
   - Submit your **GitHub repository URL**
   - Include your **final automated grade screenshot**

### ✅ Submission Checklist

- [ ] All 4 modules implemented (`data_structures.py`, `data_subsetting.py`, `data_joins.py`, `file_operations.py`)
- [ ] All unit tests passing (green ✅ in GitHub Actions)  
- [ ] Performance benchmarks meeting requirements
- [ ] Code quality checks passing (Black, Ruff, MyPy)
- [ ] Final score ≥ 18/30 points (60%)
- [ ] Repository URL submitted on Canvas
- [ ] Grade report screenshot submitted

---

## 🎓 Professional Skills Developed

### 🔥 Industry-Relevant Capabilities
- **Automated Testing**: Write code that passes comprehensive test suites
- **Performance Optimization**: Optimize algorithms for speed and memory
- **Code Quality**: Follow professional formatting and linting standards  
- **CI/CD Pipelines**: Experience with automated deployment workflows
- **Documentation**: Write clear, maintainable code with proper type hints

### 🚀 Career Preparation
- **Version Control**: Advanced git workflows with automated testing
- **Code Review**: Understanding automated feedback and quality metrics
- **Data Engineering**: Professional pandas techniques for large datasets
- **DevOps Practices**: CI/CD pipeline configuration and management

---

## 📚 Additional Resources

### 📖 Pandas Documentation
- [Pandas Official Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)

### 🧪 Testing Resources  
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://realpython.com/pytest-python-testing/)

### ⚡ Performance Optimization
- [Pandas Performance Tips](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)
- [Memory Usage Optimization](https://pandas.pydata.org/docs/user_guide/categorical.html)

### 🔧 Code Quality Tools
- [Black Code Formatter](https://black.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)

---

## 🏆 Success Tips

1. **Start Early**: Begin implementing functions immediately - don't wait
2. **Test Frequently**: Run tests after each function implementation  
3. **Read Error Messages**: The automated feedback is very detailed
4. **Focus on Correctness First**: Get tests passing before optimizing
5. **Use Type Hints**: They help catch errors and improve grades
6. **Ask Questions**: Use the discussion forum and office hours
7. **Review Sample Data**: Understand the CSV files in the `data/` folder
8. **Check GitHub Actions**: Monitor your automated grades regularly

---

**Good luck! 🚀 This assignment will teach you valuable professional skills while building strong pandas fundamentals.**

**Remember: The automated grading system is your friend - it provides immediate, detailed feedback to help you succeed!**