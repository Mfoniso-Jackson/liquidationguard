from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import FeedbackRequest, FeedbackResponse


router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
def create_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)) -> FeedbackResponse:
    record = models.Feedback(
        rating=payload.rating,
        message=payload.message,
        email=str(payload.email) if payload.email else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return FeedbackResponse(id=record.id)
