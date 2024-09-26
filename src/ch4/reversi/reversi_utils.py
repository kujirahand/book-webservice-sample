# リバーシの石の状態を表す定数 --- (※1)
EMPTY, BLACK, WHITE, CAN_FLIP = 0, 1, 2, 3
STATUS = ["□", "黒", "白", "・"]
# 8方向の相対座標を表す定数 [(dx, dy)…] --- (※2)
DIR_OFFSET = [ (-1, -1), (-1, 0), (-1, 1),
               ( 0, -1),          ( 0, 1),
               ( 1, -1), ( 1, 0), ( 1, 1) ]
# ボードを初期化する関数 --- (※3)
def generate_board() -> list[list[int]]:
    board = [ [EMPTY] * 8 for _ in range(8) ]
    board[3][4] = board[4][3] = BLACK
    board[3][3] = board[4][4] = WHITE
    return board
# (x, y)がボードの範囲内かどうかを調べる関数 --- (※4)
def is_on_board(x: int, y: int) -> bool:
    return 0 <= y < 8 and 0 <= x < 8
# 白黒を反転する関数 --- (※5)
def toggle(status: int) -> int:
    if status == EMPTY:
        return EMPTY
    return BLACK if status == WHITE else WHITE
# 位置(x, y)の方向(dx, dy)に石を置けるかどうかを調べる --- (※6)
def can_flip_dir(board: list[list[int]],
        x: int, y: int, dx: int, dy: int, who: int) -> bool:
    if board[y][x] != EMPTY:  # 石が既にあるなら置けない
        return False
    if not is_on_board(x + dx, y + dy):  # 範囲外なら置けない
        return False
    if board[y + dy][x + dx] != toggle(who):  # 自分の石なら置けない
        return False
    # ひっくり返せるかどうか調べる --- (※7)
    for i in range(2, 8):
        if not is_on_board(x + dx * i, y + dy * i): # 範囲外
            return False
        if board[y + dy * i][x + dx * i] == EMPTY:  # 空白
            return False
        if board[y + dy * i][x + dx * i] == who: # OK
            return True
    return False
# 位置(x, yに石を置けるか八方向を調べる --- (※8)
def can_flip(board: list[list[int]],
        x: int, y:int, who: int) -> bool:
    for dx, dy in DIR_OFFSET:
        if can_flip_dir(board, x, y, dx, dy, who):
            return True
    return False
# 方向(dx, dy)に石を置く --- (※9)
def flip_dir(board: list[list[int]],
             x: int, y: int, dx: int, dy: int, who: int) -> int:
    if not can_flip_dir(board, x, y, dx, dy, who):
        return 0
    count = 0
    for i in range(1, 8):
        if not is_on_board(x + dx * i, y + dy * i):
            break
        if board[y + dy * i][x + dx * i] == who:
            break
        board[y + dy * i][x + dx * i] = who
        count += 1
    return count
# 位置(x, y)に石を置く。ひっくり返した石の数を返す --- (※10)
def flip(board: list[list[int]], x:int, y:int, who: int) -> int:
    if not can_flip(board, x, y, who):
        return 0
    count = 0
    for dx, dy in DIR_OFFSET:
        count += flip_dir(board, x, y, dx, dy, who)
    board[y][x] = who
    return count
# 石を置ける場所にマークをつける関数 --- (※11)
def add_flip_mark(board: list[list[int]], who: int) -> list[list[int]]:
    res = generate_board()
    for y in range(8):
        for x in range(8):
            res[y][x] = board[y][x]
            if board[y][x] == EMPTY:
                if can_flip(board, x, y, who):
                    res[y][x] = CAN_FLIP
    return res
# 石の数を数える --- (※12)
def count_stone(board: list[list[int]], who: int) -> int:
    return sum([ row.count(who) for row in board ])
def count_stone_both(board: list[list[int]]) -> tuple[int, int]:
    return count_stone(board, BLACK), count_stone(board, WHITE)