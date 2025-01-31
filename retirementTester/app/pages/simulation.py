import streamlit as st
from retirementTester.app.components.input_form import simulation_form  # Use absolute import

def show():
    st.title("Run a Retirement Simulation")
    simulation_form()
