import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Caminho base do projeto (um nível acima da pasta src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho completo do CSV
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "ocorrencias_mock.csv")

st.write("Lendo arquivo:", CSV_PATH)   # debug opcional

df = pd.read_csv(CSV_PATH, encoding="latin1")

st.title("Mapa Digital Urbano – Ocorrências")

# Criar mapa centralizado
m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=13)

# Plotar pontos
for _, row in df.iterrows():
    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=f"{row.get('tipo', 'Sem tipo')} - {row.get('descricao', 'Sem descrição')}"
    ).add_to(m)

st_folium(m, width=900, height=600)
