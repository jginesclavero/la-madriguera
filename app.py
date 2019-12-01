# app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
system_up = False

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import SystemStatus

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

   
@app.route('/heating-system')
def heating_system_index():
  return render_template("heating-system-set-status.html")

# A welcome message to test our server
@app.route('/')
def index():
  return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run()

#if __name__ == '__main__':
#    # Threaded option to enable multiple instances for multiple user access support
#    app.run(threaded=True, port=5000)