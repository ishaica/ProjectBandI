from flask import Flask
from db import db
from routes.main import main
from routes.api import api

app = Flask(__name__)

app.config['SQLALCHEMY_BINDS'] = {
    'event_db': 'sqlite:////home/BenCarmel123/fatty-popup/fatty-popup/event.db'
}
app.config['ADMIN_USERNAME'] = 'affogato_master'
app.config['ADMIN_PASSWORD'] = 'BenjiBear1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'benji'

db.init_app(app)

with app.app_context():
    db.create_all(bind_key='event_db')  
app.register_blueprint(main)
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
