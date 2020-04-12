import re

# RaceListの1レーサー分のデータをスクレイプし、保持する
class RaceListRacer:
    COUSE_INDEX = 0
    PARSONAL_INDEX = 2
    FL_INDEX = 3
    MOT0R_INDEX = 6
    BOAT_INDEX = 7


    def __init__(self, elm):
        self.elm = elm
        self.couse = None
        self.name = None
        self.racer_id = None
        self.rank = None
        self.age = None
        self.weight = None
        self.f_score = None
        self.l_score = None
        self.st_ave = None
        self.moter_id = None
        self.boat_id = None
        self.scrape()
        self._print_self()


    def scrape(self):
        _tds = self.elm.select("tr td")
        self.couse = int(_tds[self.COUSE_INDEX].text)
        self._set_parsonal(_tds[self.PARSONAL_INDEX])
        self._set_fl(_tds[self.FL_INDEX])
        self._set_motor(_tds[self.MOT0R_INDEX])
        self._set_boat(_tds[self.BOAT_INDEX])


    def _print_self(self):
        print("couse: %i, name: %s, racer_id: %s, rank: %s, age: %s, weight: %s, f: %s, l: %s, st: %s, motor_id: %s, boat_id: %s"
         % (self.couse, self.name, self.racer_id, self.rank, self.age, self.weight, self.f_score, self.l_score, self.st_ave, self.moter_id, self.boat_id))


    def _set_parsonal(self, elm):
        self.name = elm.select_one("a").text
        _dtl = elm.select_one("div").text
        _dtl = _dtl.splitlines()
        self.racer_id = _dtl[1].strip(' ')
        self.rank = _dtl[2].strip(' ''/')
        _dtl2 = elm.select("div")[-1].text.splitlines()
        self.age = self._parse_age(_dtl2[2].strip())
        self.weight = self._parse_weight(_dtl2[2].strip())


    def _parse_age(self, string):
        return re.findall('(.*)歳', string)[0]


    def _parse_weight(self, string):
        return re.findall('.*/(.*)kg', string)[0]

    def _set_fl(self, elm):
        _dtl = elm.text.splitlines()
        self.f_score = re.findall('F(.*)', _dtl[1].strip())[0]
        self.l_score = re.findall('L(.*)', _dtl[2].strip())[0]
        self.st_ave = _dtl[3].strip()


    def _set_motor(self, elm):
        _dtl = elm.text.splitlines()
        self.moter_id = int(_dtl[1].strip())


    def _set_boat(self, elm):
        _dtl = elm.text.splitlines()
        self.boat_id = int(_dtl[1].strip())
