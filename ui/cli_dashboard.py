import pandas as pd

from models.forecast_engine import run_13_week_forecast
from models.draw_logic import adjust_for_liquidity
from models.alerts import liquidity_alerts

def main():

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------
    bank_df = pd.read_csv("data/bank_balances.csv")
    forecast_df = pd.read_csv("data/forecast_inputs.csv")

    # Opening cash = total across all banks
    opening_cash = bank_df["balance"].sum()

    # --------------------------------------------------
    # RUN BASE FORECAST + LIQUIDITY ADJUSTMENTS
    # --------------------------------------------------
    forecast = run_13_week_forecast(opening_cash, forecast_df)
    adjusted_path = adjust_for_liquidity(forecast)

    cash_balances = [x[0] for x in adjusted_path]
    revolver_balances = [x[1] for x in adjusted_path]

    # --------------------------------------------------
    # PRINT HEADER
    # --------------------------------------------------
    print("\n==================================================")
    print("          LIQUIDITY MANAGEMENT SYSTEM")
    print("==================================================")
    print(f"Opening Cash Balance:       ${opening_cash:,.0f}")
    print("Forecast Horizon:           13 weeks")
    print("Minimum Operating Cash:     $500,000")
    print("Covenant Threshold:         $300,000")
    print("Revolver Limit:             $5,000,000")
    print("==================================================\n")

    # --------------------------------------------------
    # WEEKLY FORECAST OUTPUT
    # --------------------------------------------------
    print("Week | Ending Cash | Revolver Balance")
    print("--------------------------------------")
    for i, (cash, rev) in enumerate(adjusted_path, start=1):
        print(f"{str(i).rjust(4)} | ${cash:,.0f}    | ${rev:,.0f}")

    # --------------------------------------------------
    # ALERTS / WARNINGS
    # --------------------------------------------------
    alerts = liquidity_alerts(cash_balances)

    if alerts:
        print("\n==================================================")
        print("                 LIQUIDITY ALERTS")
        print("==================================================")
        for alert in alerts:
            print(alert)
        print("==================================================\n")
    else:
        print("\nNo liquidity issues detected. Cash remains above critical thresholds.\n")

    print("Run complete.\n")


if __name__ == "__main__":
    main()

