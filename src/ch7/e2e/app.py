import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chromeの設定 --- (※1)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # ヘッドレスモードで実行
options.add_argument('--disable-dev-shm-usage')  # メモリ不足のクラッシュ回避

# WebDriverのセットアップ --- (※2)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ウェブサイトを開く --- (※3)
url = "https://example.com"  # 対象のウェブサイト
driver.get(url)

# 結果を格納する変数 --- (※4)
result = True

# 期待するH1タグの内容 --- (※5)
expected_h1_text = "掲示板のトップページ"  # 期待するテキストをここに指定

# H1タグの内容が期待する文字列が含まれるか確認 --- (※6)
h1_element = driver.find_element(By.TAG_NAME, "h1")
h1_text = h1_element.text
if expected_h1_text in h1_text:
    print(f"H1タグが期待通りです。取得した内容: {h1_text}")
else:
    print(f"エラー: H1タグが期待する内容と一致しません。取得した内容: {h1_text}")
    result = False

# ブラウザを閉じる --- (※7)
driver.quit()

# 結果により終了コードを制御 --- (※8)
if result == False:
    sys.exit(1)  # エラー終了
