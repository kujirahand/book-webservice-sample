import os
from PIL import Image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np
# ラーメンの種類を定義 --- (※1)
labels = ["salt", "soy_sauce", "spicy", "miso", "chilled"]
base_dir = "./data"
# 画像のサイズを指定 --- (※2)
img_w, img_h = 32, 32
# 画像データを読み込んでリストに格納 --- (※3)
images = []
labels_num = []
for no, label in enumerate(labels):
    label_dir = os.path.join(base_dir, label)
    for filename in os.listdir(label_dir):
        if not filename.endswith(".jpg"):
            continue
        img_path = os.path.join(label_dir, filename)
        print("load_image=", img_path)
        # 回転画像を追加 --- (※4)
        img = Image.open(img_path)
        img = img.resize((img_w, img_h))
        for angle in range(0, 360, 45): # 45度ずつ回転
            img_rot = img.rotate(angle)
            img_rot = img_rot.resize((img_w, img_h))
            images.append(np.array(img_rot) / 255.0)
            labels_num.append(labels.index(label))
            # 反転画像を追加 --- (※5)
            img_flip = img_rot.transpose(Image.FLIP_LEFT_RIGHT)
            images.append(np.array(img_flip) / 255.0)
            labels_num.append(labels.index(label))
# 入出力のデータをNumPy配列に変換 --- (※6)
X = np.array(images)
y = to_categorical(np.array(labels_num))
print("X.shape=", X.shape)
# テスト用と訓練用にデータを分割 --- (※7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
# モデルの定義 --- (※8)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_w, img_h, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(labels), activation='softmax')
])
# モデルのコンパイル --- (※9)
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])
# モデルの訓練 --- (※10)
model.fit(
    X_train, y_train, epochs=27, batch_size=128, # 27 = 0.8
    validation_split=0.2)
# モデルの精度を確認 --- (※11)
score = model.evaluate(X_test, y_test)
print("正解率=", score[1])
# モデルの保存 --- (※12)
model.save('data/ramen.keras')