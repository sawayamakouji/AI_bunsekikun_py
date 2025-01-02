import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import re
from dotenv import load_dotenv

# フォント設定
font_path = os.path.abspath("./NotoSansJP-Regular.ttf")  # フォントファイルの絶対パスを指定
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    fm.fontManager.addfont(font_path)  # フォントを追加登録
    matplotlib.rcParams['font.family'] = font_prop.get_name()
else:
    st.warning("指定されたフォントファイルが見つかりませんでした。デフォルトのフォントを使用します。")

# API設定
load_dotenv()
api_key = os.getenv("API_KEY") or "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

# Streamlit UI
st.title("Gemini Data Analysis with Custom Code Execution")
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

# ファイルアップロード確認
if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        if data.empty:
            st.error("アップロードされたファイルにデータがありません。適切なCSVファイルをアップロードしてください。")
        else:
            # データ列名を英語変換（必要に応じて）
            data.columns = [re.sub(r'[^\w]', '_', col) for col in data.columns]
            
            st.write("データプレビュー:", data.head())
            user_query = st.text_input("分析内容を自然言語で入力してください")

            if user_query:
                headers = ", ".join(data.columns)
                # プロンプトにアップロードデータの指定を明記
                prompt = f"""
                次のデータを使用して、'{user_query}'の通りの分析を行うためのPythonコードを書いてください。

                データは以下の形式です:
                - データのヘッダー情報: {headers}
                - データサンプル:
                {data.head().to_string()}

                注意:
                - アップロードされたCSVデータは既に `data` という変数に格納されています。
                - データの再読み込みを行わず、既存の `data` 変数を使用してください。
                - データ操作は全て `data` 変数を用いて行い、Streamlitで表示できるようにしてください。
                - 必ず `data` 変数を用いた操作にしてください（例: `data.groupby(...)`, `data['列名']` など）。
                """

                try:
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
                        generated_code = re.sub(r"plt\.show", "st.pyplot()", generated_code)
                        # データの再読み込み部分を削除し、`data` 変数を利用するよう修正
                        generated_code = re.sub(r"data\s*=\s*pd\.read_csv.*?\n", "", generated_code)
                        # `uploaded_file` の利用を削除し、アップロードされたデータを直接利用
                        generated_code = re.sub(r"uploaded_file\s*=\s*.*?\n", "", generated_code)

                        # セキュリティチェック
                        prohibited_keywords = ["os.system", "subprocess", "eval"]
                        if any(keyword in generated_code for keyword in prohibited_keywords):
                            st.error("生成されたコードに危険な操作が含まれています。")
                            st.stop()

                        st.write("Geminiが生成したコード（修正後）:")
                        st.code(generated_code, language="python")

                        # 実行ボタン
                        if st.button("生成されたコードを実行する"):
                            try:
                                st.write("コードを実行しています...（この処理には時間がかかる場合があります）")
                                with st.spinner('コード実行中です。しばらくお待ちください...'):
                                    local_vars = {'pd': pd, 'st': st, 'plt': plt, 'data': data, 'font_prop': font_prop}
                                    exec(generated_code, {}, local_vars)
                                st.success("コードの実行が完了しました。")
                            except Exception as e:
                                st.error(f"コードの実行中にエラーが発生しました: {e}")
                    else:
                        st.error("Geminiから有効なコードが生成されませんでした。プロンプトを調整してください。")
                except Exception as e:
                    st.error(f"Gemini APIからの応答中にエラーが発生しました: {e}")
    except pd.errors.EmptyDataError:
        st.error("アップロードされたファイルにデータが含まれていません。別のCSVファイルを試してください。")
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
else:
    st.info("CSVファイルをアップロードしてください。")