import streamlit as st

def show_documentation():
    """Display documentation for the Trading Expectancy Calculator."""
    
    st.title("Documentation")
    
    # Table of contents
    st.markdown("""
    ## Table of Contents
    - [Losing Streak Calculator](#losing-streak-calculator)
    - [Expectancy Calculator](#expectancy-calculator)
    - [Interpreting Results](#interpreting-results)
    - [Glossary](#glossary)
    """)
    
    # Losing Streak Calculator
    st.markdown("""
    ## Losing Streak Calculator
    
    ### What is it?
    The Losing Streak Calculator estimates the maximum number of consecutive losing trades you might experience based on your win rate and the number of trades.
    
    ### How it works
    The calculator uses probability theory to estimate the expected maximum losing streak. It's based on the formula:
    
    ```
    Expected Max Losing Streak = log(N) / log(1 / (1 - Win Rate))
    ```
    
    Where:
    - N is the number of trades
    - Win Rate is expressed as a decimal (e.g., 0.50 for 50%)
    
    ### How to use it
    1. Enter your expected win rate (as a percentage)
    2. Enter the number of trades you plan to take
    3. The calculator will show you the expected maximum losing streak
    
    ### Why it's important
    Understanding potential losing streaks helps you:
    - Prepare psychologically for drawdowns
    - Set appropriate position sizing to survive worst-case scenarios
    - Avoid abandoning a profitable strategy during normal losing streaks
    """)
    
    # Expectancy Calculator
    st.markdown("""
    ## Expectancy Calculator
    
    ### What is it?
    The Expectancy Calculator simulates trading outcomes based on your parameters to show potential results, including profit/loss, drawdowns, and the mathematical expectancy of your trading system.
    
    ### How it works
    The calculator runs a trade sequence simulation that:
    1. Generates random trade outcomes based on your win rate
    2. Applies your reward-to-risk ratio to calculate profits and losses
    3. Tracks account balance, drawdowns, and other metrics
    4. Calculates the mathematical expectancy of your trading system
    
    ### How to use it
    1. Enter your starting account balance
    2. Specify your win rate (percentage of winning trades)
    3. Set your reward-to-risk ratio (how much you win vs. how much you risk)
    4. Define your risk percentage per trade
    5. Choose the number of trades to simulate
    6. Run the simulation to see the results
    
    ### Key metrics explained
    
    **Final Account Balance**: The ending account value after all simulated trades
    
    **Profit/Loss**: The total profit or loss from the simulation
    
    **Return**: The percentage return on your initial investment
    
    **Max Drawdown**: The largest percentage drop from a peak to a trough in your account balance
    
    **Expectancy**: The average amount you can expect to win or lose per dollar risked
    
    **Expectancy R**: The average amount you can expect to win or lose per trade, expressed in terms of R (your initial risk)
    
    **Minimum Win Rate**: The break-even win rate for your given reward-to-risk ratio
    """)
    
    # Interpreting Results
    st.markdown("""
    ## Interpreting Results
    
    ### Equity Curve
    The equity curve shows how your account balance changes over time. A steadily rising curve indicates a profitable strategy, while a declining curve suggests losses.
    
    ### Drawdown Analysis
    The drawdown chart shows the percentage drop from peak equity. This helps you understand the potential downside risk of your strategy.
    
    ### Trade Results
    The trade results table shows detailed information about each simulated trade, including:
    - Pre-trade balance
    - Risk amount
    - Win/loss outcome
    - Profit or loss
    - Post-trade balance
    - Drawdown percentage
    
    ### Insights
    The insights section provides an automated analysis of your simulation results, highlighting:
    - Overall profitability
    - Win rate adequacy
    - Drawdown significance
    - Expectancy evaluation
    """)
    
    # Glossary
    st.markdown("""
    ## Glossary
    
    **Win Rate**: The percentage of trades that are profitable.
    
    **Reward-to-Risk Ratio (RRR)**: The ratio of your average win to your average loss. For example, a 2:1 RRR means your average win is twice the size of your average loss.
    
    **Risk Percentage**: The percentage of your account balance you risk on each trade.
    
    **Expectancy**: The average amount you can expect to win or lose per dollar risked. Calculated as: (Win Rate × Average Win) - (Loss Rate × Average Loss).
    
    **Drawdown**: A measure of the decline from a peak in account value to a trough before a new peak is achieved.
    
    **R-Multiple**: A way to measure trade performance in terms of the initial risk (R). A trade that makes twice your risk has an R-multiple of +2R.
    
    **Minimum Win Rate**: The win rate required to break even, given your reward-to-risk ratio. Calculated as: 1 / (1 + Reward-to-Risk Ratio).
    """)
