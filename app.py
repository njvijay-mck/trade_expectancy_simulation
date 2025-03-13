import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from documentation import show_documentation

# Set page configuration
st.set_page_config(
    page_title="Trading Expectancy Calculator",
    page_icon="💹",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .footer {
        font-size: 0.8rem;
        color: #888;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'sample_size' not in st.session_state:
    st.session_state.sample_size = 100

# Function to calculate expected losing streak
def calculate_losing_streak(win_rate, sample_size):
    """
    Calculate the expected maximum losing streak based on win rate and sample size.
    
    Formula: log(sample_size) / log(1/(1-win_rate))
    
    Args:
        win_rate (float): Win rate as a decimal (e.g., 0.5 for 50%)
        sample_size (int): Number of trades
        
    Returns:
        float: Expected maximum losing streak
    """
    if win_rate >= 1.0:
        return 0  # If win rate is 100%, no losing streaks expected
    
    # Calculate using the formula
    denominator = math.log(1/(1-win_rate))
    if denominator == 0:
        return float('inf')  # Handle division by zero
    
    losing_streak = math.log(sample_size) / denominator
    return losing_streak

# Function to run trading simulation
def run_simulation(account_balance, win_rate, reward_risk, risk_percent, trade_count):
    """
    Run a trading simulation based on input parameters.
    
    Args:
        account_balance (float): Initial account balance
        win_rate (float): Win rate as a decimal (e.g., 0.5 for 50%)
        reward_risk (float): Reward to risk ratio
        risk_percent (float): Risk percentage per trade as a decimal
        trade_count (int): Number of trades to simulate
        
    Returns:
        tuple: (DataFrame with trade results, dict with summary statistics)
    """
    # Initialize DataFrame to store results
    results = []
    
    # Initialize tracking variables
    current_balance = account_balance
    peak_balance = account_balance
    max_drawdown = 0
    win_count = 0
    
    # Generate random win/loss sequence based on win rate
    outcomes = np.random.choice(
        ['Win', 'Loss'], 
        size=trade_count, 
        p=[win_rate, 1-win_rate]
    )
    
    # Simulate each trade
    for i in range(trade_count):
        # Store pre-trade balance
        pre_balance = current_balance
        
        # Calculate risk amount based on current balance
        risk_amount = current_balance * risk_percent
        
        # Determine P&L based on outcome
        if outcomes[i] == 'Win':
            pnl = risk_amount * reward_risk
            win_count += 1
        else:
            pnl = -risk_amount
        
        # Update balance
        current_balance += pnl
        
        # Update peak balance if new high
        if current_balance > peak_balance:
            peak_balance = current_balance
        
        # Calculate current drawdown
        current_drawdown = (peak_balance - current_balance) / peak_balance * 100 if peak_balance > 0 else 0
        
        # Update max drawdown if needed
        if current_drawdown > max_drawdown:
            max_drawdown = current_drawdown
        
        # Store trade results
        results.append({
            'Trade Number': i + 1,
            'Win/Loss': outcomes[i],
            'Pre-Balance': pre_balance,
            'Risk Amount': risk_amount,
            'P&L': pnl,
            'After-Balance': current_balance,
            'Drawdown': current_drawdown,
            'Peak Balance': peak_balance
        })
    
    # Create DataFrame from results
    df = pd.DataFrame(results)
    
    # Calculate summary statistics
    actual_win_rate = win_count / trade_count
    profit = current_balance - account_balance
    return_pct = (profit / account_balance) * 100
    
    # Calculate expectancy
    avg_win = df[df['Win/Loss'] == 'Win']['P&L'].mean() if win_count > 0 else 0
    avg_loss = abs(df[df['Win/Loss'] == 'Loss']['P&L'].mean()) if trade_count - win_count > 0 else 0
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
    expectancy_r = expectancy / avg_loss if avg_loss > 0 else 0
    
    # Calculate minimum profitable win rate
    min_win_rate = 1 / (1 + reward_risk)
    
    # Create summary dictionary
    summary = {
        'Final Balance': current_balance,
        'Profit': profit,
        'Return': return_pct,
        'Max Drawdown': max_drawdown,
        'Expectancy': expectancy,
        'Expectancy R': expectancy_r,
        'Actual Win Rate': actual_win_rate * 100,
        'Minimum Win Rate': min_win_rate * 100,
        'Trades': trade_count
    }
    
    return df, summary

# App title
st.title("Trading Expectancy Calculator")

# Introduction
st.markdown("""
This application provides tools to help traders understand the statistical aspects of their trading strategies,
including potential losing streaks and expected performance through trade sequence simulation.
""")

# Create tabs for different calculators
tab1, tab2, tab3 = st.tabs(["Expectancy Calculator", "Losing Streak Calculator", "Documentation"])

# Tab 1: Expectancy Calculator
with tab1:
    st.markdown("## Expectancy Calculator")
    st.markdown("""
    This calculator simulates trading outcomes based on your strategy parameters and provides 
    insights into expected performance including profit, drawdown, and expectancy.
    """)
    
    # Input form for simulation parameters
    with st.form(key="simulation_params"):
        st.subheader("Simulation Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            account_balance = st.number_input(
                "Initial Account Balance ($)",
                min_value=100.0,
                max_value=1000000.0,
                value=10000.0,
                step=1000.0,
                help="Your starting account balance"
            )
            
            win_rate = st.slider(
                "Win Rate (%)",
                min_value=5,
                max_value=95,
                value=40,
                step=1,
                help="Percentage of trades that are winners"
            ) / 100
            
            reward_risk = st.number_input(
                "Reward:Risk Ratio",
                min_value=0.1,
                max_value=10.0,
                value=2.0,
                step=0.1,
                help="Average winner size divided by average loser size"
            )
        
        with col2:
            risk_percent = st.slider(
                "Risk % Per Trade",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1,
                help="Percentage of account risked on each trade"
            ) / 100
            
            trade_count = st.number_input(
                "Number of Trades",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Number of trades to simulate"
            )
        
        # Add a button to run simulation
        run_button = st.form_submit_button(label="Run Simulation")
    
    # Run simulation when button is clicked
    if run_button:
        # Run the simulation
        results_df, summary = run_simulation(
            account_balance=account_balance,
            win_rate=win_rate,
            reward_risk=reward_risk,
            risk_percent=risk_percent,
            trade_count=trade_count
        )
        
        # Store in session state for persistence
        st.session_state.results_df = results_df
        st.session_state.summary = summary
    
    # Display results if simulation has been run
    if 'results_df' in st.session_state and 'summary' in st.session_state:
        # Get data from session state
        results_df = st.session_state.results_df
        summary = st.session_state.summary
        
        # Create dashboard layout
        st.subheader("Simulation Results")
        
        # Summary metrics in a nice grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Add up/down arrow and percentage to account balance
            profit_pct = summary['Return']
            
            # In Streamlit's st.metric, for delta_color:
            # "normal" means: positive values are green, negative values are red
            # "inverse" means: positive values are red, negative values are green
            # We want positive values green and negative values red, so use "normal"
            st.metric(
                "Final Account Balance", 
                f"${summary['Final Balance']:,.2f}", 
                f"{profit_pct:.2f}%",
                delta_color="normal"
            )
            st.metric("Profit/Loss", f"${summary['Profit']:,.2f}")
        
        with col2:
            st.metric("Return", f"{summary['Return']:.2f}%")
            st.metric("Max Drawdown", f"{summary['Max Drawdown']:.2f}%")
        
        with col3:
            st.metric("Expectancy", f"${summary['Expectancy']:,.2f}")
            st.metric("Expectancy R", f"{summary['Expectancy R']:.2f}")
        
        with col4:
            st.metric("Actual Win Rate", f"{summary['Actual Win Rate']:.2f}%")
            st.metric("Minimum Win Rate", f"{summary['Minimum Win Rate']:.2f}%")
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Equity Curve", "Trade Results", "Drawdown"])
        
        # Tab 1: Equity Curve
        with viz_tab1:
            # Create equity curve chart
            fig = go.Figure()
            
            # Add equity curve line
            fig.add_trace(
                go.Scatter(
                    x=results_df['Trade Number'],
                    y=results_df['After-Balance'],
                    mode='lines',
                    name='Account Balance',
                    line=dict(color='blue', width=2)
                )
            )
            
            # Add initial balance reference line
            fig.add_trace(
                go.Scatter(
                    x=[1, results_df['Trade Number'].max()],
                    y=[account_balance, account_balance],
                    mode='lines',
                    name='Initial Balance',
                    line=dict(color='red', width=1, dash='dash')
                )
            )
            
            # Update layout
            fig.update_layout(
                title="Equity Curve",
                xaxis_title="Trade Number",
                yaxis_title="Account Balance ($)",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 2: Trade Results
        with viz_tab2:
            # Create two columns for the visualizations
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create P&L bar chart
                fig_bar = go.Figure()
                
                # Add P&L bars with colors based on win/loss
                colors = ['green' if x == 'Win' else 'red' for x in results_df['Win/Loss']]
                
                fig_bar.add_trace(
                    go.Bar(
                        x=results_df['Trade Number'],
                        y=results_df['P&L'],
                        marker_color=colors,
                        name='P&L'
                    )
                )
                
                # Update layout
                fig_bar.update_layout(
                    title="P&L per Trade",
                    xaxis_title="Trade Number",
                    yaxis_title="P&L ($)",
                    height=500,
                    hovermode="x unified"
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Create win/loss pie chart
                win_count = (results_df['Win/Loss'] == 'Win').sum()
                loss_count = (results_df['Win/Loss'] == 'Loss').sum()
                
                fig_pie = go.Figure(
                    go.Pie(
                        labels=['Wins', 'Losses'],
                        values=[win_count, loss_count],
                        marker=dict(colors=['green', 'red']),
                        hole=0.4,
                        textinfo='label+percent'
                    )
                )
                
                # Update layout
                fig_pie.update_layout(
                    title="Win/Loss Distribution",
                    height=500
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tab 3: Drawdown
        with viz_tab3:
            # Create a figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add drawdown line on primary y-axis
            fig.add_trace(
                go.Scatter(
                    x=results_df['Trade Number'],
                    y=results_df['Drawdown'],
                    mode='lines',
                    name='Drawdown',
                    line=dict(color='red', width=2),
                    fill='tozeroy'
                ),
                secondary_y=False
            )
            
            # Add equity curve on secondary y-axis
            fig.add_trace(
                go.Scatter(
                    x=results_df['Trade Number'],
                    y=results_df['After-Balance'],
                    mode='lines',
                    name='Account Balance',
                    line=dict(color='blue', width=2)
                ),
                secondary_y=True
            )
            
            # Add initial balance reference line on secondary y-axis
            fig.add_trace(
                go.Scatter(
                    x=[1, results_df['Trade Number'].max()],
                    y=[account_balance, account_balance],
                    mode='lines',
                    name='Initial Balance',
                    line=dict(color='green', width=1, dash='dash')
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title="Drawdown and Equity Curve",
                xaxis_title="Trade Number",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=500,
                hovermode="x unified"
            )
            
            # Set y-axes titles
            fig.update_yaxes(title_text="Drawdown (%)", secondary_y=False, color="red")
            fig.update_yaxes(title_text="Account Balance ($)", secondary_y=True, color="blue")
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display trade data table
        st.subheader("Trade Data")
        
        # Format columns for better display
        display_df = results_df.copy()
        display_df['Pre-Balance'] = display_df['Pre-Balance'].map('${:,.2f}'.format)
        display_df['Risk Amount'] = display_df['Risk Amount'].map('${:,.2f}'.format)
        display_df['P&L'] = display_df['P&L'].map('${:,.2f}'.format)
        display_df['After-Balance'] = display_df['After-Balance'].map('${:,.2f}'.format)
        display_df['Drawdown'] = display_df['Drawdown'].map('{:.2f}%'.format)
        display_df['Peak Balance'] = display_df['Peak Balance'].map('${:,.2f}'.format)
        
        st.dataframe(display_df, use_container_width=True)
        
        # Add dynamic insights section
        st.subheader("Insights")
        
        # Determine insights based on simulation results
        is_profitable = summary['Profit'] > 0
        actual_win_rate = summary['Actual Win Rate']
        min_win_rate = summary['Minimum Win Rate']
        win_rate_sufficient = actual_win_rate >= min_win_rate
        max_drawdown = summary['Max Drawdown']
        high_drawdown = max_drawdown > 30  # Consider drawdown over 30% as significant
        positive_expectancy = summary['Expectancy'] > 0
        
        # Create insights with appropriate icons
        insights = []
        
        # Profitability insight
        if is_profitable:
            insights.append("✅ The system was profitable in this simulation.")
        else:
            insights.append("❌ The system was not profitable in this simulation.")
        
        # Win rate insight
        if win_rate_sufficient:
            insights.append(f"✅ The actual win rate ({actual_win_rate:.1f}%) was above the minimum required win rate ({min_win_rate:.1f}%).")
        else:
            insights.append(f"⚠️ The actual win rate ({actual_win_rate:.1f}%) was below the minimum required win rate ({min_win_rate:.1f}%).")
        
        # Drawdown insight
        if high_drawdown:
            insights.append(f"⚠️ The maximum drawdown ({max_drawdown:.1f}%) was significant. Consider reducing position size.")
        else:
            insights.append(f"✅ The maximum drawdown ({max_drawdown:.1f}%) was within reasonable limits.")
        
        # Expectancy insight
        if positive_expectancy:
            insights.append("✅ The system has a positive expectancy. It's expected to be profitable in the long run.")
        else:
            insights.append("❌ The system has a negative expectancy. It's not expected to be profitable in the long run.")
        
        # Display insights
        for insight in insights:
            st.markdown(insight)
    
    # Explanation section
    st.markdown("""
    ### How to Interpret the Results

    This simulation provides a realistic view of how your trading strategy might perform over time, 
    taking into account the randomness of trading outcomes.

    **Key metrics explained:**
    - **Final Balance**: Your account balance after all simulated trades
    - **Profit/Loss**: Total profit or loss from the simulation
    - **Return**: Percentage return on your initial investment
    - **Max Drawdown**: Largest percentage drop from a peak to a trough
    - **Expectancy**: Average amount you can expect to win (or lose) per trade
    - **Expectancy R**: Expectancy expressed in terms of risk (R)
    - **Minimum Win Rate**: The win rate needed to break even with your reward:risk ratio

    **Note**: Each simulation run will produce different results due to randomization, 
    even with the same parameters. Run multiple simulations to get a better understanding 
    of the range of possible outcomes.
    """)

# Tab 2: Losing Streak Calculator
with tab2:
    st.markdown("## Losing Streak Calculator")
    st.markdown("""
    This calculator helps traders understand the potential losing streaks they might encounter 
    based on their strategy's win rate and the number of trades they plan to make.
    """)
    
    # Parameters section
    st.subheader("Parameters")
    
    # Create a form for the parameters
    with st.form(key="losing_streak_params"):
        sample_size_input = st.number_input(
            "Sample Size (Number of Trades)",
            min_value=10,
            max_value=10000,
            value=st.session_state.sample_size,
            step=10,
            help="Enter the total number of trades you plan to make"
        )
        
        # Add a button to apply changes
        submit_button = st.form_submit_button(label="Calculate Losing Streaks")
        if submit_button:
            st.session_state.sample_size = sample_size_input

    # Only show results if form has been submitted
    if 'sample_size' in st.session_state:
        # Define specific win rates to display (not incremental)
        win_rates = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 
                    0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
        
        results = []
        for win_rate in win_rates:
            losing_streak = calculate_losing_streak(win_rate, st.session_state.sample_size)
            results.append({
                "Win Rate %": f"{win_rate*100:.0f}%",
                "Expected Losing Streak": f"{round(losing_streak, 2):.2f}"  # Format to always show 2 decimal places
            })

        # Create a DataFrame from the results
        df = pd.DataFrame(results)
        
        # Create a better layout with columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display results in a styled table
            st.subheader(f"Expected Losing Streaks for {st.session_state.sample_size} Trades")
            
            # Display table with proper styling
            st.table(df)
        
        with col2:
            # Create a combined visualization
            st.subheader("Visualization of Expected Losing Streaks")
            
            # Convert string values back to float for plotting
            df_plot = df.copy()
            df_plot["Expected Losing Streak"] = df_plot["Expected Losing Streak"].apply(lambda x: float(x))
            
            # Create a combined figure with both bar and line
            fig = go.Figure()
            
            # Add bar chart
            fig.add_trace(
                go.Bar(
                    x=df_plot["Win Rate %"],
                    y=df_plot["Expected Losing Streak"],
                    name="Expected Losing Streak",
                    marker_color='lightblue',
                    opacity=0.7
                )
            )
            
            # Add line chart on top
            fig.add_trace(
                go.Scatter(
                    x=df_plot["Win Rate %"],
                    y=df_plot["Expected Losing Streak"],
                    mode='lines+markers',
                    name="Trend Line",
                    line=dict(color='darkblue', width=3),
                    marker=dict(size=8, color='darkblue')
                )
            )
            
            # Update layout
            fig.update_layout(
                title=f"Expected Losing Streaks for {st.session_state.sample_size} Trades",
                xaxis_title="Win Rate %",
                yaxis_title="Expected Losing Streak",
                legend_title="Chart Type",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)

        # Explanation section
        st.markdown("""
        ### How to Interpret the Results

        The table and chart above show the expected maximum losing streak you might encounter based on your win rate and the number of trades.

        **Key insights:**
        - Higher win rates lead to shorter expected losing streaks
        - As the sample size (number of trades) increases, the potential for longer losing streaks also increases
        - This information can help you prepare psychologically and financially for drawdowns

        ### Formula Used
        The expected maximum losing streak is calculated using:

        `Expected Maximum Losing Streak ≈ log(N) / log(1/(1-p))`

        Where:
        - N is the sample size (number of trades)
        - p is the win rate (as a decimal)
        """)

# Tab 3: Documentation
with tab3:
    show_documentation()

# Footer
st.markdown("""
<div class="footer">
    Trading Expectancy Calculator | Created with Streamlit | Data is simulated
</div>
""", unsafe_allow_html=True)
