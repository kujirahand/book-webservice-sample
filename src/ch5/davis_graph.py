import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_fontja  # noqa: F401 文字化けを防ぐ

# CSVファイルを読み込む --- (※1)
df = pd.read_csv("davis_bmi.csv")
# ラベルごとにデータを分割する --- (※2)
normal = df[df["label"] == "普通"]
underwt = df[df["label"] == "低体重"]
obese = df[df["label"] == "肥満"]
# グラフを描画する --- (※3)
plt.scatter(underwt["height"], underwt["weight"],
    label="低体重", color="green", marker="v")
plt.scatter(normal["height"], normal["weight"],
    label="普通", color="blue", marker="o")
plt.scatter(obese["height"], obese["weight"],
    label="肥満", color="red", marker="x")
# 軸ラベルとタイトルを設定する --- (※4)
plt.xlabel("身長")
plt.ylabel("体重")
plt.title("身長と体重の関係")
plt.legend()  # 凡例を表示する
# グラフを表示する --- (※5)
plt.show()