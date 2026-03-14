from flask import Flask, render_template, request

app = Flask(__name__)

services = [
    {"name": "Electrician", "contact": "999-111-222"},
    {"name": "Plumber", "contact": "999-333-444"},
    {"name": "Carpenter", "contact": "999-555-666"},
]

# bookings list
bookings = []

@app.route("/")
def home():
    return render_template("index.html", services=services)

@app.route("/contact", methods=["POST"])
def contact():
    return render_template("index.html", services=services, success=True)

@app.route("/booking", methods=["POST"])
def booking():
    name = request.form["name"]
    phone = request.form["phone"]
    service = request.form["service"]
    address = request.form["address"]

    bookings.append({
        "name": name,
        "phone": phone,
        "service": service,
        "address": address
    })

    return render_template("index.html", services=services)

# ADMIN PANEL
@app.route("/admin")
def admin():
    return render_template("admin.html", bookings=bookings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
