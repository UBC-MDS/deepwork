"""Tests for get_affirmation function."""

import pytest
from deepwork.affirmation import get_affirmation


class TestGetAffirmationBasic:
    """Basic functionality tests for get_affirmation."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = get_affirmation(name="Alice", mood="happy", energy=5)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        """Test that result dict has required keys."""
        result = get_affirmation(name="Alice", mood="happy", energy=5)
        assert "text" in result
        assert "category" in result
        assert "mood_alignment" in result

    def test_name_in_text(self):
        """Test that name appears in affirmation text."""
        result = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        assert "Alice" in result["text"]

    def test_seed_reproducibility(self):
        """Test that same seed produces same result."""
        result1 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        result2 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        assert result1["text"] == result2["text"]

class TestGetAffirmationMoods:
    """Tests for different mood types."""

    def test_stressed_mood_prefers_selfcare(self):
        categories = []
        for seed in range(20):
            result = get_affirmation(name="Test", mood="stressed", energy=5, seed=seed)
            categories.append(result["category"])
        assert "self-care" in categories or "persistence" in categories

    def test_specific_category_override(self):
        result = get_affirmation(name="Test", mood="stressed", energy=5, category="growth", seed=42)
        assert result["category"] == "growth"


class TestGetAffirmationEdgeCases:
    """Edge case tests for get_affirmation."""

    def test_empty_name_uses_default(self):
        result = get_affirmation(name="   ", mood="happy", energy=5, seed=42)
        assert "Developer" in result["text"]

    def test_name_capitalization(self):
        result = get_affirmation(name="alice", mood="happy", energy=5, seed=42)
        assert "Alice" in result["text"]


class TestGetAffirmationExceptions:
    """Exception handling tests for get_affirmation."""

    def test_name_not_string_raises_typeerror(self):
        with pytest.raises(TypeError, match="name must be a string"):
            get_affirmation(name=123, mood="happy", energy=5)

    def test_energy_not_int_raises_typeerror(self):
        with pytest.raises(TypeError, match="energy must be an integer"):
            get_affirmation(name="Alice", mood="happy", energy="5")

    def test_invalid_mood_raises_valueerror(self):
        with pytest.raises(ValueError, match="Invalid mood"):
            get_affirmation(name="Alice", mood="invalid", energy=5)

    def test_energy_out_of_range_raises_valueerror(self):
        with pytest.raises(ValueError, match="must be between 1 and 10"):
            get_affirmation(name="Alice", mood="happy", energy=0)

    def test_invalid_category_raises_valueerror(self):
        with pytest.raises(ValueError, match="Invalid category"):
            get_affirmation(name="Alice", mood="happy", energy=5, category="invalid")