import json
from flask import logging
from flask import Blueprint, request
from backend.domains.user import User
from backend import db_session

login_blueprint = Blueprint('login', __name__)
logger = logging.logging

@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')
    users = db_session.query(User).filter(User.email == email).all()

    for user in users:
        if user.password == password:
            return json.dumps({"result": "success"})
    return json.dumps({"result": "fail"})
