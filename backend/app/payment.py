from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from .database import SessionLocal
from .models import Payment
from .schemas import PaymentCreate
from services.cashfree_service import create_cashfree_order

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-payment")
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    try:
        order_id = "ORD_" + str(uuid.uuid4())[:8]

        cf_response = create_cashfree_order(
            order_id,
            data.amount,
            data.customer_id,
            data.phone,
            data.email
        )

        print("Cashfree Response:", cf_response)

        if not cf_response or "payment_session_id" not in cf_response:
            return {
                "error": "Cashfree Error",
                "details": cf_response
            }

        payment = Payment(
            order_id=order_id,
            amount=data.amount,
            status="PENDING",
            payment_session_id=cf_response.get("payment_session_id")
        )

        db.add(payment)
        db.commit()

        return {
            "payment_session_id": cf_response.get("payment_session_id"),
            "order_id": order_id
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}