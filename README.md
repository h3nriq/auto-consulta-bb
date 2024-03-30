# Bot verifica pagamentos 

Objetivo do bot é ser simples, mas funcional, aqui não foi aplicado boas práticas :)

#### Tem opções para buscar os seguintes fundos:
- FPM
- Royalties de petróelo da ANP

#### Fluxo: 
> Webscrapping no site do Banco do Brasil, procurando um município exemplo, na data de HOJE 
> Caso o município TENHA recebido o fundo, envia mensagem no discord (configure o seu)
> Caso NÃO TENHA recebido não faz nada :)

#### Bibliotecas utilizadas:
- datetime
- selenium
- discord_webhook
- dotenv
- os
- time