from sentence_transformers import SentenceTransformer, util

# Embeddingに使用するモデルを指定 --- (※1)
model = SentenceTransformer("stsb-xlm-r-multilingual")
# 文章リストと検索ワードを指定 --- (※2)
sentences = [
    "私は犬の散歩に行きました。",
    "今日は良い天気ですね。",
    "プログラミングを勉強するのが好きです。",
    "美味しいコーヒーを飲みたいです。",
    "彼は勉強が大好きです。"
]
query = "Pythonの学習は楽しい"

# 文章と検索ワードのEmbeddingを取得 --- (※3)
sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
query_embedding = model.encode(query, convert_to_tensor=True)
# 類似度を計算して並び替え --- (※4)
similarities = util.cos_sim(query_embedding, sentence_embeddings)[0]
sorted_indices = similarities.argsort(descending=True)

# 結果を表示 --- (※5)
print("検索ワード:", query)
print("| ------ | ---------------------------------")
print("| 類似度 | 検索結果 (近い順)")
print("| ------ | ---------------------------------")
for idx in sorted_indices:
    print(f"| {similarities[idx]:.4f} | {sentences[idx]}")