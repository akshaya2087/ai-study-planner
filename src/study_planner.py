
from dataclasses import dataclass, field
from typing import List, Dict
@dataclass
class Subject:
    name: str
    deadline_days: int      # deadline, counted in days from today (day 0)
    difficulty: int         # 1 (easy) .. 5 (hard)
    weight: int             # 1 (low priority) .. 5 (high priority / high marks)
    hours_needed: float     # total hours of study still required
    hours_done: float = field(default=0.0, init=False)

    @property
    def hours_remaining(self) -> float:
        return max(0.0, self.hours_needed - self.hours_done)

    @property
    def is_complete(self) -> bool:
        return self.hours_remaining <= 1e-9


# ---------------------------------------------------------------------------
# 2. The utility (priority) function
# ---------------------------------------------------------------------------
#
# For a subject that still needs work, on a given day with `days_left`
# days remaining until its deadline, the agent computes:
#
#     urgency    = 1 / max(days_left, 0.5)         -> explodes as deadline nears
#     importance = weight * difficulty              -> "how much this subject
#                                                       is worth in outcome"
#     utility    = importance * urgency
#
# Why this rule is rational given the stated objective ("maximise coverage
# of high-priority topics before deadlines"):
#   - It is monotonically increasing in weight and difficulty, so a subject
#     that is worth more marks / is harder always outranks an easier,
#     lower-weight subject, all else equal.
#   - It is monotonically increasing as days_left shrinks, so two subjects
#     of equal importance are correctly ordered by which one runs out of
#     time first (a subject due tomorrow beats one due in 3 weeks).
#   - A subject with hours_remaining == 0 has utility 0 and drops out, so
#     the agent never wastes hours on completed work (no wasted actions).
#   - Because utility is recomputed EVERY day (not fixed once at the start),
#     the agent is reactive to its own progress: as it chips away at a
#     subject, importance*urgency for the *other* subjects keeps rising in
#     relative terms, so it naturally rebalances effort across the week
#     instead of tunnel-visioning on one topic.

def utility(subject: Subject, days_left: float) -> float:
    if subject.is_complete or days_left < 0:
        return 0.0
    urgency = 1.0 / max(days_left, 0.5)
    importance = subject.weight * subject.difficulty
    return importance * urgency


# ---------------------------------------------------------------------------
# 3. The agent: turns percepts -> actions (a day-by-day timetable)
# ---------------------------------------------------------------------------

class StudyPlannerAgent:
    """
    A utility-based rational agent.

    Each simulated day it:
      1. Perceives the current state of every subject (hours_remaining,
         days_left).
      2. Scores every unfinished subject with `utility()`.
      3. Greedily allocates the day's available hours to subjects in
         DESCENDING utility order, giving each subject at most as many
         hours as it still needs, until either the day's hours or the
         subjects run out.
      4. Logs the action (what it studied and why) so the rationale is
         auditable, then moves to the next day.

    This greedy-by-utility allocation is optimal for this problem because
    utility is additive across subjects and each hour spent on the
    highest-utility subject can never be improved on by spending it
    elsewhere while that subject still needs hours (classic fractional-
    knapsack-style argument: sort by "value per unit" and take greedily).
    """

    def __init__(self, subjects: List[Subject], daily_hours: float, horizon_days: int):
        self.subjects = subjects
        self.daily_hours = daily_hours
        self.horizon_days = horizon_days
        self.timetable: Dict[int, List[Dict]] = {}
        self.rationale_log: List[str] = []

    def plan(self) -> Dict[int, List[Dict]]:
        for day in range(self.horizon_days):
            hours_left_today = self.daily_hours
            day_plan = []

            # Step 1 + 2: perceive & score
            scored = []
            for s in self.subjects:
                days_left = s.deadline_days - day
                u = utility(s, days_left)
                if u > 0:
                    scored.append((u, days_left, s))

            # Step 3: act — greedy allocation by descending utility
            scored.sort(key=lambda t: t[0], reverse=True)
            for u, days_left, s in scored:
                if hours_left_today <= 1e-9:
                    break
                if days_left < 0:
                    continue  # deadline already passed; utility was 0 anyway
                give = min(hours_left_today, s.hours_remaining)
                if give <= 0:
                    continue
                s.hours_done += give
                hours_left_today -= give
                day_plan.append({
                    "subject": s.name,
                    "hours": round(give, 2),
                    "utility_score": round(u, 2),
                    "days_left": days_left,
                })

            self.timetable[day] = day_plan
            self._log_day(day, day_plan, hours_left_today)

        return self.timetable

    def _log_day(self, day, day_plan, hours_left_today):
        if not day_plan:
            self.rationale_log.append(f"Day {day}: nothing scheduled (all subjects complete or no hours).")
            return
        parts = ", ".join(
            f"{e['subject']} ({e['hours']}h, utility={e['utility_score']}, {e['days_left']}d left)"
            for e in day_plan
        )
        note = f"Day {day}: {parts}."
        if hours_left_today > 1e-9:
            note += f" {round(hours_left_today, 2)}h left unused (no unfinished subject needed it)."
        self.rationale_log.append(note)


# ---------------------------------------------------------------------------
# 4. Rendering: turn the timetable dict into a readable weekly table
# ---------------------------------------------------------------------------

def render_timetable(agent: StudyPlannerAgent) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("WEEKLY STUDY TIMETABLE")
    lines.append("=" * 60)
    for day, entries in agent.timetable.items():
        lines.append(f"\nDay {day + 1}:")
        if not entries:
            lines.append("  (free day — all subjects on track)")
            continue
        for e in entries:
            lines.append(f"  - {e['subject']:<15} {e['hours']:>4}h   "
                         f"[utility={e['utility_score']}, {e['days_left']}d to deadline]")

    lines.append("\n" + "=" * 60)
    lines.append("COVERAGE SUMMARY")
    lines.append("=" * 60)
    for s in agent.subjects:
        pct = 0 if s.hours_needed == 0 else round(100 * s.hours_done / s.hours_needed, 1)
        status = "DONE" if s.is_complete else f"{pct}% covered"
        lines.append(f"  {s.name:<15} weight={s.weight} difficulty={s.difficulty} "
                     f"deadline=day {s.deadline_days} -> {status}")

    lines.append("\n" + "=" * 60)
    lines.append("AGENT RATIONALE LOG (why each day looks the way it does)")
    lines.append("=" * 60)
    for entry in agent.rationale_log:
        lines.append("  " + entry)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Demo run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    subjects = [
        Subject(name="Maths",   deadline_days=2, difficulty=4, weight=5, hours_needed=6),
        Subject(name="History", deadline_days=6, difficulty=2, weight=2, hours_needed=4),
        Subject(name="Physics", deadline_days=3, difficulty=5, weight=4, hours_needed=8),
        Subject(name="English", deadline_days=5, difficulty=1, weight=3, hours_needed=3),
    ]

    agent = StudyPlannerAgent(subjects=subjects, daily_hours=3, horizon_days=7)
    agent.plan()

    print(render_timetable(agent))
