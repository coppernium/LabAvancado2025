import numpy as np
from scipy import optimize
import os
import pandas as pd
from pathlib import Path

def encontrar_x0(df):
    """
    Encontra o ponto de transição (x0) em um ajuste piecewise linear.
    
    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame contendo os dados.
    coluna_x : str
        Nome da coluna correspondente ao eixo x.
    coluna_y : str
        Nome da coluna correspondente ao eixo y.

    Retorna
    -------
    float
        O valor de x0 (ponto de transição).
    """
    coluna_x='tensao (V) (0,001)'
    coluna_y='corrente (mA) (0,0001)'

    # Extrair colunas como numpy arrays
    x = df[coluna_x].to_numpy()
    y = df[coluna_y].to_numpy()

    # Arredonda os valores
    x = np.round(x, 2)
    y = np.round(y, 3)

    # Função piecewise linear
    def piecewise_linear(x, x0, y0, k1, k2):
        return np.piecewise(
            x, 
            [x < x0, x >= x0], 
            [lambda x: k1*x + y0 - k1*x0, 
             lambda x: k2*x + y0 - k2*x0]
        )

    # Ajuste (chute inicial)
    p0 = [np.median(x), np.median(y), 0.1, 1]
    p, _ = optimize.curve_fit(piecewise_linear, x, y, p0=p0)

    # Extrair parâmetros
    x0, y0, k1, k2 = p

    return x0



def extrair_pico_variancia(df):
    """
    Encontra o ponto x_max e a variância da gaussiana ajustada a dados experimentais.

    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame contendo duas colunas: [x, y].

    Retorna
    -------
    tuple
        (x_max, variancia_fit) onde:
        - x_max: posição do pico (float)
        - variancia_fit: variância ajustada da gaussiana (float)
    """

    # Extrair colunas
    x = df.iloc[:, 0].to_numpy()
    y = df.iloc[:, 1].to_numpy()

    # Normalizar y
    y = (y - np.min(y)) / (np.max(y) - np.min(y))

    # Pico
    idx_max = np.argmax(y)
    x_max, y_max = x[idx_max], y[idx_max]

    # --------- 1) Estimativa via FWHM ---------
    half_max = y_max / 2
    indices = np.where(y >= half_max)[0]
    x_left, x_right = x[indices[0]], x[indices[-1]]
    FWHM = x_right - x_left
    sigma_est = FWHM / (2 * np.sqrt(2 * np.log(2)))

    # --------- 2) Ajuste de curva (Gaussiana) ---------
    def gaussiana(x, A, mu, sigma):
        return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

    p0 = [y_max, x_max, sigma_est]
    popt, _ = curve_fit(gaussiana, x, y, p0=p0)

    _, mu_fit, sigma_fit = popt
    var_fit = sigma_fit**2

    return x_max, var_fit

def processar_pares(pasta_iv, pasta_espectro, arquivo_saida):
    resultados = []

    for arquivo_iv in os.listdir(pasta_iv):
        # Aceita tanto .txt quanto .csv
        if not (arquivo_iv.lower().endswith("-iv.txt") or arquivo_iv.lower().endswith("-iv.csv")):
            continue

        base_name = arquivo_iv.replace("-iv.txt", "").replace("-iv.csv", "")
        arquivo_espectro = f"{base_name}-espectro.txt"

        caminho_iv = Path(pasta_iv) / arquivo_iv
        caminho_espectro = Path(pasta_espectro) / arquivo_espectro

        if not caminho_espectro.exists():
            print(f"⚠️ Espectro não encontrado para {base_name}, pulando...")
            continue

        # ==== Leitura dos arquivos ====
        print(f"Processando {base_name}...")

        # Descubra o separador do IV
        with open(caminho_iv, 'r') as f:
            print("Primeira linha do IV:", f.readline())

        # df_iv = pd.read_csv(caminho_iv, sep=";", decimal=",")  # Ajuste o sep conforme necessário
        df_iv = pd.read_csv(caminho_iv, sep=",", decimal=".", quotechar='"')
        print("Colunas IV:", df_iv.columns)

        df_espectro = pd.read_csv(caminho_espectro, sep="\t", header=None, decimal=",")

        # ==== Cálculos ====
        from scipy.optimize import curve_fit
        x0 = encontrar_x0(df_iv)
        x_max, var_fit = extrair_pico_variancia(df_espectro)

        resultados.append({
            "led": base_name,
            "x0": x0,
            "x_max": x_max,
            "var_fit": var_fit
        })

    # ==== Salvando resultados ====
    if resultados:
        df_resultados = pd.DataFrame(resultados)
        df_resultados.to_csv(arquivo_saida, index=False, sep=",")
        print(f"✅ Resultados salvos em {arquivo_saida}")
    else:
        print("⚠ Nenhum resultado gerado! Verifique os nomes dos arquivos e separadores.")


pasta_iv = "Dados/IV-A-2"
pasta_espectro = "Dados/Espectro-A-2"
pasta_saida = "/Dados/Resultados/a2-resultados.csv"
processar_pares(pasta_iv, pasta_espectro, pasta_saida)