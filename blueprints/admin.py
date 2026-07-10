from flask import session, Blueprint, flash, url_for, render_template, redirect, request
from models import db, User, Trek, Booking
from datetime import datetime

admin = Blueprint("admin", __name__)
@admin.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    user = User.query.get(session["user_id"])
    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    pending_approvals = User.query.filter_by(role="staff", is_approved=False).count()

    return render_template("admin/dashboard.html",
                           user=user,
                           total_users=total_users,
                           total_staff=total_staff,
                           total_treks=total_treks,
                           total_bookings=total_bookings,
                           pending_approvals=pending_approvals
                           )

@admin.route("/admin/staff-approvals")
def staff_approvals():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    unapproved_staff = User.query.filter_by(role="staff", is_approved=False).all()

    return render_template("admin/staff_approvals.html", unapproved_staff=unapproved_staff)

@admin.route("/admin/approve-staff/<int:user_id>", methods=["POST"])
def approve_staff(user_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    s = User.query.get(user_id)

    if s and s.role == "staff":
        s.is_approved = True
        db.session.commit()
        flash("Staff approved")
    else:
        flash("Staff not found")

    return redirect(url_for("admin.staff_approvals"))

@admin.route("/admin/staff")
def admin_staff():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = User.query.filter_by(role="staff")

    if search:
        filter = [User.name.ilike(f"%{search}%"), User.email.ilike(f"%{search}")]
        if search.isdigit():
            filter.append(User.id == int(search))
        query = query.filter(db.or_(*filter))

    if status == "blacklisted":
        query = query.filter_by(is_blacklisted=True)
    elif status == "unblacklisted":
        query = query.filter_by(is_blacklisted=False)
    elif status == "approved":
        query = query.filter_by(is_approved=True)
    elif status == "pending":
        query = query.filter_by(is_approved=False)

    staff = query.all()

    return render_template("admin/staff.html", staff=staff, search=search, status=status)

@admin.route("/admin/blacklist-staff/<int:user_id>", methods=["POST"])
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

    return redirect(url_for("admin.admin_staff"))

@admin.route("/admin/unblacklist-staff/<int:user_id>", methods=["POST"])
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

    return redirect(url_for("admin.admin_staff"))

@admin.route("/admin/users")
def admin_users():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = User.query.filter_by(role="user")

    if search:
        filter = [User.name.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")]
        if search.isdigit():
            filter.append(User.id == int(search))
        query = query.filter(db.or_(*filter))
    if status == "blacklisted":
        query = query.filter_by(is_blacklisted=True)
    elif status == "unblacklisted":
        query = query.filter_by(is_blacklisted=False)

    users = query.all()

    return render_template("admin/users.html", users=users, search=search, status=status)

@admin.route("/admin/blacklist/<int:user_id>", methods=["POST"])
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

    return redirect(url_for("admin.admin_users"))

@admin.route("/admin/unblacklist/<int:user_id>", methods=["POST"])
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

    return redirect(url_for("admin.admin_users"))

@admin.route("/admin/treks")
def admin_treks():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    status = request.args.get("status", "")

    query = Trek.query
    if search:
        filter = [Trek.name.ilike(f"%{search}%"), Trek.location.ilike(f"%{search}%")]
        if search.isdigit():
            filter.append(Trek.id == int(search))
        query = query.filter(db.or_(*filter))

    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if status:
        query = query.filter_by(status=status)

    treks = query.all()

    return render_template("admin/treks.html", treks=treks, search=search, difficulty=difficulty, status=status)

@admin.route("/admin/treks/create", methods=["GET", "POST"])
def create_trek():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    staff_list = User.query.filter_by(role="staff", is_approved=True, is_blacklisted=False).all()

    if request.method == "POST":
        name = request.form["name"]
        difficulty = request.form["difficulty"]
        location = request.form["location"]
        duration = request.form["duration"]
        description = request.form["description"]
        available_slots = request.form["available_slots"]
        staff_id = request.form["staff_id"] or None
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()

        if end_date < start_date:
            flash("End date can't be before start date")
            return redirect(url_for("admin.create_trek"))

        image_urls = request.form["image_urls"]

        new_trek = Trek(
            name=name,
            difficulty=difficulty,
            location=location,
            duration=duration,
            description=description,
            available_slots=available_slots,
            staff_id=staff_id,
            start_date=start_date,
            end_date=end_date,
            status="Pending"
        )
        db.session.add(new_trek)
        db.session.commit()

        if image_urls:
            for url in image_urls.split(","):
                url = url.strip()
                if url:
                    from models import TrekImage
                    image = TrekImage(trek_id=new_trek.id, image_url=url)
                    db.session.add(image)

        db.session.commit()
        flash("Trek created")
        return redirect(url_for("admin.admin_treks"))

    return render_template("admin/create_trek.html", staff_list=staff_list)

@admin.route("/admin/treks/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)
    if not trek:
        flash("Trek not found")
        return redirect(url_for("admin.admin_treks"))

    staff_list = User.query.filter_by(role="staff", is_approved=True, is_blacklisted=False).all()

    if request.method == "POST":
        trek.name = request.form["name"]
        trek.difficulty = request.form["difficulty"]
        trek.location = request.form["location"]
        trek.duration = request.form["duration"]
        trek.description = request.form["description"]
        trek.available_slots = request.form["available_slots"]
        trek.staff_id = request.form["staff_id"] or None
        trek.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        trek.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        trek.status = request.form["status"]

        image_urls = request.form["image_urls"]
        from models import TrekImage
        TrekImage.query.filter_by(trek_id=trek_id).delete()
        if image_urls:
            for url in image_urls.split(","):
                url = url.strip()
                if url:
                    image = TrekImage(trek_id=trek.id, image_url=url)
                    db.session.add(image)

        db.session.commit()
        flash("Trek edited")
        return redirect(url_for("admin.admin_treks"))

    current_images = ", ".join([image.image_url for image in trek.images])
    return render_template("admin/edit_trek.html", trek=trek, current_images=current_images, staff_list=staff_list)

@admin.route("/admin/treks/delete/<int:trek_id>", methods=["POST"])
def delete_trek(trek_id):
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    trek = Trek.query.get(trek_id)

    if trek:
        db.session.delete(trek)
        db.session.commit()
        flash("Trek deleted")
    else:
        flash("Trek not found")
    return redirect(url_for("admin.admin_treks"))

@admin.route("/admin/bookings")
def admin_bookings():
    if "user_id" not in session:
        return redirect(url_for("authentication.login"))

    if session["role"] != "admin":
        return redirect(url_for("authentication.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = Booking.query

    if status:
        query = query.filter_by(status=status)

    bookings = query.all()

    if search:
        filtered = []
        for b in bookings:
            if search.lower() in b.user.name.lower() or search.lower() in b.trek.name.lower():
                filtered.append(b)
        bookings = filtered

    return render_template("admin/bookings.html", bookings=bookings, search=search, status=status)