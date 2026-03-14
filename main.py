from flask import Flask, render_template, request

app = Flask(name)

services = [
{"name": "Electrician", "contact": "999-111-222"},
{"name": "Plumber", "contact": "999-333-444"},
{"name": "Carpenter", "contact": "999-555-666"},
]

@app.route("/")
def home():
return render_template("index.html", services=services)

@app.route("/contact", methods=["POST"])
def contact():
name = request.form.get("name")
email = request.form.get("email")
message = request.form.get("message")

print(name, email, message)

return render_template("index.html", services=services, success=True)

@app.route("/booking", methods=["POST"])
def booking():
name = request.form.get("name")
phone = request.form.get("phone")
service = request.form.get("service")
address = request.form.get("address")

print(name, phone, service, address)

return render_template("index.html", services=services)

if name == "main":
app.run(host="0.0.0.0", port=10000)
