# python 3.7

import datetime
import os
import re
import sys

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


# setup package
# pip install -r requirements.txt


def main():
    # 읍면리동 input search
    search = input("검색할 동을 입력해 주세요. 예시) 혜화동\n>>").strip()
    # options = webdriver.ChromeOptions()

    # pyinstaller set if value
    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "./chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path)
    else:
        driver = webdriver.Chrome()
    # $ pyinstaller --onefile --add-binary "chromedriver.exe;." main.py

    # driver.implicitly_wait(3)
    driver.get(
        f'https://s.search.naver.com/n/csearch/content/eprender.nhn?where=nexearch&pkid=252&q={search}%20영문주소&key=address_eng')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ko_parser = soup.select('table tbody tr td dl dd span.r_addr')
    en_parser = soup.select('table tbody tr td strong')

    ko_list = [ko.text for ko in ko_parser]
    # e.g. 전라북도 순창군 금과면 금풍로 206 (금과면) 에서 (금과면) 제거
    ko_list2 = [re.sub('\(.*\)', '', ko.text) for ko in ko_parser]
    en_list = [en.text for en in en_parser]

    driver.quit()

    df = pd.DataFrame({'ko_address': ko_list,
                       'ko_address_repl': ko_list2,
                       'en_address': en_list})
    # time set
    now = datetime.datetime.now()
    now_time = now.strftime('%Y-%m-%d_%H%M%S_')
    print(now_time)  # 2018-07-28_12:11:32_

    df.to_excel('./' + now_time + 'crawling_test.xlsx', index=False)
    os.close()
    print("End")


if __name__ == '__main__':
    main()
