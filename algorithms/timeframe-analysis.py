from config import (
    MIN_AGE_THRESHOLD
)

def check_market_age(age: int) -> bool:
    """
    Check if the market age meets the minimum threshold.

    Args:
        age (int): The age of the market (in whatever units are expected).

    Returns:
        bool: True if the market age is above or equal to the minimum threshold, False otherwise.
    """
    return age >= MIN_AGE_THRESHOLD