import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Flask Demo App!",
        "version": "1.0.0"
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": 'Field "message" is required'}), 400

    return jsonify({
        "echo": data["message"],
        "receivedAt": datetime.now(timezone.utc).isoformat()
    }), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
