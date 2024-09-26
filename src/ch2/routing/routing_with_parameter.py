from flask import Flask

app: Flask = Flask(__name__)


# 「/」にアクセスがあった場合のルーティング
@app.route("/")
def index():
    return "<h1>これは掲示板のトップページです。</h1>"


# 「/write」にアクセスがあった場合のルーティング
@app.route("/write")
def write():
    return "<h1>これは掲示板の書き込みページです。</h1>"


# 「/edit/message_id」にアクセスがあった場合のルーティング ---（※１）
@app.route("/edit/<message_id>")
def edit(message_id):
    return f"<h1>これはID={message_id}の編集ページです。</h1>"


if __name__ == "__main__":
    app.run(debug=True)
