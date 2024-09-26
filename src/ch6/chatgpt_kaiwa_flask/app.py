import os
from typing import Any, Dict, List

import markdown
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from openai import OpenAI

# Flaskインスタンスを生成
app: Flask = Flask(__name__)

# 環境変数を読み込み、APIキーとセッションのシークレットキーを設定　 --- (※１)
load_dotenv()
client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app.secret_key = os.getenv("APP_SECRET_KEY")


# セッションを初期化するための関数　 --- (※２)
def initialize_session():
    session.clear()
    session["messages"] = [
        # 役割の設定
        {
            "role": "system",
            "content": "あなたは、子供向けにシンプルにわかりやすく教える大阪弁の英語の先生です。",
        }
    ]


# セッションに会話を追加するための関数　 --- (※３)
def append_session(role: str, content: str):
    messages: List = session["messages"]
    messages.append({"role": role, "content": content})
    session["messages"] = messages


# ChatGPTと会話するための関数　 --- (※４)
def ask_chatgpt(user_question: str, model: str = "gpt-4o-mini"):
    # ユーザーの質問をセッションに追加
    append_session("user", user_question)

    # ChatGPTのAPIを使って、質問する
    response: Dict[str, Any] = client.chat.completions.create(
        model=model,
        messages=session["messages"],
    )

    # ChatGPTの回答を取得し、セッションに追加
    chatgpt_answer: str = response.choices[0].message.content
    append_session("assistant", chatgpt_answer)

    # ChatGPTの回答をhtml文字列に変換して返却
    return markdown.markdown(chatgpt_answer)


# 「/」にアクセスがあった場合のルーティング --- (※５)
@app.route("/")
def index():
    return render_template("index.html")


# 「/translate」にアクセスがあった場合のルーティング　 --- (※６)
@app.route("/translate", methods=["POST"])
def translate():
    # セッションを初期化
    initialize_session()

    # ユーザーの入力値を取得して、質問を作成
    user_input: str = request.form.get("user_input")
    user_question: str = "「" + user_input + "」" + "を英語に翻訳してください。"

    # ChatGPTに質問して、結果を取得
    translation_result: str = ask_chatgpt(user_question)

    # 結果を返却
    return render_template(
        "translation_result.html", translation_result=translation_result
    )


# 「/tokenize」にアクセスがあった場合のルーティング　--- (※７)
@app.route("/tokenize", methods=["POST"])
def tokenize():
    # 質問を作成
    user_question: str = (
        "翻訳結果を単語分割して、それぞれの単語の意味と発音を教えてください。"
    )
    # ChatGPTに質問して、結果を取得
    tokenization_result: str = ask_chatgpt(user_question)

    # 結果を返却
    return render_template(
        "tokenization_result.html", tokenization_result=tokenization_result
    )


if __name__ == "__main__":
    app.run(debug=True)
