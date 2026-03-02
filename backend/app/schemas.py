from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    payment_method: str

class PaymentCreate(BaseModel):
    amount: float
    customer_id: str
    phone: str
    email: str