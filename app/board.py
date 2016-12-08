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

        pics = []

        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        json = []
        count = 0

        for count, b in enumerate(soup.find_all('b')):
            json.append({"category": b.text, "boards": []})
            for a in b.find_next_siblings():
                if a.name == 'b': break
                json[count]["boards"].append({"url": a.get("href"), "board": a.text})

        return json
