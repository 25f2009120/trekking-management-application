from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

authentication = Blueprint('authentication', __name__)

#Routes

@authentication.route("/")
def index():
    return render_template("index.html")

@authentication.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == "staff" and not user.is_approved:
                flash("You are not approved")
                return redirect(url_for("authentication.login"))

            if user.is_blacklisted:
                flash("You are blacklisted")
                return redirect(url_for("authentication.login"))

            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif user.role == "staff":
                return redirect(url_for("staff.staff_dashboard"))
            else:
                return redirect(url_for("user.user_dashboard"))

        else:
            flash("Invalid username or password")
            return redirect(url_for("authentication.login"))

    return render_template("authentication/login.html")

@authentication.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("authentication.login"))

@authentication.route("/register/user", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email address already registered")
            return redirect(url_for("authentication.user_register"))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("authentication.user_register"))

        new_user = User(
            name=name,
            email = email,
            phone = phone,
            role = "user"
        )

        new_user.password_hash(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("authentication.login"))
    return render_template("authentication/user_registration.html")

@authentication.route("/register/staff", methods=["GET", "POST"])
def staff_register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email address already registered")
            return redirect(url_for("authentication.staff_register"))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("authentication.staff_register"))

        new_staff = User(
            name = name,
            email = email,
            phone = phone,
            role = "staff",
            is_approved = False
        )

        new_staff.password_hash(password)

        db.session.add(new_staff)
        db.session.commit()

        return redirect(url_for("authentication.login"))
    return render_template("authentication/staff_registration.html")