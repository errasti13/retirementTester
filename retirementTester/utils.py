# Dictionary mapping asset names to ticker symbols
ASSET_TICKERS = {
    'Global Stocks': '^990100-USD-STRD',
    'American Bonds': '^FVX',
    'American Stocks': '^SP500TR',
    'European Stocks': '^STOXX50E',
    # Add more assets as needed
}

def convert_assets_to_tickers(assets):
    """
    Convert asset names to tickers using the ASSET_TICKERS dictionary.
    
    Args:
        assets (dict): Dictionary of asset names and their allocations
    
    Returns:
        dict: Dictionary of assets with tickers and allocations
    """
    return {
        asset_name: {'ticker': ASSET_TICKERS[asset_name], 'allocation': allocation}
        for asset_name, allocation in assets.items()
    }

def setup_simulation_params(initial_portfolio, annual_withdrawal, retirement_years, n_simulations, assets):
    """
    Set up the simulation parameters.
    
    Args:
        initial_portfolio (float): Initial portfolio value
        annual_withdrawal (float): Annual withdrawal amount
        retirement_years (int): Number of retirement years
        n_simulations (int): Number of simulations
        assets (dict): Dictionary of asset names and their allocations
    
    Returns:
        dict: Dictionary of simulation parameters
    """
    return {
        'initial_portfolio': initial_portfolio,
        'annual_withdrawal': annual_withdrawal,
        'retirement_years': retirement_years,
        'n_simulations': n_simulations,
        'assets': convert_assets_to_tickers(assets)
    }
