from datetime import datetime
from . import db

TREK_STATUSES = ["Pending", "Approved", "Open", "Closed", "Started", "Completed"]

STAFF_STATUS_TRANSITIONS = {
    "Approved": ["Open"],
    "Open": ["Closed", "Started"],
    "Closed": ["Open", "Started"],
    "Started": ["Completed"]
}

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
    bookings = db.relationship("Booking", back_populates="trek", lazy="dynamic", cascade="all, delete-orphan")
    images = db.relationship("TrekImage", back_populates="trek", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Trek('{self.id}', '{self.name}', '{self.difficulty}', '{self.location}', '{self.duration}', '{self.description}', '{self.available_slots}', '{self.status}', '{self.staff_id}', '{self.start_date}', '{self.end_date}', '{self.created_at}')"
