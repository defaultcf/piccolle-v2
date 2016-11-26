from flask import Flask, request, jsonify
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.update(
    DEBUG=True
)

@app.route("/collecter")
def index():
    url = request.args.get('url', '')
    res = collecter(url)
    return jsonify(res)

if __name__ == "__main__":
    app.run()


def collecter(url):
    """
    画像のスクレイピングを行い、結果をjsonで返す
    @param url スクレイピングしたいURL
    @return スクレイピング結果のjson
    """
    if(url == ""):
        return
    
    count = 0
    pics = []

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        text = str(a.string)
        if text.endswith("jpg") or text.endswith("png"):
            count += 1
            pics.append({"src": text})

    return pics
