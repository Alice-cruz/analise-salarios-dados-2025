# %%
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
#import numpy as np
import plotly.express as px

# link base de dados
df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

# renomeando colunas para ptbr
df = df.rename(columns={
    "work_year": "ano",
    "experience_level": "nivel_experiencia",
    "employment_type": "tipo_contratacao",
    "job_title": "cargo",
    "salary": "salario",
    "salary_currency": "moeda_salario",
    "salary_in_usd": "salario_em_usd",
    "employee_residence": "residencia_funcionario",
    "remote_ratio": "proporcao_remoto",
    "company_locatison": "local_empresa",
    "company_size": "tamanho_empresa"
})

#aqui é a contagem das linhas e colunas
linhas, colunas = df.shape[0], df.shape[1]
#print(f"Linhas: {linhas}, Colunas: {colunas}")

## funcao para alterar a tabela em lote ela recebe uma coluna que vamos modificar e um dicinario com os novos dados
def alterar_tabela(coluna, dicionario):
    df[coluna] = df[coluna].replace(dicionario)

## dicionario onde serao criadas as chaves para substituir os valores
dict_pares_para_substituicao = {
    "nivel_experiencia" :{
        "EN": "Junior",
        "MI": "Pleno",
        "SE": "Senior",
        "EX": "Executive"
    },
    "tipo_contratacao" :{
        "FT": "Full-time",
        "CT": "Contract",
        "PT": "Part-time",
        "FL": "Freelance"
    },
    "proporcao_remoto" : {
        0 : "on-site",
        50: "hybrid",
        100: "remote"
    },
    "tamanho_empresa" : {
        "L": "Large",
        "M": "Medium",
        "S": "Small"
    }
}

for coluna, dicionario in dict_pares_para_substituicao.items():
    alterar_tabela(coluna, dicionario)

## medidas estatisticas
df["proporcao_remoto"].value_counts()

df.describe(include="object")

# mostra as linhas que possuem valores vazios
df[df.isnull().any(axis=1)]

# removemos valores vazio, são poucos e nao fazem muita diferenca
df_limpo = df.dropna()
df_limpo.isnull().sum()

df_limpo = df_limpo.assign(ano=df_limpo["ano"].astype('int64'))



#### cria um csv para ser encaminhado 
df_limpo.to_csv('dados_limpos.csv', index=False)

##### parquet para o streamlit
df_limpo.to_parquet('dados_limpos.parquet', index=False)





####### criando gráficos ###################
# sns.barplot(data=df_limpo, x='nivel_experiencia', y='salario_em_usd', estimator='median')


# plt.figure(figsize=(8,6))
# sns.barplot(data=df_limpo, x='nivel_experiencia', y='salario_em_usd', estimator=np.mean)
# plt.title('salario medio senioridade em USD')
# plt.xlabel('senioridade')
# plt.ylabel('salario medio (USD)')
# plt.show()

# ordem_salarios = df_limpo.groupby('nivel_experiencia')['salario_em_usd'].mean().sort_values(ascending=True).index
# ordem_salarios

# plt.figure(figsize=(7,9))
# grafico_salarios_em_barras = sns.barplot(data=df_limpo, x='nivel_experiencia', y='salario_em_usd', estimator=np.mean,  order=ordem_salarios)
# plt.show()

# plt.figure(figsize=(8,4))
# sns.histplot(data=df_limpo, x='salario_em_usd', bins=50, kde=True)
# plt.title('distribuicao dos salarios (USD)')
# plt.show()


# plt.figure(figsize=(8,6))
# sns.boxplot(x=df_limpo['salario_em_usd'])
# plt.title('box plot salarios')
# plt.show()


# ordem = ['Senior', 'Pleno', 'Junior', 'Executive']
# plt.figure(figsize=(8,6))
# sns.boxplot(x='nivel_experiencia', data=df_limpo, y='salario_em_usd', order=ordem)


# #### grafico interativo com o plotlty
# remoto_contagem = df_limpo['proporcao_remoto'].value_counts().reset_index()
# remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

# fig = px.pie(
#     remoto_contagem,
#     names='tipo_trabalho',
#     values='quantidade',
#     title='Proporção dos Tipos de Trabalho',
#     hole=0.5  # opcional: transforma em donut chart
# )
# fig.update_traces(textinfo='percent+label')
# fig.show()


# df_ds_cargo = df_limpo[df_limpo['cargo'] == 'Data Scientist']
# pais_frequencia_media = df_ds_cargo.groupby('residencia_funcionario')['salario_em_usd'].mean().sort_values(ascending=False).reset_index()

# sns.barplot(x='residencia_funcionario', y='salario_em_usd', data=pais_frequencia_media.head(5))




# %%
