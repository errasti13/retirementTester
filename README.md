# Retirement Portfolio Simulator

A Python-based Monte Carlo simulation tool for retirement portfolio analysis. This tool helps evaluate different retirement scenarios by simulating portfolio performance using historical market data.

## Features

- Monte Carlo simulation of retirement portfolios
- Historical data analysis from 1928 onwards
- Configurable asset allocation between stocks and bonds
- Visualization of portfolio projections including:
  - Best and worst case scenarios
  - Median path
  - 50% and 90% confidence bands
- Risk analysis including probability of portfolio depletion

## Requirements

- Python 3.8+
- yfinance
- pandas
- numpy
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/retirementTester.git
cd retirementTester
```

2. Install required packages:
```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

Run the simulation with default parameters:
```bash
python main.py
```

### Configuration Parameters

- `initial_portfolio`: Starting portfolio value
- `asset_allocation`: Distribution between stocks and bonds (e.g., 65% stocks, 35% bonds)
- `annual_withdrawal`: Yearly withdrawal amount
- `retirement_years`: Number of years to simulate
- `n_simulations`: Number of Monte Carlo simulations to run

### Example

```python
simulation_params = {
    'initial_portfolio': 1500000,
    'asset_allocation': {'stocks': 0.65, 'bonds': 0.35},
    'annual_withdrawal': 60000,
    'retirement_years': 30,
    'n_simulations': 2000
}
```

## Output

The simulation provides:
1. Visual representation of portfolio projections
2. Probability of portfolio depletion
3. Best, median, and worst-case final portfolio values
4. Confidence bands showing the range of likely outcomes

## Data Sources

- Stock market data: S&P 500 Index (^GSPC)
- Bond market data: Synthetic data based on historical treasury returns

## License

MIT License

## Author

Jon Errasti