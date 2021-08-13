from flask import Blueprint
from flask import logging
import sys
import datetime
sys.path.append("../")
sys.path.append("../models/")
sys.path.append("../scraper/")
from backend.domains.race import Race, RaceStatusEnum
from backend.domains.timetable_racer import TimetableRacer
from backend.domains.racer_result import RacerResult
from backend.domains.result import Result
from backend.models.scraper import data_download, txt_to_dto_timetable, before_info, race_result
from backend import db_session

batch = Blueprint('batch', __name__)
logger = logging.logging

# 当日のレース予定インポート http://127.0.0.1:5000/batch/race_index/
# 直前情報インポート http://127.0.0.1:5000/batch/before_info/

# 重複でインポートしようとしてエラーにならないように一件ずつコミット
def commit(race):
    try:
        db_session.add(race)
        db_session.commit()
    except :
        logger.error("%s のインポートに失敗しました" % race.info())
    finally:
        db_session.expunge_all()

def find_race_id_by_dto(dto):
    race = Race.query.filter_by(place=dto.place, race_number=dto.race_number, deadline=dto.deadline).first()
    if race:
        return race.id
    else:
        logger.error("place:%s, race_number:%s, deadline:%s のレースが見つかりません" % (dto.place, dto.race_number, dto.deadline.strftime("%Y/%m/%d %H:%M:%S")) )
        return None

@batch.route("/race_index/")
def index():
    logger.debug("debug/race_index")
    today = datetime.date.today()
    import_race_data(today)
    return "ok"

def import_race_data(date):
    directory = "backend/tmp/racedata"
    filename = data_download.download_and_unpacked(date, directory)
    file = txt_to_dto_timetable.open_file(filename)
    race_dto_list = txt_to_dto_timetable.get_data(file)
    logger.info("%i レースの情報を取得しました" % len(race_dto_list))
    races = [Race().set_params_from_dto(race_dto) for race_dto in race_dto_list]
    for race in races: commit(race) #レースの保存
    for race in race_dto_list: #レーサーの保存
        race.set_race_id(find_race_id_by_dto(race))
        racers = [TimetableRacer().set_params_from_dto(racer_dto) for racer_dto in race.racers ]
        for racer in racers: commit(racer)

# 15分内に締め切りを迎えるレースの直前情報を取得する
@batch.route("/before_info/")
def before_info_batch():
    now = datetime.datetime.now()
    time = datetime.timedelta(minutes=15)
    deadline_datetime = now + time
    # 展示タイムが表示される前の可能性があるので、IMMEDIATELY_BEFOREのレースも取得する
    races = Race.query.filter(deadline_datetime >= Race.deadline, (Race.status == RaceStatusEnum.BEFORE) | (Race.status == RaceStatusEnum.IMMEDIATELY_BEFORE) ).all()
    logger.info( f"{len(races)} 直前情報の取得中")
    for race in races:
        try:
            logger.info(race.before_info_url())
            before_info_data = before_info.get_data(race.before_info_url())
            racers = race.timetable_racers
            # racerもbefore_info_racerも枠順に取得しているため一緒にイテレートできる
            for (racer, before_info_racer) in zip(racers, before_info_data.racers):
                if not racer.has_before_info():
                    racer.set_before_info(before_info_racer)
            race.status = RaceStatusEnum.IMMEDIATELY_BEFORE
            db_session.commit()
        except Exception as e:
            logger.error(f"直前情報の取得に失敗しました {race.id} {race.before_info_url()}")
            logger.error(f"type: {str(type(e))}")
            logger.error(f"args: {str(e.args)}")
    return "ok"

# 30分以上前に締め切りを迎えたレースの結果を取得する
@batch.route("/race_result/")
def race_result_batch():
    now = datetime.datetime.now()
    time = datetime.timedelta(minutes=30)
    deadline_datetime = now - time
    races = Race.query.filter(deadline_datetime >= Race.deadline,Race.status == RaceStatusEnum.IMMEDIATELY_BEFORE).all()
    for race in races:
        try:
            logger.info(race.race_result_url())
            race_rst = race_result.get_data(race.race_result_url())
            if race_rst is not None: #まだレース結果が表示されていなければ次にいく
                if race_rst.stop:
                    race.status = RaceStatusEnum.STOPPED
                    race.has_prediction = True
                    db_session.commit()
                    db_session.expunge(race)
                else:
                    race_rst.race_id = race.id
                    result = Result().set_params_from_dto(race_rst)
                    db_session.add(result)

                    racers = race.timetable_racers
                    for (rr, racer) in zip(race_rst.racer_results, racers):
                        rr.timetable_racer_id = racer.id
                        racer_result = RacerResult().set_params_from_dto(rr)
                        db_session.add(racer_result)

                    race.status = RaceStatusEnum.FINISHED
                    # 結果を取得したレースはレース結果を予想する必要がないので、予想済フラグを立てる
                    race.has_prediction = True
                    db_session.commit()
                    db_session.expunge(result)
                    db_session.expunge(racer_result)
                    db_session.expunge(race)
        except Exception as e:
            logger.error(f"レース結果の取得に失敗しました {race.id}")
            logger.error(f"type: {str(type(e))}")
            logger.error(f"args: {str(e.args)}")
    return "ok"