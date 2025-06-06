import streamlit as st
import time
import os
from ia_modelo import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados
from coleta import fetch_latest_result, salvar_resultado_em_arquivo

CAMINHO_ARQUIVO = "historico_resultados.txt"
CAMINHO_ACERTOS = "acertos_ia.txt"

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

st.title("🎯 XXXtreme Lightning Roulette - Monitoramento com IA")
st.markdown("Sistema inteligente para capturar, analisar e prever números.")

# Inicialização do histórico
if "historico" not in st.session_state:
    st.session_state.historico = carregar_resultados(CAMINHO_ARQUIVO)

# 🔄 Captura automática
resultado = fetch_latest_result()
novo = False

# if resultado:
    if resultado["timestamp"] not in st.session_state.historico["timestamp"].values:
        salvar_resultado_em_arquivo([resultado], caminho=CAMINHO_ARQUIVO)
        if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=["numero", "lucky_numbers", "timestamp"])
        st.session_state.historico = pd.concat([st.session_state.historico, pd.DataFrame([{
            "numero": resultado["number"],
            "lucky": ",".join(map(str, resultado["lucky_numbers"])),
            "timestamp": resultado["timestamp"]
        }])], ignore_index=True)
        novo = True

# 🔍 Exibir últimos resultados
st.subheader("🧾 Últimos 10 Resultados")
ultimos = st.session_state.historico.tail(10)
st.table(ultimos)

# 📈 IA - Previsão com base no histórico
st.subheader("🤖 Previsão da IA")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)

if previsoes:
    col1, col2 = st.columns(2)
    with col1:
        for i, p in enumerate(previsoes):
            st.markdown(
                f"<div style='background-color:#DFF0D8;padding:10px;margin:5px;border-radius:5px;'>"
                f"<strong>Previsão {i+1}:</strong> 🎯 Número <strong>{p['numero']}</strong> | "
                f"Cor: {p['cor']} | Tipo: {p['range']}</div>",
                unsafe_allow_html=True
            )

    # 🎯 Verificar acertos
    ult_num = int(ultimos.iloc[-1]["numero"])
    acertou = [p for p in previsoes if int(p["numero"]) == ult_num]

    if acertou:
        st.success(f"✅ A IA acertou o número: {ult_num}!")
        salvar_acerto(acertou, caminho=CAMINHO_ACERTOS)

# 📥 Botão para baixar histórico
st.subheader("📁 Download de Resultados")
if os.path.exists(CAMINHO_ARQUIVO):
    with open(CAMINHO_ARQUIVO, "rb") as file:
        st.download_button("📥 Baixar histórico de resultados", data=file, file_name="resultados.txt")
else:
    st.warning("⚠️ O arquivo de resultados ainda não foi criado.")

# 🔁 Auto-refresh visual
st.markdown("<hr><center><small>Atualizando automaticamente a cada novo número coletado</small></center>", unsafe_allow_html=True)
st.experimental_rerun() if novo else time.sleep(5)
