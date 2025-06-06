import streamlit as st
import pandas as pd
from coleta import fetch_latest_result, salvar_resultado_em_arquivo
from modelo_ia import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

CAMINHO_ARQUIVO = "historico_resultados.csv"
REFRESH_INTERVAL = 10  # segundos

# Auto-refresh a cada 10 segundos
st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="auto_refresh")

st.title("🎯 XXXtreme Lightning Roulette com IA")
st.caption("Monitoramento ao vivo com inteligência artificial e destaque de acertos.")

if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

resultado = fetch_latest_result()

if resultado:
    if resultado["timestamp"] not in st.session_state.historico["timestamp"].values:
        salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)
        st.session_state.historico = pd.concat([
            st.session_state.historico,
            pd.DataFrame([{
                "numero": resultado["number"],
                "timestamp": resultado["timestamp"],
                "lucky_numbers": ",".join(map(str, resultado["lucky_numbers"]))
            }])
        ], ignore_index=True)

st.subheader("🧠 Previsões de IA (últimos 300 registros)")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)

col1, col2 = st.columns(2)
with col1:
    st.write("🔢 Último número sorteado:", f"**{resultado['number']}**" if resultado else "Carregando...")

with col2:
    if st.button("⬇️ Baixar histórico"):
        with open(CAMINHO_ARQUIVO, "rb") as file:
            st.download_button("Clique para baixar", data=file, file_name="resultados.csv")

st.markdown("---")
st.subheader("📈 Resultados Recentes")

tabela = st.session_state.historico.tail(10)[["numero", "timestamp"]].reset_index(drop=True)

def destacar(val):
    return "background-color: lightgreen; font-weight: bold" if val in [p["numero"] for p in previsoes] else ""

st.dataframe(
    tabela.style.applymap(destacar, subset=["numero"]),
    use_container_width=True
)

# Salvar se houve acerto nas previsões
if resultado:
    salvar_acerto(previsoes, resultado["number"])
