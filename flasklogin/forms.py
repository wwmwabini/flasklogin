from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

from flasklogin.models import Users


class LoginForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	remember = BooleanField("Remember Me", default=False)
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Register")

	def validate_email(form, email):
		emailaddress = Users.query.filter_by(email=email.data).first()
		if emailaddress:
			raise ValidationError("Email already in use. Please select a diffrent email.")

	def validate_password(form, password):
		digits, uppercase, lowercase = 0, 0, 0

		if len(password.data) >= 10:
			for character in password.data:
				if character.isdigit():
					digits+=1
				if character.isupper():
					uppercase+=1
				if character.islower():
					lowercase+=1

			if digits < 1 or uppercase < 1 or lowercase < 1:
				raise ValidationError("Password must be at least 10 characters long and contain lowercase, uppercase and digit characters.")
		else:
			raise ValidationError("Password must be at least 10 characters long and contain lowercase, uppercase and digit characters.")

class ForgotPasswordForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	submit = SubmitField("Reset Password")

	def validate_email(form, email):
		emailaddress = Users.query.filter_by(email=email.data).first()
		if not emailaddress:
			raise ValidationError("No user associated with that email.")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Reset")

	def validate_password(form, password):
		digits, uppercase, lowercase = 0, 0, 0

		if len(password.data) >= 10:
			for character in password.data:
				if character.isdigit():
					digits+=1
				if character.isupper():
					uppercase+=1
				if character.islower():
					lowercase+=1

			if digits < 1 or uppercase < 1 or lowercase < 1:
				raise ValidationError("Password must be at least 10 characters long and contain lowercase, uppercase and digit characters.")
		else:
			raise ValidationError("Password must be at least 10 characters long and contain lowercase, uppercase and digit characters.")


class ProfileForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	profile_picture = FileField("Update profile picture", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'])])
	submit = SubmitField("Update")

	def validate_email(form, email):
		if form.email.data != current_user.email:
			emailaddress = Users.query.filter_by(email=email.data).first()
			if emailaddress:
				raise ValidationError("Email already in use. Please select a diffrent email.")