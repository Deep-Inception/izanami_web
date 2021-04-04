from flask import Flask
from flask_cors import CORS
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

app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(race_bp, url_prefix="/races")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(batch, url_prefix="/batch")
app.register_blueprint(prediction, url_prefix="/prediction")

def get_app(debug=True):
    config_path = 'backend.configs.config.BaseConfig'
    log_config_path = 'configs/log_conf_debug.ini'
    if not debug:
        config_path = 'backend.configs.config.ProductionConfig'
    
    app.config.from_object(config_path)
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), log_config_path))
    return app
        

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    else:
        app.config.from_object('backend.configs.config.ProductionConfig')
    return render_template("index.html")
