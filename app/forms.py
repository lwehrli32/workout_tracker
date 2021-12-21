from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app.constants.categories import workout_categories
from app.workout.manager import Workout_Manager
from app.utils import *

# fields for registration form
class RegistrationForm(FlaskForm):

	first_name = StringField("First Name", validators=[DataRequired()])

	last_name = StringField('Last Name', validators=[DataRequired()])

	# email field
	email = StringField('Email', validators=[DataRequired(), Email()])
	
	# password field
	password = PasswordField('Password', validators=[DataRequired()])
	
	# confirm password field
	confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	
	# submit button
	submit = SubmitField('Sign Up')
	
	# validates the username. Makes sure the username doesn't exist
	def validate_email(self, email):
		
		# gets the first user from the database with the specified username
		user = User.query.filter_by(email=email.data).first()
		
		# if the user doesn't exist, throw error
		if user:
			raise ValidationError('There is already an account associated with this email.')
			
	# validates the email. Makes sure the email doesn't exist
	def validate_email(self, email):
		
		# gets the first user from the database with the specified email
		user = User.query.filter_by(email=email.data).first()
		
		# if the user doesn't exist, throw error
		if user:
			raise ValidationError('This email taken. Please choose a different one.')

# fields for the login form
class LoginForm(FlaskForm):
	
	# email field
	email = StringField('Email', validators=[DataRequired(), Email()])
	
	# password field
	password = PasswordField('Password', validators=[DataRequired()])
	
	# remember me field
	remember = BooleanField('Remember Me')
	
	# submit button
	submit = SubmitField('Login')
	
# fields for account info form
class UpdateAccountForm(FlaskForm):

	first_name = StringField("First Name", validators=[DataRequired()])

	last_name = StringField('Last Name', validators=[DataRequired()])

	# email field
	email = StringField('Email', validators=[DataRequired(), Email()])

	profile_img = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	
	# submit button
	submit = SubmitField('Save')
	
	# validates the username. Makes sure the username doesn't exist
	def validate_email(self, email):
		
		# checks if the current user changed their username
		if email.data != current_user.email:
		
			# gets the first user from the database with the specified username
			user = User.query.filter_by(username=email.data).first()
			
			# if the user doesn't exist, throw error
			if user:
				raise ValidationError('This username taken. Please choose a different one.')
			
	# validates the email. Makes sure the email doesn't exist
	def validate_email(self, email):
		
		# checks if the current user changed their email
		if email.data != current_user.email:
			# gets the first user from the database with the specified email
			user = User.query.filter_by(email=email.data).first()
			
			# if the user doesn't exist, throw error
			if user:
				raise ValidationError('This email taken. Please choose a different one.')


# Form for new workout
class NewWorkout(FlaskForm):

	# Workout category
	category = SelectField('Category', choices=create_tuples(workout_categories), validators=[DataRequired()])

	# get exercises based off category
	wm = Workout_Manager()
	exercise_list = wm.get_all_exercises()

	# add all exercises for all categories
	abs = SelectField('Exercise', choices=create_tuples(exercise_list[0]), validators=[DataRequired()])
	arms = SelectField('Exercise', choices=create_tuples(exercise_list[1]), validators=[DataRequired()])
	back = SelectField('Exercise', choices=exercise_list[2], validators=[DataRequired()])
	cardio = SelectField('Exercise', choices=exercise_list[3], validators=[DataRequired()])
	chest = SelectField('Exercise', choices=exercise_list[4], validators=[DataRequired()])
	legs = SelectField('Exercise', choices=exercise_list[5], validators=[DataRequired()])
	shoulders = SelectField('Exercise', choices=exercise_list[6], validators=[DataRequired()])

	sets = IntegerField('Sets', validators=[DataRequired()])

	reps = IntegerField('Reps', validators=[DataRequired()])

	weight = IntegerField('Weight', validators=[DataRequired()])

	location = StringField('Location', validators=[Length(min=0, max=250)])

	# Workout title field
	notes = StringField('Notes', validators=[Length(min=0, max=1000)])

	#create button to create new workout
	submit = SubmitField('Create Workout')

	def validate_categories(selfself, categories):
		pass
