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

# Definir o índice do DataFrame
tabela = tabela.set_index("Papel")

# Exibir o DataFrame
print(tabela)

# Fechar o navegador
driver.quit()
