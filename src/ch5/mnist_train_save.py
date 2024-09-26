import pickle
from keras.datasets import mnist
from sklearn import svm

# MNISTデータを読み込み、一次元のデータに変形 --- (※1)
(train_data, train_label), (test_data, test_label) = mnist.load_data()
# マシンスペックがよくない場合、以下のコメントを外してデータ数を減らしてください
# train_data = train_data[:3000]
# train_label = train_label[:3000]
train_data = train_data.reshape(-1, 784)
test_data = test_data.reshape(-1, 784)

# 機械学習で画像を学習する --- (※2)
clf = svm.SVC(verbose=True)
clf.fit(train_data, train_label)
# ファイルに保存する --- (※3)
with open("mnist_model.pkl", "wb") as fp:
    pickle.dump(clf, fp)
print("saved.")