import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import holoviews as hv
import hvplot.pandas
import re

sns.set_theme(style="whitegrid")  

st.set_page_config(page_title="Tablero ENMA", layout="wide")

@st.cache_data  
def load_data():
    df_2023 = pd.read_csv('data/raw/ENMA_2023.csv',sep=";")
    df_2020 = pd.read_csv('data/raw/ENMA_2020.csv',sep=";")
    return df_2023, df_2020

df_2020, df_2023 = load_data()

conteo = pd.DataFrame({
    'Año': ['2020', '2023'],
    'Registros': [len(df_2020), len(df_2023)]
})

fig = px.bar(
    conteo,
    x='Año',
    y='Registros',
    text='Registros',
    title='Cantidad de registros por año',
    color='Año',
    color_discrete_sequence=['#636EFA', '#EF553B']
)

fig.update_traces(textposition='outside')
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

st.title("Encuesta Nacional de Migrantes Argentina (ENMA)")
st.write("Comparativa 2020 vs 2023")