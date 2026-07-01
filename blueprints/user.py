from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User

user = Blueprint("user", __name__)

@user.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])
    return render_template("user/dashboard.html", user=user)