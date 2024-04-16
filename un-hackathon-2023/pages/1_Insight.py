import pandas as pd
import streamlit as st
from utils import geospatial as gs
from utils import transformation as ts
import plotly.express as px


sta, stb, stc = st.columns(3)

with stb:
    stb.image('./images/un-datathon.png')

st.markdown('<h3 style=\'text-align:center;\'> CO2 Emission Based on Fossil Fuel and Renewable Energy Consumption </h3>',
            unsafe_allow_html=True)

df_europe = pd.read_excel('./dataset/list_europe.xlsx', engine='openpyxl')
dfs = pd.read_excel('./dataset/final_dataset.xlsx', engine='openpyxl')

df_final = dfs[dfs['country'].isin(df_europe['country'])]
col_data = ['country', 'year', 'oil_consumption', 'renewable_production', 'CO2_emission']

country_list = df_final['country'].unique()
year_list = df_final['year'].unique()
fossil_list = df_final['commodity_transaction_x'].unique()
renew_list = df_final['commodity_transaction_y'].unique()

df_map = df_final[col_data].groupby(by=['country', 'year']).sum()
df_map_final = ts.transform_data(df_map, df_final)

st8, st9 = st.columns(2)
with st8:
    add_commodity = st8.selectbox('Select the commodity:',
                                  ['oil_consumption', 'renewable_production'])
with st9:
    add_year = st9.selectbox('Select the year:',
                             year_list)

st10, st11 = st.columns(2)
with st10:
    fig1 = gs.get_plotly_map(df_map_final[df_map_final['year'] == add_year],
                             df_final,
                             add_commodity,
                             'Distribution ' + ''.join(add_commodity.replace('_', ' ')).title())
    st10.plotly_chart(fig1,
                      theme='streamlit',
                      use_container_width=True)

with st11:
    fig2 = gs.get_plotly_map(df_map_final[df_map_final['year'] == add_year],
                             df_final,
                             'CO2_emission',
                             'Distribution CO2 Level')
    st11.plotly_chart(fig2,
                      theme='streamlit',
                      use_container_width=True)

st.markdown('<h5 style=\'text-align:center;\'> Histogram CO2 Emission by Country (Top Five) </h5>',
            unsafe_allow_html=True)

df_hist = df_map_final[df_map_final['year'] == add_year].sort_values(by=['CO2_emission']).head()
fig3 = px.bar(df_hist, x='country', y='CO2_emission')
st.plotly_chart(fig3,
                theme='streamlit',
                use_container_width=True)

st.markdown('<h5 style=\'text-align:center;\'> Line Chart Oil Consumption, Electricity Production, and CO2 Emission by Country </h5>',
            unsafe_allow_html=True)

df_line = df_final[col_data].groupby(by=['country', 'year']).sum()
country = st.selectbox('Select the country:',
                       country_list)
df_lines = ts.transpose_data(df_line)
fig4 = px.line(df_lines[df_lines['country'] == country],
               x='year', y='value',
               color='commodity',
               markers=True)

st.plotly_chart(fig4,
                theme='streamlit',
                use_container_width=True)
