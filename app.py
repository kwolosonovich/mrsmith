import requests
import pprint

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for, Markup
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap 
from flask_login import LoginManager, UserMixin


from user_form import LoginForm, RegisterForm
from secure import secret_key
from models import User, connect_db, db, Board, Image, Like, Follow, Like
from seed import seed_database
from smithsonian_api import get_images

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///smithsonian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY']= secret_key

toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)
connect_db(app)

DEBUG = False

if DEBUG:
   seed_database()
else:
   db.create_all()

API_BASE_URL = 'https://api.si.edu/openaccess/api/v1.0/search'


# TODO: Disabling Session Cookie for API

STATUS = 'login'

@app.route('/')
@app.route("/<id>")
# TODO: add JS for event listener to direct to section on homepage
def homepage(id=None):
   '''Render homepage'''
   global STATUS 
   
   if STATUS == 'login':
      form = LoginForm()
   elif STATUS == 'register':
      form = RegisterForm()
   else:
      raise Exception(f'Status = {STATUS} not implemented')
   # get random inages from API 
   image_urls = get_images()

   return render_template('homepage.html', image_urls=image_urls, form=form, status=STATUS, id=id)


# ********* USER ROUTES *********

# login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))


@app.route('/register', methods=['GET','POST'])
def register():
   '''Register new user'''
   global STATUS
   STATUS = 'register'
   
   form = RegisterForm()
   
   if form.validate_on_submit():

      username=form.username.data
      email=form.email.data
      profile_image=form.profile_image.data
      backdrop_image=form.backdrop_image.data
      password=form.password.data

      user = User.create(username, email, profile_image, backdrop_image, password)

      db.session.commit()
      flash('Welcome! Your account had been created.', 'success')
      return redirect(url_for('show_boards'))
   else: 
       flash('Registration unsuccessful, Please resubmit. If you already\
          have an account please login.', 'warning')
   return redirect('/') 

@app.route('/login', methods=['GET','POST'])
def login():
   '''Login returning user.'''
   # TODO: validate if user is already authenticated
   # if current_user.is_authenticated:
   #     return redirect(url_for('show_boards'))
   global STATUS
   STATUS = 'login'
   
   form = LoginForm()
   
   if form.validate_on_submit():
      
      user = User.query.filter_by(username=form.username.data).first()
      if user and authenticate(user.username, form.password.data): 
         login_user(user, remember=form.remember.data, authenticated=True)
      flash('Successsfully logged-in', 'success')
      return redirect(url_for('show_boards'))
   else: 
       flash('Login unsuccessful, please resubmit. If you do not already\
          have an account please register to join.', 'warning')

   return redirect('/')


# add route for user boards - requires login_required decorater 
@app.route("/user/boards")
# @login_required
def show_boards():
   """Render user boards."""
   return render_template('user/boards.html')


@app.route("/user/likes")
# @login_required
def show_likes():
   """Render user likes."""
   return render_template('user/likes.html')
 
 
@app.route("/user/following")
# @login_required
def show_following():
   """Render user following."""
   return render_template('user/following.html')
 

@app.route("/user/logout")
# @login_required
def logout():
   '''Logout user.'''
   logout_user()
   return render_template('user/logout.html')

if __name__ == "__main__":
     app.run(debug=True)
