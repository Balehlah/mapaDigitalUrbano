"""
Gerenciador de dados - CRUD completo para ocorrências.
"""
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import uuid

from config import (
    OCORRENCIAS_CSV, 
    REPORTES_JSON, 
    IMAGES_DIR,
    TIPOS_OCORRENCIA,
    STATUS_OCORRENCIA,
    PRIORIDADES
)


class DataManager:
    """Gerenciador centralizado de dados de ocorrências."""
    
    def __init__(self):
        self._cache_csv: Optional[pd.DataFrame] = None
        self._cache_json: Optional[List[Dict]] = None
        self._last_load: Optional[datetime] = None
    
    def _carregar_csv(self) -> pd.DataFrame:
        """Carrega dados do CSV de ocorrências mock."""
        if not OCORRENCIAS_CSV.exists():
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(OCORRENCIAS_CSV, encoding="utf-8")
            # Normalizar nomes de colunas
            df.columns = df.columns.str.lower().str.strip()
            
            # Garantir colunas essenciais
            if "tipo_ocorrencia" in df.columns:
                df["tipo"] = df["tipo_ocorrencia"]
            
            # Adicionar colunas padrão se não existirem
            if "status" not in df.columns:
                df["status"] = "Pendente"
            if "prioridade" not in df.columns:
                df["prioridade"] = "Media"
            if "fonte" not in df.columns:
                df["fonte"] = "CSV"
            if "id" not in df.columns:
                df["id"] = range(1, len(df) + 1)
            
            # Converter data
            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"], errors="coerce")
            
            return df
            
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return pd.DataFrame()
    
    def _carregar_reportes(self) -> List[Dict]:
        """Carrega reportes do JSON."""
        if not REPORTES_JSON.exists():
            return []
        
        try:
            with open(REPORTES_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar reportes: {e}")
            return []
    
    def _salvar_reportes(self, reportes: List[Dict]) -> bool:
        """Salva reportes no JSON."""
        try:
            with open(REPORTES_JSON, "w", encoding="utf-8") as f:
                json.dump(reportes, f, indent=2, ensure_ascii=False, default=str)
            self._cache_json = None  # Invalida cache
            return True
        except Exception as e:
            print(f"Erro ao salvar reportes: {e}")
            return False
    
    def carregar_todas_ocorrencias(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Carrega todas as ocorrências (CSV + JSON) em um DataFrame unificado.
        """
        # Carregar CSV
        df_csv = self._carregar_csv()
        
        # Carregar reportes JSON
        reportes = self._carregar_reportes()
        
        if reportes:
            df_json = pd.DataFrame(reportes)
            df_json["fonte"] = "Usuário"
            
            # Normalizar colunas do JSON
            if "data_envio" in df_json.columns:
                df_json["data"] = pd.to_datetime(df_json["data_envio"], errors="coerce")
            
            # Unificar DataFrames
            if not df_csv.empty:
                df = pd.concat([df_csv, df_json], ignore_index=True)
            else:
                df = df_json
        else:
            df = df_csv
        
        # Preencher valores nulos
        df["status"] = df.get("status", pd.Series(["Pendente"] * len(df))).fillna("Pendente")
        df["prioridade"] = df.get("prioridade", pd.Series(["Media"] * len(df))).fillna("Media")
        
        return df
    
    def adicionar_ocorrencia(
        self,
        tipo: str,
        descricao: str,
        latitude: float,
        longitude: float,
        bairro: str,
        prioridade: str = "Media",
        fotos: Optional[List[str]] = None,
        usuario: str = "Anonimo"
    ) -> Dict[str, Any]:
        """
        Adiciona uma nova ocorrência ao sistema.
        
        Returns:
            Dict com os dados da ocorrência criada
        """
        # Gerar ID único
        id_ocorrencia = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:6]
        
        ocorrencia = {
            "id": id_ocorrencia,
            "tipo": tipo,
            "descricao": descricao,
            "latitude": latitude,
            "longitude": longitude,
            "bairro": bairro,
            "status": "Pendente",
            "prioridade": prioridade,
            "fotos": fotos or [],
            "usuario": usuario,
            "data_envio": datetime.now().isoformat(),
            "data_atualizacao": datetime.now().isoformat(),
            "votos": 0,
            "comentarios": []
        }
        
        # Carregar reportes existentes e adicionar novo
        reportes = self._carregar_reportes()
        reportes.append(ocorrencia)
        
        if self._salvar_reportes(reportes):
            return ocorrencia
        else:
            raise Exception("Falha ao salvar ocorrência")
    
    def atualizar_ocorrencia(self, id_ocorrencia: str, atualizacoes: Dict) -> bool:
        """Atualiza uma ocorrência existente."""
        reportes = self._carregar_reportes()
        
        for i, rep in enumerate(reportes):
            if rep.get("id") == id_ocorrencia:
                reportes[i].update(atualizacoes)
                reportes[i]["data_atualizacao"] = datetime.now().isoformat()
                return self._salvar_reportes(reportes)
        
        return False
    
    def votar_ocorrencia(self, id_ocorrencia: str) -> bool:
        """Incrementa o contador de votos de uma ocorrência."""
        reportes = self._carregar_reportes()
        
        for i, rep in enumerate(reportes):
            if rep.get("id") == id_ocorrencia:
                reportes[i]["votos"] = reportes[i].get("votos", 0) + 1
                return self._salvar_reportes(reportes)
        
        return False
    
    def adicionar_comentario(self, id_ocorrencia: str, comentario: str, autor: str = "Anonimo") -> bool:
        """Adiciona um comentário a uma ocorrência."""
        reportes = self._carregar_reportes()
        
        for i, rep in enumerate(reportes):
            if rep.get("id") == id_ocorrencia:
                if "comentarios" not in reportes[i]:
                    reportes[i]["comentarios"] = []
                
                reportes[i]["comentarios"].append({
                    "texto": comentario,
                    "autor": autor,
                    "data": datetime.now().isoformat()
                })
                return self._salvar_reportes(reportes)
        
        return False
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais das ocorrências."""
        df = self.carregar_todas_ocorrencias()
        
        if df.empty:
            return {
                "total": 0,
                "por_tipo": {},
                "por_status": {},
                "por_bairro": {},
                "por_prioridade": {},
                "ultimos_7_dias": 0,
                "taxa_resolucao": 0
            }
        
        # Por tipo
        por_tipo = df["tipo"].value_counts().to_dict() if "tipo" in df.columns else {}
        
        # Por status
        por_status = df["status"].value_counts().to_dict() if "status" in df.columns else {}
        
        # Por bairro
        por_bairro = df["bairro"].value_counts().to_dict() if "bairro" in df.columns else {}
        
        # Por prioridade
        por_prioridade = df["prioridade"].value_counts().to_dict() if "prioridade" in df.columns else {}
        
        # Últimos 7 dias
        ultimos_7_dias = 0
        if "data" in df.columns:
            data_limite = datetime.now() - pd.Timedelta(days=7)
            ultimos_7_dias = len(df[df["data"] >= data_limite])
        
        # Taxa de resolução
        total = len(df)
        resolvidos = por_status.get("Resolvido", 0)
        taxa_resolucao = (resolvidos / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "por_tipo": por_tipo,
            "por_status": por_status,
            "por_bairro": por_bairro,
            "por_prioridade": por_prioridade,
            "ultimos_7_dias": ultimos_7_dias,
            "taxa_resolucao": round(taxa_resolucao, 1)
        }
    
    def salvar_imagem(self, id_ocorrencia: str, arquivo, nome_arquivo: str) -> str:
        """Salva uma imagem associada a uma ocorrência."""
        pasta_imagem = IMAGES_DIR / id_ocorrencia
        pasta_imagem.mkdir(parents=True, exist_ok=True)
        
        caminho_arquivo = pasta_imagem / nome_arquivo
        
        with open(caminho_arquivo, "wb") as f:
            f.write(arquivo.getbuffer())
        
        return str(caminho_arquivo)


# Instância global
data_manager = DataManager()

