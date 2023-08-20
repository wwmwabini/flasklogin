import os
from flask import Flask, flash, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from intasend import APIService

from datetime import timedelta

load_dotenv()

app = Flask(__name__)

#prevent user from using the Back button in browsers to return to session pages after logout
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.environ.get("USER_HOME_DIR") + "/flasklogin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config['MAIL_DEBUG']  = False


mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
intasend = APIService(token=os.environ.get("INTASEND_API_KEY"), publishable_key=os.environ.get("INTASEND_PUBLISHABLE_KEY"), test=True)

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login first to access that resource.", "info")
    return redirect(url_for('login'))

from flasklogin import routes

