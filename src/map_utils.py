"""
Utilitários para criação e manipulação de mapas com Folium.
"""
import folium
from folium import plugins
import pandas as pd
from typing import Optional, List, Dict, Any

from config import MAP_CONFIG, TIPOS_OCORRENCIA, STATUS_OCORRENCIA


def criar_mapa_base(
    center_lat: Optional[float] = None,
    center_lon: Optional[float] = None,
    zoom: int = None
) -> folium.Map:
    """
    Cria um mapa base configurado com tiles e controles.
    """
    lat = center_lat or MAP_CONFIG["center_lat"]
    lon = center_lon or MAP_CONFIG["center_lon"]
    zoom_level = zoom or MAP_CONFIG["zoom_start"]
    
    # Criar mapa com tile customizado
    mapa = folium.Map(
        location=[lat, lon],
        zoom_start=zoom_level,
        min_zoom=MAP_CONFIG["min_zoom"],
        max_zoom=MAP_CONFIG["max_zoom"],
        tiles=None
    )
    
    # Adicionar múltiplos tiles
    folium.TileLayer(
        tiles="CartoDB positron",
        name="Claro",
        attr="CartoDB"
    ).add_to(mapa)
    
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        name="Escuro",
        attr="CartoDB"
    ).add_to(mapa)
    
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Padrão",
        attr="OpenStreetMap"
    ).add_to(mapa)
    
    # Adicionar controle de camadas
    folium.LayerControl(position="topright").add_to(mapa)
    
    # Adicionar controle de tela cheia
    plugins.Fullscreen(
        position="topleft",
        title="Tela Cheia",
        title_cancel="Sair da Tela Cheia"
    ).add_to(mapa)
    
    # Adicionar localizador de posição
    plugins.LocateControl(
        position="topleft",
        strings={"title": "Minha Localização"}
    ).add_to(mapa)
    
    return mapa


def criar_icone_marcador(tipo: str, status: str = "Pendente") -> folium.Icon:
    """
    Cria um ícone personalizado baseado no tipo e status da ocorrência.
    """
    config_tipo = TIPOS_OCORRENCIA.get(tipo, TIPOS_OCORRENCIA["Outro"])
    
    # Definir cor baseada no status (prioridade ao status se resolvido)
    if status == "Resolvido":
        cor = "green"
    elif status == "Em Andamento":
        cor = "blue"
    else:
        # Mapear cores hex para nomes de cores do Folium
        cor_hex = config_tipo["cor"]
        cor_map = {
            "#e74c3c": "red",
            "#f39c12": "orange",
            "#27ae60": "green",
            "#3498db": "blue",
            "#9b59b6": "purple",
            "#1abc9c": "lightgreen",
            "#2d5016": "darkgreen",
            "#7f8c8d": "gray"
        }
        cor = cor_map.get(cor_hex, "blue")
    
    return folium.Icon(
        color=cor,
        icon=config_tipo["icone"],
        prefix="fa"
    )


def criar_popup_ocorrencia(row: pd.Series) -> folium.Popup:
    """
    Cria um popup HTML formatado para uma ocorrência.
    """
    tipo = row.get("tipo", row.get("tipo_ocorrencia", "Não informado"))
    descricao = row.get("descricao", "Sem descrição")
    bairro = row.get("bairro", "Não informado")
    data = row.get("data", "Não informada")
    status = row.get("status", "Pendente")
    prioridade = row.get("prioridade", "Média")
    votos = row.get("votos", 0)
    
    # Formatar data
    if pd.notna(data) and hasattr(data, 'strftime'):
        data_formatada = data.strftime("%d/%m/%Y")
    else:
        data_formatada = str(data) if pd.notna(data) else "Não informada"
    
    # Cores de status e prioridade
    status_config = STATUS_OCORRENCIA.get(status, {"cor": "#7f8c8d", "icone": "❓"})
    
    prioridade_cores = {
        "Baixa": "#27ae60",
        "Média": "#f39c12",
        "Alta": "#e67e22",
        "Crítica": "#e74c3c"
    }
    cor_prioridade = prioridade_cores.get(prioridade, "#7f8c8d")
    
    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; min-width: 250px; max-width: 300px;">
        <h4 style="margin: 0 0 10px 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;">
            {tipo}
        </h4>
        
        <p style="margin: 8px 0; color: #555; font-size: 13px;">
            {descricao}
        </p>
        
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
            <span style="background: #ecf0f1; padding: 3px 8px; border-radius: 12px; font-size: 11px;">
                📍 {bairro}
            </span>
            <span style="background: #ecf0f1; padding: 3px 8px; border-radius: 12px; font-size: 11px;">
                📅 {data_formatada}
            </span>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-top: 12px; padding-top: 10px; border-top: 1px solid #eee;">
            <span style="background: {status_config['cor']}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">
                {status_config['icone']} {status}
            </span>
            <span style="background: {cor_prioridade}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">
                ⚡ {prioridade}
            </span>
        </div>
        
        <div style="margin-top: 10px; text-align: center; color: #7f8c8d; font-size: 11px;">
            👍 {votos} apoios
        </div>
    </div>
    """
    
    return folium.Popup(html, max_width=320)


def adicionar_marcadores(
    mapa: folium.Map,
    df: pd.DataFrame,
    agrupar: bool = True
) -> folium.Map:
    """
    Adiciona marcadores de ocorrências ao mapa.
    
    Args:
        mapa: Mapa Folium base
        df: DataFrame com as ocorrências
        agrupar: Se True, agrupa marcadores próximos em clusters
    """
    if df.empty:
        return mapa
    
    # Criar grupo de marcadores (cluster ou não)
    if agrupar:
        marker_cluster = plugins.MarkerCluster(
            name="Ocorrências",
            options={
                "maxClusterRadius": 50,
                "spiderfyOnMaxZoom": True,
                "showCoverageOnHover": False,
                "zoomToBoundsOnClick": True
            }
        )
    else:
        marker_cluster = folium.FeatureGroup(name="Ocorrências")
    
    # Adicionar cada marcador
    for _, row in df.iterrows():
        lat = row.get("latitude")
        lon = row.get("longitude")
        
        if pd.isna(lat) or pd.isna(lon):
            continue
        
        tipo = row.get("tipo", row.get("tipo_ocorrencia", "Outro"))
        status = row.get("status", "Pendente")
        
        marcador = folium.Marker(
            location=[lat, lon],
            popup=criar_popup_ocorrencia(row),
            tooltip=f"{tipo} - {row.get('bairro', 'Local não informado')}",
            icon=criar_icone_marcador(tipo, status)
        )
        
        marcador.add_to(marker_cluster)
    
    marker_cluster.add_to(mapa)
    
    return mapa


def criar_mapa_calor(df: pd.DataFrame) -> folium.Map:
    """
    Cria um mapa de calor das ocorrências.
    """
    mapa = criar_mapa_base()
    
    if df.empty:
        return mapa
    
    # Preparar dados para heatmap
    heat_data = [
        [row["latitude"], row["longitude"]]
        for _, row in df.iterrows()
        if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude"))
    ]
    
    if heat_data:
        plugins.HeatMap(
            heat_data,
            name="Mapa de Calor",
            min_opacity=0.3,
            radius=25,
            blur=15,
            gradient={
                0.2: 'blue',
                0.4: 'lime',
                0.6: 'yellow',
                0.8: 'orange',
                1.0: 'red'
            }
        ).add_to(mapa)
    
    return mapa


def criar_mapa_seletor() -> folium.Map:
    """
    Cria um mapa para seleção de localização (usado no formulário de reporte).
    """
    mapa = criar_mapa_base()
    
    # Adicionar popup de lat/lng ao clicar
    mapa.add_child(folium.LatLngPopup())
    
    # Adicionar instruções
    folium.Marker(
        location=[MAP_CONFIG["center_lat"], MAP_CONFIG["center_lon"]],
        popup="Clique no mapa para selecionar a localização",
        icon=folium.Icon(color="gray", icon="info", prefix="fa")
    ).add_to(mapa)
    
    return mapa
