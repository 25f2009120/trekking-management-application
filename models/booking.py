from datetime import datetime
from . import db

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