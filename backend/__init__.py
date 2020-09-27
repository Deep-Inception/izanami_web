from flask import Flask
from flask_cors import CORS
import requests
from flask_sqlalchemy import SQLAlchemy
import logging.config
import os

app = Flask('FLASK-VUE',
            static_folder = "./dist/static",
            template_folder = "./dist")

app.config.from_object('backend.configs.config.BaseConfig')

db = SQLAlchemy(app)
db_session = db.session

from backend.controllers.login import login_blueprint
from backend.controllers.batch import batch
from backend.controllers.prediction import prediction
app.register_blueprint(login_blueprint, url_prefix="/login")
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(batch, url_prefix="/batch")
app.register_blueprint(prediction, url_prefix="/prediction")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'configs/log_conf_debug.ini'))
        return requests.get('http://localhost:8080/{}'.format(path)).text
    logging.config.fileConfig('configs/log_conf.ini')
    return render_template("index.html")