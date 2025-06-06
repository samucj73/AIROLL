import pandas as pd

def carregar_resultados(caminho):
    try:
        df = pd.read_csv(caminho, sep='|', header=None, names=['numero', 'lucky', 'timestamp'])
        df['numero'] = df['numero'].astype(str).str.strip()
        df['timestamp'] = df['timestamp'].astype(str).str.strip()
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['numero', 'lucky', 'timestamp'])
    except Exception as e:
        print(f"[Erro ao carregar resultados]: {e}")
        return pd.DataFrame(columns=['numero', 'lucky', 'timestamp'])

def salvar_acerto(acertos, caminho="acertos_ia.txt"):
    try:
        with open(caminho, 'a') as f:
            for a in acertos:
                linha = f"{a['numero']} | {a['cor']} | {a['range']}\n"
                f.write(linha)
    except Exception as e:
        print(f"[Erro ao salvar acertos]: {e}")
