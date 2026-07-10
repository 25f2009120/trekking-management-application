from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .trek import Trek, TREK_STATUSES, STAFF_STATUS_TRANSITIONS
from .booking import Booking
from .trek_image import TrekImage