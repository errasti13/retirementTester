import streamlit as st
import pandas as pd
import logging
from .data import fetch_historical_data
from .utils import SimulationConfig

logger = logging.getLogger(__name__)

def get_data_start_date() -> str:
    """Get the earliest available date from the fetched data."""
    if 'all_asset_data' in st.session_state:
        data = st.session_state.all_asset_data
        if isinstance(data, pd.DataFrame) and not data.empty:
            logger.debug(f"Data start date: {data.index[0].year}")
            return str(data.index[0].year)
    logger.debug("Data not available")
    return "Not available"

def initialize_all_assets():
    """Silently initialize data for all possible assets when the app starts."""
    if 'all_asset_data' not in st.session_state:
        logger.info("Initializing all asset data")
        # Get all unique tickers
        tickers = tuple(SimulationConfig.ASSET_TICKERS.values())
        
        try:
            # Fetch all data at once and store the DataFrame directly
            data = fetch_historical_data(tickers)
            if isinstance(data, pd.DataFrame) and not data.empty:
                st.session_state.all_asset_data = data
                st.session_state.data_fetched = True
                logger.info("Successfully fetched all asset data")
            else:
                logger.error("Failed to fetch data: empty result")
                st.session_state.all_asset_data = pd.DataFrame()
                st.session_state.data_fetched = False
        except Exception as e:
            logger.error(f"Failed to fetch initial data: {e}")
            st.session_state.all_asset_data = pd.DataFrame()
            st.session_state.data_fetched = False
    else:
        logger.info("All asset data already initialized")
        st.session_state.data_fetched = True

def get_asset_data(tickers: tuple[str, ...]) -> pd.DataFrame:
    """Get asset data from session state or fetch if needed."""
    if 'all_asset_data' not in st.session_state:
        initialize_all_assets()
    return st.session_state.all_asset_data
