"""
Esse codigo extrai os dados diarios (D1) de determinada empresa, adiciona uma coluna de dia da semana para me dizer se
aquela data é segunda, terça e etc... e salva em uma planilha

By: George Telles
+55 11 93290-7425
"""

import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

def extrair_dados():
    mt5.initialize()

    ativos = ativos_entry.get().split(',')
    nome_do_arquivo = nome_entry.get()
    dataini_str = dataini_entry.get()

    if not ativos or not nome_do_arquivo or not dataini_str:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    dataini = datetime.strptime(dataini_str, "%Y-%m-%d")

    nomedoarquivo = os.path.join(os.path.expanduser("~"), "Desktop", f"{nome_do_arquivo}.xlsx")

    # Crie um arquivo Excel antes do loop de ativos
    writer = pd.ExcelWriter(nomedoarquivo)

    for ativo in ativos:
        try:
            calcular_resultados_diarios(ativo, dataini, writer)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao extrair dados para {ativo}: {str(e)}")

    # Feche o arquivo Excel após o loop de ativos
    writer.close()

    messagebox.showinfo("Concluído", "Extração de dados concluída. O arquivo foi salvo no Desktop.")

def calcular_resultados_diarios(ativo, dataini, writer):
    timeframe_enum = mt5.TIMEFRAME_D1

    candles = mt5.copy_rates_range(ativo, timeframe_enum, dataini, datetime.today())
    df_candles = pd.DataFrame(candles)

    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    df_candles["data"] = df_candles["time"].dt.date
    df_candles["hora"] = df_candles["time"].dt.time

    dataini = df_candles["time"].iloc[0]

    df_candles["resuValor"] = (df_candles["close"] - df_candles["open"])
    df_candles["resuPorc"] = (((df_candles["close"] - df_candles["open"]) / df_candles["open"]) * 100)
    df_candles["low"] = df_candles["low"]
    df_candles["VarMin"] = (((df_candles["low"] - df_candles["open"]) / df_candles["open"]) * 100)
    df_candles["ResuHolder"] = (df_candles["close"].iloc[-1] - df_candles["open"].iloc[0])/df_candles["open"].iloc[0]
  

    df_candles.drop(["high", "tick_volume", "spread", "real_volume"], axis=1, inplace=True)

    # Adicionar uma coluna para o dia da semana
    df_candles["dia_da_semana"] = df_candles["time"].dt.strftime('%A')

    # Adicione o DataFrame como uma planilha no arquivo Excel
    df_candles.to_excel(writer, sheet_name=f"{ativo}", index=False)

root = tk.Tk()
root.title("Extrair Dados Financeiros")

frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0)

ativos_label = ttk.Label(frame, text="Ativos (separe por vírgula):")
ativos_label.grid(column=0, row=0, sticky="W")

ativos_entry = ttk.Entry(frame, width=30)
ativos_entry.grid(column=1, row=0)

dataini_label = ttk.Label(frame, text="Data Inicial (AAAA-MM-DD):")
dataini_label.grid(column=0, row=1, sticky="W")

dataini_entry = ttk.Entry(frame, width=30)
dataini_entry.grid(column=1, row=1)

nome_label = ttk.Label(frame, text="Nome do arquivo:")
nome_label.grid(column=0, row=2, sticky="W")

nome_entry = ttk.Entry(frame, width=30)
nome_entry.grid(column=1, row=2)

extrair_button = ttk.Button(frame, text="Extrair Dados", command=extrair_dados)
extrair_button.grid(column=0, row=3, columnspan=2)

root.mainloop()
