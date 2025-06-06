import streamlit as st
import pandas as pd
import os
from ia_modelo import prever_proximos_numeros_com_ia
from utils import salvar_acerto
from streamlit_autorefresh import st_autorefresh

ARQUIVO = 'historico_resultados.csv'
ACERTOS = 'acertos_previsao.csv'

st_autorefresh(interval=15000, limit=None, key="auto-refresh")

st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")
st.markdown("""
    <style>
    .main { padding-bottom: 100px; }
    h1 { text-align: center; }
    .highlight { font-size: 24px; font-weight: bold; color: green; text-align: center; }
    footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background-color: #f0f0f5; text-align: center; padding: 10px;
        font-size: 14px; color: #888;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎯 XXXtreme Lightning Roulette – Monitoramento em Tempo Real</h1>", unsafe_allow_html=True)

if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    df = df.sort_values(by="timestamp", ascending=False).reset_index(drop=True)

    st.subheader("📊 Últimos Resultados Capturados")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("🤖 Números previstos pela IA")
    previsoes = prever_proximos_numeros_com_ia(ARQUIVO, qtd=5)

    if previsoes:
        col1, col2, col3 = st.columns(3)
        for i, p in enumerate(previsoes):
            col = [col1, col2, col3][i % 3]
            col.markdown(f"<div class='highlight'>🎯 {p['numero']}</div>", unsafe_allow_html=True)

        numero_real = int(df.iloc[0]['numero'])
        timestamp_real = df.iloc[0]['timestamp']
        acertos = [p['numero'] for p in previsoes if p['numero'] == numero_real]

        if acertos:
            st.success(f"✅ A IA acertou o número sorteado: {numero_real}")
            salvar_acerto(numero_previsto=numero_real, numero_real=numero_real, timestamp=timestamp_real)
        else:
            st.info(f"🔍 Último número sorteado: {numero_real}")
    else:
        st.warning("Aguardando dados suficientes para previsão...")
else:
    st.warning("Arquivo de dados ainda não criado. Aguarde a coleta inicial.")

if os.path.exists(ARQUIVO):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar resultados (.csv)", csv, file_name="resultados.csv", mime='text/csv')

st.markdown("""
    <footer>
        Monitoramento ao vivo da Roleta XXXtreme Lightning 🎲 Desenvolvido com ❤️
    </footer>
""", unsafe_allow_html=True)
