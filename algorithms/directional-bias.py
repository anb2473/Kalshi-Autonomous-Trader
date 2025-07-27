from db import (get_buy_countdown, 
                update_target_timestamp, 
                get_target_timestamp_age, 
                decrease_buy_countdown, 
                decrease_sell_countdown, 
                create_position, 
                is_target, 
                create_target,
                is_position,
                start_sell_countdown,
                get_sell_countdown,
                update_position_timestamp, 
                get_position_timestamp_age, )

# This is a static algorithm that determines whether to buy a target or sell a position based on price thresholds.

# Determine whether market buy countdown should be started, an immediate purchase made, or the market should be disregarded
def begin_investment_countdown(price, immediateBuyThreshold, buyCountdownThreshold, marketTicker):
    if price > immediateBuyThreshold:
        create_position(marketTicker)
        return True
    
    if price > buyCountdownThreshold:
        create_target(marketTicker)
        return False
    
    return False

# Decrease buy countdown and update timestamp
def check_investment_countdown(marketTicker):
    lastChecked = get_target_timestamp_age(marketTicker)
    if lastChecked is None:
        update_target_timestamp(marketTicker)
        return None
    
    decrease_buy_countdown(marketTicker, lastChecked)
    update_target_timestamp(marketTicker)

    return get_buy_countdown(marketTicker)

# Evaluate if the investment should be made based on the current price and thresholds
# Input: market ticker, static price, thresholds
def evaluate_buy_target(price, immediateBuyThreshold, buyCountdownThreshold, marketTicker):    
    if not is_target(marketTicker):
        return begin_investment_countdown(price, immediateBuyThreshold, buyCountdownThreshold, marketTicker)
    
    buyCountdown = check_investment_countdown(marketTicker)

    if buyCountdown is None:
        return False

    if buyCountdown <= 0:
        return True
    
    return False

# Check sell countdown and determine if the position should be sold
def begin_sell_countdown(price, immediateSellThreshold, sellCountdownThreshold, marketTicker):
    if price < immediateSellThreshold:
        return True
    
    if price < sellCountdownThreshold:
        start_sell_countdown(marketTicker)
        return False
    
    return False

def check_sell_countdown(marketTicker):
    # update timestamp for position
    lastChecked = get_position_timestamp_age(marketTicker)
    if lastChecked is None:
        update_position_timestamp(marketTicker)
        return None

    # decrease sell countdown
    
    decrease_sell_countdown(marketTicker, lastChecked)

    sellCountdown = get_sell_countdown(marketTicker)
    
    if sellCountdown is not None:
        update_position_timestamp(marketTicker)
        
        return sellCountdown
    
    return None

# Evaluate if the position should be sold
# Input: market ticker, static price, thresholds
# Throw: ValueError if market ticker is not a position
def evaluate_sell_position(price, immediateSellThreshold, sellCountdownThreshold, marketTicker):
    if not is_position(marketTicker):
        raise ValueError("Market ticker is not a position")
    
    sellCountdown = check_sell_countdown(marketTicker)

    if sellCountdown <= 0:
        return True
    if sellCountdown is None:
        return True
    
    return begin_sell_countdown(price, immediateSellThreshold, sellCountdownThreshold, marketTicker)