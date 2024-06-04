import streamlit as st
import pandas as pd

#工作列
st.set_page_config(
    page_title="資料分析期末",
    layout = "wide",
    menu_items={
        "About":"資料來源：[臺電官網](https://www.taipower.com.tw/tc/index.aspx)",
        #"About":"https://www.taipower.com.tw/tc/index.aspx",
    }
)


def main():
    st.title('臺灣能源現況')
    st.write('410971105 顏詠璇 資料分析期末')
    
    tab1, tab2 = st.tabs(["主介面", "臺灣能源政策目標"])

    with tab1:
        df = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/capacity%20classification.csv')
        dfshow = df.rename(columns={'年':'index'}).set_index('index')
        st.subheader('裝置容量結構')
        col1a, col2a = st.columns(2)
        with col1a:
            multiselected_columns = st.multiselect('選擇要顯示的列',dfshow.columns)
        with col2a:
             chart_type=st.selectbox('選擇圖表類型',['折線圖','柱狀圖'])
        
        if multiselected_columns:
            df_selected = dfshow[multiselected_columns]
            if chart_type == '折線圖':
                st.line_chart(df_selected)
            elif chart_type == '柱狀圖':
                st.bar_chart(df_selected)
        else:
            if chart_type == '折線圖':
                st.line_chart(dfshow)
            elif chart_type == '柱狀圖':
                st.bar_chart(dfshow)
        
        #顯示數據
        show_raw= st.checkbox('顯示原始數據')

        if show_raw:
            col1b, col2b = st.columns([2, 1])

            with col1b:
                sort_option= st.selectbox('排列方式',['年升序','年降序'])
                if sort_option == '年升序':
                    sored_data = df.sort_values(by='年',ascending=True)
                else:
                    sored_data = df.sort_values(by='年',ascending=False)

                st.write(sored_data)
            with col2b:
                st.write('數據統計摘要')
                st.write(df.describe())
    with tab2:
        st.header("臺灣能源政策")
        with st.expander('前言'):
            st.write('111年3月公布「臺灣2050淨零排放路徑及策略總說明」')
            st.write('111年12月公布「12項關鍵戰略行動計畫」')
            st.write('112年1月核定「淨零排放路徑112-115年綱要計畫」，針對淨零碳排目標進行各面向的減緩與調適。')
            st.write('112年2月15日總統公布施行《氣候變遷因應法》，並納入2050年淨零排放目標、提升氣候治理層級、徵收碳費專款專用、增訂氣候變遷調適專章、納入碳足跡及產品標示管理機制')


if __name__ == '__main__':
    main()
