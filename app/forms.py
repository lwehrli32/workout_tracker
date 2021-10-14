from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app.constants.categories import workout_categories

# fields for registration form
class RegistrationForm(FlaskForm):

	# username field
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	
	# email field
	email = StringField('Email', validators=[DataRequired(), Email()])
	
	# password field
	password = PasswordField('Password', validators=[DataRequired()])
	
	# confirm password field
	confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	
	# submit button
	submit = SubmitField('Sign Up')
	
	# validates the username. Makes sure the username doesn't exist
	def validate_username(self, username):
		
		# gets the first user from the database with the specified username
		user = User.query.filter_by(username=username.data).first()
		
		# if the user doesn't exist, throw error
		if user:
			raise ValidationError('This username taken. Please choose a different one.')
			
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

	# username field
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	
	# email field
	email = StringField('Email', validators=[DataRequired(), Email()])
	
	# submit button
	submit = SubmitField('Save')
	
	# validates the username. Makes sure the username doesn't exist
	def validate_username(self, username):
		
		# checks if the current user changed their username
		if username.data != current_user.username:
		
			# gets the first user from the database with the specified username
			user = User.query.filter_by(username=username.data).first()
			
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

	# Workout title field
	title = StringField('Title', validators=[DataRequired(), Length(min=3, max=20)])

	# Workout category
	categories = SelectField('Categories', choices=workout_categories, validators=[DataRequired()])

	#create button to create new workout
	submit = SubmitField('Create Workout')

	def validate_categories(selfself, categories):
		pass
