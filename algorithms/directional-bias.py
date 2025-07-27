from db import (
    get_buy_countdown,
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
    get_position_timestamp_age,
)

from utils.logger import setup_logger

# Configure logging
logger = setup_logger(__name__)

# Constants
BUY_THRESHOLD = 155.0
BUY_COUNTDOWN_THRESHOLD = 150.0
SELL_THRESHOLD = 160.0
SELL_COUNTDOWN_THRESHOLD = 155.0

class DirectionalBiasError(Exception):
    """Base class for directional bias exceptions."""
    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)

    def __str__(self) -> str:
        return f"DirectionalBiasError: {self.message}"

class InvalidThresholdError(DirectionalBiasError):
    """Raised when thresholds are invalid."""
    def __init__(self, message: str, threshold_type: str, value: float, *args: object) -> None:
        self.threshold_type = threshold_type
        self.value = value
        super().__init__(message, *args)

    def __str__(self) -> str:
        return f"InvalidThresholdError: {self.message} (Type: {self.threshold_type}, Value: {self.value})"

class MarketStateError(DirectionalBiasError):
    """Raised when market state is invalid."""
    def __init__(self, message: str, market_ticker: str, *args: object) -> None:
        self.market_ticker = market_ticker
        super().__init__(message, *args)

    def __str__(self) -> str:
        return f"MarketStateError: {self.message} (Ticker: {self.market_ticker})"

def begin_investment_countdown(
    price: float, 
    market_ticker: str
) -> bool:
    """
    Determine whether to start market buy countdown or make immediate purchase.
    
    Args:
        price: Current market price
        market_ticker: Market identifier
    
    Returns:
        bool: True if immediate purchase should be made, False otherwise
    """
    try:
        if price > BUY_THRESHOLD:
            logger.info(f"Creating position for {market_ticker} at price {price}")
            create_position(market_ticker)
            return True
        
        if price > BUY_COUNTDOWN_THRESHOLD:
            logger.info(f"Creating target for {market_ticker} at price {price}")
            create_target(market_ticker)
            return False
        
        return False
    except Exception as e:
        logger.error(f"Error in begin_investment_countdown: {str(e)}")
        raise

def check_investment_countdown(market_ticker: str) -> Optional[int]:
    """
    Decrease buy countdown and update timestamp.
    
    Args:
        market_ticker: Market identifier
    
    Returns:
        Optional[int]: Current countdown value or None if not applicable
    """
    try:
        last_checked = get_target_timestamp_age(market_ticker)
        if last_checked is None:
            logger.debug(f"No timestamp found for {market_ticker}, updating")
            update_target_timestamp(market_ticker)
            return None
        
        decrease_buy_countdown(market_ticker, last_checked)
        update_target_timestamp(market_ticker)
        return get_buy_countdown(market_ticker)
    except Exception as e:
        logger.error(f"Error in check_investment_countdown: {str(e)}")
        raise

def evaluate_buy_target(
    price: float, 
    market_ticker: str
) -> bool:
    """
    Evaluate if investment should be made based on current price and thresholds.
    
    Args:
        price: Current market price
        market_ticker: Market identifier
    
    Returns:
        bool: True if investment should be made, False otherwise
    
    Raises:
        MarketStateError: If market state is invalid
    """
    try:
        if not is_target(market_ticker):
            return begin_investment_countdown(price, market_ticker)
        
        countdown = check_investment_countdown(market_ticker)
        if countdown is None:
            return False
            
        return countdown <= 0
    except Exception as e:
        logger.error(f"Error in evaluate_buy_target: {str(e)}")
        raise

def begin_sell_countdown(
    price: float, 
    market_ticker: str
) -> bool:
    """
    Determine whether to start market sell countdown or make immediate sale.
    
    Args:
        price: Current market price
        market_ticker: Market identifier
    
    Returns:
        bool: True if immediate sale should be made, False otherwise
    """
    try:
        if price < SELL_THRESHOLD:
            logger.info(f"Selling position for {market_ticker} at price {price}")
            return True
        
        if price < SELL_COUNTDOWN_THRESHOLD:
            logger.info(f"Starting sell countdown for {market_ticker} at price {price}")
            start_sell_countdown(market_ticker)
            return False
        
        return False
    except Exception as e:
        logger.error(f"Error in begin_sell_countdown: {str(e)}")
        raise

def check_sell_countdown(market_ticker: str) -> Optional[int]:
    """
    Decrease sell countdown and update timestamp.
    
    Args:
        market_ticker: Market identifier
    
    Returns:
        Optional[int]: Current countdown value or None if not applicable
    """
    try:
        last_checked = get_position_timestamp_age(market_ticker)
        if last_checked is None:
            logger.debug(f"No timestamp found for {market_ticker}, updating")
            update_position_timestamp(market_ticker)
            return None
        
        decrease_sell_countdown(market_ticker, last_checked)
        update_position_timestamp(market_ticker)
        return get_sell_countdown(market_ticker)
    except Exception as e:
        logger.error(f"Error in check_sell_countdown: {str(e)}")
        raise

def evaluate_sell_position(
    price: float, 
    market_ticker: str
) -> bool:
    """
    Evaluate if position should be sold based on current price and thresholds.
    
    Args:
        price: Current market price
        market_ticker: Market identifier
    
    Returns:
        bool: True if position should be sold, False otherwise
    
    Raises:
        MarketStateError: If market state is invalid
    """
    try:
        if not is_position(market_ticker):
            raise MarketStateError("Market ticker is not a position", market_ticker)
        
        countdown = check_sell_countdown(market_ticker)
        if countdown is None:
            return False
            
        return countdown <= 0 or begin_sell_countdown(price, market_ticker)
    except Exception as e:
        logger.error(f"Error in evaluate_sell_position: {str(e)}")
        raise