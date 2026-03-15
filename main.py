from flask import Flask, render_template, request, redirect, url_for
import urllib.parse

app = Flask(__name__)

# Services data
services = [
    {"name": "Electrician", "contact": "9876543210"},
    {"name": "Plumber", "contact": "9876543211"},
    {"name": "Carpenter", "contact": "9876543212"},
    {"name": "AC Repair", "contact": "9876543213"}
]

# Booking storage
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

    # WhatsApp notification link
    text = f"New Booking:\nName: {name}\nPhone: {phone}\nService: {service}\nAddress: {address}"
    whatsapp_url = f"https://wa.me/919193626374?text={urllib.parse.quote(text)}"
    print("WhatsApp URL:", whatsapp_url)

    return render_template("index.html", services=services, booking_success=True)

# ---------------- Admin Panel ----------------
@app.route("/admin")
def admin():
    # Count bookings per service
    service_count = {}
    for s in services:
        service_count[s['name']] = sum(1 for b in bookings if b['service'] == s['name'])
    return render_template("admin.html", bookings=bookings, service_count=service_count)

@app.route("/delete_booking/<int:index>")
def delete_booking(index):
    if 0 <= index < len(bookings):
        bookings.pop(index)
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)
