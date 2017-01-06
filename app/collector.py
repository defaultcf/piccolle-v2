from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Collector:
    def getImgs(self, url:str) -> list:
        """
        画像のスクレイピングを行い、結果をlistで返す
        @param url スクレイピングしたいURL
        @return スクレイピング結果のlist
        """
        if not url: return []

        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        if self.is2ch(url):
            return self.collect2ch(soup)
        else:
            return self.collectNormal(soup, url)


    def is2ch(self, url:str) -> bool:
        """
        urlから2chかどうかを判別する
        @param url 2chかどうか判別したいurl
        @return 2chならTrue、それ以外ならFalse
        """
        for x in ['2ch', 'bbspink']:
            if x in url: return True

        return False


    def collect2ch(self, soup) -> list:
        """
        aタグで書かれた画像のソースを取ってくる
        @param soup BeautifulSoupのsoup
        @return list
        """

        pics = []

        for res in soup.find_all("dd"):
            for line in res.contents:
                text = line.string
                if not text: break
                text = str(text).strip()
                if text.startswith("ttp://") and text.endswith(("jpg", "png")):
                    src = "h" + text
                    pics.append({"src": src})

        for a in soup.find_all("a"):
            text = str(a.string)
            if text.endswith(("jpg", "png")):
                pics.append({"src": text})

        return pics


    def collectNormal(self, soup, url:str) -> list:
        """
        imgタグのsrc属性から画像のソースを取ってくる
        @param soup BeautifulSoupのsoup
        @return list
        """
        pics = []
        for img in soup.find_all("img"):
            src = img.get("src")
            src = urljoin(url, src)
            if src:
                pics.append({"src": src})

        return pics
