# Bot verifica pagamentos 

Objetivo do bot é ser simples, mas funcional, aqui não foi aplicado boas práticas :)

#### Tem opções para buscar os seguintes fundos:
- FPM
- Royalties de petróelo da ANP

#### Fluxo: 
- Consulta API do Banco do Brasil para buscar fundos* 
- Caso o município TENHA recebido o fundo, envia mensagem no discord (configure o seu)
- Caso NÃO TENHA recebido não faz nada :)

  
  *antigamente utilizava webscrapping, por que a API não estava funcionando. confira bot_old.

#### Bibliotecas utilizadas:
- requests
- json
- time
- datetime
- discord_webhook
- os
- dotenv
- logging
- re
