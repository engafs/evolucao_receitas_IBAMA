import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange


def grafico_barra(dados: pd.DataFrame, coluna: str,
                  qt_barra: int, titulo: str) -> None:
    """Função para geração dos gráficos de barras de acordo com a coluna
       desejada, utilizando a contagem de cada valor da coluna.

       :param dados: Dados a serem utilizados para geração do gráfico
       :type dados: pd.DataFrame
       :param coluna: Nome da coluna para contagem dos valores dela
       :type coluna: str
       :param qt_barra: Quantidade de barras a serem exibidas no gráfico
       :type qt_barra: str
       :param titulo: Nome do título do gráfico de barra
       :type titulo: str
    """
    plt.figure(figsize=(15, 5))
    if qt_barra >= 10:
        dados.value_counts(coluna)[:qt_barra].sort_values().plot(
            kind='barh', color=plt.cm.Set1(arange(qt_barra-1, -1, -1)))
        plt.xticks(fontsize=20, rotation=0)
        plt.xlabel('Contagem', fontdict={'fontsize': 20})
        plt.yticks(fontsize=15)
    else:
        dados.value_counts(coluna)[:qt_barra].plot(
            kind='bar', color=plt.cm.Set2(arange(qt_barra)))
        plt.xticks(rotation=0, fontsize=20)
        plt.ylabel('Contagem', fontdict={'fontsize': 20})
        plt.yticks(fontsize=20)
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.show()
    return None


def grafico_barra_colunas(dados: pd.DataFrame, col1: str,
                          col2: str, qt_barra: int,
                          titulo: str) -> None:
    """Função para geração dos gráficos de barras de acordo com as colunas
       desejadas.

       :param dados: Dados a serem utilizados para geração do gráfico
       :type dados: pd.DataFrame
       :param col1: Nome da primeira coluna para contagem dos valores dela
       :type coluna: str
       :param col2: Nome da segunda coluna para contagem dos valores dela
       :type coluna: str
       :param qt_barra: Quantidade de barras a serem exibidas no gráfico
       :type qt_barra: str
       :param titulo: Nome do título do gráfico de barra
       :type titulo: str
    """
    plt.figure(figsize=(15, 5))
    if qt_barra >= 10:
        plt.barh(dados[col1][:qt_barra], dados[col2][:qt_barra])
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
    else:
        plt.bar(dados[col1][:qt_barra], dados[col2][:qt_barra])
        plt.xticks(rotation=20)
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.show()
    return None


df: pd.DataFrame = pd.read_csv('receitas_arrecadadas.csv', sep=';')
df = df.loc[df["Ano"] <= 2023]
df['Valor (R$)'] = df['Valor (R$)'].apply(
    lambda x: float(x.replace(".", "").replace(",", ".")))
df['Valor (R$)'] = df['Valor (R$)'].astype(float)

df_total_receita: pd.DataFrame = df.groupby(
    'Descrição Receita', as_index=False)['Valor (R$)'].agg(
        ['sum', 'count']).sort_values(by='sum', ascending=False)

df_total_ano: pd.DataFrame = df.groupby(
    'Ano', as_index=False)['Valor (R$)'].agg('sum')

df_tcfa: pd.DataFrame = df.loc[
    df["Descrição Receita"] == 'Taxa de controle e fiscalização ambiental']

grafico_barra(
    df, 'Descrição Receita',
    10, 'Os 10 tipos de receitas mais contabilizadas pelo IBAMA (1996-2023)')

grafico_barra_colunas(df_total_receita, 'Descrição Receita',
                      'sum', 10,
                      '10 receitas mais arrecadadas pelo IBAMA (1996-2023)')

plt.figure(figsize=(15, 5))
plt.plot(df_total_ano['Ano'], df_total_ano['Valor (R$)'],
         marker='o', linestyle='--', color='b')
plt.xlabel('Anos', fontsize=15)
plt.ylabel('Valores (100.000.000 R$)', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Quantidade de receita arrecadada pelo IBAMA (1996-2023)',
          fontdict={'fontsize': 20, 'fontweight': 'bold'})
plt.grid(True)
plt.show()

plt.figure(figsize=(15, 5))
plt.plot(df_total_ano['Ano'], df_total_ano['Valor (R$)'],
         marker='o', linestyle='--', color='b', label='Total receitas')
plt.plot(df_tcfa['Ano'], df_tcfa['Valor (R$)'],
         marker='o', linestyle='--', color='green', label='TCFA')
plt.xlabel('Anos', fontsize=15)
plt.ylabel('Valores (100.000.000 R$)', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Comparação entre TCFA e total arrecadado pelo IBAMA (1996-2023)',
          fontdict={'fontsize': 20, 'fontweight': 'bold'})
plt.grid(True)
plt.legend(loc="upper left")
plt.show()

plt.figure(figsize=(10, 5))
df_total_ano['Valor (R$)'].plot(kind='box')
plt.show()
