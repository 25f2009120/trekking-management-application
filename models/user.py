from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

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
