from flasklogin import app

application = app

if "__main__" == __name__:
	app.run(debug=True, host="0.0.0.0", port=5027)
