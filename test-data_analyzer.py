#!/usr/bin/env python3
import requests
import unittest
from flask import Flask, request
from db import db
from data_collector import Weather

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather'
#db = SQLAlchemy(app)
db.init_app(app)


class TestDataAnalyzer(unittest.TestCase):

#   Tests whether average of values can be calculated and returned in json format
#   Will be useful in server.py

    def test_avg_calculation(self):
        params = {'lat': 'test',
                  'lon': 'test'}
        avg_calc_result = requests.post(url="http://0.0.0.0:5000/average", json=params)
        self.assertEqual(avg_calc_result.json()['message'], 1.5)


if __name__ == "__main__":
    unittest.main()