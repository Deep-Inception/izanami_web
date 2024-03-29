from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
import sys, re
sys.path.append("../")
sys.path.append("../izanamiutils")

from backend.utils.izanamiutils import math_util

def get_data(url):
    session = requests.Session()
    retries = Retry(total=5,  # リトライ回数
                backoff_factor=1,  # sleep時間
                status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    r = session.get(url=url,
                       stream=True,
                       timeout=(10.0, 20.0))

    result = RaceResult(r)
    if result.has_race_result():
        result.scrape()
        return result
    else:
        return None

def delete_comma(value):
    value = value.replace("¥", "")
    return value.replace(",", "")

class RaceResult:
    RACE_TIME_TABLE = 1
    RESULT_TABLE = 3

    def __init__(self, request=None):
        self.soup = BeautifulSoup(request.text, "html.parser")
        self.race_id = None
        self.win = None # 単勝
        self.exacta =  None # 二連単
        self.quinella =  None # 二連複
        self.trifecta =  None # 三連単
        self.trio =  None # 三連複
        self.show1 =  None # 複勝1位
        self.show2 =  None # 複勝2位
        self.racer_results = []
        self.stop = False

    def scrape(self):
        if self.stop_race():
            self.stop = True
        else:
            tables = self.soup.select("div.contentsFrame1 table")

            odds = tables[self.RESULT_TABLE].select("tbody tr")
            self.set_odds(odds)

            race_times = tables[self.RACE_TIME_TABLE].select("tbody tr")
            racer_results = [RacerResult(elm) for elm in race_times]
            self.racer_results = sorted(racer_results, key=lambda x:x.couse) # コース順に並び替える

    def has_race_result(self):
        return len(self.soup.select("div.contentsFrame1 table")) == 7 or self.stop_race()

    def set_odds(self, odds):
        self.trifecta = math_util.cast_to_int(delete_comma(odds[0].select("td")[2].text))
        self.trio = math_util.cast_to_int(delete_comma(odds[2].select("td")[2].text))
        self.exacta = math_util.cast_to_int(delete_comma(odds[4].select("td")[2].text))
        self.quinella = math_util.cast_to_int(delete_comma(odds[6].select("td")[2].text))
        self.win = math_util.cast_to_int(delete_comma(odds[13].select("td")[2].text))
        self.show1 = math_util.cast_to_int(delete_comma(odds[15].select("td")[2].text))
        self.show2 = math_util.cast_to_int(delete_comma(odds[16].select("td")[1].text))

    def stop_race(self):
        ru = self.soup.select("h3.title12_title")
        if len(ru) == 1:
            race_result_text = ru[0].text
            return re.search(r"レース中止",race_result_text)
        else:
            return False

class RacerResult:
    PLIZE = 0
    COUSE = 1
    TIME = 3

    def __init__(self, elm):
        self.elm = elm
        self.timetable_racer_id = None
        self.time = None
        self.prize = None
        self.couse = None
        self.scrape()

    def scrape(self):
        tds = self.elm.select("td")
        if len(tds[self.PLIZE].text.strip()) > 0:
            self.prize = math_util.trim_text(tds[self.PLIZE].text)
        race_time = re.split("[\'\"]", tds[self.TIME].text)
        if len(race_time) == 3:
            self.time = math_util.cast_to_float(race_time[0])*60 + math_util.cast_to_float(race_time[1]) + math_util.cast_to_float(race_time[2])/10
        self.couse = math_util.cast_to_int(tds[self.COUSE].text)
        return None
