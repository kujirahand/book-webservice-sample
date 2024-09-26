import matplotlib.pyplot as plt
import numpy as np
from japanmap import picture, get_data, pref_map

# 都道府県をどの色で塗るのかを指定 --- (※1)
pct: np.ndarray = picture({
    "北海道": "yellow",
    "東京都": "yellow",
    "静岡県": "yellow",
})
plt.axis("off") # 軸を非表示にする
plt.imshow(pct) # 描画 --- (※2)
plt.savefig("map.png") # 画像を保存 ---- (※3)
plt.show() # 画面を表示 --- (※4)