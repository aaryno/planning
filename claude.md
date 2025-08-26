Background:

Working directory: planning/module-5-python-gis-programming/
Course map: planning/course_map.md

Overview:
This is all for a course named GIST 604B - Open Source GIS Programming. This is part of the GIST curriculum at the U of A.
The course descriptions for other courses in the GIST program can be found in the reference/ directory (including that of GIST604B which you can ignore since we will update it later). When students have completed the required courses they take GIST 604B last.

Ignore the gist-604b directories for now. They represent the assignments before this current course refresh which is the point of this chat session with you.


About the students: The students are not good programmers so they need a lot of guidance.
Refer to the course_map.md to see what other concepts students will have learned before any given lecture or assignment.

All data should be accessible to the students either in this repository or from downloads. Scripts will be provided for any assignment that needs the data.

Any programming assignments should be testable in CI but there should be companion jupyter notebooks so students can learn how to use the tools and visualize the data as they work on the assignments.

All assignments should be automatically graded in GitLab Workflows.

Use the module 5 python-pandas as a template for all assignments.

The README.md of the assignment templates should reference the fact that many (most) of the students are not in a Unix environment nor are Unix savvy. It should be clear to Windows users that much of the open source world operates best in a unix environment but not necessarily so. Point out how Windows users can perform the same tasks or else point out that the codespace provides the unix environment for them to work in. Unfortunately the instructor cannot assist with windows-related issues.

Since this course is the last course in the GIS Programming specialization, build on concepts learned in previous courses (reference/ directory).

Action: Look at the project status for python-rasterio and do what needs to be done to ensure that the assignment as written is do-able by the students, testable in CI, and automatically graded in GitLab Workflows. Rename it "python-rasterio" to simplify

At some point you were interrupted! 
---
To pick up where I left off, here's a concise summary:

## ✅ What I've Completed:

1. **Renamed** `python-rasterio-advanced` → `python-rasterio`
2. **Created missing source module**: `memory_efficient.py` with student implementation stubs
3. **Created comprehensive test files**:
   - `test_cog_operations.py` (561 lines)
   - `test_stac_integration.py` (637 lines) 
   - `test_memory_efficient.py` (767 lines)
   - `test_performance.py` (615 lines)
   - `test_windowed_processing.py` (679 lines, completed)
4. **Added missing functions** to `cog_operations.py` and `stac_integration.py` to match test expectations

## 🔄 Still Need To Complete:

1. **Create** `tests/test_raster_vector.py` (was interrupted)
2. **Update** `README.md` to remove GeoPandas references and focus on rasterio
3. **Update** `PROJECT_STATUS.md` to reflect current completed state
4. **Test** the CI workflow runs without errors
5. **Generate sample data** if needed (`data/create_sample_data.py` exists)

## 💡 Best Continuation Prompt:

**"Continue completing the python-rasterio assignment. You were creating test_raster_vector.py for raster-vector integration tests. After that, update the README.md and PROJECT_STATUS.md to reflect the current state, and ensure the CI workflow works properly. The assignment should be ready for students to implement the NotImplementedError functions."**

The assignment now has comprehensive test coverage and the expected function signatures - students just need to implement the actual functionality where there are `NotImplementedError` placeholders.