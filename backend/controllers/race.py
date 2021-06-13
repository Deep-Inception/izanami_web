import datetime
from itertools import groupby

from flask import Blueprint, jsonify, request, make_response, request
from flask import logging
from backend.domains.race import Race
from backend.domains.timetable_racer import TimetableRacer

race_bp = Blueprint('races', __name__)
logger = logging.logging

@race_bp.route('/')
def index():
    date_str = request.args.get('date')
    today = datetime.datetime.today()
    date_str = date_str if date_str != None else today.strftime("%Y%m%d")
    date_sta = datetime.datetime.strptime( date_str + "0000", "%Y%m%d%H%M")
    date_en = datetime.datetime.strptime( date_str + "2359", "%Y%m%d%H%M")
    races = Race.query.filter(Race.deadline >= date_sta, Race.deadline <= date_en).all()
    race_li = [race.race_index_hash() for race in races]
    race_li.sort(key=lambda item: item['place'])
    race_grouped = groupby(race_li, key=lambda m: m['place'])
    race_dict = to_dict_from_groupby(race_grouped)
    return jsonify(race_dict)

def to_dict_from_groupby(item):
    res = []
    for key, group in item:
        place_datum = {}
        place_datum["place"] = key
        place_datum["races"] = list(group)
        res.append(place_datum)
    return res

@race_bp.route('/<date>/<place>/<race_number>')
def race(date, place, race_number):
    date_sta = datetime.datetime.strptime( date + "0000", "%Y%m%d%H%M")
    date_en = datetime.datetime.strptime( date + "2359", "%Y%m%d%H%M")
    race = Race.query.filter(Race.place == place, Race.race_number ==  int(race_number), Race.deadline >= date_sta, Race.deadline <= date_en).first()
    if race == None:
        return jsonify({})
    racers = race.timetable_racers
    return jsonify(racer_dict(racers))

def racer_dict(racers):
    result = []
    for racer in racers:
        datum = {}
        datum["couse"] = racer.couse
        datum["racer"] = racer.detail()
        result.append(datum)
    return result
