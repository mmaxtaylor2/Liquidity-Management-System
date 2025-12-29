import pandas as pd

def run_13_week_forecast(opening_cash: float, forecast_df: pd.DataFrame):
    """
    Generates a 13-week rolling cash forecast based on inflows/outflows.
    opening_cash should be a number (float or int)
    forecast_df must contain columns: inflows, outflows
    """
    cash = opening_cash
    forecast = []

    for _, row in forecast_df.iterrows():
        inflow = row.get("inflows", 0)
        outflow = row.get("outflows", 0)

        cash = cash + inflow - outflow
        forecast.append(cash)

    return forecast

