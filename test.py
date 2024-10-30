import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 日本語フォントの設定
font_path = 'NotoSansJP-VariableFont_wght.ttf'  # フォントファイルのパスを指定
font_prop = font_manager.FontProperties(fname=font_path)

st.set_page_config(layout='wide')  # レイアウトを横に広げる設定

st.title('データ可視化アプリ')

# サイドバーにマニュアルボタンを追加
if st.sidebar.button('マニュアルを見る'):
    with st.expander("マニュアル", expanded=True):
        st.markdown("""
        # データ可視化アプリ ユーザーマニュアル

        ようこそ！このデータ可視化アプリを使用して、アップロードしたCSVファイルのデータを簡単に視覚化しましょう。本マニュアルでは、初心者の方でも分かりやすいように、ステップバイステップで操作方法をご紹介します。

        ---

        ## 1. アプリの概要

        ...（前述のマニュアル内容をここに挿入）...

        """, unsafe_allow_html=True)

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
        
        # データのフィルタリング
        st.sidebar.header('データのフィルタリング')
        
        # 数値項目のフィルタリング（エクスパンダー内に配置）
        with st.sidebar.expander('数値項目のフィルタリング'):
            numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
            for col in numeric_columns:
                min_value = float(df[col].min())
                max_value = float(df[col].max())
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
                fig.update_xaxes(title_text='日付')
                fig.update_yaxes(title_text='売上（千円）')
                fig.update_yaxes(title_text=y_axis, ticksuffix='')
                st.plotly_chart(fig)
            else:
                st.error("時系列グラフを作成するには日付列が必要です。")
        # その他のグラフの描画はここにあるが、長いので繁雑を避けるため省略
        # ただし、各グラフの作成方法はこの概要を追従する



        if graph_type == '棒グラフ':
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
