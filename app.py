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

with st.spinner('Loading data...'):
    df = load_data()
st.success("Dados carregados corretamente!")

############# filtro da barra lateral ########################
# barra lateral com o nome
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis_df = sorted(df['ano'].unique())
anos_selected = st.sidebar.multiselect('Anos', anos_disponiveis_df, default= max(anos_disponiveis_df))

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
##### df filtrado com base nos filtros criados acima
df_filtrado = df[
    (df['ano'].isin(anos_selected)) &
    (df['nivel_experiencia'].isin(senioridade_selected)) &
    (df['tipo_contratacao'].isin(contrato_selected)) &
    (df['tamanho_empresa'].isin(tamanho_empresa_selected))
]

#### formatacao pagina inicial

st.title('🎲 Dashboard: Analise de Salários na Area de Dados')
st.markdown('Explore as informações. Lembresse de fazer os filtros na aba lateral')

##### kpis

st.subheader('Metricas de Salarios Anuais (USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['salario_em_usd'].mean()
    salario_max = df_filtrado['salario_em_usd'].max()
    total_registros = df_filtrado.shape[0]
    ## moda do cargo comum pegando o 1 item
    cargo_mais_comum = df_filtrado['cargo'].mode()[0]
else:
    salario_medio,salario_max, total_registros, cargo_mais_comum = 0,0,0,""

# cards na home
col1, col2, col3, col4= st.columns(4)

col1.metric("Salario Medio", f"${salario_medio:,.0f}")
col2.metric("Maior Salario", f'${salario_max:,.0f}')
col3.metric("Total de Campos", f"{total_registros:,}")
col4.metric("Cargo Mais Comum", cargo_mais_comum)
st.markdown("---")
##################

###insercao dos gratifocs interativos
st.subheader("Gráficos")

#with abre a coluna onde o grafico vai ser plotado

col1_grap1, col2_grap2 = st.columns(2)

with col1_grap1:
    if not df_filtrado.empty:
        top_cargos = df.groupby('cargo')['salario_em_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        graf_cargos = px.bar(
            top_cargos,
            x='salario_em_usd',
            y='cargo',
            orientation='h',
            title='Top 10 Salários - Média (USD)',
            labels={'salario_em_usd': "Media salarial", 'cargo': ""}

        )
        graf_cargos.update_layout(title_x=0.5, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(graf_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")


