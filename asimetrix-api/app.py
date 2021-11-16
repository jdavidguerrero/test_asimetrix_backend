import os
from flask import Flask,request,jsonify, make_response  
from database import db
from sqlalchemy import text
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import Company, Farm, Barn, Sensor, Data
from datetime import timedelta
import sys
from flask_cors import CORS
import json
from operator import itemgetter
from itertools import groupby

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
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
        #return jsonify({ "status": 200, "token": access_token.decode('utf8'), "company_id": company.id, "name":company.name,"role":company.role })
        return jsonify({ "status": 200, "token": access_token, "company_id": company.id, "name":company.name,"role":company.role })
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
        result = app.response_class(
        response=json.dumps({"status":200,"message":"Client added. company id={}".format(company.id)}),
        status=200,
        mimetype='application/json'
         )
        return result
    except Exception as e:
        response = app.response_class(
        response=str(e),
        status=500,
        mimetype='application/json'
         )
        return response

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
        result = app.response_class(
        response=json.dumps({"status":200,"message":"Client removed. company id={}".format(company.id)}),
        status=200,
        mimetype='application/json'
         )
        return result
    except Exception as e:
        response = app.response_class(
        response=str(e),
        status=500,
        mimetype='application/json'
         )
        return response
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
        result = db.engine.execute(sql, params)
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

@app.route("/getInitData/<id_company>")
@jwt_required()
def getInitData(id_company):
    try:
        id_company = id_company
        sql = text(
                """select 
                count(distinct f.id) as Farms,
                count(distinct b.id) as Barns,
                count( distinct s.id) as Sensors
                from public.company c
                join public.farm f on f.company_id = c.id 
                join public.barn b on b.farm_id = f.id 
                join public.sensor s on s.barn_id = b.id 
                where c.id = :x
                group by 
                c.id """
        )
        sql2= text(
            """select 
                s.name as Type,
                cast(round(cast(AVG(d.value)as numeric),2)as varchar) as Value
                from public.data d
                left join public.sensor s on d.sensor_id = s.id 
                left join public.barn b on s.barn_id = b.id 
                left join public.farm f on b.farm_id = f.id 
                left join public.company c on f.company_id = c.id 
                where c.id = :x and d.value >0
                group by 
                s.name"""
        )
        params ={"x": id_company}
        result = db.engine.execute(sql, params)
        result2 = db.engine.execute(sql2, params)
        count = []
        average = []
        keys_count = ('farms','barns','sensors')
        for row in result:
            count.append(dict(zip(keys_count,row)))
        keys_avg = ('type', 'value')
        for row in result2:
            average.append(dict(zip(keys_avg,row)))
        data = {
            "count": count,
            "average": average
        }
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
	    
@app.route("/getDataPieTemp/<id_company>")
@jwt_required()
def getDataPieTemp(id_company):
    try:
        id_company = id_company
        sql = text(
                """select 
                    f.name as farm,
                    AVG(d.value) as value
                    from public.data d
                    left join public.sensor s on d.sensor_id = s.id 
                    left join public.barn b on s.barn_id = b.id 
                    left join public.farm f on b.farm_id = f.id 
                    left join public.company c on f.company_id = c.id 
                    where c.id = :x and s.name = 'temp' and d.value >0
                    group by 
                    f.name """
        )
        
        params ={"x": id_company}
        result = db.engine.execute(sql, params)
        data = []
        keys= ('name','y')
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

@app.route("/getDataPieHum/<id_company>")
@jwt_required()
def getDataPieHum(id_company):
    try:
        id_company = id_company
        sql = text(
                """select 
                    f.name as farm,
                    AVG(d.value) as value
                    from public.data d
                    left join public.sensor s on d.sensor_id = s.id 
                    left join public.barn b on s.barn_id = b.id 
                    left join public.farm f on b.farm_id = f.id 
                    left join public.company c on f.company_id = c.id 
                    where c.id = :x and s.name = 'hum' and d.value >0
                    group by 
                    f.name """
        )
        
        params ={"x": id_company}
        result = db.engine.execute(sql, params)
        data = []
        keys= ('name','y')
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

@app.route("/getDataLine/<id_company>")
@jwt_required()
def getDataLine(id_company):
    try:
        id_company = id_company
        sql = text(
                """select 
                    d.sensor_id as id,
                    REPLACE(concat(d.ts,',',d.value), '"','')as value
                    from public.data d
                    left join public.sensor s on d.sensor_id = s.id 
                    left join public.barn b on s.barn_id = b.id 
                    left join public.farm f on b.farm_id = f.id 
                    left join public.company c on f.company_id = c.id 
                    where  c.id = :x and date between '2021-10-21 00:00' and CAST('2021-10-21' AS TIMESTAMP(0)) + INTERVAL '12 hour' and s.name ='temp'
                    group by
                    d.sensor_id,
                    d.ts,
                    d.value """
        )
        
        params ={"x": id_company}
        result = db.engine.execute(sql, params)
        data = []
        data_result=[]
        keys= ('id', 'value')
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
    app.run(host='0.0.0.0', port=80)