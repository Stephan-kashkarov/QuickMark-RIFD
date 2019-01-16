from server.app import db, login
from flask_login import UserMixin
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
	"""User loader for flask login."""
	return Person.query.get(int(id))

# INTERMIDEARY TABLES
class Access(db.Model):
	__tablename__ = "access"

	person_id = db.Column(db.Integer, db.ForeignKey("person.id"), primary_key=True)
	class_id =  db.Column(db.Integer, db.ForeignKey("class.id"), primary_key=True)

class Roll_Student(db.Model):
	__tablename__ = "roll_student"
	extend_existing = True
	roll_id = db.Column(db.Integer, db.ForeignKey("roll.id"), primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
	present = db.Column(db.Boolean, default=False)

class Class_Student(db.Model):
	__tablename__ = "class_student"

	roll_id = db.Column(db.Integer, db.ForeignKey("class.id"), primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)


# DATA TABLES
class Class(db.Model):
	__tablename__ = "class"

	id =           db.Column(db.Integer, primary_key=True)
	title =        db.Column(db.String(50))
	users =        db.relationship("Access", backref="class", lazy="dynamic")
	students =     db.relationship("Roll_Class", backref="class", lazy="dynamic")

	def __repr__(self):
		return "<Class: {}>".format(self.title)

class Roll(db.Model):
	__tablename__ = "roll"

	id =       db.Column(db.Integer, primary_key=True)
	date =     db.Column(db.Date, default=date.today())
	class_id = db.Column(db.Integer)
	roll =     db.relationship("Roll_Student", backref="roll", lazy="dynamic")

	def __repr__(self):
		return "<Roll object Student: {} is in Class: {}>".format(self.student_id, self.class_id)


class Student(db.Model):
	__tablename__ = "student"

	id =           db.Column(db.Integer, primary_key=True)
	student_id =   db.Column(db.Integer)
	student_name = db.Column(db.String(50))
	rfid =         db.Column(db.BLOB)
	roll =         db.relationship("Student_Roll", backref="student", lazy="dynamic")

	def __repr__(self):
		return "<Student, id: {}, name: {}, dbId: {}>".format(self.student_id, self.student_name, self.id)


# USER TABLES
class Person(db.Model, UserMixin):
	__tablename__ = "person"

	id =            db.Column(db.Integer, primary_key=True)
	username =      db.Column(db.String(64), index=True, unique=True)
	email =         db.Column(db.String(120), nullable=True)
	password_hash = db.Column(db.String(128))
	logins =        db.Column(db.Integer, default=0)
	classes =       db.relationship("Access", backref="person", lazy="dynamic")

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		"""Runs the passwords through a hash and appends."""
		self.password_hash = generate_password_hash(str(password))

	def check_password(self, password):
		"""Checks a password against the hash."""
		return check_password_hash(self.password_hash, password)

class RFIDStation(db.Model):
	__tablename__ = "rfid_station"
	id =            db.Column(db.Integer, primary_key=True)
	name =          db.Column(db.String(64))
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Station {}>'.format(self.name)

	def set_password(self, password):
		"""Runs the passwords through a hash and appends."""
		self.password_hash = generate_password_hash(str(password))

	def check_password(self, password):
		"""Checks a password against the hash."""
		return check_password_hash(self.password_hash, password)