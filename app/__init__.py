from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# initialization of app

app = Flask(__name__)

# config variables
app.config['SECRET_KEY'] = 'd871dc9c8ba70b6a47be7a8c89f51055'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# initialize the database
db = SQLAlchemy(app)

# initialize bcrypt for hashing passwords
bcrypt = Bcrypt(app)

# initialize login manager for keeping track of who is logged in
login_manager = LoginManager(app)

# redirects users to login page if they are not logged in and are
# trying to view pages that they need to be logged in to use
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app import routes