import os
from flask import Flask,request,jsonify, make_response  
from database import db
from sqlalchemy import text
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import Company, Farm, Barn, Sensor, Data
import datetime
import sys
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
jwt = JWTManager(app)


@app.route("/")
def hello():
    return "Hello World!"




@app.route("/create_admin", methods=['POST'])
def create_admin():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    name = data ['name']
    email = data ['email']
    role = "admin"
    status = 1
    try:
        company=Company(
            name=name,
            password=hashed_password,
            email=email,
            role = role,
            status = status
        )
        db.session.add(company)
        db.session.commit()
        return jsonify({"message":"Admin added. company id={}".format(company.id)})
    except Exception as e:
	    return jsonify({"error":str(e)})


@app.route('/login', methods=['GET', 'POST'])  
def login(): 
 
    data = request.get_json()   
    email = data ['email']
    password = data ['password']
    if not data or not email or not password:  
        return make_response('could not verify', 401, {'"message": "login required"'})    

    company = Company.query.filter_by(email=email).first()   
     
    if check_password_hash(company.password, password):  
        access_token = create_access_token(identity=company.id)
        return jsonify({ "status": 200, "token": access_token.decode('utf8'), "company_id": company.id, "name":company.name,"role":company.role })
    return make_response('could not verify',  401, {'"message": "Verify Data"'})

@app.route("/create_client", methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    name = data ['name']
    email = data ['email']
    role = "client"
    status = 1
    try:
        company=Company(
            name=name,
            password=hashed_password,
            email=email,
            role = role,
            status = status
        )
        db.session.add(company)
        db.session.commit()
        return jsonify({"message":"Client added. company id={}".format(company.id)})
    except Exception as e:
	    return jsonify({"error":str(e)})

@app.route("/getall")
@jwt_required()
def get_all():
    try:
        companies=Company.query.filter_by(role="client", status=1)
        return  jsonify([e.serialize() for e in companies])
    except Exception as e:
	    return(str(e))

@app.route("/remove_client/<id_>")
@jwt_required()
def remove_client(id_):
    try:
        company=Company.query.filter_by(id=id_).first()
        company.status=0
        db.session.commit()
        return jsonify({"message":"Client wiht company id={} was removed".format(company.id)})
    except Exception as e:
	    return(str(e))

@app.route("/getFarms/<id_company>")
@jwt_required()
def getFarms(id_company):
    try:
        farm=Farm.query.filter_by(company_id=id_company)
        return  jsonify([e.serialize() for e in farm])
    except Exception as e:
	    return(str(e))

@app.route("/getFarm/<id_>")
@jwt_required()
def getFarm(id_):
    try:
        farm=Farm.query.filter_by(id=id_).first()
        return jsonify(farm.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/getBarns/<id_farm>")
@jwt_required()
def getBarns(id_farm):
    try:
        barn=Barn.query.filter_by(farm_id=id_farm)
        return  jsonify([e.serialize() for e in barn])
    except Exception as e:
	    return(str(e))

@app.route("/getBarn/<id_>")
@jwt_required()
def getBarn(id_):
    try:
        barn=Barn.query.filter_by(id=id_).first()
        return jsonify(barn.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/getSensors/<id_barn>")
@jwt_required()
def getSensors(id_barn):
    try:
        sensor=Sensor.query.filter_by(barn_id=id_barn)
        return  jsonify([e.serialize() for e in sensor])
    except Exception as e:
	    return(str(e))

@app.route("/getSensor/<id_>")
@jwt_required()
def getSensor(id_):
    try:
        sensor=Sensor.query.filter_by(id=id_).first()
        return jsonify(sensor.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/getSensorData/<id_sensor>")
@jwt_required()
def getSensorData(id_sensor):
    try:
        data=Data.query.filter_by(sensor_id=id_sensor)
        #result = db.session.execute('SELECT data.id AS data_id, data.timestamp AS data_timestamp, data.sensor_id AS data_sensor_id, data.value AS data_value FROM public.data WHERE sensor_id = :val', {'val': id_sensor})
        return  jsonify([e.serialize() for e in data])
    except Exception as e:
	    return(str(e))

@app.route("/getSensorDataByDate/<date>")
@jwt_required()
def getSensgetSensorDataByDateorData(date):
    try:
        #data=Data.query.filter_by(sensor_id=id_sensor)
        #result = db.session.execute('SELECT data.id AS data_id, data.timestamp AS data_timestamp, data.sensor_id AS data_sensor_id, data.value AS data_value FROM public.data WHERE sensor_id = :val', {'val': id_sensor})
        date_data = date
        sql = text("select s.name,d.sensor_id, d.id, d.value,cast(d.date as varchar) from public.data d join public.sensor s on s.id = d.sensor_id where date between :x and CAST( :x AS TIMESTAMP(0)) + INTERVAL '1 day'")
        params ={"x": date_data}
        print
        result = db.engine.execute(sql, params)
        #print (result.first())
        data = []
        keys = ('type','sensor_id','id','value','date')
        for row in result:
            data.append(dict(zip(keys,row)))
        response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
         )
        return response
    except Exception as e:
        response = app.response_class(
        response=str(e),
        status=500,
        mimetype='application/json'
         )
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)