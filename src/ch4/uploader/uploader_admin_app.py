from flask import Flask, request, render_template, redirect, url_for
from models import DB_URI, db, User, add_user

# Flaskとデータベースの初期化 --- (※1)
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db.init_app(app)
with app.app_context():
    db.create_all()

# 管理者画面の表示 --- (※2)
@app.route("/", methods=["GET", "POST"])
def index():
    msg = "新規ユーザーを追加できます。"
    if request.method == "POST":
        # パラメータを取得
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        password2 = request.form.get("password2", "").strip()
        # パラメータの検証
        if password != password2:
            return "パスワードが一致しません"
        if email == "" or password == "":
            return "メールアドレスとパスワードを入力してください"
        User.query.filter_by(email=email).delete() # 既存ユーザーを削除
        # ユーザーを追加
        add_user(email, password)
        msg = f"ユーザー<{email}>を追加しました"
    users = User.query.all()
    return render_template("admin.html",
        app_title="ファイル共有 - 管理者ツール", message=msg, users=users)

# ユーザーの削除 --- (※3)
@app.route("/delete_user/<int:id>")
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=9999)