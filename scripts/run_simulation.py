from retirementTester.simulation import *
from retirementTester.visualization import *

def main():
    simulation_params = {
        'initial_portfolio': 1.5e06,
        'annual_withdrawal': 60000,
        'retirement_years': 15,
        'n_simulations': 2000,
        'assets': {
            'American Stocks': {'ticker': '^SP500TR', 'allocation': 0.7},
            'American Bonds': {'ticker': '^FVX', 'allocation': 0},
            'European Stocks': {'ticker': '^STOXX50E', 'allocation': 0.3}
        }
    }

    results, depletion_risk, best_case, worst_case = run_retirement_simulation(simulation_params)

    visualize_results(results, depletion_risk, simulation_params, best_case, worst_case)

if __name__ == "__main__":
    main()
