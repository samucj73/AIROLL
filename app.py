import streamlit as st
import pandas as pd
from coleta import fetch_latest_result, salvar_resultado_em_arquivo
from modelo_ia import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

CAMINHO_ARQUIVO = "historico_resultados.csv"

st.title("🎯 XXXtreme Lightning Roulette com IA")
st.caption("Monitoramento ao vivo com inteligência artificial.")

if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

# Buscar novo resultado
resultado = fetch_latest_result()

# Verifica se é um novo número
if resultado:
    novo_timestamp = resultado["timestamp"]
    historico_ts = st.session_state.historico["timestamp"].values

    if novo_timestamp not in historico_ts:
        # Salva novo resultado
        salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)

        # Atualiza histórico em cache
        novo = pd.DataFrame([{
            "numero": resultado["number"],
            "timestamp": novo_timestamp,
            "lucky_numbers": ",".join(map(str, resultado["lucky_numbers"]))
        }])
        st.session_state.historico = pd.concat([st.session_state.historico, novo], ignore_index=True)

        # Força refresh para atualizar visualmente a interface
        st.experimental_rerun()

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

for i, row in recentes.iterrows():
    num = row["numero"]
    ts = row["timestamp"]
    if num in numeros_previstos:
        st.markdown(f"🟢 **{num}** – ⏱ {ts}")
    else:
        st.markdown(f"{num} – ⏱ {ts}")

# Registrar acerto
if resultado:
    salvar_acerto(previsoes, resultado["number"])
