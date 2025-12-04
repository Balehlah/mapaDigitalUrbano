"""
Página do Mapa Interativo com filtros e visualização de ocorrências.
"""
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import data_manager
from map_utils import criar_mapa_base, adicionar_marcadores, criar_mapa_calor
from config import TIPOS_OCORRENCIA, STATUS_OCORRENCIA, BAIRROS, PRIORIDADES


def render():
    """Renderiza a página do mapa interativo."""
    
    st.markdown("## 🗺️ Mapa de Ocorrências")
    st.markdown("Visualize todos os problemas reportados pela comunidade em tempo real.")
    
    # Carregar dados
    df = data_manager.carregar_todas_ocorrencias()
    
    if df.empty:
        st.warning("📭 Nenhuma ocorrência registrada ainda. Seja o primeiro a reportar!")
        return
    
    # ================== FILTROS ==================
    with st.expander("🔍 Filtros", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Filtro por tipo
            tipos_disponiveis = ["Todos"] + sorted(df["tipo"].dropna().unique().tolist())
            tipo_selecionado = st.selectbox(
                "Tipo de Ocorrência",
                tipos_disponiveis,
                index=0
            )
        
        with col2:
            # Filtro por status
            status_disponiveis = ["Todos"] + list(STATUS_OCORRENCIA.keys())
            status_selecionado = st.selectbox(
                "Status",
                status_disponiveis,
                index=0
            )
        
        with col3:
            # Filtro por bairro
            bairros_disponiveis = ["Todos"] + sorted(df["bairro"].dropna().unique().tolist())
            bairro_selecionado = st.selectbox(
                "Bairro",
                bairros_disponiveis,
                index=0
            )
        
        with col4:
            # Filtro por prioridade
            prioridades_disponiveis = ["Todas"] + list(PRIORIDADES.keys())
            prioridade_selecionada = st.selectbox(
                "Prioridade",
                prioridades_disponiveis,
                index=0
            )
    
    # ================== APLICAR FILTROS ==================
    df_filtrado = df.copy()
    
    if tipo_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_selecionado]
    
    if status_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["status"] == status_selecionado]
    
    if bairro_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["bairro"] == bairro_selecionado]
    
    if prioridade_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["prioridade"] == prioridade_selecionada]
    
    # ================== MÉTRICAS RÁPIDAS ==================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Exibido",
            len(df_filtrado),
            delta=f"de {len(df)} total"
        )
    
    with col2:
        pendentes = len(df_filtrado[df_filtrado["status"] == "Pendente"])
        st.metric("Pendentes", pendentes)
    
    with col3:
        em_andamento = len(df_filtrado[df_filtrado["status"] == "Em Andamento"])
        st.metric("Em Andamento", em_andamento)
    
    with col4:
        resolvidos = len(df_filtrado[df_filtrado["status"] == "Resolvido"])
        st.metric("Resolvidos", resolvidos)
    
    st.markdown("---")
    
    # ================== TABS DE VISUALIZAÇÃO ==================
    tab_marcadores, tab_calor = st.tabs(["📍 Marcadores", "🔥 Mapa de Calor"])
    
    with tab_marcadores:
        # Opções de visualização
        col1, col2 = st.columns([3, 1])
        with col2:
            agrupar = st.checkbox("Agrupar marcadores próximos", value=True)
        
        # Criar e exibir mapa
        if not df_filtrado.empty:
            # Centralizar no centro dos dados filtrados
            center_lat = df_filtrado["latitude"].mean()
            center_lon = df_filtrado["longitude"].mean()
            
            mapa = criar_mapa_base(center_lat=center_lat, center_lon=center_lon)
            mapa = adicionar_marcadores(mapa, df_filtrado, agrupar=agrupar)
            
            st_folium(mapa, width=None, height=550, use_container_width=True)
        else:
            st.info("Nenhuma ocorrência corresponde aos filtros selecionados.")
    
    with tab_calor:
        st.markdown("#### Concentracao de Ocorrencias")
        st.markdown("Areas em **vermelho** indicam maior concentracao de problemas. Areas em **azul** indicam menor concentracao.")
        
        if not df_filtrado.empty:
            # Centralizar no centro dos dados filtrados
            center_lat = df_filtrado["latitude"].mean()
            center_lon = df_filtrado["longitude"].mean()
            
            mapa_calor = criar_mapa_calor(df_filtrado, center_lat=center_lat, center_lon=center_lon)
            st_folium(mapa_calor, width=None, height=550, use_container_width=True, key="mapa_calor")
            
            # Legenda
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem;">
                <span style="display: flex; align-items: center; gap: 0.3rem;">
                    <span style="width: 20px; height: 12px; background: linear-gradient(to right, blue, cyan); border-radius: 2px;"></span>
                    Baixa
                </span>
                <span style="display: flex; align-items: center; gap: 0.3rem;">
                    <span style="width: 20px; height: 12px; background: linear-gradient(to right, lime, yellow); border-radius: 2px;"></span>
                    Media
                </span>
                <span style="display: flex; align-items: center; gap: 0.3rem;">
                    <span style="width: 20px; height: 12px; background: linear-gradient(to right, orange, red); border-radius: 2px;"></span>
                    Alta
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma ocorrencia corresponde aos filtros selecionados.")
    
    # ================== LISTA DE OCORRÊNCIAS ==================
    st.markdown("---")
    st.markdown("### 📋 Lista de Ocorrências")
    
    if not df_filtrado.empty:
        # Preparar dados para exibição
        colunas_exibir = ["tipo", "descricao", "bairro", "status", "prioridade", "data"]
        colunas_existentes = [c for c in colunas_exibir if c in df_filtrado.columns]
        
        df_exibir = df_filtrado[colunas_existentes].copy()
        
        # Renomear colunas para exibição
        rename_map = {
            "tipo": "Tipo",
            "descricao": "Descrição",
            "bairro": "Bairro",
            "status": "Status",
            "prioridade": "Prioridade",
            "data": "Data"
        }
        df_exibir = df_exibir.rename(columns=rename_map)
        
        # Formatar data
        if "Data" in df_exibir.columns:
            df_exibir["Data"] = pd.to_datetime(df_exibir["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
        
        # Limitar descrição
        if "Descrição" in df_exibir.columns:
            df_exibir["Descrição"] = df_exibir["Descrição"].str[:80] + "..."
        
        st.dataframe(
            df_exibir,
            use_container_width=True,
            hide_index=True,
            height=300
        )
        
        # Download dos dados
        col1, col2, col3 = st.columns([2, 1, 1])
        with col3:
            csv = df_filtrado.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                "📥 Exportar CSV",
                csv,
                "ocorrencias_filtradas.csv",
                "text/csv",
                use_container_width=True
            )
    else:
        st.info("Nenhuma ocorrência para exibir.")





