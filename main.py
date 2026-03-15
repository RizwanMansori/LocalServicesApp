import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
import urllib.parse

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# Services
services = [
    {"name": "Electrician", "contact": "9876543210"},
    {"name": "Plumber", "contact": "9876543211"},
    {"name": "Carpenter", "contact": "9876543212"},
    {"name": "AC Repair", "contact": "9876543213"}
]

# JSON file for bookings
BOOKING_FILE = "bookings.json"
try:
    with open(BOOKING_FILE, "r") as f:
        bookings = json.load(f)
except:
    bookings = []

# -------- Home Page --------
@app.route("/")
def home():
    return render_template("index.html", services=services)

@app.route("/contact", methods=["POST"])
def contact():
    return render_template("index.html", services=services, success=True)

@app.route("/booking", methods=["POST"])
def booking():
    name = request.form.get("name")
    phone = request.form.get("phone")
    service = request.form.get("service")
    address = request.form.get("address")

    bookings.append({"name": name, "phone": phone, "service": service, "address": address})
    with open(BOOKING_FILE, "w") as f:
        json.dump(bookings, f)

    # WhatsApp notification (console)
    text = f"New Booking:\nName: {name}\nPhone: {phone}\nService: {service}\nAddress: {address}"
    whatsapp_url = f"https://wa.me/919876543210?text={urllib.parse.quote(text)}"
    print("WhatsApp URL:", whatsapp_url)

    return render_template("index.html", services=services, booking_success=True)

# -------- Admin Panel --------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    if not session.get("admin_logged_in"):
        return render_template("admin_login.html")

    service_count = {s["name"]: sum(1 for b in bookings if b["service"] == s["name"]) for s in services}
    return render_template("admin.html", bookings=bookings, service_count=service_count, services=services)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))

# -------- Delete Booking --------
@app.route("/delete_booking/<int:index>")
def delete_booking(index):
    if 0 <= index < len(bookings):
        bookings.pop(index)
        with open(BOOKING_FILE, "w") as f:
            json.dump(bookings, f)
    return redirect(url_for("admin"))

# -------- Add Service --------
@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")
        services.append({"name": name, "contact": contact})
        return render_template("add_service.html", success=True, service_name=name)

    return render_template("add_service.html")

# -------- Remove Service --------
@app.route("/delete_service/<int:index>")
def delete_service(index):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if 0 <= index < len(services):
        services.pop(index)
    return redirect(url_for("admin"))

# -------- Run App --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
