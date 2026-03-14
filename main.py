from flask import Flask, render_template, request

app = Flask(name)

Services data

services = [
{"name": "Electrician", "contact": "999-111-222"},
{"name": "Plumber", "contact": "999-333-444"},
{"name": "Carpenter", "contact": "999-555-666"},
]

@app.route("/")
def home():
return render_template("index.html", services=services)

Contact form

@app.route("/contact", methods=["POST"])
def contact():
name = request.form.get("name")
email = request.form.get("email")
message = request.form.get("message")

print(f"New message from {name} ({email}): {message}")

return render_template("index.html", services=services, success=True)

Booking form

@app.route("/booking", methods=["POST"])
def booking():
name = request.form.get("name")
phone = request.form.get("phone")
service = request.form.get("service")
address = request.form.get("address")

print(f"Booking: {name}, {phone}, {service}, {address}")

return "Booking Received!"

if name == "main":
app.run(debug=True)
