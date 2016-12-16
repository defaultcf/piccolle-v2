from flask import Flask, request, jsonify

from collector import Collector
from board import Board

app = Flask(__name__)
app.config.update(
    DEBUG=True
)

@app.route("/collector")
def index_collector():
    url = request.args.get('url', '')
    res = Collector().getImgs(url)
    return jsonify(res)

@app.route("/board-list")
def index_boardList():
    mode = request.args.get('mode', '')
    json = Board().getList(mode)
    return jsonify(json)

@app.route("/thread-list")
def index_threadList():
    url = request.args.get('url', '')
    res = Board().getThread(url)
    return jsonify(res)

if __name__ == "__main__":
    app.run()
