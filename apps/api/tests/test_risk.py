import pytest
from pydantic import ValidationError

from app.schemas import RiskRequest
from app.services.risk import calculate_risk


def test_long_trade_calculation():
    payload = RiskRequest(
        account_balance=1000,
        direction="Long",
        entry_price=100,
        stop_price=95,
        leverage=10,
        risk_percent=2,
    )

    result = calculate_risk(payload)

    assert result.risk_per_unit == 5
    assert result.position_size_units == 4
    assert result.notional_position_value == 400
    assert result.margin_required == 40
    assert result.money_at_risk == 20
    assert result.account_risk_percent == 2
    assert result.liquidation_price == 90
    assert result.distance_to_stop_percent == 5
    assert result.distance_to_liquidation_percent == 10
    assert result.safety_status == "Moderate"


def test_short_trade_calculation():
    payload = RiskRequest(
        account_balance=5000,
        direction="Short",
        entry_price=2000,
        stop_price=2100,
        leverage=20,
        risk_percent=1,
    )

    result = calculate_risk(payload)

    assert result.position_size_units == 0.5
    assert result.liquidation_price == 2100
    assert result.safety_status == "Conservative"


def test_liquidation_closer_than_stop_warning():
    payload = RiskRequest(
        account_balance=1000,
        direction="Long",
        entry_price=100,
        stop_price=80,
        leverage=10,
        risk_percent=2,
    )

    result = calculate_risk(payload)

    assert result.liquidation_vs_stop_warning is True
    assert "Liquidation is closer than your stop loss." in result.warnings
    assert "dangerous" in result.interpretation


def test_invalid_long_stop_direction():
    with pytest.raises(ValidationError):
        RiskRequest(
            account_balance=1000,
            direction="Long",
            entry_price=100,
            stop_price=105,
            leverage=10,
            risk_percent=2,
        )


def test_invalid_risk_percent_limit():
    with pytest.raises(ValidationError):
        RiskRequest(
            account_balance=1000,
            direction="Short",
            entry_price=100,
            stop_price=105,
            leverage=10,
            risk_percent=11,
        )
