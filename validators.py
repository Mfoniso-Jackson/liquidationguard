"""Input validation for LiquidationGuard."""


def validate_inputs(
    account_balance: float,
    direction: str,
    entry_price: float,
    stop_price: float,
    leverage: float,
    risk_percent: float,
) -> list[str]:
    """Validate user inputs and return a list of friendly error messages."""
    errors = []

    if account_balance <= 0:
        errors.append("Account balance must be greater than 0.")
    if entry_price <= 0:
        errors.append("Entry price must be greater than 0.")
    if stop_price <= 0:
        errors.append("Stop price must be greater than 0.")
    if leverage < 1:
        errors.append("Leverage must be at least 1x.")
    if risk_percent <= 0 or risk_percent > 10:
        errors.append("Risk percentage must be greater than 0 and no more than 10.")

    if entry_price > 0 and stop_price > 0:
        if stop_price == entry_price:
            errors.append("Stop price must not equal entry price.")
        elif direction == "Long" and stop_price >= entry_price:
            errors.append("For a Long trade, the stop price should be below entry price.")
        elif direction == "Short" and stop_price <= entry_price:
            errors.append("For a Short trade, the stop price should be above entry price.")

    return errors
