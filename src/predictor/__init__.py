"""
Prediction system for CA Fantasy 5.

This module provides a complete prediction pipeline:
- Historical data loading
- Contact-based number analysis (bias-corrected)
- Position-based filtering (EDA-derived optimal ranges)
- Ticket generation with multiple strategies
- Backtesting capabilities

Usage:
    from src.predictor import CA5Predictor

    # Create predictor
    predictor = CA5Predictor(
        matrix_type='proximity',  # or 'weighted'
        capture_level='85',       # or '80', '90'
        lookback_draws=1
    )

    # Generate predictions for tomorrow
    result = predictor.predict(num_tickets=20)
    print(result['tickets'])

    # Backtest on a specific date
    from datetime import datetime
    result = predictor.backtest_single(datetime(2025, 12, 30), num_tickets=20)
    print(f"Best match: {result['best_match']}")
"""

from .data_loader import DrawHistory
from .position_filter import PositionFilter, OPTIMAL_RANGES_85, OPTIMAL_RANGES_90
from .ticket_generator import TicketGenerator
from .predictor import CA5Predictor

__all__ = [
    'DrawHistory',
    'PositionFilter',
    'TicketGenerator',
    'CA5Predictor',
    'OPTIMAL_RANGES_85',
    'OPTIMAL_RANGES_90',
]
