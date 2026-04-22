# Fund Return & Risk Analysis Tool
A Streamlit-based interactive application for analyzing fund performance metrics including Net Value Trend, Daily Return, Sharpe Ratio, and Max Drawdown.

## Features
- **Input Fund Code**: Support for China A-Share funds (e.g., 000001).
- **Date Filter**: Persistent date selection for historical data analysis.
- **Comprehensive Metrics**:
  - Annual Return
  - Volatility
  - Sharpe Ratio
  - Max Drawdown
- **Risk Level Classification**: Conservative, Balanced, Aggressive.
- **Visualization**: Clear trend chart of fund net value.
- **Data Table**: Latest 10 net value records for detailed reference.

## Data Source
Fund historical net value data is fetched from **East Money** via the **AkShare** API.
*Data is for educational purposes only and does not constitute investment advice.*

## How to Run Locally

### 1. Install required packages
```bash
pip install streamlit pandas numpy matplotlib akshare
### 2. Run the application
```bash
streamlit run fund_app.py