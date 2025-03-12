# Trading Expectancy Calculator

A Python Streamlit application with Plotly visualizations for trading strategy analysis and simulation.

## Features

### Current Modules:
- **Expectancy Calculator**: Simulates trading outcomes based on your parameters to show potential results, including profit/loss, drawdowns, and mathematical expectancy
- **Losing Streak Calculator**: Calculate expected losing streaks based on win rate and sample size
- **Documentation**: Comprehensive guide explaining all features and how to interpret results

### Key Features:
- **Trade Sequence Simulation**: Generate random trade sequences based on win rate and analyze outcomes
- **Dynamic Insights**: Automated analysis of simulation results with actionable feedback
- **Interactive Visualizations**: Equity curves, drawdown charts, and trade result tables
- **Risk Analysis**: Calculate risk amount per trade and see its impact on overall performance
- **Performance Metrics**: View key metrics like expectancy, maximum drawdown, and minimum win rate

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

## Expectancy Calculator

This module simulates trading outcomes based on your strategy parameters and provides insights into expected performance including profit, drawdown, and expectancy.

### Parameters:
- **Account Balance**: Your starting trading capital
- **Win Rate**: Percentage of trades that are winners
- **Reward-to-Risk Ratio**: Average win divided by average loss
- **Risk Per Trade**: Percentage of account risked on each trade
- **Number of Trades**: How many trades to simulate

### Key Metrics:
- **Final Account Balance**: Ending capital after all trades
- **Profit/Loss**: Total profit or loss from the simulation
- **Return**: Percentage return on initial investment
- **Max Drawdown**: Largest percentage drop from peak to trough
- **Expectancy**: Average amount you can expect to win or lose per dollar risked
- **Expectancy R**: Average amount you can expect to win or lose per trade in R-multiples
- **Minimum Win Rate**: Break-even win rate for your reward-to-risk ratio

## Losing Streak Calculator

This module helps traders understand the potential losing streaks they might encounter based on their strategy's win rate and the number of trades they plan to make.

### Formula:
The expected maximum losing streak is calculated using:

```
Expected Maximum Losing Streak ≈ log(N) / log(1/(1-p))
```

Where:
- N is the sample size (number of trades)
- p is the win rate (as a decimal)

## Dynamic Insights

The application provides automated analysis of your simulation results, including:

- Overall profitability assessment
- Win rate adequacy compared to minimum required win rate
- Drawdown significance evaluation
- Expectancy analysis for long-term profitability

## Visualization Features

- **Equity Curve**: Track account balance changes over time
- **Drawdown Chart**: Visualize percentage drops from peak equity
- **Trade Results Table**: Detailed information about each simulated trade
- **Risk Amount Display**: See exactly how much is risked on each trade

## License

This project is open source and available for personal and educational use.

## Recent Updates

- Added Expectancy Calculator with trade sequence simulation
- Implemented dynamic insights with actionable feedback
- Added risk amount calculation to trade data table
- Combined equity curve and drawdown visualization
- Added comprehensive documentation tab
- Updated UI with improved metrics display
