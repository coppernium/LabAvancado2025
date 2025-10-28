import os
import pandas as pd

def converter_xlsx_para_csv(pasta):
    """
    Converte todos os arquivos .xlsx em uma pasta para .csv
    """
    # Garantir que a pasta existe
    if not os.path.exists(pasta):
        print(f"❌ A pasta '{pasta}' não existe!")
        return

    # Percorrer todos os arquivos da pasta
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith('.xlsx'):
            caminho_arquivo = os.path.join(pasta, arquivo)

            try:
                # Ler o arquivo Excel
                df = pd.read_excel(caminho_arquivo)

                # Nome do arquivo CSV
                nome_csv = os.path.splitext(arquivo)[0] + ".csv"
                caminho_csv = os.path.join(pasta, nome_csv)

                # Salvar em CSV
                df.to_csv(caminho_csv, index=False)
                print(f"✅ Convertido: {arquivo} → {nome_csv}")

            except Exception as e:
                print(f"⚠️ Erro ao converter '{arquivo}': {e}")

# ======== COMO USAR =========
# Coloque o caminho completo da pasta
pasta_alvo = "Dados/IV-A-1"
converter_xlsx_para_csv(pasta_alvo)
