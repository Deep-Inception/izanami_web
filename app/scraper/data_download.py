import time
import os, datetime, requests
import lhafile

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
    file_name = "b" + "{0:02d}".format(year)  + "{0:02d}".format(mon) + "{0:02d}".format(day) +  ".lzh"
    r = get_request(date)

    # 成功したら、書き込み
    if r is not None:
        if r.status_code == 200:
            f = open("tmp/%s" % file_name,"wb")
            f.write(r.content)
            f.close()
            print( url+ "を取得しました")
        else :
            print(file_name + "がダウンロードできませんでした")
    return file_name

def unpacked(filename):
    lzhfile_path = "tmp/%s" % filename
    f = lhafile.Lhafile(lzhfile_path)
    print(lzhfile_path)
    unpackedpath = lzhfile_path.replace(".lzh", ".txt")
    unpackedname = os.path.basename(unpackedpath)
    if not os.path.exists(unpackedpath):
        print("Unpacking", lzhfile_path)
        f = lhafile.Lhafile(lzhfile_path)
        info = f.infolist()
        unpacked_name = info[0].filename
        fileobj = open(unpackedpath, "w")
        fileobj.write(f.read(unpacked_name).decode(encoding="shift-jis"))
        fileobj.close()
        os.remove(lzhfile_path)
    return unpackedname