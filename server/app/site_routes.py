from server.app import app, db
from flask import redirect, url_for, flash, render_template, request
from server.app.models import Class, Roll, Student, Person 

from flask_login import current_user, login_user, login_required, logout_user

@app.route("/")
def index():
	return render_template("main.html")

@login_required
@app.route("/dash")
def dash():
	return render_template("dash.html")

# AUTH ROUTES
@app.route("/auth", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		# incase there is no json
		try:
			data = request.json
		except:
			data = None
			flash("Server: No data in json")
			return "No json"

		if data:
			if data['type'] == 'login':
				username = data["username"]
				password = data["passowrd"]

				user = Person.query.filter_by(username=username).first()
				if user:
					if user.check_password(password):
						login_user(user)
						flash("Login succsessful!")
						user.logins += 1
						db.session.commit()
						return "Success"
					flash("Login unsucsessful!")
					return "Incorrect login"
				return "No User"
			else:
				username = data['username']
				email = data['email']
				password = data['password']
				if not Person.query.filter_by(username=username).first():
					p = Person()
					p.username = username
					p.email = email
					p.set_password(password)
					db.session.add(p)
					db.session.commit()
					flash("User created, Try logging in!")
					return "Success"
				return "User Exists"

	return render_template("auth.html")	


@login_required
@app.route("/auth/logout", methods=["POST", "GET"])
def logout():
	logout_user()
	return redirect(url_for('login'))


# CLASS ROUTES
@app.route("/<class_id>/mark")
def mark(class_id):
	students = Roll.query.filter_by(class_id=class_id)
	return "Marking {}".format(class_id)

