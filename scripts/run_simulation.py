from retirementTester.simulation import *
from retirementTester.visualization import *
from retirementTester.utils import setup_simulation_params

def main():

    simulation_params = setup_simulation_params(
        initial_portfolio=1.5e06,
        annual_withdrawal=30000,
        retirement_years=30,
        n_simulations=2000,
        assets= {
        'Global Stocks': 0.7,
        'American Bonds': 0.3
        }
    )

    results, depletion_risk, best_case, worst_case = run_retirement_simulation(simulation_params)

    visualize_results(results, depletion_risk, simulation_params, best_case, worst_case)

if __name__ == "__main__":
    main()
