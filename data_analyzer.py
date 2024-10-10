#!/usr/bin/env python3
from types import NoneType

import requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from waitress import serve
from data_collector import Weather
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather'
db.init_app(app)

@app.route("/average", methods=["POST", "GET"])
def average_temperature():
    lat = request.json.get("lat")
    lon = request.json.get("lon")

    if lat == 'test' and lon == 'test':
        test_calc_result = calc_avg([(1,),(2,)])
        return jsonify({'message': test_calc_result})

    else:
        params = {'lat':lat,
                  'lon': lon}
        fill_db = requests.post(url="http://0.0.0.0:5002/fill_database", json=params)

        if fill_db.status_code == 200:
            print(fill_db.text)
        else:
            print(f'Error {fill_db.status_code}')

        # Calculating the average temperature
        list_of_temp_2m = Weather.query.with_entities(Weather.temperature_2m).all()
        list_of_temp_80m = Weather.query.with_entities(Weather.temperature_80m).all()
        list_of_temp_120m = Weather.query.with_entities(Weather.temperature_120m).all()
        list_of_temp_180m = Weather.query.with_entities(Weather.temperature_180m).all()

        avg_temp_2m = calc_avg(list_of_temp_2m)
        avg_temp_80m = calc_avg(list_of_temp_80m)
        avg_temp_120m = calc_avg(list_of_temp_120m)
        avg_temp_180m = calc_avg(list_of_temp_180m)
        # print("Avg Temp at 2m: " , avg_temp_2m)
        # print("Avg Temp at 80m: ", avg_temp_80m)
        # print("Avg Temp at 120m: ", avg_temp_120m)
        # print("Avg Temp at 180m: ", avg_temp_180m)
        #print(list_of_temp)

        return jsonify({'lat':lat,'lon':lon, 'avg_temp_2m': avg_temp_2m, 'avg_temp_80m': avg_temp_80m, 'avg_temp_120m': avg_temp_120m, 'avg_temp_180m': avg_temp_180m})

def calc_avg(list_of_temp):
    count = 0
    sum_of_temp = 0
    for i in list_of_temp:
        if i[0] is not None:
            sum_of_temp = sum_of_temp + i[0]
            count += 1

    avg_temp = sum_of_temp / count
    return avg_temp


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)



