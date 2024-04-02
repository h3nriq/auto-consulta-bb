# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Instalação de utilitários necessários, wget para downloads e unzip para extrair arquivos
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Adiciona o repositório do Google Chrome à lista de fontes e instala o Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Instala a versão mais recente do ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod 0755 /usr/local/bin/chromedriver

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do Python a partir do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para executar o bot
CMD ["python", "bot.py"]
