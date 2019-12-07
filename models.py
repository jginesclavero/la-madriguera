from app import db
from random import randrange
from flask_login import UserMixin

class User(UserMixin, db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
  username = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))

  def __init__(self, username, password):
    self.id = randrange(100)
    self.username = username
    self.password = password

  def __repr__(self):
    return '<id {}>'.format(self.id)
    
  def serialize(self):
    return {
      'id': self.id, 
      'username': self.username,
      'password': self.password
    }

class SystemStatus(db.Model):
  __tablename__ = 'system_status'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  status = db.Column(db.Integer)
  temp = db.Column(db.Integer)
    
  def __init__(self, id, name, status, temp):
    self.name = name
    self.status = status
    self.id = id
    self.temp = temp
  def __repr__(self):
    return '<id {}>'.format(self.id)
    
  def serialize(self):
    return {
      'id': self.id, 
      'name': self.name,
      'status': self.status,
      'temp': self.temp
    }