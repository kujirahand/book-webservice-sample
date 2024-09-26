# render_templateのインポート ---（※１）
from flask import Flask, render_template

app: Flask = Flask(__name__)


# 「/」にアクセスがあった場合のルーティング
@app.route("/")
def index():
    login_user_name: str = "osamu"
    # 「top.html」に「login_user_name」を当てはめて表示 ---（※２）
    return render_template("top.html", login_user_name=login_user_name)


# 「/write」にアクセスがあった場合のルーティング
@app.route("/write")
def write():
    # 「write.html」の表示 ---（※３）
    return render_template("write.html")


if __name__ == "__main__":
    app.run(debug=True)
