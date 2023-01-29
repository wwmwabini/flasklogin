from flasklogin import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def loaduser(user_id):
	return Users.query.get(user_id)

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(500), nullable=False, unique=True)
	password = db.Column(db.String(60), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)