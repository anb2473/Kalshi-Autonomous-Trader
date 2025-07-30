from config import (
    MIN_AGE_THRESHOLD,
    MAX_AGE_THRESHOLD
)

from datetime import utctime as now, timedelta, datetime

def check_market_age(age: int) -> bool:
    """
    Check if the market age meets the minimum threshold.

    Args:
        age (int): The age of the market (in whatever units are expected).

    Returns:
        bool: True if the market age is above or equal to the minimum threshold, False otherwise.
    """
    return age >= MIN_AGE_THRESHOLD

def check_market_timeline(end_date, age):
    if not check_market_age(age): return False

    end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    time_range = now() + timedelta(days=MAX_AGE_THRESHOLD)

    if end_date <= time_range:
        return True
    
    return False
