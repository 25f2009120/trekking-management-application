from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User, Trek, TrekImage, Booking
from datetime import datetime

staff = Blueprint("staff", __name__)

@staff.route("/staff/dashboard")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])
    assigned_treks = Trek.query.filter_by(staff_id=user.id).all()

    total_treks = len(assigned_treks)
    total_participants = sum(trek.bookings.count() for trek in assigned_treks)

    pending_treks = sum(1 for t in assigned_treks if t.status == "Pending")
    approved_treks = sum(1 for t in assigned_treks if t.status == "Approved")
    completed_treks = sum(1 for t in assigned_treks if t.status == "Completed")
    canceled_treks = sum(1 for t in assigned_treks if t.status == "Canceled")

    return render_template(
        "staff/dashboard.html",
        user=user,
        total_treks = total_treks,
        total_participants = total_participants,
        pending_treks = pending_treks,
        approved_treks = approved_treks,
        completed_treks = completed_treks,
        canceled_treks = canceled_treks
    )

@staff.route("/staff/treks")
def staff_treks():

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = Trek.query.filter_by(staff_id=session["user_id"])

    if search:
        query = query.filter(
            Trek.name.ilike(f"%{search}%") |
            Trek.location.ilike(f"%{search}%")
        )

    if status:
        query = query.filter_by(status=status)

    treks = query.all()

    return render_template(
        "staff/treks.html",
        treks = treks,
        search = search,
        status = status
    )

@staff.route("/staff/treks/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)

    if not trek:
        flash("Trek not found")
        return redirect(url_for("staff.staff_treks"))

    if trek.staff_id != session["user_id"]:
        flash("You are not authorized to edit this trek")
        return redirect(url_for("staff.staff_treks"))

    if request.method == "POST":
        trek.status = request.form["status"]
        trek.available_slots = request.form["available_slots"]
        db.session.commit()
        flash("Trek updated")
        return redirect(url_for("staff.staff_treks"))

    return render_template("staff/edit_trek.html", trek = trek)

@staff.route("/staff/treks/<int:trek_id>/participants")
def trek_participants(trek_id):

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)

    if not trek:
        flash("Trek not found")
        return redirect(url_for("staff.staff_treks"))

    if trek.staff_id != session["user_id"]:
        flash("You are not authorized to edit this trek")
        return redirect(url_for("staff.staff_treks"))

    bookings = trek.bookings.all()

    return render_template(
        "staff/participants.html",
        bookings = bookings,
        trek = trek,
    )

@staff.route("/staff/treks/<int:trek_id>/participants/remove/<int:booking_id>")
def remove_participant(trek_id, booking_id):

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)

    if trek.staff_id != session["user_id"]:
        flash("You are not authorized to edit this trek")
        return redirect(url_for("staff.staff_treks"))

    booking = Booking.query.get(booking_id)

    if booking and booking.trek_id == trek_id:
        trek.available_slots += 1
        db.session.delete(booking)
        db.session.commit()
        flash("Participant removed")
    else:
        flash("Booking of Participant not found")

    return redirect(url_for("staff.trek_participants", trek_id=trek_id))

@staff.route("/staff/profile", methods=["GET", "POST"])
def staff_profile():

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "staff":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        existing = User.query.filter_by(phone=phone).first()
        if existing and existing.id != user.id:
            flash("Phone number already in used")
            return redirect(url_for("staff.staff_profile"))

        user.name = name
        user.phone = phone
        db.session.commit()
        flash("Profile updated")
        return redirect(url_for("staff.staff_profile"))

    return render_template("staff/profile.html", user = user)