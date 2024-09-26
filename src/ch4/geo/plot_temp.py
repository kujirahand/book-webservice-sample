import os
import requests
import folium

# 気象情報APIのURL --- (※1)
WEATHER_API = "https://api.aoikujira.com/tenki/week.php?fmt=json"

# 都市ごとの緯度経度のCSVから読んで辞書型に変換 --- (※2)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_INFO_FILE = os.path.join(SCRIPT_DIR, "city_info.csv")
with open(CITY_INFO_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip().split(",") for line in f.readlines()]
    lines = lines[1:] # ヘッダ行を除外
city_info = {}
for line in lines:
    city = line[1].replace("市", "")
    city_info[city] = (float(line[2]), float(line[3]))

# 気象情報をAPIから取得 --- (※3)
def get_weather_data(key = "maxtemp"):
    #　APIから気象情報を取得 --- (※4)
    obj = requests.get(WEATHER_API).json()
    # 各都市の現在の情報を取得 --- (※5)
    info = {}
    for city, clist in obj.items():
        if city == "mkdate": # 日付情報は除外
            continue
        # 週間予報の先頭の情報を取得
        v = clist[0][key] if clist[0][key] != "-" else clist[1][key]
        info[city] = int(v)
        print(city, v, city_info[city])
    return info

# 緯度経度を指定して地図を表示 --- (※6)
def save_weather_map(htmlfile: str):
    # 新宿を中心とした地図を作成 --- (※7)
    map = folium.Map(location=[35.690921, 139.700258], zoom_start=6)
    winfo = get_weather_data()
    for city, v in winfo.items():
        # 都市名と最高気温をHTMLで指定 --- (※8)
        html = """<div style='font-size:7pt; width:25pt;
            text-align:right; padding:2pt; color:black;
            background-color:rgba(255,255,255,0.7);'>{}<br>{}℃</div>
            """.format(city, v)
        # マーカーを作成して地図に追加 --- (※9)
        folium.Marker(
            location=city_info[city],
            popup=f"{city} {v}℃",
            icon=folium.DivIcon(html=html)
        ).add_to(map)
    # HTMLファイルに保存 --- (※10)
    map.save(htmlfile)

if __name__ == "__main__":
    save_weather_map("map.html")