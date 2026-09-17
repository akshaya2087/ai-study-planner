import pytest
from src.planner import StudyPlannerAgent

def test_planner_initialization():
    """Verifies that the StudyPlanner Agent instantiates correctly with metrics."""
    subjects = ["Math", "Science"]
    agent = StudyPlannerAgent(topics=subjects, total_hours=10)
    assert agent.total_hours == 10
    assert len(agent.topics) == 2

def test_plan_generation_not_empty():
    """Ensures the heuristic generation maps all given subject streams."""
    subjects = ["Math", "Science"]
    agent = StudyPlannerAgent(topics=subjects, total_hours=10)
    plan = agent.generate_plan()
    
    for subject in subjects:
        assert subject in plan
        assert plan[subject] > 0
