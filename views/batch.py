# vim:fileencoding=utf8
from flask import Blueprint
from config.database import db_session
import sys
sys.path.append('../')
sys.path.append('../models/')
sys.path.append('../scraper/')
from models.race import Race
from scraper import race_index

batch_app = Blueprint('batch', __name__, template_folder='../templates', static_folder='./static')

def commit(race):
    try:
        db_session.add(race)
        db_session.commit()
    except:
        print ("import error! %s : %s" % (race.place, race.race_number))
    finally:
        db_session.remove()

@batch_app.route('/race_index/')
def index():
    race = Race()
    race_list_indexes = race_index.run()
    race_dto_list = []
    for race_list_index in race_list_indexes:
        if race_list_index.has_race(): race_dto_list.extend(race_list_index.races)
    races = [Race().set_params_from_dto(race_dto) for race_dto in race_dto_list]
    for race in races: commit(race)
    return "%i races are imported." % len(race_dto_list)