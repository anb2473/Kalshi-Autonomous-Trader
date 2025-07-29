# Directional Bias Trading Algorithm Overview

The directional bias algorithm is a trading strategy that makes buy/sell decisions based on price thresholds and countdown timers. This approach helps reduce noise in trading decisions by implementing a two-tiered system for both buying and selling.

## Core Concepts

### Price Thresholds

The algorithm uses four key price thresholds:

1. **BUY_THRESHOLD**: The price at which an immediate purchase is made
2. **BUY_COUNTDOWN_THRESHOLD**: The price at which a countdown timer starts for buying
3. **SELL_THRESHOLD**: The price at which an immediate sale is made
4. **SELL_COUNTDOWN_THRESHOLD**: The price at which a countdown timer starts for selling

### Countdown System

The algorithm implements a countdown system to prevent rapid trading and reduce noise:

- When a countdown is active, the algorithm waits for the countdown to expire before making a trade
- This helps prevent overreacting to short-term price movements
- Countdowns are tracked per market ticker

## Trading Flow

### Buying Process

1. When current price > BUY_THRESHOLD:
   - Immediate purchase is made
   - Position is created

2. When current price > BUY_COUNTDOWN_THRESHOLD:
   - Target is created
   - Countdown timer starts
   - When countdown expires and price is still above threshold:
     - Position is created

### Selling Process
1. When current price < SELL_THRESHOLD:
   - Immediate sale is made
   - Position is closed

2. When current price < SELL_COUNTDOWN_THRESHOLD:
   - Sell countdown timer starts
   - When countdown expires and price is still below threshold:
     - Position is sold

## Key Components

### 1. Investment Evaluation

- `evaluate_buy_target`: Determines if a new position should be created
- `evaluate_sell_position`: Determines if an existing position should be closed

### 2. Countdown Management

- `check_investment_countdown`: Manages buy countdown timers
- `check_sell_countdown`: Manages sell countdown timers

### 3. Decision Points

- `begin_investment_countdown`: Starts buy countdown or makes immediate purchase
- `begin_sell_countdown`: Starts sell countdown or makes immediate sale

## Error Handling

The algorithm includes robust error handling:

1. **Threshold Validation**:
   - Ensures thresholds are within valid price ranges
   - Verifies logical relationships between thresholds

2. **Market State Validation**:
   - Checks if market tickers are valid positions or targets
   - Prevents invalid trading operations

3. **Database Operations**:
   - Handles database errors gracefully
   - Maintains transaction consistency
   - Includes proper logging for debugging

## Usage Example

```python
# Example usage of the directional bias algorithm

def main():
    market_ticker = "AAPL"
    current_price = 150.0
    
    # Evaluate buy opportunity
    should_buy = evaluate_buy_target(current_price, market_ticker)
    
    # Evaluate sell opportunity
    should_sell = evaluate_sell_position(current_price, market_ticker)
    
    if should_buy:
        print(f"Creating position for {market_ticker} at price {current_price}")
    elif should_sell:
        print(f"Selling position for {market_ticker} at price {current_price}")
```

## Best Practices

1. **Threshold Configuration**:
   - BUY_THRESHOLD should be higher than BUY_COUNTDOWN_THRESHOLD
   - SELL_THRESHOLD should be lower than SELL_COUNTDOWN_THRESHOLD
   - Adjust thresholds based on market volatility

2. **Monitoring**:
   - Regularly review trading logs
   - Monitor position sizes and exposure
   - Track performance metrics

3. **Risk Management**:
   - Implement position sizing limits
   - Set maximum position exposure
   - Monitor market conditions
