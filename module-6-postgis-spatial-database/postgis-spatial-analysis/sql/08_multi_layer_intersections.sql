-- ===================================================================
-- PostGIS Spatial Analysis Assignment - Query 8
-- Multi-Layer Spatial Intersections
-- ===================================================================
--
-- OBJECTIVE: Perform complex multi-layer intersection analysis to understand
-- how different spatial datasets overlap and interact across the landscape.
--
-- BUSINESS CONTEXT: Multi-layer intersection analysis is crucial for
-- environmental impact assessment, conservation planning, and regulatory
-- compliance. For example, determining where transportation infrastructure
-- intersects with protected areas and sensitive watersheds simultaneously.
--
-- LEARNING GOALS:
-- - Master complex intersection operations across 3+ spatial layers
-- - Calculate precise overlap areas and percentages
-- - Understand cumulative spatial impacts
-- - Develop advanced spatial analysis problem-solving skills
--
-- POINTS: 2 (Hints only - significant independent work required)
-- ===================================================================

-- ANALYSIS CHALLENGE:
-- Create a comprehensive multi-layer intersection analysis that examines
-- where transportation networks intersect with both protected areas AND
-- sensitive watersheds, then calculate the environmental impact potential.

-- STRATEGIC HINTS:

-- HINT 1: CORE ANALYSIS APPROACH
-- You need to find transportation routes that cross through protected areas
-- AND also pass through major watersheds (>15,000 sq mi drainage area).
-- This represents potentially high environmental impact corridors.

-- HINT 2: KEY SPATIAL FUNCTIONS TO USE
-- - ST_Intersects() to test if features overlap
-- - ST_Intersection() to get the actual overlap geometry
-- - ST_Length() to measure intersection distances
-- - ST_Area() for watershed overlap calculations
-- - Multiple JOIN conditions with spatial relationships

-- HINT 3: REQUIRED CALCULATIONS
-- For each qualifying transportation route, calculate:
-- - Total length of route within protected areas (miles)
-- - Number of different protected areas crossed
-- - Names of all protected areas intersected
-- - Primary watershed(s) affected
-- - Environmental sensitivity score (your own scoring system)

-- HINT 4: FILTERING CRITERIA
-- Focus on:
-- - Transportation routes of type 'Interstate Highway' or 'US Highway'
-- - Protected areas with designation 'National Park' or 'Wilderness Area'
-- - Watersheds with drainage_area_sqmi > 15000
-- - Only routes that intersect BOTH protected areas AND major watersheds

-- HINT 5: SCORING METHODOLOGY
-- Create an environmental impact score based on:
-- - Length of route through protected areas (longer = higher impact)
-- - Number of protected areas crossed (more = higher impact)
-- - Wilderness vs. Park designation (wilderness = higher sensitivity)
-- - Watershed size (larger watershed = broader impact potential)

-- HINT 6: OUTPUT STRUCTURE
-- Your results should include columns for:
-- - Route name and type
-- - Total protected area intersection length
-- - List of protected areas crossed
-- - Primary watershed information
-- - Environmental impact score (1-100 scale)
-- - Impact classification (Low/Medium/High/Critical)

-- HINT 7: ADVANCED TECHNIQUES NEEDED
-- - Complex multi-table joins with spatial conditions
-- - Aggregate functions (COUNT, SUM, STRING_AGG)
-- - Conditional logic (CASE statements)
-- - Subqueries for complex calculations
-- - Proper coordinate transformations for accurate measurements

-- HINT 8: BUSINESS INTELLIGENCE INSIGHTS
-- Your analysis should identify:
-- - Which transportation corridors pose highest environmental risk
-- - Protected areas most vulnerable to transportation impacts
-- - Watersheds with multiple infrastructure crossings
-- - Recommendations for environmental monitoring priorities

-- YOUR TASK:
-- Build the complete SQL query that implements this multi-layer analysis.
-- No template is provided - you must construct the entire query logic.
-- Focus on creating actionable environmental impact intelligence.

-- EXPECTED RESULT CHARACTERISTICS:
-- - 5-15 transportation routes that meet all intersection criteria
-- - Accurate length measurements in miles
-- - Meaningful environmental impact scores
-- - Professional-quality analysis suitable for environmental planning

-- SUCCESS CRITERIA:
-- □ Correctly identifies routes intersecting both protected areas AND major watersheds
-- □ Accurately calculates intersection lengths using proper coordinate transformations
-- □ Implements a logical environmental impact scoring system
-- □ Provides comprehensive route impact profiles
-- □ Demonstrates mastery of complex multi-layer spatial analysis

-- CHALLENGE LEVEL: Advanced
-- You must synthesize multiple PostGIS concepts and create original analysis logic.
-- This mirrors real-world environmental consulting analysis requirements.
