from flask import Flask, jsonify
from forebet_scraper import get_forebet_predictions
import os
import json

app = Flask(__name__)

@app.route("/typy")
def typy():
    try:
        get_forebet_predictions()
    except Exception as e:
        return jsonify({"error": f"Błąd w scraperze: {str(e)}"}), 500

    if not os.path.exists("matches.json"):
        return jsonify({"error": "Nie znaleziono pliku matches.json"}), 500

    with open("matches.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
