import os
import time
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    service_chrome = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_chrome, options=options)
    return driver

def open_site_and_configure_search(driver, city, uf, fundo, today_formatted, three_days_ahead):
    try:
        SITE_MAP = site_map()
        driver.get(site_link)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, SITE_MAP["inputs"]["busca_municipio"]["xpath"])))
        driver.find_element(By.XPATH, SITE_MAP["inputs"]["busca_municipio"]["xpath"]).send_keys(city)
        driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar"]["xpath"]).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "formulario:comboBeneficiario")))
        Select(driver.find_element(By.ID, "formulario:comboBeneficiario")).select_by_visible_text(f"{city} - {uf}")
        driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_inicial"]["xpath"]).send_keys(today_formatted)
        driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_final"]["xpath"]).send_keys(three_days_ahead)
        Select(driver.find_element(By.ID, "formulario:comboFundo")).select_by_visible_text(fundo)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"])))
        driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"]).click()
    except Exception as e:
        logging.error(f"Erro ao procurar elemento na página, no tipo {fundo}: {e}")
        if 'driver' in locals():  # Verifica se o 'driver' foi criado
            driver.quit()

def check_and_notify(driver, title, description, name):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, site_map()["span"]["credito_beneficiario"]["xpath"])))
        payment = driver.find_element(By.XPATH, site_map()["span"]["credito_beneficiario"]["xpath"]).text
        send_discord(title, description, name)
        logging.info(f"Valor de {name}: R$ {payment}")
        driver.quit()
        return True
    except NoSuchElementException:
        return False

def check_notification(tipo, today_formatted, three_days_ahead):
    try:
        logging.info(f"Verificando notificação para {tipo}: Notificado em {notifications[tipo]}, Hoje é {today_formatted}")
        if notifications[tipo] != today_formatted:
            driver = config_webdriver()
            if tipo == "FPM":
                logging.info("Procurando FPM")
                open_site_and_configure_search(driver, "TEFE", "AM", "FPM - FUNDO DE PARTICIPACAO", today_formatted, three_days_ahead)
                if check_and_notify(driver, "Dia de Pagamento", "$$$$ FPM $$$$", "Bot Municipal"):
                    notifications[tipo] = today_formatted
                    logging.info("Notificou FPM")
            elif tipo == "ROYALTIES":
                logging.info("Procurando ROYALTIES")
                open_site_and_configure_search(driver, "TEFE", "AM", "ANP - ROYALTIES DA ANP", today_formatted, three_days_ahead)
                if check_and_notify(driver, "Dia de Pagamento", "Psiu, psiu, olha o royalties", "Bot ANP"):
                    notifications[tipo] = today_formatted
                    logging.info("Notificou Royalties")
        else:
            logging.info(f"Já notificou hoje: {notifications[tipo]}")
    except Exception as e:
        logging.error(f"Erro ao verificar notificação para {tipo}: {e}")
        if 'driver' in locals():  # Verifica se o 'driver' foi criado
            driver.quit()

while True:
    today_formatted = datetime.now().strftime('%d/%m/%Y')
    three_days_ahead = (datetime.now() + timedelta(days=3)).strftime('%d/%m/%Y')
    logging.info(f"Procurando hoje: {today_formatted}")
    logging.info(f"Procurando +3 dias: {three_days_ahead}")
    # check_notification("FPM", today_formatted, three_days_ahead)
    time.sleep(5)  
    check_notification("ROYALTIES", today_formatted, three_days_ahead)
    logging.info("Aguardando 2 minutos")
    time.sleep(120)  # Espera 2 minutos antes da próxima iteração
