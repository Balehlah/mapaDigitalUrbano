"""
Página para reportar novos problemas urbanos.
"""
import streamlit as st
from streamlit_folium import st_folium
import folium
import sys
from pathlib import Path
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import data_manager
from config import TIPOS_OCORRENCIA, BAIRROS, PRIORIDADES, MAP_CONFIG


def render():
    """Renderiza a página de reportar problemas."""
    
    st.markdown("## 📣 Reportar Problema Urbano")
    st.markdown("Ajude a melhorar sua cidade! Reporte problemas de infraestrutura de forma rápida e fácil.")
    
    # Layout em duas colunas
    col_mapa, col_form = st.columns([1, 1])
    
    with col_mapa:
        st.markdown("### 📍 Selecione a Localização")
        st.markdown("Clique no mapa para marcar o local exato do problema.")
        
        # Criar mapa para seleção
        mapa = folium.Map(
            location=[MAP_CONFIG["center_lat"], MAP_CONFIG["center_lon"]],
            zoom_start=MAP_CONFIG["zoom_start"],
            tiles="CartoDB positron"
        )
        
        # Adicionar popup de coordenadas
        mapa.add_child(folium.LatLngPopup())
        
        # Exibir mapa
        output = st_folium(
            mapa,
            height=400,
            width=None,
            use_container_width=True,
            key="mapa_reportar"
        )
        
        # Capturar coordenadas
        lat = None
        lon = None
        
        if output and output.get("last_clicked"):
            lat = output["last_clicked"]["lat"]
            lon = output["last_clicked"]["lng"]
            st.success(f"✅ Local selecionado: {lat:.6f}, {lon:.6f}")
        else:
            st.info("👆 Clique no mapa para selecionar a localização")
    
    with col_form:
        st.markdown("### 📝 Detalhes do Problema")
        
        with st.form("form_reportar", clear_on_submit=True):
            # Tipo de problema
            tipo = st.selectbox(
                "Tipo do Problema *",
                list(TIPOS_OCORRENCIA.keys()),
                help="Selecione a categoria que melhor descreve o problema"
            )
            
            # Descrição do tipo selecionado
            st.caption(f"ℹ️ {TIPOS_OCORRENCIA[tipo]['descricao']}")
            
            # Descrição detalhada
            descricao = st.text_area(
                "Descrição Detalhada *",
                placeholder="Descreva o problema com detalhes. Ex: Buraco de aproximadamente 50cm de diâmetro na esquina da rua...",
                height=120,
                max_chars=500
            )
            
            # Bairro
            bairro = st.selectbox(
                "Bairro *",
                BAIRROS,
                help="Selecione o bairro onde está localizado o problema"
            )
            
            # Prioridade
            prioridade = st.select_slider(
                "Prioridade *",
                options=list(PRIORIDADES.keys()),
                value="Média",
                help="Baixa: não urgente | Média: pode esperar | Alta: precisa atenção | Crítica: risco imediato"
            )
            
            # Mostrar cor da prioridade
            cor_prioridade = PRIORIDADES[prioridade]["cor"]
            st.markdown(
                f'<div style="height: 4px; background: {cor_prioridade}; border-radius: 2px; margin-bottom: 1rem;"></div>',
                unsafe_allow_html=True
            )
            
            # Upload de fotos
            st.markdown("#### 📷 Fotos (opcional)")
            fotos = st.file_uploader(
                "Adicione fotos do problema",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                help="Você pode adicionar até 5 fotos"
            )
            
            if fotos and len(fotos) > 5:
                st.warning("⚠️ Máximo de 5 fotos permitidas. Apenas as 5 primeiras serão salvas.")
                fotos = fotos[:5]
            
            # Prévia das fotos
            if fotos:
                cols = st.columns(min(len(fotos), 5))
                for i, foto in enumerate(fotos[:5]):
                    with cols[i]:
                        st.image(foto, width=80)
            
            # Nome do usuário (opcional)
            st.markdown("#### 👤 Identificação (opcional)")
            nome_usuario = st.text_input(
                "Seu nome",
                placeholder="Anônimo",
                max_chars=100
            )
            
            # Termos
            aceita_termos = st.checkbox(
                "Declaro que as informações são verdadeiras e autorizo o uso para fins de melhoria urbana.",
                value=False
            )
            
            # Botão de envio
            submitted = st.form_submit_button(
                "🚀 Enviar Reporte",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validações
                erros = []
                
                if lat is None or lon is None:
                    erros.append("Selecione a localização no mapa")
                
                if not descricao or len(descricao.strip()) < 10:
                    erros.append("A descrição deve ter pelo menos 10 caracteres")
                
                if not aceita_termos:
                    erros.append("Você deve aceitar os termos para continuar")
                
                if erros:
                    for erro in erros:
                        st.error(f"❌ {erro}")
                else:
                    # Salvar fotos
                    paths_fotos = []
                    id_temp = datetime.now().strftime("%Y%m%d%H%M%S")
                    
                    if fotos:
                        for foto in fotos[:5]:
                            try:
                                path = data_manager.salvar_imagem(
                                    id_temp,
                                    foto,
                                    foto.name
                                )
                                paths_fotos.append(path)
                            except Exception as e:
                                st.warning(f"Erro ao salvar foto: {foto.name}")
                    
                    # Salvar ocorrência
                    try:
                        ocorrencia = data_manager.adicionar_ocorrencia(
                            tipo=tipo,
                            descricao=descricao.strip(),
                            latitude=lat,
                            longitude=lon,
                            bairro=bairro,
                            prioridade=prioridade,
                            fotos=paths_fotos,
                            usuario=nome_usuario.strip() or "Anônimo"
                        )
                        
                        st.success("🎉 Ocorrência registrada com sucesso!")
                        st.balloons()
                        
                        # Mostrar resumo
                        st.markdown("---")
                        st.markdown("#### ✅ Resumo do Reporte")
                        
                        resumo_cols = st.columns(2)
                        with resumo_cols[0]:
                            st.markdown(f"**Tipo:** {tipo}")
                            st.markdown(f"**Bairro:** {bairro}")
                            st.markdown(f"**Prioridade:** {prioridade}")
                        with resumo_cols[1]:
                            st.markdown(f"**ID:** `{ocorrencia['id'][:15]}...`")
                            st.markdown(f"**Status:** Pendente")
                            st.markdown(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar: {str(e)}")
    
    # ================== DICAS ==================
    st.markdown("---")
    
    with st.expander("💡 Dicas para um bom reporte"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📍 Localização Precisa**
            - Use o zoom para localizar exatamente o ponto
            - Clique o mais próximo possível do problema
            - Se necessário, mencione pontos de referência na descrição
            """)
            
            st.markdown("""
            **📝 Descrição Clara**
            - Seja objetivo e específico
            - Mencione tamanho aproximado do problema
            - Informe há quanto tempo existe
            """)
        
        with col2:
            st.markdown("""
            **📷 Fotos Úteis**
            - Tire fotos durante o dia para melhor visibilidade
            - Mostre o problema de diferentes ângulos
            - Inclua referências visuais (postes, placas)
            """)
            
            st.markdown("""
            **⚡ Prioridade Correta**
            - **Crítica:** Risco à vida (buraco profundo, fiação exposta)
            - **Alta:** Precisa atenção urgente
            - **Média:** Pode ser resolvido normalmente
            - **Baixa:** Melhoria desejável
            """)

