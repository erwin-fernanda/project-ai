import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import pycountry as pc
from utils import geospatial as gs
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from streamlit_folium import st_folium


sta, stb, stc = st.columns(3)

with stb:
    stb.image('./images/un-datathon.png')

st.markdown('<h3 style=\'text-align:center;\'> Overview of CO2 Emission based on Fossil Fuel and Renewable Energy Production Data </h3>',
            unsafe_allow_html=True)
