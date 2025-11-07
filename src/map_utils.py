import folium

def gerar_mapa(df, latitude_padrao=-11.4400, longitude_padrao=-61.4600, zoom=13):
    """
    Gera um mapa Folium com base no DataFrame de ocorrências.
    """

    # Cria o mapa centralizado em Cacoal
    mapa = folium.Map(location=[latitude_padrao, longitude_padrao], zoom_start=zoom)

    # Adiciona marcadores
    for _, linha in df.iterrows():
        folium.Marker(
            location=[linha["latitude"], linha["longitude"]],
            popup=f"{linha['tipo_problema']} - {linha['descricao']}",
            tooltip=linha["tipo_problema"]
        ).add_to(mapa)

    return mapa
