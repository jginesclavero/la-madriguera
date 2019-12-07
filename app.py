# app.py
from flask import Blueprint, Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import SystemStatus, User

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

app.register_blueprint(main)
app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  # since the user_id is just the primary key of our user table, use it in the query for the user
  return User.query.get(int(user_id))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/heating-system')
@login_required
def heating_system():
  return render_template("heating-system.html")

@app.route('/login')
def login():
  return render_template('login.html') 

def check_login(username, password):
  user = User.query.filter_by(username=username).first()
  if not user or not check_password_hash(user.password, password): 
    return False
  return True

@app.route('/login', methods=['POST'])
def login_post():
  username = request.form.get('username')
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  # check if user actually exists
  # take the user supplied password, hash it, and compare it to the hashed password in database
  if not check_login(username, password): 
    flash('Please check your login details and try again.')
    return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

  # if the above check passes, then we know the user has the right credentials
  login_user(user, remember=remember)
  return redirect(url_for('heating_system'))

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
  username = request.form.get('username')
  password = request.form.get('password')

  user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

  if user: # if a user is found, we want to redirect back to signup page so user can try again
    flash('Username already exists')
    return redirect(url_for('signup'))

  # create new user with the form data. Hash the password so plaintext version isn't saved.
  new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
  
  # add the new user to the database
  db.session.add(new_user)
  db.session.commit()
  return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


@app.route('/heating-system/getStatus', methods=['GET'])
def respond():
  try:
    query = SystemStatus.query.filter_by(name='heating system')
    return  jsonify([e.serialize() for e in query])
  except Exception as e:
	  return(str(e))

@app.route("/heating-system/setTemp")
def set_temp():
  name = "heating system"

  temp = request.args.get('temp')
  username = request.args.get('username')
  password = request.args.get('password')

  if not check_login(username, password): 
    return "Loggin required"

  user_query = SystemStatus.query.filter_by(name='heating system')
  if user_query.count() > 0:
    user_query.update({SystemStatus.temp:temp}, synchronize_session = False)
    db.session.commit()
    return "System exists... Updating temp"
  else:
    try:
      system_status = SystemStatus(
        id = 1,
        name = name,
        status = True,
        temp = temp
      )
      db.session.add(system_status)
      db.session.commit()
      return "System temp added. system id={}".format(system_status.id)
    except Exception as e:
	    return(str(e))    

@app.route("/heating-system/setStatus")
def set_status():
  name = "heating system"
  status = request.args.get('status')

  username = request.args.get('username')
  password = request.args.get('password')

  if not check_login(username, password): 
    return "Loggin required"

  user_query = SystemStatus.query.filter_by(name='heating system')
  if user_query.count() > 0:
    user_query.update({SystemStatus.status:status}, synchronize_session = False)
    db.session.commit()
    return "System exists... Updating status"
  else:
    try:
      system_status = SystemStatus(
        id = 1,
        name = name,
        status = status,
        temp = 18.0
      )
      db.session.add(system_status)
      db.session.commit()
      return "System status added. system id={}".format(system_status.id)
    except Exception as e:
	    return(str(e))

   
if __name__ == '__main__':
    app.run()

