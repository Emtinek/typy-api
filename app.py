from flask import Flask, jsonify
from forebet_scraper import get_forebet_predictions

app = Flask(__name__)

@app.route("/typy")
def typy():
    get_forebet_predictions()
    with open("matches.json", encoding="utf-8") as f:
        data = f.read()
    return jsonify(data)

if __name__ == "__main__":
    app.run()
