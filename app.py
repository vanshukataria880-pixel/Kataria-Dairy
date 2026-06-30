from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "kataria_dairy_secret_2026"

# Database create function
def init_db():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            address TEXT,
            quantity TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/order")
def order():
    return render_template("order.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    mobile = request.form["mobile"]
    address = request.form["address"]
    quantity = request.form["quantity"]
    time = request.form["time"]

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO orders (name, mobile, address, quantity, time) VALUES (?, ?, ?, ?, ?)",
        (name, mobile, address, quantity, time)
    )

    conn.commit()
    conn.close()

    return "Order Saved Successfully ✅"


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "vanshu kataria" and password == "Kataria@211":
            session["admin"] = True
            return redirect("/admin")

        return "Wrong Username or Password"

    return render_template("login.html")


@app.route("/admin")
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    search = request.args.get("search", "")

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    if search:
        c.execute(
            "SELECT * FROM orders WHERE name LIKE ? OR mobile LIKE ?",
            (f"%{search}%", f"%{search}%")
        )
    else:
        c.execute("SELECT * FROM orders")

    orders = c.fetchall()

    total_orders = len(orders)

    conn.close()

    return render_template(
        "admin.html",
        orders=orders,
        total_orders=total_orders,
        search=search
    )
@app.route("/delete/<int:id>")
def delete(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("orders.db")
    c = conn.cursor()

    c.execute("DELETE FROM orders WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
