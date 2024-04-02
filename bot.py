import os
import time
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.common.exceptions import NoSuchElementException

from mapeamentos.map_site import *

# Configurar env
load_dotenv()
discord_wh = os.getenv('WEBHOOK_DISCORD')

def send_discord():
    webhook = DiscordWebhook(url=discord_wh)
    embed = DiscordEmbed(title='Dia de Pagamento', description='$$$$ FPM $$$$', color='03b2f8')
    embed.set_author(name='Bot Municipal')

    webhook.add_embed(embed)
    webhook.execute(embed)

def abrir_site(driver, url):
    driver.get(url)

def extrair_dados_fpm(driver):
    city='TEFE'
    uf='AM'
    fundo='FPM - FUNDO DE PARTICIPACAO'
    SITE_MAP = site_map()

    # PROCURAE MUNICÍPIO
    input_element = driver.find_element("xpath", SITE_MAP["inputs"]["busca_municipio"]["xpath"])
    input_element.send_keys(city)

    # CONTINUAE
    driver.find_element("xpath", SITE_MAP["buttons"]["continuar"]["xpath"]).click()    
    time.sleep(1)

    # SELECIONAR MUNICÍPIO CORRETO
    sel = Select(driver.find_element("id", "formulario:comboBeneficiario"))
    sel.select_by_visible_text(city+ ' - '+uf)

    # COLOCAR DATA DE HOJE PARA DATA INICIAL 
    input_element = driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_inicial"]["xpath"])
    input_element.send_keys(today_formatted)

    # COLOCAR DATA DE HOJE PARA DATA INICIAL 
    input_element = driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_final"]["xpath"])
    input_element.send_keys(today_formatted)

    # SELECIONA O FUNDO    
    sel = Select(driver.find_element("id", "formulario:comboFundo"))
    sel.select_by_visible_text(fundo)

    # BUSCAR EXTRATO HOJE
    driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"]).click()
    time.sleep(2)

    # TENTAR IDENTIFICAR PAGAMENTO
    try:
        # Tenta encontrar o elemento na página e extrair seu texto
        driver.find_element(By.XPATH, SITE_MAP["span"]["credito_beneficiario"]["xpath"]).text
        # Formata o texto extraído, mantendo apenas os números
        finded = 1
    except NoSuchElementException:
        # Se o elemento não for encontrado, atribui 0 à variável
        finded = 0

    # SE NÃO TIVER PAGAMENTO PASSA
    if finded == 0:
        pass

    # SE TIVER PAGAMENTO, ENVIA MENSAGEM PARA O DISCORD
    else: 
        send_discord()
        pass
    pass

def config_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # service_chrome = Service(ChromeDriverManager().install())
    service_chrome = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service_chrome, options=options)
    # driver.set_window_size(800, 700)

    return driver

def extrair_dados_royalties(driver):
    city='TEFE'
    uf='AM'
    fundo='ANP - ROYALTIES DA ANP'
    SITE_MAP = site_map()

    # PROCURAE MUNICÍPIO
    input_element = driver.find_element("xpath", SITE_MAP["inputs"]["busca_municipio"]["xpath"])
    input_element.send_keys(city)

    # CONTINUAE
    driver.find_element("xpath", SITE_MAP["buttons"]["continuar"]["xpath"]).click()    
    time.sleep(1)

    # SELECIONAR MUNICÍPIO CORRETO
    sel = Select(driver.find_element("id", "formulario:comboBeneficiario"))
    sel.select_by_visible_text(city+ ' - '+uf)

    # COLOCAR DATA DE HOJE PARA DATA INICIAL 
    input_element = driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_inicial"]["xpath"])
    input_element.send_keys(today_formatted)

    # COLOCAR DATA DE HOJE PARA DATA INICIAL 
    input_element = driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_final"]["xpath"])
    input_element.send_keys(today_formatted)

    # SELECIONA O FUNDO    
    sel = Select(driver.find_element("id", "formulario:comboFundo"))
    sel.select_by_visible_text(fundo)

    # BUSCAR EXTRATO HOJE
    driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"]).click()
    time.sleep(2)

    # TENTAR IDENTIFICAR PAGAMENTO
    try:
        # Tenta encontrar o elemento na página e extrair seu texto
        driver.find_element(By.XPATH, SITE_MAP["span"]["credito_beneficiario"]["xpath"]).text
        # Formata o texto extraído, mantendo apenas os números
        finded = 1
    except NoSuchElementException:
        # Se o elemento não for encontrado, atribui 0 à variável
        finded = 0

    # SE NÃO TIVER PAGAMENTO PASSA
    if finded == 0:
        pass

    # SE TIVER PAGAMENTO, ENVIA MENSAGEM PARA O DISCORD
    else: 
        send_discord()
        pass
    pass

while True:
    # Obter a data atual
    today = datetime.now()

    # Formatar a data (dd/MM/yyyy)
    today_formatted = today.strftime('%d/%m/%Y')
    
    # Procurar se recebeu FPM hoje
    driver = config_webdriver()
    abrir_site(driver, 'https://www42.bb.com.br/portalbb/daf/beneficiario,802,4647,4652,0,1.bbx')
    extrair_dados_fpm(driver)
    driver.quit()
    
    time.sleep(2)

    # Procurar se recebeu Royalties hoje
    driver = config_webdriver()
    abrir_site(driver, 'https://www42.bb.com.br/portalbb/daf/beneficiario,802,4647,4652,0,1.bbx')
    extrair_dados_royalties(driver)
    driver.quit()

    time.sleep(120)