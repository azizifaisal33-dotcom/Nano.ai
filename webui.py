
from flask import Flask, jsonify, request
from core.memory import memory
import subprocess

app = Flask(__name__)


# =========================
# STATUS
# =========================
@app.route("/")
def home():
    return "🧠 NanoAI OS Running"


# =========================
# MEMORY VIEW
# =========================
@app.route("/memory")
def get_memory():
    return jsonify(memory.stats())


# =========================
# SEARCH MEMORY
# =========================
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return jsonify(memory.search(q))


# =========================
# RUN COMMAND
# =========================
@app.route("/run", methods=["POST"])
def run():
    data = request.json
    cmd = data.get("cmd")

    try:
        result = subprocess.getoutput(cmd)
        return jsonify({"output": result})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)