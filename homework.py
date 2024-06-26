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
            df_renew = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/RenewableEnergyinEachCity.csv')
            st.subheader('再生能源發電量')
            col_renewraw1, col_renewraw2 = st.columns([2, 1])
            with col_renewraw1:
                renewyear = st.slider("取得資料年份", 101, 113)
                
            with col_renewraw2:
                renewtype = st.selectbox('選擇再生能源類型',['風力','太陽光電','其他(含水力)'])

            df_log=df_renew[df_renew['年'] == renewyear]
            df_renewshow= df_log.loc[:,['縣市',renewtype]]

            Taiwan = {
                "縣市": ['基隆市', '台北市', '新北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣'],
                "經度": [121.627, 121.561, 121.447, 121.282, 120.979, 121.019, 120.933, 120.646, 120.479, 120.960, 120.431, 120.445,120.687,120.322,120.408,120.674,121.613,121.383,121.013,119.594,118.383,119.937],
                "緯度": [25.138 , 25.063 , 25.067 , 24.916 , 24.800 , 24.820 , 24.473 , 24.162 , 23.962 , 23.872 , 23.728 , 23.485 ,23.446,23.161 ,22.745 ,22.473 ,24.552 ,23.778 ,22.903 ,23.568 ,24.465 ,26.154],
            }
            df_tw = pd.DataFrame(Taiwan)
            df_merged = pd.merge(df_renewshow, df_tw, on='縣市', how='inner')
            
            df_merged['scaled_sizes'] = df_merged[renewtype] / 50
            st.map(df_merged,
                latitude='緯度',
                longitude='經度',
                size= 'scaled_sizes'
            )
            
        col_main3, col_main4 = st.columns(2)
        with col_main3:
            df_department = pd.read_csv('https://raw.githubusercontent.com/YENN0/testt/main/DepartmentConsumption.csv')
            df_department_show = df_department.rename(columns={'年':'index'}).set_index('index')
            st.subheader('各部門用電占比')
            multi_department_columns = st.multiselect('選擇要顯示的列',df_department_show.columns)
            if multi_department_columns:
                df_department_selected = df_department_show[multi_department_columns]
                st.bar_chart(df_department_selected)
            else:
                st.bar_chart(df_department_show)
            
        with col_main4:
            st.subheader('各部門用電狀況年增減')
            department_columns = st.selectbox('選擇部門',df_department_show.columns)
            df_cal_department=df_department
            df_cal_department['Difference'] = df_cal_department[department_columns].diff()
            df_cal_department = df_cal_department.dropna()
            df_cal_department = df_cal_department.drop(df_cal_department.index[-1])
            df_cal_department_selected = df_cal_department['Difference']
            st.bar_chart(df_cal_department_selected)
            
        
        #顯示數據
        show_raw= st.checkbox('顯示原始數據')
        if show_raw:
            choose_option= st.selectbox('觀察表格',['各機組發電量','各部門用電','再生能源發電量'])
            
            col_caparaw1, col_caparaw2 = st.columns([2, 1])
            if choose_option=='各機組發電量':
                choose_data=df_capa
            elif choose_option=='各部門用電':
                choose_data=df_department
            elif choose_option=='再生能源發電量':
                choose_data=df_renew

            with col_caparaw1:
                sort_option= st.selectbox('排列方式',['年升序','年降序'])
                if sort_option == '年升序':
                    sored_data = choose_data.sort_values(by='年',ascending=True)
                else:
                    sored_data = choose_data.sort_values(by='年',ascending=False)

                st.write(sored_data)
            with col_caparaw2:
                st.write('數據統計摘要')
                st.write(choose_data.describe())
    with tab2:
        st.header("臺灣能源政策")
        with st.expander('前言'):
            st.write('111年3月公布「臺灣2050淨零排放路徑及策略總說明」')
            st.write('111年12月公布「12項關鍵戰略行動計畫」')
            st.write('112年1月核定「淨零排放路徑112-115年綱要計畫」，針對淨零碳排目標進行各面向的減緩與調適。')
            st.write('112年2月15日總統公布施行《氣候變遷因應法》，並納入2050年淨零排放目標、提升氣候治理層級、徵收碳費專款專用、增訂氣候變遷調適專章、納入碳足跡及產品標示管理機制')
        st.subheader('展綠：經濟部訂定2025年再生能源發電占比20％政策目標。')
        st.write('現正積極推動太陽光電及風力發電，預計2025年太陽光電裝置容量達20GW，離岸風力裝置容量則達5.7GW以上。')
        st.subheader('增氣：天然氣發電占比將達50%')
        st.write('臺灣2018年增訂天然氣安全存量，逐步提高自備儲槽容積及安全存量。現行儲槽容積天數至少為15天，安全存量天數至少為7天，2027年儲槽容積天數至少為24天，安全存量天數至少為14天。')
        st.subheader('減煤：2025年前未規劃新擴建任何燃煤機組')
        st.write('燃煤機組除役後，改建為燃氣機組。')

if __name__ == '__main__':
    main()
