import os
from typing import Any, Dict, List

import markdown
from dotenv import load_dotenv
from flask import Flask, render_template, request, session

# Ollama用のパッケージをインポート　 --- (※１)
from ollama import Client

# Flaskインスタンスを生成
app: Flask = Flask(__name__)

# 環境変数を読み込み、セッションのシークレットキーを設定　 --- (※２)
load_dotenv()
app.secret_key = os.getenv("APP_SECRET_KEY")

# OllamaのAPIクライアント用インスタンスを生成　 --- (※３)
client: Client = Client(host="http://localhost:11434")


# セッションを初期化するための関数
def initialize_session():
    session.clear()
    session["messages"] = [
        # 役割の設定
        {
            "role": "system",
            "content": "あなたは、子供向けにシンプルにわかりやすく教える大阪弁の英語の先生です。",
        }
    ]


# セッションに会話を追加するための関数
def append_session(role: str, content: str):
    messages: List = session["messages"]
    messages.append({"role": role, "content": content})
    session["messages"] = messages


# オープンソースLLMと会話するための関数　 --- (※４)
def ask_openllm(user_question: str, model: str = "llama3.1"):
    # ユーザーの質問をセッションに追加
    append_session("user", user_question)

    # オープンソースLLMを使って、質問する
    response: Dict[str, Any] = client.chat(
        model=model,
        messages=session["messages"],
    )

    # オープンソースLLMの回答を取得し、セッションに追加
    openllm_answer: str = response["message"]["content"]
    append_session("assistant", openllm_answer)

    # ChatGPTの回答をhtml文字列に変換して返却
    return markdown.markdown(openllm_answer)


# 「/」にアクセスがあった場合のルーティング
@app.route("/")
def index():
    return render_template("index.html")


# 「/translate」にアクセスがあった場合のルーティング
@app.route("/translate", methods=["POST"])
def translate():
    # セッションを初期化
    initialize_session()

    # ユーザーの入力値を取得して、質問を作成
    user_input: str = request.form.get("user_input")
    user_question: str = "「" + user_input + "」" + "を英語に翻訳してください。"

    # オープンLLMに質問して、結果を取得　 --- (※５)
    translation_result: str = ask_openllm(user_question)

    # 結果を返却
    return render_template(
        "translation_result.html", translation_result=translation_result
    )


# 「/tokenize」にアクセスがあった場合のルーティング
@app.route("/tokenize", methods=["POST"])
def tokenize():
    # 質問を作成
    user_question: str = (
        "翻訳結果を単語分割して、それぞれの単語の意味と発音を教えてください。"
    )
    # オープンLLMに質問して、結果を取得　 --- (※６)
    tokenization_result: str = ask_openllm(user_question)

    # 結果を返却
    return render_template(
        "tokenization_result.html", tokenization_result=tokenization_result
    )


if __name__ == "__main__":
    app.run(debug=True)
