import streamlit as st
import pandas as pd
import time
import os

from coleta import fetch_latest_result, salvar_resultado_em_arquivo
from modelo_ia import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

CAMINHO_ARQUIVO = "historico_resultados.csv"
REFRESH_INTERVAL = 10  # segundos

st.title("🎯 XXXtreme Lightning Roulette com IA")
st.caption("Monitoramento ao vivo com inteligência artificial e destaque de acertos.")

# Garante que o arquivo exista
if not os.path.exists(CAMINHO_ARQUIVO):
    pd.DataFrame(columns=["numero", "timestamp", "lucky_numbers"]).to_csv(CAMINHO_ARQUIVO, index=False)

if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

# 🔄 Coleta o último resultado
resultado = fetch_latest_result()

if resultado and resultado["timestamp"] not in st.session_state.historico["timestamp"].values:
    salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)
    novo_df = pd.DataFrame([{
        "numero": resultado["number"],
        "timestamp": resultado["timestamp"],
        "lucky_numbers": ",".join(map(str, resultado["lucky_numbers"]))
    }])
    st.session_state.historico = pd.concat([st.session_state.historico, novo_df], ignore_index=True)
    salvar_acerto(prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5), resultado["number"])
    time.sleep(1)
    st.experimental_rerun()

st.subheader("🧠 Previsões de IA (últimos 300 registros)")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)

col1, col2 = st.columns(2)
with col1:
    st.write("🔢 Último número sorteado:", f"**{resultado['number']}**" if resultado else "Carregando...")

with col2:
    with open(CAMINHO_ARQUIVO, "rb") as file:
        st.download_button("⬇️ Baixar histórico", data=file, file_name="resultados.csv")

st.markdown("---")
st.subheader("📈 Resultados Recentes")

# Tabela com os últimos resultados
tabela = st.session_state.historico.tail(10)[["numero", "timestamp"]].reset_index(drop=True)

def destacar(val):
    return "background-color: lightgreen; font-weight: bold" if int(val) in [p["numero"] for p in previsoes] else ""

st.dataframe(
    tabela.style.applymap(destacar, subset=["numero"]),
    use_container_width=True
)
