import os
from flask import flash, render_template
from flasklogin import app, mail
from flask_mail import Message

def send_password_reset_email(email, token):
	try:
		msg = Message('Password Reset Instructions', sender=('Login System', os.environ.get('MAIL_DEFAULT_SENDER')), recipients=[email])
		msg.html = render_template('passwordreset.html', reset_token=token, base_url=os.environ.get('BASE_URL'))
		msg.reply_to = email
		mail.send(msg)

		flash('Please check email for instructions on how to complete password reset.', 'success')
	except Exception as e:
		flash('An error occured trying to send reset email. Please try again.', 'danger')
		print(e)