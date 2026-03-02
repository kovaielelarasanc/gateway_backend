from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), unique=True, index=True)
    amount = Column(Float)
    status = Column(String(50), default="PENDING")
    payment_session_id = Column(String(255))
    cf_payment_id = Column(String(255), nullable=True)