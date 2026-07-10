from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import WaitlistRequest, WaitlistResponse


router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])


@router.post("", response_model=WaitlistResponse)
def join_waitlist(payload: WaitlistRequest, db: Session = Depends(get_db)) -> WaitlistResponse:
    existing = (
        db.query(models.WaitlistSignup)
        .filter(models.WaitlistSignup.email == str(payload.email).lower())
        .one_or_none()
    )
    if existing:
        return WaitlistResponse(id=existing.id)

    record = models.WaitlistSignup(
        email=str(payload.email).lower(),
        trader_type=payload.trader_type,
        desired_feature=payload.desired_feature,
    )
    db.add(record)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(models.WaitlistSignup)
            .filter(models.WaitlistSignup.email == str(payload.email).lower())
            .one()
        )
        return WaitlistResponse(id=existing.id)

    db.refresh(record)
    return WaitlistResponse(id=record.id)
