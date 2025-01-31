import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import List
import pandas as pd
import streamlit as st
from .utils import SimulationParams

def visualize_results(
    results_df: pd.DataFrame, 
    depletion_prob: float, 
    params: SimulationParams, 
    best_sim: List[float], 
    worst_sim: List[float]
) -> None:
    """
    Generate professional visualizations of simulation results.
    """
    plt.style.use('seaborn-v0_8')

    fig, ax = plt.subplots(figsize=(12, 7))
    
    percentiles = results_df.quantile([0.05, 0.25, 0.5, 0.75, 0.95], axis=0).T
    percentiles.columns = ['5th', '25th', 'Median', '75th', '95th']

    usd_formatter = FuncFormatter(lambda x, _: f'${x:,.0f}')
    
    ax.fill_between(percentiles.index, percentiles['5th'], percentiles['95th'], alpha=0.15, color='blue', label='90% Confidence Band')
    ax.fill_between(percentiles.index, percentiles['25th'], percentiles['75th'], alpha=0.3, color='green', label='50% Confidence Band')
    
    ax.plot(percentiles['Median'], color='black', linewidth=2, label='Median Path')
    ax.plot(worst_sim, color='red', linewidth=2, linestyle=':', label='Worst Case')
    ax.plot(best_sim, color='green', linewidth=2, linestyle=':', label='Best Case')
    
    title = "Retirement Portfolio Projection"
    if params is not None:
        title += f" ({params.retirement_years} Years)\n"
        title += f"Initial: ${params.initial_portfolio:,.0f} | "
        title += f"Withdrawal: ${params.annual_withdrawal:,.0f}/yr | "
        
        if hasattr(params, 'assets'):
            asset_allocation_str = " / ".join(
                [f"{asset_name}: {asset_info['allocation']:.0%}" 
                for asset_name, asset_info in params.assets.items()]
            )
            title += f"\n{asset_allocation_str}"
    
    title += f"\nDepletion Risk: {depletion_prob:.1%}"
    ax.set_title(title, pad=20)
    
    ax.set_xlabel("Years Into Retirement")
    ax.set_ylabel("Portfolio Value")
    ax.yaxis.set_major_formatter(usd_formatter)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    st.pyplot(fig)
