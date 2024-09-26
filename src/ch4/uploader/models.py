import os, hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask

# データベースのURIを指定
DB_URI = "sqlite:///uploader.sqlite"
# データベースモデルを定義
db = SQLAlchemy()
# アップロードしたファイルの情報 --- (※1)
class FileItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    owner_user_id: int = db.Column(db.Integer) # 誰がアップしたか
    allow_user_id: int = db.Column(db.Integer) # 誰に共有するか
    comment: str = db.Column(db.Text) # コメント
    filename: str = db.Column(db.Text) # ファイル名
    data: bytes = db.Column(db.LargeBinary) # バイナリデータ

# ユーザー情報 --- (※2)
class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.Text, nullable=False, unique=True)
    hash: str = db.Column(db.Text, nullable=False) # パスワードのハッシュ
    salt: str = db.Column(db.Text, nullable=False) # ハッシュを作成するため

# パスワードのハッシュ化 --- (※3)
def get_hash(password: str, salt: str) -> str:
    s = password + "::" + salt
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# ユーザーを追加する処理 --- (※4)
def add_user(email: str, password: str):
    salt = os.urandom(24).hex()
    m = User(email=email, hash=get_hash(password, salt), salt=salt)
    db.session.add(m)
    db.session.commit()

# ログイン判定してユーザー情報取得 --- (※5)
def try_login(email: str, password: str) -> User|None:
    usr: User = User.query.filter_by(email=email).first()
    if usr:
        salt = usr.salt
        if get_hash(password, salt) == usr.hash:
            return usr
    return None

# ファイルを取得する処理 --- (※6)
def get_file(id: int, user_id: int) -> FileItem|None:
    f = FileItem.query.filter_by(id=id).first()
    if f is None:
        return None
    # 全員に共有しているか?
    if f.allow_user_id == 0:
        return f
    # 特定のユーザーに共有か自分がアップロードしたファイルか?
    if f.owner_user_id != user_id and f.allow_user_id != user_id:
        return None
    return f

# Gmailを用いてメールを送信する --- (※7)
def send_mail(app:Flask, to: str, subject: str, body: str):
    print("[mail]", to, subject, body)
    # 環境変数から設定を取得
    gmail_id = os.environ.get("GMAIL_ID", None)
    gmail_pw = os.environ.get("GMAIL_APP_PASSWORD", None)
    if gmail_id is None or gmail_pw is None:
        print("GMAIL_ID または GMAIL_APP_PASSWORD が設定されていません")
        return
    # Gmailからメールを送信
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_USERNAME"] = gmail_id
    app.config["MAIL_PASSWORD"] = gmail_pw
    app.config['MAIL_DEFAULT_SENDER'] = gmail_id
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config['MAIL_USE_SSL'] = False
    mail = Mail(app)
    mail.send_message(subject=subject, recipients=[to], body=body)

# ファイル共有通知メールを送信 --- (※8)
def send_mail_share(app:Flask, to: str, file: str, url: str):
    subject = "ファイルが共有されました"
    body = f"{to}さんからファイル「{file}」が共有されました。" + \
        f"[URL] {url}"
    send_mail(app, to, subject, body)