import requests
from flask import Flask, render_template, request
from waitress import serve

#makes this app a Flask app
app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/temperature', methods=["POST", "GET"])

def get_weather():
    lat = request.args.get('LAT Value')
    lon = request.args.get('LON Value')

    lat = lat.strip()
    lon = lon.strip()

    if lat == '' or lon == '':
        return render_template("wrong-location.html")
    else:
        lat = int(lat)
        lon = int(lon)
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return render_template("city-not-found.html")

    params = {'lat':lat,
              'lon': lon}
    weather_data = requests.post(url="http://0.0.0.0:5000/average", json=params)

    if weather_data.status_code == 200:
        print(weather_data.text)
    else:
        print(f'Error {weather_data.status_code}')

    return render_template(
        "weather.html",
        LATITUDE=f"{weather_data.json()['lat']:.2f}",
        LONGITUDE=f"{weather_data.json()['lon']:.2f}",
        temp_2m=f"{weather_data.json()['avg_temp_2m']:.1f}",
        temp_80m=f"{weather_data.json()['avg_temp_80m']:.1f}",
        temp_120m=f"{weather_data.json()['avg_temp_120m']:.1f}",
        temp_180m=f"{weather_data.json()['avg_temp_180m']:.1f}",

    )

if __name__=="__main__":
    #app.run(host="0.0.0.0", port=8000)

    #necessary for getting out of development server warning in Flask
    serve(app, host="0.0.0.0", port=8000)


