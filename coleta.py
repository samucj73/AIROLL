import requests
import csv
import os

API_URL = "https://api.casinoscores.com/svc-evolution-game-events/api/xxxtremelightningroulette/latest"
HEADERS = {"User-Agent": "Mozilla/5.0"}
ARQUIVO = "historico_resultados.csv"

def fetch_latest_result():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            result = data.get("result", {})
            outcome = result.get("outcome", {})
            lucky_list = result.get("luckyNumbersList", [])

            number = outcome.get("number")
            timestamp = data.get("startedAt")
            lucky_numbers = [item["number"] for item in lucky_list]

            return {"numero": number, "lucky_numbers": lucky_numbers, "timestamp": timestamp}
    except:
        return None

def salvar_resultado_em_arquivo(resultado):
    if not resultado:
        return

    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['numero', 'lucky_numbers', 'timestamp'])

    with open(ARQUIVO, 'r') as f:
        linhas = f.readlines()
        if any(str(resultado["timestamp"]) in linha for linha in linhas):
            return  # já salvo

    with open(ARQUIVO, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            resultado["numero"],
            ",".join(map(str, resultado["lucky_numbers"])),
            resultado["timestamp"]
        ])
