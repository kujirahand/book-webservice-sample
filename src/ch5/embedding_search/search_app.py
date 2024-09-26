import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer, util
from flask import Flask, request, render_template, redirect, url_for
from markdown import markdown

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
INDEX_FILE = os.path.join(SCRIPT_DIR, "index.pkl")

# Embeddingに使用するモデルを指定 --- (※1)
model = SentenceTransformer("stsb-xlm-r-multilingual")
# Embeddingのインデックスを読み込む --- (※2)
with open(INDEX_FILE, "rb") as fp:
    database = pickle.load(fp)
# Flaskのアプリケーションを作成 --- (※3)
app: Flask = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # 検索テキストボックスを表示 --- (※4)
        return render_template("index.html")
    # 検索実行
    query = request.form.get("query")
    if query is None or len(query) <= 2:
        return redirect(url_for("index"))
    # 検索クエリをEmbeddingに変換 --- (※5)
    query_embedding = model.encode(query, convert_to_tensor=False)
    print(query_embedding)
    # 類似度を計算 --- (※6)
    index = database["index"]
    embeddings = np.array([x[2] for x in index])
    similarities = util.cos_sim(query_embedding, embeddings)[0]
    # 類似度が高い順にソート --- (※7)
    sorted_indices = similarities.argsort(descending=True)
    # 結果を表示 --- (※8)
    results = []
    print(sorted_indices)
    for i in sorted_indices[:10]:
        file, sentence, _ = index[i]
        rate = similarities[i].item()
        results.append({
            "file": file,
            "sentence": sentence,
            "rate": f"{rate:.3f}"
        })
    return render_template("index.html", query=query, results=results)

@app.route("/text/<file>")
def text(file):
    # ファイルの内容を表示 --- (※9)
    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        text = f.read()
    md = markdown(text)
    return render_template("text.html", file=file, markdown=md)

if __name__ == "__main__":
    app.run(debug=True)