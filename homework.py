import streamlit as st
import pandas as pd

#工作列
st.set_page_config(
    page_title="資料分析期末",
    layout = "wide",
    initial_sidebar_state="auto",#auto:預設開，頁面縮小關, collapsed 預設關, expanded永久開
    menu_items={
        "About":"https://www.taipower.com.tw/tc/index.aspx",
    }
)


def main():
    st.title('臺灣能源現況')
    st.write('410971105 顏詠璇 資料分析期末')
    
    tab1, tab2 = st.tabs(["主介面", "臺灣能源政策目標"])

    with tab1:
        df = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/capacity%20classification.csv')

        #顯示數據
        st.write('原始數據')
        sored_data = df.sort_values(by='年',ascending=False)
        st.write(sored_data)
        #選擇顯示的欄位
        if df is not None:
            #日期區間選擇
            if '年' in df.columns:
                df['年'] = pd.to_datetime(df['年'])
                #設定區間
                min_date = df['年'].min().year()
                max_date = df['年'].max().year()

                #日期元件
                date_range = st.date_input('選擇年範圍',(min_date,max_date))
                start_date = pd.Timestamp(date_range[0])
                end_date = pd.Timestamp(date_range[1])

                filtered_df = df[(df['年']>=start_date)&df(['年']<=end_date)]

                st.write('篩選後的')
                st.write(filtered_df)

            show_summary= st.checkbox('顯示摘要')

            if show_summary:
                st.write('數據統計摘要')
                st.write(df.describe())
    with tab2:
        st.header("臺灣能源政策")
        with st.expander('前言'):
            st.write('111年3月公布「臺灣2050淨零排放路徑及策略總說明」')
            st.write('111年12月公布「12項關鍵戰略行動計畫」')
            st.write('112年1月核定「淨零排放路徑112-115年綱要計畫」，針對淨零碳排目標進行各面向的減緩與調適。')
            st.write('112年2月15日總統公布施行《氣候變遷因應法》，並納入2050年淨零排放目標、提升氣候治理層級、徵收碳費專款專用、增訂氣候變遷調適專章、納入碳足跡及產品標示管理機制')

    
'''
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
'''


if __name__ == '__main__':
    main()
