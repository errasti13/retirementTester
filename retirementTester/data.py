from typing import List, Optional, Dict
import yfinance as yf
import pandas as pd
from functools import lru_cache
import logging
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

class MarketDataConfig:
    """Configuration for market data fetching."""
    DEFAULT_START_DATE: str = '1900-01-01'
    DEFAULT_END_DATE: str = datetime.now().strftime('%Y-%m-%d')
    MIN_YEARS_DATA: int = 30
    CACHE_SIZE: int = 32
    DATE_FORMAT: str = '%Y-%m-%d'

def validate_dates(start_date: str, end_date: str) -> tuple[str, str]:
    """
    Validate and parse date strings.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Tuple of validated start and end dates
        
    Raises:
        ValueError: If dates are invalid or end_date is before start_date
    """
    try:
        start = datetime.strptime(start_date, MarketDataConfig.DATE_FORMAT)
        end = datetime.strptime(end_date, MarketDataConfig.DATE_FORMAT)
        
        if end < start:
            raise ValueError("End date must be after start date")
            
        return start_date, end_date
    except ValueError as e:
        logger.error(f"Date validation failed: {e}")
        raise ValueError(f"Invalid date format. Use {MarketDataConfig.DATE_FORMAT}")

@lru_cache(maxsize=MarketDataConfig.CACHE_SIZE)
def fetch_historical_data(
    tickers: tuple[str, ...],
    start_date: str = MarketDataConfig.DEFAULT_START_DATE,
    end_date: str = MarketDataConfig.DEFAULT_END_DATE
) -> pd.DataFrame:
    """
    Fetch and process historical market data using yfinance.
    
    Args:
        tickers: Tuple of ticker symbols (immutable for caching)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        DataFrame with annual returns for each ticker
        
    Raises:
        RuntimeError: If data fetch fails or processing errors occur
        ValueError: If input validation fails
    """
    logger.info(f"Fetching historical data for tickers: {tickers}")
    
    try:
        # Validate inputs
        if not tickers:
            raise ValueError("No tickers provided")
        start_date, end_date = validate_dates(start_date, end_date)
        
        # Fetch data
        data = yf.download(list(tickers), start=start_date, end=end_date, progress=False)
        if data.empty:
            raise RuntimeError("No data retrieved")
            
        if 'Close' not in data:
            available_cols = data.keys() if isinstance(data, pd.DataFrame) else "No columns"
            raise RuntimeError(f"'Close' prices not found. Available columns: {available_cols}")

        # Process data
        close_prices = data['Close']
        daily_returns = close_prices.pct_change(fill_method=None).dropna()
        annual_returns = daily_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
        
        # Validate output
        if annual_returns.empty:
            raise RuntimeError("No annual returns calculated")
        if annual_returns.isnull().any().any():
            logger.warning("NaN values present in annual returns")
            
        # Ensure minimum years of data
        if len(annual_returns) < MarketDataConfig.MIN_YEARS_DATA:
            logger.warning(f"Less than {MarketDataConfig.MIN_YEARS_DATA} years of data available")
            
        logger.info(f"Successfully processed data for {len(tickers)} tickers")
        return annual_returns

    except Exception as e:
        logger.error(f"Failed to fetch historical data: {str(e)}")
        raise RuntimeError(f"Failed to fetch historical data: {str(e)}")
