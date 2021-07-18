from flask import Blueprint, jsonify, logging
import datetime
import numpy as np
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.race import Race, RaceStatusEnum
from backend.controllers import prediction_racer_prize_lgb
from backend import db_session
from backend.models import boatticket
import backend.utils.izanamiutils.race_util as race_util

view_prediction = Blueprint('view_prediction', __name__)
logger = logging.logging

@view_prediction.route("/<date>/<place>/<race_number>")
def predict(date, place, race_number):
    date_sta = datetime.datetime.strptime( date + "0000", "%Y%m%d%H%M")
    date_en = datetime.datetime.strptime( date + "2359", "%Y%m%d%H%M")
    race = Race.query.filter(Race.place == place, Race.race_number ==  int(race_number), Race.deadline >= date_sta, Race.deadline <= date_en).first()
    if race is None:
        return jsonify({})
    pred_values, course_list = prediction_values(race, "racer_prize_lgb", 1)

    if len(pred_values) == 0:
        return jsonify({})

    win_rates = race_util.win_rate(pred_values)
    exacta = boatticket.exacta.Exacta(win_rates)
    trifecta = boatticket.trifecta.Trifecta(win_rates)
    quinella = boatticket.quinella.Quinella(win_rates)
    trio = boatticket.trio.Trio(win_rates)
    data = {}
    data["exacta"] = index_to_course(list(exacta.predict()), course_list)
    data["trifecta"] = index_to_course(list(trifecta.predict()), course_list)
    data["quinella"] = index_to_course(list(quinella.predict()), course_list)
    data["trio"] = index_to_course(list(trio.predict()), course_list)
    return jsonify(data)

def prediction_values(race, model, version):
    predictions = [tr.racer_predictions for tr in race.timetable_racers]
    pred_list = []
    couse_list = []
    for preds in predictions:
        for pred in preds:
            if pred.is_this_version(model, version):
                pred_list.append(pred.value)
                couse_list.append(str(pred.timetable_racer.couse))
    return pred_list, couse_list

def index_to_course(pred_list, course_list):
    res = []
    for pred in pred_list:
        pred_couse = [course_list[pred_idx] for pred_idx in pred]
        res.append(pred_couse)
    return res
