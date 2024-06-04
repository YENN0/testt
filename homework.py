import streamlit as st
import pandas as pd
import numpy as np

#Info.
st.set_page_config(
    page_title="資料分析期末",
    layout = "wide",
    menu_items={
        "About":"資料來源：[臺電官網](https://www.taipower.com.tw/tc/index.aspx)、[經濟部能源署](https://www.esist.org.tw/database/search?tab=%E9%9B%BB%E5%8A%9B%E7%B5%B1%E8%A8%88)",
    }
)

#Main
def main():
    st.title('臺灣能源現況')
    st.write('410971105 顏詠璇 資料分析期末')

    tab1, tab2 = st.tabs(["主介面", "臺灣能源政策目標"])

    with tab1:
        col_main1, col_main2 = st.columns(2)
        with col_main1:
            df_capa = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/capacity%20classification.csv')
            df_capa_show = df_capa.rename(columns={'年':'index'}).set_index('index')
            st.subheader('各機組發電量')
            col_capa1, col_capa2 = st.columns(2)
            with col_capa1:
                multiselected_columns = st.multiselect('選擇要顯示的列',df_capa_show.columns)
            with col_capa2:
                chart_type=st.selectbox('選擇圖表類型',['折線圖','柱狀圖'])
            
            if multiselected_columns:
                df_capa_selected = df_capa_show[multiselected_columns]
                if chart_type == '折線圖':
                    st.line_chart(df_capa_selected)
                elif chart_type == '柱狀圖':
                    st.bar_chart(df_capa_selected)
            else:
                if chart_type == '折線圖':
                    st.line_chart(df_capa_show)
                elif chart_type == '柱狀圖':
                    st.bar_chart(df_capa_show)
        with col_main2:
            df_department = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/DepartmentConsumption.csv')
            df_department_show = df_department.rename(columns={'年':'index'}).set_index('index')
            st.subheader('各部門用電占比')
            multi_department_columns = st.multiselect('選擇要顯示的列',df_department_show.columns)
            if multi_department_columns:
                df_department_selected = df_department_show[multi_department_columns]
                st.bar_chart(df_department_selected)
            else:
                st.bar_chart(df_department_show)

        col_main3, col_main4 = st.columns(2)
        with col_main3:
            st.subheader('各機組發電量')
            
        with col_main4:
            st.subheader('各部門用電狀況')
            department_columns = st.selectbox('選擇圖表類型',df_department_show.columns)
            df_cal_department=df_department
            df_cal_department['Difference'] = df_cal_department[department_columns].diff()
            df_cal_department = df_cal_department.dropna()
            st.write(df_cal_department)
            st.bar_chart(df_department_show[['年',"Difference"]].set_index('年'))
        
        #顯示數據
        show_raw= st.checkbox('顯示原始數據')

        if show_raw:
            col_caparaw1, col_caparaw2 = st.columns([2, 1])

            with col_caparaw1:
                sort_option= st.selectbox('排列方式',['年升序','年降序'])
                if sort_option == '年升序':
                    sored_data = df_capa.sort_values(by='年',ascending=True)
                else:
                    sored_data = df_capa.sort_values(by='年',ascending=False)

                st.write(sored_data)
            with col_caparaw2:
                st.write('數據統計摘要')
                st.write(df_capa.describe())
    with tab2:
        st.header("臺灣能源政策")
        with st.expander('前言'):
            st.write('111年3月公布「臺灣2050淨零排放路徑及策略總說明」')
            st.write('111年12月公布「12項關鍵戰略行動計畫」')
            st.write('112年1月核定「淨零排放路徑112-115年綱要計畫」，針對淨零碳排目標進行各面向的減緩與調適。')
            st.write('112年2月15日總統公布施行《氣候變遷因應法》，並納入2050年淨零排放目標、提升氣候治理層級、徵收碳費專款專用、增訂氣候變遷調適專章、納入碳足跡及產品標示管理機制')


if __name__ == '__main__':
    main()
