#!/usr/bin/env python3
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from waitress import serve
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather'
#db = SQLAlchemy(app)
db.init_app(app)

app.app_context().push()

class Weather(db.Model):
    datetime = db.Column(db.String(200), primary_key=True, nullable=True)
    # id = db.Column(db.Integer, primary_key=True)
    # datetime = db.Column(db.String(200), nullable=True)
    temperature_2m = db.Column(db.Float, nullable=True)
    temperature_80m = db.Column(db.Float, nullable=True)
    temperature_120m = db.Column(db.Float, nullable=True)
    temperature_180m = db.Column(db.Float, nullable=True)

@app.route("/fill_database", methods=["POST", "GET"])
def fill_database():
    lat = request.json.get("lat")
    lon = request.json.get("lon")

    if lat == 'test' and lon == 'test':
            db.drop_all()
            db.create_all()
            new_entry = Weather(datetime="sample_date")
            db.session.add(new_entry)
            db.session.commit()
            return jsonify({'message': 'Test condition was entered in data_collector.py'})
    else:
        db.drop_all()
        db.create_all()

        current_temperature_2m = get_temperature(lat, lon)["hourly"]["temperature_2m"]
        current_temperature_80m = get_temperature(lat, lon)["hourly"]["temperature_80m"]
        current_temperature_120m = get_temperature(lat, lon)["hourly"]["temperature_120m"]
        current_temperature_180m = get_temperature(lat, lon)["hourly"]["temperature_180m"]
        current_datetime = get_temperature(lat, lon)["hourly"]["time"]
        #index = 0
        for datetime_data, temp_2m, temp_80m, temp_120m, temp_180m in zip(current_datetime, current_temperature_2m, current_temperature_80m, current_temperature_120m, current_temperature_180m):
            new_entry = Weather(datetime=datetime_data, temperature_2m=temp_2m, temperature_80m = temp_80m, temperature_120m = temp_120m, temperature_180m = temp_180m)
            db.session.add(new_entry)
            #index += 1

        db.session.commit()

        return jsonify({'lat': lat, 'lon': lon})

'''
Helper function to get temperature
using API
'''

def get_temperature(lat=52.52, lon=14.31):
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,temperature_80m,temperature_120m,temperature_180m&temperature_unit=fahrenheit&past_days=92&forecast_days=16')
    return response.json()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5002)

    # db.drop_all()
    # db.create_all()
    #
    # current_temperature = get_temperature()["hourly"]["temperature_2m"]
    # current_datetime = get_temperature()["hourly"]["time"]
    # index = 0
    # for datetime_data, temp_data in zip(current_datetime, current_temperature):
    #     new_entry = Weather(datetime=datetime_data, temperature=temp_data)
    #     db.session.add(new_entry)
    #     index += 1
    #
    # db.session.commit()


