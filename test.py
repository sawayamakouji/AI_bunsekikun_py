import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import plotly.express as px
from datetime import datetime

# 日本語フォントの設定
font_path = 'NotoSansJP-VariableFont_wght.ttf'  # フォントファイルのパスを指定
font_prop = font_manager.FontProperties(fname=font_path)

st.set_page_config(layout='wide')  # レイアウトを横に広げる設定

# マニュアルの内容
manual_content = """
# データ可視化アプリ ユーザーマニュアル
ようこそ！このデータ可視化アプリを使用して、アップロードしたCSVファイルのデータを簡単に視覚化しましょう。

本マニュアルでは、初心者の方でも分かりやすいように、ステップバイステップで操作方法をご紹介します。

---

## 1. アプリの概要
このアプリは、CSV形式のデータファイルをアップロードし、様々なグラフを作成することでデータを視覚的に分析するためのツールです。
以下の機能を提供しています：

- データのプレビュー
- 数値・カテゴリ・日付データのフィルタリング
- 複数のグラフタイプ（棒グラフ、散布図、折れ線グラフ、ヒートマップ、相関行列、時系列グラフ）の作成
- グラフのカスタマイズオプション

---

## 2. アプリの使用方法

### ステップ1: CSVファイルのアップロード
サイドバーの「CSVファイルをアップロードしてください。」
セクションを見つけます。

「ファイルを選択」ボタンをクリックし、パソコンから目的のCSVファイルを選択します。

**(画像はイメージです)**

#### アップロード前のデータ形式についての注意事項：
- **ヘッダーの存在**：CSVファイルは必ずヘッダー行（各列の名前が記載された最初の行）を含んでいる必要があります。
ヘッダーがない場合、アプリが正しくデータを認識できません。
- **データの整合性**：各列のデータ型が一貫していることを確認してください。
例えば、数値データの列にはすべて数値が含まれている必要があります。
- **日付形式**：日付データを含む場合、標準的な日付形式（例：YYYY-MM-DD）を使用してください。
不正な日付形式はフィルタリング機能に影響を与える可能性があります。
- **文字コード**：UTF-8形式で保存されたCSVファイルを使用してください。異なる文字コードの場合、文字化けが発生することがあります。

**例：**

日付,地域,売上,顧客数

2023-01-01,東京,5000,200

2023-01-02,大阪,4500,180

2023-01-03,名古屋,4700,190


---

### ステップ2: データのプレビュー
ファイルが正常にアップロードされると、画面上部に「グラフの可視化」と「データ」の2つのタブが表示されます。

「データ」タブをクリックし、「データのプレビュー」をクリックして、アップロードしたデータの内容を確認できます。

**(画像はイメージです)**

---

### ステップ3: データのフィルタリング
データを可視化する前に、必要なデータのみを抽出するためにフィルタリングを行います。

#### 3.1 数値項目のフィルタリング
サイドバーの「データのフィルタリング」セクションを展開し、「数値項目のフィルタリング」をクリックします。

各数値列に対してスライダーが表示されるので、スライダーを調整して表示したいデータの範囲を選択します。

**例**: 売上データが1000から5000の場合、スライダーを動かして特定の範囲を選択できます。

#### 3.2 カテゴリ項目のフィルタリング
「カテゴリ項目のフィルタリング」をクリックします。
各カテゴリ列に対して選択ボックスが表示され、表示したいカテゴリを選択または解除します。

**例**: 地域別データがある場合、特定の地域のみを選択できます。

#### 3.3 日付データのフィルタリング
「日付データのフィルタリング」セクションを確認します。

日付列が存在する場合、日付列を選択し、スライダーを使用して表示したい日付範囲を選択します。

**例**: 2023年1月1日から2023年12月31日までのデータを表示。

---

### ステップ4: グラフタイプの選択
サイドバーの「グラフタイプの選択」セクションを確認し、「グラフの種類を選択してください」ラジオボタンから希望のグラフタイプを選びます。

**利用可能なグラフタイプ：**
- 棒グラフ
- 散布図
- 折れ線グラフ
- ヒートマップ
- 相関行列
- 時系列グラフ

---

### ステップ5: グラフのカスタマイズ

#### 5.1 Y軸の集約方法選択
サイドバーの「Y軸集約オプション」セクションを確認し、「Y軸の集約方法を選択してください」ラジオボタンから希望の集約方法を選びます。

**選択肢：**
- そのまま
- 合計
- 平均
- 最大
- 最小

#### 5.2 時系列グラフのカテゴリ別フィルタリング（オプション）
時系列グラフを選択した場合のみ表示されるオプションです。「時系列カテゴリの選択」セクションを確認し、カテゴリ列を選択し表示したいカテゴリ値を選びます。

#### 5.3 ラベル表示オプション
サイドバーの「ラベル表示オプション」セクションで「X軸ラベルの表示方法を選択してください」ラジオボタンから希望の表示方法を選びます。

**選択肢：**
- 間引く
- 縮小
- 自動調整

---

### ステップ6: グラフの作成
メイン画面の「グラフの可視化」セクションに移動し、「X軸の列を選択してください。」ドロップダウンからX軸に使用する列を選び、「Y軸の列を選択してください。」ドロップダウンからY軸に使用する列を選びます。

選択が完了すると、自動的に選択したグラフが表示されます。

- **棒グラフ**：選択したX軸とY軸に基づいて棒グラフが表示されます。
- **散布図**：X軸とY軸のデータポイントをプロットします。
- **折れ線グラフ**：時間的な変化を折れ線で表示します。
- **ヒートマップ**：X軸とY軸の交差部分のデータ密度を色で表現します。
- **相関行列**：数値データ間の相関関係を視覚化します。
- **時系列グラフ**：選択した日付列に基づいてデータを時系列で表示します。

---

## 3. 各グラフタイプの詳細
### 3.1 棒グラフ
- 用途：カテゴリごとのデータの比較。
- カスタマイズ：頻度、合計、平均で集約可能。

### 3.2 散布図
- 用途：2つの変数間の関係性を視覚化。
- カスタマイズ：データポイントの色やサイズも変更可能。

### 3.3 折れ線グラフ
- 用途：データの時間的な変化を追跡。
- カスタマイズ：複数のデータ系列を同時に表示。

### 3.4 ヒートマップ
- 用途：2つのカテゴリ間の関係性や密度を色で表現。
- カスタマイズ：色のスケールやラベルの表示方法を調整。

### 3.5 相関行列
- 用途：数値データ間の相関関係を分析。
- カスタマイズ：表示する数値列を選択可能。

### 3.6 時系列グラフ
- 用途：時間に沿ったデータの変動を分析。
- カスタマイズ：集約方法（合計、平均、最大、最小）やカテゴリ別の表示。

---

## 4. トラブルシューティング
### 問題1: CSVファイルが読み込めない
- **原因**：ファイル形式がCSVではない、またはファイルが破損している可能性。
- **対策**：
  - ファイルが正しいCSV形式であることを確認。
  -

 別のCSVファイルを試してみる。

### 問題2: 日付フィルタリングが機能しない
- **原因**：日付列に不正な値が含まれている可能性。
- **対策**：
  - CSVファイル内の日付データが正しい形式（例：YYYY-MM-DDやYYYY/MM/DD）であることを確認。
  - 不正な日付値を修正または削除。

### 問題3: グラフが表示されない
- **原因**：選択したデータに基づくグラフが適切に作成されていない可能性。
- **対策**：
  - X軸とY軸に適切な列が選択されているか確認。
  - フィルタリングによってデータが絞り込みすぎていないか確認。

---

## 5. 追加のヒント
- **データの前処理**：グラフを作成する前に、データが正しく整形されていることを確認するとスムーズです。
- **グラフの保存**：作成したグラフは右上のメニューから画像として保存できます。
- **フィルタリングの活用**：データを絞り込むことで、より具体的な分析が可能になります。

---

## 6. まとめ
このデータ可視化アプリを活用することで、複雑なデータも直感的に理解しやすいグラフで表現できます。ぜひ、様々なデータを試して、データ分析の楽しさを体験してください！

ご不明点やフィードバックがありましたら、サポートまでご連絡ください。

---

## 開発者より
このアプリをご利用いただきありがとうございます。皆様のデータ分析がより効率的で有意義なものとなるよう、今後も機能の改善を続けてまいります。

---

## 参考リンク
- [Streamlit 公式ドキュメント](https://docs.streamlit.io)
- [Pandas 公式ドキュメント](https://pandas.pydata.org/docs/)
- [Plotly 公式ドキュメント](https://plotly.com/python/)

このマニュアルは2024年10月30日現在の情報に基づいて作成されています。アプリのアップデートに伴い内容が変更される場合がありますので、最新情報は公式サイトをご確認ください。
```
"""  # マニュアルの長い説明は省略しています

# タイトルとマニュアルのエクスパンダーを配置
st.title('データ可視化アプリ')

with st.expander("データ可視化アプリ ユーザーマニュアル", expanded=False):
    st.markdown(manual_content)

# データアップロード処理
uploaded_file = st.sidebar.file_uploader('CSVファイルをアップロードしてください。', type='csv')

if uploaded_file is not None:
    # データの読み込み
    df = pd.read_csv(uploaded_file)

    # メイン画面にタブを追加して、データのプレビューを右側に隠す
    tab1, tab2 = st.tabs(["グラフの可視化", "データ"])

    with tab2:
        with st.expander('データのプレビュー', expanded=False):
            st.dataframe(df)

    with tab1:
        # すべての列を取得
        all_columns = df.columns.tolist()

        # （以下、残りのコードはそのまま）


        # データのフィルタリング
        st.sidebar.header('データのフィルタリング')

        # 数値項目のフィルタリング（エクスパンダー内に配置）
        with st.sidebar.expander('数値項目のフィルタリング'):
            numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
            for col in numeric_columns:
                min_value = float(df[col].min())
                max_value = float(df[col].max())
                if min_value == max_value:
                    # スライダーが不要な場合
                    selected_range = (min_value, max_value)
                else:
                    selected_range = st.slider(
                        f'{col}の範囲', 
                        min_value, 
                        max_value, 
                        (min_value, max_value),
                        key=f'{col}_slider',
                        step=(max_value - min_value) / 100  # スライダーのステップサイズを調整
                    )
                df = df[df[col].between(*selected_range)]

        # カテゴリ項目のフィルタリング（エクスパンダー内に配置）
        with st.sidebar.expander('カテゴリ項目のフィルタリング'):
            categorical_columns = df.select_dtypes(exclude=np.number).columns.tolist()
            for col in categorical_columns:
                unique_values = df[col].unique()
                selected_values = st.multiselect(
                    f'{col}の選択', 
                    unique_values, 
                    default=unique_values, 
                    key=f'{col}_multiselect'
                )
                df = df[df[col].isin(selected_values)]

        # 日付データのフィルタ（タイムライン用）
        date_columns = df.select_dtypes(include=['datetime64', 'object']).columns.tolist()
        date_columns = [col for col in date_columns if pd.to_datetime(df[col], errors='coerce').notna().any()]
        selected_date_column = None
        if date_columns:
            st.sidebar.header('日付データのフィルタリング')
            selected_date_column = st.sidebar.selectbox('日付列を選択してください', date_columns)
            df[selected_date_column] = pd.to_datetime(df[selected_date_column], errors='coerce')
            df = df.dropna(subset=[selected_date_column])
            min_date = df[selected_date_column].min()
            max_date = df[selected_date_column].max()
            if pd.isna(min_date) or pd.isna(max_date):
                st.sidebar.error("日付データに不正な値が含まれています。適切な日付形式で入力してください。")
            else:
                selected_date_range = st.sidebar.slider(
                    '日付範囲を選択してください', 
                    min_value=min_date.to_pydatetime(), 
                    max_value=max_date.to_pydatetime(), 
                    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
                    format='YYYY-MM-DD'
                )
                
                # 選択した日付範囲でフィルタリング
                df = df[(df[selected_date_column] >= pd.Timestamp(selected_date_range[0])) & (df[selected_date_column] <= pd.Timestamp(selected_date_range[1]))]

        # グラフタイプの選択（ユーザーが自由に選択可能にする）
        st.sidebar.header('グラフタイプの選択')
        graph_type = st.sidebar.radio('グラフの種類を選択してください', ['棒グラフ', '散布図', '折れ線グラフ', 'ヒートマップ', '相関行列', '時系列グラフ'])

        # Y軸の集約方法選択オプションを追加
        st.sidebar.header('Y軸集約オプション')
        aggregation_method = st.sidebar.radio('Y軸の集約方法を選択してください', ['そのまま', '合計', '平均', '最大', '最小'])

        # 時系列グラフのカテゴリ別フィルタリングオプションを追加
        st.sidebar.header('時系列カテゴリの選択')
        if graph_type == '時系列グラフ':
            category_columns = df.select_dtypes(exclude=np.number).columns.tolist()
            if category_columns:
                selected_category_column = st.sidebar.selectbox('カテゴリ列を選択してください', category_columns, key='category_column')
                unique_category_values = df[selected_category_column].unique()
                selected_category_values = st.sidebar.multiselect(f'{selected_category_column}の選択', unique_category_values, default=unique_category_values, key='category_multiselect')
                df = df[df[selected_category_column].isin(selected_category_values)]

        # ラベル表示オプションの選択
        st.sidebar.header('ラベル表示オプション')
        label_option = st.sidebar.radio('X軸ラベルの表示方法を選択してください', ['間引く', '縮小', '自動調整'])

        # 分析と可視化（メイン画面に表示）
        st.subheader('グラフの可視化')
        x_axis = st.selectbox('X軸の列を選択してください。', all_columns, key='x_axis')
        y_axis = st.selectbox('Y軸の列を選択してください。', all_columns, key='y_axis')

        # グラフ描画の実装
        if graph_type == '時系列グラフ':
            if selected_date_column:
                # 時系列グラフの集約処理
                if aggregation_method == '合計':
                    df_grouped = df.groupby([selected_date_column, selected_category_column])[y_axis].sum().reset_index()
                elif aggregation_method == '平均':
                    df_grouped = df.groupby([selected_date_column, selected_category_column])[y_axis].mean().reset_index()
                elif aggregation_method == '最大':
                    df_grouped = df.groupby([selected_date_column, selected_category_column])[y_axis].max().reset_index()
                elif aggregation_method == '最小':
                    df_grouped = df.groupby([selected_date_column, selected_category_column])[y_axis].min().reset_index()
                else:
                    df_grouped = df.copy()

                # 時系列グラフの作成（カテゴリ別に色分け）
                fig = px.line(df_grouped, x=selected_date_column, y=y_axis, color=selected_category_column, title=f'{selected_date_column}と{y_axis}の時系列グラフ（{selected_category_column}別）')
                fig.update_xaxes(title_text='日付', tickformat='%Y年%m月%d日')
                fig.update_yaxes(title_text='売上（千円）', tickformat='~s', tickprefix='', ticksuffix='千円')
                fig.update_yaxes(title_text=y_axis, ticksuffix='')
                st.plotly_chart(fig)
            else:
                st.error("時系列グラフを作成するには日付列が必要です。")
        elif graph_type == '棒グラフ':
            aggregation_type = st.radio('集計方法を選択してください', ['頻度', '合計', '平均'], key='aggregation_type')
            if aggregation_type == '頻度':
                data = df[x_axis].value_counts().reset_index()
                data.columns = [x_axis, 'count']
                fig = px.bar(data, x=x_axis, y='count', title=f'{x_axis}の棒グラフ', labels={x_axis: x_axis, 'count': '頻度'})
            elif aggregation_type == '合計':
                data = df.groupby(x_axis)[y_axis].sum().reset_index()
                fig = px.bar(data, x=x_axis, y=y_axis, title=f'{x_axis}ごとの合計{y_axis}', labels={x_axis: x_axis, y_axis: f'合計{y_axis}'})
            elif aggregation_type == '平均':
                data = df.groupby(x_axis)[y_axis].mean().reset_index()
                fig = px.bar(data, x=x_axis, y=y_axis, title=f'{x_axis}ごとの平均{y_axis}', labels={x_axis: x_axis, y_axis: f'平均{y_axis}'})
            st.plotly_chart(fig)
        elif graph_type == '散布図':
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{x_axis}と{y_axis}の散布図')
            st.plotly_chart(fig)
        elif graph_type == '折れ線グラフ':
            fig = px.line(df, x=x_axis, y=y_axis, title=f'{x_axis}と{y_axis}の折れ線グラフ')
            st.plotly_chart(fig)
        elif graph_type == 'ヒートマップ':
            crosstab = pd.crosstab(df[y_axis], df[x_axis])
            fig, ax = plt.subplots(figsize=(12, 8))
            cax = ax.matshow(crosstab, cmap='viridis')
            fig.colorbar(cax)
            ax.set_xticks(range(len(crosstab.columns)))
            ax.set_xticklabels(crosstab.columns, rotation=45, ha='right', fontproperties=font_prop)
            ax.set_yticks(range(len(crosstab.index)))
            ax.set_yticklabels(crosstab.index, fontproperties=font_prop, fontsize=10)
            ax.set_xlabel(x_axis, fontproperties=font_prop)
            ax.set_ylabel(y_axis, fontproperties=font_prop)
            ax.set_title(f'{x_axis}と{y_axis}のクロス集計', fontproperties=font_prop)
            if label_option == '縮小':
                plt.xticks(fontsize=8)
            elif label_option == '間引く':
                for label in ax.get_xticklabels()[::2]:
                    label.set_visible(False)
            st.pyplot(fig)
        elif graph_type == '相関行列':
            dimensions = [x_axis, y_axis] if pd.api.types.is_numeric_dtype(df[x_axis]) and pd.api.types.is_numeric_dtype(df[y_axis]) else df.select_dtypes(include=np.number).columns.tolist()
            if len(dimensions) > 1:
                fig_corr = px.scatter_matrix(df, dimensions=dimensions, title='数値データの相関関係の散布図行列')
                st.plotly_chart(fig_corr)
            else:
                st.error("相関行列を作成するには少なくとも2つの数値列が必要です。")
