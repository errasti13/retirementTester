from retirementTester.simulation import *
from retirementTester.visualization import *

def main():
    simulation_params = {
        'initial_portfolio': 1.5e06,
        'asset_allocation': {'stocks': 1, 'bonds': 0},
        'annual_withdrawal': 60000,
        'retirement_years': 62,
        'n_simulations': 2000,
        'tickers': ['^GSPC', '^FVX', '^TNX']
    }

    results, depletion_risk, best_case, worst_case = run_retirement_simulation(simulation_params)

    visualize_results(results, depletion_risk, simulation_params, best_case, worst_case)

if __name__ == "__main__":
    main()
