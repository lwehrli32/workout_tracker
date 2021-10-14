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
	
	# username column
	username = db.Column(db.String(20), unique=True, nullable=False)
	
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
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# workouts table
class Workout(db.Model):

	# id column
	id = db.Column(db.Integer, primary_key=True)
	
	# workout category
	category = db.Column(db.String(20), nullable=False)
	
	# date of workout
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	# id of user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	# this is what will be printed out when you query the workouts table
	def __repr__(self):
		return f"Workout('{self.category}', '{self.date_posted}'"