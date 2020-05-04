from bs4 import BeautifulSoup
from .items.before_info_racer import BeforeInfoRacer
import requests

def get_data(url):
    r = requests.get(url)
    re = BeforeInfo(r)
    re.scrape()
    return re

# BeforeInfoページの情報を保持するクラス
class BeforeInfo():
    def __init__(self, request):
        # self.text = request.text
        self.soup = BeautifulSoup(request.text, 'html.parser')
        self.racers = []

    def scrape(self):
        self.racers = [BeforeInfoRacer(elm) for elm in self.soup.select('div.table1 tbody.is-fs12')]
