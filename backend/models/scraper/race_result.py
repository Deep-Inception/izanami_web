from bs4 import BeautifulSoup
import requests
import sys, re
sys.path.append("../")
sys.path.append("../izanamiutils")

from backend.utils.izanamiutils import math_util

def get_data(url):
    r = requests.get(url)
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

    def scrape(self):
        tables = self.soup.select("div.contentsFrame1 table")

        odds = tables[self.RESULT_TABLE].select("tbody tr")
        self.set_odds(odds)

        race_times = tables[self.RACE_TIME_TABLE].select("tbody tr")
        racer_results = [RacerResult(elm) for elm in race_times]
        self.racer_results = sorted(racer_results, key=lambda x:x.couse) # コース順に並び替える

    def has_race_result(self):
        return len(self.soup.select("div.contentsFrame1 table")) == 7

    def set_odds(self, odds):
        self.trifecta = math_util.cast_to_int(delete_comma(odds[0].select("td")[2].text))
        self.trio = math_util.cast_to_int(delete_comma(odds[2].select("td")[2].text))
        self.exacta = math_util.cast_to_int(delete_comma(odds[4].select("td")[2].text))
        self.quinella = math_util.cast_to_int(delete_comma(odds[6].select("td")[2].text))
        self.win = math_util.cast_to_int(delete_comma(odds[13].select("td")[2].text))
        self.show1 = math_util.cast_to_int(delete_comma(odds[15].select("td")[2].text))
        self.show2 = math_util.cast_to_int(delete_comma(odds[16].select("td")[1].text))

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
