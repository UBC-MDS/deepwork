"""Tests for plan_pomodoro function."""

import pytest
import pandas as pd
from deepwork.pomodoro import plan_pomodoro


class TestPlanPomodoroBasic:
    """Basic functionality tests for plan_pomodoro."""

    def test_returns_dataframe(self):
        """Test that function returns a pandas DataFrame."""
        result = plan_pomodoro(total_minutes=60)
        assert isinstance(result, pd.DataFrame)

    def test_has_required_columns(self):
        """Test that result DataFrame has required columns."""
        result = plan_pomodoro(total_minutes=60)
        assert "session" in result.columns
        assert "type" in result.columns
        assert "duration_minutes" in result.columns
        assert "start_minute" in result.columns
        assert "end_minute" in result.columns

    def test_pomodoro_technique_25_5(self):
        """Test default pomodoro technique creates 25-min work sessions."""
        result = plan_pomodoro(total_minutes=60, technique="pomodoro")
        work_sessions = result[result["type"] == "work"]
        assert work_sessions.iloc[0]["duration_minutes"] == 25

    def test_schedule_starts_at_zero(self):
        """Test that schedule starts at minute 0."""
        result = plan_pomodoro(total_minutes=60)
        assert result.iloc[0]["start_minute"] == 0