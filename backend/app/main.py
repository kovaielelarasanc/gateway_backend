from fastapi import FastAPI
from .database import Base, engine
from .payment import router as payment_router
from .webhook import router as webhook_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router, prefix="/payment", tags=["Payment"])
app.include_router(webhook_router, prefix="/payment", tags=["Webhook"])