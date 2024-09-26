from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 


app: Flask = Flask(__name__)
login_user_name: str = "osamu"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contents = db.Column(db.String(100))


@app.route("/")
def index():
    search_word: str = request.args.get("search_word")

    if search_word is None:
        message_list: list[Message] = Message.query.all()
    else:
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
        contents: str = request.form.get("contents")
        user_name: str = request.form.get("user_name")
        new_message = Message(user_name=user_name, contents=contents)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for("index"))

# 更新機能のルーティング --- (※1)
@app.route("/update/<int:message_id>", methods=["GET", "POST"])
def update(message_id: int):
    # メッセージIDから更新対象のメッセージを取得 --- (※2)
    message: Message = Message.query.get(message_id)

    # 更新画面を表示 --- (※3)
    if request.method == "GET":
        return render_template("update.html", login_user_name=login_user_name, message=message)

    # 更新処理 --- (※4)
    elif request.method == "POST":
        message.contents = request.form.get("contents")
        db.session.commit()

        return redirect(url_for("index"))

# 削除機能のルーティング --- (※5)
@app.route("/delete/<int:message_id>")
def delete(message_id: int):
    # メッセージIDから削除対象のメッセージを取得 --- (※6)
    message: Message = Message.query.get(message_id)
    # メッセージを削除 --- (※7)
    db.session.delete(message)
    db.session.commit()

    return redirect(url_for("index"))


with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)
