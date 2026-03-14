from flask import Flask, render_template, request, redirect, session
import sqlite3
import urllib.parse

app = Flask(__name__)
app.secret_key = "secret"  # Admin session secret

# Services data
services = [
    {"name": "Electrician", "contact": "999111222"},
    {"name": "Plumber", "contact": "999333444"},
    {"name": "Carpenter", "contact": "999555666"},
]

# Initialize database
def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            name TEXT,
            phone TEXT,
            service TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html", services=services)

# Contact form
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    print(f"New message from {name} ({email}): {message}")
    return render_template("index.html", services=services, success=True)

# Booking form
@app.route("/booking", methods=["POST"])
def booking():
    name = request.form["name"]
    phone = request.form["phone"]
    service = request.form["service"]
    address = request.form["address"]

    # Save booking to SQLite
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings VALUES (?,?,?,?)", (name, phone, service, address))
    conn.commit()
    conn.close()

    # WhatsApp notification URL
    whatsapp_number = "919193626374"  # Change to your number
    message = f"New Booking!\nName: {name}\nPhone: {phone}\nService: {service}\nAddress: {address}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

    print("WhatsApp URL:", whatsapp_url)  # Logs में देख सकते हो

    return render_template("index.html", services=services)

# Admin login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

# Admin panel
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    data = c.fetchall()  # Tuple list [(name, phone, service, address), ...]
    conn.close()

    return render_template("admin.html", bookings=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
