"""
Página Sobre - Informações do projeto e como usar.
"""
import streamlit as st
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import APP_CONFIG, TIPOS_OCORRENCIA


def render():
    """Renderiza a página Sobre."""
    
    st.markdown("## ℹ️ Sobre o Projeto")
    
    # Hero section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a5f 0%, #0d7377 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    ">
        <h2 style="margin: 0; font-size: 1.8rem;">🗺️ Mapa Digital Comunitário de Infraestrutura Urbana</h2>
        <p style="margin: 1rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
            Dando voz e poder à população para reportar e visualizar problemas urbanos usando tecnologia acessível.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs de conteúdo
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Missão", "📖 Como Usar", "🏷️ Tipos de Problema", "🤝 Contribua"])
    
    with tab1:
        st.markdown("### 🎯 Nossa Missão")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### O Problema
            
            Muitas cidades enfrentam desafios de infraestrutura urbana que afetam diretamente 
            a qualidade de vida dos moradores:
            
            - 🕳️ Buracos nas vias
            - 💡 Iluminação deficiente
            - 🗑️ Acúmulo de lixo
            - 🌊 Pontos de alagamento
            - 🚶 Calçadas danificadas
            
            A falta de um canal direto entre a população e a gestão pública dificulta 
            a identificação e resolução desses problemas.
            """)
        
        with col2:
            st.markdown("""
            #### Nossa Solução
            
            O **Mapa Digital Urbano** é uma plataforma colaborativa que permite:
            
            - ✅ **Reportar problemas** de forma simples e rápida
            - ✅ **Visualizar ocorrências** em um mapa interativo
            - ✅ **Acompanhar o status** de cada problema
            - ✅ **Gerar dados** para tomada de decisão
            - ✅ **Engajar a comunidade** na melhoria urbana
            
            Transparência, participação cidadã e tecnologia a serviço da cidade.
            """)
        
        st.markdown("---")
        
        st.markdown("### 👥 Para Quem é Esta Plataforma?")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            **🏠 Moradores**
            
            Reporte problemas do seu bairro e acompanhe as resoluções.
            """)
        
        with col2:
            st.markdown("""
            **👑 Líderes Comunitários**
            
            Utilize os dados para reivindicar melhorias junto à prefeitura.
            """)
        
        with col3:
            st.markdown("""
            **🏛️ Gestão Pública**
            
            Tenha uma visão clara dos problemas e priorize ações.
            """)
        
        with col4:
            st.markdown("""
            **👷 Engenheiros**
            
            Acesse dados georreferenciados para planejamento urbano.
            """)
    
    with tab2:
        st.markdown("### 📖 Como Usar a Plataforma")
        
        st.markdown("#### 📣 Reportando um Problema")
        
        st.markdown("""
        1. **Acesse "Reportar Problema"** no menu lateral
        2. **Clique no mapa** para marcar a localização exata
        3. **Preencha o formulário** com:
           - Tipo do problema
           - Descrição detalhada
           - Bairro
           - Prioridade
           - Fotos (opcional)
        4. **Envie o reporte** e pronto!
        
        > 💡 **Dica:** Quanto mais detalhado o reporte, mais fácil será a resolução!
        """)
        
        st.markdown("---")
        
        st.markdown("#### 🗺️ Explorando o Mapa")
        
        st.markdown("""
        1. **Acesse "Mapa Interativo"** no menu lateral
        2. **Use os filtros** para encontrar tipos específicos
        3. **Clique nos marcadores** para ver detalhes
        4. **Alterne entre visualizações:**
           - 📍 Marcadores: veja cada problema individualmente
           - 🔥 Mapa de Calor: identifique áreas críticas
        5. **Exporte os dados** para análises externas
        """)
        
        st.markdown("---")
        
        st.markdown("#### 📊 Analisando Dados")
        
        st.markdown("""
        O **Dashboard** oferece:
        
        - 📈 **KPIs principais**: total, pendentes, resolvidos
        - 🥧 **Gráficos por tipo**: distribuição dos problemas
        - 🏘️ **Análise por bairro**: identifique áreas mais afetadas
        - 📅 **Linha do tempo**: evolução temporal
        - ⚡ **Índice de urgência**: priorização automática
        - 📥 **Exportação**: CSV e relatórios em texto
        """)
    
    with tab3:
        st.markdown("### 🏷️ Tipos de Problemas")
        st.markdown("Conheça as categorias disponíveis para reportar:")
        
        cols = st.columns(2)
        tipos_list = list(TIPOS_OCORRENCIA.items())
        
        for i, (tipo, config) in enumerate(tipos_list):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="
                    background: {config['cor']}15;
                    border-left: 4px solid {config['cor']};
                    padding: 1rem;
                    border-radius: 8px;
                    margin-bottom: 0.75rem;
                ">
                    <strong style="color: {config['cor']};">
                        <i class="fa fa-{config['icone']}"></i> {tipo}
                    </strong>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #555;">
                        {config['descricao']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🤝 Como Contribuir")
        
        st.markdown("""
        Este é um projeto de código aberto e comunitário. Você pode contribuir de várias formas:
        
        #### 📣 Como Cidadão
        - Reporte problemas que você encontrar
        - Compartilhe a plataforma com vizinhos e amigos
        - Valide reportes de outros usuários
        - Sugira melhorias
        
        #### 💻 Como Desenvolvedor
        - Contribua com código no repositório
        - Reporte bugs e sugira funcionalidades
        - Ajude na documentação
        - Crie integrações com outros sistemas
        
        #### 🏛️ Como Gestor Público
        - Integre a plataforma aos sistemas da prefeitura
        - Utilize os dados para planejamento
        - Dê feedback sobre as ocorrências
        - Promova a participação cidadã
        """)
        
        st.markdown("---")
        
        # Info do projeto
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Versão**  
            `{APP_CONFIG['versao']}`
            """)
        
        with col2:
            st.markdown("""
            **Tecnologias**  
            `Python` `Streamlit` `Folium`
            """)
        
        with col3:
            st.markdown("""
            **Licença**  
            `MIT` - Código Aberto
            """)





