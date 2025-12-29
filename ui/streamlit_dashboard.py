import pandas as pd
import streamlit as st
import sys, os
from pathlib import Path

# ====================================================================
# FIX IMPORT PATH FOR STREAMLIT
# ====================================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from models.forecast_engine import run_13_week_forecast
from models.draw_logic import adjust_for_liquidity
from models.alerts import liquidity_alerts

# ====================================================================
# PAGE CONFIG
# ====================================================================
st.set_page_config(page_title="Liquidity Management System", layout="wide")
st.title("Liquidity Management System")
st.subheader("Daily Cash Position + 13-Week Forecast + Liquidity Controls")
st.write("---")

# ====================================================================
# LOAD DATA
# ====================================================================
bank_df = pd.read_csv(str(ROOT_DIR / "data/bank_balances.csv"))
forecast_df = pd.read_csv(str(ROOT_DIR / "data/forecast_inputs.csv"))
opening_cash = bank_df["balance"].sum()

# ====================================================================
# SCENARIO SELECTOR
# ====================================================================
scenario = st.selectbox(
    "Select Scenario:",
    ["Base Case", "Mild Stress (-5% inflows)", "Severe Stress (-10% inflows)", "Outflow Shock (+15% outflows)"]
)
scenario_df = forecast_df.copy()

if scenario == "Mild Stress (-5% inflows)":
    scenario_df["inflows"] *= 0.95
elif scenario == "Severe Stress (-10% inflows)":
    scenario_df["inflows"] *= 0.90
elif scenario == "Outflow Shock (+15% outflows)":
    scenario_df["outflows"] *= 1.15

# ====================================================================
# FORECAST + REVOLVER
# ====================================================================
forecast = run_13_week_forecast(opening_cash, scenario_df)
adjusted = adjust_for_liquidity(forecast)
cash_balances = [c for c, _ in adjusted]
revolver_balances = [r for _, r in adjusted]
alerts = liquidity_alerts(cash_balances)

# ====================================================================
# STATUS LOGIC
# ====================================================================
last_cash = cash_balances[-1]
if last_cash >= 500000:
    status_text = "Stable Liquidity"
elif last_cash >= 300000:
    status_text = "Warning: Liquidity Buffer Declining"
else:
    status_text = "Critical: Covenant Risk"

st.markdown(f"### Liquidity Status: **{status_text}**")

# ====================================================================
# METRICS ROW
# ====================================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Opening Cash", f"${opening_cash:,.0f}")
col2.metric("Ending Cash (Week 13)", f"${last_cash:,.0f}")
col3.metric("Max Revolver Drawn", f"${max(revolver_balances):,.0f}")
col4.metric("Scenario", scenario)

st.write("---")

# ====================================================================
# CHARTS
# ====================================================================
chart_df = pd.DataFrame({
    "Week": range(1, len(cash_balances)+1),
    "Cash Balance": cash_balances,
    "Revolver Balance": revolver_balances
}).set_index("Week")

st.subheader("13-Week Liquidity Projection")
st.line_chart(chart_df)

st.write("---")
st.subheader("Bank Balance Distribution")
st.bar_chart(bank_df.set_index("bank")["balance"])

# ====================================================================
# ALERTS
# ====================================================================
st.write("---")
st.subheader("Warnings & Risk Signals")
if alerts:
    for a in alerts:
        st.error(a)
else:
    st.success("No liquidity issues detected during this period.")

# ====================================================================
# DATA + EXPORT
# ====================================================================
st.write("---")
st.subheader("Detailed Data Table")
st.dataframe(chart_df.reset_index())

st.download_button(
    label="Download Forecast CSV",
    data=chart_df.reset_index().to_csv(index=False),
    file_name="treasury_liquidity_forecast.csv",
    mime="text/csv"
)

st.write("Report generated successfully.")

