from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	email = EmailField("Email Address", validators=[DataRequired(), Length(min=3, max=500)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password)])
	submit = SubmitField("Register")

