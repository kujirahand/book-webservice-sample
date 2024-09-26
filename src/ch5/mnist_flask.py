import os
import io
import pickle
import base64
from PIL import Image
from flask import Flask, request, jsonify, render_template
from keras.datasets import mnist
from sklearn import svm

# スクリプトのディレクトリを取得
SCRIPT_DIR = os.path.dirname(__file__)
# MNISTのデータセットを読み込む --- (※1)
with open(os.path.join(SCRIPT_DIR, "mnist_model.pkl"), "rb") as fp:
    clf:svm.SVC = pickle.load(fp)
# Flaskのインスタンスを作成
app = Flask(__name__)

# ルートへアクセスがあった時の処理 --- (※2)
@app.route("/")
def root():
    # HTMLファイルを読む
    with open(os.path.join(SCRIPT_DIR, "mnist_draw.html"), "r") as fp:
        return fp.read()

# 手描き数字の画像データから推論を行う --- (※3)
@app.route("/predict", methods=["POST"])
def predict():
    # リクエストデータ(Base64のJSON)を取得 --- (※4)
    canvas_data: str = request.json.get("data")
    # Base64形式のデータをImageに変換
    bin: str = base64.b64decode(canvas_data.split(",")[1])
    image: Image = Image.open(io.BytesIO(bin))
    # 28x28にリサイズしてグレイスケールに変換 --- (※5)
    image = image.resize((28, 28))
    image_bg: Image = Image.new("RGB", image.size, "white")
    image_bg.paste(image, (0, 0), mask=image.split()[3])
    gray_image = image_bg.convert("L")
    # ピクセルデータに変換して一次元のデータに変換 --- (※6)
    pixels: list[int] = list(gray_image.getdata())
    pixels = [255 - x for x in pixels] # 白黒反転
    print(pixels) # 確認のためデータを表示
    # 予測する --- (※7)
    predict: str = str(clf.predict([pixels])[0])
    return jsonify(result=predict) # 結果をJSONで返す

if __name__ == "__main__":
    app.run(debug=True, port=8888)