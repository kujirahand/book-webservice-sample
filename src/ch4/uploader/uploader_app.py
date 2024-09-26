import io
from flask import Flask, request, redirect, url_for, session, render_template, send_file
from models import DB_URI, db, User, FileItem, try_login
import models
from sqlalchemy import or_

# 定数の宣言やFlaskとデータベースの初期化 --- (※1)
APP_TITLE = "ファイル共有ツール"
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.secret_key = "VLxa_R#0X0q-yuMFKEj" # ランダムなシークレットを指定
db.init_app(app)

# ルートへのアクセス処理 --- (※2)
@app.route("/")
def index():
    if "login" not in session: # ログインしてなければログインページへ
        return redirect(url_for("login"))
    user_id, email = session["login"]
    # 取得可能ファイルを取得
    files = FileItem.query.filter(
        or_(FileItem.owner_user_id==user_id, # 自分がオーナー
            FileItem.allow_user_id==user_id, # 共有先に自分が指定
            FileItem.allow_user_id==0) # ログインしている全員を指定
        ).order_by(FileItem.id.desc()).all()
    users = {u.id: u.email for u in User.query.all()}
    users[0] = "全員"
    return render_template("index.html", app_title=APP_TITLE,
        email=email, user_id=user_id, users=users, files=files)

# ログイン処理 --- (※3)
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = "ログインしてください。"
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = try_login(email, password)
        if user:
            # ログインしていることを記録
            session["login"] = [user.id, user.email]
            return redirect(url_for("index"))
        msg = "ログインに失敗しました。"
    return render_template("login.html", app_title=APP_TITLE, message=msg)

@app.route("/logout")
def logout():
    session.pop("login", None)
    return "ログアウトしました"

# アップロード処理 --- (※4)
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "login" not in session: # ログインが必要
        return redirect(url_for("login"))
    user_id, _email = session["login"]
    if request.method == "POST": # ファイルをアップロードした時
        # コメントや共有先を確認 --- (※5)
        comment = request.form.get("comment")
        share_user_id = int(request.form.get("user_id", 0))
        if share_user_id > 0: # 特定のユーザーを指定した場合
            share_user = User.query.filter_by(id=share_user_id).first()
            if share_user is None:
                return "指定されたユーザーは存在しません"
        f = request.files["file"]
        if f:
            # データベースに情報を保存 --- (※6)
            m: FileItem = FileItem(owner_user_id=user_id,
                allow_user_id=share_user_id, comment=comment,
                filename=f.filename, data=f.read())
            db.session.add(m)
            db.session.commit()
            # メールを送信して通知
            if share_user_id > 0:
                models.send_mail_share(app, share_user.email,
                    f.filename, request.host_url)
            return redirect(url_for("index"))
    return render_template("upload.html", app_title=APP_TITLE,
                           users=User.query.all())

# ファイルのダウンロード処理 --- (※7)
@app.route("/download/<int:id>")
def download(id):
    if "login" not in session:
        return redirect(url_for("login"))
    user_id, email = session["login"]
    # ファイルをDBから取得
    f = models.get_file(id, user_id)
    if f is None:
        return "ファイルが見つかりません"
    return send_file(io.BytesIO(f.data),
            mimetype="application/octet-stream", as_attachment=True,
            download_name=f.filename)

# ファイルの削除処理 --- (※8)
@app.route("/delete/<int:id>")
def delete(id):
    if "login" not in session:
        return redirect(url_for("login"))
    user_id, email = session["login"]
    # ファイルをDBから取得
    f = models.get_file(id, user_id)
    if f is None:
        return "ファイルが見つかりません"
    if user_id == f.owner_user_id: # オーナーであれば削除可能
        db.session.delete(f)
        db.session.commit()
        return redirect(url_for("index"))
    return "削除する権限がありません。"

if __name__ == "__main__":
    app.run(debug=True, port=8888)