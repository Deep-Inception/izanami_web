import time
import os, datetime, requests
import lhafile
from .data_download import unpacked

def get_request(date):
    #変数初期化
    baseurl = "http://www1.mbrace.or.jp/od2/K/"
    url = ""
    file_name = ""
    year = date.year - 2000
    mon = date.month
    first = ""
    second = ""
    day = date.day

    time.sleep(1)
    first = "20" + "{0:02d}".format(year) + "{0:02d}".format(mon)
    second = "/k" + "{0:02d}".format(year)  + "{0:02d}".format(mon) + "{0:02d}".format(day)
    #リンク作成
    url = baseurl + first + second +  ".lzh"
    r = requests.get(url)
    return r

def download_lzh(date):
    #変数初期化
    year = date.year - 2000
    mon = date.month
    first = ""
    second = ""
    day = date.day
    time.sleep(1)
    file_name = "k" + "{0:02d}".format(year)  + "{0:02d}".format(mon) + "{0:02d}".format(day) +  ".lzh"
    r = get_request(date)

    # 成功したら、書き込み
    if r is not None:
        if r.status_code == 200:
            f = open("tmp/%s" % file_name,"wb")
            f.write(r.content)
            f.close()
            print( file_name + "を取得しました")
        else :
            print(file_name + "がダウンロードできませんでした")
    return file_name