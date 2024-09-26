import matplotlib.pyplot as plt
from keras.datasets import mnist

# KerasのサンプルデータセットからMNISTを読み込む --- (※1)
(train_data, train_label), (test_data, test_label) = mnist.load_data()

# 20個の画像データを表示 --- (※2)
plt.figure(figsize=(10, 10))
for i in range(20):
    plt.subplot(4, 5, i + 1) # 表示位置の指定
    plt.imshow(train_data[i], cmap='gray') # 画像データの描画
    plt.axis("off") # 軸を非表示にする
plt.show() # 画像の表示

# 画像データに関する情報を表示 --- (※3)
print("学習データ", train_data.shape)
print("学習ラベル", train_label.shape)
print("テストデータ", test_data.shape)
print("テストラベル", test_label.shape)
print("画像データの例:", type(train_data[0]))
print(train_data[0])