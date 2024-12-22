from flask import Flask
from db import db
from routes.main import main
from routes.api import api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/benca/ProjectBandI/sqlite/host.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'benji'

db.init_app(app)

# Create tables when the app starts
with app.app_context():
    db.create_all()

app.register_blueprint(main)
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
