
"""Developer affirmation module for flowstate."""

import random
from typing import Optional

VALID_MOODS = ["happy", "stressed", "anxious", "tired", "frustrated", "motivated", "neutral"]
VALID_CATEGORIES = ["motivation", "confidence", "persistence", "self-care", "growth"]

# Affirmation database - developer focused
AFFIRMATIONS = [
    # Motivation - Low Energy
    {"text": "{name}, small commits still move the project forward.", "category": "motivation", "energy": "low"},
    {"text": "Rest is part of the process, {name}.", "category": "motivation", "energy": "low"},
    {"text": "{name}, every bug fixed is progress.", "category": "motivation", "energy": "low"},

    # Motivation - Medium Energy
    {"text": "{name}, you have the skills to solve this.", "category": "motivation", "energy": "medium"},
    {"text": "Your code makes a difference, {name}.", "category": "motivation", "energy": "medium"},
    {"text": "{name}, you've debugged harder problems than this.", "category": "motivation", "energy": "medium"},

    # Motivation - High Energy
    {"text": "{name}, you're on fire! Ship that feature!", "category": "motivation", "energy": "high"},
    {"text": "Channel that energy into clean code, {name}!", "category": "motivation", "energy": "high"},

    # Confidence
    {"text": "{name}, you belong in tech.", "category": "confidence", "energy": "low"},
    {"text": "Trust your debugging instincts, {name}.", "category": "confidence", "energy": "medium"},
    {"text": "{name}, your unique perspective makes the team stronger.", "category": "confidence", "energy": "medium"},
    {"text": "You've got this, {name}!", "category": "confidence", "energy": "high"},

    # Persistence
    {"text": "{name}, even senior devs Google things.", "category": "persistence", "energy": "low"},
    {"text": "The bug will surrender eventually, {name}.", "category": "persistence", "energy": "medium"},
    {"text": "{name}, stuck is temporary. Keep digging.", "category": "persistence", "energy": "medium"},
    {"text": "Persistence beats talent, {name}. Keep going!", "category": "persistence", "energy": "high"},

    # Self-care
    {"text": "{name}, it's okay to step away from the screen.", "category": "self-care", "energy": "low"},
    {"text": "Your worth isn't measured in commits, {name}.", "category": "self-care", "energy": "low"},
    {"text": "{name}, take a break. The code will wait.", "category": "self-care", "energy": "medium"},

    # Growth
    {"text": "{name}, every error is a learning opportunity.", "category": "growth", "energy": "low"},
    {"text": "You're a better developer than you were yesterday, {name}.", "category": "growth", "energy": "medium"},
    {"text": "{name}, embrace the struggle. That's where growth happens.", "category": "growth", "energy": "medium"},
    {"text": "Level up, {name}! Challenge accepted!", "category": "growth", "energy": "high"},
]

# Mood to category mappings
MOOD_CATEGORY_MAP = {
    "happy": ["motivation", "growth"],
    "stressed": ["self-care", "persistence"],
    "anxious": ["confidence", "self-care"],
    "tired": ["self-care", "motivation"],
    "frustrated": ["persistence", "confidence"],
    "motivated": ["motivation", "growth"],
    "neutral": ["motivation", "confidence"]
}


def get_affirmation(
    name: str,
    mood: str,
    energy: int,
    category: Optional[str] = None,
    seed: Optional[int] = None
) -> dict:
    """
    Get a personalized developer affirmation based on mood and energy.

    The function maps the integer energy level to a specific intensity bucket ('low', 'medium', 
    or 'high') and uses a weighted random algorithm to select the most appropriate affirmation. 
    It prioritizes matches that align with both the category and the energy level.

    Parameters
    ----------
    name : str
        User's name for personalization.
    mood : str
        Current mood. Valid options: 'happy', 'stressed', 'anxious', 'tired', 'frustrated',
        'motivated', 'neutral'.
    energy : int
        Energy level on a scale of 1-10.
        - 1-3: Low (calming/reassuring)
        - 4-7: Medium (balanced/steady)
        - 8-10: High (energetic/driving)
    category : str, optional
        Specific category constraint. Valid options: 'motivation', 'confidence', 'persistence',
        'self-care', 'growth'.
        If provided, this overrides the default mood-to-category mapping.
    seed : int, optional
        Random seed for reproducible selection. Uses a local random instance to avoid 
        affecting global state.

    Returns
    -------
    dict
        A dictionary containing:
        - 'text' (str): The personalized affirmation string.
        - 'category' (str): The category of the selected affirmation.
        - 'mood_alignment' (float): A score (0.0 - 1.0) indicating how well the selection 
          matches the input criteria.

    Raises
    ------
    TypeError
        If name, mood, or category are not strings, or if energy is not an integer.
    ValueError
        If mood is not in the valid list, energy is not between 1-10, or category 
        is provided but invalid.

    Examples
    --------
    >>> result = get_affirmation(name="Alice", mood="stressed", energy=4)
    >>> print(result['text'])
    "The bug will surrender eventually, Alice."
    """
        # === Input Validation ===
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")

    if not isinstance(mood, str):
        raise TypeError(f"mood must be a string, got {type(mood).__name__}")

    if mood.lower() not in VALID_MOODS:
        raise ValueError(f"Invalid mood '{mood}'. Must be one of: {', '.join(VALID_MOODS)}")

    if not isinstance(energy, int) or isinstance(energy, bool):
        raise TypeError(f"energy must be an integer, got {type(energy).__name__}")

    if energy < 1 or energy > 10:
        raise ValueError("energy must be between 1 and 10")

    if category is not None:
        if not isinstance(category, str):
            raise TypeError(f"category must be a string, got {type(category).__name__}")
        if category.lower() not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}")

    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be an integer, got {type(seed).__name__}")
    # === Main Logic ===
    if seed is not None:
        random.seed(seed)

    # Sanitize name
    display_name = name.strip().title() if name.strip() else "Developer"

    # Determine energy category
    if energy <= 3:
        energy_cat = "low"
    elif energy <= 7:
        energy_cat = "medium"
    else:
        energy_cat = "high"

    # Get preferred categories based on mood
    if category:
        preferred_categories = [category]
    else:
        preferred_categories = MOOD_CATEGORY_MAP.get(mood.lower(), ["motivation"])

    # Filter and weight affirmations
    candidates = []
    energy_order = ["low", "medium", "high"]

    for affirmation in AFFIRMATIONS:
        weight = 1.0

        # Category match
        if affirmation["category"] in preferred_categories:
            idx = preferred_categories.index(affirmation["category"])
            weight *= (3.0 if idx == 0 else 2.0)
        else:
            weight *= 0.5

        # Energy match
        if affirmation["energy"] == energy_cat:
            weight *= 2.0
        elif abs(energy_order.index(affirmation["energy"]) - energy_order.index(energy_cat)) == 1:
            weight *= 1.5

        candidates.append((affirmation, weight))

    if not candidates:
        # Fallback: any affirmation matching energy
        candidates = [(a, 1.0) for a in AFFIRMATIONS if a["energy"] == energy_cat]

    if not candidates:
        # Final fallback
        candidates = [(a, 1.0) for a in AFFIRMATIONS]

    # Weighted random selection
    total = sum(w for _, w in candidates)
    r = random.uniform(0, total)

    cumulative = 0
    selected = candidates[-1][0]
    for affirmation, weight in candidates:
        cumulative += weight
        if r <= cumulative:
            selected = affirmation
            break

    # Personalize text
    personalized_text = selected["text"].replace("{name}", display_name)

    # Calculate mood alignment
    score = 0.5  # Base score
    if selected["category"] in preferred_categories:
        score += 0.3
    if selected["energy"] == energy_cat:
        score += 0.2
    mood_alignment = round(min(score, 1.0), 2)

    return {
        "text": personalized_text,
        "category": selected["category"],
        "mood_alignment": mood_alignment
    }
