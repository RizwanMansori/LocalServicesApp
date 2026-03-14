from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

services = [
    {"name": "Electrician", "contact": "999111222"},
    {"name": "Plumber", "contact": "999333444"},
    {"name": "Carpenter", "contact": "999555666"},
]

# Initialize DB
def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            service TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

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
    service_name = request.form["service"]
    address = request.form["address"]

    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, phone, service, address) VALUES (?, ?, ?, ?)",
              (name, phone, service_name, address))
    conn.commit()
    conn.close()

    # Optionally: WhatsApp URL trigger
    return render_template("index.html", services=services, booking_success=True)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/admin")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()

    c.execute("SELECT service, COUNT(*) FROM bookings GROUP BY service")
    counts = c.fetchall()
    conn.close()
    return render_template("admin.html", bookings=bookings, counts=counts)

@app.route("/delete/<int:id>")
def delete_booking(id):
    if not session.get("admin"):
        return redirect("/login")
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)
