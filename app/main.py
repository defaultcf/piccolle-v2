from flask import Flask, request, jsonify
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.update(
    DEBUG=True
)

@app.route("/collector")
def index():
    url = request.args.get('url', '')
    res = collector(url)
    return jsonify(res)

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
