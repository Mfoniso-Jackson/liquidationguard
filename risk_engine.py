"""Core risk calculations for LiquidationGuard."""


def calculate_risk(
    account_balance: float,
    direction: str,
    entry_price: float,
    stop_price: float,
    leverage: float,
    risk_percent: float,
) -> dict:
    """Calculate futures position sizing and liquidation risk estimates."""
    risk_per_unit = abs(entry_price - stop_price)
    max_risk_amount = account_balance * (risk_percent / 100)
    position_size_units = max_risk_amount / risk_per_unit
    notional_position_value = position_size_units * entry_price
    margin_required = notional_position_value / leverage
    money_at_risk = position_size_units * risk_per_unit
    account_risk_percent = (money_at_risk / account_balance) * 100

    if direction == "Long":
        liquidation_price = entry_price * (1 - (1 / leverage))
    else:
        liquidation_price = entry_price * (1 + (1 / leverage))

    distance_to_stop_percent = (risk_per_unit / entry_price) * 100
    distance_to_liquidation_percent = (
        abs(entry_price - liquidation_price) / entry_price
    ) * 100
    liquidation_vs_stop_warning = distance_to_liquidation_percent < distance_to_stop_percent

    safety_status = get_safety_status(account_risk_percent)
    warnings = get_warnings(
        margin_required=margin_required,
        account_balance=account_balance,
        liquidation_vs_stop_warning=liquidation_vs_stop_warning,
        leverage=leverage,
    )
    decision = get_decision_text(
        liquidation_vs_stop_warning=liquidation_vs_stop_warning,
        leverage=leverage,
        safety_status=safety_status,
    )

    return {
        "risk_per_unit": risk_per_unit,
        "max_risk_amount": max_risk_amount,
        "position_size_units": position_size_units,
        "notional_position_value": notional_position_value,
        "margin_required": margin_required,
        "money_at_risk": money_at_risk,
        "account_risk_percent": account_risk_percent,
        "liquidation_price": liquidation_price,
        "distance_to_stop_percent": distance_to_stop_percent,
        "distance_to_liquidation_percent": distance_to_liquidation_percent,
        "liquidation_vs_stop_warning": liquidation_vs_stop_warning,
        "safety_status": safety_status,
        "warnings": warnings,
        "decision": decision,
    }


def get_safety_status(account_risk_percent: float) -> str:
    """Classify the trade by account risk."""
    if account_risk_percent <= 1:
        return "Conservative"
    if account_risk_percent <= 3:
        return "Moderate"
    return "High Risk"


def get_warnings(
    margin_required: float,
    account_balance: float,
    liquidation_vs_stop_warning: bool,
    leverage: float,
) -> list[str]:
    """Return plain-English warnings for the calculated setup."""
    warnings = []

    if margin_required > account_balance:
        warnings.append("Margin required exceeds your account balance.")
    if liquidation_vs_stop_warning:
        warnings.append("Liquidation is closer to entry than your stop loss.")
    if leverage > 20:
        warnings.append("Leverage is above 20x.")

    warnings.append("Liquidation estimate is approximate.")
    return warnings


def get_decision_text(
    liquidation_vs_stop_warning: bool,
    leverage: float,
    safety_status: str,
) -> str:
    """Summarize the risk result as a trading decision prompt."""
    if liquidation_vs_stop_warning:
        return (
            "This setup is dangerous because liquidation is closer than your stop "
            "loss. Reduce position size or leverage before entering."
        )
    if leverage > 20:
        return "This setup is acceptable, but leverage is high."
    if safety_status == "High Risk":
        return "Reduce position size or risk percentage before entering."
    return "This setup fits your chosen risk level."
