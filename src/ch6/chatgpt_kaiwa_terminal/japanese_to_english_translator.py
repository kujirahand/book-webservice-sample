# python-dotenvパッケージやosパッケージのインポート
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

# APIキーを環境変数から読み込んで設定
load_dotenv()
openai_api_key: str = os.getenv("OPENAI_API_KEY")

# OpenAIインスタンス作成
client: OpenAI = OpenAI(api_key=openai_api_key)

# 役割や質疑応答の内容を保存するリスト --- (※１)
messages: List[Dict[str, str]] = [
    # 役割の設定 --- (※２)
    {
        "role": "system",
        "content": "あなたは、子供向けにシンプルにわかりやすく教える大阪弁の英語の先生です。",
    }
]


# ChatGPTと会話するための関数 --- (※３)
def ask_chatgpt(user_question: str, model: str = "gpt-4o-mini"):
    # 質問をリストに追加 --- (※４)
    messages.append({"role": "user", "content": user_question})

    # ChatGPTのAPIを使って、質問する --- (※５)
    response: Dict[str, Any] = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    # ChatGPTの回答を取得
    chatgpt_answer: str = response.choices[0].message.content

    # ChatGPTの回答をリストに追加 --- (※６)
    messages.append({"role": "assistant", "content": chatgpt_answer})

    # ChatGPTの回答を返却
    return chatgpt_answer


if __name__ == "__main__":
    # ask_chatgpt関数を使って、日本語から英語への翻訳を依頼 --- (※７)
    print("*****英語に翻訳したい文章を日本語で入力してください。")
    user_input: str = input("日本語>")
    user_question: str = "「" + user_input + "」" + "を英語に翻訳してください。"
    print("ChatGPTの回答>" + ask_chatgpt(user_question))

    # ask_chatgpt関数を使って、単語分割を依頼 --- (※８)
    print("*****さらに、単語分割の結果も知りたいですか？（1:知りたい、2：不要）")
    user_input = input("1:知りたい、1以外：不要 >")
    if user_input != "1":
        quit()
    user_question: str = (
        "翻訳結果を単語分割して、それぞれの単語の意味と発音を教えてください。"
    )
    print(ask_chatgpt(user_question))
