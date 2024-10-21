import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from mapeamentos.map_site import *
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# Configurar env
load_dotenv()
discord_wh = os.getenv('WEBHOOK_DISCORD')
notifications = {"FPM": None, "ROYALTIES": None}
site_link= 'https://demonstrativos.apps.bb.com.br/arrecadacao-federal'
city = 'MANACAPURU'
states = 'AM'

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
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--window-size=1920x1080")
    service_chrome = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_chrome, options=options)
    return driver

def open_site_and_configure_search(driver, city, uf, fundo, today_formatted, three_days_ahead):
    wait = WebDriverWait(driver, 10)

    logging.info("Comecar a procura")
    SITE_MAP = site_map()
    driver.get(site_link)
    logging.info("Abriu o link")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, SITE_MAP["inputs"]["busca_municipio"]["xpath"])))
    logging.info("Esperou carregar a página inicial")
    driver.find_element(By.XPATH, SITE_MAP["inputs"]["busca_municipio"]["xpath"]).send_keys(city)
    driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar"]["xpath"]).click()
    logging.info("Entrou na próxima página")
    element = wait.until(EC.element_to_be_clickable((By.XPATH, SITE_MAP["class"]["overlay_municipio"]["xpath"])))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[.//span[contains(@class, 'menu-title') and contains(text(), ' {city} - {uf} ')]]")))
    element.click()
    logging.info("Selecionou o município")
    driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_inicial"]["xpath"]).send_keys(today_formatted)
    driver.find_element(By.XPATH, SITE_MAP["inputs"]["data_final"]["xpath"]).send_keys(three_days_ahead)
    logging.info("Selecionou as datas")
    element = wait.until(EC.element_to_be_clickable((By.XPATH, SITE_MAP["class"]["overlay_fundo"]["xpath"])))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[.//span[contains(@class, 'menu-title') and contains(text(), ' {fundo} ')]]")))
    element.click()
    logging.info("Selecionou o fundo")
    driver.find_element(By.XPATH, SITE_MAP["buttons"]["continuar_page2"]["xpath"]).click()
    logging.info("Continuou para a página de credito")

def check_and_notify(driver, title, description, name):
    try:
        logging.info("Entrou na notificação")

        # Esperar até que a tabela esteja visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table.bb-table"))
        )
        logging.info("Achou payment")

        # Localizar todos os elementos <td> que correspondam ao critério
        valores = driver.find_elements(By.CSS_SELECTOR, "td.bb-cell.bb-cell-align-right[style='color: rgb(0, 0, 255);']")
        
        # Pegar o último valor da lista
        ultimo_valor = valores[-1].text if valores else "Nenhum valor encontrado"
   
        if ultimo_valor == "0,00C" or ultimo_valor == "Nenhum valor encontrado":
            logging.info("Não teve pagamento pra essa data")
            return False
        else: 
            send_discord(title, description, name)
            logging.info("ENVIOU NOTIFICAÇÃO DISCORD")
            logging.info(f"Valor de {name}: R$ {ultimo_valor}")
            return True

    except NoSuchElementException:
        return False
    except TimeoutException:
        logging.info("TimeOut no check_and_notify")
        return False
    except Exception as e:
        logging.info(f"Ocorreu um erro generico: {e}")
        return False
    finally:
        driver.quit()

def check_notification(tipo, today_formatted, three_days_ahead):
    try:
        logging.info(f"Verificando notificação para {tipo}: Notificado em {notifications[tipo]}, Hoje é {today_formatted}")
        if notifications[tipo] != today_formatted:
            driver = config_webdriver()
            if tipo == "FPM":
                logging.info("Procurando FPM")
                open_site_and_configure_search(driver, city, states, "FPM - FUNDO DE PARTICIPACAO", today_formatted, three_days_ahead)
                if check_and_notify(driver, "Dia de Pagamento", "$$$$ FPM $$$$", "Bot Municipal"):
                    notifications[tipo] = today_formatted
                    logging.info("Notificou FPM")
            elif tipo == "ROYALTIES":
                logging.info("Procurando ROYALTIES")
                open_site_and_configure_search(driver, city, states, "ANP - ROYALTIES DA ANP", today_formatted, three_days_ahead)
                if check_and_notify(driver, "Dia de Pagamento", "Psiu, psiu, olha o royalties", "Bot ANP"):
                    notifications[tipo] = today_formatted
                    logging.info("Notificou Royalties")
        else:
            logging.info(f"Já notificou hoje: {notifications[tipo]}")
    except Exception as e:
        logging.error(f"Erro ao verificar notificação para {tipo}: {e}")
        driver.quit()

while True:
    today_formatted = datetime.now().strftime('%d/%m/%Y')
    three_days_ahead = (datetime.now() + timedelta(days=3)).strftime('%d/%m/%Y')
    logging.info(f"Procurando hoje: {today_formatted}")
    logging.info(f"Procurando +3 dias: {three_days_ahead}")
    check_notification("FPM", today_formatted, three_days_ahead)
    time.sleep(5)  
    check_notification("ROYALTIES", today_formatted, three_days_ahead)
    logging.info("Aguardando 2 minutos")
    time.sleep(120)  # Espera 2 minutos antes da próxima iteração