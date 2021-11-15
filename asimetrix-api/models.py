from database import db
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.dialects.postgresql import JSON



class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())
    status = db.Column(db.Integer())


    def __init__(self, name, email,password, role, status ):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status':self.status
            }

class Farm(db.Model):
    __tablename__ = 'farm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    company_id = db.Column(db.Integer())
    status = db.Column(db.Integer())


    def __init__(self, name, company_id, status ):
        self.name = name
        self.company_id = company_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'company_id': self.company_id,
            'status':self.status
            }

class Barn(db.Model):
    __tablename__ = 'barn'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    farm_id = db.Column(db.Integer())
    status = db.Column(db.Integer())


    def __init__(self, name, farm_id, status ):
        self.name = name
        self.farm_id = farm_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'farm_id': self.farm_id,
            'status':self.status
            } 

class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    barn_id = db.Column(db.Integer())
    status = db.Column(db.Integer())


    def __init__(self, name, barn_id, status ):
        self.name = name
        self.barn_id = barn_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'barn_id': self.barn_id,
            'status':self.status
            } 

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.String())
    sensor_id = db.Column(db.Integer())
    value = db.Column(db.Integer())
    date = db.Column(db.DateTime(timezone=False))


    def __init__(self, timestamp, sensor_id, value ):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.value = value

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'timestamp': self.timestamp,
            'sensor_id': self.sensor_id,
            'value':str(self.value),
            'date':self.date
            } 