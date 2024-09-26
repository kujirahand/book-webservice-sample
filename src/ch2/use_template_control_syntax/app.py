# render_templateのインポート
from flask import Flask, render_template

app: Flask = Flask(__name__)


# 掲示板の一つ一つのメッセージを示すクラス ---（※１）
class Message:
    # コンストラクタ
    def __init__(self, id: str, user_name: str, contents: str):
        self.id = id
        self.user_name = user_name
        self.contents = contents


# 「/」にアクセスがあった場合のルーティング
@app.route("/")
def index():
    login_user_name: str = "osamu"
    # メッセージリストを作成 ---（※２）
    message_list = [
        Message("202400502102310", "osamu", "朝からビールですか！楽しみです。"),
        Message("202400502100223", "noriko", "こちらこそ！次回はABコースで！"),
        Message("202400502092101", "osamu", "昨日はHBコース楽しかったです！"),
    ]
    # 「top.html」に「login_user_name」や「message_list」を当てはめて表示 ---（※３）
    return render_template(
        "top.html", login_user_name=login_user_name, message_list=message_list
    )


# 「/write」にアクセスがあった場合のルーティング
@app.route("/write")
def write():
    # 「write.html」の表示
    return render_template("write.html")


if __name__ == "__main__":
    app.run(debug=True)
