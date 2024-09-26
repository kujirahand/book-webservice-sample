import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# CSVファイルを読み込む --- (※1)
df = pd.read_csv("davis_bmi.csv")
# 読み込んだデータの一部を表示
print("--- 元のCSVデータ ---")
print(df[0:3])
# 読み込んだデータを学習用とテスト用に分割 --- (※2)
values = df[["height", "weight"]].values
label = df["label"].values
train_data, test_data, train_label, test_label = train_test_split(
    values, label, test_size=0.1)
print("--- 学習用データ ---")
print("label=", train_label[0:3], "\ndata=", train_data[0:3])
print("--- テスト用データ ---")
print("label=", test_label[0:3], "\ndata=", test_data[0:3])

# 学習用データを用いてデータを学習 --- (※3)
clf = RandomForestClassifier()
clf.fit(train_data, train_label)
print("--- 学習しました ---")
# テストデータを使って予測 --- (※4)
predict = clf.predict(test_data)
# 予測結果の一部を表示
print("正解データ=", test_label[0:3])
print("予測データ=", predict[0:3])

# 正解率を計算する --- (※5)
ac_score = accuracy_score(test_label, predict)
print("正解率=", ac_score)