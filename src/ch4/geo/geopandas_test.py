import geopandas as gpd
import matplotlib.pyplot as plt

# ダウンロードしたファイルのパス
GEOJSON_FILE = "N03-20240101.geojson"
# GeoJSONファイルを読み込む
map = gpd.read_file(GEOJSON_FILE, encoding="utf-8")
map.plot(edgecolor="gray", facecolor="none")
# 軸を非表示にする
plt.axis("off")
# 画面を表示
plt.show()
