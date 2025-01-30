import streamlit as st
from retirementTester.app.simulation import run_retirement_simulation
from retirementTester.app.utils import setup_simulation_params

def simulation_form():
    initial_portfolio = st.number_input("Initial Portfolio ($)", value=1.5e6)
    annual_withdrawal = st.number_input("Annual Withdrawal ($)", value=30000)
    retirement_years = st.number_input("Retirement Duration (years)", value=30)
    n_simulations = 1000  # Set number of simulations to 1000 internally

    assets = {
        "Global Stocks": st.slider("Global Stocks (%)", 0, 100, 70) / 100,
        "American Bonds": st.slider("American Bonds (%)", 0, 100, 30) / 100
    }

    if st.button("Run Simulation"):
        params = setup_simulation_params(initial_portfolio, annual_withdrawal, retirement_years, n_simulations, assets)
        results, depletion_risk, best_case, worst_case = run_retirement_simulation(params)
        st.session_state["params"] = params  # Store params in session state
        st.session_state["results"] = (results, depletion_risk, best_case, worst_case)
        st.success("Simulation Complete! Go to the 'Results' tab.")
