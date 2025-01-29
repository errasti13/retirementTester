import numpy as np
import pandas as pd
from .data import fetch_historical_data

def run_retirement_simulation(params):
    """
    Run a Monte Carlo simulation for retirement portfolio analysis.
    
    Args:
        params (dict): Dictionary containing simulation parameters
    
    Returns:
        tuple: (simulation results DataFrame, depletion probability, best_simulation, worst_simulation)
    """
    required_keys = ['initial_portfolio', 'asset_allocation', 
                     'annual_withdrawal', 'retirement_years', 'n_simulations']
    if not all(key in params for key in required_keys):
        raise ValueError("Missing required parameters in input dictionary")

    initial_value = params['initial_portfolio']
    allocation = params['asset_allocation']
    withdrawal = params['annual_withdrawal']
    years = params['retirement_years']
    n_sims = params['n_simulations']

    returns_data = fetch_historical_data(['SPY', 'IEF'])
    
    simulations = []
    depletion_count = 0
    best_simulation = None
    worst_simulation = None
    best_final_value = float('-inf')
    worst_final_value = float('inf')

    for _ in range(n_sims):
        portfolio = initial_value
        history = []
        depleted = False
        
        max_start = len(returns_data) - years
        if max_start <= 0:
            raise ValueError("Insufficient historical data for simulation period")
        
        start_idx = np.random.randint(0, max_start)
        selected_returns = returns_data.iloc[start_idx:start_idx+years]
        
        for year in range(years):
            if portfolio <= 0:
                depleted = True
                break
            
            portfolio -= withdrawal

            stock_return = selected_returns.iloc[year]['SPY']
            bond_return = selected_returns.iloc[year]['IEF']
            portfolio *= (allocation['stocks'] * (1 + stock_return) +
                         allocation['bonds'] * (1 + bond_return))

            stock_value = portfolio * allocation['stocks']
            bond_value = portfolio * allocation['bonds']
            portfolio = stock_value + bond_value

            history.append(portfolio)
        
        if depleted or portfolio <= 0:
            depletion_count += 1
            history += [0] * (years - len(history))
            
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
