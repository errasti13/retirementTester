import streamlit as st
from retirementTester.app.data_fetcher import get_data_start_date

def is_data_fetched():
    return 'data_fetched' in st.session_state and st.session_state.data_fetched

def sidebar():
    st.sidebar.title("Navigation")
    
    # Show data availability info
    start_year_placeholder = st.sidebar.empty()
    
    if 'data_fetched' in st.session_state and st.session_state.data_fetched:
        start_year = get_data_start_date()
        start_year_placeholder.caption(f"📊 Historical data from: {start_year}")
    else:
        start_year_placeholder.caption("📊 Historical data: Loading...")
    
    return st.sidebar.radio("", ["Home", "Run Simulation", "Results"])
