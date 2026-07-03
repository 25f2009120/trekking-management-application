from flask import Flask
from models import db, User, Trek, Booking, TrekImage
from blueprints.authentication import authentication
from blueprints.user import user
from blueprints.staff import staff
from blueprints.admin import admin

app = Flask(__name__)

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Treeking_Management_Application"
db.init_app(app)

#Routes
app.register_blueprint(authentication)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(staff)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)