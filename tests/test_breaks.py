import pytest
from deepwork.breaks import suggest_break


class TestSuggestBreakBasic:
    """Basic functionality tests for suggest_break."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = suggest_break(minutes_worked=60, energy_level=5)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        """Test that result dict has required keys."""
        result = suggest_break(minutes_worked=60, energy_level=5)
        assert "name" in result
        assert "description" in result
        assert "duration_minutes" in result
        assert "category" in result
        assert "energy_required" in result
        assert "location" in result

    def test_active_break_type(self):
        """Test that active break type returns active activity."""
        result = suggest_break(minutes_worked=60, energy_level=5, break_type="active")
        assert result["category"] == "active"

    def test_seed_reproducibility(self):
        """Test that same seed produces same result."""
        result1 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
        result2 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
        assert result1["name"] == result2["name"]

    def test_minutes_worked_negative_raises_value_error(self):
        """Test that minutes worked is not a negative number."""
        with pytest.raises(ValueError, match="minutes_worked cannot be negative"):
            suggest_break(minutes_worked=-5, energy_level=5)

    def test_empty_break_type_raises_value_error(self):
        """Test that break type is not an empty string."""
        with pytest.raises(ValueError, match="Invalid break_type"):
            suggest_break(60, 5, break_type="")
