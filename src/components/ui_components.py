"""
Componentes de UI reutilizáveis para Streamlit.
"""
import streamlit as st
from typing import Optional, Any
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import APP_CONFIG, TIPOS_OCORRENCIA, STATUS_OCORRENCIA, PRIORIDADES


def aplicar_estilos_customizados():
    """Aplica estilos CSS customizados à aplicação."""
    st.markdown("""
    <style>
        /* Importar fontes */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        /* Reset e base */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Header customizado */
        .main-header {
            background: linear-gradient(135deg, #1e3a5f 0%, #0d7377 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            margin: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            font-size: 0.95rem;
        }
        
        /* Cards de KPI */
        .kpi-card {
            background: white;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #3498db;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .kpi-card .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
            margin: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .kpi-card .kpi-label {
            color: #7f8c8d;
            font-size: 0.85rem;
            margin-top: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .kpi-card .kpi-delta {
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        
        .kpi-delta.positive { color: #27ae60; }
        .kpi-delta.negative { color: #e74c3c; }
        
        /* Badges */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .tipo-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.35rem 0.85rem;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        /* Sidebar customizada */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3a5f 0%, #14293d 100%);
        }
        
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.2);
        }
        
        /* Botões */
        .stButton > button {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2980b9 0%, #1f6391 100%);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        
        /* Form inputs */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
        }
        
        /* Alerts */
        .stAlert {
            border-radius: 10px;
        }
        
        /* Success message */
        .success-message {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        /* Animações */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.3s ease-out;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renderiza o header principal da aplicação."""
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_CONFIG['titulo']}</h1>
        <p>{APP_CONFIG['subtitulo']} • v{APP_CONFIG['versao']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Renderiza a sidebar com navegação."""
    with st.sidebar:
        st.markdown("## 🧭 Navegação")
        st.markdown("---")
        
        pagina = st.radio(
            "Ir para:",
            ["🗺️ Mapa Interativo", "📣 Reportar Problema", "📊 Dashboard", "ℹ️ Sobre"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Info rápida
        st.markdown("### 📈 Resumo Rápido")
        
        return pagina


def render_kpi_card(
    valor: Any,
    label: str,
    cor: str = "#3498db",
    delta: Optional[str] = None,
    delta_positivo: bool = True
):
    """
    Renderiza um card de KPI estilizado.
    
    Args:
        valor: Valor principal a exibir
        label: Rótulo descritivo
        cor: Cor da borda lateral
        delta: Texto de variação (opcional)
        delta_positivo: Se a variação é positiva
    """
    delta_html = ""
    if delta:
        delta_class = "positive" if delta_positivo else "negative"
        delta_icon = "↑" if delta_positivo else "↓"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {delta}</div>'
    
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {cor};">
        <div class="kpi-value">{valor}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_status_badge(status: str) -> str:
    """Retorna HTML de um badge de status."""
    config = STATUS_OCORRENCIA.get(status, {"cor": "#7f8c8d", "icone": "❓"})
    return f"""
    <span class="status-badge" style="background-color: {config['cor']}; color: white;">
        {config['icone']} {status}
    </span>
    """


def render_tipo_badge(tipo: str) -> str:
    """Retorna HTML de um badge de tipo de ocorrência."""
    config = TIPOS_OCORRENCIA.get(tipo, TIPOS_OCORRENCIA["Outro"])
    return f"""
    <span class="tipo-badge" style="background-color: {config['cor']}20; color: {config['cor']}; border: 1px solid {config['cor']}40;">
        <i class="fa fa-{config['icone']}"></i> {tipo}
    </span>
    """

