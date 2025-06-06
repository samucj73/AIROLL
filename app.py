import streamlit as st
import pandas as pd
import os
from ia_modelo import prever_proximos_numeros_com_ia
from utils import salvar_acerto, carregar_resultados
from streamlit_autorefresh import st_autorefresh

# ✅ Configuração da página - DEVE SER A PRIMEIRA INSTRUÇÃO Streamlit
st.set_page_config(page_title="XXXtreme Lightning Roulette", layout="centered")

# ✅ Atualização automática a cada 15 segundos
st_autorefresh(interval=15000, limit=None, key="auto-refresh")

# ✅ Título
st.title("🎰 XXXtreme Lightning Roulette - Monitoramento em Tempo Real")

# ✅ Caminho do arquivo de histórico
CAMINHO_ARQUIVO = 'historico_resultados.txt'

# ✅ Carregar dados salvos
df = carregar_resultados(CAMINHO_ARQUIVO)

# ✅ Exibir últimos resultados capturados
st.subheader("🧾 Últimos Resultados Capturados")
if not df.empty:
    ultimos = df.tail(10)[['numero', 'timestamp']]
    st.dataframe(ultimos.rename(columns={'numero': 'Número Sorteado', 'timestamp': 'Horário'}), use_container_width=True)
else:
    st.info("Nenhum resultado ainda capturado.")

# ✅ IA: Prever próximos números
st.subheader("🧠 Números Previstos pela IA")
previsoes = prever_proximos_numeros_com_ia(CAMINHO_ARQUIVO, qtd=5)

if previsoes:
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("🔮 **Previsões:**")
        for prev in previsoes:
            st.markdown(f"<span style='font-size: 24px; color: blue;'>{prev['numero']}</span>", unsafe_allow_html=True)

    with col2:
        # Verificar se algum número previsto foi sorteado recentemente
        ultimos_numeros = df['numero'].astype(int).tail(10).tolist()
        acertos = [p for p in previsoes if p['numero'] in ultimos_numeros]

        if acertos:
            st.success(f"✅ **Acertos recentes da IA:** {[a['numero'] for a in acertos]}")
            salvar_acerto(acertos)
        else:
            st.warning("Nenhum acerto recente.")
else:
    st.info("IA ainda não fez previsões.")

# ✅ Botão para download do histórico completo
st.subheader("⬇️ Download do Histórico")
with open(CAMINHO_ARQUIVO, "rb") as file:
    st.download_button("📥 Baixar histórico de resultados", data=file, file_name="resultados.txt")

# ✅ Rodapé
st.markdown("---")
st.markdown("<center><small>App desenvolvido para monitorar e prever resultados da XXXtreme Lightning Roulette ⚡</small></center>", unsafe_allow_html=True)
