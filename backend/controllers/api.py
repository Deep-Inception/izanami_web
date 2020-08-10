from flask import Blueprint, jsonify, request, make_response
from flask import logging
from backend import app, db

# from backend.models import Task

api = Blueprint('api', __name__)
from backend.controllers.batch import batch
from backend.controllers.prediction import prediction
app.register_blueprint(batch, url_prefix="/batch")
app.register_blueprint(prediction, url_prefix="/prediction")

logger = logging.logging

@api.route('/hello/<string:name>/')
def say_hello(name):
    response = { 'msg': "Hello {}".format(name) }
    return jsonify(response)

@api.route('/random')
def random_number():
    response = {
        'randomNumber': 99
    }
    return jsonify(response)

@api.route('/get', methods=['GET'])
def get_taks():
    taks = Task.query.order_by(Task.id.desc()).all()
    taks_dict = [task.to_dict() for task in taks]
    return jsonify(taks_dict)

@api.route('/add', methods=['POST'])
def add_task():
    task = Task(
            title=request.form['title'],
            text=request.form['text']
            )
    db.session.add(task)
    db.session.commit()
    task = Task.query.order_by(Task.id.desc()).first()
    id = str(task.id)
    r = make_response(id)
    return r

@api.route('/delete', methods=['POST'])
def delete_task():
    id=request.form['id']
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    r = make_response(id)
    return r