from flask import Flask, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# CSRFトークンの生成に使用する秘密鍵を設定
app.config['SECRET_KEY'] = 'secretkey'

# CSRF保護を有効化
csrf = CSRFProtect(app)

# WTFormsを使用してフォームを定義
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        # トークンを検証し、フォームが有効な場合の処理
        return redirect(url_for('success'))
    
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>CSRF Protection Example</title>
    </head>
    <body>
        <h1>Submit Form</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.name.label }} {{ form.name() }}<br>
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)

@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
