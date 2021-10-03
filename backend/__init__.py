from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import logging.config
import os

app = Flask('FLASK-VUE',
            static_folder="./dist/static",
            template_folder="./dist")
app.url_map.strict_slashes = False
app.config.from_object('backend.configs.config.BaseConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db_session = db.session

from backend.controllers.login import login_blueprint
from backend.controllers.batch import batch
from backend.controllers.prediction import prediction
from backend.controllers.race import race_bp
from backend.controllers.view_prediction import view_prediction
from backend.controllers.statistics import statistics_blueprint


app.register_blueprint(login_blueprint, url_prefix="/api/login")
app.register_blueprint(race_bp, url_prefix="/api/races")
app.register_blueprint(view_prediction, url_prefix="/api/view_prediction")
app.register_blueprint(statistics_blueprint, url_prefix="/api/statistics")

app.register_blueprint(batch, url_prefix="/batch")
app.register_blueprint(prediction, url_prefix="/prediction")

def get_app(debug=True):
    config_path = 'backend.configs.config.BaseConfig'
    log_config_path = 'configs/log_conf_debug.ini'
    if not debug:
        config_path = 'backend.configs.config.ProductionConfig'
        log_config_path = 'configs/log_conf.ini'
    
    app.config.from_object(config_path)
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), log_config_path))
    return app

@app.route('/', defaults={'path': ''})
def catch_all(path):
    return "ok"
