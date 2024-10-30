import os
from dotenv import load_dotenv
import google.generativeai as genai

# 環境変数からAPIキーを読み込む
load_dotenv()
api_key = os.getenv("API_KEY")

# APIキーが設定されているか確認
if not api_key:
    print("APIキーが設定されていません。'.env'ファイルを確認してください。")
else:
    # Gemini APIを設定
    genai.configure(api_key=api_key)
    
    # モデルの選択とテキスト生成リクエスト
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("教えてほしい、幸せの秘訣って何？")

        # 結果を表示
        print("Gemini APIからの応答:")
        print(response.text)

    except Exception as e:
        print("APIリクエストでエラーが発生しました:", e)
