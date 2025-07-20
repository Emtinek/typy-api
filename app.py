from flask import Flask, jsonify
from forebet_scraper import get_forebet_predictions

app = Flask(__name__)

@app.route(typy)
def typy()
    matches = get_forebet_predictions()
    return jsonify(matches)
