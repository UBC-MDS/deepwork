
"""Affirmation function for deepwork."""

from typing import Optional

def get_affirmation(
    name: str,
    mood: str,
    energy: int,
    category: Optional[str] = None,
    seed: Optional[int] = None
) -> dict:
    """
    Get a personalized developer affirmation using weighted selection based on mood and energy.

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