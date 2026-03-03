from flask import Blueprint, render_template, request, redirect, session, url_for
from database import get_db

crud = Blueprint("crud", __name__)

def login_required():
    if "user_id" not in session:
        return False
    return True

@crud.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db()
    records = conn.execute(
        "SELECT * FROM records WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", records=records)

@crud.route("/add", methods=["POST"])
def add():
    if not login_required():
        return redirect(url_for("auth.login"))

    title = request.form.get("title")
    description = request.form.get("description")

    conn = get_db()
    conn.execute(
        "INSERT INTO records (title, description, user_id) VALUES (?, ?, ?)",
        (title, description, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("crud.dashboard"))

@crud.route("/delete/<int:id>")
def delete(id):
    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db()
    conn.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("crud.dashboard"))