from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

driver = webdriver.Remote(
    command_executor='http://phantomjs:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS
)
wait = WebDriverWait(driver, 5)

class Board:
    def getList(self, mode:str) -> list:
        """
        掲示板のリストをlistにして返す
        @return list
        """
        if not mode: return []

        if mode == "sc":
            url = "https://2ch.sc/bbstable.html"
        else:
            url = "http://www.2ch.net/bbstable.html"

        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        json = []

        for b in soup.find_all('b'):
            boards = []
            for a in b.find_next_siblings():
                if a.name == 'b': break
                boards.append({"url": a.get("href"), "board": a.text})
            obj = {"category": b.text, "boards": boards}
            json.append(obj)

        return json


    def getThread(self, url:str) -> list:
        """
        板のURLからスレッド一覧を取得してlistにして返す
        @return list
        """
        if not url: return []

        driver.get(url)
        wait.until(ec.presence_of_all_elements_located)

        url = driver.current_url + "subback.html"

        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        # baseタグがあった時の対策
        if soup.find('base'):
            url = soup.find('base').get("href")

        if self.is2chNet(url):
            return self.boardNet(soup, url)
        else:
            return self.boardSc(soup, url)


    def is2chNet(self, url:str) -> bool:
        """
        2ch.netかどうかを判別する
        @param url 2ch.netかどうか判別したいurl
        @return 2ch.netならTrue、それ以外ならFalse
        """
        for x in ['2ch.net', 'bbspink.com']:
            if x in url: return True

        return False


    def boardNet(self, soup, url:str):
        json = []
        for lists in soup.find_all('small'):
            for a in lists.find_all('a'):
                href = urljoin(url, a.get("href"))
                json.append({"thread": a.text, "url": href})

        return json


    def boardSc(self, soup, url:str):
        json = []
        lists = soup.find('small')
        for a in lists.find_all('a'):
            href = urljoin(url, a.get("href"))
            json.append({"thread": a.text, "url": href})

        return json
