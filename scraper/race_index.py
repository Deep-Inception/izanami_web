from bs4 import BeautifulSoup

# ある日のあるレース会場のレース情報を保持するクラス
class RaceIndex:
    base_url = 'http://www.boatrace.jp'
    def __init__(self, request):
        self.text = request.text
        self.soup = BeautifulSoup(request.text, 'html.parser')
        self.races = []

    def scrape(self):
        races = self.soup.select('div.contentsFrame1 div.table1 tbody')
        self.races = [RaceDTO(url=RaceIndex.base_url + race.select('td a')[0]['href'], deadline=None) for race in races]

    def has_race(self):
        return len(self.races) > 0

class RaceDTO:
    def __init__(self, url=None, deadline=None):
        self.url = url
        self.deadline = deadline