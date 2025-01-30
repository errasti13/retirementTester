import streamlit as st
from retirementTester.simulation import run_retirement_simulation
from retirementTester.utils import setup_simulation_params

# Set the title of the app
st.title("Retirement Portfolio Simulator")

# User Inputs
initial_portfolio = st.number_input("Initial Portfolio ($)", min_value=0, value=1500000, step=10000)
annual_withdrawal = st.number_input("Annual Withdrawal ($)", min_value=0, value=30000, step=1000)
retirement_years = st.slider("Retirement Years", min_value=1, max_value=50, value=30)
n_simulations = st.slider("Number of Simulations", min_value=100, max_value=5000, value=2000, step=100)

# Asset allocation input
st.subheader("Asset Allocation")
global_stocks = st.slider("Global Stocks (%)", min_value=0, max_value=100, value=70)
american_bonds = st.slider("American Bonds (%)", min_value=0, max_value=100, value=30)

# Ensure total allocation is 100%
if global_stocks + american_bonds != 100:
    st.error("Total asset allocation must sum to 100%")
else:
    # Run Simulation
    if st.button("Run Simulation"):
        assets = {"Global Stocks": global_stocks / 100, "American Bonds": american_bonds / 100}
        params = setup_simulation_params(
            initial_portfolio=initial_portfolio,
            annual_withdrawal=annual_withdrawal,
            retirement_years=retirement_years,
            n_simulations=n_simulations,
            assets=assets
        )

        # Run retirement simulation
        results, depletion_risk, best_case, worst_case = run_retirement_simulation(params)

        # Display results
        st.write(f"**Depletion Risk:** {depletion_risk:.2%}")
        
        # Plot results
        st.subheader("Portfolio Growth Over Time")
        st.line_chart(results.T)  # Transpose to match Streamlit's format
