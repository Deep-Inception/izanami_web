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

from backend.controllers.api import api
app.register_blueprint(api, url_prefix="/api")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'configs/log_conf_debug.ini'))
        return requests.get('http://localhost:8080/{}'.format(path)).text
    logging.config.fileConfig('configs/log_conf.ini')
    return render_template("index.html")