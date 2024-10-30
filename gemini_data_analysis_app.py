import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv

# フォント設定（省略）

# API設定
load_dotenv()
api_key = os.getenv("API_KEY") or "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

# Streamlit UI
st.title("Gemini Data Analysis with Custom Code Execution")
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

# ファイルアップロード確認
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("データプレビュー:", data.head())
    user_query = st.text_input("分析内容を自然言語で入力してください")
    
    if user_query:
        headers = ", ".join(data.columns)
        # プロンプトにアップロードデータの指定を明記
        prompt = f"""
        次のデータを使用して、'{user_query}'の通りの分析結果を出力してください
        またそれを行うPythonコードを書いてください。

        データは以下の形式です:
        - データのヘッダー情報: {headers}
        - データサンプル:
        {data.head().to_string()}

        注意:
        - `uploaded_file`としてアップロードされたデータを使ってください。
        - データの読み込みは `data = pd.read_csv(uploaded_file)` としてください。
        - 結果はStreamlitで表示できるようにしてください。
        """
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        generated_code_full = response.text

        # 生成されたコードを表示
        st.write("Geminiが生成したコード:")
        st.code(generated_code_full, language="python")

        # codeブロック内のコードだけを抽出
        code_block_match = re.search(r'```python\n(.*?)\n```', generated_code_full, re.DOTALL)
        if code_block_match:
            generated_code = code_block_match.group(1)
            
            # `plt.show()` を `st.pyplot()` に置き換え
            generated_code = re.sub(r"plt\.show\(\)", "st.pyplot()", generated_code)
            # `st.file_uploader()` を削除し、`uploaded_file`を使うように置換
            generated_code = re.sub(r"uploaded_file\s*=\s*st\.file_uploader\(.*?\)", "", generated_code)
            
            st.write("Geminiが生成したコード（修正後）:")
            st.code(generated_code, language="python")

            # 実行ボタン
            if st.button("生成されたコードを実行する"):
                try:
                    st.write("コードを実行しています...")
                    local_vars = {'uploaded_file': uploaded_file, 'pd': pd, 'st': st, 'plt': plt}
                    exec(generated_code, {}, local_vars)
                except Exception as e:
                    st.error(f"コードの実行中にエラーが発生しました: {e}")
        else:
            st.error("Geminiからのコードブロックが見つかりませんでした。生成されたコードの形式を確認してください。")
else:
    st.info("CSVファイルをアップロードしてください。")
