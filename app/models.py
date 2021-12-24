from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

'''
	Tables in database
'''

# returns the user given the id of the user
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# user table in database
# UserMixin takes care of user sessions
class User(db.Model, UserMixin):

	# id column
	id = db.Column(db.Integer, primary_key=True)

	first_name = db.Column(db.String(320), nullable=False)

	last_name = db.Column(db.String(320), nullable=False)

	# email column
	email = db.Column(db.String(320), unique=True, nullable=False)
	
	# account image file
	image_file = db.Column(db.String(20), nullable=False, default='default_account_image.png')
	
	# password column
	password = db.Column(db.String(60), nullable=False)
	
	# relationship to the workouts
	workouts = db.relationship('Workout', backref='user', lazy=True)
	
	# this is what will be printed out when you query the users table
	def __repr__(self):
		return f"User('{self.email}', '{self.image_file}')"

# workouts table
class Workout(db.Model):

	# id column
	id = db.Column(db.Integer, primary_key=True)
	
	# workout category
	category = db.Column(db.String(20), nullable=False)

	# date of workout
	workout_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	#location of workout
	location = db.Column(db.String(250))

	# notes of workout
	notes = db.Column(db.String(1000))
	
	# id of user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	# this is what will be printed out when you query the workouts table
	def __repr__(self):
		return f"Workout('{self.category}', '{self.date_posted}'"

class Sets(db.Model):
	set_id = db.Column(db.Integer, primary_key=True)

	# exercise
	exercise = db.Column(db.String(100), nullable=False)

	# sets
	sets = db.Column(db.Integer, nullable=False)

	# reps
	reps = db.Column(db.Integer, nullable=False)

	# weight
	weight = db.Column(db.Integer, nullable=False)

	# id of user
	workout_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)