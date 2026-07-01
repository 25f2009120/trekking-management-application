from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Trek, Booking, TrekImage

app = Flask(__name__)

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Treeking_Management_Application"
db.init_app(app)

#Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == "staff" and not user.is_approved:
                flash("You are not approved")
                return redirect(url_for("login"))

            if user.is_blacklisted:
                flash("You are blacklisted")
                return redirect(url_for("login"))

            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user.role == "staff":
                return redirect(url_for("staff_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))

        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))

    return render_template("authentication/login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.route("/register/user", methods=["GET", "POST"])
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
            return redirect(url_for("user_register"))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("user_register"))

        new_user = User(
            name=name,
            email = email,
            phone = phone,
            password = generate_password_hash(password),
            role = "user"
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("authentication/user_registration.html")

@app.route("/register/staff", methods=["GET", "POST"])
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
            return redirect(url_for("staff_register"))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("staff_register"))

        new_staff = User(
            name = name,
            email = email,
            phone = phone,
            password = generate_password_hash(password),
            role = "staff",
            is_approved = False
        )
        db.session.add(new_staff)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("authentication/staff_registration.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("admin/dashboard.html", user=user)

@app.route("/admin/staff-approvals")
def staff_approvals():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    unapproved_staff = User.query.filter_by(role="staff", is_approved=False).all()

    return render_template("admin/staff_approvals.html", unapproved_staff=unapproved_staff)

@app.route("/admin/approve-staff/<int:user_id>")
def approve_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    staff = User.query.get(user_id)

    if staff and staff.role == "staff":
        staff.is_approved = True
        db.session.commit()
        flash("Staff approved")
    else:
        flash("Staff not found")

    return redirect(url_for("staff_approvals"))

@app.route("/admin/users")
def admin_users():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    uses = User.query.filter_by(role="user").all()

    return render_template("admin/users.html", users=users)

@app.route("/admin/blacklist/<int:user_id>")
def blacklist_user(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))


    if session["role"] != "admin":
        return redirect(url_for("login"))

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = True
        db.session.commit()
        flash("Blacklisted")
    else:
        flash("User not found")

    return redirect(url_for("admin_users"))

@app.route("/admin/unblacklist/<int:user_id>")
def unblacklist_user(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = False
        db.session.commit()
        flash("Unblacklisted")
    else:
        flash("User not found")

    return redirect(url_for("admin_users"))


@app.route("/staff/dashboard")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("staff/dashboard.html", user=user)

@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return render_template("user/dashboard.html", user=user)

@app.route("/users")
def users():
    users = User.query.all()
    output = ""
    for user in users:
        output += f"ID = {user.id}<br> name = {user.name}<br> email = {user.email}<br> phone = {user.phone}<br> password = {user.password}<br> role = {user.role}<br> created_at = {user.created_at}<br> is_approved = {user.is_approved}<br> is_blacklisted = {user.is_blacklisted}<br>"
    return output

@app.route("/delete-users")
def delete_users():
    User.query.delete()
    db.session.commit()
    return "All users deleted."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)