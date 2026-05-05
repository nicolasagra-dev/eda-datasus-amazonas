from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = ROOT / "data" / "processed"


st.set_page_config(
    page_title="EDA DataSUS Amazonas",
    layout="wide",
)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    municipios = pd.read_csv(PROCESSED_DIR / "municipios_tratados.csv")
    faixa = pd.read_csv(PROCESSED_DIR / "internacoes_faixa_etaria_ano_am_limpo.csv")
    ranking = pd.read_csv(PROCESSED_DIR / "ranking_volume_vs_taxa.csv")
    return municipios, faixa, ranking


def format_int(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def format_float(value: float) -> str:
    return f"{value:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


municipios, faixa, ranking = load_data()

st.title("EDA DataSUS: Morbidade Hospitalar no Amazonas")
st.caption("SIH/SUS via TABNET, com população municipal do IBGE como denominador populacional.")

anos = sorted(municipios["ano"].unique())
municipios_lista = sorted(municipios["municipio"].unique())
faixas_lista = [item for item in faixa["faixa_etaria"].dropna().unique()]

with st.sidebar:
    st.header("Filtros")
    anos_selecionados = st.multiselect("Ano", anos, default=anos)
    municipios_selecionados = st.multiselect(
        "Município",
        municipios_lista,
        default=municipios_lista[:10],
    )
    faixas_selecionadas = st.multiselect(
        "Faixa etária",
        faixas_lista,
        default=faixas_lista,
    )

dados_filtrados = municipios[
    municipios["ano"].isin(anos_selecionados)
    & municipios["municipio"].isin(municipios_selecionados)
].copy()
faixa_filtrada = faixa[
    faixa["ano"].isin(anos_selecionados)
    & faixa["faixa_etaria"].isin(faixas_selecionadas)
].copy()

if dados_filtrados.empty:
    st.warning("Selecione pelo menos um ano e um município para visualizar os indicadores.")
    st.stop()

total_internacoes = dados_filtrados["internacoes"].sum()
total_obitos = dados_filtrados["obitos"].sum()
taxa_mortalidade = total_obitos / total_internacoes * 100 if total_internacoes else 0
internacoes_100k = (
    dados_filtrados["internacoes"].sum() / dados_filtrados["populacao"].sum() * 100_000
    if dados_filtrados["populacao"].notna().any()
    else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Internações", format_int(total_internacoes))
col2.metric("Óbitos", format_int(total_obitos))
col3.metric("Taxa de mortalidade", f"{format_float(taxa_mortalidade)}%")
col4.metric("Internações por 100 mil hab./ano", format_float(internacoes_100k))

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Internações por ano")
    serie_ano = dados_filtrados.groupby("ano", as_index=False)["internacoes"].sum()
    st.line_chart(serie_ano, x="ano", y="internacoes")

with col_b:
    st.subheader("Top municípios por internações")
    top_municipios = (
        dados_filtrados.groupby("municipio", as_index=False)["internacoes"]
        .sum()
        .sort_values("internacoes", ascending=False)
        .head(10)
    )
    st.bar_chart(top_municipios, x="municipio", y="internacoes", horizontal=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Internações por faixa etária")
    if faixa_filtrada.empty:
        st.info("Selecione ao menos uma faixa etária.")
    else:
        resumo_faixa = (
            faixa_filtrada.groupby("faixa_etaria", as_index=False)["internacoes"]
            .sum()
            .sort_values("internacoes", ascending=False)
        )
        st.bar_chart(resumo_faixa, x="faixa_etaria", y="internacoes", horizontal=True)

with col_d:
    st.subheader("Volume absoluto x taxa anual por 100 mil")
    ranking_preview = ranking[
        [
            "municipio",
            "internacoes",
            "internacoes_por_100k",
            "rank_volume",
            "rank_taxa_100k",
        ]
    ].sort_values("rank_taxa_100k")
    st.dataframe(ranking_preview.head(15), hide_index=True, width="stretch")

st.subheader("Dados filtrados")
st.dataframe(
    dados_filtrados[
        [
            "codigo_municipio",
            "municipio",
            "ano",
            "populacao",
            "internacoes",
            "internacoes_por_100k",
            "obitos",
            "taxa_mortalidade",
        ]
    ].sort_values(["ano", "municipio"]),
    hide_index=True,
    width="stretch",
)
