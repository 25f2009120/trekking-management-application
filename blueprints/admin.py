from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])
    return render_template("admin/dashboard.html", user=user)

@admin.route("/admin/staff-approvals")
def staff_approvals():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    unapproved_staff = User.query.filter_by(role="staff", is_approved=False).all()

    return render_template("admin/staff_approvals.html", unapproved_staff=unapproved_staff)

@admin.route("/admin/approve-staff/<int:user_id>")
def approve_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    staff = User.query.get(user_id)

    if staff and staff.role == "staff":
        staff.is_approved = True
        db.session.commit()
        flash("Staff approved")
    else:
        flash("Staff not found")

    return redirect(url_for("addmin.staff_approvals"))

@admin.route("/admin/staff")
def admin_staff():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    staff = User.query.filter_by(role="staff").all()

    return render_template("admin/staff.html", staff=staff)

@admin.route("/admin/blacklist-staff/<int:user_id>")
def blacklist_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    staff = User.query.get(user_id)

    if staff:
        staff.is_blacklisted = True
        db.session.commit()
        flash("Staff blacklisted")
    else:
        flash("Staff not found")

    return redirect(url_for("addmin.admin_staff"))

@admin.route("/admin/unblacklist-staff/<int:user_id>")
def unblacklist_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    staff = User.query.get(user_id)

    if staff:
        staff.is_blacklisted = False
        db.session.commit()
        flash("Staff unblacklisted")
    else:
        flash("Staff not found")

    return redirect(url_for("addmin.admin_staff"))

@admin.route("/admin/users")
def admin_users():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    users = User.query.filter_by(role="user").all()

    return render_template("admin/users.html", users=users)

@admin.route("/admin/blacklist/<int:user_id>")
def blacklist_user(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))


    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = True
        db.session.commit()
        flash("Blacklisted")
    else:
        flash("User not found")

    return redirect(url_for("addmin.admin_users"))

@admin.route("/admin/unblacklist/<int:user_id>")
def unblacklist_user(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = False
        db.session.commit()
        flash("Unblacklisted")
    else:
        flash("User not found")

    return redirect(url_for("addmin.admin_users"))