from urllib.request import urlopen
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
