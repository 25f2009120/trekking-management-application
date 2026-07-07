from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User, Trek, Booking
from datetime import datetime, date

user = Blueprint("user", __name__)

@user.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])

    bookings = user.bookings.filter_by(status="Booked").all()

    total_bookings = len(bookings)

    total_completed = sum(1 for booking in bookings if booking.trek.status == "Completed")

    today = datetime.today()

    upcoming_bookings = [
        booking for booking in bookings if booking.trek.status == "Approved" and booking.trek.start_date >= date.today()
    ]

    upcoming_bookings.sort(key=lambda booking: booking.trek.start_date)

    return render_template("user/dashboard.html", user=user, total_bookings=total_bookings, total_completed=total_completed, upcoming_bookings=upcoming_bookings)

@user.route("/user/treks")
def available_treks():

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")

    difficulty = request.args.get("difficulty", "")

    location = request.args.get("location", "")

    query = Trek.query.filter_by(status="Approved")

    if search:
        query = query.filter(
            Trek.name.ilike(f"%{search}%") | Trek.description.ilike(f"%{search}%") | Trek.location.ilike(f"%{search}%")
        )

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    treks = query.order_by(Trek.start_date.asc()).all()

    my_booked_trek_ids = {
        booking.trek_id for booking in Booking.query.filter_by(user_id=session["user_id"], status="Booked").all()
    }

    return render_template(
        "user/treks.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        location=location,
        my_booked_trek_ids=my_booked_trek_ids,
        today=date.today()
    )

@user.route("/user/treks/book/<int:trek_id>", methods=["POST"])
def book_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)

    if not trek:
        flash("Trek not found")
        return redirect(url_for("user.available_treks"))

    if trek.status != "Approved":
        flash("Trek not approved")
        return redirect(url_for("user.available_treks"))

    if trek.available_slots <= 0:
        flash("Trek is fully booked")
        return redirect(url_for("user.available_treks"))

    if trek.start_date < date.today():
        flash("Trek has already started")
        return redirect(url_for("user.available_treks"))

    existing = Booking.query.filter_by(user_id=session["user_id"], trek_id=trek_id, status="Booked").first()

    if existing:
        flash("Trek already booked")
        return redirect(url_for("user.available_treks"))

    new_booking = Booking(
        user_id=session["user_id"],
        trek_id=trek_id,
        status="Booked"
    )

    trek.available_slots -= 1

    db.session.add(new_booking)
    db.session.commit()

    flash("Trek booked")

    return redirect(url_for("user.my_bookings"))

@user.route("/user/bookings")
def my_bookings():

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    status = request.args.get("status", "")

    query = Booking.query .filter_by(user_id=session["user_id"])

    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(Booking.booking_date.desc()).all()

    return render_template("user/bookings.html", bookings=bookings, status=status)

@user.route("/user/bookings/cancel/<int:booking_id>")
def cancel_booking(booking_id):

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    booking = Booking.query.get(booking_id)

    if not booking or booking.user_id != session["user_id"]:
        flash("Booking not found")
        return redirect(url_for("user.my_bookings"))

    if booking.status != "Booked":
        flash("this booking can't be ")
        return redirect(url_for("user.my_bookings"))

    if booking.trek.start_date < date.today():
        flash("Trek has already started")
        return redirect(url_for("user.my_bookings"))

    booking.status = "Canceled"
    booking.trek.available_slots += 1
    db.session.commit()

    flash("Booking canceled")
    return redirect(url_for("user.my_bookings"))

@user.route("/user/profile", methods=["GET", "POST"])
def user_profile():

    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "user":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]

        existing = User.query.filter_by(phone=phone).first()

        if existing and existing.id != user.id:
            flash("Phone number already in use")
            return redirect(url_for("user.user_profile"))

        user.name = name
        user.phone = phone
        db.session.commit()
        flash("Profile updated")
        return redirect(url_for("user.user_profile"))

    return render_template("user/profile.html", user=user)