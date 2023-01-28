from flasklogin import app
from flask import redirect, render_template, url_for

from flasklogin.forms import LoginForm, RegisterForm


@app.route("/")
def home():
	return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	return render_template("register.html", form=form)

@app.route("/users", methods=["GET", "POST"])
def users():
	form = RegisterForm()
	return render_template("users.html", form=form, users=users)

@app.route("/me/account", methods=["GET", "POST"])
def account():
	form = RegisterForm()
	return render_template("account.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	return render_template("login.html", form=form)

@app.route("/logout")
def logout():
	return render_template("logout.html")