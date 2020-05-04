import re, os, datetime

def open_file(file_name):
    f = open("tmp/" + file_name,"r")
    return f

def get_data(f):
    # 一行目は情報なし
    date_str = re.search(r"([0-9]+)", f.name).group()
    f.readline()

    # ここから１レースごとの情報
    place = None
    race_name = None
    rase_list = []
    for r in f :
        # レース場ごとの繰り返し
        if re.search(r"BBGN",r):
            place = r[0:2]
            f.readline() # 空行
            f.readline() # 空行
            f.readline() # 番組表
            f.readline() # 空行
            race_name = f.readline().strip()
            # print(race_name)
            f.readline() # 空行
            f.readline() # 日付とか
            f.readline() # 空行
            f.readline() # 注意書き
            f.readline() # 空行
            f.readline() # 空行
            # レースごとの繰り返し
        if re.search(r"Ｒ",r) and re.search(r"Ｈ",r):
                race_number = int(re.findall('(.*)Ｒ', r)[0])
                distance = int(re.findall('Ｈ(.*)ｍ', r)[0])
                time = re.findall('電話投票締切予定(.*：.*)', r)[0]
                deadline = datetime.datetime.strptime("20" + date_str + cast_time(time), '%Y%m%d%H:%M')
                race = RaceDTO(place=place, race_number=race_number,deadline=deadline, distance=distance, title_name=race_name)
                rase_list.append(race)
                f.readline() # 空行
                f.readline() # 空行
                f.readline() # 空行
                f.readline() # 空行
                l = f.readline()

                # レーサーごとの繰り返し
                while l != "\n":
                    if re.search(r"BEND",l):
                        place = None
                        break
                    racer = create_timetable_racer(l)
                    race.racers.append(racer)
                    # print(racer.__dict__)
                    l = f.readline()
    return rase_list

def cast_time(time_str):
    hour = str(int(time_str[0:2])).zfill(2)
    min = str(int(time_str[3:5])).zfill(2)
    return "%s:%s" % (hour, min)

def create_timetable_racer(l):
    racer = TimeTableRacer()
    racer.couse = l[0]
    racer.racer_id = l[2:6]
    racer.name = l[6:10]
    racer.age = int(l[10:12])
    racer.weight = int(l[14:16])
    racer.rank = l[16:18]
    racer.win_rate = float(l[19:23])
    racer.exacta_rate = float(l[24:29])
    racer.win_rate_place = float(l[30:34])
    racer.exacta_rate_place = float(l[35:40])
    racer.moter_id = int(l[41:43])
    racer.exacta_rate_motor = float(l[44:49])
    racer.boat_id = int(l[50:52])
    racer.exacta_rate_boat = float(l[53:58])
    racer.result_1 = l[59:61]
    racer.result_2 = l[61:63]
    racer.result_3 = l[63:65]
    racer.result_4 = l[65:67]
    racer.result_5 = l[67:69]
    racer.result_6 = l[69:71]
    return racer

class RaceDTO:
    def __init__(self, place=None, race_number=None, deadline=None, distance=None, title_name=None):
        self.id = None
        self.place = place
        self.race_number = race_number
        self.deadline = deadline
        self.distance = distance
        self.title_name = title_name
        self.racers = []

    def set_race_id(self, id):
        for racer in self.racers: racer.race_id = id

class TimeTableRacer:
    def __init__(self, couse=None, name=None, racer_id=None, rank=None, age=None, weight=None, moter_id=None, boat_id=None):
        self.race_id = None
        self.couse = couse
        self.name = name
        self.racer_id = racer_id
        self.rank = rank
        self.age = age
        self.weight = weight
        # self.f_score = None
        # self.l_score = None
        self.st_ave = None
        self.moter_id = moter_id
        self.boat_id = boat_id
        self.win_rate = None
        self.exacta_rate = None
        self.win_rate_place = None
        self.exacta_rate_place = None
        self.exacta_rate_motor = None
        self.exacta_rate_boat = None
        self.result_1 = None
        self.result_2 = None
        self.result_3 = None
        self.result_4 = None
        self.result_5 = None
        self.result_6 = None
