from bs4 import BeautifulSoup
from .items.before_info_racer import BeforeInfoRacer
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

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
    re = BeforeInfo(r)
    re.scrape()
    return re

# BeforeInfoページの情報を保持するクラス
class BeforeInfo():
    def __init__(self, request):
        self.soup = BeautifulSoup(request.text, "html.parser")
        self.racers = []

    def scrape(self):
        self.racers = [BeforeInfoRacer(elm) for elm in self.soup.select("div.table1 tbody.is-fs12")]
