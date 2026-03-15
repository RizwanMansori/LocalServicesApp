from flask import Flask, render_template, request
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
    whatsapp_url = f"https://wa.me/919876543210?text={urllib.parse.quote(text)}"
    print("WhatsApp URL:", whatsapp_url)

    return render_template("index.html", services=services, booking_success=True)
