import pandas
from keras.models import Sequential
from keras.layers import Dense
import keras.utils as np_utils

# CSVファイルを読み込む
df = pandas.read_csv("Davis_bmi.csv")
# ラベルを数値に変換する
label = df["label"].map({"低体重": 0, "普通": 1, "肥満": 2})
# ラベルをone-hotエンコーディングする
label = np_utils.to_categorical(label)
# 身長と体重を入力データとする
data = df[["height", "weight"]]
# 学習用とデータとテストデータに分割する
threshold = len(data) * 2 // 3 # 2/3を閾値にする
train_data, test_data = data[:threshold], data[threshold:]
train_label, test_label = label[:threshold], label[threshold:]
print(train_data)
print(train_label)
# モデルを作成する
model = Sequential()
model.add(Dense(20, activation="relu", input_dim=2))
model.add(Dense(3, activation="softmax"))
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
# 学習する
model.fit(train_data, train_label, epochs=400, batch_size=50)
# テストデータで評価する
loss, accuracy = model.evaluate(test_data, test_label)
print(f"損失: {loss}, 精度: {accuracy}")
# モデルを保存する
model.save("davis_model.keras")
