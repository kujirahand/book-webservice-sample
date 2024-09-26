import os
import pickle
from sentence_transformers import SentenceTransformer, util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
INDEX_FILE = os.path.join(SCRIPT_DIR, "index.pkl")

# Embeddingに使用するモデルを指定 --- (※1)
model = SentenceTransformer("stsb-xlm-r-multilingual")

# インデックスを作成する関数 --- (※2)
def make_index():
    index = []
    # ファイル一覧を列挙 --- (※3)
    for file in os.listdir(INPUT_DIR):
        print("Indexing:", file)
        # ファイルを読み込む
        with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
            text = f.read()
        # 改行文章を分割 --- (※4)
        sentences = text.split("\n")
        # 文章をEmbeddingに変換して保存 --- (※5)
        for sentence in sentences:
            if sentence == "" or sentence.startswith("#"):
                continue
            embedding = model.encode(sentence, convert_to_tensor=False)
            index.append([file, sentence, embedding])
            print(file, sentence, len(embedding))
    return index

if __name__ == "__main__":
    # インデックスを作成してファイルに保存 --- (※6)
    index = make_index()
    with open(INDEX_FILE, "wb") as f:
        pickle.dump({"index": index}, f)
    print("完了です")