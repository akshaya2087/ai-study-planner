# AI-Based Study Planner Agent
**Student Name:** Akshaya  
**Register Number:** 113025148004  

---

## 1. Problem Formulation

### 1.1 Problem Statement
Students often struggle to distribute their study time efficiently across multiple complex subjects. Manual scheduling leads to uneven time allocation, fatigue, or neglect of critical topics. This project designs a localized **AI Study Planner Agent** that treats schedule creation as a State-Space Search problem, automatically generating balanced, multi-subject timelines within strict hourly limitations.

### 1.2 Component Specifications
*   **Initial State (\(S_0\)):** A list of input academic subjects/topics with zero hours allocated (\(H_i = 0\)), alongside a total target budget of hours (\(T\)).
*   **Actions (\(A\)):** Distributing integer-based time blocks (hours) out of the remaining budget to specific subjects.
*   **Transition Model (\(Result(S, A)\)):** Updates the target state by incrementing the hour count of subject \(i\) and decrementing the remaining global pool of hours.
*   **Goal State (\(G\)):** A fully complete timeline where the sum of all subject hours matches the budget exactly (\(\sum H_i = T\)), and time distributions are balanced optimally.
*   **Constraints:**
    1. **Strict Non-Zero Constraint:** No chosen topic can receive 0 hours (\(H_i \ge 1\)).
    2. **Budget Boundary:** Total hours assigned cannot exceed or fall short of the available time limit.

---

## 2. Approach & Architecture

### 2.1 Heuristic Optimization Model
The agent utilizes a State-Space Traversal algorithm optimized by a custom **Evaluation Function (\(f(n)\))**. Rather than performing a blind search, the agent uses a localized greedy heuristic to make baseline distributions and evaluates performance configurations using an objective metric.

### 2.2 Mathematical Evaluation Function
To measure the fitness and operational balance of any generated schedule, the evaluation function is structured as:

\[f(\text{schedule}) = 100 \times \text{variance\_modifier}\]

Where the variation coefficient is mathematically tied to the specific user's identification keys to ensure unique distribution grades.

### 2.3 Anti-Copy Personalisation Seeding
To enforce academic integrity and project uniqueness, the structural search tree uses the student's unique identification key as a hardcoded parameter.
*   **Active Anchor Seed:** `113025148004`
*   By initializing `random.seed(113025148004)`, the localized decision paths, randomized exploration loops, and final plan evaluation scores are entirely distinct to this repository. Even if another student runs identical inputs, their output parameters will vary based on their seed, preventing code plagiarism.

---

## 3. How-to-Run & Execution

### 3.1 Dependencies Installation
Install the core framework packages configured in the project manifest:
```bash
pip install -r requirements.txt
```

### 3.2 Executing the System Agent
Run the main source script from the application root folder to see the agent generate the state space layout:
```bash
python src/planner.py
```

### 3.3 Running Automated Testing Validations
To run the automated validation tests confirming module reliability:
```bash
python -m pytest
```

---

## 4. Sample Verification I/O

### 4.1 System Input Parameters
*   **Target Subject Streams:** `["Data Structures", "Algorithms", "System Design"]`
*   **Total Time Allocation Window:** `15 Hours`
*   **Operational Validation Key:** `113025148004`

### 4.2 System Output Manifest
```text
--- AI Study Planner Agent Output ---
Register Number Seed Active: 113025148004
Allocated Study Plan: {'Data Structures': 4, 'Algorithms': 6, 'System Design': 4}
Plan Evaluation Score: 91.0
```
