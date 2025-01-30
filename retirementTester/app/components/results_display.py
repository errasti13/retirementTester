import streamlit as st
from retirementTester.app.visualization import visualize_results

def show_results():
    if "results" in st.session_state:
        results, depletion_risk, best_case, worst_case = st.session_state["results"]
        
        st.write(f"**Depletion Risk:** {depletion_risk:.2%}")
        st.write(f"**Best Case Scenario (Final Value):** ${best_case[-1]:,.2f}")
        st.write(f"**Worst Case Scenario (Final Value):** ${worst_case[-1]:,.2f}")
        
        params = st.session_state.get("params")
        visualize_results(results, depletion_risk, params, best_case, worst_case)
    else:
        st.warning("No results to display. Please run a simulation first.")


