import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard Salários Globais - Dados",
    page_icon="📊",
    layout="wide",
)
@st.cache_data
def load_data():
    return pd.read_parquet('data/dados_limpos.parquet')

data_load_state = st.text('Loading data...')
df = load_data()
data_load_state.text("Done!")

############# filtro da barra lateral ########################
# barra lateral com o nome
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis_df = sorted(df['ano'].unique())
anos_selected = st.sidebar.multiselect('Anos', anos_disponiveis_df, default=[])

# Filtro de senioridade

senioridade = sorted(df['nivel_experiencia'].unique())
senioridade_selected = st.sidebar.multiselect('Nivel de Experiência', senioridade, default=senioridade)

# Filtro tipo de trabalho
tipo_contrato = sorted(df['tipo_contratacao'].unique())
contrato_selected = st.sidebar.multiselect('Tipo de Contratação', tipo_contrato, default=tipo_contrato)

# filtro tamanho da empresa
tamanho_companhia = sorted(df['tamanho_empresa'].unique())
tamanho_empresa_selected = st.sidebar.multiselect('Tamanho da Empresa', tamanho_companhia, default=tamanho_companhia)

################################################################