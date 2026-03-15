import os
from flask import Flask, render_template, request, redirect, url_for, session
import urllib.parse

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- Sample services ----------------
services = [
    {"name": "Electrician", "contact": "9876543210"},
    {"name": "Plumber", "contact": "9876543211"},
    {"name": "Carpenter", "contact": "9876543212"},
    {"name": "AC Repair", "contact": "9876543213"}
]

bookings = []

@app.route("/")
def home():
    return render_template("index.html", services=services)

# ---------------- PORT fix for Render ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
