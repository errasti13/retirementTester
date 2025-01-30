import streamlit as st
from retirementTester.app.components.results_display import show_results

def show():
    st.title("Simulation Results")
    show_results()
