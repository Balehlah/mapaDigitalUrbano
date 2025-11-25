"""
Configurações centralizadas do Mapa Digital Urbano.
"""
import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = RAW_DATA_DIR / "images"

# Arquivos de dados
OCORRENCIAS_CSV = RAW_DATA_DIR / "ocorrencias_mock.csv"
REPORTES_JSON = RAW_DATA_DIR / "reportes.json"

# Garantir que diretórios existam
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, IMAGES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Configurações do mapa (Cacoal - RO)
MAP_CONFIG = {
    "center_lat": -11.4400,
    "center_lon": -61.4600,
    "zoom_start": 13,
    "min_zoom": 10,
    "max_zoom": 18,
}

# Tipos de ocorrência com cores e ícones
TIPOS_OCORRENCIA = {
    "Buraco": {
        "cor": "#e74c3c",
        "icone": "road",
        "descricao": "Buracos e irregularidades no asfalto"
    },
    "Iluminação": {
        "cor": "#f39c12",
        "icone": "lightbulb",
        "descricao": "Problemas com iluminação pública"
    },
    "Lixo": {
        "cor": "#27ae60",
        "icone": "trash",
        "descricao": "Acúmulo de lixo ou entulho"
    },
    "Alagamento": {
        "cor": "#3498db",
        "icone": "water",
        "descricao": "Pontos de alagamento"
    },
    "Calçada": {
        "cor": "#9b59b6",
        "icone": "shoe-prints",
        "descricao": "Problemas em calçadas"
    },
    "Sinalização": {
        "cor": "#1abc9c",
        "icone": "signs-post",
        "descricao": "Sinalização danificada ou ausente"
    },
    "Árvore": {
        "cor": "#2d5016",
        "icone": "tree",
        "descricao": "Árvores caídas ou com risco"
    },
    "Outro": {
        "cor": "#7f8c8d",
        "icone": "circle-exclamation",
        "descricao": "Outros problemas urbanos"
    }
}

# Status das ocorrências
STATUS_OCORRENCIA = {
    "Pendente": {"cor": "#e74c3c", "icone": "⏳"},
    "Em Análise": {"cor": "#f39c12", "icone": "🔍"},
    "Em Andamento": {"cor": "#3498db", "icone": "🔧"},
    "Resolvido": {"cor": "#27ae60", "icone": "✅"},
    "Arquivado": {"cor": "#7f8c8d", "icone": "📁"}
}

# Prioridades
PRIORIDADES = {
    "Baixa": {"cor": "#27ae60", "peso": 1},
    "Média": {"cor": "#f39c12", "peso": 2},
    "Alta": {"cor": "#e67e22", "peso": 3},
    "Crítica": {"cor": "#e74c3c", "peso": 4}
}

# Bairros de Cacoal (expandido)
BAIRROS = [
    "Centro",
    "Vista Alegre",
    "Princesa Isabel",
    "Green Ville",
    "Josino Brito",
    "Liberdade",
    "Bela Vista",
    "Jardim Clodoaldo",
    "Novo Cacoal",
    "Teixeirão",
    "Industrial",
    "Outro"
]

# Configurações da aplicação
APP_CONFIG = {
    "titulo": "🗺️ Mapa Digital Urbano",
    "subtitulo": "Plataforma Comunitária de Infraestrutura",
    "versao": "2.0.0",
    "autor": "Comunidade de Cacoal"
}

