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

class TestDataCollector(unittest.TestCase):

#   Tests whether new data can be added to the database by calling collector endpoint
#   Will be useful in analyzer

    def test_database_values(self):
        params = {'lat': 'test',
                  'lon': 'test'}
        fill_db = requests.post(url="http://0.0.0.0:5002/fill_database", json=params)

        if fill_db.status_code == 200:
            print(fill_db.text)
        else:
            print(f'Error {fill_db.status_code}')

        date_in_database = Weather.query.with_entities(Weather.datetime).all()
        #print("Printing date in databases:" + str(date_in_database))
        self.assertEqual(date_in_database[0][0], 'sample_date')


if __name__ == "__main__":
    unittest.main()
