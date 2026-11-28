from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# --------------------------------
# USER MODEL
# --------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )


# --------------------------------
# FICTIONAL BANK ACCOUNT MODEL
# --------------------------------

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        server_default=text("0.00")
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        server_default=text("'INR'")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="ck_accounts_nonnegative_balance"
        ),
        CheckConstraint(
            "currency = 'INR'",
            name="ck_accounts_inr_currency"
        ),
    )
