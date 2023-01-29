import requests

from flasklogin import app, bcrypt, db, login_manager
from flask import redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required


from flasklogin.forms import LoginForm, RegisterForm
from flasklogin.models import Users



@app.route("/")
def home():

	if current_user.is_authenticated:
		return redirect(url_for('users'))
	else:
	    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():

	if current_user.is_authenticated:
		flash("You need to be logged out first to access registration page.", "info")
		return redirect(url_for('users'))


	form = RegisterForm()

	if form.validate_on_submit():
		hashedpassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		user = Users(email=form.email.data, password=hashedpassword)
		db.session.add(user)
		db.session.commit()

		flash("User registered successfully. You can now login", "success")
		return redirect(url_for('login'))

	return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

	if current_user.is_authenticated:
		flash("You need to be logged out first to access login page.", "info")
		return redirect(url_for('users'))

	form = LoginForm()

	if request.method=="POST":
		user = Users.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash("Login successful. Welcome back!", "success")
			redirect_page = request.args.get('next')
			if redirect_page:
				return redirect(redirect_page)
			else:
				return redirect(url_for('users'))
		else:
			flash("Invalid login. Please try again!", "danger")
			return redirect(url_for('login'))

	return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return render_template("logout.html")


@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
	users = Users.query.all()
	return render_template("users.html", users=users)


@app.route("/me/account", methods=["GET", "POST"])
@login_required
def account():
	return render_template("account.html")

