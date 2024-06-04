import streamlit as st
import pandas as pd

def main():
    #SHOW標題
    st.title('臺灣能源現況')
    #普通文字
    st.write('410971105 顏詠璇 資料分析期末')

    #輸入互動元素
    name= st.text_input('請輸入文字:')
    #print輸入文字
    if name:
        st.write(f'你好,{name}')

    #上傳數據
    uploaded_file= st.file_uploader('上傳文件:CSV',type=['csv','xlsx'])#上傳檔案元件
    df=None #初始化表格

    if uploaded_file is not None:
        file_extension= uploaded_file.name.split(".")[-1]
        if file_extension.lower()=='csv':
            df=pd.read_csv(uploaded_file)
        else:
            df=pd.read_excel(uploaded_file,engine='openpyxl')

    #顯示數據
    st.write('原始數據')
    st.write(df)
    #選擇顯示的欄位
    if df is not None:

        #日期區間選擇
        if '日期' in df.columns:
            df['日期'] = pd.to_datetime(df['日期'])
            #設定區間
            min_date = df['日期'].min().date()
            max_date = df['日期'].max().date()

            #日期元件
            date_range = st.date_input('選擇日期範圍',(min_date,max_date))
            start_date = pd.Timestamp(date_range[0])
            end_date = pd.Timestamp(date_range[1])

            filtered_df = df[(df['日期']>=start_date)&(df['日期']<=end_date)]

            st.write('篩選後的')
            st.write(filtered_df)

        show_summary= st.checkbox('顯示摘要')

        if show_summary:
            st.write('數據統計摘要')
            st.write(df.describe())

        multiselected_columns = st.multiselect('選擇要顯示的列',df.columns)

        if multiselected_columns:
            st.write('已選擇')
            st.write(df[multiselected_columns])

        #單一選擇欄位
        selected_column = st.selectbox('選擇要用在柱狀圖的列',['銷售金額','訂單數量'])

        #視覺化
        st.write('數據視覺化')
        st.bar_chart(df[['日期',selected_column]].set_index('日期'))

        #選擇圖表類型
        chart_type=st.selectbox('選擇圖表類型',['折線圖','柱狀圖','散點圖'])
        if chart_type == '折線圖':
            st.line_chart(df[selected_column])
        elif chart_type == '柱狀圖':
            st.bar_chart(df[selected_column])
        elif chart_type == '散點圖':
            st.scatter_chart(df[selected_column])


if __name__ == '__main__':
    main()
