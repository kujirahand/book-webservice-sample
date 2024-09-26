from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
# SQLAlchemyをインポート --- (※1)
from flask_sqlalchemy import SQLAlchemy 


app: Flask = Flask(__name__)
login_user_name: str = "osamu"


# Databbaseの設定 --- (※2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# メッセージのデータベースモデル --- (※3)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contents = db.Column(db.String(100))


@app.route("/")
def index():
    search_word: str = request.args.get("search_word")

    if search_word is None:
        # search_wordパラメータが存在しない場合は、全てのメッセージを「top.html」に表示 --- (※4)
        message_list: list[Message] = Message.query.all()
    else:
        # search_wordパラメータが存在する場合は、検索ワードでフィルタしたメッセージを「top.html」に表示
        message_list: list[Message] = Message.query.filter(Message.contents.like(f"%{search_word}%")).all()

    return render_template(
        "top.html",
        login_user_name=login_user_name,
        message_list=message_list,
        search_word=search_word,
    )


@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html", login_user_name=login_user_name)

    elif request.method == "POST":
        # POSTメソッドのフォームの値を利用して、新しいメッセージを作成 --- (※5)
        contents: str = request.form.get("contents")
        user_name: str = request.form.get("user_name")
        new_message = Message(user_name=user_name, contents=contents)
        db.session.add(new_message)
        # 変更をデータベースにコミット
        db.session.commit()

        # 「/」にリダイレクト --- (※6)
        return redirect(url_for("index"))

# データベースの初期化 --- (※7)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
