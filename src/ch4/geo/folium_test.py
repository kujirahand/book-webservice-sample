import folium

# 緯度経度を指定して地図を表示
m = folium.Map(location=[35.690921, 139.700258], zoom_start=5)
# HTMLファイルに保存
m.save("map.html")
