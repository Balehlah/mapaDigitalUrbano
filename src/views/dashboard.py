"""
Dashboard de estatísticas e KPIs das ocorrências urbanas.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import data_manager
from config import TIPOS_OCORRENCIA, STATUS_OCORRENCIA, PRIORIDADES


def render():
    """Renderiza o dashboard de estatísticas."""
    
    st.markdown("## 📊 Dashboard de Ocorrências")
    st.markdown("Análise em tempo real dos problemas urbanos reportados pela comunidade.")
    
    # Carregar dados
    df = data_manager.carregar_todas_ocorrencias()
    stats = data_manager.obter_estatisticas()
    
    if df.empty:
        st.warning("📭 Nenhuma ocorrência registrada. Os dados aparecerão aqui após o primeiro reporte.")
        return
    
    # ================== KPIs PRINCIPAIS ==================
    st.markdown("### 📈 Indicadores Principais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total de Ocorrências",
            stats["total"],
            help="Número total de problemas reportados"
        )
    
    with col2:
        pendentes = stats["por_status"].get("Pendente", 0)
        st.metric(
            "Pendentes",
            pendentes,
            delta=f"{(pendentes/stats['total']*100):.0f}%" if stats["total"] > 0 else "0%",
            delta_color="inverse"
        )
    
    with col3:
        em_andamento = stats["por_status"].get("Em Andamento", 0)
        st.metric(
            "Em Andamento",
            em_andamento
        )
    
    with col4:
        resolvidos = stats["por_status"].get("Resolvido", 0)
        st.metric(
            "Resolvidos",
            resolvidos,
            delta=f"{stats['taxa_resolucao']:.1f}%"
        )
    
    with col5:
        st.metric(
            "Últimos 7 dias",
            stats["ultimos_7_dias"],
            help="Ocorrências dos últimos 7 dias"
        )
    
    st.markdown("---")
    
    # ================== GRÁFICOS ==================
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        # Gráfico de pizza - Por Tipo
        st.markdown("#### 🏷️ Distribuição por Tipo")
        
        if stats["por_tipo"]:
            df_tipo = pd.DataFrame({
                "Tipo": list(stats["por_tipo"].keys()),
                "Quantidade": list(stats["por_tipo"].values())
            })
            
            cores = [TIPOS_OCORRENCIA.get(t, {}).get("cor", "#7f8c8d") for t in df_tipo["Tipo"]]
            
            fig_tipo = px.pie(
                df_tipo,
                values="Quantidade",
                names="Tipo",
                color_discrete_sequence=cores,
                hole=0.4
            )
            fig_tipo.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            fig_tipo.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig_tipo, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    with col_dir:
        # Gráfico de barras - Por Status
        st.markdown("#### 📊 Status das Ocorrências")
        
        if stats["por_status"]:
            df_status = pd.DataFrame({
                "Status": list(stats["por_status"].keys()),
                "Quantidade": list(stats["por_status"].values())
            })
            
            # Ordenar por quantidade
            df_status = df_status.sort_values("Quantidade", ascending=True)
            
            cores_status = [STATUS_OCORRENCIA.get(s, {}).get("cor", "#7f8c8d") for s in df_status["Status"]]
            
            fig_status = px.bar(
                df_status,
                x="Quantidade",
                y="Status",
                orientation="h",
                color="Status",
                color_discrete_sequence=cores_status
            )
            fig_status.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False,
                xaxis_title="",
                yaxis_title=""
            )
            
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    st.markdown("---")
    
    # ================== ANÁLISE POR BAIRRO ==================
    st.markdown("### 🏘️ Ocorrências por Bairro")
    
    if stats["por_bairro"]:
        df_bairro = pd.DataFrame({
            "Bairro": list(stats["por_bairro"].keys()),
            "Quantidade": list(stats["por_bairro"].values())
        }).sort_values("Quantidade", ascending=False)
        
        fig_bairro = px.bar(
            df_bairro,
            x="Bairro",
            y="Quantidade",
            color="Quantidade",
            color_continuous_scale="RdYlGn_r"
        )
        fig_bairro.update_layout(
            margin=dict(t=20, b=60, l=20, r=20),
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig_bairro, use_container_width=True)
        
        # Ranking de bairros
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Bairros Mais Afetados")
            top_bairros = df_bairro.head(5)
            for i, row in top_bairros.iterrows():
                st.markdown(f"**{row['Bairro']}**: {row['Quantidade']} ocorrências")
        
        with col2:
            st.markdown("#### 🟢 Bairros Menos Afetados")
            bottom_bairros = df_bairro.tail(5).sort_values("Quantidade")
            for i, row in bottom_bairros.iterrows():
                st.markdown(f"**{row['Bairro']}**: {row['Quantidade']} ocorrências")
    
    st.markdown("---")
    
    # ================== TIMELINE ==================
    st.markdown("### 📅 Linha do Tempo")
    
    if "data" in df.columns:
        df_timeline = df.copy()
        df_timeline["data"] = pd.to_datetime(df_timeline["data"], errors="coerce")
        df_timeline = df_timeline.dropna(subset=["data"])
        
        if not df_timeline.empty:
            # Agrupar por dia
            df_timeline["data_dia"] = df_timeline["data"].dt.date
            df_por_dia = df_timeline.groupby("data_dia").size().reset_index(name="Quantidade")
            df_por_dia["data_dia"] = pd.to_datetime(df_por_dia["data_dia"])
            
            fig_timeline = px.area(
                df_por_dia,
                x="data_dia",
                y="Quantidade",
                title="",
                color_discrete_sequence=["#3498db"]
            )
            fig_timeline.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                xaxis_title="Data",
                yaxis_title="Ocorrências"
            )
            fig_timeline.update_traces(
                fill='tozeroy',
                line=dict(width=2)
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("Dados de data não disponíveis")
    
    # ================== PRIORIDADE ==================
    st.markdown("---")
    st.markdown("### ⚡ Análise de Prioridade")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if stats["por_prioridade"]:
            df_prioridade = pd.DataFrame({
                "Prioridade": list(stats["por_prioridade"].keys()),
                "Quantidade": list(stats["por_prioridade"].values())
            })
            
            # Ordenar por peso
            ordem = ["Baixa", "Media", "Alta", "Critica"]
            df_prioridade["ordem"] = df_prioridade["Prioridade"].map(
                {p: i for i, p in enumerate(ordem)}
            )
            df_prioridade = df_prioridade.sort_values("ordem")
            
            cores_prioridade = [PRIORIDADES.get(p, {}).get("cor", "#7f8c8d") for p in df_prioridade["Prioridade"]]
            
            fig_prioridade = px.bar(
                df_prioridade,
                x="Prioridade",
                y="Quantidade",
                color="Prioridade",
                color_discrete_sequence=cores_prioridade
            )
            fig_prioridade.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False
            )
            
            st.plotly_chart(fig_prioridade, use_container_width=True)
    
    with col2:
        st.markdown("#### 🚨 Atenção Necessária")
        
        criticas = stats["por_prioridade"].get("Critica", 0)
        altas = stats["por_prioridade"].get("Alta", 0)
        
        if criticas > 0:
            st.error(f"**{criticas}** ocorrências críticas precisam de atenção imediata!")
        
        if altas > 0:
            st.warning(f"**{altas}** ocorrências de alta prioridade aguardando resolução.")
        
        if criticas == 0 and altas == 0:
            st.success("✅ Nenhuma ocorrência crítica ou de alta prioridade!")
        
        # Índice de urgência
        total = stats["total"]
        if total > 0:
            peso_total = (
                criticas * 4 + 
                altas * 3 + 
                stats["por_prioridade"].get("Media", 0) * 2 + 
                stats["por_prioridade"].get("Baixa", 0)
            )
            indice = (peso_total / (total * 4)) * 100
            
            st.markdown("---")
            st.markdown("**Índice de Urgência Geral**")
            st.progress(indice / 100)
            st.caption(f"{indice:.1f}% (quanto maior, mais urgente)")
    
    # ================== EXPORTAR RELATÓRIO ==================
    st.markdown("---")
    
    with st.expander("📥 Exportar Relatório"):
        col1, col2 = st.columns(2)
        
        with col1:
            csv_completo = df.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                "📄 Baixar Dados Completos (CSV)",
                csv_completo,
                "ocorrencias_completo.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # Resumo em texto
            resumo = f"""
RELATÓRIO DE OCORRÊNCIAS URBANAS
================================
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}

RESUMO GERAL
- Total de Ocorrências: {stats['total']}
- Taxa de Resolução: {stats['taxa_resolucao']}%
- Últimos 7 dias: {stats['ultimos_7_dias']}

POR TIPO:
{chr(10).join([f"  - {k}: {v}" for k, v in stats['por_tipo'].items()])}

POR STATUS:
{chr(10).join([f"  - {k}: {v}" for k, v in stats['por_status'].items()])}

POR BAIRRO:
{chr(10).join([f"  - {k}: {v}" for k, v in stats['por_bairro'].items()])}
            """
            
            st.download_button(
                "📊 Baixar Resumo (TXT)",
                resumo,
                "resumo_ocorrencias.txt",
                "text/plain",
                use_container_width=True
            )

