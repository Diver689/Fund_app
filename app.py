import streamlit as st
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Fund Return & Risk Analysis Tool", layout="wide")
st.title("📊 Fund Return & Risk Analysis Tool")
st.subheader("Supports: Net Value Trend, Daily Return, Sharpe Ratio, Max Drawdown")

# Session state for date persistence
if "start_date" not in st.session_state:
    st.session_state.start_date = pd.to_datetime("2020-01-01")

# User input area
col1, col2 = st.columns(2)
with col1:
    fund_code = st.text_input("Enter Fund Code (e.g., 000001)", value="000001")
with col2:
    start_date = st.date_input(
        "Select Start Date",
        value=st.session_state.start_date,
        key="start_date"
    )

# Risk level judgment function
def get_risk_level(sharpe_ratio, max_drawdown, volatility):
    if sharpe_ratio > 0.5 and max_drawdown > -0.15 and volatility < 0.15:
        return "Conservative", "#2ecc71"
    elif 0 <= sharpe_ratio <= 0.5 and -0.3 <= max_drawdown <= -0.15 and 0.15 <= volatility <= 0.25:
        return "Balanced", "#1c1915"
    else:
        return "Aggressive", "#e74c3c"

# Analysis button
if st.button("Start Analysis", type="primary"):
    with st.spinner("Fetching and calculating data..."):
        try:
            # Get fund data
            fund_df = ak.fund_open_fund_info_em(symbol=fund_code)
            fund_df["Date"] = pd.to_datetime(fund_df["净值日期"])
            fund_df["Net Value"] = fund_df["单位净值"].astype(float)
            
            # Filter by date
            fund_df = fund_df[fund_df["Date"] >= pd.to_datetime(start_date)]
            
            if len(fund_df) < 2:
                st.error("Insufficient data. Please adjust the start date or check the fund code.")
                st.stop()

            # Calculate indicators
            fund_df["Daily Return"] = fund_df["Net Value"].pct_change()
            fund_df = fund_df.dropna()
            
            annual_return = fund_df["Daily Return"].mean() * 252
            volatility = fund_df["Daily Return"].std() * np.sqrt(252)
            sharpe_ratio = annual_return / volatility if volatility != 0 else 0
            max_drawdown = (fund_df["Net Value"] / fund_df["Net Value"].cummax() - 1).min()

            # Get risk level
            risk_level, risk_color = get_risk_level(sharpe_ratio, max_drawdown, volatility)

            # Display metrics
            st.subheader("📈 Key Metrics Summary")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            # Annual Return
            if annual_return > 0:
                col1.markdown(f"<div style='text-align:center;'><div style='font-size:16px;'>Annual Return</div><div style='font-size:32px; color:#2ecc71; font-weight:bold;'>{annual_return:.2%}</div></div>", unsafe_allow_html=True)
            else:
                col1.markdown(f"<div style='text-align:center;'><div style='font-size:16px;'>Annual Return</div><div style='font-size:32px; color:#e74c3c; font-weight:bold;'>{annual_return:.2%}</div></div>", unsafe_allow_html=True)
            
            col2.markdown(f"<div style='text-align:center;'><div style='font-size:16px;'>Volatility</div><div style='font-size:32px; font-weight:bold;'>{volatility:.2%}</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div style='text-align:center;'><div style='font-size:16px;'>Sharpe Ratio</div><div style='font-size:32px; font-weight:bold;'>{sharpe_ratio:.2f}</div></div>", unsafe_allow_html=True)
            
            # Max Drawdown
            col4.markdown(f"<div style='text-align:center;'><div style='font-size:16px;'>Max Drawdown</div><div style='font-size:32px; color:#e74c3c; font-weight:bold;'>{max_drawdown:.2%}</div></div>", unsafe_allow_html=True)
            
            # Risk Level
            col5.markdown(
                f"<div style='background-color:{risk_color}; color:white; padding:20px 10px; border-radius:5px; text-align:center;'>"
                f"<strong>Risk Level</strong><br>{risk_level}</div>",
                unsafe_allow_html=True
            )

            # Net value trend chart
            st.subheader("📉 Fund Net Value Trend")
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(fund_df["Date"], fund_df["Net Value"], color="#1f77b4", linewidth=2)
            ax.set_title("Fund Net Value Trend", fontsize=14)
            ax.set_xlabel("Date")
            ax.set_ylabel("Net Value")
            st.pyplot(fig)

            # Latest data table
            st.subheader("📋 Latest 10 Net Value Records")
            st.dataframe(
                fund_df[["Date", "Net Value", "Daily Return"]].tail(10),
                hide_index=True,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check: 1. Fund code is correct 2. Date is not too early 3. Network is normal")

st.caption("Data Source: East Money via AkShare｜For educational purposes only, not investment advice.")