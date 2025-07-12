#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Fonte de dados: https://dados.antt.gov.br/dataset/acidentes-quilometro-rodovias/resource/6a66aba2-1a3c-414b-9ea0-f21b2a6e0396

#Acidentes por Km na rodovia federal RIOSP


# In[1]:


import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')


# In[49]:


dados = pd.read_csv('demostrativo_acidentes_riosp.csv', encoding = 'latin1')

coluna_para_dividir = dados.columns[0]
#Divisão dos dados em colunas via delimitador ;
dados[['Concessionaria','Data', 'Km', 'Trecho']] = dados[coluna_para_dividir].str.split(';', expand=True)
#Exclusão da coluna inicial
dados.drop(columns=[coluna_para_dividir], inplace=True)

#convertendo a coluna data para o tipo data
dados['Data'] = pd.to_datetime(dados['Data'], format='%d/%m/%Y', errors='coerce')

dados['Km'] = dados['Km'].str.replace('.', '', regex=False).astype(float)

#Criando as colunas "ano", "mês", "dia da semana" e "trimestre"
dados['Ano'] = dados['Data'].dt.year
dados = dados[dados['Ano'] < 2025]
dados['Ano'] = dados['Ano'].astype(str) 
dados['Mes'] = dados['Data'].dt.month
dados['Dia_da_semana'] = dados['Data'].dt.day_name().astype(str) 
dados['Trimestre'] = dados['Data'].dt.quarter.astype(str)


# In[50]:


#Função para criação da coluna "Estação"    
def get_estacao_hemisferio_sul(data):
    if pd.isna(data): # Lida com valores nulos (NaT) na coluna Data
        return None

    mes = data.month
    dia = data.day

    # Verão: 21/12 até 20/03
    if (mes == 12 and dia >= 21) or        (mes >= 1 and mes <= 2) or        (mes == 3 and dia <= 20):
        return 'Verão'
    # Outono: 21/03 até 20/06
    elif (mes == 3 and dia >= 21) or          (mes >= 4 and mes <= 5) or          (mes == 6 and dia <= 20):
        return 'Outono'
    # Inverno: 21/06 até 22/09
    elif (mes == 6 and dia >= 21) or          (mes >= 7 and mes <= 8) or          (mes == 9 and dia <= 22):
        return 'Inverno'
    # Primavera: 23/09 até 20/12
    elif (mes == 9 and dia >= 23) or          (mes >= 10 and mes <= 11) or          (mes == 12 and dia <= 20):
        return 'Primavera'
    else:
        return None # Caso alguma data não se encaixe (improvável com datas válidas)


# In[51]:


dados['Estacao'] = dados['Data'].apply(get_estacao_hemisferio_sul)


# In[63]:


dados['Km'].mode()[0]
acidentes_estacao = dados.groupby(['Estacao']).size()
acidentes_semana = dados.groupby('Dia_da_semana').size().sort_values(ascending=False)
acidentes_mes = dados.groupby(['Mes']).size().sort_values(ascending=False)
acidentes_estacao_ano = dados.groupby(['Ano', 'Estacao']).size()
acidentes_trecho = dados['Trecho'].value_counts()
acidentes_pordia = dados['Dia_da_semana'].value_counts().loc[
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
]


# In[56]:


#dados['Estacao'].value_counts().sort_index().plot(kind='bar', color='mediumseagreen')
acidentes_estacao_ano.plot(kind='bar', figsize=(10,6), color=['#87CEEB', '#98FB98', '#FFD700','#FF8C00'])
#plt.title("Acidentes por Estação")
plt.xlabel('Ano / Estação')
plt.ylabel("Número de acidentes")
plt.xticks(rotation=90)
#plt.legend(title='Estação')
plt.tight_layout()
plt.show()


# In[57]:


acidentes_porkm = dados['Km'].value_counts().nlargest(5)
acidentes_porkm.plot(kind='bar', color='tomato')
plt.title('Top5 Kms com mais registros de acidentes')
plt.xlabel('Km')
plt.ylabel('Quantidade de Acidentes')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# In[58]:


plt.figure(figsize=(6,4))
acidentes_ano = dados['Ano'].value_counts().sort_index()
plt.plot(acidentes_ano.index, acidentes_ano.values, marker='o', 
         linestyle='-', color='mediumseagreen')
plt.title("Acidentes por Ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade de Acidentes")
plt.tight_layout()
plt.show()


# In[61]:


plt.figure(figsize=(4, 4))
plt.pie(
    acidentes_estacao,
    labels=acidentes_estacao.index,
    autopct='%1.1f%%',
    startangle=60,
    colors=['#87CEEB', '#98FB98', '#FFD700', '#FF8C00'],
    wedgeprops={'edgecolor': 'black'}
)
plt.title("Distribuição de Acidentes por Estação do Ano")
plt.tight_layout()
plt.show()


# In[64]:


acidentes_trecho.plot(kind='barh', color ='steelblue', figsize=(6, 5))
plt.title("Trechos com Maior Número de Acidentes")
plt.xlabel("Quantidade de Acidentes")
plt.ylabel("Trecho")
plt.gca().invert_yaxis()  # Coloca o maior no topo
plt.show()


# In[67]:


plt.figure(figsize=(7,5))
plt.fill_between(acidentes_por_dia.index, acidentes_por_dia.values, color='crimson', alpha=0.6)
plt.title("Acidentes por Dia da Semana")
plt.xlabel("Dia da Semana")
plt.ylabel("Quantidade de Acidentes")
plt.tight_layout()
plt.show()


# In[66]:


acidentes_por_mes = dados['Mes'].value_counts().sort_index()

acidentes_por_mes.plot(kind='bar', color='purple')
plt.title('# Meses mais registros de acidentes')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Acidentes')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# In[ ]:




