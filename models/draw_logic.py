def adjust_for_liquidity(
    cash_levels, 
    min_cash=500000, 
    revolver_limit=5000000
):
    """
    Auto draw/repay behavior based on liquidity rules:
    - If projected cash falls below minimum operating cash, draw on revolver.
    - If cash rises above minimum and revolver has balance, repay.
    
    Returns: list of tuples -> (cash_after_adjustment, revolver_balance)
    """
    revolver_balance = 0
    adjusted = []

    for cash in cash_levels:

        # Draw if below operating minimum
        if cash < min_cash and revolver_balance < revolver_limit:
            draw_amount = min_cash - cash
            revolver_balance += draw_amount
            cash += draw_amount

        # Repay if above minimum and revolver has a balance
        elif cash > min_cash and revolver_balance > 0:
            repay_amount = min(cash - min_cash, revolver_balance)
            revolver_balance -= repay_amount
            cash -= repay_amount

        adjusted.append((cash, revolver_balance))

    return adjusted

