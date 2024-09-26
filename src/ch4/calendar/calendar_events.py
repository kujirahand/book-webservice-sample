import os, json, calendar, re
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for

# 予定イベントの保存先 --- (※1)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "calendar_events.json")
# イベントデータをファイルから読む --- (※2)
events = {}
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        events = json.load(f)

# Flaskのアプリを起動 --- (※3)
app: Flask = Flask(__name__)
# ルートへGETアクセスした時 --- (※4)
@app.route("/", methods=["GET"])
def index_get():
    # パラメータを取得し、デフォルト値を今月とする --- (※5)
    now = datetime.now()
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))
    # 月曜始まりのカレンダーを作成 --- (※6)
    cal = calendar.Calendar(calendar.MONDAY)
    weeks = cal.monthdayscalendar(year, month)
    # 翌月と前月のリンクを作成 --- (※7)
    next_year = year
    next_month = month + 1
    if next_month > 12:
        next_month, next_year = 1, year + 1
    prev_year = year
    prev_month = month - 1
    if prev_month < 1:
        prev_month, prev_year = 12, year - 1
    next_link = f"?year={next_year}&month={next_month}"
    prev_link = f"?year={prev_year}&month={prev_month}"
    # カレンダーをテンプレートエンジンで表示 --- (※8)
    return render_template("index.html",
        weeknames=list("月火水木金土日"),
        year=year, month=month,
        weeks=weeks, events=events,
        next_link=next_link, prev_link=prev_link)

# ルートへPOSTアクセスした時 --- (※9)
@app.route("/", methods=["POST"])
def index_post():
    # パラメータを得る --- (※10)
    date = request.form.get("date", "")
    event = request.form.get("event", "")
    # 入力を検証する --- (※11)
    i = re.match(r"(\d{4})-(\d{2})-\d{2}", date)
    if not i:
        return "日付形式が不正"
    year, month = int(i.group(1)), int(i.group(2))
    # イベントを年月日に追加 --- (※12)
    events[date] = event
    # ファイルに保存 --- (※13)
    with open(SAVE_FILE, "w") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    return redirect(url_for("index_get", year=year, month=month))

# Flaskを起動
if __name__ == "__main__":
    app.run(debug=True)
