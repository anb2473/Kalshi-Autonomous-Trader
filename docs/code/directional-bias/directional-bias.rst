==================
Directional Bias Module
==================

.. automodule:: algorithms.directional-bias
   :members:
   :undoc-members:
   :show-inheritance:

------------------
Module Overview
------------------

The directional-bias module provides algorithms for making trading decisions based on price thresholds and countdown timers. It includes functionality for both buying and selling positions in the market.

------------------
Constants
------------------

.. data:: BUY_THRESHOLD

   The price threshold for immediate purchase

.. data:: BUY_COUNTDOWN_THRESHOLD

   The price threshold for starting a buy countdown

.. data:: SELL_THRESHOLD

   The price threshold for immediate sale

.. data:: SELL_COUNTDOWN_THRESHOLD

   The price threshold for starting a sell countdown

------------------
Exception Classes
------------------

.. autoclass:: DirectionalBiasError
   :members:

.. autoclass:: InvalidThresholdError
   :members:

.. autoclass:: MarketStateError
   :members:

------------------
Function Reference
------------------

.. autofunction:: begin_investment_countdown

.. autofunction:: check_investment_countdown

.. autofunction:: evaluate_buy_target

.. autofunction:: begin_sell_countdown

.. autofunction:: check_sell_countdown

.. autofunction:: evaluate_sell_position

------------------
Detailed Function Descriptions
------------------

begin_investment_countdown
=========================

.. function:: begin_investment_countdown(price: float, market_ticker: str) -> bool

   Determine whether to start market buy countdown or make immediate purchase.
   
   :param price: Current market price
   :type price: float
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: True if immediate purchase should be made, False otherwise
   :rtype: bool
   :raises: InvalidThresholdError if thresholds are invalid

check_investment_countdown
=========================

.. function:: check_investment_countdown(market_ticker: str) -> Optional[int]

   Decrease buy countdown and update timestamp.
   
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: Current countdown value or None if not applicable
   :rtype: Optional[int]
   :raises: Exception for any database operation failures

evaluate_buy_target
==================

.. function:: evaluate_buy_target(price: float, market_ticker: str) -> bool

   Evaluate if investment should be made based on current price and thresholds.
   
   :param price: Current market price
   :type price: float
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: True if investment should be made, False otherwise
   :rtype: bool
   :raises: MarketStateError if market state is invalid

begin_sell_countdown
==================

.. function:: begin_sell_countdown(price: float, market_ticker: str) -> bool

   Determine whether to start market sell countdown or make immediate sale.
   
   :param price: Current market price
   :type price: float
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: True if immediate sale should be made, False otherwise
   :rtype: bool
   :raises: InvalidThresholdError if thresholds are invalid

check_sell_countdown
==================

.. function:: check_sell_countdown(market_ticker: str) -> Optional[int]

   Decrease sell countdown and update timestamp.
   
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: Current countdown value or None if not applicable
   :rtype: Optional[int]
   :raises: Exception for any database operation failures

evaluate_sell_position
=====================

.. function:: evaluate_sell_position(price: float, market_ticker: str) -> bool

   Evaluate if position should be sold based on current price and thresholds.
   
   :param price: Current market price
   :type price: float
   :param market_ticker: Market identifier
   :type market_ticker: str
   :return: True if position should be sold, False otherwise
   :rtype: bool
   :raises: MarketStateError if market state is invalid
