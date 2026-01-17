"""Task prioritization function for deepwork."""

import pandas as pd
from datetime import datetime, date
from typing import Optional

VALID_METHODS = ["weighted", "deadline"]

def prioritize_tasks(
    tasks: list[dict],
    method: str = "weighted",
    weights: Optional[dict] = None
) -> pd.DataFrame:
    """
    Rank tasks by priority using different prioritization methods.

    Parameters
    ----------
    tasks : list of dict
        List of task dictionaries. Each task should have:
        - 'name' : str (required)
        - 'deadline' : str, optional (format: 'YYYY-MM-DD'). Tasks without 
        deadlines receive a default middle urgency score.
        - 'effort' : int, optional (1-5 scale, where 1 = low effort, 5 = high effort).
          Lower effort tasks are prioritized higher. Default is 3.
        - 'importance' : int, optional (1-5 scale, where 5 = most important).
          Default is 3.
    method : str, optional
        Prioritization method: 'weighted' or 'deadline'.
        Default is 'weighted'.
    weights : dict, optional
        Custom weights for 'weighted' method. Keys: 'importance', 'effort', 'deadline'.
        Default is {'importance': 0.5, 'effort': 0.3, 'deadline': 0.2}.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: name, priority_score, rank, and original task fields.

    Raises
    ------
    TypeError
        If tasks is not a list or contains non-dict items.
    ValueError
        If tasks is empty, method is invalid, or required fields are missing.

    Examples
    --------
    >>> tasks = [
    ...     {"name": "Fix bug", "importance": 5, "effort": 2},
    ...     {"name": "Write docs", "importance": 3, "effort": 4}
    ... ]
    >>> result = prioritize_tasks(tasks, method="weighted")
    """
    if not isinstance(tasks, list):
        raise TypeError(f"tasks must be a list, got {type(tasks).__name__}")

    if len(tasks) == 0:
        raise ValueError("tasks list cannot be empty")

    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise TypeError(f"Task at index {i} must be a dict, got {type(task).__name__}")
        if "name" not in task:
            raise ValueError(f"Task at index {i} missing required field 'name'")

    if method not in VALID_METHODS:
        raise ValueError(f"Invalid method '{method}'. Must be one of: {', '.join(VALID_METHODS)}")

    if weights is not None and not isinstance(weights, dict):
        raise TypeError(f"weights must be a dict, got {type(weights).__name__}")

    # Set default weights
    if weights is None:
        weights = {"importance": 0.5, "effort": 0.3, "deadline": 0.2}

    today = date.today()
    scored_tasks = []

    # Calculate priority scores
    if method == "weighted":
        w_imp = weights.get("importance", 0.5)
        w_eff = weights.get("effort", 0.3)
        w_dead = weights.get("deadline", 0.2)

        for task in tasks:
            importance = task.get("importance", 3)
            effort = task.get("effort", 3)

            # Deadline urgency (days until deadline, normalized)
            deadline_score = 3  # default middle score
            if "deadline" in task and task["deadline"]:
                try:
                    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                    days_left = (deadline - today).days
                    if days_left <= 1:
                        deadline_score = 5
                    elif days_left <= 3:
                        deadline_score = 4
                    elif days_left <= 7:
                        deadline_score = 3
                    elif days_left <= 14:
                        deadline_score = 2
                    else:
                        deadline_score = 1
                except ValueError:
                    pass

            # Lower effort = higher priority (invert effort score)
            effort_score = 6 - effort

            score = (importance * w_imp) + (effort_score * w_eff) + (deadline_score * w_dead)

            scored_tasks.append({
                **task,
                "priority_score": round(score, 2)
            })

    elif method == "deadline":
        for task in tasks:
            days_left = None
            if "deadline" in task and task["deadline"]:
                try:
                    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                    days_left = (deadline - today).days
                    # Higher score for closer deadlines (invert days)
                    score = max(0, 100 - days_left)
                except ValueError:
                    score = 0
            else:
                score = 0  # No deadline = lowest priority

            scored_tasks.append({
                **task,
                "priority_score": score,
                "days_until_deadline": days_left if "deadline" in task else None
            })

    # Sort by priority score (descending) and assign ranks
    scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
    for i, task in enumerate(scored_tasks):
        task["rank"] = i + 1

    return pd.DataFrame(scored_tasks)
