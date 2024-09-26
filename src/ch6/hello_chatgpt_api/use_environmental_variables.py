# python-dotenvパッケージやosパッケージのインポート --- (※１)
import os
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI

# APIキーを環境変数から読み込んで設定 --- (※２)
load_dotenv()
openai_api_key: str = os.getenv("OPENAI_API_KEY")

# OpenAIインスタンス作成 --- (※３)
client: OpenAI = OpenAI(api_key=openai_api_key)

# ChatGPTのAPIを使って、質問する
response: Dict[str, Any] = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "「受けるより与える方が幸福である」を英語に翻訳してください",
        }
    ],
)

# ChatGPTの回答を表示する
print(response.choices[0].message.content)
