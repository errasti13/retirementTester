from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
import logging
from .data import fetch_historical_data
from .utils import SimulationParams

logger = logging.getLogger(__name__)

def run_retirement_simulation(
    params: SimulationParams
) -> Tuple[pd.DataFrame, float, List[float], List[float]]:
    """
    Run a Monte Carlo simulation for retirement portfolio analysis.
    
    Args:
        params: SimulationParams object containing simulation parameters.
    
    Returns:
        Tuple containing:
            - DataFrame with simulation results
            - Probability of portfolio depletion
            - Best case simulation history
            - Worst case simulation history
            
    Raises:
        ValueError: If historical data is insufficient or other validation fails.
    """
    try:
        tickers = tuple(asset['ticker'] for asset in params.assets.values())  # Convert to tuple
        returns_data = fetch_historical_data(tickers)
        
        simulations = []
        depletion_count = 0
        best_simulation = None
        worst_simulation = None
        best_final_value = float('-inf')
        worst_final_value = float('inf')

        for _ in range(params.n_simulations):
            portfolio = params.initial_portfolio
            history = []
            depleted = False
            
            max_start = len(returns_data) - params.retirement_years
            if max_start <= 0:
                raise ValueError("Insufficient historical data for simulation period")
            
            start_idx = np.random.randint(0, max_start)
            selected_returns = returns_data.iloc[start_idx:start_idx+params.retirement_years]
            
            for year in range(params.retirement_years):
                if portfolio <= 0:
                    depleted = True
                    break
                
                portfolio -= params.annual_withdrawal

                for _, asset_info in params.assets.items():
                    ticker = asset_info['ticker']
                    allocation = asset_info['allocation']
                    asset_return = selected_returns.iloc[year][ticker]
                    portfolio += portfolio * allocation * asset_return

                history.append(portfolio)
            
            if depleted or portfolio <= 0:
                depletion_count += 1
                history += [0] * (params.retirement_years - len(history))
                
            final_value = history[-1] if history else 0
            if final_value > best_final_value:
                best_final_value = final_value
                best_simulation = history.copy()
            if final_value < worst_final_value:
                worst_final_value = final_value
                worst_simulation = history.copy()
                
            simulations.append(history)

        results_df = pd.DataFrame(simulations)
        return results_df, depletion_count / params.n_simulations, best_simulation, worst_simulation

    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise
