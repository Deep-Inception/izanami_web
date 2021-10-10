import datetime
from flask import logging, jsonify
from flask import Blueprint, request
from backend import db_session

from backend.domains.race import Race
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.racer_result import RacerResult
from backend.domains.racer_prediction import RacerPrediction
from backend.domains.result import Result

statistics_blueprint = Blueprint('statistics', __name__)
logger = logging.logging


@statistics_blueprint.route('/', methods=['GET', 'POST'])
def statistics():
    ticket_type = request.args.get('ticketType', '')
    race_date = request.args.get('raceDate', '').replace('-', '')
    place = request.args.get('place', '')

    # 結果格納用
    result = {}
    ai_result = {}
    data = {}

    # 対象のレースを取得する
    race_date_from = datetime.datetime.strptime(race_date + "0000", "%Y%m%d%H%M")
    race_date_to = datetime.datetime.strptime(race_date + "2359", "%Y%m%d%H%M")
    race_id_list = db_session.query(Race.id).filter(Race.deadline >= race_date_from, Race.deadline <= race_date_to,
                                                    Race.place == place).all()

    if len(race_id_list) == 0:
        data["result"] = 'false'
        return jsonify(data)

    # レースID毎の1位のレーサーを取得する
    for race_id in race_id_list:
        racer_id = db_session.query(TimetableRacer.racer_id, RacerResult).outerjoin(RacerResult,
                                                                                      TimetableRacer.id == RacerResult.timetable_racer_id).filter(
            TimetableRacer.race_id == race_id[0], RacerResult.prize == 1).all()
        result[race_id[0]] = racer_id[0][0]

    # AI予想の1位のレーサーIDを取得
    for race_id in race_id_list:
        racer_id = db_session.query(TimetableRacer.racer_id, RacerPrediction).outerjoin(RacerPrediction,
                                                                                      TimetableRacer.id == RacerPrediction.timetable_racer_id).filter(
            TimetableRacer.race_id == race_id[0]).order_by(RacerPrediction.value).limit(1).all()
        ai_result[race_id[0]] = racer_id[0][0]

    # hitRate確認
    correct = 0
    incorrect = 0
    balance = 0
    recovery_amount = 0
    for race_id in race_id_list:
        if result[race_id[0]] == ai_result[race_id[0]]:
            correct += 1
            balance += db_session.query(Result.win).filter(Result.race_id == race_id[0]).all()[0][0] - 100
            recovery_amount += db_session.query(Result.win).filter(Result.race_id == race_id[0]).all()[0][0]
        else:
            incorrect += 1
            balance -= 100

    data["result"] = 'success'
    data["hitRate"] = round((correct / (correct + incorrect)) * 100, 1)
    data["purchaseAmount"] = len(race_id_list) * 100
    data["purchaseCount"] = len(race_id_list)
    data["balance"] = balance
    data["recoveryRate"] = round((recovery_amount / data["purchaseAmount"]) * 100, 1)

    return jsonify(data)
