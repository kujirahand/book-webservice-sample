import pickle
from keras.datasets import mnist
from sklearn import svm
from sklearn.metrics import accuracy_score

# MNISTデータを読み込み、一次元のデータに変形 --- (※1)
(train_data, train_label), (test_data, test_label) = mnist.load_data()
train_data = train_data.reshape(-1, 784)
test_data = test_data.reshape(-1, 784)
# ファイルに保存したモデルを読み込む --- (※2)
with open("mnist_model.pkl", "rb") as fp:
    clf = pickle.load(fp)
# テストデータで予測を行う --- (※3)
predicted = clf.predict(test_data)
# 精度を計測する --- (※4)
score = accuracy_score(test_label, predicted)
print("正解率=", score)