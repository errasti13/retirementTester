from dataclasses import dataclass
from typing import Dict, Any, TypedDict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AssetInfo(TypedDict):
    """Type definition for asset information."""
    ticker: str
    allocation: float

class SimulationConfig:
    """Configuration class for simulation parameters."""
    ASSET_TICKERS: Dict[str, str] = {
        'Global Stocks': '^990100-USD-STRD',
        'American Bonds': '^FVX',
        'American Stocks': '^SP500TR',
        'European Stocks': '^STOXX50E',
    }
    
    MIN_PORTFOLIO: float = 0.0
    MAX_PORTFOLIO: float = 1e9
    MIN_WITHDRAWAL: float = 0.0
    MAX_WITHDRAWAL: float = 1e7
    MIN_YEARS: int = 1
    MAX_YEARS: int = 100
    MIN_SIMS: int = 100
    MAX_SIMS: int = 10000

@dataclass
class SimulationParams:
    """Data class for simulation parameters with validation."""
    initial_portfolio: float
    annual_withdrawal: float
    retirement_years: int
    n_simulations: int
    assets: Dict[str, AssetInfo]

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validate all simulation parameters."""
        if not SimulationConfig.MIN_PORTFOLIO <= self.initial_portfolio <= SimulationConfig.MAX_PORTFOLIO:
            raise ValueError(f"Initial portfolio must be between {SimulationConfig.MIN_PORTFOLIO} and {SimulationConfig.MAX_PORTFOLIO}")
        # Add more validation as needed

def convert_assets_to_tickers(assets: Dict[str, float]) -> Dict[str, AssetInfo]:
    """
    Convert asset names to tickers using the ASSET_TICKERS dictionary.
    
    Args:
        assets: Dictionary mapping asset names to allocation percentages.
    
    Returns:
        Dictionary mapping asset names to AssetInfo objects.
        
    Raises:
        KeyError: If an asset name is not found in ASSET_TICKERS.
        ValueError: If allocations don't sum to 1.0.
    """
    if not abs(sum(assets.values()) - 1.0) < 1e-6:
        raise ValueError("Asset allocations must sum to 1.0")

    try:
        return {
            asset_name: {
                'ticker': SimulationConfig.ASSET_TICKERS[asset_name],
                'allocation': allocation
            }
            for asset_name, allocation in assets.items()
        }
    except KeyError as e:
        logger.error(f"Invalid asset name: {e}")
        raise KeyError(f"Asset {e} not found in available assets")

def setup_simulation_params(**kwargs) -> SimulationParams:
    """
    Set up and validate simulation parameters.
    
    Args:
        **kwargs: Keyword arguments for SimulationParams.
    
    Returns:
        SimulationParams object with validated parameters.
    """
    try:
        assets_with_tickers = convert_assets_to_tickers(kwargs['assets'])
        return SimulationParams(
            initial_portfolio=kwargs['initial_portfolio'],
            annual_withdrawal=kwargs['annual_withdrawal'],
            retirement_years=kwargs['retirement_years'],
            n_simulations=kwargs['n_simulations'],
            assets=assets_with_tickers
        )
    except (KeyError, ValueError) as e:
        logger.error(f"Error setting up simulation parameters: {e}")
        raise
