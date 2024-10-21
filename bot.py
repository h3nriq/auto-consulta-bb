import requests
import json
import time
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
import logging

# Carregar variáveis de ambiente
load_dotenv()
discord_wh = os.getenv('WEBHOOK_DISCORD')

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para enviar notificações no Discord
def send_discord(title, description, name):
    webhook = DiscordWebhook(url=discord_wh)
    embed = DiscordEmbed(title=title, description=description, color='03b2f8')
    embed.set_author(name=name)
    webhook.add_embed(embed)
    webhook.execute()

# Títulos e descrições das notificações
notifications = {"FPM": None, "ROYALTIES": None}
title_royalties = "Dia de Pagamento"
description_royalties = "Psiu, psiu, olha o royalties"
name_royalties = "Bot ANP"
title_fpm = "Dia de Pagamento"
description_fpm = "$$ FPM $$"
name_fpm = "Bot FPM"

# Função para verificar pagamentos de um fundo específico
def verificar_pagamento(url, headers, payload):
    try:
        # Passar o parâmetro verify=False para desabilitar a verificação SSL
        response = requests.post(url, headers=headers, json=payload, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            # Aqui você deve ajustar a lógica para verificar o retorno correto de pagamento
            if data and 'quantidadeOcorrencia' in data:
                ocorrencias = data['quantidadeOcorrencia']
                if ocorrencias:
                    logging.info(f"Pagamento encontrado para o fundo {payload['codigoFundo']}:")
                    
                    # Enviar notificação no Discord
                    if payload['codigoFundo'] == 28:  # ROYALTIES
                        send_discord(title_royalties, description_royalties, name_royalties)
                    elif payload['codigoFundo'] == 4:  # FPM
                        send_discord(title_fpm, description_fpm, name_fpm)

                    return True
            logging.info(f"Sem pagamento para o fundo {payload['codigoFundo']}.")
        else:
            logging.error(f"Erro ao consultar fundo {payload['codigoFundo']}: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro durante a requisição: {e}")
    return False

# Função principal para fazer requests e verificar pagamentos
def executar_verificacao():
    url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"
    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Origin': 'https://demonstrativos.apps.bb.com.br',
        'Referer': 'https://demonstrativos.apps.bb.com.br/'
    }

    # Definindo o intervalo de datas (hoje até 3 dias a frente) no formato DD.MM.YYYY
    hoje = datetime.today().strftime('%d.%m.%Y')
    data_futura = (datetime.today() + timedelta(days=3)).strftime('%d.%m.%Y')
    logging.info(f'Data Inicial: {hoje}')
    logging.info(f'Data Futura: {data_futura}')
    # Definindo os dois payloads
    payloads = [
        {
            "codigoBeneficiario": 4636,
            "codigoFundo": 28,  # ROYALTIES
            "dataInicio": hoje,
            "dataFim": data_futura
        },
        {
            "codigoBeneficiario": 4636,
            "codigoFundo": 4,   # FPM
            "dataInicio": hoje,
            "dataFim": data_futura
        }
    ]

    while True:
        for payload in payloads:
            verificar_pagamento(url, headers, payload)
        
        # Aguardar 2 minutos antes de repetir
        print("Aguardando 2 minutos...")
        time.sleep(120)

# Executar o sistema
if __name__ == "__main__":
    executar_verificacao()