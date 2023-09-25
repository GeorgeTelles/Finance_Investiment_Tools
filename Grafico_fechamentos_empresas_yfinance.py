"""
Esse codigo pega os dados de fechamento de determinada empresa desde o seu inicio e plota em um grafico.
no caso atual ele plota o grafico do Ibovespa

By: George Telles
+55 11 93290-7425
"""

#Importando as Bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf
yf.pdr_override()

#Obtendo os dados do mercado
ibov = web.get_data_yahoo('^BVSP')
ibov["Close"].plot(figsize=(22,8))

plt.show()

