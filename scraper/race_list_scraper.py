import requests
import datetime
import race_index

date = datetime.date.today()

def request_url(jcd, date):
    date_format = "%Y%m%d"
    date_str = date.strftime(date_format)
    return "http://www.boatrace.jp/owpc/pc/race/raceindex?jcd=%s&hd=%s" % (jcd, date_str)


def scrape_index(url):
    r = requests.get(url)
    ri = race_index.RaceIndex(r)
    ri.scrape()
    return ri

# jcds = ["01", "02", "03", "04", "05"]
jcds = ["01", "05"]
race_indexes = [scrape_index(request_url(jcd, date)) for jcd in jcds ]

for i in race_indexes:
    print(i.has_race())