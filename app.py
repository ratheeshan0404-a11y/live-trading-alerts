import os
import requests
from fastapi import FastAPI

app = FastAPI()

ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", "YOUR_ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY", "YOUR_ONESIGNAL_API_KEY")


def send_push_notification(title, message):
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "headings": {"en": title},
        "contents": {"en": message},
    }
    req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=header,
        json=payload,
    )
    return req.status_code


@app.get("/")
def read_root():
    return {"status": "Trading Alert Server is Running Live!"}


@app.get("/trigger-alert")
def trigger_alert(price: float = 4150.0, rsi: float = 75.0):
    status = send_push_notification(
        "🚨 MARKET ALERT!",
        f"Gold Price: {price} | RSI reached {rsi} (Overbought Signal)",
    )
    return {"message": "Notification sent!", "status_code": status}
  
