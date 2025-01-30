import streamlit as st
from retirementTester.app.components.input_form import simulation_form

def show():
    st.title("Run a Retirement Simulation")
    simulation_form()
