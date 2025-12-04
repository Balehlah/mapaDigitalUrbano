"""
Painel Administrativo - Gestao de Ocorrencias
Acesso restrito ao administrador
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import json

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
    st.session_state["ocorrencia_selecionada"] = None
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
                    st.session_state["ocorrencia_selecionada"] = None
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Usuario ou senha incorretos!")


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
    
    # ================== TABS PRINCIPAIS ==================
    tab_lista, tab_detalhe = st.tabs(["📋 Lista de Ocorrencias", "🔍 Gerenciar Ocorrencia"])
    
    with tab_lista:
        st.markdown("### 📋 Selecione uma Ocorrencia para Gerenciar")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_status = st.selectbox(
                "Filtrar por Status",
                ["Todos", "Pendente", "Em Analise", "Em Andamento", "Resolvido", "Arquivado"],
                key="filtro_status"
            )
        with col2:
            filtro_tipo = st.selectbox(
                "Filtrar por Tipo",
                ["Todos"] + list(TIPOS_OCORRENCIA.keys()),
                key="filtro_tipo"
            )
        with col3:
            filtro_prioridade = st.selectbox(
                "Filtrar por Prioridade",
                ["Todas", "Critica", "Alta", "Media", "Baixa"],
                key="filtro_prioridade"
            )
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if filtro_status != "Todos":
            df_filtrado = df_filtrado[df_filtrado["status"] == filtro_status]
        if filtro_tipo != "Todos":
            df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
        if filtro_prioridade != "Todas":
            df_filtrado = df_filtrado[df_filtrado["prioridade"] == filtro_prioridade]
        
        # Ordenar por prioridade e data
        prioridade_ordem = {"Critica": 0, "Alta": 1, "Media": 2, "Baixa": 3}
        df_filtrado["prioridade_ordem"] = df_filtrado["prioridade"].map(prioridade_ordem).fillna(4)
        df_filtrado = df_filtrado.sort_values(["prioridade_ordem", "data"], ascending=[True, False])
        
        st.markdown(f"**{len(df_filtrado)}** ocorrencias encontradas")
        st.markdown("---")
        
        if df_filtrado.empty:
            st.info("Nenhuma ocorrencia com os filtros selecionados.")
        else:
            # Criar lista de ocorrencias como cards clicaveis
            for idx, row in df_filtrado.iterrows():
                ocorrencia_id = str(row.get("id", idx))
                tipo = row.get("tipo", "Nao informado")
                bairro = row.get("bairro", "Nao informado")
                status = row.get("status", "Pendente")
                prioridade = row.get("prioridade", "Media")
                descricao = str(row.get("descricao", "Sem descricao"))[:100] + "..."
                
                # Cores
                status_config = STATUS_OCORRENCIA.get(status, {"cor": "#7f8c8d", "icone": "❓"})
                prioridade_config = PRIORIDADES.get(prioridade, {"cor": "#f39c12"})
                
                # Usuario
                usuario = row.get("usuario", "")
                if pd.isna(usuario) or usuario == "":
                    usuario = "Anonimo"
                
                # Card da ocorrencia
                col_card, col_btn = st.columns([4, 1])
                
                with col_card:
                    st.markdown(f"""
                    <div style="
                        background: #1e1e1e;
                        border-left: 4px solid {prioridade_config['cor']};
                        padding: 1rem;
                        border-radius: 8px;
                        margin-bottom: 0.5rem;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 1.1rem;">{status_config['icone']} {tipo}</strong>
                                <span style="color: #7f8c8d;"> | {bairro}</span>
                            </div>
                            <div>
                                <span style="background: {status_config['cor']}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">{status}</span>
                                <span style="background: {prioridade_config['cor']}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 4px;">{prioridade}</span>
                            </div>
                        </div>
                        <p style="color: #aaa; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{descricao}</p>
                        <p style="color: #666; margin: 0.3rem 0 0 0; font-size: 0.8rem;">Por: {usuario} | ID: {ocorrencia_id[:20]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_btn:
                    if st.button("⚙️ Gerenciar", key=f"btn_{ocorrencia_id}", use_container_width=True):
                        st.session_state["ocorrencia_selecionada"] = ocorrencia_id
                        st.rerun()
    
    with tab_detalhe:
        ocorrencia_id = st.session_state.get("ocorrencia_selecionada")
        
        if not ocorrencia_id:
            st.info("👆 Selecione uma ocorrencia na aba 'Lista de Ocorrencias' para gerenciar.")
            return
        
        # Buscar ocorrencia
        row = None
        for idx, r in df.iterrows():
            if str(r.get("id", idx)) == str(ocorrencia_id):
                row = r
                break
        
        if row is None:
            st.error("Ocorrencia nao encontrada.")
            st.session_state["ocorrencia_selecionada"] = None
            return
        
        # Botao voltar
        if st.button("⬅️ Voltar para Lista"):
            st.session_state["ocorrencia_selecionada"] = None
            st.rerun()
        
        st.markdown("---")
        
        # ================== DETALHES DA OCORRENCIA ==================
        col_info, col_acoes = st.columns([2, 1])
        
        with col_info:
            st.markdown("### 📍 Detalhes da Ocorrencia")
            
            tipo = row.get("tipo", "Nao informado")
            bairro = row.get("bairro", "Nao informado")
            status = row.get("status", "Pendente")
            prioridade = row.get("prioridade", "Media")
            
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
            st.markdown("**Descricao completa:**")
            descricao = row.get("descricao", "Sem descricao")
            if pd.isna(descricao):
                descricao = "Sem descricao"
            st.info(descricao)
            
            # Usuario
            usuario = row.get("usuario", "Anonimo")
            if pd.isna(usuario) or usuario == "":
                usuario = "Anonimo"
            st.markdown(f"**Reportado por:** {usuario}")
            
            # Votos
            votos = row.get("votos", 0)
            if pd.isna(votos):
                votos = 0
            st.markdown(f"**Apoios da comunidade:** 👍 {int(votos)}")
            
            # ================== FOTOS ==================
            st.markdown("---")
            st.markdown("**📷 Fotos anexadas:**")
            
            fotos = row.get("fotos", None)
            
            # Verificar se fotos existe e tem conteudo
            fotos_lista = []
            if fotos is not None and not (isinstance(fotos, float) and pd.isna(fotos)):
                if isinstance(fotos, str):
                    try:
                        fotos_lista = json.loads(fotos)
                    except:
                        if fotos.strip():
                            fotos_lista = [fotos]
                elif isinstance(fotos, list):
                    fotos_lista = fotos
            
            if fotos_lista and len(fotos_lista) > 0:
                cols_fotos = st.columns(min(len(fotos_lista), 4))
                for i, foto_path in enumerate(fotos_lista[:4]):
                    with cols_fotos[i]:
                        try:
                            st.image(foto_path, use_container_width=True)
                        except:
                            st.caption(f"📷 {Path(foto_path).name}")
            else:
                st.caption("Nenhuma foto anexada.")
            
            # ================== HISTORICO DE INTERACOES ==================
            st.markdown("---")
            st.markdown("**💬 Historico de interacoes:**")
            
            comentarios = row.get("comentarios", None)
            
            # Verificar se comentarios existe e tem conteudo
            comentarios_lista = []
            if comentarios is not None and not (isinstance(comentarios, float) and pd.isna(comentarios)):
                if isinstance(comentarios, str):
                    try:
                        comentarios_lista = json.loads(comentarios)
                    except:
                        comentarios_lista = []
                elif isinstance(comentarios, list):
                    comentarios_lista = comentarios
            
            if comentarios_lista and len(comentarios_lista) > 0:
                for com in comentarios_lista:
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
                        background: #2d2d2d;
                        padding: 0.75rem;
                        border-radius: 8px;
                        margin-bottom: 0.5rem;
                        border-left: 3px solid #3498db;
                    ">
                        <strong>{autor}</strong> <span style="color: #7f8c8d; font-size: 0.8rem;">({data_com})</span><br>
                        <span style="color: #ddd;">{texto}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Nenhuma interacao registrada ainda.")
        
        with col_acoes:
            st.markdown("### ⚙️ Acoes")
            
            status_config = STATUS_OCORRENCIA.get(status, {"cor": "#7f8c8d", "icone": "❓"})
            prioridade_config = PRIORIDADES.get(prioridade, {"cor": "#f39c12"})
            
            # Status atual
            st.markdown(f"""
            <div style="
                background: {status_config['cor']};
                color: white;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: bold;
            ">
                Status Atual: {status}
            </div>
            """, unsafe_allow_html=True)
            
            # Prioridade atual
            st.markdown(f"""
            <div style="
                background: {prioridade_config['cor']};
                color: white;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: bold;
            ">
                Prioridade: {prioridade}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Verificar se e um reporte do JSON (editavel)
            reporte_editavel = None
            for rep in reportes:
                if str(rep.get("id")) == str(ocorrencia_id):
                    reporte_editavel = rep
                    break
            
            if not reporte_editavel:
                st.warning("⚠️ Esta ocorrencia e do CSV original e nao pode ser editada.")
                return
            
            # Formulario de atualizacao
            st.markdown("#### Atualizar Ocorrencia")
            
            with st.form(f"form_atualizar_{ocorrencia_id}"):
                novo_status = st.selectbox(
                    "Novo Status",
                    list(STATUS_OCORRENCIA.keys()),
                    index=list(STATUS_OCORRENCIA.keys()).index(status) if status in STATUS_OCORRENCIA else 0
                )
                
                nova_prioridade = st.selectbox(
                    "Nova Prioridade",
                    list(PRIORIDADES.keys()),
                    index=list(PRIORIDADES.keys()).index(prioridade) if prioridade in PRIORIDADES else 1
                )
                
                comentario = st.text_area(
                    "Adicionar Comentario",
                    placeholder="Ex: Equipe enviada para verificacao local...",
                    height=100
                )
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    atualizar = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
                
                with col_btn2:
                    finalizar = st.form_submit_button("✅ Finalizar", use_container_width=True)
                
                if atualizar:
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
                        st.success("✅ Ocorrencia atualizada com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar")
                
                if finalizar:
                    data_manager.atualizar_ocorrencia(ocorrencia_id, {"status": "Resolvido"})
                    data_manager.adicionar_comentario(
                        ocorrencia_id, 
                        "Ocorrencia finalizada pelo administrador.", 
                        "Administrador"
                    )
                    st.success("✅ Ocorrencia marcada como RESOLVIDA!")
                    st.rerun()
            
            # Botoes de acao rapida
            st.markdown("---")
            st.markdown("#### Acoes Rapidas")
            
            if status == "Pendente":
                if st.button("🔍 Marcar Em Analise", use_container_width=True):
                    data_manager.atualizar_ocorrencia(ocorrencia_id, {"status": "Em Analise"})
                    data_manager.adicionar_comentario(ocorrencia_id, "Ocorrencia em analise.", "Administrador")
                    st.rerun()
            
            if status in ["Pendente", "Em Analise"]:
                if st.button("🔧 Iniciar Atendimento", use_container_width=True):
                    data_manager.atualizar_ocorrencia(ocorrencia_id, {"status": "Em Andamento"})
                    data_manager.adicionar_comentario(ocorrencia_id, "Atendimento iniciado.", "Administrador")
                    st.rerun()
            
            if status != "Arquivado":
                if st.button("📁 Arquivar", use_container_width=True):
                    data_manager.atualizar_ocorrencia(ocorrencia_id, {"status": "Arquivado"})
                    data_manager.adicionar_comentario(ocorrencia_id, "Ocorrencia arquivada.", "Administrador")
                    st.rerun()


def render():
    """Renderiza a pagina de administracao."""
    
    # Inicializar session state
    if "ocorrencia_selecionada" not in st.session_state:
        st.session_state["ocorrencia_selecionada"] = None
    
    # Verificar se esta logado
    if not verificar_login():
        tela_login()
    else:
        painel_administrativo()
