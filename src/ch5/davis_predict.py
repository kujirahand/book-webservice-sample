import pandas as pd
import keras

# ラベルの意味を定義
LABELS = ["低体重", "普通", "肥満"]

# 保存したモデルを作成
model = keras.models.load_model("davis_model.keras")

# 肥満判定を行う関数
def bmi_predict(height, weight):
    # 身長と体重を入力データとする
    data = pd.DataFrame([[height, weight]])
    # 予測する
    pred = model.predict(data, verbose=0)
    result = LABELS[pred[0].argmax()]
    print(f"身長{height}cm 体重{weight}kg => {result}")
    return result

if __name__ == "__main__":
    # 試してみる
    bmi_predict(170, 60)  # 普通
    bmi_predict(160, 40)  # 低体重
    bmi_predict(180, 100) # 肥満