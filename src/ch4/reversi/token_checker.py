import os
import hashlib

# ユーザー毎のトークン
user_tokens = ["", "", ""]
# ランダムなトークンを生成
def random_token() -> str:
    return hashlib.sha256(os.urandom(64)).hexdigest()
# ユーザー毎のトークンを返す
def get_token(who: int) -> str:
    return user_tokens[who]
# トークンが正しいかをチェック
def check_token(who: int, token: str) -> bool:
    if 1 <= who <= 2:
        return user_tokens[who] == token
    return False
# トークンをリセット
def reset_tokens():
    global user_tokens
    user_tokens = ["", random_token(), random_token()]
