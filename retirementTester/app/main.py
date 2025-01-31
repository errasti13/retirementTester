import streamlit as st
import logging
from retirementTester.app.pages import home, simulation, results
from retirementTester.app.components.sidebar import sidebar
from retirementTester.app.data_fetcher import initialize_all_assets

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(page_title="Retirement Simulator", layout="wide")
    
    # Initialize data with a spinner
    with st.spinner("Initializing all assets..."):
        logger.debug("Initializing all assets")
        initialize_all_assets()
    
    # Use the new sidebar component
    choice = sidebar()
    
    pages = {
        "Home": home.show,
        "Run Simulation": simulation.show,
        "Results": results.show,
    }
    
    pages[choice]()

if __name__ == "__main__":
    main()
