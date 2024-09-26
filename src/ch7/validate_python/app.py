from flask import Flask, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # フラッシュメッセージ用の秘密鍵

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # フォームデータを取得
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # バリデーションフラグ
        is_valid = True

        # ユーザー名のバリデーション
        if len(username) < 1:
            flash('ユーザー名を入力してください。')
            is_valid = False

        # メールアドレスのバリデーション
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            flash('有効なメールアドレスを入力してください。')
            is_valid = False

        # パスワードのバリデーション
        if len(password) < 8:
            flash('パスワードは8文字以上で入力してください。')
            is_valid = False

        # バリデーションが成功した場合の処理
        if is_valid:
            flash('登録が成功しました！')
            return redirect(url_for('register'))

    # フォームのHTMLテンプレート
    form_html = '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ユーザー登録</title>
    </head>
    <body>
        <h2>ユーザー登録フォーム</h2>
        <form method="POST">
            <label for="username">ユーザー名 (必須):</label>
            <input type="text" id="username" name="username"><br><br>

            <label for="email">メールアドレス (必須):</label>
            <input type="email" id="email" name="email"><br><br>

            <label for="password">パスワード (必須, 最小8文字):</label>
            <input type="password" id="password" name="password"><br><br>

            <input type="submit" value="登録">
        </form>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul>
                {% for message in messages %}
                    <li style="color:red;">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    </body>
    </html>
    '''
    return render_template_string(form_html)

if __name__ == '__main__':
    app.run(debug=True)
