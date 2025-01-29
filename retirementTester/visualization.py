import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def visualize_results(results_df, depletion_prob, params, best_sim, worst_sim):
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
    
    asset_allocation_str = " / ".join(
        [f"{asset_name}: {asset_info['allocation']:.0%}" for asset_name, asset_info in params['assets'].items()]
    )
    
    ax.set_title(f"Retirement Portfolio Projection ({params['retirement_years']} Years)\n"
                 f"Initial: ${params['initial_portfolio']:,.0f} | "
                 f"Withdrawal: ${params['annual_withdrawal']:,.0f}/yr | "
                 f"Depletion Risk: {depletion_prob:.1%}",
                 pad=20)
    ax.set_xlabel("Years Into Retirement")
    ax.set_ylabel("Portfolio Value")
    ax.yaxis.set_major_formatter(usd_formatter)
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Add statistics box with adjusted position
    stats_text = (
        f"Asset Allocation: {asset_allocation_str}\n"
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
