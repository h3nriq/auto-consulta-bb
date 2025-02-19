import requests
import json
import time
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from dotenv import load_dotenv
import logging
import re

#=========================================================================
# Título: Bot Banco do Brasil
# Autor: Henrique Rohamann
# Ultima Atualização: 19/02/2025
#=========================================================================

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
tipos_pagamento = {
    "FPM": {"ultima_notificacao": None, "credito_benef": None},
    "ROYALTIES": {"ultima_notificacao": None, "credito_benef": None}
}

name_bot = "Bot Banco do Brasil"
title_bot = "Dia de Pagamento"

description_royalties = "Pagamento de ROYALTIES no valor de: R$"
description_fpm = "Pagamento de FPM no valor de: R$"

# Função para verificar pagamentos de um fundo específico
def verificar_pagamento(url, headers, payload, hoje, data_futura):
    try:
        # Passar o parâmetro verify=False para desabilitar a verificação SSL
        response = requests.post(url, headers=headers, json=payload, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            # Verificar o retorno correto de pagamento
            if data and 'quantidadeOcorrencia' in data:
                ocorrencias = data['quantidadeOcorrencia']
                if ocorrencias:
                    tipo_fundo = "ROYALTIES" if payload['codigoFundo'] == 28 else "FPM"
                    
                    # Encontrar o valor recebido
                    credito_benef = ""  # Inicialize com um valor padrão
                    for item in data.get('quantidadeOcorrencia', []):
                        nome_beneficio = item.get('nomeBeneficio', '')
                        if 'CREDITO BENEF.' in nome_beneficio:
                            # Extrair o valor numérico seguido por 'C' usando regex
                            match = re.search(r'(\d{1,3}(?:\.\d{3})*,\d{2}C)', nome_beneficio)
                            if match:
                                credito_benef = match.group(1)
                                break  # Saia do loop assim que encontrar
                    logging.info(f"Valor encontrado de {credito_benef}")

                    # Verificar se já notificou nas últimas 24h ou se o valor mudou
                    agora = datetime.now()
                    ultima_vez = tipos_pagamento[tipo_fundo]["ultima_notificacao"]
                    ultimo_credito = tipos_pagamento[tipo_fundo]["credito_benef"]

                    if ultima_vez is None or (agora - ultima_vez) > timedelta(hours=24) or credito_benef != ultimo_credito:
                        logging.info(f"Pagamento encontrado para o fundo {tipo_fundo}. Enviando notificação.")
                        logging.info(f'Data Inicial: {hoje}')
                        logging.info(f'Data Futura: {data_futura}')

                        # Enviar notificação no Discord
                        if payload['codigoFundo'] == 28:  # ROYALTIES
                            # Coloca o valor do pagamento junto da descrição
                            description_payment_royalties = f"{description_royalties}{credito_benef}"
                            send_discord(title_bot, description_payment_royalties, name_bot)
                        
                        elif payload['codigoFundo'] == 4:  # FPM
                            # Coloca o valor do pagamento junto da descrição
                            description_payment_fpm = f"{description_fpm}{credito_benef}"
                            send_discord(title_bot, description_payment_fpm, name_bot)

                        # Atualizar a última notificação
                        tipos_pagamento[tipo_fundo] = {"ultima_notificacao": agora, "credito_benef": credito_benef}
                    else:
                        logging.info(f"Já foi notificado para {tipo_fundo} nas últimas 24 horas e o valor não mudou.")
                        logging.info(f'Data Inicial: {hoje}')
                        logging.info(f'Data Futura: {data_futura}')
                    
                    return True
            logging.info(f"Sem pagamento para o fundo {payload['codigoFundo']}.")
            logging.info(f'Data Inicial: {hoje}')
            logging.info(f'Data Futura: {data_futura}')
        else:
            logging.info(f'Data Inicial: {hoje}')
            logging.info(f'Data Futura: {data_futura}')
            logging.error(f"Erro ao consultar fundo {payload['codigoFundo']}: {response.status_code}")
    except Exception as e:
        logging.info(f'Data Inicial: {hoje}')
        logging.info(f'Data Futura: {data_futura}')
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

    while True:
        # Definindo o intervalo de datas (hoje até 3 dias à frente) no formato DD.MM.YYYY
        hoje = datetime.today().strftime('%d.%m.%Y')
        data_futura = (datetime.today() + timedelta(days=3)).strftime('%d.%m.%Y')
        
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
        
        # Verificar cada pagamento
        for payload in payloads:
            verificar_pagamento(url, headers, payload, hoje, data_futura)
        
        # Aguardar 2 minutos antes de repetir
        logging.info("Aguardando 2 minutos para próxima verificação...")
        time.sleep(120)

# Executar o sistema
if __name__ == "__main__":
    executar_verificacao()