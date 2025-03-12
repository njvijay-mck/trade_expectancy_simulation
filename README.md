# Trading Simulator

A Python Streamlit application with Plotly visualizations for various trading simulators.

## Features

### Current Modules:
- **Losing Streak Calculator**: Calculate expected losing streaks based on win rate and sample size

### Planned Future Modules:
- **Expectancy Calculator**: Calculate trading system expectancy based on win rate, average win, and average loss
- Additional trading simulation tools
- Risk management calculators
- Performance analysis tools

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```
streamlit run app.py
```

## Losing Streak Calculator

This module helps traders understand the potential losing streaks they might encounter based on their strategy's win rate and the number of trades they plan to make.

### Formula

The expected maximum losing streak is calculated using:

```
Expected Maximum Losing Streak ≈ log(N) / log(1/(1-p))
```

Where:
- N is the sample size (number of trades)
- p is the win rate (as a decimal)

## License

This project is open source and available for personal and educational use.
