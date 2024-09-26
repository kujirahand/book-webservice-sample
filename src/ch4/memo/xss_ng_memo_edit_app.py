# ------------------------------------------------------
# メモアプリ - XSS脆弱性バージョン
# このプログラムは、XSS脆弱性を再現したものです。
# 下記(*8)に問題があります。書籍のTips部分をご確認ください。
# ------------------------------------------------------
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.utils import escape

# Flaskとデータベースの初期化 --- (※1)
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memo_edit.sqlite"
db:SQLAlchemy = SQLAlchemy(app)
# メモのデータベースモデルを定義  --- (※2)
class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body: str = db.Column(db.Text, nullable=False)
# データベースの初期化
with app.app_context():
    db.create_all()

# 各種HTMLを定義 --- (※3)
CSS = "https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
HTML_HEADER = f"""
  <!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{CSS}">
  </head><body class="p-3">
  <h1 class="has-background-info p-3 mb-3">Memo App</h1>
"""
HTML_EDITOR_FORM = """
  <div class="card p-3"><form method="POST">
    <label class="label">タイトル:</label>
    <input type="text" name="title" value="{title}" class="input">
    <label class="label">本文:</label>
    <textarea name="body" class="textarea">{body}</textarea>
    <input type="submit" value="保存" class="button is-primary">
  </form></div>
"""
HTML_FOOTER = "</body></html>"

# メモの編集画面を表示する --- (※4)
@app.route("/", methods=["GET", "POST"])
def index():
    # データベースからメモを取得 --- (※5)
    it = MemoItem.query.get(1)
    if it is None:
        # もし、まだメモがなければ新規メモを作成 --- (※6)
        it = MemoItem(id=1, title="無題", body="")
        db.session.add(it)
        db.session.commit()
    # POSTの場合はデータを保存 --- (※7)
    if request.method == "POST":
        it.title = request.form.get("title")
        it.body = request.form.get("body")
        if it.title == "":
            return "タイトルは空にできません"
        db.session.commit()
        return redirect(url_for("index"))
    # メモの編集画面を表示 --- (※8)
    title, body = it.title, it.body
    edit = HTML_EDITOR_FORM.format(title=title, body=body)
    html = HTML_HEADER + edit + HTML_FOOTER
    return html

if __name__ == "__main__":
    app.run(debug=True, port=8888)