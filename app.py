from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)

# ── Simulated in-memory data store ──────────────────────────────────────────
user_profile = {
    "name": "Alex",
    "age": 28,
    "weight": 72,
    "height": 175,
    "goal_steps": 10000,
    "goal_calories": 2200,
    "goal_sleep": 8,
    "goal_water": 8
}

def generate_weekly_data():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "steps":    [random.randint(5000, 14000) for _ in days],
        "calories": [random.randint(1600, 2800) for _ in days],
        "sleep":    [round(random.uniform(5.5, 9.0), 1) for _ in days],
        "heart_rate":[random.randint(58, 95) for _ in days],
        "days": days
    }

def live_vitals():
    return {
        "heart_rate":   random.randint(62, 88),
        "steps":        random.randint(3000, 11000),
        "calories":     random.randint(800, 2400),
        "sleep":        round(random.uniform(5.0, 9.0), 1),
        "blood_pressure": f"{random.randint(110,130)}/{random.randint(70,85)}",
        "spo2":         random.randint(96, 100),
        "water_intake": random.randint(2, 9),
        "temperature":  round(random.uniform(36.4, 37.2), 1),
        "timestamp":    datetime.now().strftime("%H:%M:%S")
    }

alerts_store = [
    {"type": "warning",  "icon": "⚠️",  "msg": "Heart rate elevated — 102 bpm detected",  "time": "2 min ago"},
    {"type": "info",     "icon": "💊",  "msg": "Time for your evening medication",          "time": "15 min ago"},
    {"type": "success",  "icon": "🎯",  "msg": "Step goal achieved! 10,243 steps today",   "time": "1 hr ago"},
    {"type": "info",     "icon": "💧",  "msg": "Drink water — hydration below target",      "time": "2 hr ago"},
]

# ── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", profile=user_profile)

@app.route("/api/vitals")
def api_vitals():
    return jsonify(live_vitals())

@app.route("/api/weekly")
def api_weekly():
    return jsonify(generate_weekly_data())

@app.route("/api/alerts")
def api_alerts():
    return jsonify(alerts_store)

@app.route("/api/profile", methods=["GET","POST"])
def api_profile():
    global user_profile
    if request.method == "POST":
        data = request.get_json(force=True)
        user_profile.update(data)
        return jsonify({"status": "ok", "profile": user_profile})
    return jsonify(user_profile)

@app.route("/api/ai_tip")
def api_ai_tip():
    tips = [
        "Your resting heart rate improved by 3 bpm this week — great cardiovascular progress! 🏃",
        "You're averaging 7.2 hrs of sleep. Try for 8 hrs tonight for better recovery.",
        "Step count dipped Wednesday. Short 10-min walks after meals can help reach your goal.",
        "Your calorie burn is trending up — ensure adequate protein intake for muscle repair.",
        "Hydration has been low the past 2 days. Aim for 8 glasses before 9 PM.",
        "Blood pressure readings are within healthy range. Keep up the stress management!",
        "You're 85% towards your weekly fitness score — one more active session will do it!"
    ]
    return jsonify({"tip": random.choice(tips)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
