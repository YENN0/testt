import streamlit as st
import pandas as pd

def main():
    st.title('臺灣能源現況') #SHOW標題
    st.write('410971105 顏詠璇 資料分析期末')#普通文字
    
    name= st.text_input('請輸入文字:')#輸入互動元素
    if name: #將輸入文字顯示
        st.write(f'你好,{name}')
#上傳數據
    uploaded_file= st.file_uploader('上傳文件:CSV',type=['csv','xlsx'])#上傳檔案元件
    if uploaded_file is not None:
        file_extension= uploaded_file.name.split(".")[-1]
        if file_extension.lower()=='csv':
            df=pd.read_csv(uploaded_file)
        else:
            df=pd.read_excel(uploaded_file,engine='openpyxl')

    #顯示數據
    st.write('原始數據')
    st.write(df)
    #選擇欄位
    selected_column = st.selectbox('選擇要用在柱狀圖的列',['銷售金額','訂單數量'])
    #視覺化
    st.write('數據視覺化')
    st.bar_chart(df[['日期',selected_column]].set_index('日期'))

if __name__ == '__main__':
    main()
