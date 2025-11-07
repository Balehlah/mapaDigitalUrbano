import pandas as pd

def carregar_dados(caminho_csv: str):
    """
    Carrega o dataset de ocorrências comunitárias.
    """
    try:
        df = pd.read_csv(caminho_csv)
    except Exception as e:
        raise Exception(f"Erro ao carregar o arquivo CSV: {e}")

    # Verificação básica
    colunas_necessarias = ["latitude", "longitude", "tipo_problema", "descricao", "bairro"]
    for col in colunas_necessarias:
        if col not in df.columns:
            raise Exception(f"A coluna '{col}' está faltando no arquivo CSV.")

    return df
