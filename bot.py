import os
import time
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from mapeamentos.map_site import *

# Configurar env
load_dotenv()
discord_wh = os.getenv('WEBHOOK_DISCORD')
notifications = {"FPM": None, "ROYALTIES": None}
site_link= 'https://www42.bb.com.br/portalbb/daf/beneficiario,802,4647,4652,0,1.bbx'

def send_discord(title, description, name):
    webhook = DiscordWebhook(url=discord_wh)
    embed = DiscordEmbed(title=title, description=description, color='03b2f8')
    embed.set_author(name=name)
    webhook.add_embed(embed)
    webhook.execute()

def config_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service_chrome = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_chrome, options=options)
    return driver

def open_site_and_configure_search(driver, city, uf, fundo, today_formatted):
    SITE_MAP = site_map()
    driver.get(site_link)
    driver.find_element("xpath", SITE_MAP["inputs"]["busca_municipio"]["xpath"]).send_keys(city)
    driver.find_element("xpath", SITE_MAP["buttons"]["continuar"]["xpath"]).click()    
    time.sleep(1)
    Select(driver.find_element("id", "formulario:comboBeneficiario")).select_by_visible_text(f"{city} - {uf}")
    driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_inicial"]["xpath"]).send_keys(today_formatted)
    driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_final"]["xpath"]).send_keys(today_formatted)
    Select(driver.find_element("id", "formulario:comboFundo")).select_by_visible_text(fundo)
    driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"]).click()
    time.sleep(2)

def check_and_notify(driver, title, description, name):
    try:
        driver.find_element(By.XPATH, site_map()["span"]["credito_beneficiario"]["xpath"]).text
        send_discord(title, description, name)
        return True
    except NoSuchElementException:
        return False

def check_notification(tipo, today_formatted):
    if notifications[tipo] != today_formatted:
        driver = config_webdriver()
        if tipo == "FPM":
            open_site_and_configure_search(driver, "TEFE", "AM", "FPM - FUNDO DE PARTICIPACAO", today_formatted)
            if check_and_notify(driver, "Dia de Pagamento", "$$$$ FPM $$$$", "Bot Municipal"):
                notifications[tipo] = today_formatted
        elif tipo == "ROYALTIES":
            open_site_and_configure_search(driver, "TEFE", "AM", "ANP - ROYALTIES DA ANP", today_formatted)
            if check_and_notify(driver, "Dia de Pagamento", "Psiu, psiu, olha o royalties", "Bot ANP"):
                notifications[tipo] = today_formatted
        driver.quit()
  
while True:
    today_formatted = datetime.now().strftime('%d/%m/%Y')
    check_notification("FPM", today_formatted)
    time.sleep(2)  
    check_notification("ROYALTIES", today_formatted)
    time.sleep(120)  # Espera 2 minutos antes da próxima iteração