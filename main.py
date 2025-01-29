import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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
        # Download historical data
        data = yf.download(tickers, start=start_date, end=end_date)
        
        # Use 'Close' prices instead of 'Adj Close'
        if 'Close' not in data:
            raise RuntimeError(f"'Close' prices not found in the downloaded data. Available columns: {data.keys()}")
        
        # Extract the 'Close' prices for each ticker
        close_prices = data['Close']
        
        # Calculate daily returns
        daily_returns = close_prices.pct_change().dropna()
        
        # Resample to annual returns
        annual_returns = daily_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
        return annual_returns
    except Exception as e:
        raise RuntimeError(f"Failed to fetch historical data: {str(e)}")


def run_retirement_simulation(params):
    """
    Main simulation engine for retirement portfolio analysis
    
    Args:
        params (dict): Dictionary containing simulation parameters
    
    Returns:
        tuple: (simulation results DataFrame, depletion probability)
    """
    # Validate parameters
    required_keys = ['initial_portfolio', 'asset_allocation', 
                    'annual_withdrawal', 'retirement_years', 'n_simulations']
    if not all(key in params for key in required_keys):
        raise ValueError("Missing required parameters in input dictionary")
    
    # Extract parameters
    initial_value = params['initial_portfolio']
    allocation = params['asset_allocation']
    withdrawal = params['annual_withdrawal']
    years = params['retirement_years']
    n_sims = params['n_simulations']
    
    # Get historical market data
    returns_data = fetch_historical_data(['SPY', 'IEF'])
    
    # Storage for results
    simulations = []
    depletion_count = 0
    best_simulation = None
    worst_simulation = None
    best_final_value = float('-inf')
    worst_final_value = float('inf')
    
    # Main simulation loop
    for _ in range(n_sims):
        portfolio = initial_value
        history = []
        depleted = False
        
        # Randomly select historical period
        max_start = len(returns_data) - years
        if max_start <= 0:
            raise ValueError("Insufficient historical data for simulation period")
        start_idx = np.random.randint(0, max_start)
        selected_returns = returns_data.iloc[start_idx:start_idx+years]
        
        # Annual simulation loop
        for year in range(years):
            if portfolio <= 0:
                depleted = True
                break
                
            # Withdraw funds at start of year
            portfolio -= withdrawal
            
            # Apply market returns
            stock_return = selected_returns.iloc[year]['SPY']
            bond_return = selected_returns.iloc[year]['IEF']
            portfolio *= (allocation['stocks'] * (1 + stock_return) +
                         allocation['bonds'] * (1 + bond_return))
            
            # Rebalance portfolio
            stock_value = portfolio * allocation['stocks']
            bond_value = portfolio * allocation['bonds']
            portfolio = stock_value + bond_value
            
            history.append(portfolio)
        
        # Track depletion events
        if depleted or portfolio <= 0:
            depletion_count += 1
            history += [0] * (years - len(history))
            
        # Track best and worst scenarios
        final_value = history[-1] if history else 0
        if final_value > best_final_value:
            best_final_value = final_value
            best_simulation = history.copy()
        if final_value < worst_final_value:
            worst_final_value = final_value
            worst_simulation = history.copy()
            
        simulations.append(history)
    
    results_df = pd.DataFrame(simulations)
    return results_df, depletion_count / n_sims, best_simulation, worst_simulation

def visualize_results(results_df, depletion_prob, params, best_sim, worst_sim):
    """
    Generate professional visualizations of simulation results
    
    Args:
        results_df (pd.DataFrame): Simulation results from run_retirement_simulation
        depletion_prob (float): Probability of portfolio depletion
        params (dict): Original simulation parameters
    """
    plt.style.use('seaborn-v0_8')

    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate percentiles
    percentiles = results_df.quantile([0.05, 0.25, 0.5, 0.75, 0.95], axis=0).T
    percentiles.columns = ['5th', '25th', 'Median', '75th', '95th']
    
    # Create custom formatters
    usd_formatter = FuncFormatter(lambda x, _: f'${x:,.0f}')
    year_formatter = FuncFormatter(lambda x, _: f'{int(x)}')
    
    # Plot confidence bands
    ax.fill_between(percentiles.index, percentiles['5th'], percentiles['95th'],
                   alpha=0.15, color='blue', label='90% Confidence Band')
    ax.fill_between(percentiles.index, percentiles['25th'], percentiles['75th'],
                   alpha=0.3, color='green', label='50% Confidence Band')
    
    # Plot median line
    ax.plot(percentiles['Median'], color='black', linewidth=2, label='Median Path')
    
    # Plot best and worst cases
    ax.plot(worst_sim, color='red', linewidth=2, linestyle=':', 
            label='Worst Case')
    ax.plot(best_sim, color='green', linewidth=2, linestyle=':', 
            label='Best Case')
    
    # Formatting
    ax.set_title(
        f"Retirement Portfolio Projection ({params['retirement_years']} Years)\n"
        f"Initial: ${params['initial_portfolio']:,.0f} | "
        f"Withdrawal: ${params['annual_withdrawal']:,.0f}/yr | "
        f"Depletion Risk: {depletion_prob:.1%}",
        pad=20
    )
    ax.set_xlabel("Years Into Retirement")
    ax.set_ylabel("Portfolio Value")
    ax.yaxis.set_major_formatter(usd_formatter)
    ax.xaxis.set_major_formatter(year_formatter)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add statistics box with adjusted position
    stats_text = (
        f"Asset Allocation: {params['asset_allocation']['stocks']:.0%} Stocks / "
        f"{params['asset_allocation']['bonds']:.0%} Bonds\n"
        f"Simulations Run: {params['n_simulations']:,}\n"
        f"Final Value Ranges:\n"
        f"- Best Case: ${best_sim[-1]:,.0f}\n"
        f"- Median: ${results_df.iloc[:,-1].median():,.0f}\n"
        f"- Worst Case: ${worst_sim[-1]:,.0f}"
    )
    ax.annotate(stats_text, xy=(0.95, 0.05), xycoords='axes fraction',  # Changed y from 0.55 to 0.25
               ha='right', va='bottom', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Simulation parameters
    simulation_params = {
        'initial_portfolio': 1.5e06,
        'asset_allocation': {'stocks': 1, 'bonds': 0},
        'annual_withdrawal': 60000,
        'retirement_years': 10,
        'n_simulations': 2000
    }
    
    # Run simulation with updated return values
    results, depletion_risk, best_case, worst_case = run_retirement_simulation(simulation_params)
    
    # Display results
    print(f"\nSimulation Results for {simulation_params['retirement_years']} Year Retirement")
    print(f"Probability of Depletion: {depletion_risk:.1%}")
    print(f"Best Case Final Value: ${best_case[-1]:,.0f}")
    print(f"Median Final Value: ${results.iloc[:,-1].median():,.0f}")
    print(f"Worst Case Final Value: ${worst_case[-1]:,.0f}")
    
    # Generate visualization with best/worst cases
    visualize_results(results, depletion_risk, simulation_params, best_case, worst_case)