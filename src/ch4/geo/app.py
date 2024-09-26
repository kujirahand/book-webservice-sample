import os, time
from flask import Flask, redirect, url_for, render_template, request
import plot_temp

# HTMLの保存先を指定する --- (※1)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_HTML = os.path.join(SCRIPT_DIR, "static", "map.html")

app: Flask = Flask(__name__)

# ルートへのアクセスを処理する --- (※2)
@app.route("/")
def index():
    # 最高気温の地図を作成（ただし1時間に1回のみ更新) --- (※3)
    if os.path.exists(MAP_HTML):
        # 現在時刻と保存されたファイルを調べてキャッシュを更新
        st = os.stat(MAP_HTML)
        if st.st_mtime + 3600 < time.time():
            plot_temp.save_weather_map(MAP_HTML)
    else:
        plot_temp.save_weather_map(MAP_HTML)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)