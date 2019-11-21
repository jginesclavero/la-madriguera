from app import db

class SystemStatus(db.Model):
    __tablename__ = 'system_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.Integer)
    
    def __init__(self, id, name, status):
        self.name = name
        self.status = status
        self.id = id
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'status': self.status
        }