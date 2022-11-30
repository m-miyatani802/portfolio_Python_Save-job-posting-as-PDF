# -*- coding: utf-8 -*-

from glob import glob
import json
import glob
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time
import datetime
from bs4 import BeautifulSoup
import os

class methodX:
    @staticmethod
    def my_makedirs(path):
        if not os.path.isdir(path):
            os.makedirs(path)

# URLとgoogledriverのpathを設定
URL = 'https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?action=initDisp&screenId=GECA110010'
DRIVER_PATH = 'DRIVER_PATH'

# driver起動
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(URL)
# ハローワーク番号
# 5桁
UPPER_NUMBER = "27520"
# 7桁
LOWER_NUMBER = "1391873"

# 今日の日付を取得
ut = time.time()
print(ut)
dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
print(dt_now)
dir_path = './' + dt_now
methodX.my_makedirs(dir_path)

# 自分が入力、選択する所によって使い分ける

# ➀求職番号を入力
# 上５桁
element = driver.find_element_by_name("kSNoJo")
element.send_keys(UPPER_NUMBER)
# 下７桁
element = driver.find_element_by_name("kSNoGe")
element.send_keys(LOWER_NUMBER)
time.sleep(1)

# ➁求人区分
element = driver.find_element_by_id('ID_ippanCKBox1')
element.click()
element = driver.find_element_by_id("ID_LkjKbnRadioBtn5")
element.click()
time.sleep(1)
# []の中を選択
element = driver.find_element_by_id("ID_LsGSYACKBox1")
element.click()
time.sleep(1)


# ➂年齢
# 今回は使わないので省略

# ➃就業場所
# 都道府県-ドロップダウンの中を選択
element = driver.find_element_by_id('ID_tDFK1CmbBox')
select = Select(element)
# 番号を選択する
select.select_by_value('#')
time.sleep(1)

# 市区町村の選択ボタンを押し、動的ページの中のドロップダウンの中を選択し、動的ページへ
bottom =  driver.find_elements_by_css_selector('input.button')
bottom[1].click()
time.sleep(1)

# 動的ページ
# 市区町村ドロップダウン
element = driver.find_element_by_id('ID_rank1CodeMulti')
select = Select(element)
# ドロップダウンの番号を選択する
select.select_by_value('#')
time.sleep(1)

# # 閉じるボタン
# element = driver.find_element_by_id('ID_close')
# element.click()
# time.sleep(1)

# okボタン
element = driver.find_element_by_id('ID_ok')
element.click()
time.sleep(1)

# ➄希望職種
# 動的ページへ
bottom = driver.find_elements_by_css_selector('input.button')
bottom[4].click()
time.sleep(1)
# 大分類
element = driver.find_element_by_id('ID_rank1Code')
select = Select(element)
select.select_by_value('09')
time.sleep(1)

# 詳細
element = driver.find_element_by_id('ID_rank2Codes')
select = Select(element)
select.select_by_value('4 ')
time.sleep(1)

# okボタン
element = driver.find_element_by_id('ID_ok')
element.click()
time.sleep(1)

# ➅雇用形態
element = driver.find_element_by_id('ID_koyoFltmCKBox1')
element.click()
time.sleep(1)

# ➆フリーワード
element = driver.find_element_by_id('ID_freeWordRadioBtn1')
element.click()
element = driver.find_element_by_id('ID_freeWordInput')
element.send_keys("ＰＹＴＨＯＮ")
time.sleep(2)

# 詳細検索
element = driver.find_element_by_id('ID_searchShosaiBtn')
element.click()
time.sleep(1)

# 学歴
element = driver.find_element_by_id('ID_grkiFumonCKBox1')
element.click()

# ok
element = driver.find_element_by_id('ID_saveCondBtn')
element.click()
time.sleep(1)

# ➇検索ボタンクリック
# 検索後、検索結果ページに遷移する
element = driver.find_element_by_id('ID_searchBtn')
element.click()
time.sleep(5)

# element = driver.find_element_by_name("fwListNaviBtnNext")
# element.click()
# time.sleep(4)

# 検索結果を50件分表示
# element = driver.find_element_by_id('ID_fwListNaviDispTop')
# Select(element).select_by_value('50')
# time.sleep(1)

# 検索結果を10件分表示
element = driver.find_element_by_id('ID_fwListNaviDispTop')
Select(element).select_by_value('10')
time.sleep(1)


message = ""
messages = []

con = 0

# 検索結果をBeautifulSoupで読み込む
soup = BeautifulSoup(driver.page_source, "html.parser")
# ページネーションの”次へ”の部分を読み込む
nextBtn = soup.find('input', attrs={'name': 'fwListNaviBtnNext'})
# 求人の題名を読み込む
job_names = soup.find_all('td', attrs={"class": "m13"})
# 求人番号を読み込む
job_number = soup.find_all('div', attrs={"class": "width16em"})


# 検索結果のページネーションで”次へ”が押せない時に分岐
while nextBtn.has_attr("disabled") == False:
    ind = 0
    for seleni in driver.find_elements_by_id('ID_kyujinhyoBtn'):
        time.sleep(5)
        messages.append(job_number[ind].text.strip())
        print(message)
        con += 1
        ind += 1
        # オプション設定
        options = webdriver.ChromeOptions()
        appState = {
            "recentDestinations": [
                {
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": ""
                }
            ],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        dir_default = "C:/Users/kwtkt/OneDrive/デスクトップ/python_scraping/"+ dt_now
        prefs = {}
        prefs['printing.print_preview_sticky_settings.appState'] = json.dumps(appState)
        prefs['savefile.default_directory'] = dir_default
        options.add_experimental_option('prefs', prefs)
        # --kiosk-printing→印刷画面を開いた際に自動で印刷ボタンを押す
        options.add_argument('--kiosk-printing')
        driver2 = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        # 別ウィンドウで表示
        driver2.get(seleni.get_attribute("href"))
        tab_handler = driver2.current_window_handle
        # 印刷画面の表示
        driver2.execute_script('return window.print()')
        time.sleep(5)
        # ウィンドウを閉じる
        driver2.close()
        # ターミナル内で完了コメントを表示
        print(con, 'complete')

    # # 検索結果を50件分表示
    element = driver.find_element_by_id('ID_fwListNaviDispTop')
    Select(element).select_by_value('50')
    time.sleep(1)

    # ”次へ”を押しページ遷移
    allHandles = driver.window_handles
    element = driver.find_element_by_name("fwListNaviBtnNext")
    element.click()
    
    # ページ遷移後の”次へ”の情報を更新
    soup = BeautifulSoup(driver.page_source, "html.parser")
    nextBtn = soup.find('input', attrs={'name': 'fwListNaviBtnNext'})


else:
    ind = 0
    for seleni in driver.find_elements_by_id('ID_kyujinhyoBtn'):
        messages.append(job_number[ind].text.strip())
        print(message)
        con += 1
        ind += 1
        # オプション設定
        options = webdriver.ChromeOptions()
        appState = {
            "recentDestinations": [
                {
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": ""
                }
            ],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        dir_default = "C:/Users/kwtkt/OneDrive/デスクトップ/python_scraping/"+ dt_now
        prefs = {}
        prefs['printing.print_preview_sticky_settings.appState'] = json.dumps(appState)
        prefs['savefile.default_directory'] = dir_default
        options.add_experimental_option('prefs', prefs)
        # --kiosk-printing→印刷画面を開いた際に自動で印刷ボタンを押す
        options.add_argument('--kiosk-printing')
        driver2 = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        # 別ウィンドウでひょじ
        driver2.get(seleni.get_attribute("href"))
        # 印刷画面の表示
        driver2.execute_script('return window.print()')
        time.sleep(5)
        # ウィンドウを閉じる
        driver2.close()
        # ターミナル内で完了コメントを表示
        print(con, 'complete')

print(messages)

# 終了
driver.quit()
