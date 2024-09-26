import os
from flask import Flask, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import escape

# マスターパスワードを環境変数から取得 --- (※1)
MEMO_PASSWORD = os.environ.get("MEMO_PASSWORD", "test")
# Flaskとデータベースの初期化 --- (※2)
app: Flask = Flask(__name__)
app.secret_key = "y6Jq9MXPZ_pVZO9l"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memo.sqlite"
db:SQLAlchemy = SQLAlchemy(app)
# メモのデータベースモデルを定義  --- (※3)
class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body: str = db.Column(db.Text, nullable=False)
# データベースの初期化
with app.app_context():
    db.create_all()

# HTMLのヘッダとフッタを定義 --- (※4)
APP_TITLE = "Memo App"
CSS = "https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
HTML_HEADER = f"""
  <!DOCTYPE html><html><head><meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="{CSS}">
  <title>{APP_TITLE}</title></head><body class="p-3">
  <div class="p-5 has-background-info">
    <h1 class="is-size-3">{APP_TITLE}</h1></div>
"""
HTML_FOOTER = "</body></html>"

# メモの一覧を表示する
@app.route("/")
def index():
    if "login" not in session:
        return redirect(url_for("login"))
    # メモの一覧を取得
    msg = "編集したいメモを選んでください:"
    html = f"<div class='card p-2'>{msg}<ul class='p-3'>"
    html += "<li class='tag m-1'><a href='/memo/0'>📝 新規作成</a></li>"
    for it in MemoItem.query.order_by(MemoItem.title).all():
        title = "□ " + escape(it.title)
        href = f"/memo/{it.id}"
        html += f"<li class='tag m-1'><a href='{href}'>{title}</a></li>"
    html += "</ul></div>"
    return HTML_HEADER + html + HTML_FOOTER

# ログイン処理を行う
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == MEMO_PASSWORD:
            session["login"] = True
            return redirect(url_for("index"))
    return f"""{HTML_HEADER}
    <div class="card p-3"><form method="post">
        <label class="label">ログインが必要です</label>
        <input type="password" name="password">
        <input type="submit" value="ログイン">
    </form></div>{HTML_FOOTER}"""

# メモの編集画面を出す
@app.route("/memo/<int:id>", methods=["GET", "POST"])
def memo(id: int):
    if "login" not in session: # ログインチェック
        return redirect(url_for("login"))
    # メモのIDを取得
    if id > 0:
        it = MemoItem.query.get(id)
        if it is None:
            return "メモが見つかりません", 404
    else:
        # 新規メモ
        it = MemoItem(title="__新規", body="")
        db.session.add(it)
        db.session.commit()
    # POSTの場合はデータを保存
    if request.method == "POST":
        it.title = request.form["title"]
        it.body = request.form["body"]
        db.session.commit()
        return redirect(url_for("index"))
    # メモの編集画面を表示
    title = escape(it.title)
    body = escape(it.body)
    html = f"""{HTML_HEADER}<div class="card p-3">
    <form method="post">
        <label class="label">タイトル:</label>
        <input type="text" name="title" value="{title}" class="input">
        <label class="label">本文:</label>
        <textarea name="body" class="textarea">{body}</textarea>
        <input type="submit" value="保存" class="button is-primary">
    </form></div>{HTML_FOOTER}"""
    return html

if __name__ == "__main__":
    app.run(debug=True, port=8888)