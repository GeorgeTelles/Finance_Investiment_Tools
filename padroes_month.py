import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

# Inicializar a conexão
mt5.initialize()

# Lista de ativos
#ativos = ["YDUQ3"]

df_empresas = pd.read_excel('acoesfiltradas.xlsx', header=0, usecols="A")
ativos = df_empresas['Codigo'].tolist()

# Definir tradução de meses
traducao_meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

# Inicializar listas globais
empresas_globais = []
meses_globais = []
resultados_globais = []

for ativo in ativos:
    try:
        candles = mt5.copy_rates_range(ativo, mt5.TIMEFRAME_MN1, datetime(2018, 1, 1), datetime.today())
        rates_frame = pd.DataFrame(candles)
        if 'time' not in rates_frame.columns:
            print(f"Não foi possível encontrar dados para o ativo {ativo}.")
            continue  # Pular para o próximo ativo se não houver dados
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame['Mes'] = rates_frame['time'].dt.month
        rates_frame['Variacao_Porcentagem'] = ((rates_frame['close'] - rates_frame['open']) / rates_frame['open']) * 100
        grupo_mes = rates_frame.groupby('Mes')['Variacao_Porcentagem'].sum()
        group_data_filtrado = pd.DataFrame()

        # Inicializar listas temporárias para cada ativo
        empresas_temp = []
        meses_temp = []
        resultados_temp = []

        for month, group_index in rates_frame.groupby('Mes').groups.items():
            group_data = rates_frame.loc[group_index]

            if any(group_data['Variacao_Porcentagem'] < -2):
                #print(f"Pulando o mês {traducao_meses[month]} para a empresa {ativo} devido à variação negativa.")
                continue

            group_data_filtrado = pd.concat([group_data_filtrado, group_data])

        # Cria o grupo considerando apenas os dados filtrados
        grupo_mes_filtrado = group_data_filtrado.groupby('Mes')['Variacao_Porcentagem'].sum()

        # Loop sobre o grupo filtrado
        for mes, resultado in zip(grupo_mes_filtrado.index, grupo_mes_filtrado):
            mes_traduzido = traducao_meses[mes]
            resultado_formatado = "{:.2f}".format(resultado)  # Formatação com duas casas decimais

            if resultado > 80:
                empresas_temp.append(ativo)
                meses_temp.append(mes_traduzido)
                resultados_temp.append(resultado_formatado)

        # Estender as listas globais com as listas temporárias
        empresas_globais.extend(empresas_temp)
        meses_globais.extend(meses_temp)
        resultados_globais.extend(resultados_temp)

    except Exception as e:
        print(f"Erro ao processar {ativo}: {e}")

# Criação do DataFrame com as listas globais
df_resultados = pd.DataFrame({
    'Empresa': empresas_globais,
    'Mes': meses_globais,
    'Resultado': resultados_globais
})

# Restante do código para exportar para o Excel
script_directory = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(script_directory, "resultados_mensais.xlsx")
df_resultados.to_excel(excel_file_path, index=False)
print(f"Resultados exportados para {excel_file_path}")
