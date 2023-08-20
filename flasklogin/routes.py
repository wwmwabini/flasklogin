import requests, os

from flasklogin import app, bcrypt, db, login_manager, jwt, intasend
from flask import redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required



from flasklogin.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from flasklogin.models import Users
from flasklogin.mails import send_password_reset_email
from flasklogin.functions import save_picture, remove_old_picture

@app.route("/")
def home():

	if current_user.is_authenticated:
		return redirect(url_for('users'))
	else:
	    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():

	if current_user.is_authenticated:
		flash("You need to be logged out first to access that page.", "info")
		if request.referrer:
			return redirect(request.referrer)
		else:
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
		flash("You need to be logged out first to access that page.", "info")
		if request.referrer:
			return redirect(request.referrer)
		else:
			return redirect(url_for('users'))

	form = LoginForm()

	if form.validate_on_submit():
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


@app.route("/forgot", methods=["GET", "POST"])
def forgotpassword():

	if current_user.is_authenticated:
		flash("You need to be logged out first to access that page.", "info")
		if request.referrer:
			return redirect(request.referrer)
		else:
			return redirect(url_for('users'))

	form = ForgotPasswordForm()

	if form.validate_on_submit():
		reset_token = create_access_token(identity=form.email.data)
		send_password_reset_email(form.email.data, reset_token)
		return redirect(url_for('forgotpassword'))

	return render_template("forgotpassword.html", form=form)



@app.route("/pwreset", methods=["GET", "POST"])
@jwt_required()
def pwreset():
	if current_user.is_authenticated:
		flash("You need to be logged out first to access that page.", "info")
		if request.referrer:
			return redirect(request.referrer)
		else:
			return redirect(url_for('users'))

	form = ResetPasswordForm()

	reset_token=request.args.get('reset_token')

	user = get_jwt_identity()
	print(user)

	if not user:
		flash('The token is invalid or expired. Please resend the link','warning')
		return redirect(url_for('forgotpassword'))
	else:
		if form.validate_on_submit():
			hashedpassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			user.password=hashedpassword
			#db.session.add(record)
			db.session.commit()

			flash("Password updated successfully. You can now login", "success")
			return redirect(url_for('login'))


	return render_template("resetpassword.html", form=form)


@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
	users = Users.query.all()
	return render_template("users.html", users=users)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = ProfileForm()

	if form.validate_on_submit():

		if form.profile_picture.data:
			old_profile_picture_name = current_user.image
			old_profile_picture_path = os.path.join(app.root_path, 'static/profile_pictures', old_profile_picture_name)

			profile_pic_name = save_picture(form.profile_picture.data)
			current_user.image = profile_pic_name
		current_user.email = form.email.data
		db.session.commit()

		if form.profile_picture.data and old_profile_picture_name != 'default.png':
			remove_old_picture(old_profile_picture_path)

		flash("Your account has been updated successfully.", 'success')
		return redirect('account')

	return render_template("account.html", form=form)


@app.route('/simplepay', methods=['GET', 'POST'])
@login_required
def simplepay():
	return render_template("simplepay.html")


@app.route('/backendpay', methods=['GET', 'POST'])
@login_required
def backendpay():

	if request.method == "POST":
		payment_option = request.form.get('payment_options')
		response = intasend.payment_links.create(title='Payment Link', 
					   currency="KES",
					   api_ref="5879",
					   amount=10, 
					   redirect_url="http://127.0.0.1:5027/backendpay",
					   first_name = "Wallace",
					   last_name = "Mwabini",
					   email = current_user.email,
					   card_tarrif = "CUSTOMER-PAYS",
					   mobile_tarrif = "CUSTOMER-PAYS"
					   )
		print(response)

		payment_url = os.get.environ('INTASEND_ENDPOINT') + response['url']
		print(payment_url)

		return redirect(payment_url)

		"""
		Sample response

		{'id': '3a4a7453-edcd-4a3c-9931-fc1018abda72', 'title': 'Payment Link', 'is_active': True, 'redirect_url': None, 'amount': 10, 'usage_limit': 0, 'qrcode_file': 'https://intasend-staging.s3.amazonaws.com/qrcodes/3a4a7453-edcd-4a3c-9931-fc1018abda72-aceca8df-4424-4645-a74d-d57ac86fffc7.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5PEU6MDIXYQ5527D%2F20230820%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20230820T125129Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=2d1c8f3b5cdd3fa94f2a0125cd185100258bd7475c06c714a66add9e5752075b', 'url': '/pay/3a4a7453-edcd-4a3c-9931-fc1018abda72/', 'currency': 'KES', 'mobile_tarrif': 'BUSINESS-PAYS', 'card_tarrif': 'BUSINESS-PAYS', 'created_at': '2023-08-20T15:51:28.701298+03:00', 'updated_at': '2023-08-20T15:51:29.904622+03:00'}

		"""
	
	return render_template("backendpay.html")

