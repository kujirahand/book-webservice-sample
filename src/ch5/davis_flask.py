from flask import Flask
from flask import request
import davis_train_predict as davis_bmi

# Flaskのインスタンスを作成
app = Flask(__name__)

# ルートへアクセスがあった時の処理 --- (※1)
@app.route('/')
def root():
    return """
    <html><body>
    <h1>肥満度判定</h1>
    <form action="/predict" method="get">
        <label for0="weight">体重(kg):</label><br>
        <input type="text" id="weight" name="weight" placeholder="体重(kg)"><br>
        <label for="height">身長(cm):</label><br>
        <input type="text" id="height" name="height" placeholder="身長(cm)"><br>
        <input type="submit" value="判定">
    </form>
    </body></html>
    """

@app.route('/predict')
def predict():
    # 体重と身長のパラメータを取得 --- (※2)
    weight = float(request.args.get("weight"))
    height = float(request.args.get("height"))
    # 機械学習で判定 --- (※3)
    predict = davis_bmi.clf.predict([[height, weight]])[0]
    return """
    <html><body>
    <h1>判定結果</h1>
    <p>体重={}kg, 身長={}cmの場合、</p>
    <p>判定結果は「{}」です。</p>
    </body></html>
    """.format(weight, height, predict)

if __name__ == '__main__':
    app.run(debug=True, port=8888)