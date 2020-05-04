from bs4 import BeautifulSoup
from .items.race_list_racer import RaceListRacer


class RaceList:
    def __init__(self, request):
        self.text = request.text
        self.soup = BeautifulSoup(request.text, "html.parser")
        self.recers = []


    def scrape(self):
        racer_elms = self.soup.select("div.contentsFrame1 div.is-tableFixed__3rdadd tbody")
        print("%i recers will run." % len(racer_elms))
        self.racers = [self.racer_from_elm(elm) for elm in racer_elms]


    def racer_from_elm(self, elm):
        try:
            return RaceListRacer(elm)
        except:
            return None
