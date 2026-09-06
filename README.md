# AI-Based Study Planner Agent

An automated, utility-based rational AI agent built in Python that generates an optimized weekly study timetable. It dynamically calculates real-time prioritization scores to maximize weighted subject coverage before academic deadlines.

## 🧠 PEAS Formulation
*   **Performance Measure:** Maximizes total weight-weighted coverage of subjects before deadlines without exceeding maximum daily study hour bounds.
*   **Environment:** A finite horizon of study days containing fixed available hours alongside a complex set of target subjects.
*   **Actuators:** Allocates specific time blocks ($N$ hours) of a target day to an outstanding subject (timetable mapping).
*   **Sensors:** Parses initial attributes (`deadline_days`, `difficulty`, `weight`, `hours_needed`) and re-evaluates remaining capacity metrics sequentially each day.

## ⚙️ Mathematical Utility Calculation
Rather than following rigid state-action rules, the agent calculates an objective utility value for each active subject daily:

$$\text{urgency} = \frac{1}{\max(\text{days\_left}, 0.5)}$$
$$\text{importance} = \text{weight} \times \text{difficulty}$$
$$\text{utility} = \text{importance} \times \text{urgency}$$

The agent then applies a greedy fractional-knapsack sort on these values to distribute work items optimally.

## 📂 Architecture Overview
The application consists of a single module containing:
*   `Subject`: A data container tracking subject specifications, remaining work hours, and completion flags.
*   `StudyPlannerAgent`: The primary execution framework that manages the simulation timeline, updates state parameters, handles constraints, and populates an auditable rationale history log.
*   `render_timetable()`: Formats the raw analytical objects into a scannable structural summary showing data-driven reasoning workflows.

## 🚀 Getting Started

### Run the Simulation
Execute the underlying module directly through your terminal:
```bash
python "ai study_planner1.py"
```

### Sample Output Configuration
By default, the demo evaluates a four-subject payload across a 7-day timeline with a 3-hour daily capacity:
*   **Maths:** Deadline Day 2, High Importance (Weight=5, Difficulty=4).
*   **Physics:** Deadline Day 3, High Importance (Weight=4, Difficulty=5).
*   **History & English:** Longer horizons, lower cognitive weights.

 
