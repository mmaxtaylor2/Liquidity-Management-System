def liquidity_alerts(cash_levels, min_cash=500000, covenant_min=300000):
    """
    Generates text alerts based on liquidity thresholds.

    Rules:
    - Cash < covenant_min triggers a covenant warning
    - Cash < min_cash triggers an operational warning
    - Otherwise no alert

    Returns a list of alert strings.
    """
    alerts = []

    for week, cash in enumerate(cash_levels, start=1):
        if cash < covenant_min:
            alerts.append(f"Week {week}: CRITICAL - covenant breach risk (cash ${cash:,.0f})")
        elif cash < min_cash:
            alerts.append(f"Week {week}: Watchlist - below operating minimum (cash ${cash:,.0f})")

    return alerts

