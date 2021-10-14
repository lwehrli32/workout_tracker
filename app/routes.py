from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import *
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.constants.workout_en import txt
from workout.workout_manager import *

'''
    Takes care of all the routes and pages in the website
'''


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404_not_found.html'), 404


# code for logic on home page
@app.route("/")
@app.route("/home")
@app.route("/index")
@login_required
def home():
    # TODO get workouts

    workouts = []
    temp_workout = {
        "title": "Arms",
        "date": "1/1/2021",
        "partners": "Donny",
        "location": "Nic",
        "num_sets": "10",
        "duration": "2 hours"
    }
    workouts.append(temp_workout)
    workouts.append(temp_workout)
    workouts.append(temp_workout)
    workouts.append(temp_workout)
    workouts.append(temp_workout)
    workouts.append(temp_workout)
    workouts.append(temp_workout)

    return render_template('home.html', title='Home', workouts=workouts, newWorkoutTxt=txt["New Workout"])


# logic for register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    # redirects user to home page if they are logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # loads the register form
    form = RegistrationForm()

    # checks if the form has valid data
    if form.validate_on_submit():
        # hashes password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # creates new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # add user to database
        db.session.add(user)
        db.session.commit()

        # tell user their account was created
        flash(f'Your account has been created! You are now able to login.', 'success')

        # redirect them to the login page
        return redirect(url_for('login'))

    # if the data was not correct in the register form,
    # the register template will load again
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    logic for login page
    """

    app.logger.info('Start of login')

    # redirects user to home page if they are logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # loads login form
    form = LoginForm()

    # checks if the data is correct in the form
    if form.validate_on_submit():

        # sees if the user is in the database. Goes off of email
        user = User.query.filter_by(email=form.email.data).first()

        # if the user exists and the passwords match
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # logs in user
            login_user(user, remember=form.remember.data)

            # tell the user they are now logged in
            flash('You are now logged in!', 'success')

            # gets the page from the query string if there is one
            next_page = request.args.get('next')

            # redirect to page if the next page exists
            if next_page:
                return redirect(next_page)

            # redirect them to the home page
            return redirect(url_for('home'))
        else:
            # bad login. Tell the user to enter new email and password
            flash('Login unsuccessful. Please check email and password', 'danger')

    # this will hit if the login was unsuccessful or they just come to the page
    return render_template('login.html', title='Login', form=form)


# logs out the user
@app.route("/logout")
def logout():
    # logs the user out
    logout_user()

    # redirect them to the login page
    return redirect(url_for('login'))


# user account route
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # gets user account update form
    form = UpdateAccountForm()

    # if the data is valid, update in db
    if form.validate_on_submit():

        # update data
        current_user.username = form.username.data
        current_user.email = form.email.data

        # commit data
        db.session.commit()

        # tell the user their account has been updated and redirect back to account page
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    # checks if the user is going to the page for the first time and populates account info
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # get user account picture
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# New workout route
@app.route("/newWorkout", methods=['GET', 'POST'])
@login_required
def newWorkout():
    app.logger.info('Start of newWorkout')

    # create workout
    form = NewWorkout()

    if form.validate_on_submit():
        flash('New workout created!', 'success')
        return redirect(url_for('home'))

    # return the template
    return render_template('newWorkout.html', title='New Workout', form=form)


# logic on history page
@app.route("/history")
@login_required
def history():

    history = []

    workout_manager = workout_manager()

    return render_template('history.html', title='History', history=history)
