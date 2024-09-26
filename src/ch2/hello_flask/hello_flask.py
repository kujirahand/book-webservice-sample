# Flaskのインポート ---（※１）
from flask import Flask

# インスタンス作成 ---（※２）
app: Flask = Flask(__name__)


# ルーティング ---（※３）
@app.route("/")
def hello_world():
    return "<h1>Hello,World!</h1>"


# アプリケーションの実行 ---（※４）
if __name__ == "__main__":
    app.run()
