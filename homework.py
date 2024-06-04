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

        show_summary= st.checkbos('顯示摘要')

        if show_summary:
            st.write('數據統計摘要')
            st.write(df.describe())

        multiselected_columns = st.multiselect('選擇要顯示的列',df.columns)

        if multiselected_columns:
            st.write('已選擇')
            st,write(df[multiselected_columns])

        #單一選擇欄位
        selected_column = st.selectbox('選擇要用在柱狀圖的列',['銷售金額','訂單數量'])

        #視覺化
        st.write('數據視覺化')
        st.bar_chart(df[['日期',selected_column]].set_index('日期'))

if __name__ == '__main__':
    main()
