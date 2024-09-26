from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os


app = Flask(__name__)
app.secret_key = 'secretkey'

# OAuth設定 --- (※1)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', None),
    client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', None),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    redirect_uri = 'http://127.0.0.1:5000/auth/callback',
    client_kwargs = {'scope': 'openid profile email'}
)

@app.route('/')
def index():
    # ログイン済みかどうかを確認 --- (※2)
    email = dict(session).get('email', None)
    if email is None:
        return redirect(url_for('login'))
    return f'ログインに成功しました! <br/>ログイン中のアカウント： python@sample.com'

# ログインする際はGoogle認証へリダイレクト --- (※3)
@app.route('/login')
def login():
    return google.authorize_redirect(url_for('auth_callback', _external=True))

# Google認証後のコールバック --- (※4)
@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
