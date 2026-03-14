from flask import Flask, render_template, request

app = Flask(__name__)

# Sample services data
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
    print(f"New message from {name} ({email}): {message}")
    return render_template("index.html", services=services, success=True)

if __name__ == "__main__":
    app.run(debug=True)