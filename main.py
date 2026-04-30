from flask import Flask, request
import requests
import os
from google import genai

TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

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
    word = data["message"].get("text", "").strip()

    prompt = f"""
Дай одну рифму к слову: {word}.

Требования:
- только одно слово
- без объяснений
- без пунктуации
- с маленькой буквы
- без заглавных букв
- без дополнительных символов
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    answer = (response.text or "").strip().split()[0].lower()

    requests.post(f"{URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": answer
    })

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)