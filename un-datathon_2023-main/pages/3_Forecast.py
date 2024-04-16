import pandas as pd
import streamlit as st
import plotly.express as px
from utils import transformation as ts
from utils import machine_learning as ml


sta, stb, stc = st.columns(3)

with stb:
    stb.image('./images/un-datathon.png')


st.markdown('<h3 style=\'text-align:center;\'> Forecasting CO2 Emission in 2 Years </h3>',
            unsafe_allow_html=True)

df_europe = pd.read_excel('./dataset/list_europe.xlsx', engine='openpyxl')
dfs = pd.read_excel('./dataset/final_dataset.xlsx', engine='openpyxl')

df_final = dfs[dfs['country'].isin(df_europe['country'])]
col_data = ['country', 'year', 'oil_consumption', 'renewable_production', 'CO2_emission']

country_list = df_final['country'].unique()
fossil_list = df_final['commodity_transaction_x'].unique()
renew_list = df_final['commodity_transaction_y'].unique()

country = st.selectbox('Select the country:',
                       country_list)

fig = ml.arima(df_final, country, 'CO2_emission')

st.pyplot(fig)
