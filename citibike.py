import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="Citibike NYC",
                page_icon=":bike:",
                layout="wide")


st.title('Cicle Rides in NYC')

DATA_URL='citibike-tripdata.csv'

df_rows=st.sidebar.checkbox('Show raw data')

@st.cache
def load_data(nrows):
    data=pd.read_csv(DATA_URL, nrows=nrows)
    return data

if (df_rows):
    data_load_state=st.text('Loading...')
    data=load_data(1000)
    data_load_state.text('Done.. using @st.cache')
    st.dataframe(data)

df = pd.read_csv('citibike-tripdata.csv')
df = df.rename(columns={"start_lat": "lat", "start_lng": "lon"})

df['started_at']=pd.to_datetime(df['started_at'])

df['hour'] = df['started_at'].dt.strftime('%H')
horas=df['hour'].value_counts()
horas=pd.DataFrame(horas)
horas=horas.reset_index()
horas=horas.rename(columns={'index':'hour','hour':'count'})
horas=horas.sort_values(by='hour')

hora_recorrido=st.sidebar.checkbox('Recorridos por hora')

if (hora_recorrido):
    fig = px.bar(horas, x='hour', y='count')
    st.plotly_chart(fig)

df['hour']=df['hour'].astype('int64')

horario_mapa=st.sidebar.slider(
    'Selecciona el horario',
    min_value=int(df['hour'].min()),
    max_value=int(df['hour'].max()),
)

subset=df[(df['hour'] == horario_mapa)]

datos_mapa=subset[['lat','lon']]

st.map(datos_mapa)