"""Pomodoro session planning function for deepwork."""

from typing import Optional
import pandas as pd

def plan_pomodoro(
    total_minutes: int,
    technique: str = "pomodoro",
    work_length: Optional[int] = None,
    short_break: Optional[int] = None,
    long_break: Optional[int] = None,
    long_break_interval: int = 4
) -> pd.DataFrame:
    """
    Calculate a Pomodoro-style work/break schedule within a fixed time budget.

    The schedule always starts with a work session at minute 0 and alternates
    work and break sessions until `total_minutes` is reached. If there is not
    enough time remaining for a full next session, the final session is
    **truncated** to fit exactly within `total_minutes`. Zero-length sessions
    are never included.

    Technique presets set the default work/break lengths:
    - "pomodoro": 25 work, 5 short break
    - "52-17": 52 work, 17 short break
    - "90-20": 90 work, 20 short break
    - "custom": user-specified lengths via `work_length` and `short_break`

    Long breaks: after every `long_break_interval`-th work session, the next break
    is a long break (type "long_break") with duration `long_break` (or
    `short_break` if `long_break` is not provided). Otherwise breaks are short
    (type "short_break"). Long-break settings apply for all techniques.

    Parameters
    ----------
    total_minutes : int
        Total available time in minutes. Must be > 0.
    technique : str, optional
        Preset name: "pomodoro", "52-17", "90-20", or "custom". Default "pomodoro".
    work_length : int, optional
        Work period length in minutes. Required if technique="custom".
    short_break : int, optional
        Short break length in minutes. Required if technique="custom".
    long_break : int, optional
        Long break length in minutes. If None, defaults to `short_break`.
    long_break_interval : int, optional
        Number of work sessions between long breaks. Must be >= 1. Default 4.

    Returns
    -------
    pd.DataFrame
        Schedule with one row per session, in chronological order, with columns:

        - session : int
            1-based sequential session number.
        - type : str
            One of {"work", "short_break", "long_break"}.
        - duration_minutes : int
            Session length in minutes (may be shorter than the preset/parameter
            value only for the final truncated session).
        - start_minute : int
            Inclusive start minute from 0.
        - end_minute : int
            Exclusive end minute; equals start_minute + duration_minutes and
            never exceeds `total_minutes`.

    Raises
    ------
    TypeError
        If any numeric parameter is not an integer (bool is not accepted).
    ValueError
        If `total_minutes` <= 0; if `technique` is invalid; if technique="custom"
        and required parameters are missing; or if any provided duration is <= 0
        or `long_break_interval` < 1.

    Examples
    --------
    >>> schedule = plan_pomodoro(total_minutes=120, technique="pomodoro")
    >>> schedule = plan_pomodoro(total_minutes=60, technique="custom", work_length=20, short_break=5)
    >>> schedule = plan_pomodoro(total_minutes=10, technique="pomodoro")  # final work session truncated to 10
    """

