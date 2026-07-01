from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User

staff = Blueprint("staff", __name__)

@staff.route("/staff/dashboard")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])
    return render_template("staff/dashboard.html", user=user)