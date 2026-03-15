import os
from flask import Flask, render_template, request, redirect, url_for, session
import urllib.parse

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# Services and bookings
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

@app.route("/contact", methods=["POST"])
def contact():
    return render_template("index.html", services=services, success=True)

@app.route("/booking", methods=["POST"])
def booking():
    name = request.form["name"]
    phone = request.form["phone"]
    service = request.form["service"]
    address = request.form["address"]

    bookings.append({"name": name, "phone": phone, "service": service, "address": address})

    # WhatsApp notification (console)
    text = f"New Booking:\nName: {name}\nPhone: {phone}\nService: {service}\nAddress: {address}"
    whatsapp_url = f"https://wa.me/919876543210?text={urllib.parse.quote(text)}"
    print("WhatsApp URL:", whatsapp_url)

    return render_template("index.html", services=services, booking_success=True)

# Admin login & panel
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
    return render_template("admin.html", bookings=bookings, service_count=service_count)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))

@app.route("/delete_booking/<int:index>")
def delete_booking(index):
    if 0 <= index < len(bookings):
        bookings.pop(index)
    return redirect(url_for("admin"))

@app.route("/add_service", methods=["GET", "POST"])
def add_service():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        services.append({"name": name, "contact": contact})
        return render_template("add_service.html", success=True, service_name=name)
    
    return render_template("add_service.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
