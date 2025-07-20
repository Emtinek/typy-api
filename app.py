from flask import Flask, jsonify
from forebet_scraper import get_forebet_predictions
import os
import json

app = Flask(__name__)

@app.route("/typy")
def typy():
    get_forebet_predictions()

    if not os.path.exists("matches.json"):
        return jsonify({"error": "Nie znaleziono pliku matches.json"}), 500

    with open("matches.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
