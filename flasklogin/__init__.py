import os
from flask import Flask, flash, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/flasklogin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login first to access that resource.", "info")
    return redirect(url_for('login'))

from flasklogin import routes

