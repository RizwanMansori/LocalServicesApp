from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

services = [
    {"name": "Electrician", "contact": "999111222"},
    {"name": "Plumber", "contact": "999333444"},
    {"name": "Carpenter", "contact": "999555666"},
]

# DATABASE CREATE
def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings
                 (name TEXT, phone TEXT, service TEXT, address TEXT)""")
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
    service = request.form["service"]
    address = request.form["address"]

    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute("INSERT INTO bookings VALUES (?,?,?,?)",(name,phone,service,address))
    conn.commit()
    conn.close()

    return render_template("index.html", services=services)

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
    data = c.fetchall()
    conn.close()

    return render_template("admin.html", bookings=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
