import json
from flask import Flask, render_template, request, jsonify
from make_graph import make_graph

# Flaskインスタンスを生成 --- (※1)
app: Flask = Flask(__name__)

# 「/」にアクセスがあった場合のルーティング --- (※2)
@app.route("/")
def index():
    return render_template("index.html")

# 作図を実行する関数(JavaScriptから呼び出される) --- (※3)
@app.route("/api/sakuzu", methods=["POST"])
def api_sakuzu():
    # パラメータを取得 --- (※4)
    body: str = request.data.decode("utf-8")
    try:
        data = json.loads(body)
        input: str = data["input"]
        print("input:", input)
    except Exception as e:
        print(e)
        return "error"
    # 作図をして結果を返す --- (※5)
    code, result = make_graph(input)
    return jsonify({"code": code, "result": result})

if __name__ == "__main__":
    app.run(debug=True)