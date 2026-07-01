from . import db

#Images
class TrekImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable = False)
    image_url = db.Column(db.String(500), nullable = False)

    #Relationships
    trek = db.relationship("Trek", back_populates="images")

    def __repr__(self):
        return f"TrekImage('{self.id}', '{self.trek_id}', '{self.image_url}')"
