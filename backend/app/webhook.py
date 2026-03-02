from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Payment

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):

    print("🔥 WEBHOOK HIT 🔥")

    data = await request.json()
    print("Webhook Data:", data)

    order_id = data["data"]["order"]["order_id"]
    payment_status = data["data"]["payment"]["payment_status"]
    cf_payment_id = str(data["data"]["payment"]["cf_payment_id"])

    print("Updating Order:", order_id)
    print("New Status:", payment_status)

    payment = db.query(Payment).filter(Payment.order_id == order_id).first()

    if payment:
        payment.status = payment_status
        payment.cf_payment_id = cf_payment_id
        db.commit()
        db.refresh(payment)
        print("✅ DB UPDATED")
    else:
        print("❌ Order not found in DB")

    return {"status": "success"}