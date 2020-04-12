import re

# 直前情報のレーサーごとの情報を保持するクラス
class BeforeInfoRacer:
    NUMBER_INDEX = 1
    WEIGHT_INDEX = 3
    EXHIBITION_INDEX = 4
    TILT_INDEX = 5
    
    def __init__(self, elm):
        self.elm = elm
        self.number = None
        self.weight = None
        self.exhibition = None
        self.tilt = None
        self.scrape()
        
    def scrape(self):
        self._pase_elm()
        print("number: %s, weight: %s, exb: %s, tilt: %s" % (self.number, self.weight, self.exhibition, self.tilt))
    
    def _pase_elm(self):
        _tds = self.elm.select_one("tr").select("td")
        self.weight = _tds[BeforeInfoRacer.WEIGHT_INDEX].get_text()
        self.exhibition = _tds[BeforeInfoRacer.EXHIBITION_INDEX].get_text()
        self.tilt = _tds[BeforeInfoRacer.TILT_INDEX].get_text()
        _src = _tds[BeforeInfoRacer.NUMBER_INDEX].select_one("img")['src']
        self.number = self._parse_src(_src)
    
    def _parse_src(self, string):
        return re.findall('/racerphoto/(.*).jpg', string)[0]
