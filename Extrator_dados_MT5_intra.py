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

    timeframes = ["H1", "M30", "M15", "M10"]

    # Crie um arquivo Excel antes do loop de timeframes
    writer = pd.ExcelWriter(nomedoarquivo)

    for ativo in ativos:
        for timeframe in timeframes:
            try:
                calcular_resultados_por_timeframe(ativo, dataini, writer, timeframe)
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao extrair dados para {ativo} ({timeframe}): {str(e)}")

    # Feche o arquivo Excel após o loop de timeframes
    writer.close()

    messagebox.showinfo("Concluído", "Extração de dados concluída. O arquivo foi salvo no Desktop.")

def calcular_resultados_por_timeframe(ativo, dataini, writer, timeframe):
    timeframe_enum = eval("mt5.TIMEFRAME_" + timeframe)

    candles = mt5.copy_rates_range(ativo, timeframe_enum, dataini, datetime.today())
    df_candles = pd.DataFrame(candles)

    df_candles["time"] = pd.to_datetime(df_candles["time"], unit='s')

    df_candles["data"] = df_candles["time"].dt.date
    df_candles["hora"] = df_candles["time"].dt.time

    dataini = df_candles["time"].iloc[0]

    df_candles["Timeframe"] = timeframe

    df_candles["resuValor"] = (df_candles["close"] - df_candles["open"])
    df_candles["resuPorc"] = (((df_candles["close"] - df_candles["open"]) / df_candles["open"]) * 100)
    df_candles["low"] = df_candles["low"]
    df_candles["VarMin"] = (((df_candles["low"] - df_candles["open"]) / df_candles["open"]) * 100)
    df_candles["ResuHolder"] = (df_candles["close"].iloc[-1] - df_candles["open"].iloc[0])/df_candles["open"].iloc[0]
  

    df_candles.drop(["high", "tick_volume", "spread", "real_volume"], axis=1, inplace=True)

    # Adicione cada DataFrame como uma planilha separada no arquivo Excel
    df_candles.to_excel(writer, sheet_name=f"{timeframe}", index=False)

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
