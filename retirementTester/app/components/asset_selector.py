import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from retirementTester.app.utils import SimulationConfig

__all__ = ['asset_allocation_selector']

def create_allocation_pie_chart(allocations: dict):
    """Create a pie chart using matplotlib."""
    fig, ax = plt.subplots(figsize=(6, 6))
    values = [v * 100 for v in allocations.values()]
    labels = list(allocations.keys())
    
    if sum(values) > 0:
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels,
            autopct='%1.1f%%',
            textprops={'size': 'smaller'},
            colors=plt.cm.Pastel1(np.linspace(0, 1, len(labels)))
        )
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
    else:
        ax.text(0.5, 0.5, 'No allocations yet', ha='center', va='center')
    
    ax.set_title("Portfolio Allocation", pad=20)
    return fig

def asset_allocation_selector():
    """Component for selecting and allocating assets."""
    st.subheader("Asset Allocation")
    
    # Initialize session state with 60/40 split
    if 'selected_assets' not in st.session_state:
        st.session_state.selected_assets = ["Global Stocks", "American Bonds"]
        st.session_state.allocations = {
            "Global Stocks": 0.6,
            "American Bonds": 0.4
        }
    if 'allocations' not in st.session_state:
        st.session_state.allocations = {
            "Global Stocks": 0.6,
            "American Bonds": 0.4
        }
    
    # Asset selection
    available_assets = list(SimulationConfig.ASSET_TICKERS.keys())
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_asset = st.selectbox("Add Asset", 
                                    [a for a in available_assets if a not in st.session_state.selected_assets],
                                    index=None,
                                    placeholder="Choose an asset to add...")
    
    with col2:
        if selected_asset and st.button("Add"):
            st.session_state.selected_assets.append(selected_asset)
            st.session_state.allocations[selected_asset] = 0
            st.rerun()

    # Asset allocation with number inputs and pie chart
    col1, col2 = st.columns([3, 2])
    
    with col1:
        new_allocations = {}
        total_allocation = 0
        
        for asset in st.session_state.selected_assets:
            cols = st.columns([3, 1, 1])
            with cols[0]:
                allocation = st.number_input(
                    f"{asset} (%)",
                    min_value=0,
                    max_value=100,
                    value=int(st.session_state.allocations.get(asset, 0) * 100),
                    step=5
                )
                new_allocations[asset] = allocation / 100
                total_allocation += allocation
            
            with cols[2]:
                if st.button("🗑️", key=f"remove_{asset}"):
                    st.session_state.selected_assets.remove(asset)
                    del st.session_state.allocations[asset]
                    st.rerun()
    
    with col2:
        # Show pie chart
        fig = create_allocation_pie_chart(new_allocations)
        st.pyplot(fig)
        plt.close(fig)

    # Validation
    if total_allocation > 100:
        st.error(f"❌ Total allocation exceeds 100% by {total_allocation - 100}%")
        return None
    elif total_allocation < 100:
        st.warning(f"⚠️ Total allocation is {total_allocation}%")
        return None
    elif total_allocation == 100:
        st.success("✅ Total allocation is 100%")
    
    st.session_state.allocations = new_allocations
    return new_allocations
