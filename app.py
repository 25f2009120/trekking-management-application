import email

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import foreign
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Models

#User
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    phone = db.Column(db.String(15), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    role = db.Column(db.String(10), nullable = False, default = "user") # Admin, Staff, User
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)

    #Relationships
    assigned_treks = db.relationship("Trek", back_populates="staff", foreign_keys="Trek.staff_id")
    bookings = db.relationship("Booking", back_populates="user", lazy="dynamic")

    def password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', '{self.phone}', '{self.password}', '{self.role}', '{self.created_at}', '{self.is_approved}', '{self.is_blacklisted}')"

#Trek
class Trek(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    difficulty = db.Column(db.String(10), nullable = False, default = "Easy") # Easy, Normal, Difficult
    location = db.Column(db.String(150), nullable = False)
    duration = db.Column(db.Integer, nullable = False, default = 1)
    description = db.Column(db.Text, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False, default = 0)
    status = db.Column(db.String(10), nullable = False, default = "Pending") # Pending, Approved, Canceled, Completed
    staff_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = True)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Relationships
    staff = db.relationship("User", back_populates="assigned_treks", foreign_keys="Trek.staff_id")
    bookings = db.relationship("Booking", back_populates="trek", lazy="dynamic")
    images = db.relationship("TrekImage", back_populates="trek")

    def __repr__(self):
        return f"Trek('{self.id}', '{self.name}', '{self.difficulty}', '{self.location}', '{self.duration}', '{self.description}', '{self.available_slots}', '{self.status}', '{self.staff_id}', '{self.start_date}', '{self.end_date}', '{self.created_at}')"

#Images
class TrekImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    image_url = db.Column(db.String(500), nullable = False)

    #Relationships
    trek = db.relationship("Trek", back_populates="images")

    def __repr__(self):
        return f"TrekImage('{self.id}', '{self.trek_id}', '{self.image_url}')"

#Booking
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    status = db.Column(db.String(10), nullable = False, default = "Booked")
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    #Relationships
    user = db.relationship("User", back_populates="bookings")
    trek = db.relationship("Trek", back_populates="bookings")

    def __repr__(self):
        return f"Booking('{self.id}', '{self.user_id}', '{self.trek_id}', '{self.status}', '{self.booking_date}')"

#Routes
@app.route("/")
def index():
    return "Hello World!"

@app.route("/users")
def users():
    users = User.query.all()

    output = ""

    for user in users:
        output += f"ID = {user.id}<br> name = {user.name}<br> email = {user.email}<br> phone = {user.phone}<br> password = {user.password}<br> role = {user.role}<br> created_at = {user.created_at}<br> is_approved = {user.is_approved}<br> is_blacklisted = {user.is_blacklisted}<br>"

    return output

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)