from flask import Blueprint
from backend.domains.database import db_session
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

batch = Blueprint('batch', __name__)

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

# 20分内に締め切りを迎えるレースの直前情報を取得する
@batch.route("/before_info/")
def before_info_batch():
    now = datetime.datetime.now()
    time = datetime.timedelta(minutes=20)
    deadline_datetime = now + time
    races = Race.query.filter(deadline_datetime >= Race.deadline, Race.status == RaceStatusEnum.BEFORE).all()
    for race in races:
        try:
            logger.debug(race.before_info_url())
            before_info_data = before_info.get_data(race.before_info_url())
            racers = race.timetable_racers
            # racerもbefore_info_racerも枠順に取得しているため一緒にイテレートできる
            for (racer, before_info_racer) in zip(racers, before_info_data.racers):
                if not racer.has_before_info():
                    racer.set_before_info(before_info_racer)
                    db_session.commit()
            race.status = RaceStatusEnum.IMMEDIATELY_BEFORE
            db_session.commit()
        except:
            logger.error("直前情報の取得に失敗しました")
    return "ok"

@batch.route("/race_result/")
def race_result_batch():
    races = Race.query.filter(Race.status == RaceStatusEnum.IMMEDIATELY_BEFORE).all()
    for race in races:
        try:
            logger.info(race.race_result_url())
            race_rst = race_result.get_data(race.race_result_url())

            if race_rst is not None: #まだレース結果が表示されていなければ次にいく
                race_rst.race_id = race.id
                result = Result().set_params_from_dto(race_rst)
                db_session.add(result)
                db_session.commit()
                db_session.expunge(result)

                racers = race.timetable_racers
                for (rr, racer) in zip(race_rst.racer_results, racers):
                    rr.timetable_racer_id = racer.id
                    racer_result = RacerResult().set_params_from_dto(rr)
                    db_session.add(racer_result)
                    db_session.commit()
                    db_session.expunge(racer_result)
                race.status = RaceStatusEnum.FINISHED
                db_session.commit()
                db_session.expunge(race)
        except:
            logger.error("レース結果の取得に失敗しました")
    return "ok"