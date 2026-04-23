from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.database import get_db
from app.models import PaymentTransaction, User
from app.schemas import PaymentCreate
from app.security import require_roles, ROLE_ADMIN, ROLE_SECRETARY, ROLE_TEACHER

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post("/payments")
def add_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_ADMIN, ROLE_SECRETARY, ROLE_TEACHER)),
):
    tx = PaymentTransaction(**payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return {
        "transaction_id": tx.id,
        "receipt_id": f"RCP-{tx.id:06d}",
        "amount": tx.amount,
    }


@router.get("/dashboard/monthly")
def monthly_dashboard(db: Session = Depends(get_db), _: User = Depends(require_roles(ROLE_ADMIN, ROLE_TEACHER))):
    income = db.scalar(select(func.coalesce(func.sum(PaymentTransaction.amount), 0.0)))
    expenses = 0.0
    return {
        "income": float(income or 0),
        "expenses": expenses,
        "net": float(income or 0) - expenses,
    }
