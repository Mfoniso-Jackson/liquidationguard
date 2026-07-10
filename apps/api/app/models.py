from datetime import UTC, datetime
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def new_id() -> str:
    return str(uuid4())


def now_utc() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)

    calculations: Mapped[list["Calculation"]] = relationship(back_populates="user")


class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"), nullable=True)
    direction: Mapped[str] = mapped_column(String, nullable=False)
    account_balance: Mapped[float] = mapped_column(Float, nullable=False)
    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    stop_price: Mapped[float] = mapped_column(Float, nullable=False)
    leverage: Mapped[float] = mapped_column(Float, nullable=False)
    risk_percent: Mapped[float] = mapped_column(Float, nullable=False)
    outputs: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    client_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)

    user: Mapped[Optional[User]] = relationship(back_populates="calculations")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class WaitlistSignup(Base):
    __tablename__ = "waitlist_signups"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    trader_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    desired_feature: Mapped[Optional[str]] = mapped_column(String, nullable=True)
