# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Instalação de utilitários necessários e libs para o Chrome
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Adiciona o repositório do Google Chrome à lista de fontes e instala o Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Instala uma versão específica do ChromeDriver
RUN CHROMEDRIVER_VERSION=123.0.6312.86 && \
    wget -N https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chrome-headless-shell-linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    mv -f ~/chromedriver /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver && \
    rm ~/chromedriver_linux64.zip

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do Python a partir do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para executar o bot
CMD ["python", "bot.py"]
