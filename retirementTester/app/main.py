import streamlit as st
from retirementTester.app.pages import home, simulation, results
from retirementTester.app.components.sidebar import sidebar

def main():
    st.set_page_config(page_title="Retirement Simulator", layout="wide")
    sidebar()

    pages = {
        "Home": home.show,
        "Run Simulation": simulation.show,
        "Results": results.show,
    }

    choice = st.sidebar.radio("Navigation", list(pages.keys()))
    pages[choice]()

if __name__ == "__main__":
    main()
