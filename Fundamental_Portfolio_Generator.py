from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from io import StringIO
import time

# Configurar o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.fundamentus.com.br/resultado.php")

# Localizar a tabela na página
local_tabela = "/html/body/div[1]/div[2]/table"
tabela_elemento = driver.find_element("xpath", local_tabela)

# Obter o HTML da tabela
html_tabela = tabela_elemento.get_attribute("outerHTML")

# Ler o HTML da tabela usando StringIO
tabela = pd.read_html(StringIO(html_tabela), thousands=".", decimal=",")[0]

# Configurar o DataFrame
tabela = tabela.set_index("Papel")
tabela = tabela[["Cotação", "EV/EBIT", "ROIC", "Liq.2meses"]]

# Limpar e converter os dados
tabela["ROIC"] = tabela["ROIC"].str.replace("%", "")
tabela["ROIC"] = tabela["ROIC"].str.replace(".", "")
tabela["ROIC"] = tabela["ROIC"].str.replace(",", ".")
tabela["ROIC"] = tabela["ROIC"].astype(float)

# Filtrar os dados
tabela = tabela[tabela["Liq.2meses"] > 1000000]
tabela = tabela[tabela["EV/EBIT"] > 0]
tabela = tabela[tabela["ROIC"] > 0]

# Calcular rankings
tabela["ranking_ev_ebit"] = tabela["EV/EBIT"].rank(ascending=True)
tabela["ranking_roic"] = tabela["ROIC"].rank(ascending=False)
tabela["ranking_final"] = tabela["ranking_ev_ebit"] + tabela["ranking_roic"]

# Ordenar e selecionar as top 10
tabela = tabela.sort_values("ranking_final")
tabela = tabela.head(10)

# Exibir o DataFrame
print(tabela)

# Fechar o navegador
driver.quit()
