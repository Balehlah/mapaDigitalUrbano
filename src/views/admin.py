"""
Painel Administrativo - Gestao de Ocorrencias
Acesso restrito ao administrador
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import base64

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import data_manager
from config import TIPOS_OCORRENCIA, STATUS_OCORRENCIA, PRIORIDADES, IMAGES_DIR

# Credenciais do administrador
ADMIN_USER = "admin"
ADMIN_PASS = "mapa2025"


def verificar_login():
    """Verifica se o usuario esta logado."""
    return st.session_state.get("admin_logado", False)


def fazer_logout():
    """Realiza o logout do administrador."""
    st.session_state["admin_logado"] = False
    st.rerun()


def tela_login():
    """Renderiza a tela de login."""
    st.markdown("## 🔐 Acesso Administrativo")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e3a5f 0%, #0d7377 100%);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h2 style="color: white; margin: 0;">🛡️ Area Restrita</h2>
            <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
                Acesso exclusivo para administradores
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login"):
            usuario = st.text_input("Usuario", placeholder="Digite seu usuario")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            submitted = st.form_submit_button("🔓 Entrar", use_container_width=True, type="primary")
            
            if submitted:
                if usuario == ADMIN_USER and senha == ADMIN_PASS:
                    st.session_state["admin_logado"] = True
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Usuario ou senha incorretos!")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #7f8c8d; font-size: 0.85rem;">
            <p>⚠️ Este painel e exclusivo para gestores autorizados</p>
        </div>
        """, unsafe_allow_html=True)


def carregar_imagem_base64(caminho):
    """Carrega uma imagem e retorna em base64 para exibicao."""
    try:
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None


def painel_administrativo():
    """Renderiza o painel administrativo completo."""
    
    # Header com logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 🛠️ Painel Administrativo")
    with col2:
        if st.button("🚪 Sair", use_container_width=True):
            fazer_logout()
    
    st.markdown("Gerencie todas as ocorrencias reportadas pela comunidade.")
    st.markdown("---")
    
    # Carregar dados
    df = data_manager.carregar_todas_ocorrencias()
    reportes = data_manager._carregar_reportes()
    
    if df.empty:
        st.warning("📭 Nenhuma ocorrencia registrada ainda.")
        return
    
    # ================== METRICAS ==================
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total", len(df))
    with col2:
        pendentes = len(df[df["status"] == "Pendente"])
        st.metric("Pendentes", pendentes)
    with col3:
        em_analise = len(df[df["status"] == "Em Analise"])
        st.metric("Em Analise", em_analise)
    with col4:
        em_andamento = len(df[df["status"] == "Em Andamento"])
        st.metric("Em Andamento", em_andamento)
    with col5:
        resolvidos = len(df[df["status"] == "Resolvido"])
        st.metric("Resolvidos", resolvidos)
    
    st.markdown("---")
    
    # ================== FILTROS ==================
    st.markdown("### 🔍 Filtrar Ocorrencias")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Pendente", "Em Analise", "Em Andamento", "Resolvido", "Arquivado"]
        )
    with col2:
        filtro_tipo = st.selectbox(
            "Tipo",
            ["Todos"] + list(TIPOS_OCORRENCIA.keys())
        )
    with col3:
        filtro_prioridade = st.selectbox(
            "Prioridade",
            ["Todas", "Critica", "Alta", "Media", "Baixa"]
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]
    if filtro_tipo != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
    if filtro_prioridade != "Todas":
        df_filtrado = df_filtrado[df_filtrado["prioridade"] == filtro_prioridade]
    
    st.markdown(f"**{len(df_filtrado)}** ocorrencias encontradas")
    st.markdown("---")
    
    # ================== LISTA DE OCORRENCIAS ==================
    st.markdown("### 📋 Ocorrencias")
    
    if df_filtrado.empty:
        st.info("Nenhuma ocorrencia com os filtros selecionados.")
        return
    
    # Ordenar por data (mais recentes primeiro) e prioridade
    prioridade_ordem = {"Critica": 0, "Alta": 1, "Media": 2, "Baixa": 3}
    df_filtrado["prioridade_ordem"] = df_filtrado["prioridade"].map(prioridade_ordem).fillna(4)
    df_filtrado = df_filtrado.sort_values(["prioridade_ordem", "data"], ascending=[True, False])
    
    # Exibir cada ocorrencia em um expander
    for idx, row in df_filtrado.iterrows():
        # Definir cor do status
        status = row.get("status", "Pendente")
        status_config = STATUS_OCORRENCIA.get(status, {"cor": "#7f8c8d", "icone": "❓"})
        
        # Definir cor da prioridade
        prioridade = row.get("prioridade", "Media")
        prioridade_config = PRIORIDADES.get(prioridade, {"cor": "#f39c12"})
        
        # ID da ocorrencia
        ocorrencia_id = str(row.get("id", idx))
        tipo = row.get("tipo", "Nao informado")
        bairro = row.get("bairro", "Nao informado")
        
        # Criar header do expander
        header = f"{status_config['icone']} **{tipo}** | {bairro} | {prioridade}"
        
        with st.expander(header, expanded=False):
            col_info, col_acoes = st.columns([2, 1])
            
            with col_info:
                st.markdown("#### 📍 Detalhes da Ocorrencia")
                
                # Info basica
                st.markdown(f"**ID:** `{ocorrencia_id}`")
                st.markdown(f"**Tipo:** {tipo}")
                st.markdown(f"**Bairro:** {bairro}")
                
                # Data
                data = row.get("data", "Nao informada")
                if pd.notna(data):
                    if hasattr(data, 'strftime'):
                        data = data.strftime("%d/%m/%Y")
                st.markdown(f"**Data:** {data}")
                
                # Coordenadas
                lat = row.get("latitude", "N/A")
                lon = row.get("longitude", "N/A")
                st.markdown(f"**Coordenadas:** {lat}, {lon}")
                
                # Descricao
                st.markdown("---")
                st.markdown("**Descricao:**")
                descricao = row.get("descricao", "Sem descricao")
                st.info(descricao)
                
                # Usuario
                usuario = row.get("usuario", "Anonimo")
                st.markdown(f"**Reportado por:** {usuario}")
                
                # Votos
                votos = row.get("votos", 0)
                st.markdown(f"**Apoios da comunidade:** 👍 {votos}")
                
                # ================== FOTOS ==================
                fotos = row.get("fotos", [])
                if isinstance(fotos, str):
                    try:
                        import json
                        fotos = json.loads(fotos)
                    except:
                        fotos = []
                
                if fotos and len(fotos) > 0:
                    st.markdown("---")
                    st.markdown("**📷 Fotos anexadas:**")
                    
                    cols_fotos = st.columns(min(len(fotos), 4))
                    for i, foto_path in enumerate(fotos[:4]):
                        with cols_fotos[i]:
                            try:
                                st.image(foto_path, use_container_width=True)
                            except:
                                st.caption(f"📷 {Path(foto_path).name}")
                
                # ================== COMENTARIOS/HISTORICO ==================
                comentarios = row.get("comentarios", [])
                if isinstance(comentarios, str):
                    try:
                        import json
                        comentarios = json.loads(comentarios)
                    except:
                        comentarios = []
                
                if comentarios and len(comentarios) > 0:
                    st.markdown("---")
                    st.markdown("**💬 Historico de interacoes:**")
                    for com in comentarios:
                        autor = com.get("autor", "Sistema")
                        texto = com.get("texto", "")
                        data_com = com.get("data", "")
                        if data_com:
                            try:
                                data_com = datetime.fromisoformat(data_com).strftime("%d/%m/%Y %H:%M")
                            except:
                                pass
                        
                        st.markdown(f"""
                        <div style="
                            background: #f8f9fa;
                            padding: 0.75rem;
                            border-radius: 8px;
                            margin-bottom: 0.5rem;
                            border-left: 3px solid #3498db;
                        ">
                            <strong>{autor}</strong> <span style="color: #7f8c8d; font-size: 0.8rem;">({data_com})</span><br>
                            {texto}
                        </div>
                        """, unsafe_allow_html=True)
            
            with col_acoes:
                st.markdown("#### ⚙️ Acoes")
                
                # Status atual
                st.markdown(f"""
                <div style="
                    background: {status_config['cor']};
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <strong>Status: {status}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Prioridade atual
                st.markdown(f"""
                <div style="
                    background: {prioridade_config['cor']};
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <strong>Prioridade: {prioridade}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Verificar se e um reporte do JSON (editavel)
                reporte_editavel = None
                for rep in reportes:
                    if str(rep.get("id")) == str(ocorrencia_id):
                        reporte_editavel = rep
                        break
                
                # Formulario de atualizacao
                with st.form(f"form_atualizar_{ocorrencia_id}"):
                    st.markdown("**Atualizar Status:**")
                    novo_status = st.selectbox(
                        "Novo status",
                        list(STATUS_OCORRENCIA.keys()),
                        index=list(STATUS_OCORRENCIA.keys()).index(status) if status in STATUS_OCORRENCIA else 0,
                        key=f"status_{ocorrencia_id}",
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("**Atualizar Prioridade:**")
                    nova_prioridade = st.selectbox(
                        "Nova prioridade",
                        list(PRIORIDADES.keys()),
                        index=list(PRIORIDADES.keys()).index(prioridade) if prioridade in PRIORIDADES else 1,
                        key=f"prioridade_{ocorrencia_id}",
                        label_visibility="collapsed"
                    )
                    
                    st.markdown("**Adicionar comentario:**")
                    comentario = st.text_area(
                        "Comentario",
                        placeholder="Ex: Equipe enviada para verificacao...",
                        key=f"comentario_{ocorrencia_id}",
                        label_visibility="collapsed",
                        height=100
                    )
                    
                    atualizar = st.form_submit_button("💾 Salvar Alteracoes", use_container_width=True, type="primary")
                    
                    if atualizar:
                        if reporte_editavel:
                            atualizacoes = {
                                "status": novo_status,
                                "prioridade": nova_prioridade
                            }
                            
                            # Adicionar comentario se houver
                            if comentario.strip():
                                data_manager.adicionar_comentario(
                                    ocorrencia_id,
                                    comentario.strip(),
                                    "Administrador"
                                )
                            
                            # Atualizar ocorrencia
                            if data_manager.atualizar_ocorrencia(ocorrencia_id, atualizacoes):
                                st.success("✅ Ocorrencia atualizada!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao atualizar")
                        else:
                            st.warning("⚠️ Esta ocorrencia e do CSV e nao pode ser editada diretamente.")
                
                # Botao de finalizar rapido
                if status != "Resolvido" and reporte_editavel:
                    st.markdown("---")
                    if st.button("✅ Marcar como Resolvido", key=f"resolver_{ocorrencia_id}", use_container_width=True):
                        data_manager.atualizar_ocorrencia(ocorrencia_id, {"status": "Resolvido"})
                        data_manager.adicionar_comentario(ocorrencia_id, "Ocorrencia finalizada pelo administrador.", "Administrador")
                        st.success("✅ Ocorrencia marcada como resolvida!")
                        st.rerun()


def render():
    """Renderiza a pagina de administracao."""
    
    # Verificar se esta logado
    if not verificar_login():
        tela_login()
    else:
        painel_administrativo()

