from app.schemas import RiskRequest, RiskResult


def calculate_risk(payload: RiskRequest) -> RiskResult:
    risk_per_unit = abs(payload.entry_price - payload.stop_price)
    max_risk_amount = payload.account_balance * (payload.risk_percent / 100)
    position_size_units = max_risk_amount / risk_per_unit
    notional_position_value = position_size_units * payload.entry_price
    margin_required = notional_position_value / payload.leverage
    money_at_risk = position_size_units * risk_per_unit
    account_risk_percent = (money_at_risk / payload.account_balance) * 100

    if payload.direction == "Long":
        liquidation_price = payload.entry_price * (1 - (1 / payload.leverage))
    else:
        liquidation_price = payload.entry_price * (1 + (1 / payload.leverage))

    distance_to_stop_percent = (risk_per_unit / payload.entry_price) * 100
    distance_to_liquidation_percent = (
        abs(payload.entry_price - liquidation_price) / payload.entry_price
    ) * 100
    liquidation_vs_stop_warning = distance_to_liquidation_percent < distance_to_stop_percent

    safety_status = get_safety_status(account_risk_percent)
    warnings = get_warnings(
        margin_required=margin_required,
        account_balance=payload.account_balance,
        leverage=payload.leverage,
        liquidation_vs_stop_warning=liquidation_vs_stop_warning,
    )
    interpretation = get_interpretation(
        safety_status=safety_status,
        leverage=payload.leverage,
        liquidation_vs_stop_warning=liquidation_vs_stop_warning,
    )

    return RiskResult(
        risk_per_unit=risk_per_unit,
        max_risk_amount=max_risk_amount,
        position_size_units=position_size_units,
        notional_position_value=notional_position_value,
        margin_required=margin_required,
        money_at_risk=money_at_risk,
        account_risk_percent=account_risk_percent,
        liquidation_price=liquidation_price,
        distance_to_stop_percent=distance_to_stop_percent,
        distance_to_liquidation_percent=distance_to_liquidation_percent,
        liquidation_vs_stop_warning=liquidation_vs_stop_warning,
        safety_status=safety_status,
        warnings=warnings,
        interpretation=interpretation,
    )


def get_safety_status(account_risk_percent: float) -> str:
    if account_risk_percent <= 1:
        return "Conservative"
    if account_risk_percent <= 3:
        return "Moderate"
    return "High Risk"


def get_warnings(
    margin_required: float,
    account_balance: float,
    leverage: float,
    liquidation_vs_stop_warning: bool,
) -> list[str]:
    warnings: list[str] = []
    if margin_required > account_balance:
        warnings.append("Margin required exceeds account balance.")
    if liquidation_vs_stop_warning:
        warnings.append("Liquidation is closer than your stop loss.")
    if leverage > 20:
        warnings.append("Leverage is above 20x.")
    warnings.append("Liquidation estimate is approximate.")
    return warnings


def get_interpretation(
    safety_status: str,
    leverage: float,
    liquidation_vs_stop_warning: bool,
) -> str:
    if liquidation_vs_stop_warning:
        return (
            "This setup is dangerous because liquidation is closer than your stop loss. "
            "Reduce position size or leverage before entering."
        )
    if leverage > 20:
        return "This setup is acceptable, but leverage is high."
    if safety_status == "High Risk":
        return "Reduce position size or risk percentage before entering."
    return "This setup fits your chosen risk level."
