# 🗺️ Mapa Digital Urbano

**Plataforma Comunitária de Infraestrutura Urbana**

> Dando voz e poder à população para reportar e visualizar problemas urbanos usando tecnologia acessível.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Sobre o Projeto

O **Mapa Digital Urbano** é uma plataforma web colaborativa que permite aos cidadãos reportar e acompanhar problemas de infraestrutura urbana em suas cidades. A ferramenta facilita a comunicação entre a população e a gestão pública, gerando dados estruturados para tomada de decisão.

### 🎯 Problema que Resolve

- Falta de canais diretos entre comunidade e gestão pública
- Ausência de dados urbanos estruturados e georreferenciados
- Dificuldade em priorizar ações de manutenção urbana
- Baixo engajamento cidadão na melhoria das cidades

### ✅ Solução Proposta

- Plataforma web aberta e interativa de mapeamento comunitário
- Sistema de reporte simples e acessível
- Dashboard com KPIs e análises em tempo real
- Exportação de dados para integração com outros sistemas

---

## 🚀 Funcionalidades

### 🗺️ Mapa Interativo
- Visualização de todas as ocorrências georreferenciadas
- Filtros por tipo, status, bairro e prioridade
- Mapa de calor para identificar áreas críticas
- Agrupamento inteligente de marcadores (clusters)
- Múltiplos estilos de mapa (Claro, Escuro, Padrão)

### 📣 Reportar Problema
- Seleção de localização clicando no mapa
- Categorização por tipo de problema
- Sistema de prioridades (Baixa a Crítica)
- Upload de fotos
- Confirmação e resumo do reporte

### 📊 Dashboard
- KPIs principais (total, pendentes, resolvidos)
- Gráficos por tipo, status e bairro
- Linha do tempo de ocorrências
- Índice de urgência automático
- Exportação de relatórios (CSV e TXT)

### 🏷️ Tipos de Ocorrência
| Tipo | Descrição |
|------|-----------|
| 🕳️ Buraco | Buracos e irregularidades no asfalto |
| 💡 Iluminação | Problemas com iluminação pública |
| 🗑️ Lixo | Acúmulo de lixo ou entulho |
| 🌊 Alagamento | Pontos de alagamento |
| 🚶 Calçada | Problemas em calçadas |
| 🪧 Sinalização | Sinalização danificada ou ausente |
| 🌳 Árvore | Árvores caídas ou com risco |

---

## 🛠️ Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/mapaDigitalUrbano.git
cd mapaDigitalUrbano
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
cd src
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

---

## 📁 Estrutura do Projeto

```
mapaDigitalUrbano/
├── 📁 assets/              # Recursos estáticos (ícones, imagens)
├── 📁 data/
│   ├── 📁 raw/             # Dados brutos
│   │   ├── ocorrencias_mock.csv
│   │   ├── reportes.json
│   │   └── 📁 images/      # Fotos dos reportes
│   └── 📁 processed/       # Dados processados
├── 📁 docs/                # Documentação adicional
├── 📁 src/
│   ├── app.py              # Aplicação principal
│   ├── config.py           # Configurações centralizadas
│   ├── data_manager.py     # Gerenciador de dados (CRUD)
│   ├── map_utils.py        # Utilitários de mapas
│   ├── 📁 components/      # Componentes reutilizáveis
│   │   ├── __init__.py
│   │   └── ui_components.py
│   └── 📁 pages/           # Páginas da aplicação
│       ├── __init__.py
│       ├── mapa.py
│       ├── reportar.py
│       ├── dashboard.py
│       └── sobre.py
├── requirements.txt
└── README.md
```

---

## 🔧 Configuração

As configurações principais estão em `src/config.py`:

```python
# Localização padrão do mapa (Cacoal - RO)
MAP_CONFIG = {
    "center_lat": -11.4400,
    "center_lon": -61.4600,
    "zoom_start": 13,
}

# Personalizar tipos de ocorrência
TIPOS_OCORRENCIA = {
    "Buraco": {"cor": "#e74c3c", "icone": "road", ...},
    # Adicione novos tipos aqui
}

# Bairros disponíveis
BAIRROS = ["Centro", "Vista Alegre", ...]
```

---

## 👥 Usuários-Alvo

- **Moradores**: Reportam problemas do bairro
- **Líderes Comunitários**: Utilizam dados para reivindicações
- **Prefeituras**: Visualizam demandas e priorizam ações
- **Engenheiros**: Acessam dados para planejamento urbano

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja como:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

- **Projeto**: Mapa Digital Urbano
- **Comunidade**: Cacoal - RO

---

<div align="center">
  <strong>Feito com ❤️ para a comunidade</strong>
  <br>
  <sub>Transformando dados em ações para cidades melhores</sub>
</div>
