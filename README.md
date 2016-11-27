# piccolle-v2
以前PHPで作ったpiccolleのPython版


## About
前作の[piccolle-v1](https://github.com/leoisaac/piccolle)は、まぁまぁ上手くいったと言える。
サーバーサイドではフレームワークを使わず一からPHPで書き、フロントエンドはBootstrapでレスポンシブに作った。

しかし、実用的とは言えなかった。要の画像保存機能は行き詰まり、極めつけはスクレイピングに失敗することもあることだ。
これではダメだと思い、今回一から書き直すことにした。

```
＿人人人人人人人人人人人＿
＞　PythonとPolymerでな　＜
￣Y^Y^Y^Y^Y^Y^Y^Y^Y^Y￣
```


## Usage
```shell
git clone git@github.com:leoisaac/piccolle-v2 && cd piccolle-v2
docker-compose up -d
```
Polymer使用のため、`htdocs/`内で`bower install`してください。
