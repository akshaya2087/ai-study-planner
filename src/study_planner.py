from datetime import datetime, timedelta


class StudyPlannerAgent:
    def __init__(self, subjects, daily_hours, objective="Maximize coverage of high-priority topics"):
        self.subjects = subjects
        self.daily_hours = daily_hours
        self.objective = objective

    # Calculate the utility/priority score
    def calculate_utility(self, subject):
        today = datetime.today().date()
        deadline = datetime.strptime(subject["deadline"], "%Y-%m-%d").date()

        remaining_days = (deadline - today).days

        # Avoid division by zero or negative values
        if remaining_days <= 0:
            remaining_days = 1

        priority = subject["priority"]
        difficulty = subject["difficulty"]

        # Rational Agent Utility Function
        utility = (priority * difficulty * 10) / remaining_days

        return round(utility, 2)

    # Calculate and sort subjects according to utility
    def prioritize_subjects(self):
        for subject in self.subjects:
            subject["utility"] = self.calculate_utility(subject)

        # Higher utility = higher priority
        self.subjects.sort(
            key=lambda x: x["utility"],
            reverse=True
        )

        return self.subjects

    # Generate a weekly timetable
    def generate_schedule(self):
        prioritized_subjects = self.prioritize_subjects()

        schedule = {}
        today = datetime.today().date()

        for day_number in range(7):
            current_day = today + timedelta(days=day_number)
            remaining_hours = self.daily_hours

            daily_plan = []

            # Allocate time based on priority
            for subject in prioritized_subjects:

                if remaining_hours <= 0:
                    break

                # Higher utility subjects receive more time
                if subject["utility"] >= 10:
                    hours = min(2, remaining_hours)
                elif subject["utility"] >= 5:
                    hours = min(1.5, remaining_hours)
                else:
                    hours = min(1, remaining_hours)

                daily_plan.append({
                    "subject": subject["name"],
                    "hours": hours,
                    "utility": subject["utility"],
                    "deadline": subject["deadline"]
                })

                remaining_hours -= hours

            schedule[current_day.strftime("%A, %d-%m-%Y")] = daily_plan

        return schedule

    # Display timetable
    def display_schedule(self, schedule):
        print("\n" + "=" * 60)
        print("          AI-BASED WEEKLY STUDY PLANNER")
        print("=" * 60)

        print(f"\nObjective: {self.objective}")
        print(f"Available Study Hours Per Day: {self.daily_hours}\n")

        for day, tasks in schedule.items():
            print("-" * 60)
            print(day)
            print("-" * 60)

            for task in tasks:
                print(
                    f"📚 {task['subject']} | "
                    f"{task['hours']} hour(s) | "
                    f"Utility Score: {task['utility']} | "
                    f"Deadline: {task['deadline']}"
                )

            print()

    # Explain the rational decision-making
    def explain_reasoning(self):
        print("\n" + "=" * 60)
        print("WHY IS THIS AGENT RATIONAL?")
        print("=" * 60)

        print("""
The agent follows a utility-based rational decision-making process.

For every subject, it considers:

1. Priority Weight
   - Important subjects receive higher priority.

2. Difficulty
   - Difficult subjects require more preparation.

3. Deadline Urgency
   - Subjects with closer deadlines become more urgent.

The utility function combines these factors:

Utility = (Priority × Difficulty × 10) / Remaining Days

The agent selects subjects with the highest utility scores first.
Therefore, the generated timetable attempts to maximize the
coverage of important and urgent subjects within the available
daily study hours.
""")


# ---------------- MAIN PROGRAM ----------------

subjects = []

number_of_subjects = int(input("Enter the number of subjects: "))
daily_hours = float(input("Enter available study hours per day: "))

for i in range(number_of_subjects):
    print(f"\nEnter details for Subject {i + 1}")

    name = input("Subject name: ")
    deadline = input("Deadline (YYYY-MM-DD): ")
    difficulty = int(input("Difficulty (1 = Easy, 5 = Very Hard): "))
    priority = int(input("Priority/Weight (1 = Low, 5 = Very High): "))

    subjects.append({
        "name": name,
        "deadline": deadline,
        "difficulty": difficulty,
        "priority": priority
    })


# Create the Rational Agent
agent = StudyPlannerAgent(
    subjects=subjects,
    daily_hours=daily_hours,
    objective="Maximize coverage of urgent and high-priority topics before deadlines"
)

# Generate timetable
weekly_schedule = agent.generate_schedule()

# Display results
agent.display_schedule(weekly_schedule)

# Explain rationality
agent.explain_reasoning() 
