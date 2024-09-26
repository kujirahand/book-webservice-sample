from keras.datasets import mnist
from sklearn import svm
from sklearn.metrics import accuracy_score

# KerasのサンプルデータセットからMNISTを読み込む --- (※1)
(train_data, train_label), (test_data, test_label) = mnist.load_data()
# SVMで学習するために、画像データをに一次元に変形 --- (※2)
train_data = train_data.reshape(-1, 784)
test_data = test_data.reshape(-1, 784)
# 全データで試すと時間がかかるので先頭の3000件だけ使う --- (*2a)
train_data = train_data[:3000]
train_label = train_label[:3000]

# 機械学習で画像を学習する --- (※3)
clf = svm.SVC()
clf.fit(train_data, train_label)
# テストデータで予測を行う --- (※4)
predicted = clf.predict(test_data)
# 精度を計測する --- (※5)
score = accuracy_score(test_label, predicted)
print("正解率=", score)