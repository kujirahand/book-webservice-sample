import pandas as pd

# 元データ「Davis.csv」を読む --- (※1)
df = pd.read_csv("Davis.csv", index_col=False)
# CSVから体重(weight)と身長(height)だけを取り出す --- (※2)
df = df[["weight", "height"]]
# 体重が140kgを超えるあり得ないデータを除外する --- (※3)
df = df[df["weight"] < 140]
# BMIを計算する --- (※4)
df["bmi"] = df["weight"] / (df["height"] / 100) ** 2
# BMIに基づいてラベルを付ける --- (※5)
df["label"] = pd.cut(
    df["bmi"],  # 計算済みのBMIの値
    bins=[0, 18.5, 25, float("inf")],  # 区分を指定
    labels=["低体重", "普通", "肥満"],  # 区分ごとのラベルを指定
)
# 加工済みファイルを保存 --- (※6)
df.to_csv("davis_bmi.csv", index=False)