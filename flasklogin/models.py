from flasklogin import db, app
from datetime import datetime

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(500), nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)