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
refresh_triggered = st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="auto_refresh")

st.title("🎯 XXXtreme Lightning Roulette com IA")
st.caption("Monitoramento ao vivo com inteligência artificial e destaque de acertos.")

# Carregamento inicial do histórico
if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

# Buscar novo resultado
resultado = fetch_latest_result()

if resultado:
    if resultado["timestamp"] not in st.session_state.historico["timestamp"].values:
        salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)
        novo_dado = pd.DataFrame([{
            "numero": resultado["number"],
            "timestamp": resultado["timestamp"],
            "lucky_numbers": ",".join(map(str, resultado["lucky_numbers"]))
        }])
        st.session_state.historico = pd.concat([st.session_state.historico, novo_dado], ignore_index=True)

# Previsões da IA
st.subheader("🧠 Previsões de IA (últimos 300 registros)")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)
numeros_previstos = [p["numero"] for p in previsoes]

# Último número sorteado
col1, col2 = st.columns(2)
with col1:
    if resultado:
        st.markdown(f"🔢 Último número sorteado: **{resultado['number']}**")
    else:
        st.markdown("🔢 Último número sorteado: *Carregando...*")

# Botão de download seguro (fora do refresh direto)
with col2:
    if not refresh_triggered:
        with open(CAMINHO_ARQUIVO, "rb") as file:
            st.download_button("⬇️ Baixar histórico", data=file, file_name="resultados.csv")

st.markdown("---")
st.subheader("📈 Resultados Recentes")

# Mostrar os últimos 10 resultados sem usar .style
tabela = st.session_state.historico.tail(10)[["numero", "timestamp"]].reset_index(drop=True)

for idx, row in tabela.iterrows():
    num = row["numero"]
    timestamp = row["timestamp"]
    if num in numeros_previstos:
        st.markdown(f"🟢 **{num}** – ⏱️ {timestamp}")
    else:
        st.markdown(f"{num} – ⏱️ {timestamp}")

# Salvar se houve acerto
if resultado:
    salvar_acerto(previsoes, resultado["number"])
