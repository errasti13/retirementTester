import streamlit as st
from retirementTester.app.utils import SimulationConfig

__all__ = ['asset_allocation_selector']

def asset_allocation_selector():
    """
    Component for selecting and allocating assets.
    Returns a dictionary of asset allocations.
    """
    st.subheader("Asset Allocation")
    
    # Initialize session state for assets if not exists
    if 'selected_assets' not in st.session_state:
        st.session_state.selected_assets = ["Global Stocks", "American Bonds"]
    if 'allocations' not in st.session_state:
        st.session_state.allocations = {asset: 0 for asset in st.session_state.selected_assets}
    
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
    
    # Asset allocation sliders
    total_allocation = 0
    new_allocations = {}
    
    for asset in st.session_state.selected_assets:
        col1, col2 = st.columns([4, 1])
        with col1:
            allocation = st.slider(f"{asset}", 0, 100, 
                                 int(st.session_state.allocations[asset] * 100),
                                 key=f"slider_{asset}")
            new_allocations[asset] = allocation / 100
            total_allocation += allocation
        with col2:
            if st.button("Remove", key=f"remove_{asset}"):
                st.session_state.selected_assets.remove(asset)
                del st.session_state.allocations[asset]
                st.rerun()
    
    # Warning for incorrect allocation
    if abs(total_allocation - 100) > 0.01:
        st.warning(f"Total allocation must be 100% (current: {total_allocation}%)")
        return None
    
    st.session_state.allocations = new_allocations
    return new_allocations
