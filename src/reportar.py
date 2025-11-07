import streamlit as st
import os
import json
from datetime import datetime
import folium
from streamlit_folium import st_folium

DATA_DIR = "../data/raw"
REPORTES_PATH = os.path.join(DATA_DIR, "reportes.json")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

os.makedirs(IMAGES_DIR, exist_ok=True)

def salvar_reporte(reporte):
    if os.path.exists(REPORTES_PATH):
        with open(REPORTES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(reporte)

    with open(REPORTES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    st.title("📣 Reportar Problema Urbano")

    st.markdown("Clique no mapa para marcar o local do problema.")

    m = folium.Map(location=[-23.55, -46.63], zoom_start=12)
    m.add_child(folium.LatLngPopup())

    output = st_folium(m, height=500)

    lat = None
    lon = None

    if output and output["last_clicked"]:
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]

        st.success(f"Local selecionado: {lat:.6f}, {lon:.6f}")

    tipo = st.selectbox("Tipo do problema:", [
        "Buraco na rua",
        "Iluminação pública",
        "Árvore caída",
        "Lixo / entulho",
        "Sinalização danificada",
        "Outro"
    ])

    descricao = st.text_area("Descrição:")

    fotos = st.file_uploader("Enviar fotos (opcional)", accept_multiple_files=True)

    if st.button("Enviar"):
        if lat is None or lon is None:
            st.error("Você deve clicar no mapa para selecionar o local!")
            return

        id_reporte = datetime.now().strftime("%Y%m%d%H%M%S")

        foto_dir = os.path.join(IMAGES_DIR, id_reporte)
        os.makedirs(foto_dir, exist_ok=True)

        paths_fotos = []
        for f in fotos or []:
            file_path = os.path.join(foto_dir, f.name)
            with open(file_path, "wb") as img:
                img.write(f.getbuffer())
            paths_fotos.append(file_path)

        reporte = {
            "id": id_reporte,
            "tipo": tipo,
            "descricao": descricao,
            "latitude": lat,
            "longitude": lon,
            "fotos": paths_fotos,
            "data_envio": datetime.now().isoformat()
        }

        salvar_reporte(reporte)
        st.success("Ocorrência enviada com sucesso!")
