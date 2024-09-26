import calendar
from datetime import datetime
from flask import Flask, request
# Flaskのアプリを起動
app: Flask = Flask(__name__)
# ルートへアクセスした時
@app.route("/")
def index():
    year = int(request.args.get("year", datetime.now().year))
    month = int(request.args.get("month", datetime.now().month))
    html = calendar.HTMLCalendar().formatmonth(year, month) # --- (※1)
    style = "td {border:1px solid #aaa; width:3em; text-align:center;}"
    return f"<html><body><style>{style}</style>{html}</body></html>"
# Flaskを起動
app.run(debug=True, port=8888)