from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    requests.post(f"{URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": f"Ты написал: {text}"
    })

    return "ok"

if __name__ == "__main__":
    app.run()