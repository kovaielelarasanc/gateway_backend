from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Payment
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        print("🔥 WEBHOOK HIT 🔥")

        data = await request.json()
        print("Webhook Data:", data)

        order_id = data.get("data", {}).get("order", {}).get("order_id")
        payment_status = data.get("data", {}).get("payment", {}).get("payment_status")
        cf_payment_id = data.get("data", {}).get("payment", {}).get("cf_payment_id")

        if not order_id:
            print("Order ID missing in webhook")
            return JSONResponse(content={"status": "ignored"}, status_code=200)

        payment = db.query(Payment).filter(Payment.order_id == order_id).first()

        if payment:
            payment.status = payment_status
            payment.cf_payment_id = str(cf_payment_id)
            db.commit()
            print("✅ DB UPDATED")
        else:
            print("Order not found")

        return JSONResponse(content={"status": "success"}, status_code=200)

    except Exception as e:
        print("Webhook Error:", str(e))
        return JSONResponse(content={"status": "error"}, status_code=200)