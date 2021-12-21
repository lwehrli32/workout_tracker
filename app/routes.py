import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import *
from app.models import User
from app.workout.manager import Workout_Manager
from app.workout.history import *
from flask_login import login_user, current_user, logout_user, login_required
from app.constants.workout_en import txt


'''
    Takes care of all the routes and pages in the website
'''


# code for logic on home page
@app.route("/")
@app.route("/home")
@app.route("/index")
@login_required
def home():
    # TODO get workouts

    workouts = []
    wm = Workout_Manager(current_user.id)

    workouts = wm.get_recent_workouts(5)

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('home.html', title='Home', workouts=workouts, newWorkoutTxt=txt["New Workout"], image_file=image_file)


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
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)

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


def save_picture(pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\img', picture_fn)

    output_size = (125, 125)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# user account route
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # gets user account update form
    form = UpdateAccountForm()

    # if the data is valid, update in db
    if form.validate_on_submit():
        if form.profile_img.data:
            fname = save_picture(form.profile_img.data)
            current_user.image_file = fname

        # update data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data

        # commit data
        db.session.commit()

        # tell the user their account has been updated and redirect back to account page
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    # checks if the user is going to the page for the first time and populates account info
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
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
        # creates new user
        #new_workout = Workout(category='Abs', exercise='Russian Twists', sets=1, reps=10, weight=0, location='',
                              #notes='', user_id=current_user.id)

        # add user to database
        #db.session.add(new_workout)
        #db.session.commit()

        #workout = Workout()

        flash('New workout created!', 'success')
        return redirect(url_for('home'))

    image_file = url_for('static', filename='img/' + current_user.image_file)

    # return the template
    return render_template('newWorkout.html', title='New Workout', form=form, image_file=image_file)


@app.route("/history")
@login_required
def history():
    past_history = get_history_list(current_user)
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('history.html', title='History', history=past_history, image_file=image_file)

@app.route("/whats_new")
@login_required
def whats_new():
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('whats_new.html', title="What's new?", image_file=image_file)
