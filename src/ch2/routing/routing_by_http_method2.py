# requestのインポート ---（※１）
from flask import Flask, request

app: Flask = Flask(__name__)


# 「/」にアクセスがあった場合のルーティング
@app.route("/")
def index():
    return "<h1>これは掲示板のトップページです。</h1>"


# 「/write」にGETメソッドかPOSTメソッドでアクセスがあった場合のルーティング ---（※２）
@app.route("/write", methods=["GET", "POST"])
def write():
    # GETメソッドの場合 ---（※３）
    if request.method == "GET":
        return """
            <html><body>
            <h1>これは掲示板の書き込みページです。</h1>
            <h3>書き込み内容：</h3>
            <form action="/write" method="POST">
                <textarea name="msg" rows="5" cols="70"></textarea><br/><br/>
                <input type="submit" value="書き込み">
            </form>
            </body></html>
        """
    # POSTメソッドの場合 ---（※４）
    elif request.method == "POST":
        return "<h1>書き込みを受け付けました。</h1>"


# 「/edit/message_id」にアクセスがあった場合のルーティング
@app.route("/edit/<int:message_id>")
def edit(message_id: int):
    return f"<h1>これはID={message_id}の編集ページです。</h1>"


if __name__ == "__main__":
    app.run(debug=True)
