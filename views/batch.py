# vim:fileencoding=utf8
from flask import Blueprint
from flask import logging
from config.database import db_session
import sys, datetime
sys.path.append("../")
sys.path.append("../models/")
sys.path.append("../scraper/")
from models.race import Race
from models.timetable_racer import TimetableRacer
from scraper import data_download, txt_to_dto_timetable, before_info
import datetime

batch_app = Blueprint("batch", __name__, template_folder="./templates", static_folder="./static")
logger = logging.logging

# 当日のレース予定インポート　http://127.0.0.1:5000/batch/race_index/
# 直前情報インポート　http://127.0.0.1:5000/batch/before_info/

# 重複でインポートしようとしてエラーにならないように一件ずつコミット
def commit(race):
    try:
        db_session.add(race)
        db_session.commit()
    except :
        logger.error("%s のインポートに失敗しました" % race.info())
    finally:
        db_session.remove()

def find_race_id_by_dto(dto):
    race = Race.query.filter_by(place=dto.place, race_number=dto.race_number, deadline=dto.deadline).first()
    if race:
        return race.id
    else:
        logger.error("place:%s, race_number:%s, deadline:%s のレースが見つかりません" % (dto.place, dto.race_number, dto.deadline.strftime("%Y/%m/%d %H:%M:%S")) )
        return None

@batch_app.route("/race_index/")
def index():
    logger.debug("debug/race_index")
    today = datetime.date.today()
    lzh_filename = data_download.download_lzh(today)
    filename = data_download.unpacked(lzh_filename)
    file = txt_to_dto_timetable.open_file(filename)
    race_dto_list = txt_to_dto_timetable.get_data(file)
    logger.info("%i レースの情報を取得しました" % len(race_dto_list))
    races = [Race().set_params_from_dto(race_dto) for race_dto in race_dto_list]
    for race in races: commit(race) #レースの保存
    for race in race_dto_list: #レーサーの保存
        race.set_race_id(find_race_id_by_dto(race))
        racers = [TimetableRacer().set_params_from_dto(racer_dto) for racer_dto in race.racers ]
        for racer in racers: commit(racer)
    return "ok"

# バッチ実行時点から20分内に締め切りを迎えるレースの直前情報を取得する
@batch_app.route("/before_info/")
def before_info_batch():
    now = datetime.datetime.now()
    time = datetime.timedelta(minutes=20)
    deadline_datetime = now + time
    races = Race.query.filter(Race.deadline.between(now, deadline_datetime)).all()
    for race in races:
        logger.debug(race.before_info_url())
        before_info_data = before_info.get_data(race.before_info_url())
        racers = race.timetable_racers
        try:
            # racerもbefore_info_racerも枠順に取得しているため一緒にイテレートできる
            for (racer, before_info_racer) in zip(racers, before_info_data.racers):
                if not racer.has_before_info():
                    racer.set_before_info(before_info_racer)
                    db_session.commit()
        except:
            logger.error("直前情報の取得に失敗しました")
    return "ok"