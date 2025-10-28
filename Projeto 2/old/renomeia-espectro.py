import os
import re

def renomear_arquivos(pasta):
    """
    Renomeia arquivos no formato:
    'led1 (azul) a1.txt' -> 'led1-a1-espectro.txt'
    'led1 (roxo) b2.txt' -> 'led1-b2-espectro.txt'
    """
    for nome in os.listdir(pasta):
        if nome.endswith(".txt"):
            # Expressão regular para capturar:
            # - Número do LED
            # - Letra (a, b, c...) e número subsequente
            match = re.match(r"led\s*(\d+)\s*\(.*?\)\s*([a-z])(\d+)\.txt", nome, re.IGNORECASE)
            if match:
                led_num = match.group(1)       # Número do LED
                letra = match.group(2).lower() # Letra (a, b, c...) - normalizada para minúscula
                intensidade = match.group(3)   # Número depois da letra

                # Novo nome
                novo_nome = f"led{led_num}-{letra}{intensidade}-espectro.txt"

                # Caminhos completos
                caminho_antigo = os.path.join(pasta, nome)
                caminho_novo = os.path.join(pasta, novo_nome)

                # Renomear
                os.rename(caminho_antigo, caminho_novo)
                print(f"Renomeado: {nome} -> {novo_nome}")
            else:
                print(f"Nome não corresponde ao padrão: {nome}")

# --- Exemplo de uso ---
pasta = 'Dados/Espectro-B-2'
renomear_arquivos(pasta)
