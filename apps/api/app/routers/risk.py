from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import RiskRequest, RiskResponse
from app.services.risk import calculate_risk


router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.post("/calculate", response_model=RiskResponse)
def calculate(payload: RiskRequest, db: Session = Depends(get_db)) -> RiskResponse:
    result = calculate_risk(payload)
    record = models.Calculation(
        direction=payload.direction,
        account_balance=payload.account_balance,
        entry_price=payload.entry_price,
        stop_price=payload.stop_price,
        leverage=payload.leverage,
        risk_percent=payload.risk_percent,
        outputs=result.model_dump(),
        client_metadata=payload.client_metadata,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return RiskResponse(calculation_id=record.id, result=result)
