from app import db

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
            'status': self.status
            'temp': self.temp
        }