from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/typy")
def typy():
    with open("matches.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)