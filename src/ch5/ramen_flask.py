import os
from flask import Flask, request, redirect, url_for, send_from_directory
import numpy as np
from keras import models
from PIL import Image
# 設定 --- (※1)
UPLOAD_FOLDER = './data/uploads'
RAMEN_MODEL_FILE = './data/ramen.keras'
LABELS = ["塩ラーメン", "醤油ラーメン", "担々麺", "味噌ラーメン", "冷やし中華"]
CSS_URL = "https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
HTML_HEADER = f"""
<!DOCTYPE html><html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="{CSS_URL}"><body>
<section class="hero has-background-info"><div class="hero-body">
    <h1 class="title">ラーメン判定AI</h1></div></section>
"""
# Flaskのインスタンスを作成 --- (※2)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# モデルを読み込む --- (※3)
model = models.load_model(RAMEN_MODEL_FILE)
# ルートへアクセスがあった時の処理 --- (※4)
@app.route('/')
def root():
    return f"""{HTML_HEADER}
    <div class="box file">
        <form method="post" action="/predict"
            enctype="multipart/form-data">
            <input type="file" name="file" class="file-label" /><br>
            <input type="submit" value="画像判定"
                class="button is-primary" />
        </form></div>
    </body></html>
    """
# ファイルをアップロードした時 --- (※5)
@app.route('/predict', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if not (file and file.filename.endswith(('.jpg', '.jpeg'))):
        return f"""{HTML_HEADER}
        <h1>アップロードできるのは画像のみです</h1></body></html>"""
    # 画像をディレクトリに保存 --- (※6)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    # 画像を読み込む --- (※7)
    try:
        img = Image.open(file_path)
        img = img.resize((32, 32))
        X = np.array([np.array(img) / 255.0])
    except Exception as e:
        return f"""{HTML_HEADER}
        <h1>画像を読み込めませんでした</h1></body></html>"""
    # 予測を行う --- (※8)
    predictions = model.predict([X])
    # 最も高い確率を持つクラスのインデックスを取得 --- (※9)
    index = np.argmax(predictions, axis=-1)[0]
    print("index=", index, "predictions=", predictions)
    # 結果を表示 --- (※10)
    return f"""{HTML_HEADER}
    <div class="card" style="font-size:2em; padding:1em;">
        判定結果: {LABELS[index]} (精度:{predictions[0][index]:.2f})<br>
        <img src="upload/{filename}" width="400"><br>
        <a href="/" class="button">次の画像</a>
    </div></body></html>
    """
# アップロードされたファイルを返す --- (※11)
@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=8888)