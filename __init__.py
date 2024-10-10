from flask import Flask
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather'
db.init_app(app) # to add the app inside SQLAlchemy()

# a simple page that says hello
@app.route('/')
def index():
    return f'Hello!'

if __name__ == '__main__':
    app.run(debug=True)