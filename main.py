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

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "Rizvan" and password == "0786":
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
    bookings = c.fetchall()  # [(id, name, phone, service, address), ...]

    # Service-wise count
    c.execute("SELECT service, COUNT(*) FROM bookings GROUP BY service")
    counts = c.fetchall()  # [('Electrician', 3), ('Plumber',2), ...]

    conn.close()
    return render_template("admin.html", bookings=bookings, counts=counts)

# Delete booking
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
