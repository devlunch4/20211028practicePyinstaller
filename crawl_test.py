import os.path
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
from PyQt5.QtWidgets import *
import requests

if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome()


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.le = QLineEdit()
        self.le.setPlaceholderText('검색어를 입력하시오. ')
        self.le.returnPressed(self.crawl)

        self.btn = QPushButton('검색')
        self.btn.clicked(self.crawl)

        grid = QGridLayout()
        grid.addWidget(self.le, 0, 0, 1, 4)
        grid.addWidget(self.btn, 2, 0, 1, 4)
        self.setLayout(grid)

        self.setWindowTitle('Ko>En Address Crawler')
        self.setGeometry(100, 100, 400, 250)
        self.show()

    def crawl(self):
        search = self.le.text()
        # options = webdriver.ChromeOptions()
        driver = webdriver.Chrome('./chromedriver.exe')
        # driver.implicitly_wait(3)

        driver.get(f'https://s.search.naver.com/n/csearch/content/eprender.nhn?where=nexearch&pkid=252&q={search}%20영문주소&key=address_eng')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ko_parser = soup.select('table tbody tr td dl dd span.r_addr')
        en_parser = soup.select('table tbody tr td strong')

        ko_list = [ko.text for ko in ko_parser]
        # 전라북도 순창군 금과면 금풍로 206 (금과면) 에서 (금과면) 제거
        ko_list2 = [re.sub('\(.*\)','',ko.text) for ko in ko_parser]
        en_list = [en.text for en in en_parser]

        driver.quit()

        df = pd.DataFrame({'ko_address': ko_list,
                           'ko_address_repl': ko_list2,
                           'en_address': en_list})
        df.to_excel('./crawling_test.xlsx', index=False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())