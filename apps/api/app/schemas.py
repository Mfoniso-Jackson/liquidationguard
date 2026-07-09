from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field, model_validator


Direction = Literal["Long", "Short"]


class RiskRequest(BaseModel):
    account_balance: float = Field(gt=0)
    direction: Direction
    entry_price: float = Field(gt=0)
    stop_price: float = Field(gt=0)
    leverage: float = Field(ge=1)
    risk_percent: float = Field(gt=0, le=10, default=2)
    client_metadata: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_stop_direction(self) -> "RiskRequest":
        if self.stop_price == self.entry_price:
            raise ValueError("Stop price must not equal entry price.")
        if self.direction == "Long" and self.stop_price >= self.entry_price:
            raise ValueError("For a Long trade, the stop price should be below entry price.")
        if self.direction == "Short" and self.stop_price <= self.entry_price:
            raise ValueError("For a Short trade, the stop price should be above entry price.")
        return self


class RiskResult(BaseModel):
    risk_per_unit: float
    max_risk_amount: float
    position_size_units: float
    notional_position_value: float
    margin_required: float
    money_at_risk: float
    account_risk_percent: float
    liquidation_price: float
    distance_to_stop_percent: float
    distance_to_liquidation_percent: float
    liquidation_vs_stop_warning: bool
    safety_status: Literal["Conservative", "Moderate", "High Risk"]
    warnings: list[str]
    interpretation: str


class RiskResponse(BaseModel):
    calculation_id: str | None = None
    result: RiskResult


class FeedbackRequest(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str | None = Field(default=None, max_length=2000)
    email: EmailStr | None = None


class FeedbackResponse(BaseModel):
    id: str
    status: Literal["received"] = "received"
