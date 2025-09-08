import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_sample_chart():
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    values = [100 + (i * 2 + i.day) for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name='Portfolio Value'))
    fig.update_layout(
        title='Portfolio Performance',
        xaxis_title='Date',
        yaxis_title='Value (₹)',
        height=400
    )
    return fig

def show_dashboard():
    if not st.session_state.login_status:
        st.warning("Please login first!")
        return

    st.title("Trading Dashboard")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview", 
        "Active Trades", 
        "Portfolio", 
        "Settings"
    ])
    
    with tab1:
        st.subheader("Dashboard Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total P&L", "₹15,000", "+1.2%")
        with col2:
            st.metric("Open Positions", "5", "-2")
        with col3:
            st.metric("Success Rate", "68%", "+3%")
        with col4:
            st.metric("Today's P&L", "₹2,500", "+0.5%")
            
        # Portfolio chart
        st.plotly_chart(create_sample_chart(), use_container_width=True)
    
    with tab2:
        st.subheader("Active Trades")
        trades_df = pd.DataFrame({
            "Symbol": ["RELIANCE", "TCS", "INFY", "HDFC", "ITC"],
            "Entry": [2500, 3400, 1500, 1600, 380],
            "Current": [2550, 3450, 1480, 1620, 385],
            "Quantity": [100, 50, 200, 150, 500],
            "P&L": ["+2%", "+1.5%", "-1.3%", "+1.2%", "+1.3%"]
        })
        st.dataframe(
            trades_df,
            column_config={
                "Symbol": "Stock",
                "Entry": st.column_config.NumberColumn("Entry Price", format="₹%d"),
                "Current": st.column_config.NumberColumn("Current Price", format="₹%d"),
                "P&L": "Profit/Loss"
            },
            hide_index=True
        )
    
    with tab3:
        st.subheader("Portfolio Analysis")
        
        # Portfolio composition
        st.markdown("### Asset Allocation")
        allocation_data = pd.DataFrame({
            "Sector": ["IT", "Banking", "Pharma", "Auto", "FMCG"],
            "Percentage": [30, 25, 15, 20, 10]
        })
        st.bar_chart(allocation_data.set_index("Sector"))
        
        # Performance metrics
        st.markdown("### Performance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("CAGR", "12.5%", "+2.3%")
            st.metric("Sharpe Ratio", "1.8", "+0.2")
        with col2:
            st.metric("Max Drawdown", "-8.5%", "+1.2%")
            st.metric("Beta", "0.85", "-0.05")
    
    with tab4:
        st.subheader("Trading Settings")
        
        # Copy trading settings
        st.markdown("### Copy Trading Configuration")
        st.checkbox("Enable Copy Trading", value=True)
        st.number_input("Risk Percentage per Trade", 
                       min_value=1, max_value=100, value=5)
        st.selectbox("Trading Mode", 
                    ["Conservative", "Moderate", "Aggressive"])
        
        # Advanced settings
        st.markdown("### Advanced Settings")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Max Open Positions", 
                          min_value=1, max_value=50, value=10)
            st.number_input("Stop Loss (%)", 
                          min_value=1, max_value=100, value=5)
        with col2:
            st.number_input("Take Profit (%)", 
                          min_value=1, max_value=1000, value=15)
            st.selectbox("Order Type", 
                        ["Market", "Limit", "Stop Loss", "Stop Loss Market"])