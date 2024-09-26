from flask import Flask, redirect, url_for, render_template, request
import reversi_utils as utils
import token_checker as tc

# 盤面の初期化 --- (※1)
board = utils.generate_board()
who = utils.BLACK
app: Flask = Flask(__name__)
tc.reset_tokens()

# 現在の盤面の状態を表示 --- (※2)
@app.route("/")
def index():
    me = int(request.args.get("who", who)) # 誰の手番か
    token = request.args.get("token", "") # トークン
    # 石の数を数えて、表示するメッセージを決定
    black, white = utils.count_stone_both(board)
    msg = utils.STATUS[who] + "の手番" # メッセージを表示
    if black + white == 64:
        msg = "黒の勝ち" if black > white else "白の勝ち"
    elif black + white >= 6: # 初期状態でなければ不正チェック
        if not tc.check_token(me, token):
            return "不正なアクセスです"
    can_place = (who == me)
    return render_template( # テンプレートに当てはめて表示 --- (※3)
        "index.html",
        board=utils.add_flip_mark(board, who) if can_place else board,
        count=(black, white), token=tc.get_token(me),
        msg=msg, me=me, can_place=can_place)

# 座標(x, y)に石を配置する関数 --- (※4)
@app.route("/place/<int:y>/<int:x>")
def place(y: int, x: int):
    global who
    me = int(request.args.get("who", who))
    token = request.args.get("token", "")
    c = sum(utils.count_stone_both(board))
    if (c >= 5)and(not tc.check_token(me, token)): # 不正を検知 --- (※5)
        return "不正なアクセスです"
    if utils.can_flip(board, x, y, who):
        utils.flip(board, x, y, who)
        who, me = utils.toggle(who), who
    return redirect(url_for("index", who=me, token=tc.get_token(me)))

# ゲームをリセットする関数 --- (※6)
@app.route("/reset")
def reset():
    global board, who
    board = utils.generate_board()
    who = utils.BLACK
    tc.reset_tokens()
    return redirect(url_for("index"))

# 手番をスキップする関数 --- (※7)
@app.route("/skip")
def skip():
    global who
    me = int(request.args.get("who", who))
    token = request.args.get("token", "")
    if who != me:  # 自分の手番ではない
        return redirect(url_for("index", who=me, token=token))
    if not tc.check_token(me, token):
        return "不正なアクセスです"
    who = utils.toggle(who)
    return redirect(url_for("index", who=me, token=tc.get_token(me)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8888) # Flaskのサーバーを起動