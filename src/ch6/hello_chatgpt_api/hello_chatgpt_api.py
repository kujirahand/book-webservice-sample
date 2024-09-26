from typing import Any, Dict

# openaiパッケージのインポート ---（※１）
from openai import OpenAI

# APIキーの指定 ---（※２）
OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"

# OpenAIインスタンス作成 ---（※３）
client: OpenAI = OpenAI(api_key=OPENAI_API_KEY)

# ChatGPTのAPIを使って、質問する ---（※４）
response: Dict[str, Any] = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "「受けるより与える方が幸福である」を英語に翻訳してください",
        }
    ],
)

# ChatGPTの回答を表示する ---（※５）
print(response.choices[0].message.content)
