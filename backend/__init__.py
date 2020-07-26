from flask import Flask, request, redirect, url_for
from flask_cors import CORS
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap

app = Flask('FLASK-VUE',
            static_folder = "./dist/static",
            template_folder = "./dist")
app.config.from_object('backend.config.BaseConfig')

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

from backend.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# 未認証の際のリダイレクト先を設定
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('app.login'))

############# route ##############

from backend.view import view
app.register_blueprint(view, url_prefix="/-")

from backend.api import api
app.register_blueprint(api, url_prefix="/api")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")