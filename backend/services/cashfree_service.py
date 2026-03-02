import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

MODE = os.getenv("CASHFREE_MODE", "sandbox")

# Auto switch base URL
if MODE == "production":
    BASE_URL = "https://api.cashfree.com"
else:
    BASE_URL = "https://sandbox.cashfree.com"

APP_ID = os.getenv("CASHFREE_APP_ID")
SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY")

# 🔥 IMPORTANT: Your current ngrok webhook URL
WEBHOOK_URL = os.getenv("CASHFREE_WEBHOOK_URL")


def create_cashfree_order(order_id, order_amount, customer_id, customer_phone, customer_email):

    url = f"{BASE_URL}/pg/orders"

    headers = {
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY,
        "x-api-version": "2022-09-01"
    }

    payload = {
        "order_id": order_id,
        "order_amount": order_amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": customer_id,
            "customer_phone": customer_phone,
            "customer_email": customer_email
        },
        "order_meta": {
            "notify_url": WEBHOOK_URL
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Cashfree Response:", response.json())

    return response.json()