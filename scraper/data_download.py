import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
import os, datetime
date = datetime.date.today()
date_format = "%d"
day_str = date.strftime(date_format)

# os.getcwd()で出力できるのはこのファイルのディレクトリのパスではなく、カレントディレクトリ
path = os.getcwd() + "/tmp"
chrome_options = Options()
# chrome_options.add_argument('--headless')
prefs = {}
prefs['download.default_directory'] = path
prefs['download.directory_upgrade'] = True
prefs['download.prompt_for_download'] = False
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('http://www1.mbrace.or.jp/od2/B/dindex.html')
wait = WebDriverWait(driver, 100)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "menu")))
drop_down = driver.find_element_by_name("MONTH")
# 今月は一番上の選択肢なので、特に指定する必要なし
drop_down.send_keys('202004')
time.sleep(10)
driver.switch_to.default_content()
time.sleep(2)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "JYOU")))
driver.find_element_by_xpath("//input[@value='%s']" % day_str).click()
time.sleep(5)
driver.find_element_by_xpath("//input[@value='ダウンロード開始']").click()