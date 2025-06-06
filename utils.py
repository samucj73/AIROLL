import csv
import os

def salvar_acerto(numero_previsto, numero_real, timestamp, caminho='acertos_previsao.csv'):
    existe = os.path.exists(caminho)
    with open(caminho, 'a', newline='') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['numero_previsto', 'numero_real', 'timestamp'])
        writer.writerow([numero_previsto, numero_real, timestamp])
