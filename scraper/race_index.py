from bs4 import BeautifulSoup
import datetime
import requests
import re

def request_url(jcd, date):
    date_format = "%Y%m%d"
    date_str = date.strftime(date_format)
    return "http://www.boatrace.jp/owpc/pc/race/raceindex?jcd=%s&hd=%s" % (jcd, date_str)


def scrape_index(url):
    r = requests.get(url)
    ri = RaceIndex(r)
    ri.scrape()
    return ri

def run():
    jcds = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
    # jcds = ["02"]
    date = datetime.date.today()
    race_indexes = [scrape_index(request_url(jcd, date)) for jcd in jcds ]
    return race_indexes

# ある日のあるレース会場のレース情報を保持するクラス
class RaceIndex:
    base_url = 'http://www.boatrace.jp'
    def __init__(self, request):
        self.text = request.text
        self.soup = BeautifulSoup(request.text, 'html.parser')
        self.races = []

    def scrape(self):
        race_elms = self.soup.select('div.contentsFrame1 div.table1 tbody')
        for race_elm in race_elms:
            time_str = race_elm.select('td')[1].text
            url_param =  race_elm.select('td a')[0]['href']
            place, race_number, date_str = self.parse_url(url_param)
            deadline = datetime.datetime.strptime(date_str + time_str, '%Y%m%d%H:%M')
            dto = RaceDTO(
                url=RaceIndex.base_url + race_elm.select('td a')[0]['href'],
                deadline=deadline,
                place=place,
                race_number=race_number
            )
            self.races.append(dto)

    def has_race(self):
        return len(self.races) > 0

    def parse_url(self, string):
        race_number = re.findall('.*rno=(.*)&jcd*', string)[0]
        place = re.findall('.*jcd=(.*)&hd*', string)[0]
        date_str = re.findall('.*hd=(.*)', string)[0]
        return (place, race_number, date_str)

class RaceDTO:
    def __init__(self, url=None, place=None, race_number=None, deadline=None):
        self.url = url
        self.place = place
        self.race_number = race_number
        self.deadline = deadline