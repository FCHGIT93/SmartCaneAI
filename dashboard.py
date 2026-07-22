from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

latest_data = {
    "object": "None",
    "danger": "SAFE",
    "direction": "None",
    "decision": "Path clear",
    "count": 0,
    "left_status": "CLEAR",
    "front_status": "CLEAR",
    "right_status": "CLEAR",
    "last_voice": "Path clear",
    "history": [],
    "stats": {
        "person": 0,
        "chair": 0,
        "car": 0,
        "bottle": 0,
        "backpack": 0,
        "cell phone": 0,
        "bench": 0,
        "couch": 0
    },
    "timeline": []
}


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/data")
def data():
    return jsonify(latest_data)


@app.route("/update", methods=["POST"])
def update():
    global latest_data

    new_data = request.json
    current_time = datetime.now().strftime("%H:%M:%S")

    latest_data.update(new_data)

    obj = new_data.get("object", "None")
    danger = new_data.get("danger", "SAFE")

    if obj in latest_data["stats"]:
        latest_data["stats"][obj] += 1

    history_item = {
        "time": current_time,
        "object": obj,
        "danger": danger,
        "direction": new_data.get("direction", "None"),
        "decision": new_data.get("decision", "Path clear"),
        "count": new_data.get("count", 0)
    }

    latest_data["history"].insert(0, history_item)

    if len(latest_data["history"]) > 12:
        latest_data["history"] = latest_data["history"][:12]

    danger_score = 10
    if danger == "WARNING":
        danger_score = 55
    elif danger == "CRITICAL":
        danger_score = 95

    latest_data["timeline"].append({
        "time": current_time,
        "danger_score": danger_score
    })

    if len(latest_data["timeline"]) > 20:
        latest_data["timeline"] = latest_data["timeline"][-20:]

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    