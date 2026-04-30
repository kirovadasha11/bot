from flask import Flask
import os
from google import genai

app = Flask(__name__)

@app.route("/")
def home():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    models = client.models.list()
    return "<br>".join([m.name for m in models])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)