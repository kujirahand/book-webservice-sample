from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pyotp
import os

app = Flask(__name__)
app.secret_key = 'secretkey'

# メールサーバーの設定 --- (※1)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_ID', None)
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD', None)
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('GMAIL_ID', None)

mail = Mail(app)

# データベースの設定 --- (※2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# ユーザー認証の設定 --- (※3)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ワンタイムパスワードをメールで送信する関数 --- (※4)
def send_otp(email):
    # シークレットキーとワンタイムパスワード生成器を生成 --- (※5)
    secret = pyotp.random_base32()    
    totp = pyotp.TOTP(secret, interval=60)
    
    # ワンタイムパスワードを生成し、メール送信 --- (※6)
    otp_code = totp.now()
    msg = Message('ワンタイムパスワード（OTP）', recipients=[email])
    msg.body = f"あなたのワンタイムパスワードは {otp_code} です。60秒間有効です"
    mail.send(msg)
    
    return secret

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # ユーザーが既に存在するかを確認
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return '既に登録されているメールアドレスです。'
        
        # 新しいユーザーをデータベースに追加
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # ユーザーの認証 --- (※7)
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # ワンタイムパスワードを送信
            secret = send_otp(email)
            
            # セッションにシークレットキーを保存
            session['otp_secret'] = secret
            session['email'] = email
            return redirect(url_for('verify'))

        return '認証情報が無効です。'

    return render_template('login.html')

# ログイン成功後のワンタイムパスワード検証 --- (※8)
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        otp_code = request.form['otp']
        
        # セッションからシークレットキーを取得
        secret = session.get('otp_secret')
        
        # 保存しておいたシークレットキーを使い、ワンタイムパスワードを検証
        totp = pyotp.TOTP(secret)
        if totp.verify(otp_code):
            # ユーザーをログイン状態にする
            email = session.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                login_user(user)
                return redirect(url_for('protected'))

        return '無効なOTPです。'

    return render_template('verify.html')

# 2段階認証が成功した後のページ --- (※9)
@app.route('/protected')
@login_required
def protected():
    return '2段階認証に成功しました。'

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
