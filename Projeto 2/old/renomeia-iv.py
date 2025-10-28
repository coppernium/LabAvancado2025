import os
import re

def renomear_arquivos(pasta):
    """
    Renomeia arquivos xlsx de LEDs em um formato padronizado.
    
    Exemplo:
    'LED 1 (azul) alta intensidade 2 - 11_09_Página1.xlsx'
    -> 'led1-a2-iv.xlsx'
    """
    for nome in os.listdir(pasta):
        if nome.endswith(".xlsx"):
            # Expressão regular para capturar LED e intensidade
            match = re.match(r"LED\s*(\d+).*alta intensidade\s*(\d+).*\.xlsx", nome, re.IGNORECASE)
            if match:
                led_num = match.group(1)
                intensidade = match.group(2)

                # Novo nome
                novo_nome = f"led{led_num}-a{intensidade}-iv.xlsx"

                # Caminhos completos
                caminho_antigo = os.path.join(pasta, nome)
                caminho_novo = os.path.join(pasta, novo_nome)

                # Renomear
                os.rename(caminho_antigo, caminho_novo)
                print(f"Renomeado: {nome} -> {novo_nome}")

# --- Exemplo de uso ---
pasta = 'Dados/IV-A-1'
renomear_arquivos(pasta)
