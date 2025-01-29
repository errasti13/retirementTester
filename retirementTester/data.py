import yfinance as yf
import pandas as pd

def fetch_historical_data(tickers, start_date='1980-01-01', end_date='2023-12-31'):
    """
    Fetch historical market data using yfinance
    Returns annual returns for specified tickers
    
    Args:
        tickers (list): List of ticker symbols (e.g., ['SPY', 'IEF'])
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    
    Returns:
        pd.DataFrame: DataFrame with annual returns for each ticker
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date)
        
        if 'Close' not in data:
            raise RuntimeError(f"'Close' prices not found. Available columns: {data.keys()}")

        close_prices = data['Close']
        daily_returns = close_prices.pct_change().dropna()
        annual_returns = daily_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)

        return annual_returns
    except Exception as e:
        raise RuntimeError(f"Failed to fetch historical data: {str(e)}")
