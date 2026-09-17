# AI-Based Study Planner Agent
**Student Name:** Akshaya  
**Register Number:** 113025148004  

## 1. Problem Formulation
This project designs a localized **AI Study Planner Agent** that treats schedule creation as a State-Space Search problem, automatically generating balanced, multi-subject timelines within strict hourly limitations.
*   **Initial State:** A list of academic subjects with zero hours allocated.
*   **Goal State:** A complete timeline matching the exact requested hours.
*   **Constraints:** No topic can have 0 hours; total hours allocated must exactly equal the target budget.

## 2. Approach
The agent utilizes a State-Space Traversal algorithm optimized by a custom **Evaluation Function**. The structural search tree uses the student's unique identification key (`113025148004`) as a hardcoded parameter via `random.seed()` to ensure operational uniqueness and prevent code plagiarism.

## 3. How-to-Run
Install the core framework packages:
```bash
pip install -r requirements.txt
```

Execute the system agent:
```bash
python src/planner.py
```

Run the automated validation tests:
```bash
python -m pytest
```

## 4. Sample Verification Output
```text
--- AI Study Planner Agent Output ---
Register Number Seed Active: 113025148004
Allocated Study Plan: {'Data Structures': 4, 'Algorithms': 6, 'System Design': 4}
Plan Evaluation Score: 91.0
```
