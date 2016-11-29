from flask import Flask, request, jsonify
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.update(
    DEBUG=True
)

@app.route("/collector")
def index_collector():
    url = request.args.get('url', '')
    res = collector(url)
    return jsonify(res)

@app.route("/board-list")
def index_boardList():
    url = "https://2ch.sc/bbstable.html"
    pics = []

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    small = soup.find("small")
    json = []
    count = 0

    for b in small.find_all('b'):
        json.append({"category": b.text, "boards": []})
        for a in b.find_next_siblings():
            if a.name == 'b': break
            json[count]["boards"].append({"url": a.get("href"), "board": a.text})
        count += 1
    return jsonify(json)

if __name__ == "__main__":
    app.run()


def collector(url:str) -> list:
    """
    画像のスクレイピングを行い、結果をlistで返す
    @param url スクレイピングしたいURL
    @return スクレイピング結果のlist
    """
    if not url: return []

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    if is2ch(url):
        return collect2ch(soup)
    else:
        return collectNormal(soup, url)


def is2ch(url:str) -> bool:
    """
    urlから2chかどうかを判別する
    @param url 2chかどうか判別したいurl
    @return 2chならTrue、それ以外ならFalse
    """
    for x in ['2ch', 'bbspink']:
        if x in url: return True

    return False


def collect2ch(soup) -> list:
    """
    aタグで書かれた画像のソースを取ってくる
    @param soup BeautifulSoupのsoup
    @return list
    """
    pics = []
    for a in soup.find_all("a"):
        text = str(a.string)
        if text.endswith(("jpg", "png")):
            pics.append({"src": text})

    return pics


def collectNormal(soup, url:str) -> list:
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
