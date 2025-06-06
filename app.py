import streamlit as st
import pandas as pd
from coleta import fetch_latest_result, salvar_resultado_em_arquivo
from modelo_ia import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

CAMINHO_ARQUIVO = "historico_resultados.csv"

# Inicializa o histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

# Verifica novo resultado
resultado = fetch_latest_result()
novo_detectado = False

if resultado:
    if resultado["timestamp"] not in st.session_state.historico["timestamp"].values:
        salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)
        novo = pd.DataFrame([{
            "numero": resultado["number"],
            "timestamp": resultado["timestamp"],
            "lucky_numbers": ",".join(map(str, resultado["lucky_numbers"]))
        }])
        st.session_state.historico = pd.concat([st.session_state.historico, novo], ignore_index=True)
        novo_detectado = True

# Se um novo número foi detectado, forçamos um refresh
if novo_detectado:
    st_autorefresh(interval=100, key="forcar_refresh", limit=1)
else:
    st_autorefresh(interval=10_000, key="refresh_regular")

# Interface
st.title("🎯 XXXtreme Lightning Roulette com IA")
st.caption("Monitoramento ao vivo com inteligência artificial e destaque de acertos.")

# Previsões da IA
st.subheader("🧠 Previsões de IA (últimos 300 registros)")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)
numeros_previstos = [p["numero"] for p in previsoes]

# Último sorteio
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"🔢 Último número sorteado: **{resultado['number']}**" if resultado else "Carregando...")

with col2:
    if st.button("⬇️ Baixar histórico"):
        with open(CAMINHO_ARQUIVO, "rb") as file:
            st.download_button("Clique para baixar", data=file, file_name="resultados.csv")

st.markdown("---")
st.subheader("📈 Últimos 10 Resultados")

recentes = st.session_state.historico.tail(10)[["numero", "timestamp"]].reset_index(drop=True)

for _, row in recentes.iterrows():
    num = row["numero"]
    ts = row["timestamp"]
    if num in numeros_previstos:
        st.markdown(f"🟢 **{num}** – ⏱ {ts}")
    else:
        st.markdown(f"{num} – ⏱ {ts}")

# Registrar acerto
if resultado:
    salvar_acerto(previsoes, resultado["number"])
