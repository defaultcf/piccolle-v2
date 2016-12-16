from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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
        url += "subback.html"

        #html = urlopen(url)
        html = requests.get(url, allow_redirects=True)
        soup = BeautifulSoup(html, "html.parser")
        json = []

        # baseタグがあった時の対策
        if soup.find('base'):
            url = soup.find('base').get("href")

        lists = soup.find('small')
        for a in lists.find_all('a'):
            href = urljoin(url, a.get("href"))
            json.append({"thread": a.text, "url": href})

        return json
