from flask import Blueprint, render_template, request, redirect, session, url_for
from database import get_db

auth = Blueprint("auth", __name__)

@auth.route("/")
def home():
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                     (name, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("crud.dashboard"))
        else:
            return "Invalid credentials"

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))