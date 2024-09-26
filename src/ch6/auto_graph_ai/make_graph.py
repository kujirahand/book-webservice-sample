import os
from dotenv import load_dotenv
from openai import OpenAI

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(SCRIPT_DIR, "mermaid.prompt.txt")

# 環境変数を読み込みOpenAIのキーを初期化  --- (※1)
load_dotenv()
openai_client: OpenAI = OpenAI()

# ChatGPTに問い合わを行う関数 --- (※2)
def ask_chatgpt(prompt: str) -> str:
    sys = "You are an expert in organizing things logically" + \
        " and creating Mermaid diagrams."
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": prompt},
        ])
    return response.choices[0].message.content

# 指示を元に作図する関数 --- (※3)
def make_graph(input: str) -> str:
    # 作図プロンプトのテンプレートを読み込む --- (※4)
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt = f.read()
    # プロンプトを作成 --- (※5)
    input = input.replace("```", "｀｀｀") # 特殊記号をエスケープ
    prompt = prompt.replace("[[INPUT]]", input)
    # ChatGPTに問い合わせ --- (※6)
    result = ask_chatgpt(prompt)
    # Mermaidのコードを取り出す --- (※7)
    code = "graph TD; A[残念]-->B[作図失敗];" # デフォルトのコード
    if "```" in result:
        text = result.replace("```mermaid", "```")
        code = text.split("```")[1]
    return code, result

if __name__ == '__main__':
    # テスト --- (※8)
    code, result = make_graph("有名なプログラミング言語を列挙してください。")
    print("code:", code)
    print("result:", result)