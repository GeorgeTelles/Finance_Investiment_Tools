"""
Esse codigo faz a extração de dados de determinada empresa na bolsa de valores
pelo Yahoo Finance. depois calcula o rendimento mensal e exibe no terminal.

By: George Telles
+55 11 93290-7425
"""

import pandas as pd
import yfinance as yf

dados_empresas = yf.download("WEGE3.SA", start = "2018-01-01", end = "2023-08-01",)

cotacao_ajustados = dados_empresas["Adj Close"]

retorno_mensal = cotacao_ajustados.resample("M").last()

retorno_mensal = cotacao_ajustados.pct_change().dropna()

print(retorno_mensal)
