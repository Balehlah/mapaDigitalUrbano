"""
Mapa Digital Urbano - Aplicação Principal
Plataforma Comunitária de Infraestrutura Urbana

Autor: Comunidade de Cacoal
Versão: 2.0.0
"""
import streamlit as st
import sys
from pathlib import Path

# Configurar path para imports locais
SRC_DIR = Path(__file__).parent
sys.path.insert(0, str(SRC_DIR))

# Imports locais
from config import APP_CONFIG
from components.ui_components import aplicar_estilos_customizados, render_header
from data_manager import data_manager

# Imports das views (páginas)
from views import mapa, reportar, dashboard, sobre, admin

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title=APP_CONFIG["titulo"],
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": f"""
        ## {APP_CONFIG['titulo']}
        
        {APP_CONFIG['subtitulo']}
        
        **Versão:** {APP_CONFIG['versao']}
        
        Plataforma colaborativa para mapeamento de problemas urbanos.
        """
    }
)

# ==================== APLICAR ESTILOS ====================
aplicar_estilos_customizados()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">🗺️</h1>
        <h3 style="margin: 0.5rem 0; color: white;">Mapa Digital</h3>
        <p style="margin: 0; opacity: 0.8; font-size: 0.85rem; color: white;">Urbano</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação
    pagina = st.radio(
        "Navegação",
        ["🗺️ Mapa Interativo", "📣 Reportar Problema", "📊 Dashboard", "ℹ️ Sobre", "🔐 Admin"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Resumo rápido
    stats = data_manager.obter_estatisticas()
    
    st.markdown("### 📈 Resumo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", stats["total"])
    with col2:
        pendentes = stats["por_status"].get("Pendente", 0)
        st.metric("Pendentes", pendentes)
    
    # Taxa de resolução
    if stats["total"] > 0:
        st.markdown("**Taxa de Resolução**")
        st.progress(stats["taxa_resolucao"] / 100)
        st.caption(f"{stats['taxa_resolucao']:.1f}% resolvidos")
    
    st.markdown("---")
    
    # Filtro rápido por tipo
    st.markdown("### 🏷️ Por Tipo")
    if stats["por_tipo"]:
        for tipo, qtd in sorted(stats["por_tipo"].items(), key=lambda x: -x[1])[:5]:
            st.markdown(f"- {tipo}: **{qtd}**")
    else:
        st.caption("Nenhum dado ainda")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; opacity: 0.7; font-size: 0.75rem; color: white;">
        v{APP_CONFIG['versao']}<br>
        © 2025 Comunidade
    </div>
    """, unsafe_allow_html=True)

# ==================== CONTEÚDO PRINCIPAL ====================

# Header principal
render_header()

# Renderizar página selecionada
if pagina == "🗺️ Mapa Interativo":
    mapa.render()
    
elif pagina == "📣 Reportar Problema":
    reportar.render()
    
elif pagina == "📊 Dashboard":
    dashboard.render()
    
elif pagina == "ℹ️ Sobre":
    sobre.render()
    
elif pagina == "🔐 Admin":
    admin.render()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.85rem; padding: 1rem 0;">
    <strong>🗺️ Mapa Digital Urbano</strong> • 
    Plataforma Comunitária de Infraestrutura • 
    Feito com ❤️ para a comunidade
</div>
""", unsafe_allow_html=True)
