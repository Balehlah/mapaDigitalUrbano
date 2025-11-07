import streamlit as st
import reportar
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="Mapa Digital Urbano", layout="wide")

# ------------------- MENU -------------------
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Mapa", "Reportar Problema"])


# ------------------- PÁGINA MAPA -------------------
if pagina == "Mapa":

    st.title("Mapa de Ocorrências Urbanas")

    # Caminho correto do CSV
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "ocorrencias_mock.csv")

    df = pd.read_csv(CSV_PATH, encoding="latin1")

    # Criar mapa centralizado nos dados
    m = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=13
    )

    # Adicionar marcadores
    for _, row in df.iterrows():
        tipo = row.get("tipo_ocorrencia", "Sem tipo")
        descricao = row.get("descricao", "Sem descrição")
        bairro = row.get("bairro", "Sem bairro")
        data = row.get("data", "Sem data")

        popup_text = f"""
        <b>Tipo:</b> {tipo}<br>
        <b>Descrição:</b> {descricao}<br>
        <b>Bairro:</b> {bairro}<br>
        <b>Data:</b> {data}
        """

        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=popup_text,
            tooltip=tipo
        ).add_to(m)

    st_folium(m, width=900, height=600)


# ------------------- PÁGINA REPORTAR -------------------
elif pagina == "Reportar Problema":
    reportar.main()
