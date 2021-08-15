import time
import os, datetime, requests
import lhafile
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def get_request(date):
    #変数初期化
    baseurl = "http://www1.mbrace.or.jp/od2/B/"
    url = ""
    file_name = ""
    year = date.year - 2000
    mon = date.month
    first = ""
    second = ""
    day = date.day

    time.sleep(1)
    first = "20" + "{0:02d}".format(year) + "{0:02d}".format(mon)
    second = "/b" + "{0:02d}".format(year)  + "{0:02d}".format(mon) + "{0:02d}".format(day)
    #リンク作成
    url = baseurl + first + second +  ".lzh"
    file_name = url.split("/")[-1]
    session = requests.Session()
    retries = Retry(total=5,  # リトライ回数
                backoff_factor=1,  # sleep時間
                status_forcelist=[500, 502, 503, 504])  # timeout以外でリトライするステータスコード
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    r = session.get(url=url,
                       stream=True,
                       timeout=(10.0, 20.0))
    return r

def download_lzh(date, directory):
    #変数初期化
    time.sleep(1)
    file_name = lzh_filename(date)
    r = get_request(date)

    # 成功したら、書き込み
    if r is not None:
        if r.status_code == 200:
            f = open(directory + "/" + file_name,"wb")
            f.write(r.content)
            f.close()
            print( file_name+ "を取得しました")
        else :
            print(file_name + "がダウンロードできませんでした")
    return file_name

def lzh_filename(date):
    year = date.year - 2000
    mon = date.month
    day = date.day
    time.sleep(1)
    file_name = "b" + "{0:02d}".format(year)  + "{0:02d}".format(mon) + "{0:02d}".format(day) +  ".lzh"
    return file_name

def unpacked(filename, directory):
    lzhfile_path = directory + "/" + filename
    f = lhafile.Lhafile(lzhfile_path)
    unpackedpath = txtfile_path(lzhfile_path)
    unpackedname = os.path.basename(unpackedpath)
    print("Unpacking", lzhfile_path)
    f = lhafile.Lhafile(lzhfile_path)
    info = f.infolist()
    unpacked_name = info[0].filename
    fileobj = open(unpackedpath, "w")
    fileobj.write(f.read(unpacked_name).decode(encoding="shift-jis"))
    fileobj.close()
    os.remove(lzhfile_path)
    return unpackedpath

def txtfile_path(lzhfile_path):
    return lzhfile_path.replace(".lzh", ".txt")

def download_and_unpacked(date, directory):
    lzh_name = lzh_filename(date)
    lzh_path = directory + "/" + lzh_name
    filepath = txtfile_path(lzh_path)

    if os.path.exists(filepath):
        print ("すでに", filepath, "は存在します。")
        return filepath

    lzh_file = download_lzh(date, directory)
    filename = unpacked(lzh_file, directory)
    return filename