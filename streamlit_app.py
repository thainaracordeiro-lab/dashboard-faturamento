import streamlit as st
import pandas as pd
import plotly.express as px

# === Configuração da página ===
st.set_page_config(page_title="Faturamento por Colaborador", layout="wide")

# === Carregar os dados ===
df = pd.read_excel("Python.xlsx")

# Padronizar nomes de colunas
df.columns = df.columns.str.strip().str.replace(".", " ", regex=False).str.title()
df.rename(columns={"Faturamento Do Serviço": "Faturamento"}, inplace=True)
df["Faturamento"] = pd.to_numeric(df["Faturamento"], errors="coerce").fillna(0)

# === Título ===
st.title("📊 Dashboard de Faturamento por Colaborador")

# === Filtros ===
col1, col2, col3 = st.columns(3)

with col1:
    grupo = st.selectbox("Grupo:", options=[""] + sorted(df["Grupo"].dropna().unique().tolist()))

with col2:
    classificacao = st.selectbox("Classificação:", options=[""] + sorted(df["Classificação"].dropna().unique().tolist()))

with col3:
    regime = st.selectbox("Regime:", options=[""] + sorted(df["Regime"].dropna().unique().tolist()))

# === Aplicar filtros ===
dff = df.copy()
if grupo:
    dff = dff[dff["Grupo"] == grupo]
if classificacao:
    dff = dff[dff["Classificação"] == classificacao]
if regime:
    dff = dff[dff["Regime"] == regime]

# === KPIs ===
total_faturamento = dff["Faturamento"].sum()
total_colaboradores = dff["Colaborador"].nunique()

st.markdown(f"### 💰 Faturamento Total: R$ {total_faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.markdown(f"#### 👥 Colaboradores Ativos: {total_colaboradores}")

# === Gráficos ===
col1, col2 = st.columns(2)

with col1:
    ranking = dff.groupby("Colaborador")["Faturamento"].sum().reset_index().sort_values(by="Faturamento", ascending=False)
    fig_ranking = px.bar(
        ranking,
        x="Colaborador",
        y="Faturamento",
        title="Ranking de Faturamento por Colaborador",
        color_discrete_sequence=["#003366"]
    )
    st.plotly_chart(fig_ranking, use_container_width=True)

with col2:
    faturamento_grupo = dff.groupby("Grupo")["Faturamento"].sum().reset_index()
    fig_grupo = px.bar(
        faturamento_grupo,
        x="Grupo",
        y="Faturamento",
        title="Faturamento por Grupo",
        color_discrete_sequence=["#006699"]
    )
    st.plotly_chart(fig_grupo, use_container_width=True)

# === Faturamento por Classificação ===
faturamento_classificacao = dff.groupby("Classificação")["Faturamento"].sum().reset_index()
fig_classificacao = px.bar(
    faturamento_classificacao,
    x="Classificação",
    y="Faturamento",
    title="Faturamento por Classificação",
    color_discrete_sequence=["#0099CC"]
)
st.plotly_chart(fig_classificacao, use_container_width=True)
